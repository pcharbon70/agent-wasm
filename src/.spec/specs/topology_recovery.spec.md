# Multi-Agent Recovery and Clustering Seams

```spec-meta
id: agent_wasm.topology_recovery
kind: workflow
status: active
summary: Clean-state multi-agent recovery, bounded resources, tenant isolation, lease behavior, and horizontal seams.
surface:
  - "lib/agent_wasm/topology_recovery/**/*.ex"
  - "test/agent_wasm/topology_recovery/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.logical_identity_disposable_placement
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-failure-evidence-and-operational-notes.md)
- [Phase 5 Integration Tests](../../../60-specification/39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-phase-5-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.topology_recovery.clean_state
  statement: Restart shall distrust pre-restart live placement and reconstruct bounded live agents from verified durable topology and observed status.
  priority: must
  stability: stable
- id: agent_wasm.topology_recovery.isolation
  statement: Recovery and topology shall not create cross-tenant routes, relationships, grants, results, mailboxes, leases, or placement authority.
  priority: must
  stability: stable
- id: agent_wasm.topology_recovery.seams
  statement: Horizontal lease transfer, topology distribution, and reconciliation coordination shall remain versioned replaceable seams with bounded evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.topology_recovery.implementation_frontier
  covers:
    - agent_wasm.topology_recovery.clean_state
    - agent_wasm.topology_recovery.isolation
    - agent_wasm.topology_recovery.seams
  reason: Multi-agent recovery, lease seams, and Milestone 6 acceptance fixtures are not implemented.
```
