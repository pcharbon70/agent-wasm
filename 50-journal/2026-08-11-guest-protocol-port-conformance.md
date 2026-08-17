---
title: "2026-08-11 Guest Protocol Port Conformance"
kind: journal
created: "2026-08-11"
tags:
  - elixir
  - extism
  - rust
  - testing
  - webassembly
aliases: []
---

# 2026-08-11 Guest Protocol Port Conformance

## Observations

The first durable Agent WASM implementation slice crosses the selected product
boundary: Elixir invokes a private Rust worker through four-byte big-endian OTP
Port frames, the worker creates a fresh Extism instance with WASI disabled and
an explicit total-invocation timeout, and a compiled Rust PDK guest executes
`describe`, `initialize`, `reduce`, and `migrate`. The worker is one-shot;
total-deadline expiry exits the process that owns the invocation thread, and the
Port maps that observed exit status to the timeout diagnostic.

This run supports only the four-function ABI requirement
`agent_wasm.guest_protocol.exports`, derived from
[Exports](../60-specification/04-turn-lifecycle-protocols-and-canonical-encoding.md#exports).
The timeout cases additionally demonstrate mechanisms needed by the broader
failure and invocation contracts, but does not establish those contracts. The
run does not establish lifecycle message-contract conformance, canonical-byte
conformance, complete schema validation, failure atomicity, cancellation,
cross-runtime equivalence, or promotion evidence for another normative chapter.

## Evidence

### Environment

The run completed at `2026-08-11T17:49:01Z` from Git revision
`5fb55e8a103c343e91a5d99085ba031bc4c15d1d` with uncommitted implementation
changes.

```text
Linux 6.8.0-51-generic x86_64
Erlang/OTP 27, ERTS 15.2.3
Elixir 1.18.4 (compiled with Erlang/OTP 27)
rustc 1.92.0 (ded5c06cf 2025-12-08)
cargo 1.92.0 (344c4567c 2025-10-21)
Extism 1.30.0
Wasmtime 43.0.2
Extism Rust PDK 1.4.1
```

Both Cargo dependency graphs are pinned by lock files in the current uncommitted
tree. Jason `1.4.5` is the Elixir-side JSON dependency.

### Artifact identities

```text
16fec6bbebf7faede306d1cb3d15a64b8b3eb566953ff179a5afa2224303307d  native/agent_wasm_runner/target/debug/agent_wasm_runner
9400dab2628b39668281a86b96706f495212d4f29e9e3148d3030590fac29a33  native/target/bootstrap_guest/wasm32-unknown-unknown/debug/bootstrap_guest.wasm
```

These are local debug artifact hashes, not release signatures or portable
artifact identities.

### Commands

Run from `src/`:

```bash
mix deps.get
mix native.build
cargo fmt --manifest-path native/agent_wasm_runner/Cargo.toml --check
cargo fmt --manifest-path test/fixtures/guest_protocol/bootstrap_guest/Cargo.toml --check
cargo clippy --locked --manifest-path native/agent_wasm_runner/Cargo.toml -- -D warnings
cargo clippy --locked --target wasm32-unknown-unknown --target-dir native/target/bootstrap_guest --manifest-path test/fixtures/guest_protocol/bootstrap_guest/Cargo.toml -- -D warnings
mix compile --warnings-as-errors
mix test test/agent_wasm/guest_protocol/lifecycle_conformance_test.exs --trace --seed 0
```

The targeted test result was:

```text
Running ExUnit with seed: 0, max_cases: 1
7 tests, 0 failures
```

The lifecycle test verifies that the compiled no-WASI guest exposes all four
exports through the real worker and returns representative responses. Negative
cases reject a function outside the lifecycle allowlist, a non-positive
`deadline_ms`, an atom-key duration above the configured host limit, and an
unbounded Port timeout. A guest-generated `"timeout"` error with the reserved
runtime-interrupt return code remains an invocation failure rather than spoofing
host-owned exhaustion. An infinite-loop fixture
verifies a bounded total-invocation cutoff and that a subsequent fresh invocation
succeeds.

## Threads

The earlier
[Elixir Port packaging probe](2026-08-10-elixir-port-packaging-probe.md)
established only framing and packaging health. This run replaces that temporary
mock boundary with durable Extism/Wasmtime code and a compiled guest, but it is
still the first layer of the broader
[WebAssembly assurance route](../10-maps/webassembly-testing-and-verification.md).

## Follow-ups

- Implement canonical JSON decoding and encoding before claiming
  `agent_wasm.guest_protocol.canonical_bytes`.
- Implement complete request and response schema and semantic validation before
  claiming `agent_wasm.guest_protocol.message_contracts`.
- Add malformed input, invalid output, trap, timeout, cancellation, and frame
  limit fixtures before claiming `agent_wasm.guest_protocol.failure_atomicity`;
  only execution-timeout interruption is covered here.
- Add artifact authorization, digest verification, output-validation order,
  cancellation, and disposition evidence before removing invocation-frontier
  exceptions.
- Build and compare the same fixture through an independent supported runtime
  family before making cross-runtime claims.
