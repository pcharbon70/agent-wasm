use extism::Plugin;
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, ErrorKind, Read, Write};
use std::sync::mpsc;
use std::thread;
use std::time::{Duration, Instant};

const MAX_FRAME_BYTES: usize = 8 * 1024 * 1024;
const MAX_TIMEOUT_MS: u64 = 60_000;
const TIMEOUT_EXIT_STATUS: i32 = 124;
const EXPORTS: [&str; 4] = ["describe", "initialize", "reduce", "migrate"];

#[derive(Deserialize)]
struct Request {
    operation: String,
    wasm_path: String,
    export: String,
    input: String,
    timeout_ms: u64,
}

#[derive(Serialize)]
struct Response {
    ok: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    output: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Diagnostic>,
}

#[derive(Serialize)]
struct Diagnostic {
    code: String,
    message: String,
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut reader = stdin.lock();
    let mut writer = stdout.lock();

    if let Some(frame) = read_frame(&mut reader)? {
        let response = handle_frame(&frame);
        let encoded = serde_json::to_vec(&response).unwrap_or_else(|_| {
            br#"{"ok":false,"error":{"code":"port.response.invalid","message":"response encoding failed"}}"#
                .to_vec()
        });
        write_frame(&mut writer, &encoded)?;
    }

    Ok(())
}

fn read_frame(reader: &mut impl Read) -> io::Result<Option<Vec<u8>>> {
    let mut header = [0_u8; 4];
    match reader.read_exact(&mut header) {
        Ok(()) => {}
        Err(error) if error.kind() == ErrorKind::UnexpectedEof => return Ok(None),
        Err(error) => return Err(error),
    }

    let length = u32::from_be_bytes(header) as usize;
    if length > MAX_FRAME_BYTES {
        return Err(io::Error::new(
            ErrorKind::InvalidData,
            "incoming frame exceeds the worker limit",
        ));
    }

    let mut frame = vec![0_u8; length];
    reader.read_exact(&mut frame)?;
    Ok(Some(frame))
}

fn write_frame(writer: &mut impl Write, frame: &[u8]) -> io::Result<()> {
    let length = u32::try_from(frame.len())
        .map_err(|_| io::Error::new(ErrorKind::InvalidData, "outgoing frame is too large"))?;
    writer.write_all(&length.to_be_bytes())?;
    writer.write_all(frame)?;
    writer.flush()
}

fn handle_frame(frame: &[u8]) -> Response {
    let result = decode_request(frame).and_then(invoke_with_timeout);
    response(result)
}

fn response(result: Result<String, Diagnostic>) -> Response {
    match result {
        Ok(output) => Response {
            ok: true,
            output: Some(output),
            error: None,
        },
        Err(error) => Response {
            ok: false,
            output: None,
            error: Some(error),
        },
    }
}

fn decode_request(frame: &[u8]) -> Result<Request, Diagnostic> {
    let request: Request = serde_json::from_slice(frame)
        .map_err(|error| diagnostic("port.request.invalid", error.to_string()))?;

    if request.operation != "invoke" {
        return Err(diagnostic(
            "port.operation.unsupported",
            "only the invoke operation is supported",
        ));
    }
    if !EXPORTS.contains(&request.export.as_str()) {
        return Err(diagnostic(
            "port.export.unsupported",
            "the requested export is not part of the guest lifecycle",
        ));
    }

    if request.timeout_ms == 0 || request.timeout_ms > MAX_TIMEOUT_MS {
        return Err(diagnostic(
            "port.timeout.invalid",
            format!("timeout_ms must be between 1 and {MAX_TIMEOUT_MS}"),
        ));
    }

    Ok(request)
}

fn invoke_with_timeout(request: Request) -> Result<String, Diagnostic> {
    let timeout = Duration::from_millis(request.timeout_ms);
    let started_at = Instant::now();
    let (sender, receiver) = mpsc::sync_channel(1);

    thread::spawn(move || {
        let _ = sender.send(invoke(request));
    });

    let remaining = timeout.saturating_sub(started_at.elapsed());

    match receiver.recv_timeout(remaining) {
        Ok(result) if started_at.elapsed() <= timeout => result,
        Ok(_late_result) => std::process::exit(TIMEOUT_EXIT_STATUS),
        Err(mpsc::RecvTimeoutError::Timeout) => std::process::exit(TIMEOUT_EXIT_STATUS),
        Err(mpsc::RecvTimeoutError::Disconnected) => Err(diagnostic(
            "port.runner.failed",
            "native invocation thread stopped without a response",
        )),
    }
}

fn invoke(request: Request) -> Result<String, Diagnostic> {
    let wasm = fs::read(&request.wasm_path)
        .map_err(|error| diagnostic("port.guest.unavailable", error.to_string()))?;
    let mut plugin = Plugin::new(wasm, [], false)
        .map_err(|error| diagnostic("extism.instance.invalid", error.to_string()))?;

    if plugin.has_wasi() {
        return Err(diagnostic(
            "extism.instance.wasi_enabled",
            "the bootstrap guest must run without WASI",
        ));
    }
    if !plugin.function_exists(&request.export) {
        return Err(diagnostic(
            "extism.invocation.export_missing",
            "the guest does not expose the requested lifecycle function",
        ));
    }

    plugin
        .call::<&str, String>(&request.export, request.input.as_str())
        .map_err(|error| diagnostic("extism.invocation.failed", error.to_string()))
}

fn diagnostic(code: &str, message: impl Into<String>) -> Diagnostic {
    Diagnostic {
        code: code.to_owned(),
        message: message.into(),
    }
}
