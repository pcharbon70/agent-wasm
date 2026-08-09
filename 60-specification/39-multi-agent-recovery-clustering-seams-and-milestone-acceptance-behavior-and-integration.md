---
title: "Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-05
  - recovery
  - clustering
  - seams
  - milestone-acceptance
  - behavior
  - integration
aliases:
  - "M6-P5 Behavior And Integration"
---

# Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-05-multi-agent-recovery-clustering-seams-and-milestone-acceptance.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the behavior and integration rules for multi-agent recovery
clustering seams and milestone acceptance, including durable topology
validation, resource bounding, and the adapter contract for future
horizontal coordination.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md),
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md),
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md),
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md),
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md),
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md),
[Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md),
[Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model](37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md),
[Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration](37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md),
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md),
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md),
[Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes](38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md),
[Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests](38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md).

## 39.2 Behavior And Integration

### Durable topology validation behavior

> **Normative definition.**
When a topology directive is submitted, the host MUST validate the
directive against the following rules in order:

1. **Schema validation**: The directive MUST conform to the topology
   schema defined in section 39.1. Missing required fields MUST be
   rejected with `topology.directive.malformed`.
2. **Owner resolution**: The `topology_owner` MUST resolve to an active
   principal in the durable registry. Unresolved owners MUST be rejected
   with `topology.directive.unavailable`.
3. **Capability check**: The `topology_owner` MUST have the
   `topology.directive.create` capability. Insufficient capabilities
   MUST be rejected with `topology.directive.unauthorized`.
4. **Version uniqueness**: The `topology_version` MUST be greater than
   the current maximum version. Duplicate versions MUST be rejected with
   `topology.directive.duplicate-version`.
5. **Node list validation**: The `nodes` list MUST be non-empty and
   each node MUST conform to the node schema. Invalid nodes MUST be
   rejected with `topology.node.malformed`.
6. **Node agent resolution**: Each node's `agent_address` MUST resolve
   to an active agent in the durable registry. Unresolved agents MUST
   cause the directive to be rejected with `topology.directive.incompatible-agent`.
7. **Dependency validation**: Each node's `dependencies` MUST reference
   existing `node_id` values within the same topology. Invalid dependencies
   MUST cause the directive to be rejected with `topology.node.incompatible-dependency`.
8. **Circular dependency check**: The topology's `nodes` list MUST NOT
   contain circular dependencies. Circular dependencies MUST cause the
   directive to be rejected with `topology.node.incompatible-circular-dependency`.
9. **Grant attenuation**: The topology's `grants` MUST be a strict subset
   of the `topology_owner`'s grants as defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
   Insufficient attenuation MUST be rejected with `topology.directive.unauthorized`.
10. **Resource limit check**: The topology MUST NOT exceed the
    implementation-defined maximum number of nodes per topology.
    Exceeding limits MUST be rejected with `topology.directive.exhausted-nodes`.

> **Non-normative note.**
Topology directive validation is designed to fail fast: the host MUST
reject invalid directives before creating any partial state.
This is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

### No durable live handles

> **Normative definition.**
The host MUST NOT persist any live actor handle, process ID, network
endpoint, or other transient resource identifier in the durable topology.
Schema validation MUST reject topology directives that include such fields.

> **Normative definition.**
The following fields are NOT permitted in the durable topology:

| Field | Reason |
|-------|--------|
| `actor_handle` | Live actor handles are transient and cannot be reconstructed from durable state. |
| `process_id` | Process IDs are assigned by the OS and are not durable. |
| `network_endpoint` | Network endpoints may change due to host migration or network reconfiguration. |
| `live_agent_id` | Live agent IDs are assigned at reconciliation time, not at topology creation time. |

> **Non-normative note.**
This invariant ensures that durable topology is always reconstructable
from a clean state without relying on transient live placement.
It is a core requirement of the recovery clustering seams defined in
section 39.1.

### No cross-tenant routes, relationships, grants, or results

> **Normative definition.**
The host MUST NOT accept topology directives that grant cross-tenant
routing, relationship, grant, or result access.
Capability policy enforcement MUST reject such directives with
`topology.directive.unauthorized`.

> **Normative definition.**
The following cross-tenant patterns are NOT permitted:

| Pattern | Description | Diagnostic |
|---------|-------------|------------|
| `cross-tenant-route` | A topology node routes signals to an agent outside its tenant. | `topology.directive.unauthorized` |
| `cross-tenant-relationship` | A topology node creates a relationship with an agent outside its tenant. | `topology.directive.unauthorized` |
| `cross-tenant-grant` | A topology node grants capabilities to an agent outside its tenant. | `topology.directive.unauthorized` |
| `cross-tenant-result` | A topology node accepts results from an agent outside its tenant. | `topology.directive.unauthorized` |

> **Non-normative note.**
This invariant is enforced by the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
Cross-tenant access MUST be mediated by explicit capability grants,
not by topology structure.

### Resource bounding under coordination load

> **Normative definition.**
The host MUST enforce the following resource bounds during reconciliation:

| Resource | Bound | Enforcement |
|----------|-------|-------------|
| `mailbox_queue_size` | Each live agent's mailbox queue MUST NOT exceed the implementation-defined maximum. | Mailbox lease enforcement. |
| `concurrent_agents` | The total number of live agent instances MUST NOT exceed the implementation-defined maximum. | Resource limit enforcement. |
| `retries_per_node` | Each topology node's retry count MUST NOT exceed the implementation-defined maximum. | Lifecycle policy enforcement. |
| `concurrent_leases` | The total number of active activation leases MUST NOT exceed the implementation-defined maximum. | Resource limit enforcement. |
| `cancellation_outstanding` | Each topology node's cancellation outstanding count MUST NOT exceed the implementation-defined maximum. | Lifecycle policy enforcement. |
| `result_retention` | Each topology node's result retention MUST NOT exceed the implementation-defined maximum. | Lifecycle policy enforcement. |

> **Non-normative note.**
Resource bounding ensures that the host does not exhaust system resources
under coordination load.
These bounds are documented in the implementation's conformance profile
as defined in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

### Reconciliation behavior

> **Normative definition.**
Reconciliation is triggered by the following events:

| Event | Trigger | Reconciliation scope |
|-------|---------|---------------------|
| `topology.directive.admitted` | A new topology version is admitted. | Full reconciliation. |
| `topology.lease.expired` | An activation lease expires. | Reconciliation for the affected `node_id`. |
| `topology.node.failed` | A live agent instance fails. | Reconciliation for the affected `node_id`. |
| `topology.node.stale` | A live agent instance becomes stale. | Reconciliation for the affected `node_id`. |
| `host.restart` | The host restarts. | Full reconciliation from durable topology. |

> **Normative definition.**
Each reconciliation pass applies the rules defined in section 39.1 in
order: missing, extra, failed, stale, moved (deferred), incompatible,
dependency-blocked.
The host MUST apply each rule to all nodes before moving to the next rule.

> **Non-normative note.**
Reconciliation is designed to be deterministic: given the same durable
topology and observed status, the host MUST produce the same live
placement.
This enables replay and testing.

### Live agent lifecycle under failure

> **Normative definition.**
Live agent lifecycle under failure is governed by the node's
`lifecycle_policy`:

| Policy | Behavior on failure |
|--------|---------------------|
| `terminate-on-topology-revoke` | Terminate the live agent instance immediately. |
| `wait-completion-on-topology-revoke` | Allow the live agent instance to complete its current turn, then terminate. |
| `allow-partial-on-topology-revoke` | Allow the live agent instance to complete its current turn, but exclude its results from topology aggregation. |

> **Normative definition.**
When a live agent instance fails, the host MUST:

1. Mark the node as `failed` in observed status.
2. Emit a `topology.node.terminated` evidence record.
3. Apply the node's `lifecycle_policy` to determine the next action:
   - If `terminate-on-topology-revoke`: terminate the live agent and
     mark the node as `terminated`.
   - If `wait-completion-on-topology-revoke`: wait for the current turn
     to complete, then terminate.
   - If `allow-partial-on-topology-revoke`: allow the current turn to
     complete, but mark the node as `partial` and exclude results from
     aggregation.
4. Emit a `topology.reconciliation.completed` or `topology.reconciliation.failed`
   evidence record.

> **Non-normative note.**
Live agent failure handling is non-transactional: if the host fails after
marking the node as `failed` but before emitting evidence, the next
reconciliation pass will detect the inconsistency and retry.
This is consistent with the atomic journal contract defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

### Recovery from clean state

> **Normative definition.**
Upon host restart, the host MUST reconstruct live placement from durable
topology by performing a full reconciliation.
The host MUST NOT rely on any transient state from before the restart.

> **Normative definition.**
The reconstruction process is:

1. Read the current durable topology version from the journal.
2. Read the current observed status from the journal.
3. Apply the reconciliation rules defined in section 39.1 to create live
   agent instances for missing nodes and terminate extra nodes.
4. Update observed status to reflect the new live placement.
5. Emit evidence records for all created and terminated nodes.

> **Non-normative note.**
Recovery from clean state is the primary mechanism for ensuring that
live placement is always consistent with durable topology.
This is consistent with the durable journal contract defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

### Adapter contract for horizontal coordination

> **Normative definition.**
Phase 5 defines the single-node placement contract.
Horizontal coordination across multiple hosts is deferred to Milestone 7.
The following adapter contract is defined for future implementation:

| Interface | Description | Status |
|-----------|-------------|--------|
| `lease.transfer` | Transfer an activation lease to another host. | Deferred to Milestone 7. |
| `topology.distribute` | Distribute a topology directive to multiple hosts. | Deferred to Milestone 7. |
| `reconciliation.coordinator` | Coordinate reconciliation across multiple hosts. | Deferred to Milestone 7. |

> **Non-normative note.**
The adapter contract defines the interfaces that Milestone 7 MUST implement
to enable horizontal coordination.
These interfaces are not implemented in Phase 5 but are defined here for
forward compatibility.

### Evidence emission

> **Normative definition.**
The host MUST emit evidence for the following events:

| Event | Evidence type | Description |
|-------|---------------|-------------|
| Topology directive admitted | `topology.directive.admitted` | A topology directive is admitted. |
| Topology directive rejected | `topology.directive.rejected` | A topology directive is rejected. |
| Reconciliation started | `topology.reconciliation.started` | A reconciliation pass starts. |
| Reconciliation completed | `topology.reconciliation.completed` | A reconciliation pass completes successfully. |
| Reconciliation failed | `topology.reconciliation.failed` | A reconciliation pass fails. |
| Reconciliation cancelled | `topology.reconciliation.cancelled` | A reconciliation pass is cancelled. |
| Node created | `topology.node.created` | A live agent instance is created for a topology node. |
| Node terminated | `topology.node.terminated` | A live agent instance is terminated. |
| Node restarted | `topology.node.restarted` | A live agent instance is restarted after failure. |
| Node cancelled | `topology.node.cancelled` | A topology node is cancelled. |
| Lease issued | `topology.lease.issued` | An activation lease is issued. |
| Lease expired | `topology.lease.expired` | An activation lease expires. |
| Lease renewed | `topology.lease.renewed` | An activation lease is renewed. |

> **Non-normative note.**
Topology audit evidence ensures that topology changes are fully auditable.
Evidence is recorded in the durable audit log as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 5 behavior and integration would invalidate
an earlier milestone assumption:

1. **Topology requires shared mutable guest state**: If topology nodes
   require shared mutable guest state, this would invalidate the
   assumption defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   that all state transitions are deterministic and replayable.
2. **Topology bypasses the durable journal**: If topology directives
   bypass the durable journal, this would invalidate the assumption
   defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   that all state transitions are durable across host restarts.
3. **Topology allows cross-tenant authority leaks**: If durable topology
   records grant cross-tenant routing, relationship, grant, or result
   access, this would invalidate the assumption defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant.

> **Non-normative note.**
These results would indicate a design flaw in Phase 5 and would require
a revision of the Phase 5 contracts before promotion to `status:
normative`.

### Cross-references and precedence

> **Non-normative note.**
This section's behavior and integration integrate with the following
earlier chapters:

1. For topology directive validation: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of topology-specific validation behavior.
2. For resource bounding: this section takes precedence over
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   for questions of topology-specific resource bounds.
3. For live agent failure handling: this section takes precedence over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of topology-specific failure handling.
4. For recovery from clean state: this section takes precedence over
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md)
   for questions of topology-specific recovery behavior.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
