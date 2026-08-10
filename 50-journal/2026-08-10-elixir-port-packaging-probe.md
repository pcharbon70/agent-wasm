---
title: "2026-08-10 Elixir Port Packaging Probe"
kind: journal
created: "2026-08-10"
tags:
  - deployment
  - elixir
  - rust
  - runtime
aliases: []
---

# 2026-08-10 Elixir Port Packaging Probe

## Observations

A temporary health-only project tested the proposed finished-product seam: an
OTP application owns a framed Port, a private native executable answers a
versioned handshake and health request, Mix packages the executable under the
application `priv` tree, and Docker copies the self-contained release into a
non-root runtime image.

The probe was intentionally kept outside the durable archive and removed after
the experiment. The reusable code and corrected pipeline are preserved in the
[packaging synthesis](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md).

## Evidence

### Environment

```text
Linux 6.8.0-51-generic x86_64
Erlang/OTP 27, ERTS 15.2.3
Elixir 1.18.4 (compiled with Erlang/OTP 27)
rustc 1.92.0 (ded5c06cf 2025-12-08)
cargo 1.92.0 (344c4567c 2025-10-21)
Docker 28.3.3, build 980b856
```

The probe dependencies resolved to Jason 1.4.5 and the Cargo versions recorded
in its generated lock file. The durable example requires both lock files to be
committed.

### Direct Port test

The worker used four-byte big-endian frames matching OTP's `{packet, 4}` Port
option. It implemented only `hello`, `health`, and `shutdown`. The Elixir
`GenServer` used an absolute `spawn_executable` path resolved from application
`priv`, negotiated protocol version 1 during `init/1`, allowed one outstanding
request, and closed the Port on timeout or invalid response.

Commands:

```bash
cargo generate-lockfile --manifest-path native/agent_wasm_runner/Cargo.toml
mix deps.get
mix format mix.exs config/config.exs 'lib/**/*.ex' 'test/**/*.exs'
cargo fmt --manifest-path native/agent_wasm_runner/Cargo.toml -- --check
cargo build --locked --manifest-path native/agent_wasm_runner/Cargo.toml
install -Dm0755 \
  native/agent_wasm_runner/target/debug/agent-wasm-runner \
  priv/runner/agent-wasm-runner
mix test
```

Result:

```text
Running ExUnit with seed: 942657, max_cases: 40
.
Finished in 0.01 seconds (0.00s async, 0.01s sync)
1 test, 0 failures
```

An earlier compile attempt called `Protocol.version/0` inside a guard, which is
not permitted for an ordinary remote function. Binding
`expected_protocol = Protocol.version()` before the `case` and comparing the
guard value fixed the example. The corrected code is the version retained in
the synthesis.

### Mix release

The release probe built the optimized worker, copied it to `priv`, compiled the
production application, assembled the release, and called the packaged worker
through the generated release command:

```bash
cargo build --locked --release \
  --manifest-path native/agent_wasm_runner/Cargo.toml
install -Dm0755 \
  native/agent_wasm_runner/target/release/agent-wasm-runner \
  priv/runner/agent-wasm-runner
MIX_ENV=prod mix deps.get --only prod
MIX_ENV=prod mix compile
MIX_ENV=prod mix release --overwrite
_build/prod/rel/agent_wasm/bin/agent_wasm eval \
  'Application.ensure_all_started(:agent_wasm); {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health(); IO.puts("release-port-health-ok")'
```

The release was created under `_build/prod/rel/agent_wasm` and printed:

```text
release-port-health-ok
```

### Container build, failures, and correction

The first Docker build failed before compilation because the slim Elixir
builder did not include CA certificates. `mix local.hex --force` could not load
operating-system CA roots and raised `:no_cacerts_found`. Adding
`ca-certificates` to the builder package list made dependency installation
work.

The corrected Docker build ran the target worker build, ExUnit test, Mix
release assembly, and release health expression inside the image. Its relevant
output was:

```text
Running ExUnit with seed: 894278, max_cases: 40
.
1 test, 0 failures
* assembling agent_wasm-0.1.0 on MIX_ENV=prod
Release created at _build/prod/rel/agent_wasm
```

The first final-container smoke call succeeded but warned that the VM inherited
Latin-1 native filename encoding. Adding `ENV LANG=C.UTF-8` to the Debian
runtime removed the warning. The final commands were:

```bash
docker build --progress=plain -t agent-wasm-port-probe:local .
docker run --rm \
  --entrypoint /opt/agent-wasm/bin/agent_wasm \
  agent-wasm-port-probe:local eval \
  'Application.ensure_all_started(:agent_wasm); {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health(); IO.puts("container-port-health-ok")'
```

Final result:

```text
container-port-health-ok
```

The final build was repeated with `ERL_AFLAGS="+JMsingle true"`, matching Mix's
guidance for release assembly through emulation; the in-image test, release
assembly, and final health call still passed. `docker buildx build --check .`
also completed with `Check complete, no warnings found`. The proposed GitHub
Actions workflow parsed successfully as YAML. The ARM64 build/push job itself
was not executed locally.

## Threads

The probe supports Elixir/OTP as the finished product and `priv` as the native
worker location. It also demonstrates why the pipeline must execute dependency
installation and the final release rather than treating a successful source
compile as sufficient packaging evidence.

It does not support claims about Extism invocation correctness, representative
performance, cancellation, worker fault containment, tenant residue, ARM64,
or the security posture of the final image. Those require dedicated evidence.

## Follow-ups

- Extend the worker protocol to `prepare`, `invoke`, `cancel`, and `dispose`
  with stable Agent WASM errors and lease/revision fencing.
- Add worker crash, malformed-frame, oversize, timeout, cancellation, and
  restart tests.
- Run native Linux ARM64 CI and verify the OCI manifest plus attestation.
- Implement and test the checksum/provenance-verifying Hex installer in offline
  and unsupported-target conditions.
