# Guest SDK and Milestone Acceptance

```spec-meta
id: agent_wasm.guest_sdk
kind: contract
status: active
summary: Language SDK lowering, compiled fixtures, diagnostics, and protocol acceptance.
surface:
  - "lib/agent_wasm/guest_sdk/**/*.ex"
  - "test/agent_wasm/guest_sdk/**/*_test.exs"
decisions:
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Guest SDK Contracts, Fixtures, and Milestone Acceptance](../../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)

## Requirements

```spec-requirements
- id: agent_wasm.guest_sdk.semantic_preservation
  statement: Guest SDKs shall preserve protocol semantics while lowering language values, exports, codecs, signals, state operations, directives, strategies, and diagnostics.
  priority: must
  stability: stable
- id: agent_wasm.guest_sdk.compiled_fixtures
  statement: Conformance shall be demonstrated by compiled guest artifacts and exact positive and negative fixtures rather than source-only tests.
  priority: must
  stability: stable
- id: agent_wasm.guest_sdk.acceptance
  statement: SDK and Milestone 1 acceptance evidence shall retain fixture status, profile, versions, and unresolved variability.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.guest_sdk.implementation_frontier
  covers:
    - agent_wasm.guest_sdk.semantic_preservation
    - agent_wasm.guest_sdk.compiled_fixtures
    - agent_wasm.guest_sdk.acceptance
  reason: No guest SDK package or compiled conformance fixture corpus exists yet.
```
