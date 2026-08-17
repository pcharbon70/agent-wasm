# State Operations, Revisions, and Conflicts

```spec-meta
id: agent_wasm.state_operations
kind: contract
status: active
summary: Ordered atomic state operations, optimistic revisions, preconditions, paths, and limits.
surface:
  - "lib/agent_wasm/state_operations/**/*.ex"
  - "test/agent_wasm/state_operations/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.atomic_durable_effects
```

## Source Traceability

- [State Operations, Patches, Revisions, and Conflicts](../../../60-specification/12-state-operations-patches-revisions-and-conflicts.md)

## Requirements

```spec-requirements
- id: agent_wasm.state_operations.atomic_patch
  statement: Set, delete, merge, append, increment, and test operations shall apply in order and atomically against an expected base revision.
  priority: must
  stability: stable
- id: agent_wasm.state_operations.revision
  statement: Successful state changes shall produce monotonic hash-linked revisions from canonical state.
  priority: must
  stability: stable
- id: agent_wasm.state_operations.conflict
  statement: Stale revisions, failed preconditions, invalid paths, schema violations, and patch limits shall reject the patch without partial state.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.state_operations.implementation_frontier
  covers:
    - agent_wasm.state_operations.atomic_patch
    - agent_wasm.state_operations.revision
    - agent_wasm.state_operations.conflict
  reason: State-operation validation, patch application, and revision hashing are not implemented.
```
