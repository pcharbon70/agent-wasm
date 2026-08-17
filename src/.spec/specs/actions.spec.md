# Actions, Instructions, Plans, and Results

```spec-meta
id: agent_wasm.actions
kind: contract
status: active
summary: Action declarations, concrete instructions, deterministic plans, validation, and result classes.
surface:
  - "lib/agent_wasm/actions/**/*.ex"
  - "test/agent_wasm/actions/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.portable_guest_protocol
```

## Source Traceability

- [Actions, Instructions, Validation, Plans, and Results](../../../60-specification/11-actions-instructions-validation-plans-and-results.md)

## Requirements

```spec-requirements
- id: agent_wasm.actions.declaration
  statement: Reusable action descriptors shall declare schemas, state access, directive kinds, grants, determinism, and timeout independently of invocations.
  priority: must
  stability: stable
- id: agent_wasm.actions.execution_plan
  statement: Instructions and sequential or DAG plans shall validate before execution and use deterministic node ordering.
  priority: must
  stability: stable
- id: agent_wasm.actions.result
  statement: Results shall distinguish success, rejection, validation, infrastructure, diagnostics, patches, directives, and domain status.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.actions.implementation_frontier
  covers:
    - agent_wasm.actions.declaration
    - agent_wasm.actions.execution_plan
    - agent_wasm.actions.result
  reason: Action registries, validation, planning, and result handling are not implemented.
```
