---
title: "Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-03
  - fan-out
  - fan-in
  - delegation
  - result-aggregation
  - aggregation-policy
aliases:
  - "M6-P3 Behavior And Integration"
---

# Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-03-fan-out-fan-in-delegation-and-result-aggregation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the behavior and integration rules for fan-out fan-in
delegation and result aggregation, including aggregation policy evaluation,
durable aggregation progress, and failure handling.

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
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md),
[Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests](37-fan-out-fan-in-delegation-and-result-aggregation-phase-3-integration-tests.md).

## 37.2 Behavior And Integration

### Aggregation policies

> **Normative definition.**
An aggregation policy determines how child results are combined into a
single aggregated result for a fan-out plan.
The following five aggregation policies are defined by this chapter:

| Policy | Aggregation behavior | Termination condition |
|--------|---------------------|----------------------|
| `all` | Collect all child results until the plan's `deadline` expires. | Plan `deadline` expires. |
| `quorum` | Collect child results until `quorum_threshold` successful results are received. | `quorum_threshold` successful results received. |
| `first-success` | Accept the first successful result; discard subsequent results. | First successful result received. |
| `best-effort` | Collect all child results and select the best according to an implementation-defined quality metric. | Plan `deadline` expires. |
| `ordered` | Collect child results in the order specified by the parent plan's `work_items` list, regardless of submission order. | All child results received or plan `deadline` expires. |

> **Non-normative note.**
The five aggregation policies provide flexibility for different use cases.
`all` is appropriate for tasks where the complete result set is required
(such as distributed queries); `quorum` is appropriate for tasks where
a majority is sufficient (such as distributed consensus); `first-success`
is appropriate for tasks where any successful result is sufficient (such
as load-balanced requests); `best-effort` is appropriate for tasks where
quality varies (such as distributed sampling); `ordered` is appropriate
for tasks where result order matters (such as distributed sorting).

> **Normative definition.**
The `all` aggregation policy collects all child results until the plan's
`deadline` expires.
The host MUST aggregate all received results, including partial results,
into the final aggregated result.
The host MUST NOT discard any results unless the plan's `cancellation_policy`
is `cancel-all` and the plan is cancelled before the deadline.

> **Non-normative note.**
The `all` policy ensures completeness; it is appropriate for tasks where
the aggregated result is meaningless without all child results (such
as distributed map-reduce operations).
The `deadline` provides a bounded wait time; if some children are slow
or hung, the plan does not wait indefinitely.

> **Normative definition.**
The `quorum` aggregation policy collects child results until
`quorum_threshold` successful results are received.
The host MUST aggregate the first `quorum_threshold` successful results
into the final aggregated result.
Subsequent successful results are discarded; failed results are included
only if they are among the first `quorum_threshold` results.

> **Non-normative note.**
The `quorum` policy ensures that the aggregated result is based on a
majority of successful results, which is appropriate for tasks where
a consensus is required (such as distributed voting or consensus
protocols).
The `quorum_threshold` must be set appropriately to balance between
completeness and timeliness; a higher threshold provides more
redundancy but may delay aggregation.

> **Normative definition.**
The `first-success` aggregation policy accepts the first successful result
and discards subsequent results.
The host MUST aggregate the first successful result into the final
aggregated result and MUST NOT process subsequent results.

> **Non-normative note.**
The `first-success` policy ensures minimal latency; it is appropriate
for tasks where any successful result is sufficient (such as load-balanced
requests or distributed lookups).
Failed results are not aggregated; if all results fail, the plan is
considered failed.

> **Normative definition.**
The `best-effort` aggregation policy uses a two-phase process.
Phase one (collection): the host collects all child results until the
plan's `deadline` expires.
Phase two (selection): the host selects the best result according to an
implementation-defined quality metric documented in the conformance profile;
the selected result becomes the aggregated output and all other results
are discarded; failed results are excluded from selection.

> **Non-normative note.**
The `best-effort` policy ensures that the best available result is
used; it is appropriate for tasks where quality varies (such as
distributed sampling or distributed inference).
The quality metric must be documented in the conformance profile and
must be deterministic to ensure reproducible aggregation.

> **Normative definition.**
The `ordered` aggregation policy collects child results in the order
specified by the parent plan's `work_items` list, regardless of
submission order.
The host MUST aggregate child results in the order of their `work_item_index`
and MUST NOT reorder results.
If a child result is missing (due to failure, timeout, or cancellation),
the host MUST record a null placeholder in the aggregated result at the
corresponding position.

> **Non-normative note.**
The `ordered` policy ensures that the aggregated result preserves the
order of the original work items; it is appropriate for tasks where
result order matters (such as distributed sorting or distributed
processing of ordered data).
Null placeholders ensure that the aggregated result has the same
structure as the original work items list.

### Durable aggregation progress

> **Normative definition.**
Aggregation progress MUST be represented durably so that activation
changes (such as host restarts, agent migrations, or engine instance
failures) do not lose work.
The host MUST persist the following aggregation state in the durable
journal defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md):

| State field | Content | Source |
|-------------|---------|--------|
| `plan_id` | The `plan_id` of the parent fan-out plan. | Fan-out plan directive. |
| `aggregation_status` | The current aggregation status: `awaiting-results`, `aggregating`, or `completed`. | Host runtime. |
| `received_results` | A list of `result_id` values for results received so far. | Child agents. |
| `successful_results` | A list of `result_id` values for successful results received so far. | Child agents. |
| `failed_results` | A list of `result_id` values for failed results received so far. | Child agents. |
| `aggregation_policy` | The aggregation policy for this plan. | Fan-out plan directive. |
| `quorum_threshold` | The quorum threshold if `aggregation_policy` is `quorum`; otherwise `null`. | Fan-out plan directive. |
| `aggregated_result` | The aggregated result if `aggregation_status` is `completed`; otherwise `null`. | Host runtime. |
| `completed_at` | The ISO 8601 timestamp of aggregation completion if `aggregation_status` is `completed`; otherwise `null`. | Host runtime. |

> **Non-normative note.**
The durable aggregation state ensures that aggregation progress is not
lost during activation changes.
If the host restarts, the host MUST resume aggregation from the last
persisted state rather than restarting from scratch.
This is consistent with the durable journal contract defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md),
which requires that all state transitions are durable across host restarts.

> **Normative definition.**
The host MUST persist aggregation state changes through the atomic commit
protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
Each aggregation state change MUST be recorded as a separate journal
entry with a deterministic entry identity derived from the `plan_id`,
the state change type, and a monotonic sequence counter.

> **Non-normative note.**
The atomic commit protocol ensures that aggregation state changes are
crash-safe; if the host crashes during an aggregation state change,
the journal provides a recovery point that allows the host to resume
aggregation from a consistent state.
This is consistent with the crash injection and durable effects
contract defined in
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md),
which requires that all state transitions are durable across crashes.

> **Normative definition.**
The host MUST resume aggregation from the last persisted state after
a host restart, engine instance failure, or agent migration.
The host MUST NOT discard previously-aggregated results unless the
plan's `cancellation_policy` is `cancel-all` and the plan is cancelled.

> **Non-normative note.**
Resuming aggregation from the last persisted state ensures that
aggregation is not disrupted by transient failures.
This is essential for long-running fan-out plans that may span multiple
host restarts or agent migrations.

### Failure handling

> **Normative definition.**
The following failure scenarios are normative invariants that every
host implementation MUST handle correctly for fan-out plans under any
aggregation policy.
Each scenario describes a specific failure condition and the expected
host behavior.

#### Child timeout

> **Normative definition.**
Child timeout occurs when a child agent has not completed its work item
within the plan's `deadline`.
The host MUST handle child timeout according to the following rules:

1. If the child agent has not completed its work item by the plan's
   `deadline`, the host MUST apply the plan's `cancellation_policy`
   to determine whether to cancel, wait, or allow partial results.
2. If the plan's `cancellation_policy` is `cancel-all`, the host MUST
   cancel the child agent and emit a `fanout.work-item.timeout` event.
3. If the plan's `cancellation_policy` is `wait-completion`, the host
   MUST continue waiting for the child agent to complete its work item
   until the child agent completes or the host's maximum wait timeout
   expires.
4. If the plan's `cancellation_policy` is `allow-partial`, the host
   MUST allow the child agent to continue executing but MUST NOT
   include its result in the aggregated result if it completes after
   the deadline.

> **Non-normative note.**
The three cancellation policies provide different tradeoffs between
completeness and timeliness.
`cancel-all` ensures that no children outlive the deadline; `wait-completion`
allows children to complete but may delay aggregation; `allow-partial`
allows children to complete but excludes late results from aggregation.
The maximum wait timeout for `wait-completion` must be documented in
the conformance profile and MUST be longer than the maximum expected
work item execution time.

#### Partial failure

> **Normative definition.**
Partial failure occurs when some child agents complete their work items
successfully but others fail.
The host MUST handle partial failure according to the following rules:

1. If the aggregation policy is `first-success`, the host MUST aggregate
   the first successful result and discard subsequent results, including
   failed results.
2. If the aggregation policy is `quorum`, the host MUST aggregate the
   first `quorum_threshold` successful results and discard subsequent
   results; failed results are included only if they are among the first
   `quorum_threshold` results.
3. If the aggregation policy is `all`, the host MUST aggregate all
   received results, including failed results, into the final aggregated
   result; the host MUST NOT discard failed results unless the plan's
   `cancellation_policy` is `cancel-all` and the plan is cancelled.
4. If the aggregation policy is `best-effort`, the host MUST aggregate
   all received results and select the best according to the quality
   metric; failed results are excluded from selection.
5. If the aggregation policy is `ordered`, the host MUST aggregate
   child results in the order of their `work_item_index`; failed results
   are recorded as null placeholders.

> **Non-normative note.**
Partial failure is a common outcome in distributed systems where some
children may fail due to transient errors, infrastructure failures, or
application-level errors.
The aggregation policies above provide different tradeoffs between
completeness and robustness; implementations SHOULD document their
partial failure handling behavior in the conformance profile.

#### Conflicting results

> **Normative definition.**
Conflicting results occur when two or more child agents submit results
for the same work item that differ in content.
The host MUST handle conflicting results according to the following rules:

1. If the results have the same `result_id`, the host MUST reject the
   second result with the diagnostic `fanout.result.duplicate`.
2. If the results have different `result_id` values but the same
   `work_item_id` and the same `result_data` hash, the host MUST reject
   the second result with the diagnostic `fanout.result.duplicate-content`.
3. If the results have different `result_id` values, the same `work_item_id`,
   but different `result_data` hashes, the host MUST record both results
   and emit a `fanout.result.conflict` event; the host MUST NOT discard
   either result.

> **Non-normative note.**
Conflicting results are a sign of a bug in the child agent or the
fan-out plan implementation.
The host MUST record conflicting results and emit an event so that
operators can investigate and correct the issue.
The host MUST NOT discard conflicting results because doing so would
violate the audit and provenance requirements defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

#### Late result

> **Normative definition.**
Late result occurs when a child agent submits a result after the
aggregation has completed.
The host MUST handle late results according to the following rules:

1. If the aggregation has completed, the host MUST reject the late
   result with the diagnostic `fanout.result.late`.
2. The host MUST record the late result in the durable journal with
   the diagnostic and the corresponding plan's `plan_id`.
3. The host MUST NOT include late results in the aggregated result.

> **Non-normative note.**
Late results are a sign of a bug in the child agent or the host's
aggregation implementation.
The host MUST record late results so that operators can investigate
and correct the issue.

#### Cancelled parent

> **Normative definition.**
Cancelled parent occurs when the delegating agent is cancelled,
terminated, or becomes unresolvable while the fan-out plan is still
active.
The host MUST handle cancelled parent according to the following rules:

1. If the delegating agent is cancelled, the host MUST apply the plan's
   `cancellation_policy` to determine whether to cancel, wait, or allow
   partial results.
2. If the plan's `cancellation_policy` is `cancel-all`, the host MUST
   cancel all child agents and emit a `fanout.plan.parent-cancelled`
   event.
3. If the plan's `cancellation_policy` is `wait-completion`, the host
   MUST continue waiting for child agents to complete their work items.
4. If the plan's `cancellation_policy` is `allow-partial`, the host
   MUST allow child agents to complete their work items but MUST NOT
   include their results in the aggregated result.

> **Non-normative note.**
Cancelled parent is a rare but important failure scenario.
The cancellation policies above provide different tradeoffs between
completeness and resource efficiency.
`cancel-all` ensures that no resources are wasted on cancelled plans;
`wait-completion` allows plans to complete but may waste resources;
`allow-partial` allows plans to complete but excludes results.

#### Aggregation restart

> **Normative definition.**
Aggregation restart occurs when the host needs to restart aggregation
after a host restart, engine instance failure, or agent migration.
The host MUST handle aggregation restart according to the following rules:

1. The host MUST resume aggregation from the last persisted state.
2. The host MUST NOT discard previously-aggregated results unless the
   plan's `cancellation_policy` is `cancel-all` and the plan is cancelled.
3. The host MUST continue aggregation from the state where it left off
   before the restart.

> **Non-normative note.**
Aggregation restart ensures that aggregation is not disrupted by
transient failures.
This is essential for long-running fan-out plans that may span multiple
host restarts or agent migrations.

### Cross-references and precedence

> **Non-normative note.**
This section's behavior and integration rules integrate with the following
earlier chapters:

1. For aggregation policy evaluation: this section takes precedence over
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   for questions of fan-out plan-specific aggregation policy evaluation.
2. For durable aggregation state: this section takes precedence over
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   for questions of fan-out plan-specific aggregation state persistence.
3. For atomic commit of aggregation state: this section takes precedence
   over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of fan-out plan-specific atomic commit steps.
4. For child agent timeout and cancellation: this section takes precedence
   over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of child agent timeout and cancellation within a fan-out
   plan context.
5. For failure event emission: this section takes precedence over
   [Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md)
   for questions of fan-out plan-specific failure event format.
6. For crash-safe aggregation: this section takes precedence over
   [Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md)
   for questions of fan-out plan-specific crash safety.
7. Where both sections are applicable and agree, they are mutually
   reinforcing.
