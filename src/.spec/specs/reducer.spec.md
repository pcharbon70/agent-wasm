# Deterministic Reducer

```spec-meta
id: agent_wasm.reducer
kind: workflow
status: active
summary: Deterministic resolution from admitted signal and snapshot to validated patch and directives.
surface:
  - "lib/agent_wasm/reducer/**/*.ex"
  - "test/agent_wasm/reducer/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Deterministic Reducer Semantics and Milestone Acceptance](../../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Requirements

```spec-requirements
- id: agent_wasm.reducer.resolution_order
  statement: Reducer resolution shall preserve the specified signal, routing, execution, patch, directive, and result-construction order.
  priority: must
  stability: stable
- id: agent_wasm.reducer.determinism
  statement: Identical canonical inputs and profile shall produce canonically equivalent outputs without ambient nondeterminism.
  priority: must
  stability: stable
- id: agent_wasm.reducer.acceptance
  statement: Replay and metamorphic fixtures shall prove field-order and canonical-reencoding equivalence and reject stale or unauthorized output.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.reducer.implementation_frontier
  covers:
    - agent_wasm.reducer.resolution_order
    - agent_wasm.reducer.determinism
    - agent_wasm.reducer.acceptance
  reason: Reducer orchestration and deterministic conformance fixtures are not implemented.
```
