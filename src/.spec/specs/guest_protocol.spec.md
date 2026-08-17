# Guest Protocol and Canonical Encoding

```spec-meta
id: agent_wasm.guest_protocol
kind: contract
status: active
summary: Describe, initialize, reduce, and migrate envelopes over canonical bytes.
surface:
  - "lib/agent_wasm/invocation/port_worker.ex"
  - "native/agent_wasm_runner/Cargo.toml"
  - "native/agent_wasm_runner/Cargo.lock"
  - "native/agent_wasm_runner/src/main.rs"
  - "test/agent_wasm/guest_protocol/lifecycle_conformance_test.exs"
  - "test/fixtures/guest_protocol/bootstrap_guest/Cargo.toml"
  - "test/fixtures/guest_protocol/bootstrap_guest/Cargo.lock"
  - "test/fixtures/guest_protocol/bootstrap_guest/src/lib.rs"
decisions:
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.host_owned_authority
```

## Source Traceability

- [Turn Lifecycle Protocols and Canonical Encoding](../../../60-specification/04-turn-lifecycle-protocols-and-canonical-encoding.md)

## Requirements

```spec-requirements
- id: agent_wasm.guest_protocol.exports
  statement: The bootstrap artifact shall expose describe, initialize, reduce, and migrate through the Extism no-argument bytes-in/bytes-out calling convention.
  priority: must
  stability: stable
- id: agent_wasm.guest_protocol.message_contracts
  statement: Each lifecycle export shall implement its specified request-response schema and semantic contract.
  priority: must
  stability: stable
- id: agent_wasm.guest_protocol.canonical_bytes
  statement: Protocol messages shall use validated canonical encoding with stable version, identity, revision, and diagnostic fields.
  priority: must
  stability: stable
- id: agent_wasm.guest_protocol.failure_atomicity
  statement: Decode, schema, semantic, revision, trap, timeout, cancellation, and limit failures shall publish no successful or partial authoritative result.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.guest_protocol.implementation_frontier
  covers:
    - agent_wasm.guest_protocol.message_contracts
    - agent_wasm.guest_protocol.canonical_bytes
    - agent_wasm.guest_protocol.failure_atomicity
  reason: Complete schema and semantic validation, canonical codecs, negative fixtures, and failure-atomicity evidence are not implemented.
```

## Verification

```spec-verification
- kind: command
  target: mix test test/agent_wasm/guest_protocol/lifecycle_conformance_test.exs --trace
  execute: true
  covers:
    - agent_wasm.guest_protocol.exports
```
