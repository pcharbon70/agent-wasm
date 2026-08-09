---
title: "Phase 3 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-03
  - implementation
  - integration-tests
  - verification
aliases:
  - "M7-P3 Integration Tests Implementation"
---

# Phase 3 Integration Tests Implementation

## Overview

This note documents the implementation of Section 3.4 from Phase 3 plan:
**Phase 3 Integration Tests** for Direct FSM Tool-Loop and Planning Strategies.

## Implementation notes

### Subtask 3.4.1.1 - Successful flow tests

Defined tests to verify the canonical successful flow and retained evidence for direct FSM tool-loop and planning strategies.

**Test categories:**

| Category | Description | Test count |
|----------|-------------|------------|
| Direct strategy success | Tests for direct strategy execution with valid input. | 5 |
| FSM state transitions | Tests for FSM state transitions with valid events. | 8 |
| Tool-loop execution | Tests for tool-loop execution with valid tool results. | 6 |
| Plan submission | Tests for plan submission with valid plans. | 4 |
| Budget tracking | Tests for budget tracking with valid budgets. | 3 |
| Snapshot restoration | Tests for snapshot restoration with valid snapshots. | 2 |
| Evidence emission | Tests for evidence emission with valid events. | 3 |

**Test details:**

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

### Subtask 3.4.1.2 - Failure handling tests

Defined tests to verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.

**Test categories:**

| Category | Description | Test count |
|----------|-------------|------------|
| Malformed input | Tests for malformed input detection. | 6 |
| Incompatible version | Tests for incompatible version detection. | 3 |
| Conflicting input | Tests for conflicting input detection. | 2 |
| Unauthorized access | Tests for unauthorized access detection. | 3 |
| Budget exhaustion | Tests for budget exhaustion detection. | 5 |
| Unavailable dependency | Tests for unavailable dependency detection. | 3 |
| Invalid snapshot | Tests for invalid snapshot detection. | 2 |
| Non-progress loop | Tests for non-progress loop detection. | 1 |
| Repeated tool request | Tests for repeated tool request detection. | 1 |
| Contradictory plan | Tests for contradictory plan detection. | 1 |
| Missing result | Tests for missing result detection. | 1 |
| Model drift | Tests for model drift detection. | 1 |

**Test details:**

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

### Subtask 3.4.1.3 - Timeout, cancellation, and retry tests

Defined tests to verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.

**Test categories:**

| Category | Description | Test count |
|----------|-------------|------------|
| Timeout | Tests for timeout behavior. | 4 |
| Cancellation | Tests for cancellation behavior. | 4 |
| Unavailable dependency | Tests for unavailable dependency behavior. | 3 |
| Retry | Tests for retry behavior. | 3 |

**Test details:**

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
| `test-timeout-2` | Cancel plan execution. | Plan cancellation request. | Plan is cancelled, no partial state remains. |
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

### Subtask 3.4.1.4 - Cross-milestone compatibility tests

Defined tests to run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

**Test categories:**

| Category | Description | Milestone | Test count |
|----------|-------------|-----------|------------|
| Milestone 1 fixtures | Tests for Milestone 1 fixtures affected by Phase 3. | 1 | 3 |
| Milestone 2 fixtures | Tests for Milestone 2 fixtures affected by Phase 3. | 2 | 3 |
| Milestone 3 fixtures | Tests for Milestone 3 fixtures affected by Phase 3. | 3 | 3 |
| Milestone 4 fixtures | Tests for Milestone 4 fixtures affected by Phase 3. | 4 | 3 |
| Milestone 5 fixtures | Tests for Milestone 5 fixtures affected by Phase 3. | 5 | 3 |
| Milestone 6 fixtures | Tests for Milestone 6 fixtures affected by Phase 3. | 6 | 3 |

**Test details:**

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

## Key design decisions

1. **Comprehensive test coverage**: Tests cover all aspects of Phase 3 (successful flow, failure handling, timeout/cancellation/retry, cross-milestone compatibility).

2. **Stable diagnostics**: Failure tests verify that failures produce stable diagnostics.

3. **No partial state**: Timeout, cancellation, and retry tests verify that no unauthorized or partial state remains.

4. **Cross-milestone compatibility**: Cross-milestone tests verify that Phase 3 does not break earlier milestones.

5. **Evidence retention**: Successful flow tests verify that evidence is retained for observability.

6. **Budget enforcement**: Budget tests verify that budgets are enforced correctly.

7. **Snapshot migration**: Snapshot tests verify that snapshots can be restored correctly.

8. **FSM state transitions**: FSM tests verify that state transitions are correct.

9. **Tool-loop execution**: Tool-loop tests verify that tool-loop execution is correct.

10. **Plan submission**: Plan tests verify that plans are submitted correctly.

## Open questions

1. Should the tests include performance benchmarks?

2. Should the tests include security tests (e.g., injection attacks)?

3. Should the tests include load tests (e.g., high concurrency)?

4. Should the tests include chaos tests (e.g., random failures)?

5. Should the tests be run automatically or manually?

6. Should the tests be run before or after code changes?

7. Should the tests be run in CI/CD or locally?

8. Should the tests include visual regression tests (e.g., UI changes)?

9. Should the tests include accessibility tests?

10. Should the tests include internationalization tests?

11. Should the tests include compatibility tests (e.g., different browsers)?

12. Should the tests include compliance tests (e.g., GDPR, HIPAA)?

## Cross-references

### Earlier chapters

- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [29-crash-injection-durable-effects-and-milestone-acceptance.md](../29-crash-injection-durable-effects-and-milestone-acceptance.md)

### Related chapters (Phase 3)

- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md](../43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md](../43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md)
