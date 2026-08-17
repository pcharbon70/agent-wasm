# Embedded and Server Host Platform

```spec-meta
id: agent_wasm.host_platform
kind: contract
status: active
summary: Stable host operations, envelopes, lifecycle, configuration, dependency injection, transports, and packaging.
surface:
  - "lib/agent_wasm/host_platform/**/*.ex"
  - "test/agent_wasm/host_platform/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/46-embedded-and-server-host-apis-configuration-and-packaging-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/46-embedded-and-server-host-apis-configuration-and-packaging-failure-evidence-and-operational-notes.md)
- [Phase 1 Integration Tests](../../../60-specification/46-embedded-and-server-host-apis-configuration-and-packaging-phase-1-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.host_platform.operations
  statement: Embedded and server hosts shall expose the complete stable operation set through canonical request, response, error, pagination, idempotency, and streaming boundaries.
  priority: must
  stability: stable
- id: agent_wasm.host_platform.lifecycle_config
  statement: Configure, initialize, ready, drain, shutdown, cancel, and health behavior shall validate layered configuration, profiles, secret references, and dependencies before readiness.
  priority: must
  stability: stable
- id: agent_wasm.host_platform.adapters_packaging
  statement: Transport, runtime, storage, telemetry, and secrets adapters plus packages shall preserve host semantics, compatibility, provenance, and bounded diagnostics.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.host_platform.implementation_frontier
  covers:
    - agent_wasm.host_platform.operations
    - agent_wasm.host_platform.lifecycle_config
    - agent_wasm.host_platform.adapters_packaging
  reason: Host operations, lifecycle, configuration, adapters, transports, and packaging are not implemented.
```
