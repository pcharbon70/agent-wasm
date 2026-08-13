---
title: "Phase 3 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-03
  - implementation
  - behavior
  - integration
aliases:
  - "M7-P3 Behavior And Integration Implementation"
---

# Phase 3 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 3.2 from Phase 3 plan:
**Behavior And Integration** for Direct FSM Tool-Loop and Planning Strategies.

## Implementation notes

### Subtask 3.2.1.1 - Planning strategy outputs

Defined planning strategy outputs as reviewable plan state and directives rather than unbounded private reasoning traces.

**Planning strategy flow:**

1. **Input**: The planning strategy receives the current state, instructions, and available tools.

2. **Plan generation**: The planning strategy generates a plan (sequence of steps) based on the input.

3. **Plan validation**: The plan is validated against the current state and constraints.

4. **Plan submission**: The validated plan is submitted as a directive.

5. **Plan execution**: The tool-loop executes the plan step by step.

6. **Plan monitoring**: The planning strategy monitors the plan execution and reacts to events.

7. **Plan adaptation**: The planning strategy adapts the plan based on new information or failures.

8. **Plan completion**: The planning strategy completes the plan and emits results.

**Plan state schema:**

| Field | Content | Source |
|-------|---------|--------|
| `plan_id` | The `PlanId` of the plan. | Host runtime |
| `plan_state` | The current state of the plan (`pending`, `active`, `completed`, `failed`, `cancelled`). | Host runtime |
| `steps` | The sequence of steps in the plan. | Planning strategy |
| `current_step_index` | The index of the current step being executed. | Host runtime |
| `created_at` | The ISO 8601 timestamp of plan creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last plan update. | Host clock |
| `completed_at` | The ISO 8601 timestamp of plan completion (null if not complete). | Host clock |
| `failure_reason` | The reason for plan failure (null if not failed). | Host runtime |
| `cancellation_reason` | The reason for plan cancellation (null if not cancelled). | Host runtime |

**Directive submission:**

1. **Plan directive**: The planning strategy submits a plan directive to the host.

2. **Step directives**: The planning strategy submits step directives for each step in the plan.

3. **Adaptation directives**: The planning strategy submits adaptation directives to modify the plan.

4. **Completion directives**: The planning strategy submits completion directives when the plan is complete.

5. **Cancellation directives**: The planning strategy submits cancellation directives when the plan is cancelled.

**Reviewability requirements:**

1. **Plan visibility**: The plan state is visible to the operator and can be inspected at any time.

2. **Step visibility**: Each step in the plan is visible and can be inspected.

3. **Decision visibility**: The decisions made by the planning strategy are visible and can be audited.

4. **Adaptation visibility**: Any adaptations to the plan are visible and can be audited.

5. **Failure visibility**: Any failures are visible and include a reason.

### Subtask 3.2.1.2 - Budget enforcement

Defined turn, token, tool, cost, time, and recursion budgets in host policy and strategy inputs.

**Budget enforcement flow:**

1. **Budget initialization**: The host initializes the budgets for the strategy execution.

2. **Budget tracking**: The host tracks the remaining budgets for the strategy execution.

3. **Budget checking**: Before each strategy transition, the host checks if the budgets are exhausted.

4. **Budget deduction**: After each strategy transition, the host deducts the cost from the budgets.

5. **Budget exhaustion**: If any budget is exhausted, the host terminates the strategy execution.

**Budget types:**

| Budget type | Unit | Tracked by | Checked by |
|-------------|------|------------|------------|
| `turns` | Number of turns | Host runtime | Host policy |
| `tokens` | Number of tokens | Host runtime | Host policy |
| `tools` | Number of tool executions | Host runtime | Host policy |
| `cost` | Monetary cost (e.g., USD) | Host runtime | Host policy |
| `time` | Elapsed time (e.g., seconds) | Host runtime | Host policy |
| `recursion_depth` | Recursion depth | Host runtime | Host policy |

**Budget configuration:**

| Budget type | Default | Maximum | Source |
|-------------|---------|---------|--------|
| `turns` | 100 | 1000 | Host configuration |
| `tokens` | 10000 | 100000 | Host configuration |
| `tools` | 50 | 500 | Host configuration |
| `cost` | 1.0 | 10.0 | Host configuration |
| `time` | 60 | 600 | Host configuration |
| `recursion_depth` | 5 | 50 | Host configuration |

**Budget enforcement points:**

1. **Strategy initialization**: The host checks if the strategy can be initialized within the budgets.

2. **Strategy transition**: The host checks if the strategy transition is within the budgets.

3. **Tool execution**: The host checks if the tool execution is within the budgets.

4. **Model request**: The host checks if the model request is within the budgets.

5. **Plan submission**: The host checks if the plan submission is within the budgets.

6. **Plan adaptation**: The host checks if the plan adaptation is within the budgets.

**Budget exhaustion behavior:**

1. **Turn budget exhausted**: The strategy execution is terminated with a `turn_budget_exhausted` diagnostic.

2. **Token budget exhausted**: The strategy execution is terminated with a `token_budget_exhausted` diagnostic.

3. **Tool budget exhausted**: The strategy execution is terminated with a `tool_budget_exhausted` diagnostic.

4. **Cost budget exhausted**: The strategy execution is terminated with a `cost_budget_exhausted` diagnostic.

5. **Time budget exhausted**: The strategy execution is terminated with a `time_budget_exhausted` diagnostic.

6. **Recursion budget exhausted**: The strategy execution is terminated with a `recursion_budget_exhausted` diagnostic.

### Subtask 3.2.1.3 - Failure behavior

Defined invalid snapshot, nonprogress loop, repeated tool request, contradictory plan, missing result, model drift, and forced termination behavior.

**Invalid snapshot behavior:**

1. **Detection**: The host detects an invalid snapshot during restoration.

2. **Termination**: The FSM transitions to `terminated` and emits an `invalid_snapshot` diagnostic.

3. **Evidence emission**: The host emits evidence with the invalid snapshot details.

4. **History preservation**: The invalid snapshot is preserved in history for debugging.

5. **No recovery**: The FSM does not attempt to recover from an invalid snapshot.

**Non-progress loop behavior:**

1. **Detection**: The FSM detects a non-progress loop by monitoring state transitions.

2. **Threshold**: A non-progress loop is detected when the same state is entered N times without progress.

3. **Termination**: The FSM transitions to `terminated` and emits a `nonprogress_loop_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the loop details (states, transitions, duration).

5. **History preservation**: The loop details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a non-progress loop.

**Repeated tool request behavior:**

1. **Detection**: The FSM detects a repeated tool request by monitoring tool requests.

2. **Threshold**: A repeated tool request is detected when the same tool is requested N times without a different result.

3. **Termination**: The FSM transitions to `terminated` and emits a `repeated_tool_request_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the repeated tool details (tool ID, request count, duration).

5. **History preservation**: The repeated tool details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a repeated tool request.

**Contradictory plan behavior:**

1. **Detection**: The FSM detects a contradictory plan by comparing plan steps.

2. **Contradiction types**: Contradictions include conflicting tool requests, incompatible state changes, or impossible conditions.

3. **Termination**: The FSM transitions to `terminated` and emits a `contradictory_plan_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the contradictory plan details.

5. **History preservation**: The contradictory plan details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a contradictory plan.

**Missing result behavior:**

1. **Detection**: The FSM detects a missing result when a required result is not available.

2. **Timeout**: The FSM waits for a configured timeout period for the result.

3. **Termination**: If the result is not available within the timeout, the FSM transitions to `terminated` and emits a `missing_result_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the missing result details (result ID, timeout duration).

5. **History preservation**: The missing result details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a missing result.

**Model drift behavior:**

1. **Detection**: The host detects model drift by comparing model behavior to expected behavior.

2. **Drift indicators**: Drift indicators include unexpected output format, inconsistent results, or performance degradation.

3. **Termination**: The FSM transitions to `terminated` and emits a `model_drift_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the model drift details (drift indicators, comparison data).

5. **History preservation**: The model drift details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from model drift.

**Forced termination behavior:**

1. **Trigger**: Forced termination is triggered by human cancellation, budget exhaustion, or critical failure.

2. **Cleanup**: The FSM performs cleanup (e.g., cancelling in-progress tool executions, releasing resources).

3. **Termination**: The FSM transitions to `terminated` and emits a `forced_termination` diagnostic.

4. **Evidence emission**: The host emits evidence with the forced termination details (trigger, cleanup status).

5. **History preservation**: The forced termination details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from forced termination.

## Key design decisions

1. **Reviewable plans**: Plans are reviewable and auditable, not hidden private reasoning traces.

2. **Host-enforced budgets**: Budgets are enforced at the host level, not in the strategy, to prevent bypass.

3. **Explicit failure detection**: Failure detection is explicit and documented, not implicit or hidden.

4. **Bounded history**: The FSM maintains a bounded history of state transitions for non-progress detection.

5. **No recovery from critical failures**: The FSM does not attempt to recover from critical failures (invalid snapshot, non-progress loop, etc.).

6. **Evidence emission**: Every failure emits bounded evidence for observability and debugging.

7. **Plan adaptation**: The planning strategy can adapt the plan based on new information or failures.

8. **Step-level visibility**: Each step in the plan is visible and can be inspected.

9. **Decision auditing**: The decisions made by the planning strategy are visible and can be audited.

10. **Forced termination**: The FSM supports forced termination by human cancellation, budget exhaustion, or critical failure.

## Open questions

1. Should the FSM support parallel execution of multiple steps in a plan?

2. Should the budget enforcement be strict (hard limits) or soft (warnings)?

3. Should the planning strategy support preemption (interrupting a step execution)?

4. Should the FSM support checkpointing to external storage (e.g., S3)?

5. Should the non-progress detection threshold be configurable?

6. Should the repeated tool request detection threshold be configurable?

7. Should the model drift detection be based on statistical analysis or rule-based?

8. Should the FSM support hot-swapping the planning strategy at runtime?

9. Should the plan adaptation support rollback (undoing adaptations)?

10. Should the budget exhaustion trigger human approval or automatic termination?

11. Should the FSM support multiple human approvers (e.g., for critical operations)?

12. Should the forced termination trigger cleanup of in-progress external requests (e.g., HTTP calls)?

## Cross-references

### Earlier chapters

- [11-actions-instructions-validation-plans-and-results.md](../../60-specification/11-actions-instructions-validation-plans-and-results.md)
- [13-directives-strategies-continuations-and-terminal-states.md](../../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- [27-effect-handlers-attempts-idempotency-and-result-signals.md](../../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)

### Related chapters (Phase 3)

- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md](../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md](../../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md)
