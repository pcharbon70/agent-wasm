# Extism Invocation Boundary

```spec-meta
id: agent_wasm.invocation
kind: module
status: active
summary: Tenant-isolated artifact resolution, bounded guest invocation, output validation, and disposition.
surface:
  - "lib/agent_wasm/invocation/**/*.ex"
  - "test/agent_wasm/invocation/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.portable_guest_protocol
```

## Source Traceability

- [Extism Invocation Boundary, Instances, and Output Validation](../../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)

## Requirements

```spec-requirements
- id: agent_wasm.invocation.isolation
  statement: The host shall verify tenant authorization and artifact digest before creating a fresh bounded guest instance for each turn.
  priority: must
  stability: stable
- id: agent_wasm.invocation.validation_order
  statement: Guest output shall pass byte, encoding, schema, patch, revision, directive-capability, and usage checks before state logic observes it.
  priority: must
  stability: stable
- id: agent_wasm.invocation.disposition
  statement: Success, trap, timeout, cancellation, and invalid output shall dispose or quarantine the instance with bounded evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.invocation.implementation_frontier
  covers:
    - agent_wasm.invocation.isolation
    - agent_wasm.invocation.validation_order
    - agent_wasm.invocation.disposition
  reason: The bootstrap Port adapter exists, but authorization, digest verification, complete resource limits, cancellation, output validation, and disposition evidence are not implemented.
```
