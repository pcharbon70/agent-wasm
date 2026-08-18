# Milestone 6 - Multi-Agent Coordination And Topology

Extend durable single-agent semantics to agent relationships, delegation, coordination, topology reconciliation, placement, and recoverable multi-agent workflows.

Specification-plan status: phases 1-5 complete. Runtime implementation and
conformance are tracked separately in the
[package-local SpecLed workspace](../../../../src/.spec/README.md).

## Purpose

Provide the ordered, section-sized specification work and evidence requirements
needed to define this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for multi-agent coordination and topology.

## Dependencies And Entry Gate

- Milestone 5 defines identities, grants, tenant boundaries, and plugin composition.
- Milestone 4 durable effects can carry child and coordination results.

## Phase Order

1. [Phase 1 - Agent Identity Addressing Ownership And Dependency Relations](phase-01-agent-identity-addressing-ownership-and-dependency-relations.md)
2. [Phase 2 - Child Lifecycle Cancellation Monitoring And Restart Policy](phase-02-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
3. [Phase 3 - Fan-Out Fan-In Delegation And Result Aggregation](phase-03-fan-out-fan-in-delegation-and-result-aggregation.md)
4. [Phase 4 - Pod Topology Placement Activation Leases And Reconciliation](phase-04-pod-topology-placement-activation-leases-and-reconciliation.md)
5. [Phase 5 - Multi-Agent Recovery Clustering Seams And Milestone Acceptance](phase-05-multi-agent-recovery-clustering-seams-and-milestone-acceptance.md)

## Planned Artifacts

- Agent relationship and addressing contracts
- Coordination, delegation, aggregation, and lifecycle protocols
- Durable topology, placement, and reconciliation model

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until its specification artifact and
  traceability record exist.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-scenario section.
- Author and commit one section at a time.

## Shared Assumptions And Defaults

- Durable topology contains logical identities, never live handles.
- Single-node placement is implemented before multi-node coordination adapters.
- Parallelism occurs across agents and effects, not within one committed turn.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

This is a runtime and conformance gate; the specification-plan status above
does not claim that it has passed.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Agent Identity Addressing Ownership And Dependency Relations](phase-01-agent-identity-addressing-ownership-and-dependency-relations.md) — defines and traces this ordered phase.
- [Phase 2 - Child Lifecycle Cancellation Monitoring And Restart Policy](phase-02-child-lifecycle-cancellation-monitoring-and-restart-policy.md) — defines and traces this ordered phase.
- [Phase 3 - Fan-Out Fan-In Delegation And Result Aggregation](phase-03-fan-out-fan-in-delegation-and-result-aggregation.md) — defines and traces this ordered phase.
- [Phase 4 - Pod Topology Placement Activation Leases And Reconciliation](phase-04-pod-topology-placement-activation-leases-and-reconciliation.md) — defines and traces this ordered phase.
- [Phase 5 - Multi-Agent Recovery Clustering Seams And Milestone Acceptance](phase-05-multi-agent-recovery-clustering-seams-and-milestone-acceptance.md) — defines and traces this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
