---
title: "Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests"
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
  - integration-tests
aliases:
  - "M6-P3 Phase 3 Integration Tests"
---

# Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-03-fan-out-fan-in-delegation-and-result-aggregation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It defines the integration tests that verify fan-out fan-in delegation
and result aggregation across its real dependency boundaries.

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
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md).

## 37.4 Phase 3 Integration Tests

### Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes the full
fan-out fan-in delegation and result aggregation under normal operating
conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Fan-out plan creation flow

| Test ID | Description |
|---------|-------------|
| `P3-SF-001` | Create a fan-out plan with a valid fan-out plan directive and verify that all five atomic commit steps are executed (plan registry entry, plan journal entry, child work items, aggregation state initialization, evidence emission). |
| `P3-SF-002` | Create a fan-out plan with a deterministic `plan_id` and verify that two identical directives produce the same `plan_id`. |
| `P3-SF-003` | Create a fan-out plan with all five aggregation policy types and verify that each policy is correctly recorded in the plan registry entry. |
| `P3-SF-004` | Create a fan-out plan with attenuated delegation grants and verify that the child agents' grants are strictly a subset of the delegating agent's grants as defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). |
| `P3-SF-005` | Create a fan-out plan with a valid `result_contract` and verify that the contract is recorded in the evidence emission. |

> **Non-normative note.**
Tests `P3-SF-001` through `P3-SF-005` exercise the full fan-out plan
creation flow defined in section 37.1.
Test `P3-SF-001` is the primary creation test and MUST verify the complete
atomic commit sequence defined in section 37.1.
Each of the five steps MUST be observable as a separate entry in the
durable state journal as defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Child work item execution flow

| Test ID | Description |
|---------|-------------|
| `P3-SF-006` | Verify that a child work item transitions through the following lifecycle states in order: `pending`, `activated`, `executing`, then `completed`, with each transition emitting the correct lifecycle event into the child's mailbox. |
| `P3-SF-007` | Verify that each lifecycle event includes the required fields defined in section 37.1 and that the `sequence_number` is monotonically incremented. |
| `P3-SF-008` | Verify that `child.lifecycle.accepted` is emitted before `child.lifecycle.activated` and that `child.lifecycle.activated` is emitted before `child.lifecycle.initialized`. |
| `P3-SF-009` | Verify that `child.lifecycle.completed` includes a valid `completion_status` and `result_summary` populated by the child's live actor. |
| `P3-SF-010` | Verify that `child.lifecycle.failed` is emitted with a valid `failure_code`, `failure_message`, and `snapshot_at_failure` when the child exits with an error. |

> **Non-normative note.**
Tests `P3-SF-006` through `P3-SF-010` validate the child work item
lifecycle defined in section 37.1.
The lifecycle ordering tests `P3-SF-006` through `P3-SF-008` validate
the state machine transitions defined by the eight lifecycle event types.
Test `P3-SF-010` exercises the failure path that is distinct from the
cancellation and termination paths.

#### Result submission and aggregation flow

| Test ID | Description |
|---------|-------------|
| `P3-SF-011` | Submit a child result for a child work item and verify that the result is accepted and aggregated according to the parent plan's `aggregation_policy`. |
| `P3-SF-012` | Submit multiple child results for a child work item and verify that duplicate suppression is applied correctly. |
| `P3-SF-013` | Submit a child result that does not satisfy the parent plan's `result_contract` and verify that the result is rejected with `fanout.result.contract-violation`. |
| `P3-SF-014` | Verify that the aggregated result is correctly composed according to the parent plan's `aggregation_policy` and `result_contract`. |
| `P3-SF-015` | Verify that the aggregated result is recorded in the durable journal and emitted as evidence. |

> **Non-normative note.**
Tests `P3-SF-011` through `P3-SF-015` exercise the full result submission
and aggregation flow defined in section 37.1 and 37.2.
Test `P3-SF-011` is the primary aggregation test and MUST verify that
the result is aggregated correctly according to the parent plan's
`aggregation_policy`.
Test `P3-SF-012` validates the duplicate suppression invariant defined
in section 37.1.
Test `P3-SF-013` validates the `result_contract` invariant defined
in section 37.1.

#### All aggregation policy flow

| Test ID | Description |
|---------|-------------|
| `P3-SF-016` | Create a fan-out plan with `aggregation_policy: all` and verify that all child results are aggregated into the final result. |
| `P3-SF-017` | Create a fan-out plan with `aggregation_policy: quorum` and `quorum_threshold: 2` and verify that aggregation completes when 2 successful results are received. |
| `P3-SF-018` | Create a fan-out plan with `aggregation_policy: first-success` and verify that aggregation completes when the first successful result is received. |
| `P3-SF-019` | Create a fan-out plan with `aggregation_policy: best-effort` and verify that the best result is selected according to the implementation-defined quality metric. |
| `P3-SF-020` | Create a fan-out plan with `aggregation_policy: ordered` and verify that results are aggregated in the order of their `work_item_index`. |

> **Non-normative note.**
Tests `P3-SF-016` through `P3-SF-020` exercise the full aggregation
policy behavior defined in section 37.2.
Each test validates one of the five aggregation policies and verifies
that the aggregation completes correctly according to the policy's
termination condition.

#### Causal attachment flow

| Test ID | Description |
|---------|-------------|
| `P3-SF-021` | Verify that every child result includes the correct `plan_id`, `work_item_id`, `delegating_agent`, `originating_request_id`, and `correlation_id`. |
| `P3-SF-022` | Verify that causal attachment metadata is recorded in the durable journal and emitted as evidence. |
| `P3-SF-023` | Verify that causal attachment metadata is immutable once recorded. |

> **Non-normative note.**
Tests `P3-SF-021` through `P3-SF-023` validate the causal attachment
invariant defined in section 37.1.
Test `P3-SF-023` validates the immutability invariant, which is essential
for audit and provenance.

### Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-001` | Fan-out plan directive with missing `plan_id` field. | `fanout.plan.malformed` |
| `P3-FH-002` | Fan-out plan directive with empty `work_items` list. | `fanout.plan.malformed-work-items` |
| `P3-FH-003` | Fan-out plan directive with `concurrency_bound: 0`. | `fanout.plan.malformed-concurrency-bound` |
| `P3-FH-004` | Fan-out plan directive with past `deadline`. | `fanout.plan.malformed-deadline` |
| `P3-FH-005` | Fan-out plan directive with `aggregation_policy: invalid`. | `fanout.plan.malformed-aggregation-policy` |
| `P3-FH-006` | Child work item with missing `work_item_id` field. | `fanout.work-item.malformed` |
| `P3-FH-007` | Child work item with invalid artifact digest. | `fanout.work-item.malformed-artifact` |
| `P3-FH-008` | Child result with missing `result_id` field. | `fanout.result.malformed` |
| `P3-FH-009` | Child result with invalid `result_data`. | `fanout.result.malformed-data` |

> **Normative definition.**
Each malformed input test MUST verify that the host: (1) rejects the
directive with the specified diagnostic, (2) does NOT create a partial
registry entry or journal record, and (3) does NOT leave any live actor
instance in an indeterminate state.

> **Non-normative note.**
The malformed input tests validate the schema validation layer that guards
the atomic commit protocol.
Without these tests, a malformed directive could cause inconsistent state
or leave partial state in the durable journal, violating the atomicity
guarantees defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-010` | Fan-out plan directive with `lifecycle_policy` that does not name a defined policy. | `fanout.plan.incompatible` |
| `P3-FH-011` | Child work item with `manifest` digest that does not correspond to `artifact` digest. | `fanout.plan.incompatible-manifest-artifact` |
| `P3-FH-012` | Child work item with `plan_id` that does not resolve to an active plan. | `fanout.plan.incompatible-plan` |
| `P3-FH-013` | Child result that does not satisfy the parent plan's `result_contract`. | `fanout.result.incompatible-contract` |

> **Non-normative note.**
The incompatible input tests validate the semantic validation layer that
guards the atomic commit protocol.
Without these tests, an incompatible directive could cause inconsistent
state or leave partial state in the durable journal.

#### Conflicting input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-014` | Two fan-out plan directives with the same `plan_id` submitted concurrently. | `fanout.plan.duplicate-plan-id` for the second directive. |
| `P3-FH-015` | Two child work item directives for the same plan submitted concurrently. | `fanout.work-item.duplicate-work-item-id` for the second directive. |
| `P3-FH-016` | Two child results with the same `result_id` submitted for the same work item. | `fanout.result.duplicate` for the second result. |
| `P3-FH-017` | Two child results with different `result_id` values, same `work_item_id`, but different `result_data` hashes. | `fanout.result.conflict` event emitted. |
| `P3-FH-018` | Child result submitted after aggregation has completed. | `fanout.result.late` for the late result. |

> **Non-normative note.**
The conflicting input tests validate the deduplication and conflict
resolution layer that guards the atomic commit protocol.
Without these tests, conflicting directives could cause inconsistent
state or leave partial state in the durable journal.

#### Unauthorized input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-019` | Fan-out plan directive whose `delegating_agent` does not have the `fanout.plan.create` capability. | `fanout.plan.unauthorized` |
| `P3-FH-020` | Child work item whose `delegating_agent` does not have the `fanout.work-item.create` capability. | `fanout.work-item.unauthorized` |
| `P3-FH-021` | Child result whose child agent does not have the `fanout.result.submit` capability. | `fanout.result.unauthorized` |

> **Non-normative note.**
The unauthorized input tests validate the capability enforcement layer
that guards the atomic commit protocol.
Without these tests, unauthorized directives could bypass the capability
policy and compromise system security.

#### Exhausted input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-022` | Fan-out plan directive that would exceed the implementation-defined maximum concurrency per plan. | `fanout.plan.exhausted-concurrency` |
| `P3-FH-023` | Child work item that would exceed the parent plan's `concurrency_bound`. | `fanout.work-item.exhausted-concurrency` |
| `P3-FH-024` | Child result that would exceed the implementation-defined maximum number of results per plan. | `fanout.plan.exhausted-results` |

> **Non-normative note.**
The exhausted input tests validate the resource limit enforcement layer
that guards the atomic commit protocol.
Without these tests, exhausted directives could cause resource exhaustion
and compromise system stability.

#### Unavailable input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FH-025` | Fan-out plan directive whose `delegating_agent` is not active in the durable registry. | `fanout.plan.unavailable` |
| `P3-FH-026` | Child work item whose parent plan is not active in the durable registry. | `fanout.work-item.unavailable-plan` |
| `P3-FH-027` | Child result whose parent plan is not active in the durable registry. | `fanout.result.unavailable-plan` |

> **Non-normative note.**
The unavailable input tests validate the agent registry lookup layer
that guards the atomic commit protocol.
Without these tests, unavailable directives could bypass the agent
registry and compromise system consistency.

### Timeout and cancellation tests

> **Normative definition.**
Timeout and cancellation tests verify that the host correctly handles
child timeout, plan cancellation, and parent cancellation under various
`cancellation_policy` settings.

#### Child timeout tests

| Test ID | Description |
|---------|-------------|
| `P3-TO-001` | Create a fan-out plan with `cancellation_policy: cancel-all` and verify that child agents are cancelled when the plan's `deadline` expires. |
| `P3-TO-002` | Create a fan-out plan with `cancellation_policy: wait-completion` and verify that child agents are allowed to complete their work items even after the plan's `deadline` expires. |
| `P3-TO-003` | Create a fan-out plan with `cancellation_policy: allow-partial` and verify that child agents are allowed to complete their work items but their results are excluded from aggregation if they complete after the deadline. |
| `P3-TO-004` | Verify that a `fanout.work-item.timeout` event is emitted when a child agent times out. |

> **Non-normative note.**
Tests `P3-TO-001` through `P3-TO-004` validate the child timeout behavior
defined in section 37.2.
Each test validates one of the three `cancellation_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Plan cancellation tests

| Test ID | Description |
|---------|-------------|
| `P3-CA-001` | Cancel a fan-out plan with `cancellation_policy: cancel-all` and verify that all child agents are cancelled and no results are aggregated. |
| `P3-CA-002` | Cancel a fan-out plan with `cancellation_policy: wait-completion` and verify that child agents are allowed to complete their work items and their results are aggregated. |
| `P3-CA-003` | Cancel a fan-out plan with `cancellation_policy: allow-partial` and verify that child agents are allowed to complete their work items but their results are excluded from aggregation. |
| `P3-CA-004` | Verify that a `fanout.plan.cancelled` event is emitted when a fan-out plan is cancelled. |

> **Non-normative note.**
Tests `P3-CA-001` through `P3-CA-004` validate the plan cancellation
behavior defined in section 37.2.
Each test validates one of the three `cancellation_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Parent cancellation tests

| Test ID | Description |
|---------|-------------|
| `P3-PA-001` | Cancel the delegating agent of a fan-out plan with `cancellation_policy: cancel-all` and verify that all child agents are cancelled and no results are aggregated. |
| `P3-PA-002` | Cancel the delegating agent of a fan-out plan with `cancellation_policy: wait-completion` and verify that child agents are allowed to complete their work items and their results are aggregated. |
| `P3-PA-003` | Cancel the delegating agent of a fan-out plan with `cancellation_policy: allow-partial` and verify that child agents are allowed to complete their work items but their results are excluded from aggregation. |
| `P3-PA-004` | Verify that a `fanout.plan.parent-cancelled` event is emitted when the delegating agent is cancelled. |

> **Non-normative note.**
Tests `P3-PA-001` through `P3-PA-004` validate the parent cancellation
behavior defined in section 37.2.
Each test validates one of the three `cancellation_policy` settings and
verifies that the host behaves correctly according to the policy.

### Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 3 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 3 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 3
contracts interact with many earlier milestones (see the cross-reference
summary in section 37.1).
Without these tests, a Phase 3 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 3
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 6 Phase 1 | Signal envelopes, causality routing, and delivery | All fixtures continue to pass; fan-out plan signals are correctly routed through the signal envelope mechanism. |
| Milestone 6 Phase 1 | Actions, instructions, validation, plans, and results | All fixtures continue to pass; fan-out plan directives are correctly validated through the actions validation flow. |
| Milestone 6 Phase 1 | State operations, patches, revisions, and conflicts | All fixtures continue to pass; fan-out plan state is correctly managed through the state operations mechanism. |
| Milestone 6 Phase 1 | Directives, strategies, continuations, and terminal states | All fixtures continue to pass; fan-out plan terminal states are consistent with the directive terminal states. |
| Milestone 6 Phase 1 | Deterministic reducer semantics and milestone acceptance | All fixtures continue to pass; fan-out plan results are correctly processed by the deterministic reducer. |
| Milestone 6 Phase 1 | Extism invocation boundary instances and output validation | All fixtures continue to pass; fan-out plan child agents are subject to the same Extism invocation boundary. |
| Milestone 6 Phase 1 | Mailboxes, ordering, bounds, fairness, and turn leases | All fixtures continue to pass; fan-out plan lifecycle events are correctly delivered through mailboxes. |
| Milestone 6 Phase 1 | Agent registry, activation, cancellation, and completion | All fixtures continue to pass; fan-out plan registry entries are consistent with the agent registry contract. |
| Milestone 6 Phase 1 | Sensors, schedules, timers, and external signal ingress | All fixtures continue to pass; fan-out plan notifications are correctly delivered through the sensor mechanism. |
| Milestone 6 Phase 1 | Single-agent host flow and milestone acceptance | All fixtures continue to pass; fan-out plan lifecycle is consistent with the single-agent host flow. |
| Milestone 6 Phase 1 | Revisioned snapshots, journals, history, and storage contracts | All fixtures continue to pass; fan-out plan snapshots are correctly captured and journaled. |
| Milestone 6 Phase 1 | Atomic state journal and directive-outbox commits | All fixtures continue to pass; fan-out plan atomic commits are consistent with the journal protocol. |
| Milestone 6 Phase 1 | Effect handlers, attempts, idempotency, and result signals | All fixtures continue to pass; fan-out plan lifecycle events are correctly processed as effect handlers. |
| Milestone 6 Phase 1 | Retry, timer, recovery, replay, hibernate, and migration | All fixtures continue to pass; fan-out plan restart policy does not conflict with the retry mechanism. |
| Milestone 6 Phase 1 | Crash injection, durable effects, and milestone acceptance | All fixtures continue to pass; fan-out plan lifecycle events are durable across crashes. |
| Milestone 6 Phase 2 | Child lifecycle, cancellation, monitoring, and restart policy | All fixtures continue to pass; fan-out plan child agents are consistent with the child lifecycle contract. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; fan-out plan grants are consistent with the threat model. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; fan-out plan grant attenuation is consistent with the capability policy. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; fan-out plan child agents are consistent with the framework plugin model. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; fan-out plan child agents are subject to the same WASI restrictions. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; fan-out plan lifecycle evidence is correctly signed and audited. |
| Milestone 5 | Agent identity, addressing, ownership, and dependency relations | All fixtures continue to pass; fan-out plan addresses and relationships are consistent with the identity model. |

> **Normative definition.**
A cross-milestone compatibility test passes if and only if: (1) every
fixture listed in the table above continues to produce the same expected
output as before the Phase 3 contracts were active, and (2) no new
regressions are introduced.
If any fixture fails, the Phase 3 implementation MUST be revised and the
affected milestone MUST be re-validated according to the cross-milestone
revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).

> **Non-normative note.**
The table above lists 22 fixture scopes from 7 milestones that are affected
by the Phase 3 contracts.
This is consistent with the cross-reference summary in section 37.1, which
identifies 11 direct integration points with earlier chapters.
The broader fixture scope accounts for indirect effects through shared
subsystems (such as the agent registry, mailboxes, and durable journal).

### Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 3
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: draft` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 37.4.1 through 37.4.5:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P3-SF-001`). | String. |
| `test_objective` | The test objective this scenario addresses. | String. |
| `setup` | The test setup description (input data, preconditions). | Structured text. |
| `expected_outcome` | The expected observable behavior. | Structured text. |
| `actual_outcome` | The actual observable behavior. | Structured text. |
| `result` | `pass`, `fail`, or `blocked`. | Enum. |
| `evidence_digest` | A deterministic hash of the evidence record. | Hash digest. |
| `timestamp` | The ISO 8601 timestamp of test execution. | ISO 8601 string. |
| `regression` | For cross-milestone tests, whether the test previously passed. | Boolean. |
| `approved_variability` | For cross-milestone tests, any approved variability from the baseline. | Structured text. |

> **Non-normative note.**
The evidence format above is consistent with the evidence record format
defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
The `evidence_digest` field enables downstream systems to verify that the
evidence record has not been tampered with after creation.
The `approved_variability` field enables operators to document and
retroactively approve intentional deviations from the baseline, which
is important for cross-milestone compatibility testing where some
variations are acceptable (such as implementation-defined bounded times).

> **Normative definition.**
A run of all Phase 3 integration tests passes if and only if:

1. Every test scenario defined in sections 37.4.1 through 37.4.5 produces
   a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 37.4.6
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 3 integration tests as defined above.
2. A passing run of all cross-milestone compatibility tests as defined
   above.
3. All evidence records for the passing run, signed and stored in the
   durable evidence log.
4. A written report summarizing the test run, including any approved
   variability, regressions, or deviations from the baseline.

> **Non-normative note.**
The evidence requirements above ensure that promotion to `status: normative`
is based on reproducible, auditable evidence rather than subjective
assessment.
The signed evidence records provide a tamper-evident trail that
downstream consumers (such as the provenance and audit layer) can
verify independently.
The written report provides context and narrative that structured
evidence records cannot capture, such as explanations of approved
variability or deviations from the baseline.

### Cross-reference summary

> **Non-normative note.**
This section's integration tests integrate with the following earlier
chapters:

1. For fan-out plan and child work item validation: this section takes
   precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of fan-out plan-specific validation tests.
2. For fan-out plan and child work item atomic commits: this section
   takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of fan-out plan-specific atomic commit tests.
3. For fan-out plan and child work item evidence emission: this section
   takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of fan-out plan-specific evidence tests.
4. For child agent execution within a fan-out plan: this section takes
   precedence over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of child agent lifecycle tests within a fan-out plan context.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
