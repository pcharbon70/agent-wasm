---
title: "Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-04
  - pod-topology
  - placement
  - activation-leases
  - reconciliation
  - failure-evidence
aliases:
  - "M6-P4 Failure Evidence And Operational Notes"
---

# Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-04-pod-topology-placement-activation-leases-and-reconciliation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the failure evidence and operational notes for pod topology
placement activation leases and reconciliation, including failure outcomes,
bounded diagnostics, evidence emission, and profiled configuration.

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
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md).

## 38.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The following failure outcomes are normative invariants that every
host implementation MUST handle correctly for pod topology placement
activation leases and reconciliation.
Each outcome describes a specific failure condition and the expected
host behavior.

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.malformed` | Topology directive with missing required fields. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-nodes` | Topology directive with empty or invalid `nodes` list. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-node-id` | Topology directive with invalid `node_id` format. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-agent-address` | Topology directive with invalid `agent_address` format. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-role` | Topology directive with unknown `role` value. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-activation-mode` | Topology directive with unknown `activation_mode` value. | Reject directive; do NOT create partial topology state. |
| `topology.directive.malformed-lifecycle-policy` | Topology directive with unknown `lifecycle_policy` value. | Reject directive; do NOT create partial topology state. |
| `topology.node.malformed` | Topology node with missing required fields. | Reject node; do NOT create partial node state. |
| `topology.node.malformed-dependencies` | Topology node with invalid `dependencies` list. | Reject node; do NOT create partial node state. |
| `topology.lease.malformed` | Activation lease with missing required fields. | Reject lease; do NOT apply lease. |
| `topology.lease.malformed-expiry` | Activation lease with past or invalid `expires_at` timestamp. | Reject lease; do NOT apply lease. |

> **Non-normative note.**
Malformed outcomes are caused by invalid input data.
The host MUST reject malformed input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.incompatible-agent` | Topology directive whose `agent_address` does not resolve to an active agent in the durable registry. | Reject directive; do NOT create partial topology state. |
| `topology.node.incompatible-agent` | Topology node whose `agent_address` does not resolve to an active agent in the durable registry. | Mark node as `incompatible`; do NOT create live agent instance. |
| `topology.node.incompatible-dependency` | Topology node whose `dependencies` reference non-existent `node_id` values. | Reject node; do NOT create partial node state. |
| `topology.node.incompatible-circular-dependency` | Topology directive whose `nodes` list contains a circular dependency. | Reject directive; do NOT create partial topology state. |
| `topology.node.incompatible-resource-class` | Topology node whose `resource_class` is not `default`. | Reject node; do NOT create partial node state. |
| `topology.lease.transfer-unsupported` | A request attempts to transfer a lease between hosts in version `0.1.0`. | Reject transfer; preserve the current lease unchanged. |

> **Non-normative note.**
Incompatible outcomes are caused by input data that is structurally valid
but semantically inconsistent with the topology or node.
The host MUST reject incompatible input without creating partial state,
which is consistent with the validation rules defined in
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md).

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.duplicate-version` | Topology directive with `topology_version` that matches an already-admitted version. | Reject directive; do NOT create partial topology state. |
| `topology.node.duplicate-node-id` | Two topology directives with the same `node_id` submitted concurrently. | Reject second directive; do NOT create partial node state. |
| `topology.lease.expired-fence` | Activation lease with `fence_token` less than the current fence token for the same `node_id`. | Reject lease; do NOT apply lease. |
| `topology.reconciliation.conflict` | Two reconciliation passes attempt to modify the same `node_id` concurrently. | Reject second reconciliation pass; do NOT apply updates. |

> **Non-normative note.**
Conflicting outcomes are caused by concurrent or duplicate requests.
The host MUST reject conflicting input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.unauthorized` | Topology directive whose `topology_owner` does not have the `topology.directive.create` capability. | Reject directive; do NOT create partial topology state. |
| `topology.node.unauthorized` | Topology node whose `owner` does not have the `topology.node.create` capability. | Reject node; do NOT create partial node state. |
| `topology.lease.unauthorized` | Activation lease whose `host_id` does not have the `topology.lease.acquire` capability. | Reject lease; do NOT apply lease. |

> **Non-normative note.**
Unauthorized outcomes are caused by principals that lack the required
capabilities.
The host MUST reject unauthorized requests without creating partial
state, which is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.exhausted-nodes` | Topology directive would exceed the disclosed maximum-nodes implementation limit under [Implementation limits](#implementation-limits). | Reject directive; do NOT create partial topology state. |
| `topology.node.exhausted-concurrency` | Topology node would exceed the disclosed topology-concurrency implementation limit under [Implementation limits](#implementation-limits). | Reject node; do NOT create partial node state. |
| `topology.lease.exhausted-concurrency` | Host would exceed the disclosed concurrent-leases implementation limit under [Implementation limits](#implementation-limits). | Reject lease; do NOT apply lease. |
| `topology.directive.timeout` | Topology directive validation exceeded 30 seconds. | Reject directive; do NOT create partial topology state. |
| `topology.lease.expired-timeout` | An admitted activation lease reached its `expires_at` timestamp. | Reject use of the expired lease; do NOT apply it. |

> **Non-normative note.**
Exhausted outcomes are caused by resource limits.
The host MUST reject exhausted requests without creating partial state,
which is consistent with the resource limits defined in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `topology.directive.unavailable` | Topology directive whose `topology_owner` does not resolve as active in the agent or principal registry selected by its address discriminant. | Reject directive; do NOT create partial topology state. |
| `topology.node.unavailable-agent` | Topology node whose `agent_address` is not active in the durable registry. | Mark node as `unavailable`; do NOT create live agent instance. |
| `topology.lease.unavailable-host` | Activation lease whose `host_id` is not active in the host registry. | Reject lease; do NOT apply lease. |

> **Non-normative note.**
Unavailable outcomes are caused by principals or hosts that are not active.
The host MUST reject unavailable requests without creating partial
state, which is consistent with the agent registry contract defined in
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).

### Bounded diagnostics and evidence

> **Normative definition.**
The host MUST emit bounded diagnostics and evidence for every failure
outcome.
Diagnostics identify the phase contract, profile, and failed boundary
without exposing secrets.
Evidence is recorded in the durable audit log as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Every diagnostic MUST use exactly the Chapter 04 `Diagnostic` top-level
structure. The listed topology diagnostic is `code`, `severity` is `error`,
and `details` contains `phase`, `section`, `contract`, `profile`,
`failed_boundary`, `timestamp`, `retryable`, `topology_identity`, `node_id`,
and `lease_id`; inapplicable identifiers are JSON `null`.

| Failure category | Family |
|------------------|--------|
| Malformed | `identity.validation.topology` |
| Incompatible | `identity.compatibility.topology` |
| Conflicting | `identity.conflict.topology` |
| Unauthorized | `identity.authorization.topology` |
| Exhausted | `identity.limit.topology` |
| Unavailable | `identity.resource.topology` |

The code has the family of the failure-outcome table containing it. No
additional top-level diagnostic member is permitted.

> **Non-normative note.**
The bounded diagnostic format ensures that diagnostics are consistent,
auditable, and actionable.
The `phase`, `section`, `contract`, `profile`, and `failed_boundary`
fields enable operators to quickly identify the source and context
of a failure.
The `message` field provides a human-readable description that enables
operators to understand the failure and take corrective action.

> **Normative definition.**
Every evidence record MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_type` | The evidence type (`topology.directive.admitted`, `topology.directive.rejected`, `topology.reconciliation.started`, `topology.reconciliation.completed`, `topology.reconciliation.failed`, `topology.node.created`, `topology.node.terminated`, `topology.node.restarted`). | Host runtime. |
| `topology_identity` | The deterministic topology identity. | Host runtime. |
| `node_id` | The `node_id` of the topology node, if applicable. | Host runtime. |
| `lease_id` | The `lease_id` of the activation lease, if applicable. | Host runtime. |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock. |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime. |

> **Non-normative note.**
The evidence record format ensures that all topology events are auditable
and tamper-evident.
The `evidence_digest` field enables downstream systems to verify that
the evidence record has not been tampered with after creation.
This is consistent with the provenance and audit contract defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Implementation limits

> **Normative definition.**
The following resource ceilings are implementation limits. A conforming host
MUST publish each positive limit in its conformance profile and use the listed
diagnostic when otherwise valid work exceeds it. Lease expiry and stale-node
detection are fixed at 30 and 60 seconds respectively.

| Limit | Constraint | Exhaustion diagnostic |
|-------|------------|-----------------------|
| Maximum nodes per topology | Positive integer disclosed in the conformance profile. | `topology.directive.exhausted-nodes` |
| Maximum concurrency per topology | Positive integer disclosed in the conformance profile. | `topology.node.exhausted-concurrency` |
| Maximum concurrent leases | Positive integer disclosed in the conformance profile. | `topology.lease.exhausted-concurrency` |

> **Non-normative note.**
These limits bound resource admission without changing topology, lease, or
stale-node semantics.

### Deferred work

> **Normative definition.**
The following work is deferred to future phases or milestones:

1. **Multi-node placement**: Topology nodes distributed across multiple
   host processes or nodes are deferred to Milestone 7.
2. **Distributed reconciliation**: Reconciliation across multiple hosts
   requires distributed consensus and is deferred to Milestone 7.
3. **Topology priority**: Prioritizing topology directives for resource
   allocation is deferred to Milestone 7.
4. **Topology cost tracking**: Tracking the cost of topology nodes for
   billing or resource accounting is deferred to Milestone 7.
5. **Lease transfer**: Transferring an activation lease between hosts is
   deferred to Milestone 7.

> **Non-normative note.**
The deferred work above is not within the scope of Phase 4 but may
be addressed in future phases.
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 4 would invalidate an earlier milestone
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

> **Non-normative note.**
These results would indicate a design flaw in Phase 4 and would require
a revision of the Phase 4 contracts before promotion to `status:
normative`.
Implementations MUST NOT deviate from the contracts defined in this
chapter without evidence from a corresponding revision.

### Cross-references and precedence

> **Non-normative note.**
This section's failure evidence and operational notes integrate with the
following earlier chapters:

1. For failure diagnostics: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of topology-specific diagnostic format.
2. For evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of topology-specific evidence record format.
3. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of topology-specific capability enforcement.
4. For resource limits: this section takes precedence over
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   for questions of topology-specific resource limits.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
