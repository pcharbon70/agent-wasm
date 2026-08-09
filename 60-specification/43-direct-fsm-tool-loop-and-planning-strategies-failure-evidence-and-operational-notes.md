---
title: "Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes"
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
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
aliases:
  - "M7-P3 Failure Evidence And Operational Notes"
---

# Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-03-direct-fsm-tool-loop-and-planning-strategies.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for direct FSM
tool-loop and planning strategies, including failure outcomes, bounded
diagnostics, evidence emission, implementation-defined choices, deferred
work, and results that would invalidate earlier milestone assumptions.

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
[Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests](43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md).

## 43.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The following failure outcomes are normative invariants that every host
implementation MUST handle correctly for direct FSM tool-loop and planning
strategies.
Each outcome describes a specific failure condition and the expected host
behavior.

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_strategy_input` | The strategy input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_strategy_input` diagnostic. |
| `malformed_plan_input` | The plan input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_plan_input` diagnostic. |
| `malformed_snapshot_input` | The snapshot input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_snapshot_input` diagnostic. |
| `malformed_budget_input` | The budget input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_budget_input` diagnostic. |

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_strategy_version` | The strategy version is incompatible with the host version. | Reject the input and emit an `incompatible_strategy_version` diagnostic. |
| `incompatible_plan_version` | The plan version is incompatible with the host version. | Reject the input and emit an `incompatible_plan_version` diagnostic. |
| `incompatible_snapshot_version` | The snapshot version is incompatible with the host version. | Reject the input and emit an `incompatible_snapshot_version` diagnostic. |

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_strategy_kind` | The strategy kind is conflicting with the current strategy kind. | Reject the input and emit a `conflicting_strategy_kind` diagnostic. |
| `conflicting_plan_steps` | The plan steps are conflicting (e.g., conflicting tool requests, incompatible state changes). | Reject the plan and emit a `conflicting_plan_steps` diagnostic. |

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_strategy_access` | The agent is not authorized to use the strategy. | Reject the input and emit an `unauthorized_strategy_access` diagnostic. |
| `unauthorized_plan_access` | The agent is not authorized to submit the plan. | Reject the input and emit an `unauthorized_plan_access` diagnostic. |
| `unauthorized_snapshot_access` | The agent is not authorized to restore the snapshot. | Reject the input and emit an `unauthorized_snapshot_access` diagnostic. |

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `turn_budget_exhausted` | The turn budget is exhausted. | Terminate the strategy execution and emit a `turn_budget_exhausted` diagnostic. |
| `token_budget_exhausted` | The token budget is exhausted. | Terminate the strategy execution and emit a `token_budget_exhausted` diagnostic. |
| `tool_budget_exhausted` | The tool budget is exhausted. | Terminate the strategy execution and emit a `tool_budget_exhausted` diagnostic. |
| `cost_budget_exhausted` | The cost budget is exhausted. | Terminate the strategy execution and emit a `cost_budget_exhausted` diagnostic. |
| `time_budget_exhausted` | The time budget is exhausted. | Terminate the strategy execution and emit a `time_budget_exhausted` diagnostic. |
| `recursion_budget_exhausted` | The recursion budget is exhausted. | Terminate the strategy execution and emit a `recursion_budget_exhausted` diagnostic. |
| `iteration_budget_exhausted` | The iteration budget is exhausted. | Terminate the strategy execution and emit an `iteration_budget_exhausted` diagnostic. |

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model_unavailable` | The model is unavailable (e.g., network error, service down). | Retry the model request or terminate the strategy execution and emit a `model_unavailable` diagnostic. |
| `tool_unavailable` | The tool is unavailable (e.g., network error, service down). | Retry the tool request or terminate the strategy execution and emit a `tool_unavailable` diagnostic. |
| `snapshot_store_unavailable` | The snapshot store is unavailable (e.g., network error, service down). | Retry the snapshot restoration or terminate the strategy execution and emit a `snapshot_store_unavailable` diagnostic. |

### Bounded diagnostics

> **Normative definition.**
Every diagnostic MUST include the following fields:

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

> **Normative definition.**
Diagnostics MUST be bounded and MUST NOT expose secrets.

### Evidence emission

> **Normative definition.**
Every evidence record MUST include the following fields:

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

> **Normative definition.**
Evidence records MUST be bounded and MUST NOT expose secrets.

> **Normative definition.**
The following evidence types are normative:

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

### Implementation-defined choices

> **Normative definition.**
The following implementation-defined choices MUST be documented in host configuration:

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

### Deferred work

> **Non-normative guidance.**
The following work is deferred to future phases:

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

### Results that would invalidate earlier milestone assumptions

> **Non-normative guidance.**
The following results would invalidate earlier milestone assumptions:

| Result | Description | Impact |
|--------|-------------|--------|
| None yet | No results have been identified that invalidate earlier milestone assumptions. | None |

## Variability register

### 43.3.1 Non-progress loop threshold

- **Permission**: The host MAY configure the non-progress loop threshold (N) different from the default.
- **Recommendation**: The host SHOULD use a threshold between 3 and 10.
- **Permitted presentation**: The host MAY present the configured threshold to the operator.
- **Limit**: The host MUST document the configured threshold.

### 43.3.2 Repeated tool request threshold

- **Permission**: The host MAY configure the repeated tool request threshold (N) different from the default.
- **Recommendation**: The host SHOULD use a threshold between 3 and 10.
- **Permitted presentation**: The host MAY present the configured threshold to the operator.
- **Limit**: The host MUST document the configured threshold.

### 43.3.3 Missing result timeout

- **Permission**: The host MAY configure the missing result timeout different from the default.
- **Recommendation**: The host SHOULD use a timeout between 10 and 60 seconds.
- **Permitted presentation**: The host MAY present the configured timeout to the operator.
- **Limit**: The host MUST document the configured timeout.

### 43.3.4 Budget defaults

- **Permission**: The host MAY configure default budget values different from the defaults stated in Section 43.1.
- **Recommendation**: The host SHOULD use the default values stated in Section 43.1 as a starting point.
- **Permitted presentation**: The host MAY present the configured budget values to the operator.
- **Limit**: The host MUST not exceed the maximum values stated in Section 43.1.

### 43.3.5 Snapshot history size

- **Permission**: The host MAY configure the snapshot history size different from the default.
- **Recommendation**: The host SHOULD use a size between 50 and 200 transitions.
- **Permitted presentation**: The host MAY present the configured size to the operator.
- **Limit**: The host MUST document the configured size.

### 43.3.6 Plan step visibility

- **Permission**: The host MAY configure plan step visibility different from the default.
- **Recommendation**: The host SHOULD make all steps visible by default.
- **Permitted presentation**: The host MAY present the configured visibility to the operator.
- **Limit**: The host MUST document the configured visibility.

### 43.3.7 Decision auditing

- **Permission**: The host MAY configure decision auditing different from the default.
- **Recommendation**: The host SHOULD audit all decisions by default.
- **Permitted presentation**: The host MAY present the configured auditing to the operator.
- **Limit**: The host MUST document the configured auditing.
