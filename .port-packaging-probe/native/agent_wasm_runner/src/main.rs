use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::io::{self, ErrorKind, Read, Write};

const PROTOCOL_VERSION: u16 = 1;
const MAXIMUM_FRAME_BYTES: usize = 16 * 1024 * 1024;

#[derive(Deserialize)]
struct Request {
    protocol: u16,
    id: String,
    op: String,
}

#[derive(Serialize)]
struct Response {
    id: String,
    ok: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    result: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Value>,
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut input = stdin.lock();
    let mut output = stdout.lock();

    while let Some(frame) = read_frame(&mut input)? {
        let keep_running = handle_frame(&frame, &mut output)?;
        if !keep_running {
            break;
        }
    }

    Ok(())
}

fn handle_frame(frame: &[u8], output: &mut impl Write) -> io::Result<bool> {
    let request: Request = match serde_json::from_slice(frame) {
        Ok(request) => request,
        Err(error) => {
            eprintln!("invalid request: {error}");
            return write_response(
                output,
                Response {
                    id: String::new(),
                    ok: false,
                    result: None,
                    error: Some(json!({"code": "protocol.decode"})),
                },
            )
            .map(|_| true);
        }
    };

    if request.protocol != PROTOCOL_VERSION {
        write_response(
            output,
            Response {
                id: request.id,
                ok: false,
                result: None,
                error: Some(json!({"code": "protocol.incompatible"})),
            },
        )?;
        return Ok(true);
    }

    let (response, keep_running) = match request.op.as_str() {
        "hello" => (
            Response {
                id: request.id,
                ok: true,
                result: Some(json!({
                    "protocol": PROTOCOL_VERSION,
                    "worker_version": env!("CARGO_PKG_VERSION"),
                    "engine": "packaging-probe",
                    "features": ["health"]
                })),
                error: None,
            },
            true,
        ),
        "health" => (
            Response {
                id: request.id,
                ok: true,
                result: Some(json!({"status": "ok"})),
                error: None,
            },
            true,
        ),
        "shutdown" => (
            Response {
                id: request.id,
                ok: true,
                result: Some(json!({"status": "stopping"})),
                error: None,
            },
            false,
        ),
        _ => (
            Response {
                id: request.id,
                ok: false,
                result: None,
                error: Some(json!({"code": "protocol.unsupported_operation"})),
            },
            true,
        ),
    };

    write_response(output, response)?;
    Ok(keep_running)
}

fn read_frame(input: &mut impl Read) -> io::Result<Option<Vec<u8>>> {
    let mut length = [0_u8; 4];
    match input.read_exact(&mut length) {
        Ok(()) => {}
        Err(error) if error.kind() == ErrorKind::UnexpectedEof => return Ok(None),
        Err(error) => return Err(error),
    }

    let frame_length = u32::from_be_bytes(length) as usize;
    if frame_length > MAXIMUM_FRAME_BYTES {
        return Err(io::Error::new(ErrorKind::InvalidData, "frame too large"));
    }

    let mut frame = vec![0_u8; frame_length];
    input.read_exact(&mut frame)?;
    Ok(Some(frame))
}

fn write_response(output: &mut impl Write, response: Response) -> io::Result<()> {
    let frame = serde_json::to_vec(&response).map_err(io::Error::other)?;
    let length = u32::try_from(frame.len())
        .map_err(|_| io::Error::new(ErrorKind::InvalidData, "response too large"))?;
    output.write_all(&length.to_be_bytes())?;
    output.write_all(&frame)?;
    output.flush()
}
