---
title: "Direct FSM Tool-Loop And Planning Strategies Behavior And Integration"
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
  - behavior
  - integration
aliases:
  - "M7-P3 Behavior And Integration"
---

# Direct FSM Tool-Loop And Planning Strategies Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-03-direct-fsm-tool-loop-and-planning-strategies.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for direct FSM tool-loop
and planning strategies, including planning strategy outputs, budget
enforcement, and failure behavior for invalid snapshots, non-progress loops,
repeated tool requests, contradictory plans, missing results, model drift,
and forced termination.

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
[Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes](43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md),
[Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests](43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md).

## 43.2 Behavior And Integration

### Planning strategy outputs

> **Normative definition.**
The planning strategy produces reviewable plan state and directives rather
than unbounded private reasoning traces.
The plan state is visible to the operator and can be inspected at any time.

> **Normative definition.**
The planning strategy MUST produce the following outputs:

| Output | Content | Source |
|--------|---------|--------|
| `plan_id` | The `PlanId` of the plan. | Planning strategy |
| `plan_state` | The current state of the plan (`pending`, `active`, `completed`, `failed`, `cancelled`). | Planning strategy |
| `steps` | The sequence of steps in the plan. | Planning strategy |
| `current_step_index` | The index of the current step being executed. | Host runtime |
| `created_at` | The ISO 8601 timestamp of plan creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last plan update. | Host clock |
| `completed_at` | The ISO 8601 timestamp of plan completion (null if not complete). | Host clock |
| `failure_reason` | The reason for plan failure (null if not failed). | Planning strategy |
| `cancellation_reason` | The reason for plan cancellation (null if not cancelled). | Planning strategy |

> **Normative definition.**
The planning strategy MUST follow this flow:

1. **Input**: The planning strategy receives the current state, instructions, and available tools.

2. **Plan generation**: The planning strategy generates a plan (sequence of steps) based on the input.

3. **Plan validation**: The plan is validated against the current state and constraints.

4. **Plan submission**: The validated plan is submitted as a directive.

5. **Plan execution**: The tool-loop executes the plan step by step.

6. **Plan monitoring**: The planning strategy monitors the plan execution and reacts to events.

7. **Plan adaptation**: The planning strategy adapts the plan based on new information or failures.

8. **Plan completion**: The planning strategy completes the plan and emits results.

> **Normative definition.**
The planning strategy MUST enforce reviewability requirements:

1. **Plan visibility**: The plan state is visible to the operator and can be inspected at any time.

2. **Step visibility**: Each step in the plan is visible and can be inspected.

3. **Decision visibility**: The decisions made by the planning strategy are visible and can be audited.

4. **Adaptation visibility**: Any adaptations to the plan are visible and can be audited.

5. **Failure visibility**: Any failures are visible and include a reason.

### Budget enforcement

> **Normative definition.**
The host enforces turn, token, tool, cost, time, and recursion budgets in
host policy and strategy inputs.
Budget enforcement is done at the host level to prevent bypass.

> **Normative definition.**
The host MUST follow this budget enforcement flow:

1. **Budget initialization**: The host initializes the budgets for the strategy execution.

2. **Budget tracking**: The host tracks the remaining budgets for the strategy execution.

3. **Budget checking**: Before each strategy transition, the host checks if the budgets are exhausted.

4. **Budget deduction**: After each strategy transition, the host deducts the cost from the budgets.

5. **Budget exhaustion**: If any budget is exhausted, the host terminates the strategy execution.

> **Normative definition.**
The host MUST enforce the following budget types:

| Budget type | Unit | Tracked by | Checked by |
|-------------|------|------------|------------|
| `turns` | Number of turns | Host runtime | Host policy |
| `tokens` | Number of tokens | Host runtime | Host policy |
| `tools` | Number of tool executions | Host runtime | Host policy |
| `cost` | Monetary cost (e.g., USD) | Host runtime | Host policy |
| `time` | Elapsed time (e.g., seconds) | Host runtime | Host policy |
| `recursion_depth` | Recursion depth | Host runtime | Host policy |

> **Normative definition.**
The host MUST enforce budgets at the following points:

1. **Strategy initialization**: The host checks if the strategy can be initialized within the budgets.

2. **Strategy transition**: The host checks if the strategy transition is within the budgets.

3. **Tool execution**: The host checks if the tool execution is within the budgets.

4. **Model request**: The host checks if the model request is within the budgets.

5. **Plan submission**: The host checks if the plan submission is within the budgets.

6. **Plan adaptation**: The host checks if the plan adaptation is within the budgets.

> **Normative definition.**
When a budget is exhausted, the host MUST terminate the strategy execution
and emit the corresponding diagnostic:

| Budget type | Diagnostic |
|-------------|------------|
| `turns` | `turn_budget_exhausted` |
| `tokens` | `token_budget_exhausted` |
| `tools` | `tool_budget_exhausted` |
| `cost` | `cost_budget_exhausted` |
| `time` | `time_budget_exhausted` |
| `recursion_depth` | `recursion_budget_exhausted` |

### Invalid snapshot behavior

> **Normative definition.**
When the host detects an invalid snapshot during restoration, the FSM MUST
transition to `terminated` and emit an `invalid_snapshot` diagnostic.

> **Normative definition.**
The host MUST enforce the following invalid snapshot behavior:

1. **Detection**: The host detects an invalid snapshot during restoration.

2. **Termination**: The FSM transitions to `terminated` and emits an `invalid_snapshot` diagnostic.

3. **Evidence emission**: The host emits evidence with the invalid snapshot details.

4. **History preservation**: The invalid snapshot is preserved in history for debugging.

5. **No recovery**: The FSM does not attempt to recover from an invalid snapshot.

### Non-progress loop behavior

> **Normative definition.**
When the FSM detects a non-progress loop, the FSM MUST transition to
`terminated` and emit a `nonprogress_loop_detected` diagnostic.

> **Normative definition.**
A non-progress loop is detected when the same state is entered N times
without progress.
The threshold N is implementation-defined but MUST be documented.

> **Normative definition.**
The host MUST enforce the following non-progress loop behavior:

1. **Detection**: The FSM detects a non-progress loop by monitoring state transitions.

2. **Threshold**: A non-progress loop is detected when the same state is entered N times without progress.

3. **Termination**: The FSM transitions to `terminated` and emits a `nonprogress_loop_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the loop details (states, transitions, duration).

5. **History preservation**: The loop details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a non-progress loop.

### Repeated tool request behavior

> **Normative definition.**
When the FSM detects a repeated tool request, the FSM MUST transition to
`terminated` and emit a `repeated_tool_request_detected` diagnostic.

> **Normative definition.**
A repeated tool request is detected when the same tool is requested N times
without a different result.
The threshold N is implementation-defined but MUST be documented.

> **Normative definition.**
The host MUST enforce the following repeated tool request behavior:

1. **Detection**: The FSM detects a repeated tool request by monitoring tool requests.

2. **Threshold**: A repeated tool request is detected when the same tool is requested N times without a different result.

3. **Termination**: The FSM transitions to `terminated` and emits a `repeated_tool_request_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the repeated tool details (tool ID, request count, duration).

5. **History preservation**: The repeated tool details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a repeated tool request.

### Contradictory plan behavior

> **Normative definition.**
When the FSM detects a contradictory plan, the FSM MUST transition to
`terminated` and emit a `contradictory_plan_detected` diagnostic.

> **Normative definition.**
A contradictory plan includes conflicting tool requests, incompatible state
changes, or impossible conditions.

> **Normative definition.**
The host MUST enforce the following contradictory plan behavior:

1. **Detection**: The FSM detects a contradictory plan by comparing plan steps.

2. **Contradiction types**: Contradictions include conflicting tool requests, incompatible state changes, or impossible conditions.

3. **Termination**: The FSM transitions to `terminated` and emits a `contradictory_plan_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the contradictory plan details.

5. **History preservation**: The contradictory plan details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a contradictory plan.

### Missing result behavior

> **Normative definition.**
When the FSM detects a missing result, the FSM MUST transition to
`terminated` and emit a `missing_result_detected` diagnostic after waiting
for a configured timeout period.

> **Normative definition.**
The host MUST enforce the following missing result behavior:

1. **Detection**: The FSM detects a missing result when a required result is not available.

2. **Timeout**: The FSM waits for a configured timeout period for the result.

3. **Termination**: If the result is not available within the timeout, the FSM transitions to `terminated` and emits a `missing_result_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the missing result details (result ID, timeout duration).

5. **History preservation**: The missing result details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from a missing result.

### Model drift behavior

> **Normative definition.**
When the host detects model drift, the FSM MUST transition to `terminated`
and emit a `model_drift_detected` diagnostic.

> **Normative definition.**
Model drift is detected by comparing model behavior to expected behavior.
Drift indicators include unexpected output format, inconsistent results, or
performance degradation.

> **Normative definition.**
The host MUST enforce the following model drift behavior:

1. **Detection**: The host detects model drift by comparing model behavior to expected behavior.

2. **Drift indicators**: Drift indicators include unexpected output format, inconsistent results, or performance degradation.

3. **Termination**: The FSM transitions to `terminated` and emits a `model_drift_detected` diagnostic.

4. **Evidence emission**: The host emits evidence with the model drift details (drift indicators, comparison data).

5. **History preservation**: The model drift details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from model drift.

### Forced termination behavior

> **Normative definition.**
When forced termination is triggered, the FSM MUST perform cleanup and
transition to `terminated` and emit a `forced_termination` diagnostic.

> **Normative definition.**
Forced termination is triggered by human cancellation, budget exhaustion,
or critical failure.

> **Normative definition.**
The host MUST enforce the following forced termination behavior:

1. **Trigger**: Forced termination is triggered by human cancellation, budget exhaustion, or critical failure.

2. **Cleanup**: The FSM performs cleanup (e.g., cancelling in-progress tool executions, releasing resources).

3. **Termination**: The FSM transitions to `terminated` and emits a `forced_termination` diagnostic.

4. **Evidence emission**: The host emits evidence with the forced termination details (trigger, cleanup status).

5. **History preservation**: The forced termination details are preserved in history for debugging.

6. **No recovery**: The FSM does not attempt to recover from forced termination.

## Variability register

### 43.2.1 Non-progress loop threshold

- **Permission**: The host MAY configure the non-progress loop threshold (N) different from the default.
- **Recommendation**: The host SHOULD use a threshold between 3 and 10.
- **Permitted presentation**: The host MAY present the configured threshold to the operator.
- **Limit**: The host MUST document the configured threshold.

### 43.2.2 Repeated tool request threshold

- **Permission**: The host MAY configure the repeated tool request threshold (N) different from the default.
- **Recommendation**: The host SHOULD use a threshold between 3 and 10.
- **Permitted presentation**: The host MAY present the configured threshold to the operator.
- **Limit**: The host MUST document the configured threshold.

### 43.2.3 Missing result timeout

- **Permission**: The host MAY configure the missing result timeout different from the default.
- **Recommendation**: The host SHOULD use a timeout between 10 and 60 seconds.
- **Permitted presentation**: The host MAY present the configured timeout to the operator.
- **Limit**: The host MUST document the configured timeout.

### 43.2.4 Budget defaults

- **Permission**: The host MAY configure default budget values different from the defaults stated in Section 43.1.
- **Recommendation**: The host SHOULD use the default values stated in Section 43.1 as a starting point.
- **Permitted presentation**: The host MAY present the configured budget values to the operator.
- **Limit**: The host MUST not exceed the maximum values stated in Section 43.1.
