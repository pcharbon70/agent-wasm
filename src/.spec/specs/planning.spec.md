# Direct, FSM, Tool-Loop, and Planning Strategies

```spec-meta
id: agent_wasm.planning
kind: workflow
status: active
summary: Explicit direct, FSM, bounded-loop, and reviewable planning state with budgets and termination.
surface:
  - "lib/agent_wasm/planning/**/*.ex"
  - "test/agent_wasm/planning/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md)
- [Phase 3 Integration Tests](../../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.planning.explicit_state
  statement: Direct, FSM, tool-loop, and planning strategies shall use explicit serialized state, plans, waits, iterations, budgets, and bounded history without hidden continuation.
  priority: must
  stability: stable
- id: agent_wasm.planning.budgets_termination
  statement: Turn, token, tool, cost, time, iteration, and recursion limits plus loop, repeated-request, contradiction, missing-result, and model-drift detection shall force explicit termination.
  priority: must
  stability: stable
- id: agent_wasm.planning.resume_evidence
  statement: Snapshot migration, deterministic resume, plan adaptation, state transitions, and every failure class shall retain bounded evidence and integration proof.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.planning.implementation_frontier
  covers:
    - agent_wasm.planning.explicit_state
    - agent_wasm.planning.budgets_termination
    - agent_wasm.planning.resume_evidence
  reason: Strategy state machines, budgets, planning, loop detection, resume, and fixtures are not implemented.
```
