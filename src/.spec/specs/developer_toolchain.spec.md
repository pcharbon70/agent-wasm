# Guest SDK, CLI, Simulator, Templates, Fixtures, and Debugging

```spec-meta
id: agent_wasm.developer_toolchain
kind: contract
status: active
summary: Developer SDKs, CLI commands, deterministic simulation, templates, fixtures, debugging, compatibility, and offline use.
surface:
  - "lib/agent_wasm/developer_toolchain/**/*.ex"
  - "test/agent_wasm/developer_toolchain/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-failure-evidence-and-operational-notes.md)
- [Phase 2 Integration Tests](../../../60-specification/47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-phase-2-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.developer_toolchain.surfaces
  statement: Guest SDK and CLI surfaces shall preserve canonical host semantics for manifests, exports, codecs, artifacts, composition, fixtures, local execution, replay, reduction, and evidence inspection.
  priority: must
  stability: stable
- id: agent_wasm.developer_toolchain.determinism
  statement: Simulator controls, fixtures, templates, builds, and offline operation shall be isolated, reproducible, deterministic, and digest pinned.
  priority: must
  stability: stable
- id: agent_wasm.developer_toolchain.compatibility_debug
  statement: Compatibility negotiation, deprecation, actionable failures, and capability-controlled redacted debug views shall remain versioned and testable.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.developer_toolchain.implementation_frontier
  covers:
    - agent_wasm.developer_toolchain.surfaces
    - agent_wasm.developer_toolchain.determinism
    - agent_wasm.developer_toolchain.compatibility_debug
  reason: Guest SDKs, CLI, simulator, templates, fixtures, debug views, and reproducible build tooling are not implemented.
```
