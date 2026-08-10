---
title: "Elixir/OTP Port Finished-Product Packaging and Release Pipeline"
kind: note
created: "2026-08-10"
maturity: developing
tags:
  - agent-tools
  - deployment
  - elixir
  - extism
  - implementation-language
  - rust
  - runtime
aliases:
  - "Elixir OTP product packaging"
  - "Elixir Port release pipeline"
---

# Elixir/OTP Port Finished-Product Packaging and Release Pipeline

Agent WASM should be delivered as an **Elixir/OTP product**. Its public API,
application lifecycle, configuration, telemetry, state model, supervision,
and operator experience should all be Elixir. The Extism/Wasmtime engine can
remain a small native executable behind an Erlang Port, but that executable is
a private component of the Elixir release—not a second product surface and not
an SDK that users must understand.

This makes the language choice concrete. An Elixir developer adds a Hex
dependency. An operator pulls one OCI image or installs one target-specific Mix
release. Neither installs Rust, Cargo, Go, Rustler, or a separate engine. The
release pipeline compiles the private worker, places it in the Elixir
application's `priv` directory, proves the pair can communicate, and publishes
the pair under one product version and digest.

## Decision

The finished product has one authoritative implementation language and one
public programming model: **Elixir/OTP**.

The boundary is deliberately asymmetric:

| Area | Product owner | Consequence |
| --- | --- | --- |
| Public library and service APIs | Elixir | Users write and operate Elixir, not engine bindings. |
| Agent state, policy, mailboxes, leases, effects, and durability | Elixir/OTP | The semantics stay in supervised BEAM processes and durable stores. |
| Wasm compilation and invocation | Private Port worker | Native engine work is replaceable and cannot become authoritative state. |
| Native implementation source | Rust | This is a build-time and supply-chain detail, comparable to an embedded database executable. |
| Release, configuration, telemetry, and upgrades | Elixir/OTP | One release version, one configuration system, one health surface, and one rollback unit. |

No Rust host API, Go host API, Rustler API, or polyglot product platform is part
of this design. The only matrix discussed below is the ordinary release matrix
for operating systems, CPU architectures, and ABIs.

## Scope and confidence

This is a non-normative implementation synthesis. It operationalizes the draft
host contracts without changing their authority. The examples prove packaging,
Port framing, startup negotiation, health calls, Mix-release assembly, and a
non-root container smoke test. They intentionally use a health-only worker so
that the evidence is not mistaken for a completed Extism adapter.

| Claim | Status |
| --- | --- |
| Elixir/OTP is the product language and control plane | Selected direction |
| A native worker can be bundled under application `priv` | Supported by Mix releases and locally exercised |
| A supervised Port can negotiate and exchange framed JSON | Locally exercised |
| The same pair runs from a self-contained release and final container | Locally exercised |
| The full `prepare`/`invoke`/`cancel`/`dispose` engine protocol is correct | Proposed; not yet implemented by the probe |
| Linux AMD64 and ARM64 images pass native CI | Pipeline-defined; only local AMD64 was exercised |
| Extism cancellation, fault containment, and service objectives pass | Open qualification work |

## Why Elixir/OTP is the obvious product fit

The host is mostly a long-lived coordination system, not a Wasm instruction
interpreter. It owns authenticated admission, bounded mailboxes, serialized
agent turns, deadlines, revision fencing, durable state and outboxes,
supervision, topology, quotas, audit evidence, and operational introspection.
Those duties map directly to OTP processes, supervisors, monitors, registries,
timers, behaviours, and releases. The
[Elixir process and supervision evidence](../30-sources/elixir-project-2026-processes-and-supervision.md)
also records the important qualification: a raw process mailbox is not itself
the host's admission or fairness contract, so the Elixir implementation must
still enforce explicit bounds.

This choice avoids rebuilding an actor lifecycle before implementing the
actual Agent WASM rules. It also gives native engine failure a natural
containment boundary. OTP's own guidance distinguishes in-VM NIFs from
external Ports: a NIF shares the VM's address space and failure scope, while a
Port communicates with a separate operating-system process. The latter fits a
coarse bytes-in/bytes-out Extism call especially well; see
[Erlang NIFs, Dirty Schedulers, and Ports](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md).

The native engine remains useful, but it is subordinated to the Elixir host:

- it receives an immutable invocation request and returns an immutable result;
- it never owns the canonical agent state, mailbox, outbox, policy, secret
  store, artifact trust decision, or lease;
- it cannot commit an effect or a state revision;
- it may be killed and replaced whenever its answer becomes late or uncertain;
- its protocol is versioned independently but compatibility is checked at
  release startup; and
- it is built, signed, installed, upgraded, and rolled back with the Elixir
  release.

This is not a general multilingual architecture. It is an Elixir/OTP
application using one private executable for the small part that must call the
reference Extism/Wasmtime engine.

## What the end user receives

### Operator-facing product

The primary production artifact should be a multi-architecture OCI image named
for the Elixir application, for example:

```text
ghcr.io/agent-wasm/agent-wasm:0.1.0
ghcr.io/agent-wasm/agent-wasm@sha256:<manifest-digest>
```

The tag points to an OCI manifest list. Docker selects the Linux AMD64 or
Linux ARM64 image for the machine, but each selected image contains a
target-native ERTS and worker. This is target portability, not runtime
language choice. The [Docker multi-platform source
note](../30-sources/docker-project-2026-multi-platform-builds.md) explains the
manifest-list behavior.

The final image contains:

```text
/opt/agent-wasm/
├── bin/agent_wasm
├── erts-15.x/
├── lib/
│   ├── agent_wasm-0.1.0/
│   │   ├── ebin/
│   │   └── priv/
│   │       └── runner/
│   │           └── agent-wasm-runner
│   ├── elixir-*/
│   └── ...
└── releases/
    ├── 0.1.0/
    └── start_erl.data
```

Mix releases include ERTS by default and do not require Erlang, Elixir, source
code, or build tools on the target. They are target-specific: architecture,
operating system, ABI, and dynamically linked dependencies must match. The
[Mix releases source note](../30-sources/elixir-project-2026-mix-releases.md)
anchors both properties.

### Non-container operator artifact

For systemd, air-gapped, or other non-container deployments, publish the same
release tree as a target-named archive rather than inventing another runtime:

```text
agent-wasm-0.1.0-x86_64-unknown-linux-gnu.tar.gz
agent-wasm-0.1.0-aarch64-unknown-linux-gnu.tar.gz
SHA256SUMS
```

Mix can add `:tar` after its `:assemble` release step. Each archive must be
built and smoked on a matching target, contain the paired worker and release
manifest, and receive the same SBOM and provenance treatment as the OCI child
image. Extraction creates one versioned directory whose generated
`bin/agent_wasm start` command is managed by the operator's service manager.
Configuration and writable state stay outside that immutable directory.

The archive is a secondary distribution of the same Elixir product. It should
not be published for a target merely because the worker cross-compiled; the
packaged ERTS and full release must execute there too.

### Elixir-developer product

An application developer should see an ordinary Hex dependency:

```elixir
defp deps do
  [
    {:agent_wasm, "~> 0.1"}
  ]
end
```

The package exposes only Elixir modules and configuration. A Mix installer or
compile hook selects a supported worker artifact, verifies it, and stages it
under the dependency's build `priv/runner` directory. The release then copies
that application and its `priv` content normally.

The Phoenix `esbuild` package demonstrates the user experience: an Elixir
package manages a target-specific executable under `_build` and invokes it
through Mix. Agent WASM should adopt the distribution shape, while adding
stronger checksum, provenance, offline, and release-pairing rules. See
[Phoenix Esbuild Binary Installer](../30-sources/phoenix-project-2026-esbuild-binary-installer.md).

The installer must:

1. map `:os.type/0` and `:erlang.system_info(:system_architecture)` to an
   explicit supported target;
2. select an asset from a versioned, committed manifest rather than a mutable
   `latest` URL;
3. fetch during dependency/build preparation, never during application boot;
4. verify SHA-256 and the project's release attestation before extraction;
5. reject an unknown OS, architecture, ABI, digest, or executable mode;
6. support an offline cache and an explicit `AGENT_WASM_RUNNER_PATH` override;
7. copy the verified executable into the built application's `priv/runner`;
8. run the `hello` handshake as a build or test gate; and
9. record the worker version, target, and digest in the product SBOM and release
   manifest.

There is no runtime auto-download. Production boot must fail closed when the
paired worker is absent or incompatible.

### WebAssembly package users

The host language does not alter the guest artifact contract. Authors still
compile an allowed guest language to the pinned Wasm/Extism profile and publish
the resulting artifact plus manifest and provenance. Consumers of those
packages do not rebuild the host and do not need Elixir or Rust knowledge.

What changes for them is operationally favorable:

- one Elixir host performs artifact admission, policy, limits, state, effects,
  telemetry, and Extism invocation consistently;
- the same Wasm package is admitted by artifact digest and profile, not by the
  source language used to create it;
- an engine update arrives as an Agent WASM product update rather than a new
  SDK choice; and
- support documentation has one host behavior and one error vocabulary.

## Runtime architecture inside the release

The smallest useful ownership picture is:

```text
client / Hex caller / network adapter
                 │
                 ▼
      Elixir Agent WASM public API
                 │
                 ▼
 admission → mailbox → leased turn → state/outbox transaction
                               │
                               ▼
                    bounded OTP Port pool
                               │ framed bytes
                               ▼
                  private native Extism worker
                               │
                               ▼
                      Extism / Wasmtime / Wasm
```

The worker returns a candidate result. The Elixir host validates the result and
lease, then owns the only state/outbox commit. A worker exit therefore loses at
most disposable compilation or invocation work, not authoritative agent state.

### Suggested supervision tree

```text
AgentWasm.Application
└── AgentWasm.Supervisor (:rest_for_one)
    ├── AgentWasm.Telemetry
    ├── AgentWasm.ArtifactStore
    ├── AgentWasm.Engine.Registry
    ├── AgentWasm.Engine.PortPoolSupervisor
    │   ├── AgentWasm.Engine.PortWorker #1
    │   ├── AgentWasm.Engine.PortWorker #2
    │   └── ... bounded to configured capacity
    ├── AgentWasm.AgentRegistry
    └── AgentWasm.AgentSupervisor
        └── AgentWasm.AgentCell ...
```

The reference probe below uses one `GenServer` and one worker to keep the
packaging example executable. Production should put a fixed number of workers
behind a checkout queue with explicit queue length, queue-age, per-tenant, and
deadline admission rules. Spawning an unbounded Port per request would merely
move the resource-exhaustion problem to operating-system processes.

### Port launch contract

Use `Port.open/2` with `{:spawn_executable, absolute_path}` rather than a shell
command:

```elixir
Port.open(
  {:spawn_executable, String.to_charlist(path)},
  [:binary, {:packet, 4}, :exit_status, :use_stdio]
)
```

`spawn_executable` runs the explicit executable without a `PATH` search and
without normal shell argument expansion. `{packet, 4}` gives each message a
big-endian four-byte length header; the worker must read and write the same
framing. `:binary` avoids lists of bytes, `:exit_status` reports termination,
and `:use_stdio` assigns stdin/stdout to protocol traffic. These behaviors are
defined by [Erlang `open_port/2`](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md).

Standard output must contain protocol frames only. Worker diagnostics go to
standard error as bounded structured records, where the container log collector
can capture them. Secrets, full prompts, untrusted output, and unrestricted
Wasm backtraces must not be logged.

### Protocol shape

Protocol version 1 should reserve these operations:

| Operation | Purpose |
| --- | --- |
| `hello` | Negotiate protocol, product/worker versions, engine version, target, features, and limits. |
| `health` | Prove the process and engine loop are responsive without loading an untrusted artifact. |
| `prepare` | Validate and optionally compile/cache one content-addressed artifact. |
| `invoke` | Execute one bounded Extism call against an explicit artifact and invocation context. |
| `cancel` | Cooperatively interrupt an identified invocation before the host's kill grace expires. |
| `dispose` | Drop worker-side compiled state or an instance lease. |
| `shutdown` | Complete an orderly release shutdown. |

Every request needs a correlation ID and protocol version. Invocation messages
also need the host's artifact digest, tenant and agent identities, turn/lease
identity, expected state revision, absolute deadline, declared limits, grants,
and input bytes. A representative envelope is:

```json
{
  "protocol": 1,
  "id": "req-01J...",
  "op": "invoke",
  "deadline_unix_ms": 1786387200000,
  "artifact": {
    "digest": "sha256:...",
    "export": "agent_turn"
  },
  "fence": {
    "tenant_id": "tenant:acme",
    "agent_id": "agent:42",
    "turn_id": "turn:99",
    "lease_id": "lease:100",
    "expected_revision": 17
  },
  "limits": {
    "input_bytes": 1048576,
    "output_bytes": 1048576,
    "memory_bytes": 67108864,
    "duration_ms": 5000
  },
  "payload_base64": "..."
}
```

Responses echo `id` and the complete fence. An answer with an unknown request,
expired deadline, lost lease, wrong revision, wrong artifact digest, duplicate
completion, or incompatible protocol is rejected before state validation or
commit.

JSON is suitable for the first coarse protocol because it is inspectable and
the Extism boundary already copies byte buffers. Large payloads should be
measured before adopting shared memory, file descriptors, or another codec.
Those optimizations increase lifetime and cleanup complexity and should not be
introduced merely to avoid an unmeasured copy.

### Concurrency, timeouts, and cancellation

The safe baseline is one in-flight invocation per worker and a bounded pool of
workers. It makes request ownership and crash recovery unambiguous. A worker
may internally cache compiled modules, but an instance is scoped to one
invocation unless a tested pool/reset policy proves no tenant residue.

For each call the Elixir host:

1. rejects work that cannot start before its deadline;
2. checks out a worker under queue and tenant limits;
3. starts an Elixir timer before sending the frame;
4. sends `cancel` when the deadline or caller cancellation fires;
5. waits only for a small configured kill grace;
6. closes the Port and terminates the OS worker if work remains uncertain;
7. lets OTP replace that worker; and
8. rejects every late result through request, lease, and revision fencing.

Closing a Port is not by itself proof that all descendant processes have died.
The production worker should remain a single process or be placed in a
container/cgroup or OS process group whose complete lifetime the launcher can
terminate. Extism cancellation must be exercised separately; killing the
worker is the final containment mechanism, not the normal fast path.

Synchronous engine-to-BEAM callbacks should not be in the first protocol.
Provide immutable context up front and return declarative effect requests. If
an unavoidable host function is later required, design an explicitly
re-entrant protocol with separate callback IDs, capability checks, deadlines,
and a demonstrated absence of pool deadlock.

## Reference packaging probe

The following small project is an executable packaging proof, not the complete
Agent WASM implementation. It demonstrates the exact release seam that the
real Extism worker would occupy.

```text
agent_wasm/
├── .github/workflows/release.yml
├── config/config.exs
├── lib/agent_wasm/application.ex
├── lib/agent_wasm/runner.ex
├── lib/agent_wasm/runner/protocol.ex
├── native/agent_wasm_runner/
│   ├── Cargo.toml
│   ├── Cargo.lock
│   └── src/main.rs
├── test/runner_test.exs
├── Dockerfile
├── mix.exs
└── mix.lock
```

Both lock files are committed. The examples use version tags for readability;
a production repository should also pin builder image digests and GitHub
Actions to reviewed full commit SHAs.

### Mix project and OTP application

```elixir
# mix.exs
defmodule AgentWasm.MixProject do
  use Mix.Project

  def project do
    [
      app: :agent_wasm,
      version: "0.1.0",
      elixir: "~> 1.18",
      start_permanent: Mix.env() == :prod,
      deps: [{:jason, "~> 1.4"}],
      releases: [agent_wasm: [include_executables_for: [:unix]]]
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {AgentWasm.Application, []}
    ]
  end
end
```

```elixir
# lib/agent_wasm/application.ex
defmodule AgentWasm.Application do
  use Application

  @impl true
  def start(_type, _args) do
    Supervisor.start_link(
      [{AgentWasm.Runner, name: AgentWasm.Runner}],
      strategy: :one_for_one,
      name: AgentWasm.Supervisor
    )
  end
end
```

### Framed protocol and Port owner

```elixir
# lib/agent_wasm/runner/protocol.ex
defmodule AgentWasm.Runner.Protocol do
  @version 1
  @maximum_frame_bytes 16 * 1024 * 1024

  def version, do: @version

  def request(operation) when operation in ["hello", "health", "shutdown"] do
    id = System.unique_integer([:positive, :monotonic]) |> Integer.to_string()
    payload = Jason.encode!(%{"protocol" => @version, "id" => id, "op" => operation})
    {id, payload}
  end

  def decode_response(payload) when byte_size(payload) <= @maximum_frame_bytes do
    with {:ok, response} when is_map(response) <- Jason.decode(payload),
         true <- is_binary(response["id"]),
         true <- is_boolean(response["ok"]) do
      {:ok, response}
    else
      _ -> {:error, :malformed_response}
    end
  end

  def decode_response(_payload), do: {:error, :oversized_response}
end
```

```elixir
# lib/agent_wasm/runner.ex
defmodule AgentWasm.Runner do
  use GenServer

  alias AgentWasm.Runner.Protocol

  @startup_timeout 5_000
  @request_timeout 5_000

  def start_link(options) do
    GenServer.start_link(__MODULE__, options, name: Keyword.fetch!(options, :name))
  end

  def health(server \\ __MODULE__) do
    GenServer.call(server, {:request, "health"}, @request_timeout + 1_000)
  end

  @impl true
  def init(_options) do
    Process.flag(:trap_exit, true)
    path = worker_path()

    if File.regular?(path) do
      port =
        Port.open(
          {:spawn_executable, String.to_charlist(path)},
          [:binary, {:packet, 4}, :exit_status, :use_stdio]
        )

      handshake(port)
    else
      {:stop, {:worker_not_found, path}}
    end
  end

  @impl true
  def handle_call({:request, operation}, from, %{pending: nil} = state) do
    {id, payload} = Protocol.request(operation)

    if Port.command(state.port, payload) do
      timer = Process.send_after(self(), {:request_timeout, id}, @request_timeout)
      {:noreply, %{state | pending: %{id: id, from: from, timer: timer}}}
    else
      {:reply, {:error, :worker_closed}, state}
    end
  end

  def handle_call({:request, _operation}, _from, state) do
    {:reply, {:error, :worker_busy}, state}
  end

  @impl true
  def handle_info({port, {:data, payload}}, %{port: port, pending: pending} = state)
      when not is_nil(pending) do
    case Protocol.decode_response(payload) do
      {:ok, %{"id" => id, "ok" => true, "result" => result}} when id == pending.id ->
        Process.cancel_timer(pending.timer)
        GenServer.reply(pending.from, {:ok, result})
        {:noreply, %{state | pending: nil}}

      {:ok, %{"id" => id, "ok" => false, "error" => error}} when id == pending.id ->
        Process.cancel_timer(pending.timer)
        GenServer.reply(pending.from, {:error, error})
        {:noreply, %{state | pending: nil}}

      _ ->
        GenServer.reply(pending.from, {:error, :invalid_worker_response})
        {:stop, :invalid_worker_response, %{state | pending: nil}}
    end
  end

  def handle_info({:request_timeout, id}, %{pending: %{id: id} = pending} = state) do
    GenServer.reply(pending.from, {:error, :timeout})
    Port.close(state.port)
    {:stop, :worker_timeout, %{state | pending: nil}}
  end

  def handle_info({port, {:exit_status, status}}, %{port: port} = state) do
    reply_pending(state.pending, {:error, {:worker_exit, status}})
    {:stop, {:worker_exit, status}, %{state | pending: nil}}
  end

  def handle_info({:EXIT, port, reason}, %{port: port} = state) do
    reply_pending(state.pending, {:error, {:worker_exit, reason}})
    {:stop, {:worker_exit, reason}, %{state | pending: nil}}
  end

  @impl true
  def terminate(_reason, %{port: port}) when is_port(port) do
    if Port.info(port), do: Port.close(port)
    :ok
  end

  def terminate(_reason, _state), do: :ok

  defp handshake(port) do
    expected_protocol = Protocol.version()
    {id, payload} = Protocol.request("hello")
    true = Port.command(port, payload)

    receive do
      {^port, {:data, response_payload}} ->
        case Protocol.decode_response(response_payload) do
          {:ok,
           %{
             "id" => ^id,
             "ok" => true,
             "result" => %{"protocol" => protocol}
           } = response}
          when protocol == expected_protocol ->
            {:ok, %{port: port, hello: response, pending: nil}}

          other ->
            Port.close(port)
            {:stop, {:incompatible_worker, other}}
        end

      {^port, {:exit_status, status}} ->
        {:stop, {:worker_exit_during_handshake, status}}
    after
      @startup_timeout ->
        Port.close(port)
        {:stop, :worker_handshake_timeout}
    end
  end

  defp worker_path do
    System.get_env("AGENT_WASM_RUNNER_PATH") ||
      Application.app_dir(:agent_wasm, ["priv", "runner", executable_name()])
  end

  defp executable_name do
    if match?({:win32, _}, :os.type()), do: "agent-wasm-runner.exe", else: "agent-wasm-runner"
  end

  defp reply_pending(nil, _reply), do: :ok

  defp reply_pending(pending, reply) do
    Process.cancel_timer(pending.timer)
    GenServer.reply(pending.from, reply)
  end
end
```

This probe permits only one outstanding request. Production code must also
handle an unsolicited frame when `pending` is `nil`, a Port `eof`, request
queue admission, engine-specific cancellation, telemetry, and all stable Agent
WASM error mappings. `{packet, 4}` simplifies framing but allows a trusted
worker to declare a large packet before application-level decoding; deployment
resource controls and worker integrity therefore remain necessary.

### Minimal private worker

The worker is intentionally not an end-user API. This minimal implementation
only proves framing and health. The real worker replaces the operation body
with Extism calls while preserving the same process contract.

```toml
# native/agent_wasm_runner/Cargo.toml
[package]
name = "agent-wasm-runner"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
// native/agent_wasm_runner/src/main.rs
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
        if !handle_frame(&frame, &mut output)? {
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
            write_response(
                output,
                Response {
                    id: String::new(),
                    ok: false,
                    result: None,
                    error: Some(json!({"code": "protocol.decode"})),
                },
            )?;
            return Ok(true);
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
    match input.read(&mut length[..1])? {
        0 => return Ok(None),
        1 => {}
        _ => unreachable!("the input slice has length one"),
    }
    input.read_exact(&mut length[1..])?;

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
    if frame.len() > MAXIMUM_FRAME_BYTES {
        return Err(io::Error::new(ErrorKind::InvalidData, "response too large"));
    }
    let length = u32::try_from(frame.len())
        .map_err(|_| io::Error::new(ErrorKind::InvalidData, "response too large"))?;
    output.write_all(&length.to_be_bytes())?;
    output.write_all(&frame)?;
    output.flush()
}
```

### Contract test

```elixir
# test/runner_test.exs
defmodule AgentWasm.RunnerTest do
  use ExUnit.Case, async: false

  test "the packaged Port worker completes its handshake and health request" do
    assert {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health()
  end
end
```

This test is deliberately run after the target worker has been copied to
`priv/runner`. It therefore catches wrong names, permissions, targets, framing,
protocol versions, and immediate worker exits rather than testing only an
Elixir mock.

## Reproducible container definition

This Dockerfile builds both internals, assembles a self-contained Mix release,
executes the Port contract test and release smoke test, and copies only the
finished release into a non-root runtime image.

```dockerfile
# syntax=docker/dockerfile:1.7

FROM rust:1.92-bookworm AS rust-build
WORKDIR /src
COPY native/agent_wasm_runner/Cargo.toml native/agent_wasm_runner/Cargo.lock ./
COPY native/agent_wasm_runner/src ./src
RUN cargo build --locked --release

FROM elixir:1.18.4-otp-27-slim AS elixir-build
ENV MIX_ENV=prod
# Mix documents this setting for releases assembled through emulation.
ENV ERL_AFLAGS="+JMsingle true"
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && mix local.hex --force \
    && mix local.rebar --force
COPY mix.exs mix.lock ./
COPY config ./config
RUN mix deps.get --only prod && mix deps.compile
COPY lib ./lib
COPY test ./test
COPY --from=rust-build \
     /src/target/release/agent-wasm-runner \
     /app/priv/runner/agent-wasm-runner
RUN chmod 0755 /app/priv/runner/agent-wasm-runner \
    && MIX_ENV=test mix test \
    && MIX_ENV=prod mix compile \
    && MIX_ENV=prod mix release --overwrite \
    && _build/prod/rel/agent_wasm/bin/agent_wasm eval \
       'Application.ensure_all_started(:agent_wasm); {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health()'

FROM scratch AS release-files
COPY --from=elixir-build /app/_build/prod/rel/agent_wasm /agent_wasm

FROM debian:bookworm-slim AS runtime
ENV LANG=C.UTF-8
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates libgcc-s1 libncurses6 libssl3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system agent-wasm \
    && useradd --system --gid agent-wasm \
       --home-dir /opt/agent-wasm agent-wasm
WORKDIR /opt/agent-wasm
COPY --from=elixir-build --chown=agent-wasm:agent-wasm \
     /app/_build/prod/rel/agent_wasm ./
USER agent-wasm
ENTRYPOINT ["/opt/agent-wasm/bin/agent_wasm"]
CMD ["start"]
```

The production version should pin each `FROM` image by digest, scan both build
graphs, and derive the runtime library list from linked ERTS and worker
artifacts for every target. The example's Debian runtime is a deliberate
pairing with Debian-based builders; an Alpine/musl target is a different
release artifact, not an interchangeable smaller final layer.

Local build and smoke commands are:

```bash
docker build --progress=plain -t agent-wasm:local .

docker run --rm \
  --entrypoint /opt/agent-wasm/bin/agent_wasm \
  agent-wasm:local eval \
  'Application.ensure_all_started(:agent_wasm); {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health(); IO.puts("container-port-health-ok")'
```

## Working release workflow

The primary release workflow publishes one product name with Linux AMD64 and
ARM64 variants, an SBOM, and a build-provenance attestation. The Docker build
itself runs the target-specific Port test and Mix-release smoke test, so a
variant cannot be pushed merely because its files compiled.

```yaml
name: Release Agent WASM

on:
  push:
    tags: ["v*.*.*"]
  workflow_dispatch:

permissions:
  contents: read
  packages: write
  id-token: write
  attestations: write
  artifact-metadata: write

env:
  IMAGE_NAME: ghcr.io/${{ github.repository }}

jobs:
  image:
    runs-on: ubuntu-latest
    steps:
      # Pin reviewed full commit SHAs in the production repository.
      - uses: actions/checkout@v6
      - uses: docker/setup-qemu-action@v4
      - uses: docker/setup-buildx-action@v4

      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: metadata
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - id: build
        uses: docker/build-push-action@v7
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.metadata.outputs.tags }}
          labels: ${{ steps.metadata.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          sbom: true
          # A separate step below creates the GitHub/Sigstore provenance.
          provenance: false

      - uses: actions/attest@v4
        with:
          subject-name: ${{ env.IMAGE_NAME }}
          subject-digest: ${{ steps.build.outputs.digest }}
          push-to-registry: true
```

`actions/attest` requires the fully qualified image name without a tag plus the
digest returned by the image build. It emits SLSA build provenance by default
and stores a Sigstore bundle; see [GitHub Artifact
Attestations](../30-sources/github-project-2026-artifact-attestations.md).

The current Milestone 8 Phase 6 seed notes mention detached PGP signatures,
whereas this executable pipeline recommends GitHub OIDC/Sigstore provenance for
OCI subjects. Those are distinct trust-policy choices. Before a production
release, the project must either revise that seed decision consistently or add
the required PGP signing and verification gate for file archives; it must not
claim that a Sigstore attestation silently satisfies a PGP requirement.

For a protected release, the tag workflow is the promotion stage, not the first
time the code is tested. Branch CI should run formatting, static analysis,
unit/property tests, Port contract tests, worker crash tests, and a single-
platform Docker build. The release job should depend on those required checks
and on an approved semantic version derived from the Elixir application.

## Pipeline definition and release gates

The finished pipeline is an ordered set of fail-closed gates:

| Stage | Required action | Release-blocking evidence |
| --- | --- | --- |
| 1. Resolve | Check out one source revision and locked Hex/Cargo dependencies. | Clean lock resolution; no mutable dependency references. |
| 2. Verify Elixir | Format, compile with warnings-as-errors, run static analysis and unit/property tests. | Host contract suite passes. |
| 3. Build worker | Build the private worker for the target with `--locked`. | Worker binary, target triple, dependency graph, and digest recorded. |
| 4. Verify boundary | Copy worker to `priv`, run `hello`, health, malformed-frame, wrong-version, timeout, and crash tests. | Stable results and supervised recovery. |
| 5. Verify Extism | Run pinned guest fixtures for prepare/invoke/cancel/dispose, limits, traps, and residue. | Exact profile and engine evidence. |
| 6. Assemble | Build the Mix release on a host matching the target. | ERTS, application, worker, and release manifest form one immutable tree. |
| 7. Smoke | Boot the assembled release and final image as the runtime user. | Public health, Port health, configuration, and graceful shutdown pass. |
| 8. Harden | Scan dependencies/image, enforce non-root/read-only policy, generate SBOM. | No unaccepted finding; runtime contains no compiler or package manager requirement. |
| 9. Publish | Push every target variant and the manifest list by immutable digest. | Registry reports all promised targets. |
| 10. Attest | Sign/attest source revision, image digest, SBOM, builder, and workflow identity. | Consumer verification succeeds from a clean environment. |
| 11. Promote | Move a human-readable version/channel tag to the tested digest. | Approval and rollback target recorded. |

Do not build the private worker in one workflow and resolve “the latest worker”
from another. The source revision, worker, ERTS, BEAM code, configuration
schema, SBOM, and image manifest are one release subject.

### Release manifest

The image should carry a machine-readable manifest such as:

```json
{
  "product": "agent-wasm",
  "product_version": "0.1.0",
  "host_protocol": "0.1.0",
  "port_protocol": 1,
  "elixir": "1.18.4",
  "otp": "27.3",
  "target": "x86_64-unknown-linux-gnu",
  "worker": {
    "version": "0.1.0",
    "sha256": "...",
    "extism": "<pinned-version>",
    "wasmtime": "<resolved-version>"
  },
  "source_revision": "<git-commit>",
  "image_digest": "sha256:..."
}
```

The `hello` response must agree with the embedded manifest. A mismatch is a
startup failure, not a warning. The health endpoint should report the product
version and compatibility status but need not reveal the complete dependency
graph to untrusted callers.

## Target matrix without a language matrix

The initial product promise should be deliberately small:

| Product channel | Initial target | Build rule |
| --- | --- | --- |
| OCI service | `linux/amd64/gnu` | Build and smoke inside the target image. |
| OCI service | `linux/arm64/gnu` | Build and smoke on native ARM64 CI where possible; emulation is a fallback. |
| Hex embedding | The same two Linux targets first | Installer selects and verifies exactly one worker artifact. |

macOS and Windows archives can be added when native CI runners execute the
full release and Port suites. Mix releases cannot be assembled once and copied
across target triples. A target is supported only when its actual ERTS and
worker pair passes; a successful cross-compile alone is insufficient.

The Milestone 8 Phase 6 seed material currently enumerates Linux, macOS, and
Windows targets while also deferring automated platform testing. This research
recommends treating Linux AMD64/ARM64 as the initial supported product and the
other entries as planned until their native evidence exists. Adopting that
recommendation requires bringing the Milestone 8 deployment notes into sync;
this synthesis does not silently relabel untested targets as supported.

This restraint simplifies support for early adopters. It does not restrict the
languages from which users compile WebAssembly packages.

## Configuration and operations

Build-time configuration chooses only immutable release facts, such as the
paired protocol and worker manifest. Secrets, service endpoints, pool sizes,
queue bounds, and tenant policy belong in `config/runtime.exs` or an explicit
configuration provider. Mix is unavailable inside a release, and production
boot must validate every required runtime setting before accepting traffic.

At minimum expose:

- application readiness, worker-pool capacity, compatible-worker count, and
  queue age;
- counters for prepare/invoke outcomes, worker exits, protocol violations,
  cancellations, hard kills, restarts, and late-result rejections;
- latency histograms split into admission queue, Port transfer, engine work,
  result validation, and durable commit;
- target, product, protocol, engine, and worker versions as bounded telemetry
  attributes; and
- crash evidence correlated by request and worker identity without logging
  secrets or unrestricted guest bytes.

Readiness should fail when no compatible worker can serve the required
profile. Liveness should distinguish a recoverable worker restart from a stuck
BEAM node. A rolling deploy becomes ready only after the startup handshake and
representative engine self-test pass.

## Security boundary

A Port supplies address-space and crash separation from the BEAM; it is not a
complete sandbox for the native process. The Wasm engine, worker, container,
operating system, and deployment policy remain part of the trusted computing
base.

The primary container should run as a numeric non-root user with a read-only
root filesystem, a writable bounded cache volume only when compilation caching
is enabled, no ambient secrets in the worker environment, dropped Linux
capabilities, `no-new-privileges`, bounded memory/PIDs/CPU, and a reviewed
seccomp/AppArmor or equivalent profile. Network and filesystem access are
denied by default and granted through the host contract, not inherited merely
because the worker process could access them.

The Elixir host must verify guest artifacts before asking the worker to load
them. The worker must independently enforce the supplied digest, profile,
deadline, memory/output limits, and Extism/WASI capability configuration. That
defense in depth does not transfer policy ownership to the worker.

## Upgrades and rollback

An upgrade replaces the complete immutable release. It never swaps the worker
under a running host from a mutable filesystem path.

1. Build and attest version `N+1` as a new digest.
2. Run backward-compatible storage and protocol checks before traffic.
3. Start new instances; each validates its embedded worker through `hello`.
4. Drain old Elixir turn admission while allowing bounded in-flight work to
   complete or cancel.
5. Shift traffic only after new readiness and representative invocation pass.
6. Retain version `N`'s image digest and storage compatibility evidence.
7. Roll back by redeploying that complete digest, not by mixing its worker with
   version `N+1` BEAM code.

The Port protocol can support a short compatibility window, but the ordinary
release should still ship matching versions. Compatibility exists to enable
controlled rolling deployment and diagnosis, not arbitrary component drift.

## Local evidence

The [2026-08-10 packaging probe
journal](../50-journal/2026-08-10-elixir-port-packaging-probe.md) records the
environment, commands, failures, corrections, and results. In summary:

- Erlang/OTP 27 with ERTS 15.2.3 and Elixir 1.18.4 compiled the host;
- Rust/Cargo 1.92.0 built the private worker;
- the direct ExUnit Port test completed with `1 test, 0 failures`;
- `mix release` produced a self-contained release whose health call passed;
- the first container attempt exposed missing CA certificates in the slim
  builder and was corrected;
- the first final-container run exposed a missing UTF-8 locale and was
  corrected with `LANG=C.UTF-8`; and
- Docker 28.3.3 then built the image and the non-root final container printed
  `container-port-health-ok` without the locale warning.

Those are useful packaging results, not engine correctness results. The probe
did not execute Extism, inject a worker crash, prove cancellation, measure Port
overhead, test tenant residue, or run the ARM64 workflow.

## Work remaining before production

1. Replace the health-only worker body with a pinned Extism implementation and
   commit its complete dependency lock.
2. Freeze the Port protocol schema, maximums, stable error mapping, and
   compatibility policy.
3. Implement a bounded supervised worker pool with fair tenant admission.
4. Exercise malformed, truncated, oversized, duplicate, late, and unsolicited
   frames plus worker panic/abort/kill behavior.
5. Prove cooperative Extism cancellation and hard-kill cleanup under real
   deadlines.
6. Run guest conformance, state/effect, artifact, and tenant-residue fixtures.
7. Build and smoke every promised target on native CI where possible.
8. Implement the checksum/attestation-verifying Hex installer and offline
   override path.
9. Generate and verify the combined Hex, Cargo, OS-package, ERTS, and container
   SBOM.
10. Measure end-to-end latency and capacity; optimize the boundary only if the
    result violates a product objective.

None of this remaining work reopens the public language decision. It qualifies
the private engine boundary and the Elixir product release.

## Falsification criteria

The Port packaging approach should be reconsidered only if representative
evidence shows that it cannot satisfy an explicit product objective after
bounded pooling and coarse messages are implemented—for example, unacceptable
end-to-end latency, inability to stop work before lease expiry, or an
unsupported required operating-system target. A microbenchmark of an empty
call is not sufficient; the comparison must include validation, Wasm work,
state/outbox commit, and recovery behavior.

Even if the private boundary changes, Elixir/OTP remains the product and
authoritative host unless the host requirements themselves change. The
research does not maintain parallel public implementations.

## Connections

- [Agent WASM Host Implementation Language and Runtime Boundary](agent-wasm-host-implementation-language-and-runtime-boundary.md)
  supplies the earlier comparative evidence; this note converts its Elixir
  recommendation into a finished-product design.
- [Host implementation inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
  now treats Elixir/OTP as selected and keeps only boundary qualification open.
- [Profile Vocabulary and Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)
  identifies the host-owned responsibilities that remain in Elixir.
- [Extism Invocation Boundary](../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
  defines the draft behavior the production Port adapter must preserve.
- [Milestone 8 Phase 6 deployment work](m8-p6-behavior-and-integration-implementation.md)
  states the broader artifact and integrity goals that this concrete pipeline
  begins to operationalize.

## Sources

- [Elixir Project: Mix Releases](../30-sources/elixir-project-2026-mix-releases.md)
- [Erlang NIFs, Dirty Schedulers, and Ports](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md)
- [Docker Multi-Platform Builds](../30-sources/docker-project-2026-multi-platform-builds.md)
- [GitHub Artifact Attestations](../30-sources/github-project-2026-artifact-attestations.md)
- [Phoenix Esbuild Binary Installer](../30-sources/phoenix-project-2026-esbuild-binary-installer.md)
- [Extism Reference Runtime](../30-sources/extism-project-2026-reference-runtime.md)
