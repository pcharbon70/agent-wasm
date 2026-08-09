---
title: "Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-03
  - fsm
  - tool-loop
  - planning-strategies
  - integration-tests
  - verification
aliases:
  - "M7-P3 Integration Tests"
---

# Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-03-direct-fsm-tool-loop-and-planning-strategies.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It defines the integration tests that verify direct FSM tool-loop and
planning strategies across their real dependency boundaries, including
successful flow tests, failure handling tests, timeout and cancellation
tests, and cross-milestone compatibility tests.

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
[Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests](37-fan-out-fan-in-delegation-and-result-aggregation-phase-3-integration-tests.md),
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md),
[Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes](38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md),
[Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests](38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Failure Evidence And Operational Notes](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-failure-evidence-and-operational-notes.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-phase-5-integration-tests.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests](41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md),
[Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md),
[Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md),
[Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md),
[Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests](42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md),
[Direct FSM Tool-Loop And Planning Strategies Contract And Data Model](43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md),
[Direct FSM Tool-Loop And Planning Strategies Behavior And Integration](43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md),
[Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes](43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md).

## 43.4 Phase 3 Integration Tests

### Successful flow tests

> **Normative definition.**
The following tests verify the canonical successful flow and retained
evidence for direct FSM tool-loop and planning strategies.

#### Direct strategy success tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-direct-strategy-success-1` | Execute direct strategy with valid input. | Valid strategy input, valid action, valid result. | Direct strategy produces next action and termination signal. |
| `test-direct-strategy-success-2` | Execute direct strategy with iteration tracking. | Valid strategy input, valid action, valid result, iteration counter. | Direct strategy increments iteration counter and produces next action. |
| `test-direct-strategy-success-3` | Execute direct strategy with budget tracking. | Valid strategy input, valid action, valid result, budget. | Direct strategy deducts budget and produces next action. |
| `test-direct-strategy-success-4` | Execute direct strategy with continuation state. | Valid strategy input, valid action, valid result, continuation state. | Direct strategy produces continuation state and next action. |
| `test-direct-strategy-success-5` | Execute direct strategy to completion. | Valid strategy input, valid action, valid result, terminal state. | Direct strategy produces termination signal and final result. |

#### FSM state transitions tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-fsm-transition-1` | Transition from `idle` to `planning` on `plan_submitted`. | FSM in `idle` state, `plan_submitted` event. | FSM transitions to `planning` state. |
| `test-fsm-transition-2` | Transition from `planning` to `waiting_for_tool` on tool request. | FSM in `planning` state, tool request event. | FSM transitions to `waiting_for_tool` state. |
| `test-fsm-transition-3` | Transition from `waiting_for_tool` to `planning` on `tool_completed`. | FSM in `waiting_for_tool` state, `tool_completed` event. | FSM transitions to `planning` state. |
| `test-fsm-transition-4` | Transition from `waiting_for_tool` to `planning` on `tool_failed`. | FSM in `waiting_for_tool` state, `tool_failed` event. | FSM transitions to `planning` state. |
| `test-fsm-transition-5` | Transition from `planning` to `waiting_for_model` on model request. | FSM in `planning` state, model request event. | FSM transitions to `waiting_for_model` state. |
| `test-fsm-transition-6` | Transition from `waiting_for_model` to `planning` on `model_completed`. | FSM in `waiting_for_model` state, `model_completed` event. | FSM transitions to `planning` state. |
| `test-fsm-transition-7` | Transition from `planning` to `waiting_for_human` on approval request. | FSM in `planning` state, approval request event. | FSM transitions to `waiting_for_human` state. |
| `test-fsm-transition-8` | Transition from `waiting_for_human` to `terminated` on `human_cancelled`. | FSM in `waiting_for_human` state, `human_cancelled` event. | FSM transitions to `terminated` state. |

#### Tool-loop execution tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-tool-loop-1` | Execute tool-loop with valid tool result. | Tool-loop in `requesting_tool` state, valid tool result. | Tool-loop transitions to `processing_result` state. |
| `test-tool-loop-2` | Execute tool-loop with model request. | Tool-loop in `processing_result` state, model request event. | Tool-loop transitions to `requesting_model` state. |
| `test-tool-loop-3` | Execute tool-loop with model response. | Tool-loop in `requesting_model` state, model response event. | Tool-loop transitions to `processing_model` state. |
| `test-tool-loop-4` | Execute tool-loop with approval request. | Tool-loop in `processing_model` state, approval request event. | Tool-loop transitions to `requesting_approval` state. |
| `test-tool-loop-5` | Execute tool-loop with approval response. | Tool-loop in `requesting_approval` state, approval response event. | Tool-loop transitions to `processing_approval` state. |
| `test-tool-loop-6` | Execute tool-loop to completion. | Tool-loop in `processing_approval` state, completion event. | Tool-loop transitions to `terminated` state. |

#### Plan submission tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-plan-submission-1` | Submit valid plan. | Valid plan, valid agent. | Plan is submitted and plan ID is returned. |
| `test-plan-submission-2` | Submit plan with multiple steps. | Valid plan with multiple steps, valid agent. | Plan is submitted and all steps are recorded. |
| `test-plan-submission-3` | Submit plan with budget constraints. | Valid plan with budget constraints, valid agent. | Plan is submitted and budgets are tracked. |
| `test-plan-submission-4` | Submit plan and monitor execution. | Valid plan, valid agent, monitoring enabled. | Plan execution is monitored and events are emitted. |

#### Budget tracking tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-budget-tracking-1` | Track budget deductions. | Valid strategy execution, budget deduction. | Budget is deducted and remaining budget is updated. |
| `test-budget-tracking-2` | Track multiple budget types. | Valid strategy execution, multiple budget deductions. | All budgets are deducted and remaining budgets are updated. |
| `test-budget-tracking-3` | Track budget to exhaustion. | Valid strategy execution, budget exhaustion. | Budget is exhausted and strategy is terminated. |

#### Snapshot restoration tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-snapshot-restoration-1` | Restore valid snapshot. | Valid snapshot ID, valid agent. | Snapshot is restored and FSM state is updated. |
| `test-snapshot-restoration-2` | Restore snapshot and continue execution. | Valid snapshot ID, valid agent, continuation enabled. | Snapshot is restored and FSM continues execution. |

#### Evidence emission tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-evidence-emission-1` | Emit evidence on FSM state transition. | FSM state transition event. | Evidence is emitted with FSM state transition details. |
| `test-evidence-emission-2` | Emit evidence on budget exhaustion. | Budget exhaustion event. | Evidence is emitted with budget exhaustion details. |
| `test-evidence-emission-3` | Emit evidence on forced termination. | Forced termination event. | Evidence is emitted with forced termination details. |

### Failure handling tests

> **Normative definition.**
The following tests verify that malformed, incompatible, stale, duplicate,
and boundary-limit inputs fail with stable diagnostics where applicable.

#### Malformed input tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-malformed-1` | Reject malformed strategy input. | Malformed strategy input (invalid JSON). | Diagnostic `malformed_strategy_input` is emitted. |
| `test-malformed-2` | Reject malformed plan input. | Malformed plan input (invalid JSON). | Diagnostic `malformed_plan_input` is emitted. |
| `test-malformed-3` | Reject malformed snapshot input. | Malformed snapshot input (invalid JSON). | Diagnostic `malformed_snapshot_input` is emitted. |
| `test-malformed-4` | Reject malformed budget input. | Malformed budget input (invalid JSON). | Diagnostic `malformed_budget_input` is emitted. |
| `test-malformed-5` | Reject strategy input with missing required fields. | Strategy input with missing required fields. | Diagnostic `malformed_strategy_input` is emitted. |
| `test-malformed-6` | Reject plan input with invalid field values. | Plan input with invalid field values. | Diagnostic `malformed_plan_input` is emitted. |

#### Incompatible version tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-incompatible-1` | Reject incompatible strategy version. | Strategy with incompatible version. | Diagnostic `incompatible_strategy_version` is emitted. |
| `test-incompatible-2` | Reject incompatible plan version. | Plan with incompatible version. | Diagnostic `incompatible_plan_version` is emitted. |
| `test-incompatible-3` | Reject incompatible snapshot version. | Snapshot with incompatible version. | Diagnostic `incompatible_snapshot_version` is emitted. |

#### Conflicting input tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-conflicting-1` | Reject conflicting strategy kind. | Strategy with conflicting kind. | Diagnostic `conflicting_strategy_kind` is emitted. |
| `test-conflicting-2` | Reject conflicting plan steps. | Plan with conflicting steps. | Diagnostic `conflicting_plan_steps` is emitted. |

#### Unauthorized access tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-unauthorized-1` | Reject unauthorized strategy access. | Strategy access by unauthorized agent. | Diagnostic `unauthorized_strategy_access` is emitted. |
| `test-unauthorized-2` | Reject unauthorized plan access. | Plan access by unauthorized agent. | Diagnostic `unauthorized_plan_access` is emitted. |
| `test-unauthorized-3` | Reject unauthorized snapshot access. | Snapshot access by unauthorized agent. | Diagnostic `unauthorized_snapshot_access` is emitted. |

#### Budget exhaustion tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-budget-exhaustion-1` | Terminate on turn budget exhaustion. | Turn budget exhausted. | Diagnostic `turn_budget_exhausted` is emitted, strategy is terminated. |
| `test-budget-exhaustion-2` | Terminate on token budget exhaustion. | Token budget exhausted. | Diagnostic `token_budget_exhausted` is emitted, strategy is terminated. |
| `test-budget-exhaustion-3` | Terminate on tool budget exhaustion. | Tool budget exhausted. | Diagnostic `tool_budget_exhausted` is emitted, strategy is terminated. |
| `test-budget-exhaustion-4` | Terminate on cost budget exhaustion. | Cost budget exhausted. | Diagnostic `cost_budget_exhausted` is emitted, strategy is terminated. |
| `test-budget-exhaustion-5` | Terminate on time budget exhaustion. | Time budget exhausted. | Diagnostic `time_budget_exhausted` is emitted, strategy is terminated. |

#### Unavailable dependency tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-unavailable-1` | Handle model unavailable. | Model unavailable. | Diagnostic `model_unavailable` is emitted, retry or terminate. |
| `test-unavailable-2` | Handle tool unavailable. | Tool unavailable. | Diagnostic `tool_unavailable` is emitted, retry or terminate. |
| `test-unavailable-3` | Handle snapshot store unavailable. | Snapshot store unavailable. | Diagnostic `snapshot_store_unavailable` is emitted, retry or terminate. |

#### Invalid snapshot tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-invalid-snapshot-1` | Terminate on invalid snapshot. | Invalid snapshot. | Diagnostic `invalid_snapshot` is emitted, FSM transitions to `terminated`. |
| `test-invalid-snapshot-2` | Preserve invalid snapshot in history. | Invalid snapshot. | Invalid snapshot is preserved in history. |

#### Non-progress loop tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-nonprogress-loop-1` | Terminate on non-progress loop. | Non-progress loop detected. | Diagnostic `nonprogress_loop_detected` is emitted, FSM transitions to `terminated`. |

#### Repeated tool request tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-repeated-tool-request-1` | Terminate on repeated tool request. | Repeated tool request detected. | Diagnostic `repeated_tool_request_detected` is emitted, FSM transitions to `terminated`. |

#### Contradictory plan tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-contradictory-plan-1` | Terminate on contradictory plan. | Contradictory plan detected. | Diagnostic `contradictory_plan_detected` is emitted, FSM transitions to `terminated`. |

#### Missing result tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-missing-result-1` | Terminate on missing result after timeout. | Missing result after timeout. | Diagnostic `missing_result_detected` is emitted, FSM transitions to `terminated`. |

#### Model drift tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-model-drift-1` | Terminate on model drift. | Model drift detected. | Diagnostic `model_drift_detected` is emitted, FSM transitions to `terminated`. |

### Timeout, cancellation, and retry tests

> **Normative definition.**
The following tests verify that timeout, cancellation, unavailable dependency,
and retry behavior leave no unauthorized or partial state.

#### Timeout tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-timeout-1` | Terminate on strategy timeout. | Strategy timeout. | Strategy is terminated, no partial state remains. |
| `test-timeout-2` | Terminate on plan timeout. | Plan timeout. | Plan is terminated, no partial state remains. |
| `test-timeout-3` | Terminate on tool execution timeout. | Tool execution timeout. | Tool execution is terminated, no partial state remains. |
| `test-timeout-4` | Terminate on model request timeout. | Model request timeout. | Model request is terminated, no partial state remains. |

#### Cancellation tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-cancellation-1` | Cancel strategy execution. | Strategy cancellation request. | Strategy is cancelled, no partial state remains. |
| `test-cancellation-2` | Cancel plan execution. | Plan cancellation request. | Plan is cancelled, no partial state remains. |
| `test-cancellation-3` | Cancel tool execution. | Tool cancellation request. | Tool execution is cancelled, no partial state remains. |
| `test-cancellation-4` | Cancel model request. | Model cancellation request. | Model request is cancelled, no partial state remains. |

#### Unavailable dependency tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-unavailable-dependency-1` | Handle model unavailable and retry. | Model unavailable, retry enabled. | Model request is retried, no partial state remains. |
| `test-unavailable-dependency-2` | Handle tool unavailable and retry. | Tool unavailable, retry enabled. | Tool request is retried, no partial state remains. |
| `test-unavailable-dependency-3` | Handle snapshot store unavailable and retry. | Snapshot store unavailable, retry enabled. | Snapshot restoration is retried, no partial state remains. |

#### Retry tests

| Test ID | Description | Input | Expected output |
|---------|-------------|-------|-----------------|
| `test-retry-1` | Retry on transient model failure. | Transient model failure, retry enabled. | Model request is retried and succeeds. |
| `test-retry-2` | Retry on transient tool failure. | Transient tool failure, retry enabled. | Tool request is retried and succeeds. |
| `test-retry-3` | Retry on transient snapshot store failure. | Transient snapshot store failure, retry enabled. | Snapshot restoration is retried and succeeds. |

### Cross-milestone compatibility tests

> **Normative definition.**
The following tests run all earlier milestone fixtures affected by this
phase and record regressions or approved variability.

#### Milestone 1 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m1-fixture-1` | Run Milestone 1 profile vocabulary fixture. | Profile vocabulary fixture. | Fixture passes, no regressions. |
| `test-m1-fixture-2` | Run Milestone 1 stable identities fixture. | Stable identities fixture. | Fixture passes, no regressions. |
| `test-m1-fixture-3` | Run Milestone 1 agent manifests fixture. | Agent manifests fixture. | Fixture passes, no regressions. |

#### Milestone 2 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m2-fixture-1` | Run Milestone 2 signal envelopes fixture. | Signal envelopes fixture. | Fixture passes, no regressions. |
| `test-m2-fixture-2` | Run Milestone 2 actions and plans fixture. | Actions and plans fixture. | Fixture passes, no regressions. |
| `test-m2-fixture-3` | Run Milestone 2 state operations fixture. | State operations fixture. | Fixture passes, no regressions. |

#### Milestone 3 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m3-fixture-1` | Run Milestone 3 Extism invocation fixture. | Extism invocation fixture. | Fixture passes, no regressions. |
| `test-m3-fixture-2` | Run Milestone 3 mailboxes fixture. | Mailboxes fixture. | Fixture passes, no regressions. |
| `test-m3-fixture-3` | Run Milestone 3 agent registry fixture. | Agent registry fixture. | Fixture passes, no regressions. |

#### Milestone 4 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m4-fixture-1` | Run Milestone 4 snapshot journal fixture. | Snapshot journal fixture. | Fixture passes, no regressions. |
| `test-m4-fixture-2` | Run Milestone 4 atomic commit fixture. | Atomic commit fixture. | Fixture passes, no regressions. |
| `test-m4-fixture-3` | Run Milestone 4 effect handlers fixture. | Effect handlers fixture. | Fixture passes, no regressions. |

#### Milestone 5 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m5-fixture-1` | Run Milestone 5 threat model fixture. | Threat model fixture. | Fixture passes, no regressions. |
| `test-m5-fixture-2` | Run Milestone 5 capability policy fixture. | Capability policy fixture. | Fixture passes, no regressions. |
| `test-m5-fixture-3` | Run Milestone 5 provenance fixture. | Provenance fixture. | Fixture passes, no regressions. |

#### Milestone 6 fixtures

| Test ID | Description | Fixture | Expected output |
|---------|-------------|---------|-----------------|
| `test-m6-fixture-1` | Run Milestone 6 agent identity fixture. | Agent identity fixture. | Fixture passes, no regressions. |
| `test-m6-fixture-2` | Run Milestone 6 child lifecycle fixture. | Child lifecycle fixture. | Fixture passes, no regressions. |
| `test-m6-fixture-3` | Run Milestone 6 fan-out fan-in fixture. | Fan-out fan-in fixture. | Fixture passes, no regressions. |

## Test evidence requirements

> **Normative definition.**
Every test MUST produce the following evidence:

| Evidence type | Content |
|---------------|---------|
| `test.passed` | Evidence that the test passed. |
| `test.failed` | Evidence that the test failed, including diagnostic and stack trace. |
| `test.skipped` | Evidence that the test was skipped, including reason. |
| `test.regression` | Evidence of a regression in an earlier milestone fixture. |
| `test.variability` | Evidence of approved variability in an earlier milestone fixture. |

> **Normative definition.**
Test evidence MUST be retained for the lifetime of the milestone and made
available for review.

## Variability register

### 43.4.1 Test execution environment

- **Permission**: The host MAY configure the test execution environment (e.g., CI/CD, local).
- **Recommendation**: The host SHOULD run tests in CI/CD before merging to main.
- **Permitted presentation**: The host MAY present test results to the operator.
- **Limit**: The host MUST run all tests before promoting the milestone to `status: normative`.

### 43.4.2 Test retry behavior

- **Permission**: The host MAY configure retry behavior for transient failures.
- **Recommendation**: The host SHOULD retry transient failures up to 3 times.
- **Permitted presentation**: The host MAY present retry results to the operator.
- **Limit**: The host MUST not retry permanent failures.

### 43.4.3 Test timeout

- **Permission**: The host MAY configure test timeout different from the default.
- **Recommendation**: The host SHOULD use a timeout between 30 and 300 seconds per test.
- **Permitted presentation**: The host MAY present the configured timeout to the operator.
- **Limit**: The host MUST document the configured timeout.
