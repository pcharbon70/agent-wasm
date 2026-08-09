---
title: "Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-04
  - pod-topology
  - placement
  - activation-leases
  - reconciliation
  - reconciliation-behavior
aliases:
  - "M6-P4 Behavior And Integration"
---

# Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-04-pod-topology-placement-activation-leases-and-reconciliation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the behavior and integration rules for pod topology
placement activation leases and reconciliation, including activation lease
fencing, deterministic reconciliation, topology versioning, and audit
evidence.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
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
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md).

## 38.2 Behavior And Integration

### Activation leases

> **Normative definition.**
An activation lease is a host-owned, time-bounded fence that grants a
reconciliation pass exclusive authority to modify live placement for a
specific topology node.
Activation leases prevent split-brain placement, concurrent reconciliation
collisions, and orphaned live agents.

> **Normative definition.**
Every activation lease MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `lease_id` | A deterministic lease identity derived from the topology identity, `node_id`, and a monotonic per-host sequence counter. | Host runtime. |
| `topology_identity` | The deterministic topology identity. | Host runtime. |
| `node_id` | The `node_id` of the topology node that this lease authorizes placement for. | Host runtime. |
| `host_id` | The implementation-defined identifier of the host that holds this lease. | Host runtime. |
| `issued_at` | The ISO 8601 timestamp of lease issuance. | Host clock. |
| `expires_at` | The ISO 8601 timestamp of lease expiration. | Host clock. |
| `lease_type` | The lease type: `create`, `update`, `terminate`, or `reconcile`. | Host runtime. |
| `fence_token` | A deterministic fence token that increases monotonically for each lease issued for the same `node_id`; older leases are rejected with this token. | Host runtime. |

> **Normative definition.**
Activation leases are time-bounded: a lease MUST expire after a maximum
duration defined in the implementation-defined lease timeout.
If a reconciliation pass does not complete before the lease expires, the
lease is automatically revoked and the host MUST NOT use the expired lease
to modify live placement.

> **Normative definition.**
Activation leases are fenced: a reconciliation pass MUST NOT apply a lease
whose `fence_token` is less than the current `fence_token` recorded in
observed status for the same `node_id`.
Fenced leases are rejected with the diagnostic `topology.lease.expired-fence`.

> **Non-normative note.**
Fencing prevents split-brain placement: if two reconciliation passes issue
leases for the same node concurrently, only the lease with the higher
`fence_token` is applied; the other is rejected.
This ensures that only one reconciliation pass has authority over a given
node at any time.

> **Normative definition.**
Activation leases are renewable: a reconciliation pass MAY renew an
active lease before expiration by issuing a new lease with the same
`lease_id` and an incremented `fence_token`.
Renewed leases extend the lease's `expires_at` timestamp.

> **Normative definition.**
Activation leases are transferable: a reconciliation pass MAY transfer
an active lease to another host by revoking the current lease and issuing
a new lease on the target host.
Transfer is used for host failover: if the host holding a lease crashes,
the target host MUST issue a new lease with an incremented `fence_token`
to take over placement authority.

> **Non-normative note.**
Lease transfer is essential for fault tolerance: if a host crashes while
holding an active lease, the lease is automatically revoked on the crashed
host; the target host MUST issue a new lease to take over placement
authority.
This ensures that placement is never lost due to host crashes.

### Reconciliation of missing, extra, failed, stale, moved, incompatible, and dependency-blocked agents

> **Normative definition.**
Reconciliation is the deterministic process that turns desired topology
into live placement by applying the following rules in order:

1. **Missing nodes**: For each node in desired topology that is NOT
   present in live placement, create a live agent instance according to
   the node's `activation_mode`.
   If the node has unmet dependencies (nodes in `missing` or `failed`
   state), defer creation until dependencies are resolved; the node is
   marked as `dependency-blocked`.

2. **Extra nodes**: For each node in live placement that is NOT present
   in desired topology, terminate the corresponding live agent instance.
   If the node is part of an active fan-out plan, apply the plan's
   `cancellation_policy` to determine whether to cancel, wait, or allow
   partial results.

3. **Failed nodes**: For each node in live placement that has failed,
   apply the node's `lifecycle_policy` to determine whether to restart,
   wait, or allow partial results:
   - `terminate-on-topology-revoke`: Do NOT restart; the node is
     removed from live placement.
   - `wait-completion-on-topology-revoke`: Wait for the node to complete
     its current work before removing from live placement.
   - `allow-partial-on-topology-revoke`: Allow the node to continue
     executing; do NOT include its results in aggregated results.

4. **Stale nodes**: For each node in live placement whose live state has
   not been refreshed within the implementation-defined stale timeout,
   mark the node as `stale` and apply the node's `lifecycle_policy` to
   determine whether to restart, wait, or allow partial results.

5. **Moved nodes**: For each node in live placement that has been moved
   to a different host, update the observed status to reflect the new
   host and refresh the activation lease.

6. **Incompatible nodes**: For each node in desired topology whose
   `agent_address` does not resolve to an active agent in the durable
   registry, mark the node as `incompatible` and do NOT create a live
   agent instance.
   Emit a `topology.node.incompatible` event.

7. **Dependency-blocked nodes**: For each node in desired topology that
   has unmet dependencies, mark the node as `dependency-blocked` and do
   NOT create a live agent instance.
   Emit a `topology.node.dependency-blocked` event.

> **Non-normative note.**
Reconciliation is deterministic: the same desired topology and observed
status always produce the same live placement updates.
This ensures that reconciliation is replayable from the durable state
journal without depending on transient host memory.

> **Normative definition.**
Reconciliation is atomic: all live placement updates produced by a single
reconciliation pass MUST be applied atomically through the atomic commit
protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
If any update fails, the entire reconciliation pass is rolled back and
observed status is updated with the failure diagnostic.

> **Non-normative note.**
Atomic reconciliation ensures that live placement is always consistent
with desired topology.
Without atomic reconciliation, a partial reconciliation could leave the
system in an inconsistent state where some nodes are created but others
are not, leading to unpredictable behavior.

### Topology versioning, validation, rollout, rollback, and audit evidence

> **Normative definition.**
Topology versioning ensures that desired topology changes are
deterministic, auditable, and reversible.
Each topology directive creates a new topology version; topology versions
are monotonically increasing and immutable once recorded.

> **Normative definition.**
Topology versioning includes the following operations:

| Operation | Description |
|-----------|-------------|
| `create` | Create a new topology version with the specified nodes. |
| `update` | Update an existing topology version by adding, removing, or modifying nodes. |
| `rollback` | Roll back to a previous topology version by creating a new version that matches the previous version's nodes. |
| `validate` | Validate a topology version against the schema and invariant rules defined in this chapter. |

> **Non-normative note.**
Topology versioning ensures that topology changes are auditable and
reversible.
If a topology change introduces inconsistencies or failures, operators
can roll back to a previous version without losing desired topology
history.

> **Normative definition.**
Topology validation ensures that topology directives are structurally
valid and semantically consistent before admission.
The host MUST validate the following rules for every topology directive:

1. The `topology_owner` address MUST resolve to an active agent in the
   durable registry.
2. The `nodes` list MUST contain at least one node.
3. Each node's `agent_address` MUST resolve to an active agent in the
   durable registry.
4. Each node's `dependencies` list MUST reference `node_id` values that
   exist in the same topology version; circular dependencies MUST be
   rejected.
5. Each node's `activation_mode` MUST name a defined activation mode
   (`durable`, `ephemeral`, or `manual`).
6. Each node's `lifecycle_policy` MUST name a defined lifecycle policy
   (`terminate-on-topology-revoke`, `wait-completion-on-topology-revoke`,
   or `allow-partial-on-topology-revoke`).
7. A topology directive whose `topology_version` matches an already-
   admitted version (recorded in the durable state journal) MUST be
   rejected with the diagnostic `topology.directive.duplicate-version`.

> **Non-normative note.**
Topology validation ensures that topology directives are valid before
admission.
Circular dependency detection prevents infinite reconciliation loops;
activation mode and lifecycle policy validation ensures that nodes are
created and managed correctly.

> **Normative definition.**
Topology rollout and rollback are implemented through topology directives:

- **Rollout**: To rollout a new topology version, the operator submits
  a topology directive with the new topology version and updated nodes.
  The host validates the directive, creates the new topology version,
  and triggers reconciliation.

- **Rollback**: To rollback to a previous topology version, the operator
  submits a topology directive that copies the previous version's nodes
  into a new topology version.
  The host validates the directive, creates the new topology version,
  and triggers reconciliation.

> **Non-normative note.**
Topology rollout and rollback are implemented through topology directives
rather than special-purpose APIs.
This ensures that topology changes are consistent with the existing
directive validation and atomic commit protocol.

> **Normative definition.**
Topology audit evidence is emitted for every topology directive and
reconciliation pass through
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
The host MUST emit evidence for the following events:

| Evidence type | Trigger |
|---------------|---------|
| `topology.directive.admitted` | A topology directive passes validation and is admitted. |
| `topology.directive.rejected` | A topology directive fails validation and is rejected. |
| `topology.reconciliation.started` | A reconciliation pass starts. |
| `topology.reconciliation.completed` | A reconciliation pass completes successfully. |
| `topology.reconciliation.failed` | A reconciliation pass fails. |
| `topology.node.created` | A live agent instance is created for a topology node. |
| `topology.node.terminated` | A live agent instance is terminated. |
| `topology.node.restarted` | A live agent instance is restarted after failure. |

> **Non-normative note.**
Topology audit evidence ensures that topology changes are fully auditable.
Operators can reconstruct any topology execution sequence from the evidence
log alone.

### Cross-references and precedence

> **Non-normative note.**
This section's behavior and integration rules integrate with the following
earlier chapters:

1. For activation lease fencing: this section takes precedence over
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   for questions of topology-specific lease fencing semantics.
2. For topology reconciliation atomicity: this section takes precedence
   over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of topology-specific atomic commit steps.
3. For topology node lifecycle: this section takes precedence over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of topology node-specific lifecycle behavior.
4. For topology node fan-out coordination: this section takes precedence
   over
   [Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration](37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md)
   for questions of topology node-specific fan-out coordination.
5. For topology directive evidence emission: this section takes precedence
   over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of topology directive-specific evidence record format.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
