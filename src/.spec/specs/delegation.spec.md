# Fan-Out, Fan-In, Delegation, and Aggregation

```spec-meta
id: agent_wasm.delegation
kind: workflow
status: active
summary: Durable plans, delegated work, bounded concurrency, causal results, aggregation, cancellation, and evidence.
surface:
  - "lib/agent_wasm/delegation/**/*.ex"
  - "test/agent_wasm/delegation/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md)
- [Phase 3 Integration Tests](../../../60-specification/37-fan-out-fan-in-delegation-and-result-aggregation-phase-3-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.delegation.plan
  statement: Fan-out plans and work items shall use deterministic identities, bounded concurrency, deadlines, cancellation policy, attenuated grants, and result contracts.
  priority: must
  stability: stable
- id: agent_wasm.delegation.aggregation
  statement: All, quorum, first-success, best-effort, and ordered aggregation shall be host-owned, deterministic, durable, and duplicate-aware.
  priority: must
  stability: stable
- id: agent_wasm.delegation.evidence
  statement: Result conflicts, timeouts, cancellation, recovery, aggregation progress, and cross-milestone behavior shall retain bounded signed evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.delegation.implementation_frontier
  covers:
    - agent_wasm.delegation.plan
    - agent_wasm.delegation.aggregation
    - agent_wasm.delegation.evidence
  reason: Fan-out scheduling, child work, durable aggregation, and integration fixtures are not implemented.
```
