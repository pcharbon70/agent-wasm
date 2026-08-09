---
title: "Phase 3 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-03
  - implementation
  - contract
  - data-model
aliases:
  - "M7-P3 Contract And Data Model Implementation"
---

# Phase 3 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 3.1 from Phase 3 plan:
**Contract And Data Model** for Direct FSM Tool-Loop and Planning Strategies.

## Implementation notes

### Subtask 3.1.1.1 - Direct strategy behavior

Defined direct strategy behavior for one validated action and result without hidden continuation state.

**Key fields:**

| Field | Content | Source |
|-------|---------|--------|
| `strategy_kind` | The strategy kind (`direct`, `fsm`, `tool_loop`). | Host runtime |
| `strategy_id` | The `StrategyId` of the strategy instance. | Host runtime |
| `action_id` | The `ActionId` of the validated action being executed. | Host runtime |
| `result_id` | The `ResultId` of the result being processed. | Host runtime |
| `continuation` | The continuation state after processing (null if terminal). | Host runtime |
| `iteration` | The iteration counter for bounded execution. | Host runtime |
| `budget_remaining` | The remaining budget (turns, tokens, cost) for this iteration. | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the strategy transition. | Host clock |

**Key invariants:**

1. **No hidden state**: The strategy behavior is fully determined by the explicit input (action, result, current state) and produces deterministic output.

2. **Bounded continuation**: The continuation state is serialized as a snapshot and does not contain hidden runtime state.

3. **Iteration tracking**: Each strategy execution increments an iteration counter to enable budget enforcement.

4. **Budget accounting**: The strategy tracks remaining budget (turns, tokens, cost) and refuses to execute if the budget is exhausted.

### Subtask 3.1.1.2 - FSM strategy states and transitions

Defined FSM strategy states, events, guards, transitions, waiting points, snapshot schema, and migration.

**FSM states:**

| State | Description |
|-------|-------------|
| `idle` | Waiting for a new plan or directive. |
| `planning` | Generating a plan from the current state and instructions. |
| `waiting_for_tool` | Waiting for a tool execution to complete. |
| `waiting_for_model` | Waiting for a model response to complete. |
| `waiting_for_human` | Waiting for human approval or input. |
| `terminating` | Planning termination and emitting terminal signals. |
| `terminated` | Final state; no further transitions allowed. |

**FSM events:**

| Event | Cause | Next state (if guard passes) |
|-------|-------|------------------------------|
| `plan_submitted` | A new plan directive is submitted. | `idle` -> `planning` |
| `tool_completed` | A tool execution completes. | `waiting_for_tool` -> `planning` |
| `tool_failed` | A tool execution fails. | `waiting_for_tool` -> `planning` |
| `tool_cancelled` | A tool execution is cancelled. | `waiting_for_tool` -> `planning` |
| `tool_unavailable` | A tool execution cannot be completed. | `waiting_for_tool` -> `planning` |
| `model_completed` | A model response completes. | `waiting_for_model` -> `planning` |
| `model_failed` | A model response fails. | `waiting_for_model` -> `planning` |
| `model_cancelled` | A model response is cancelled. | `waiting_for_model` -> `planning` |
| `model_unavailable` | A model response cannot be completed. | `waiting_for_model` -> `planning` |
| `human_input` | Human provides input or approval. | `waiting_for_human` -> `planning` |
| `human_rejected` | Human rejects the plan. | `waiting_for_human` -> `planning` |
| `human_cancelled` | Human cancels the plan. | `waiting_for_human` -> `terminated` |
| `iteration_budget_exhausted` | The iteration budget is exhausted. | Any -> `terminated` |
| `turn_budget_exhausted` | The turn budget is exhausted. | Any -> `terminated` |
| `token_budget_exhausted` | The token budget is exhausted. | Any -> `terminated` |
| `cost_budget_exhausted` | The cost budget is exhausted. | Any -> `terminated` |
| `time_budget_exhausted` | The time budget is exhausted. | Any -> `terminated` |
| `recursion_budget_exhausted` | The recursion budget is exhausted. | Any -> `terminated` |
| `snapshot_restored` | A snapshot is restored from history. | Any -> `idle` |
| `invalid_snapshot` | The snapshot is invalid or incompatible. | Any -> `terminated` |
| `nonprogress_loop_detected` | The strategy enters a non-progress loop. | Any -> `terminated` |
| `repeated_tool_request_detected` | The strategy repeatedly requests the same tool. | Any -> `terminated` |
| `contradictory_plan_detected` | The strategy produces a contradictory plan. | Any -> `terminated` |
| `missing_result_detected` | A required result is missing. | Any -> `terminated` |
| `model_drift_detected` | The model drifts from the expected behavior. | Any -> `terminated` |

**Snapshot schema:**

| Field | Content | Source |
|-------|---------|--------|
| `snapshot_id` | The `SnapshotId` of the FSM snapshot. | Host runtime |
| `state` | The current FSM state. | Host runtime |
| `plan` | The current plan (if any). | Host runtime |
| `plan_index` | The index of the current step in the plan. | Host runtime |
| `waiting_for` | What the FSM is waiting for (tool, model, human). | Host runtime |
| `waiting_for_id` | The ID of the tool/model request being waited for. | Host runtime |
| `iteration` | The current iteration counter. | Host runtime |
| `budget_remaining` | The remaining budget. | Host runtime |
| `history` | The history of state transitions (bounded). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the snapshot. | Host clock |

**Migration rules:**

1. **Forward migration**: A snapshot can be restored only if it is compatible with the current schema version.

2. **Backward migration**: A snapshot can be migrated backward only if the migration is documented and tested.

3. **Invalid migration**: If a snapshot cannot be migrated, the FSM transitions to `terminated` and emits an `invalid_snapshot` diagnostic.

4. **Snapshot history**: The FSM maintains a bounded history of state transitions to detect non-progress loops.

5. **Snapshot rotation**: When the history exceeds the maximum size, the oldest entries are dropped.

### Subtask 3.1.1.3 - Bounded tool-loop state

Defined bounded tool-loop state for model request, tool selection, tool result, next-step decision, termination, and iteration budget.

**Tool-loop states:**

| State | Description |
|-------|-------------|
| `idle` | Waiting for a new plan or instruction. |
| `requesting_tool` | Selecting and requesting a tool. |
| `executing_tool` | The tool is executing. |
| `processing_result` | Processing the tool result. |
| `requesting_model` | Requesting a model response. |
| `processing_model` | Processing the model response. |
| `requesting_approval` | Requesting human approval. |
| `processing_approval` | Processing human approval. |
| `terminating` | Planning termination. |
| `terminated` | Final state. |

**Tool selection strategy:**

1. **Priority queue**: Tools are selected based on a priority queue that considers urgency, cost, and capability requirements.

2. **Capability matching**: The selected tool must have the required capabilities and be available in the current tenant scope.

3. **Budget awareness**: The selected tool must fit within the remaining budget (turns, tokens, cost, time).

4. **Deduplication**: The tool-loop avoids requesting the same tool repeatedly in a non-progress loop.

**Iteration budget:**

| Budget type | Default | Maximum | Enforcement |
|-------------|---------|---------|-------------|
| `turns` | 100 | 1000 | Host policy |
| `tokens` | 10000 | 100000 | Host policy |
| `cost` | 1.0 | 10.0 | Host policy |
| `time` | 60 | 600 | Host policy |
| `iterations` | 10 | 100 | Host policy |
| `recursion_depth` | 5 | 50 | Host policy |

**Termination conditions:**

1. **Budget exhaustion**: Any budget is exhausted.

2. **Invalid snapshot**: The snapshot is invalid or incompatible.

3. **Non-progress loop**: The tool-loop enters a non-progress loop.

4. **Repeated tool request**: The tool-loop repeatedly requests the same tool.

5. **Contradictory plan**: The plan is contradictory.

6. **Missing result**: A required result is missing.

7. **Model drift**: The model drifts from the expected behavior.

8. **Human cancellation**: Human cancels the plan.

9. **Terminal action**: The action completes successfully or fails fatally.

## Key design decisions

1. **Deterministic FSM**: The FSM is deterministic and fully specified by its states, events, guards, and transitions. There is no hidden state.

2. **Bounded iteration**: The tool-loop is bounded by iteration counters and budgets to prevent infinite loops.

3. **Snapshot-based state**: The FSM state is serialized as a snapshot and can be restored, migrated, or rolled back.

4. **Plan-driven execution**: The tool-loop executes a plan (sequence of steps) rather than unbounded private reasoning.

5. **Budget enforcement at host level**: Budget enforcement is done at the host level, not in the strategy, to prevent bypass.

6. **Diagnostic evidence**: Every state transition emits bounded diagnostics and evidence for observability.

7. **Migration versioning**: Snapshots are versioned and migrated explicitly to support schema evolution.

8. **Tool selection strategy**: Tools are selected based on a priority queue that considers urgency, cost, and capability requirements.

9. **Human-in-the-loop**: The FSM supports human approval and rejection of plans.

10. **Non-progress detection**: The FSM detects and terminates non-progress loops, repeated tool requests, and contradictory plans.

## Open questions

1. Should the FSM support parallel execution of multiple steps in a plan?

2. Should the tool selection strategy support preemption (interrupting a tool execution)?

3. Should the FSM support checkpointing to external storage (e.g., S3)?

4. Should the budget enforcement be strict (hard limits) or soft (warnings)?

5. Should the FSM support replay of state transitions for debugging?

6. Should the tool-loop support streaming results (e.g., for long-running tool executions)?

7. Should the FSM support multiple human approvers (e.g., for critical operations)?

8. Should the plan be versioned and immutable once submitted?

9. Should the FSM support hot-swapping the strategy at runtime?

10. Should the budget counters be reset on human approval or continue from the previous state?

11. Should the tool-loop support retry with exponential backoff for transient failures?

12. Should the FSM support conditional steps (e.g., "if tool A fails, do tool B")?

## Cross-references

### Earlier chapters

- [11-actions-instructions-validation-plans-and-results.md](../11-actions-instructions-validation-plans-and-results.md)
- [12-state-operations-patches-revisions-and-conflicts.md](../12-state-operations-patches-revisions-and-conflicts.md)
- [13-directives-strategies-continuations-and-terminal-states.md](../13-directives-strategies-continuations-and-terminal-states.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- [26-atomic-state-journal-and-directive-outbox-commits.md](../26-atomic-state-journal-and-directive-outbox-commits.md)
- [27-effect-handlers-attempts-idempotency-and-result-signals.md](../27-effect-handlers-attempts-idempotency-and-result-signals.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../31-capability-policy-attenuation-limits-and-enforcement.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../34-provenance-signing-audit-security-and-milestone-acceptance.md)

### Related chapters (Phase 3)

- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md](../43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md](../43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md](../43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md)
