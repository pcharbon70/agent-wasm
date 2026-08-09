---
title: "Direct FSM Tool-Loop And Planning Strategies Contract And Data Model"
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
  - contract
  - data-model
aliases:
  - "M7-P3 Contract And Data Model"
---

# Direct FSM Tool-Loop And Planning Strategies Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-03-direct-fsm-tool-loop-and-planning-strategies.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the contract and data model for direct FSM tool-loop and
planning strategies, including direct strategy behavior, FSM states and
transitions, bounded tool-loop state, iteration budgets, and snapshot
migration.

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
[Direct FSM Tool-Loop And Planning Strategies Behavior And Integration](43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md),
[Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes](43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md),
[Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests](43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md).

## 43.1 Contract And Data Model

### Direct strategy behavior

> **Normative definition.**
A direct strategy executes one validated action and produces one result
without hidden continuation state.
The strategy is fully determined by its explicit inputs (action, result,
current state) and produces deterministic output.

> **Normative definition.**
Every direct strategy instance MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `strategy_kind` | The strategy kind (`direct`, `fsm`, `tool_loop`). | Host runtime |
| `strategy_id` | The `StrategyId` of the strategy instance. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent using this strategy. | Host runtime |
| `action_id` | The `ActionId` of the validated action being executed. | Host runtime |
| `result_id` | The `ResultId` of the result being processed. | Host runtime |
| `continuation` | The continuation state after processing (null if terminal). | Host runtime |
| `iteration` | The iteration counter for bounded execution. | Host runtime |
| `budget_remaining` | The remaining budget (turns, tokens, cost) for this iteration. | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the strategy transition. | Host clock |

> **Normative definition.**
The direct strategy MUST produce the following outputs:

| Output | Content | Source |
|--------|---------|--------|
| `next_action` | The next action to execute (if any). | Strategy |
| `next_directive` | The next directive to submit (if any). | Strategy |
| `termination_signal` | The termination signal (if the strategy is complete). | Strategy |
| `diagnostics` | The bounded diagnostics for observability. | Strategy |
| `evidence` | The evidence record for the strategy transition. | Strategy |

> **Normative definition.**
The direct strategy MUST enforce the following invariants:

1. **No hidden state**: The strategy behavior is fully determined by the explicit input (action, result, current state) and produces deterministic output.

2. **Bounded continuation**: The continuation state is serialized as a snapshot and does not contain hidden runtime state.

3. **Iteration tracking**: Each strategy execution increments an iteration counter to enable budget enforcement.

4. **Budget accounting**: The strategy tracks remaining budget (turns, tokens, cost) and refuses to execute if the budget is exhausted.

5. **Deterministic output**: For the same input and state, the strategy produces the same output.

### FSM strategy states and transitions

> **Normative definition.**
The FSM strategy maintains explicit state, events, guards, and transitions
to drive bounded tool-loop execution.
The FSM transitions are deterministic and fully specified by its schema.

> **Normative definition.**
The FSM strategy MUST support the following states:

| State | Description |
|-------|-------------|
| `idle` | Waiting for a new plan or directive. |
| `planning` | Generating a plan from the current state and instructions. |
| `waiting_for_tool` | Waiting for a tool execution to complete. |
| `waiting_for_model` | Waiting for a model response to complete. |
| `waiting_for_human` | Waiting for human approval or input. |
| `terminating` | Planning termination and emitting terminal signals. |
| `terminated` | Final state; no further transitions allowed. |

> **Normative definition.**
The FSM strategy MUST handle the following events:

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

> **Normative definition.**
The FSM strategy MUST include the following snapshot fields:

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

> **Normative definition.**
The FSM strategy MUST enforce the following snapshot migration rules:

1. **Forward migration**: A snapshot can be restored only if it is compatible with the current schema version.

2. **Backward migration**: A snapshot can be migrated backward only if the migration is documented and tested.

3. **Invalid migration**: If a snapshot cannot be migrated, the FSM transitions to `terminated` and emits an `invalid_snapshot` diagnostic.

4. **Snapshot history**: The FSM maintains a bounded history of state transitions to detect non-progress loops.

5. **Snapshot rotation**: When the history exceeds the maximum size, the oldest entries are dropped.

### Bounded tool-loop state

> **Normative definition.**
The bounded tool-loop maintains explicit state for model request, tool
selection, tool result, next-step decision, termination, and iteration
budget.
The tool-loop is bounded by iteration counters and budgets to prevent
infinite loops.

> **Normative definition.**
The bounded tool-loop MUST support the following states:

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

> **Normative definition.**
The bounded tool-loop MUST enforce the following tool selection strategy:

1. **Priority queue**: Tools are selected based on a priority queue that considers urgency, cost, and capability requirements.

2. **Capability matching**: The selected tool must have the required capabilities and be available in the current tenant scope.

3. **Budget awareness**: The selected tool must fit within the remaining budget (turns, tokens, cost, time).

4. **Deduplication**: The tool-loop avoids requesting the same tool repeatedly in a non-progress loop.

> **Normative definition.**
The bounded tool-loop MUST enforce the following iteration budgets:

| Budget type | Default | Maximum | Enforcement |
|-------------|---------|---------|-------------|
| `turns` | 100 | 1000 | Host policy |
| `tokens` | 10000 | 100000 | Host policy |
| `cost` | 1.0 | 10.0 | Host policy |
| `time` | 60 | 600 | Host policy |
| `iterations` | 10 | 100 | Host policy |
| `recursion_depth` | 5 | 50 | Host policy |

> **Normative definition.**
The bounded tool-loop MUST terminate under the following conditions:

1. **Budget exhaustion**: Any budget is exhausted.

2. **Invalid snapshot**: The snapshot is invalid or incompatible.

3. **Non-progress loop**: The tool-loop enters a non-progress loop.

4. **Repeated tool request**: The tool-loop repeatedly requests the same tool.

5. **Contradictory plan**: The plan is contradictory.

6. **Missing result**: A required result is missing.

7. **Model drift**: The model drifts from the expected behavior.

8. **Human cancellation**: Human cancels the plan.

9. **Terminal action**: The action completes successfully or fails fatally.

## Variability register

### 43.1.1 Default budget values

- **Permission**: The host MAY configure default budget values different from the defaults stated in this chapter.
- **Recommendation**: The host SHOULD use the default values stated in this chapter as a starting point.
- **Permitted presentation**: The host MAY present the configured budget values to the operator or administrator.
- **Limit**: The host MUST not exceed the maximum values stated in this chapter.

### 43.1.2 Snapshot migration

- **Permission**: The host MAY implement custom snapshot migration logic.
- **Recommendation**: The host SHOULD implement the migration rules stated in this chapter.
- **Permitted presentation**: The host MAY log migration events for observability.
- **Limit**: The host MUST not allow invalid migrations to proceed.

### 43.1.3 Tool selection strategy

- **Permission**: The host MAY implement a custom tool selection strategy.
- **Recommendation**: The host SHOULD implement the priority queue strategy stated in this chapter.
- **Permitted presentation**: The host MAY log tool selection decisions for observability.
- **Limit**: The host MUST enforce capability matching and budget awareness.
