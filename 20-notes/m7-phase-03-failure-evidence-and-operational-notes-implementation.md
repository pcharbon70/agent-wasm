---
title: "Phase 3 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-03
  - implementation
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
aliases:
  - "M7-P3 Failure Evidence And Operational Notes Implementation"
---

# Phase 3 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 3.3 from Phase 3 plan:
**Failure Evidence And Operational Notes** for Direct FSM Tool-Loop and
Planning Strategies.

## Implementation notes

### Subtask 3.3.1.1 - Failure outcomes

Defined malformed, incompatible, conflicting, unauthorized, exhausted, and
unavailable outcomes relevant to direct FSM tool-loop and planning strategies.

**Malformed outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_strategy_input` | The strategy input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_strategy_input` diagnostic. |
| `malformed_plan_input` | The plan input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_plan_input` diagnostic. |
| `malformed_snapshot_input` | The snapshot input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_snapshot_input` diagnostic. |
| `malformed_budget_input` | The budget input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_budget_input` diagnostic. |

**Incompatible outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_strategy_version` | The strategy version is incompatible with the host version. | Reject the input and emit an `incompatible_strategy_version` diagnostic. |
| `incompatible_plan_version` | The plan version is incompatible with the host version. | Reject the input and emit an `incompatible_plan_version` diagnostic. |
| `incompatible_snapshot_version` | The snapshot version is incompatible with the host version. | Reject the input and emit an `incompatible_snapshot_version` diagnostic. |

**Conflicting outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_strategy_kind` | The strategy kind is conflicting with the current strategy kind. | Reject the input and emit a `conflicting_strategy_kind` diagnostic. |
| `conflicting_plan_steps` | The plan steps are conflicting (e.g., conflicting tool requests, incompatible state changes). | Reject the plan and emit a `conflicting_plan_steps` diagnostic. |

**Unauthorized outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_strategy_access` | The agent is not authorized to use the strategy. | Reject the input and emit an `unauthorized_strategy_access` diagnostic. |
| `unauthorized_plan_access` | The agent is not authorized to submit the plan. | Reject the input and emit an `unauthorized_plan_access` diagnostic. |
| `unauthorized_snapshot_access` | The agent is not authorized to restore the snapshot. | Reject the input and emit an `unauthorized_snapshot_access` diagnostic. |

**Exhausted outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `turn_budget_exhausted` | The turn budget is exhausted. | Terminate the strategy execution and emit a `turn_budget_exhausted` diagnostic. |
| `token_budget_exhausted` | The token budget is exhausted. | Terminate the strategy execution and emit a `token_budget_exhausted` diagnostic. |
| `tool_budget_exhausted` | The tool budget is exhausted. | Terminate the strategy execution and emit a `tool_budget_exhausted` diagnostic. |
| `cost_budget_exhausted` | The cost budget is exhausted. | Terminate the strategy execution and emit a `cost_budget_exhausted` diagnostic. |
| `time_budget_exhausted` | The time budget is exhausted. | Terminate the strategy execution and emit a `time_budget_exhausted` diagnostic. |
| `recursion_budget_exhausted` | The recursion budget is exhausted. | Terminate the strategy execution and emit a `recursion_budget_exhausted` diagnostic. |
| `iteration_budget_exhausted` | The iteration budget is exhausted. | Terminate the strategy execution and emit an `iteration_budget_exhausted` diagnostic. |

**Unavailable outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model_unavailable` | The model is unavailable (e.g., network error, service down). | Retry the model request or terminate the strategy execution and emit a `model_unavailable` diagnostic. |
| `tool_unavailable` | The tool is unavailable (e.g., network error, service down). | Retry the tool request or terminate the strategy execution and emit a `tool_unavailable` diagnostic. |
| `snapshot_store_unavailable` | The snapshot store is unavailable (e.g., network error, service down). | Retry the snapshot restoration or terminate the strategy execution and emit a `snapshot_store_unavailable` diagnostic. |

### Subtask 3.3.1.2 - Bounded diagnostics and evidence emission

Defined bounded diagnostics and evidence emission that identify the phase
contract, profile, and failed boundary without exposing secrets.

**Bounded diagnostics schema:**

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic_id` | The `DiagnosticId` of the diagnostic. | Host runtime |
| `diagnostic_code` | The diagnostic code (e.g., `malformed_strategy_input`, `turn_budget_exhausted`). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-03`). | Host runtime |
| `section` | The section identifier (`3.1`, `3.2`, `3.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `strategy.input`, `budget.check`, `plan.validation`). | Host runtime |
| `profile` | The profile identifier (if applicable). | Host runtime |
| `message` | A human-readable message describing the diagnostic. | Host runtime |
| `details` | Additional details about the diagnostic (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the diagnostic. | Host clock |

**Evidence emission schema:**

| Field | Content | Source |
|-------|---------|--------|
| `evidence_id` | The `EvidenceId` of the evidence. | Host runtime |
| `evidence_type` | The evidence type (`fsm.state_transition`, `fsm.budget_exhaustion`, `fsm.nonprogress_loop`, `fsm.repeated_tool_request`, `fsm.contradictory_plan`, `fsm.missing_result`, `fsm.model_drift`, `fsm.forced_termination`, `fsm.invalid_snapshot`). | Host runtime |
| `strategy_id` | The `StrategyId` of the strategy instance. | Host runtime |
| `plan_id` | The `PlanId` of the plan (if applicable). | Host runtime |
| `snapshot_id` | The `SnapshotId` of the snapshot (if applicable). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-03`). | Host runtime |
| `section` | The section identifier (`3.1`, `3.2`, `3.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `strategy.input`, `budget.check`, `plan.validation`). | Host runtime |
| `details` | Additional details about the evidence (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the evidence. | Host clock |

**Evidence types:**

| Evidence type | Description |
|---------------|-------------|
| `fsm.state_transition` | Emitted when the FSM transitions between states. |
| `fsm.budget_exhaustion` | Emitted when a budget is exhausted. |
| `fsm.nonprogress_loop` | Emitted when a non-progress loop is detected. |
| `fsm.repeated_tool_request` | Emitted when a repeated tool request is detected. |
| `fsm.contradictory_plan` | Emitted when a contradictory plan is detected. |
| `fsm.missing_result` | Emitted when a missing result is detected. |
| `fsm.model_drift` | Emitted when model drift is detected. |
| `fsm.forced_termination` | Emitted when forced termination is triggered. |
| `fsm.invalid_snapshot` | Emitted when an invalid snapshot is detected. |

### Subtask 3.3.1.3 - Implementation-defined choices

Documented implementation-defined choices, deferred work, and any result that
would invalidate an earlier milestone assumption.

**Implementation-defined choices:**

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Non-progress loop threshold (N) | 5 | MUST be documented in host configuration. |
| Repeated tool request threshold (N) | 5 | MUST be documented in host configuration. |
| Missing result timeout | 30 seconds | MUST be documented in host configuration. |
| Budget default values | As stated in Section 43.1 | MUST be documented in host configuration. |
| Budget maximum values | As stated in Section 43.1 | MUST be documented in host configuration. |
| Snapshot history size | 100 transitions | MUST be documented in host configuration. |
| Plan step visibility | All steps visible | MUST be documented in host configuration. |
| Decision auditing | All decisions audited | MUST be documented in host configuration. |

**Deferred work:**

| Item | Description | Priority |
|------|-------------|----------|
| Parallel step execution | Support parallel execution of multiple steps in a plan. | Medium |
| Soft budget enforcement | Support soft budget enforcement (warnings) in addition to hard limits. | Low |
| Step preemption | Support preemption (interrupting a step execution). | Medium |
| Snapshot external storage | Support checkpointing to external storage (e.g., S3). | Low |
| Statistical model drift detection | Support statistical analysis for model drift detection. | Medium |
| Hot-swap planning strategy | Support hot-swapping the planning strategy at runtime. | Low |
| Plan adaptation rollback | Support rollback (undoing adaptations). | Medium |
| Budget exhaustion human approval | Support human approval for budget exhaustion. | Low |
| Multiple human approvers | Support multiple human approvers for critical operations. | Medium |
| Forced termination external cleanup | Support cleanup of in-progress external requests (e.g., HTTP calls). | High |

**Results that would invalidate earlier milestone assumptions:**

| Result | Description | Impact |
|--------|-------------|--------|
| None yet | No results have been identified that invalidate earlier milestone assumptions. | None |

## Key design decisions

1. **Bounded diagnostics**: Diagnostics are bounded and do not expose secrets.

2. **Evidence emission**: Every failure emits bounded evidence for observability and debugging.

3. **Implementation-defined choices**: Implementation-defined choices are documented in host configuration.

4. **Deferred work**: Deferred work is tracked with priority and description.

5. **Milestone assumption validation**: Results that invalidate earlier milestone assumptions are tracked and documented.

6. **Diagnostic codes**: Diagnostic codes are standardized and consistent across phases.

7. **Evidence types**: Evidence types are standardized and consistent across phases.

8. **Contract identification**: Diagnostics and evidence identify the contract and section that failed.

9. **Boundary identification**: Diagnostics and evidence identify the failed boundary.

10. **Profile identification**: Diagnostics and evidence identify the profile (if applicable).

## Open questions

1. Should the non-progress loop threshold be adaptive (based on plan complexity)?

2. Should the repeated tool request threshold be adaptive (based on tool reliability)?

3. Should the missing result timeout be adaptive (based on tool latency)?

4. Should budget defaults be per-agent or global?

5. Should snapshot history size be configurable per strategy?

6. Should plan step visibility be configurable (e.g., hide sensitive steps)?

7. Should decision auditing be configurable (e.g., skip auditing for low-risk decisions)?

8. Should model drift detection use statistical analysis or rule-based?

9. Should the FSM support parallel execution of multiple steps in a plan?

10. Should the budget enforcement support soft limits (warnings) in addition to hard limits?

11. Should the planning strategy support preemption (interrupting a step execution)?

12. Should the FSM support checkpointing to external storage (e.g., S3)?

## Cross-references

### Earlier chapters

- [10-signals-causality-routing-and-delivery.md](../60-specification/10-signals-causality-routing-and-delivery.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [29-crash-injection-durable-effects-and-milestone-acceptance.md](../60-specification/29-crash-injection-durable-effects-and-milestone-acceptance.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

### Related chapters (Phase 3)

- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md)
