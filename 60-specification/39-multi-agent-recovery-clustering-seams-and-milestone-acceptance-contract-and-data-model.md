---
title: "Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-05
  - recovery
  - clustering
  - seams
  - milestone-acceptance
aliases:
  - "M6-P5 Contract And Data Model"
---

# Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-05-multi-agent-recovery-clustering-seams-and-milestone-acceptance.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the contract and data model for multi-agent recovery clustering
seams and milestone acceptance, including durable topology, recovery clustering,
activation lease semantics under failure, and the evidence requirements for
milestone acceptance.

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
[Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests](38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md).

## 39.1 Contract And Data Model

### Durable topology and desired state

> **Normative definition.**
The durable topology is the authoritative record of desired agent placement
across a multi-agent coordination graph.
It is derived from topology directives submitted by authorized principals
and is reconciled into live placement by the host.
The durable topology is immutable once committed; new versions are created
by submitting new topology directives, never by mutating existing records.

> **Normative definition.**
Every topology MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `topology_version` | A monotonic integer version of the topology. | Topology directive. |
| `topology_sequence` | The monotonic per-owner-scope `u64` sequence reserved for this distinct topology directive; system principals use the single system scope. | Topology directive. |
| `topology_identity` | The fixed `topology:sha256:<hex>` identity derived from `topology_version`, `topology_owner`, and `topology_sequence`. | Topology directive construction. |
| `topology_owner` | The `AddressablePrincipal` that owns the topology. Agents use `TenantQualifiedAgentAddress`; non-agent owners use `PrincipalAddress`. | Topology directive. |
| `nodes` | A list of topology nodes that define the desired placement. | Topology directive. |
| `created_at` | The ISO 8601 timestamp of topology creation. | Topology directive. |
| `updated_at` | The ISO 8601 timestamp of the last topology revision. | Topology directive. |
| `grants` | The attenuated grants for the topology, strictly a subset of `topology_owner`'s grants. | Topology directive. |
| `purpose` | A human-readable description of the topology's purpose. | Topology directive. |
| `status` | The current status: `active`, `revoked`, or `archived`. | Host runtime. |

> **Normative definition.**
Topology nodes are defined in
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md)
section 38.1.
Phase 5 reuses the Phase 4 node schema without deviation.
The `node_id` is derived deterministically from `topology_version`,
`role`, `agent_address`, and position index as defined in Phase 4.
The `topology_identity`, `node_id`, and retransmission sequence semantics MUST
use the exact domain-separated, length-prefixed SHA-256 constructions in
[Pod-like topology nodes](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md#pod-like-topology-nodes)
and
[Desired topology, observed status, and live placement](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md#desired-topology-observed-status-and-live-placement).

> **Non-normative note.**
The `updated_at` field is set by the host at topology admission (not from
the directive's timestamp) and is updated each time a new topology version
is committed.
This ensures that `updated_at` always reflects the most recent durable
revision, regardless of the directive's original timestamp.

> **Non-normative note.**
The durable topology is stored in the durable journal as defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
Each topology version is committed atomically through the atomic commit
protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

### Recovery clustering seams

> **Normative definition.**
Recovery clustering seams are the boundaries between the durable topology
and the live agent instances that execute the topology's desired state.
These seams define when and how live placement is reconstructed from
durable topology after actor, host, or coordinator failures.

> **Normative definition.**
Every recovery clustering seam MUST satisfy the following invariants:

| Invariant | Description | Enforcement |
|-----------|-------------|-------------|
| `no-durable-live-handles` | No live actor handle, process ID, or network endpoint is stored in the durable topology. | Schema validation at topology admission. |
| `topology-only-identities` | The durable topology contains only logical identities, relationships, and lifecycle policies. | Schema validation at topology admission. |
| `no-cross-tenant-routes` | No durable topology record grants cross-tenant routing, relationship, grant, or result access. | Capability policy enforcement at topology admission. |
| `bounded-mailboxes` | Live agent mailboxes are bounded by the mailbox contract and do not leak across topology boundaries. | Mailbox lease enforcement at reconciliation. |
| `bounded-concurrency` | Live agent concurrency is bounded by the topology's resource class and disclosed implementation limits under [Resource bounding under coordination load](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md#resource-bounding-under-coordination-load). | Resource limit enforcement at reconciliation. |
| `bounded-retries` | Live agent retry counts are bounded by the node's `lifecycle_policy` and disclosed implementation limits under [Resource bounding under coordination load](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md#resource-bounding-under-coordination-load). | Lifecycle policy enforcement at reconciliation. |

> **Non-normative note.**
Recovery clustering seams ensure that durable topology is always
reconstructable from a clean state without relying on transient live
placement.
This is consistent with the durable journal contract defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
and the single-agent host flow defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).

### Activation lease semantics under failure

> **Normative definition.**
Activation leases fence live placement authority for a single `node_id`.
They are time-bounded and renewable.
Under failure, leases are automatically revoked on the failed host.

> **Normative definition.**
Every activation lease MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `lease_id` | The fixed Chapter 38 lease identity derived from `topology_identity`, `node_id`, `host_id`, and `lease_sequence`. | Host runtime. |
| `lease_sequence` | The monotonic `u64` sequence reserved by the issuing host service. | Host runtime. |
| `topology_identity` | The deterministic identity of the topology that authorizes the lease. | Topology directive. |
| `node_id` | The `node_id` of the topology node this lease authorizes. | Topology directive. |
| `host_id` | The `PrincipalAddress` with `kind: "service"` of the host that holds the lease. | Host runtime. |
| `fence_token` | A deterministic fence token that increases monotonically for each lease issued for the same `node_id`. | Host runtime. |
| `issued_at` | The ISO 8601 timestamp of lease issuance. | Host clock. |
| `expires_at` | The ISO 8601 timestamp of lease expiration. | Host clock. |
| `lease_type` | The lease type: `create`, `update`, `terminate`, or `reconcile`. | Host runtime. |

The `lease_id`, `lease_sequence`, issuance, and renewal identity semantics MUST
be exactly those in
[Activation leases](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md#activation-leases).

> **Normative definition.**
Activation leases are time-bounded: a lease MUST expire 30 seconds after
`issued_at` unless renewed.
Expiration is enforced by the host at the next reconciliation pass.

> **Non-normative note.**
Lease expiration is a safety mechanism that prevents stale live placement
from persisting indefinitely after a host crash or network partition.
The host MUST detect expired leases and mark the corresponding nodes as
`stale` for reconciliation.

> **Normative definition.**
A lease MAY be renewed by the same host that issued it.
Renewal extends the `expires_at` timestamp but does NOT increment the
`fence_token`.
The renewed `expires_at` MUST be exactly 30 seconds after the host accepts the
renewal; `lease_id`, `lease_sequence`, `host_id`, and `fence_token` remain
unchanged.
Renewal is not transactional: if renewal fails after journal commit, the
host MUST record the failure in observed status and retry on the next
reconciliation pass.

> **Normative definition.**
The first lease issued for a `node_id` has `fence_token: 1`. A distinct lease
issued after the previous lease expires or is revoked MUST reserve a new
`lease_sequence` and increment `fence_token` by exactly one. Renewal is not a
distinct issuance and does not increment the token.

> **Normative definition.**
A lease MUST NOT be transferred to another host in version `0.1.0`.
A transfer request MUST fail with `topology.lease.transfer-unsupported` and
leave the current lease unchanged. Lease transfer is deferred to Milestone 7.

> **Non-normative note.**
Lease transfer is essential for fault tolerance in multi-node deployments:
if a host crashes while holding an active lease, the lease is automatically
revoked on the crashed host; the target host MUST issue a new lease to
take over placement authority.
Under single-node placement, fault tolerance is provided by the durable journal, which
allows live placement to be reconstructed from desired topology on restart.

### Reconciliation under failure

> **Normative definition.**
Reconciliation is the deterministic process that turns desired topology
into live placement.
Under failure, reconciliation is the sole mechanism for reconstructing
live placement from durable topology.

> **Normative definition.**
Reconciliation applies the following rules in order:

1. **Missing nodes**: For each node in desired topology that is NOT
   present in live placement, create a live agent instance according to
   the node's `activation_mode`.
2. **Extra nodes**: For each node in live placement that is NOT present
   in desired topology, terminate the live agent instance.
3. **Failed nodes**: For each node in live placement whose live agent
   instance has failed, apply the node's `lifecycle_policy` to determine
   whether to restart, wait, or allow partial results.
4. **Stale nodes**: For each node in live placement whose activation lease
   has expired, mark the node as `stale` and apply the node's
   `lifecycle_policy` to determine whether to restart, wait, or allow
   partial results.

> **Non-normative note.**
Rules 5-7 below are deferred to Milestone 7 for multi-node placement:

5. **Moved nodes**: For each node in live placement that has been moved
   to a different host, update the observed status to reflect the new
   host and refresh the activation lease.
6. **Incompatible nodes**: For each node in live placement whose
   `agent_address` no longer resolves to an active agent, mark the node
   as `incompatible` and terminate the live agent instance.
7. **Dependency-blocked nodes**: For each node in desired topology whose
   `dependencies` are not yet satisfied, defer creation until dependencies
   are resolved.

> **Normative definition.**
Reconciliation is atomic with respect to the durable journal: the journal
entries recording the desired topology version, observed status updates,
and evidence records produced by a single reconciliation pass MUST be
committed atomically through the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
If the journal commit fails, the entire reconciliation pass is rolled back
and observed status is updated with the failure diagnostic.
Live agent creation and termination are NOT transactional; if a live agent
creation fails after journal commit, the host MUST record the failure in
observed status and retry on the next reconciliation pass.

> **Non-normative note.**
Atomic journal reconciliation ensures that the durable record of topology
state is always consistent.
Live agent creation involves host OS operations (process spawning, resource
allocation) that are not naturally transactional and cannot be rolled back.
The journal provides a recovery point: if live agent creation fails after
journal commit, the next reconciliation pass will detect the inconsistency
and retry or mark the node as failed.

### Topology versioning and rollback

> **Normative definition.**
Topology versions are monotonic integers that increase with each new
topology directive.
A new topology directive with a `topology_version` greater than the current
maximum version is admitted; a directive with a duplicate or lower version
is rejected with `topology.directive.duplicate-version`.

> **Normative definition.**
Rollback to a previous topology version is NOT supported.
To "roll back" to a previous topology, the operator MUST create a new
topology directive that copies the desired nodes from the previous version
and submit it with a new `topology_version`.

> **Non-normative note.**
This design avoids the complexity of tracking topology history and
rollback semantics.
Operators that need rollback capability MUST implement it at the
topology directive level by creating new directives that reference
previous topology nodes.

### Milestone acceptance evidence

> **Normative definition.**
Milestone acceptance requires the following evidence:

| Evidence | Description | Source |
|----------|-------------|--------|
| `phase-5-integration-tests-passing` | All Phase 5 integration tests pass with the expected diagnostics and evidence. | Phase 5 integration tests. |
| `cross-milestone-fixtures-passing` | All earlier milestone fixtures that are affected by Phase 5 contracts continue to pass. | Cross-milestone compatibility tests. |
| `no-cross-tenant-leaks` | No durable topology record grants cross-tenant routing, relationship, grant, or result access. | Failure handling tests. |
| `recovery-from-clean-state` | Live placement is correctly reconstructed from durable topology after simulated host restart. | Recovery flow tests. |
| `bounded-resources` | Live agent mailboxes, concurrency, retries, and leases are bounded by disclosed implementation limits under [Resource bounding under coordination load](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md#resource-bounding-under-coordination-load). | Resource limit tests. |

> **Non-normative note.**
Milestone acceptance evidence ensures that Phase 5 contracts are
correctly implemented and do not introduce regressions in earlier
milestones.
The evidence is the primary input for promotion from `status: candidate`
to `status: normative`.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 5 would invalidate an earlier milestone
assumption:

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
3. **Topology bypasses the atomic commit protocol**: If topology
   directives bypass the atomic commit protocol, this would invalidate
   the assumption defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   that all state transitions are atomic.
4. **Topology allows cross-tenant authority leaks**: If durable topology
   records grant cross-tenant routing, relationship, grant, or result
   access, this would invalidate the assumption defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant.

> **Non-normative note.**
These results would indicate a design flaw in Phase 5 and would require
a revision of the Phase 5 contracts before promotion to `status:
normative`.
Implementations MUST NOT deviate from the contracts defined in this
chapter without evidence from a corresponding revision.

### Cross-references and precedence

> **Non-normative note.**
This section's contract and data model integrate with the following
earlier chapters:

1. For topology directive and node validation: this section takes
   precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of topology-specific validation.
2. For topology directive and node atomic commits: this section takes
   precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of topology-specific atomic commit behavior.
3. For activation lease fencing: this section takes precedence over
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   for questions of topology-specific lease semantics.
4. For recovery from clean state: this section takes precedence over
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md)
   for questions of topology-specific recovery behavior.
5. For cross-tenant isolation: this section takes precedence over
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   for questions of topology-specific authority bounds.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
