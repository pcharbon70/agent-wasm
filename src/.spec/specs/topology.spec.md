# Pod Topology, Placement, Leases, and Reconciliation

```spec-meta
id: agent_wasm.topology
kind: workflow
status: active
summary: Versioned desired topology, observed status, disposable placement, activation leases, and reconciliation.
surface:
  - "lib/agent_wasm/topology/**/*.ex"
  - "test/agent_wasm/topology/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md)
- [Phase 4 Integration Tests](../../../60-specification/38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.topology.desired_state
  statement: Desired topology shall be durable and immutable per version, observed status shall be durable, and live placement shall remain disposable.
  priority: must
  stability: stable
- id: agent_wasm.topology.leases
  statement: Placement authority shall require unexpired activation leases and monotonic fencing that rejects stale hosts.
  priority: must
  stability: stable
- id: agent_wasm.topology.reconciliation
  statement: Reconciliation shall process missing, extra, failed, stale, moved, incompatible, and dependency-blocked nodes in the governing order with evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.topology.implementation_frontier
  covers:
    - agent_wasm.topology.desired_state
    - agent_wasm.topology.leases
    - agent_wasm.topology.reconciliation
  reason: Topology versions, placement, activation leases, reconciliation, and fixtures are not implemented.
```
