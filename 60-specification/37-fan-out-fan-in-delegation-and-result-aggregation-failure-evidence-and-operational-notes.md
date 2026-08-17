---
title: "Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-03
  - fan-out
  - fan-in
  - delegation
  - result-aggregation
  - failure-evidence
aliases:
  - "M6-P3 Failure Evidence And Operational Notes"
---

# Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-03-fan-out-fan-in-delegation-and-result-aggregation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the failure evidence and operational notes for fan-out
fan-in delegation and result aggregation, including failure outcomes,
bounded diagnostics, evidence emission, and profiled configuration.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
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
[Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests](37-fan-out-fan-in-delegation-and-result-aggregation-phase-3-integration-tests.md).

## 37.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The following failure outcomes are normative invariants that every
host implementation MUST handle correctly for fan-out plans.
Each outcome describes a specific failure condition and the expected
host behavior.

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.malformed` | Fan-out plan directive with missing required fields. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.malformed-work-items` | Fan-out plan directive with empty or invalid `work_items` list. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.malformed-concurrency-bound` | Fan-out plan directive with non-positive `concurrency_bound`. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.malformed-deadline` | Fan-out plan directive with past or invalid `deadline`. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.malformed-aggregation-policy` | Fan-out plan directive with unknown `aggregation_policy`. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.malformed-quorum` | Fan-out plan directive with `aggregation_policy: quorum` but invalid `quorum_threshold` (e.g., zero, negative, or greater than the number of work items). | Reject directive; do NOT create partial plan state. |
| `fanout.work-item.malformed` | Child work item with missing required fields. | Reject work item; do NOT create partial work item state. |
| `fanout.work-item.malformed-artifact` | Child work item with invalid artifact digest. | Reject work item; do NOT create partial work item state. |
| `fanout.work-item.malformed-manifest` | Child work item with invalid manifest digest. | Reject work item; do NOT create partial work item state. |
| `fanout.result.malformed` | Child result with missing required fields. | Reject result; do NOT aggregate. |
| `fanout.result.malformed-data` | Child result with invalid `result_data`. | Reject result; do NOT aggregate. |

> **Non-normative note.**
Malformed outcomes are caused by invalid input data.
The host MUST reject malformed input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.incompatible` | Fan-out plan `result_contract` names a schema version unsupported by the admitted work-item manifests. | Reject directive; do NOT create partial plan state. |
| `fanout.plan.incompatible-manifest-artifact` | Child work item with `manifest` digest that does not correspond to `artifact` digest. | Reject work item; do NOT create partial work item state. |
| `fanout.plan.incompatible-plan` | Child work item with `plan_id` that does not resolve to an active plan. | Reject work item; do NOT create partial work item state. |
| `fanout.result.incompatible-contract` | Child result that does not satisfy the parent plan's `result_contract`. | Reject result; do NOT aggregate. |

> **Non-normative note.**
Incompatible outcomes are caused by input data that is structurally valid
but semantically inconsistent with the parent plan or work item.
The host MUST reject incompatible input without creating partial state,
which is consistent with the validation rules defined in
[Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model](37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md).

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.duplicate-plan-id` | Fan-out plan directive with `plan_id` that matches an already-admitted plan. | Reject directive; do NOT create partial plan state. |
| `fanout.work-item.duplicate-work-item-id` | Two child work item directives with the same `work_item_id` submitted for the same plan. | Reject second directive; do NOT create partial work item state. |
| `fanout.result.duplicate` | Child result with `result_id` that matches a previously-aggregated result. | Reject result; do NOT aggregate. |
| `fanout.result.duplicate-content` | Child result with `work_item_id` and result payload hash that match a previously-aggregated result. | Reject result; do NOT aggregate. |
| `fanout.result.conflict` | Child result with different `result_id` values, the same `work_item_id`, but different result payload hashes. | Record both results; emit `fanout.result.conflict` event. |
| `fanout.result.late` | Child result submitted after aggregation has completed. | Reject result; do NOT aggregate. |
| `fanout.result.causal-attachment.immutable` | Attempt to modify causal attachment metadata after it has been recorded in the durable journal. | Reject modification; do NOT alter the original causal attachment record. |

> **Non-normative note.**
Conflicting outcomes are caused by concurrent or duplicate requests.
The host MUST reject conflicting input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.unauthorized` | Fan-out plan directive whose `delegating_agent` does not have the `fanout.plan.create` capability. | Reject directive; do NOT create partial plan state. |
| `fanout.work-item.unauthorized` | Child work item whose `delegating_agent` does not have the `fanout.work-item.create` capability. | Reject work item; do NOT create partial work item state. |
| `fanout.result.unauthorized` | Child result whose child agent does not have the `fanout.result.submit` capability. | Reject result; do NOT aggregate. |

> **Non-normative note.**
Unauthorized outcomes are caused by agents that lack the required
capabilities.
The host MUST reject unauthorized requests without creating partial
state, which is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.exhausted-concurrency` | Fan-out plan directive would exceed the disclosed maximum concurrency implementation limit under [Implementation limits](#implementation-limits). | Reject directive; do NOT create partial plan state. |
| `fanout.plan.exhausted-work-items` | Fan-out plan directive would exceed the disclosed maximum work-items implementation limit under [Implementation limits](#implementation-limits). | Reject directive; do NOT create partial plan state. |
| `fanout.work-item.exhausted-concurrency` | Child work item would exceed the parent plan's `concurrency_bound`. | Reject work item; do NOT create partial work item state. |
| `fanout.plan.exhausted-results` | Fan-out plan has reached the disclosed maximum-results implementation limit under [Implementation limits](#implementation-limits). | Reject result; do NOT aggregate. |
| `fanout.work-item.exhausted-wait` | Waiting for a child under `wait-completion` reached the disclosed maximum-wait implementation limit. | Record the exhaustion event; exclude that unfinished result; include results committed before the event; finalize aggregation after all exhausted children are recorded. |

> **Non-normative note.**
Exhausted outcomes are caused by resource limits.
The host MUST reject exhausted requests without creating partial state,
which is consistent with the resource limits defined in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `fanout.plan.unavailable` | Fan-out plan directive whose `delegating_agent` is not active in the durable registry. | Reject directive; do NOT create partial plan state. |
| `fanout.work-item.unavailable-plan` | Child work item whose parent plan is not active in the durable registry. | Reject work item; do NOT create partial work item state. |
| `fanout.result.unavailable-plan` | Child result whose parent plan is not active in the durable registry. | Reject result; do NOT aggregate. |

> **Non-normative note.**
Unavailable outcomes are caused by agents or plans that are not active.
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
structure. The listed fan-out diagnostic is `code`, `severity` is `error`, and
`details` contains `phase`, `section`, `contract`, `profile`,
`failed_boundary`, `timestamp`, `retryable`, `plan_id`, `work_item_id`, and
`result_id`; inapplicable identifiers are JSON `null`.

| Failure category | Family |
|------------------|--------|
| Malformed | `identity.validation.fanout` |
| Incompatible | `identity.compatibility.fanout` |
| Conflicting | `identity.conflict.fanout` |
| Unauthorized | `identity.authorization.fanout` |
| Exhausted | `identity.limit.fanout` |
| Unavailable | `identity.resource.fanout` |

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
| `evidence_type` | The evidence type (`fanout.plan.admitted`, `fanout.plan.rejected`, `fanout.work-item.admitted`, `fanout.work-item.rejected`, `fanout.result.submitted`, `fanout.result.rejected`, `fanout.plan.completed`, `fanout.plan.failed`). | Host runtime. |
| `plan_id` | The `plan_id` of the parent fan-out plan. | Host runtime. |
| `work_item_id` | The `work_item_id` of the parent work item, if applicable. | Host runtime. |
| `result_id` | The `result_id` of the parent result, if applicable. | Host runtime. |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock. |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime. |

> **Non-normative note.**
The evidence record format ensures that all fan-out plan events are
auditable and tamper-evident.
The `evidence_digest` field enables downstream systems to verify that
the evidence record has not been tampered with after creation.
This is consistent with the provenance and audit contract defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Implementation limits

> **Normative definition.**
The following resource ceilings are implementation limits. A conforming host
MUST publish each positive limit in its conformance profile and MUST use the
listed diagnostic when otherwise valid work exceeds it.

| Limit | Constraint | Exhaustion diagnostic |
|-------|------------|-----------------------|
| Maximum concurrency per plan | Positive integer disclosed in the conformance profile. | `fanout.plan.exhausted-concurrency` |
| Maximum work items per plan | Positive integer disclosed in the conformance profile. | `fanout.plan.exhausted-work-items` |
| Maximum results per plan | Positive integer disclosed in the conformance profile. | `fanout.plan.exhausted-results` |
| Maximum wait for `wait-completion` | Positive duration disclosed in the conformance profile. | `fanout.work-item.exhausted-wait` |

> **Non-normative note.**
Implementation limits allow bounded deployments to refuse otherwise valid
work without changing aggregation semantics. The fixed `best-effort` ordering
is defined under
[Aggregation policies](37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md#aggregation-policies).

### Deferred work

> **Normative definition.**
The following work is deferred to future phases or milestones:

1. **Distributed fan-out plans**: Fan-out plans that span multiple
   host processes or nodes are deferred to Milestone 7.
2. **Dynamic fan-out plan modification**: Dynamically modifying a fan-out
   plan's structure (adding or removing work items) after admission
   is deferred to Milestone 7.
3. **Fan-out plan priority**: Prioritizing fan-out plans for resource
   allocation is deferred to Milestone 7.
4. **Fan-out plan cost tracking**: Tracking the cost of fan-out plans
   for billing or resource accounting is deferred to Milestone 7.

> **Non-normative note.**
The deferred work above is not within the scope of Phase 3 but may
be addressed in future phases.
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 3 would invalidate an earlier milestone
assumption:

1. **Fan-out plans require shared mutable guest state**: If fan-out
   plans require shared mutable guest state, this would invalidate
   the assumption defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   that all state transitions are deterministic and replayable.
2. **Fan-out plans bypass the durable journal**: If fan-out plans bypass
   the durable journal, this would invalidate the assumption defined
   in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   that all state transitions are durable across host restarts.
3. **Fan-out plans bypass the atomic commit protocol**: If fan-out plans
   bypass the atomic commit protocol, this would invalidate the
   assumption defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   that all state transitions are atomic.

> **Non-normative note.**
These results would indicate a design flaw in Phase 3 and would require
a revision of the Phase 3 contracts before promotion to `status:
normative`.
Implementations MUST NOT deviate from the contracts defined in this
chapter without evidence from a corresponding revision.

### Cross-references and precedence

> **Non-normative note.**
This section's failure evidence and operational notes integrate with the
following earlier chapters:

1. For failure diagnostics: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of fan-out plan-specific diagnostic format.
2. For evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of fan-out plan-specific evidence record format.
3. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of fan-out plan-specific capability enforcement.
4. For resource limits: this section takes precedence over
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   for questions of fan-out plan-specific resource limits.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
