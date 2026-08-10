---
title: "Agentic Workflows Provenance Safety And Milestone Acceptance Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-05
  - workflows
  - safety
  - provenance
  - milestone-acceptance
  - behavior
  - integration
  - model-bindings
  - credential-custody
aliases:
  - "M7-P5 Behavior And Integration"
---

# Agentic Workflows Provenance Safety And Milestone Acceptance Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-05-agentic-workflows-provenance-safety-and-milestone-acceptance.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for agentic workflows,
provenance, safety, and milestone acceptance, including hostile output
validation, loop termination under budgets, deterministic resume from
snapshots, and the Milestone 7 workflow corpus with provenance coverage,
safety boundaries, cost evidence, and residual model-quality limitations.

Version `0.2.0` aligns workflow safety with user-selected model bindings and
use-only credential custody. Workflow execution cannot change a pinned model
selection or obtain raw provider credentials.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
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
[Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes](43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md),
[Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests](43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md),
[Agentic Workflows Provenance Safety And Milestone Acceptance Contract And Data Model](45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md),
[Agentic Workflows Provenance Safety And Milestone Acceptance Failure Evidence And Operational Notes](45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md).

## 45.2 Behavior And Integration

### Hostile output validation

> **Normative definition.**
The host MUST validate hostile model/tool output before state, model context,
downstream tool, or user-facing admission.

> **Normative definition.**
Validation MUST occur at the following points:

| Validation point | Description |
|------------------|-------------|
| `state_admission` | Validate output before writing to agent state. |
| `model_context_admission` | Validate output before injecting into model context. |
| `downstream_tool_admission` | Validate output before passing to downstream tools. |
| `user_facing_admission` | Validate output before presenting to users. |

> **Normative definition.**
Validation MUST enforce the following constraints:

| Constraint | Description |
|------------|-------------|
| `schema_validation` | Validate output against the expected schema. |
| `length_limits` | Validate output length against limits. |
| `content_filters` | Validate output against content filters (e.g., hate speech, PII). |

> **Normative definition.**
The host MUST handle hostile output as follows:

| Behavior | Description |
|----------|-------------|
| `rejected` | Output is rejected and not admitted. |
| `sanitized` | Output is sanitized (e.g., truncated, filtered) and admitted. |
| `admitted` | Output is admitted as-is. |

> **Normative definition.**
The host MUST log hostile output detection and action for audit.

> **Normative definition.**
Evidence types for hostile output are defined as follows:

| Evidence type | Description |
|---------------|-------------|
| `hostile_output.detected` | Emitted when hostile output is detected. |
| `hostile_output.rejected` | Emitted when hostile output is rejected. |
| `hostile_output.sanitized` | Emitted when hostile output is sanitized. |
| `hostile_output.admitted` | Emitted when hostile output is admitted. |

### Loop termination and deterministic resume

> **Normative definition.**
Workflows MUST terminate under the following budget constraints:

| Budget | Description | Default limit |
|--------|-------------|---------------|
| `iterations` | Maximum number of iterations in a workflow. | 100 |
| `tools` | Maximum number of tool invocations in a workflow. | 50 |
| `time` | Maximum execution time for a workflow. | 300 seconds |
| `cost` | Maximum cost for a workflow. | 0.10 USD |
| `tokens` | Maximum tokens consumed by a workflow. | 10000 |

> **Normative definition.**
When a budget is exhausted, the host MUST:
1. Terminate the workflow.
2. Mark the workflow status as `failed` (or `completed` if partial results are acceptable).
3. Emit a `workflow.budget_exhausted` diagnostic.
4. Emit a `workflow.budget_exhausted` evidence entry.
5. Preserve the workflow state and result signals for later inspection.

> **Normative definition.**
Workflows MUST resume deterministically from durable strategy snapshots and
result signals. The resume process includes:

1. **Snapshot restoration**: The host restores the strategy snapshot from durable storage.
2. **Result signal replay**: The host replays result signals to reconstruct the workflow state.
3. **Continuation**: The host continues the workflow from the restored state.

> **Normative definition.**
Strategy snapshots MUST include:
- The current state of the FSM.
- The current state of the tool-loop.
- The current plan (sequence of steps).
- Any pending approvals or directives.
- Any pending external requests.

> **Normative definition.**
Result signals MUST include:
- The signal ID.
- The source (model, tool, retrieval, etc.).
- The content (response, output, etc.).
- The timestamp.
- The causal link to the previous signal.

> **Normative definition.**
Loop termination behaviors are defined as follows:

| Behavior | Description |
|----------|-------------|
| `terminated_normal` | The workflow terminated normally (completed or failed). |
| `terminated_budget` | The workflow terminated due to budget exhaustion. |
| `terminated_cancelled` | The workflow was cancelled. |
| `terminated_error` | The workflow terminated due to an error. |

> **Normative definition.**
Deterministic resume behaviors are defined as follows:

| Behavior | Description |
|----------|-------------|
| `resume_success` | The workflow resumed successfully from the snapshot. |
| `resume_failed` | The workflow failed to resume from the snapshot. |
| `resume_not_needed` | The workflow did not need to resume (completed or failed). |

### Milestone 7 workflow corpus

> **Normative definition.**
The Milestone 7 workflow corpus includes the following workflow types:

| Workflow type | Description | Coverage |
|---------------|-------------|----------|
| `direct-model-response` | Agent receives a direct response from the model. | 100% |
| `structured-response` | Agent receives a structured response with validated fields. | 100% |
| `model-to-tool-continuation` | Agent continues after model response with tool execution. | 100% |
| `retrieval-grounded-answer` | Agent answers using retrieved context. | 100% |
| `code-execution` | Agent executes code and uses the result. | 100% |
| `multi-agent-delegation` | Agent delegates work to child agents. | 100% |

> **Normative definition.**
Provenance coverage includes the following reference types:

| Reference type | Description | Coverage |
|----------------|-------------|----------|
| `model` | Reference to a model response. | 100% |
| `tool` | Reference to a tool output. | 100% |
| `retrieval` | Reference to retrieved context. | 100% |
| `state-revision` | Reference to a state revision. | 100% |
| `directive` | Reference to a directive. | 100% |
| `attempt` | Reference to an effect handler attempt. | 100% |
| `policy` | Reference to a policy decision. | 100% |

> **Normative definition.**
Safety boundaries include the following:

| Boundary | Description | Enforcement |
|----------|-------------|-------------|
| `quotas` | Enforce tenant/agent/model/tool quotas. | Host enforces at reservation, consumption, release, reconciliation. |
| `approvals` | Require approval for sensitive operations. | Host enforces approval workflow with eligible approvers, decision options, expiry, escalation. |
| `credentials` | Keep authenticated provider authority use-only and auditable. | User-controlled custodian enforces typed operations, scope, nonce, budget, revocation, and receipts; separated-custody host and Port processes never receive raw credentials. |
| `hostile output` | Validate and filter hostile output. | Host enforces validation at state, model context, downstream tool, and user-facing admission points. |
| `budgets` | Enforce workflow budgets (iterations, tools, time, cost, tokens). | Host enforces at workflow execution with deterministic resume from snapshots. |

Every model step MUST use the `model_slot` and binding revision recorded by
the durable model request. Resume, retry, tool continuation, and delegation
MUST NOT select a different provider, model, connection, or credential
custodian. A binding change applies only to a new model intent after user
approval.

> **Normative definition.**
Cost evidence includes the following metrics:

| Cost metric | Description | Measurement |
|-------------|-------------|-------------|
| `model_cost` | Cost of model invocations. | Tracked per workflow, per tenant, per agent. |
| `tool_cost` | Cost of tool invocations. | Tracked per workflow, per tenant, per agent. |
| `storage_cost` | Cost of storage (snapshots, journals, etc.). | Tracked per tenant, per agent. |
| `total_cost` | Total cost of all resources. | Sum of model, tool, and storage costs. |

> **Normative definition.**
Residual model-quality limitations include the following:

| Limitation | Description | Mitigation |
|------------|-------------|------------|
| `hallucination` | Model generates false or misleading information. | Retrieval-grounded answers, fact-checking tools, confidence scoring. |
| `inconsistency` | Model generates inconsistent responses across similar queries. | Structured responses, schema validation, deterministic FSM. |
| `bias` | Model generates biased or unfair responses. | Content filters, diversity monitoring, human review. |
| `toxicity` | Model generates toxic or harmful content. | Content filters, toxicity detection, human review. |
| `privacy` | Model generates responses that leak private information. | PII detection, redaction, access controls. |
| `context_limit` | Model is limited by context window size. | Chunking, summarization, retrieval-augmented generation. |
| `latency` | Model responses have high latency. | Caching, parallel processing, streaming. |
| `cost` | Model invocations are expensive. | Quotas, budget enforcement, cost optimization. |

## Variability register

### 45.2.1 Budget configurability

- **Permission**: The host MAY configure workflow budgets per tenant, with per-agent override support. Tenants are the natural billing and trust boundary — they own their agents and should control spend. Per-agent override lets a tenant run a "sandbox" agent with tighter limits while a "power" agent gets the full amount. Per-workflow configuration is not supported.
- **Recommendation**: The host SHOULD support tenant-level configuration by default.
- **Permitted presentation**: The host MAY present the configured budgets to the operator.
- **Limit**: Budgets MUST be enforced at all times.

### 45.2.2 Hostile output custom rules

- **Permission**: The host MAY support a host-configurable declarative validation pipeline beyond built-in rules (schema, length, content filters). Different tenants have different requirements — a healthcare tenant needs HIPAA-sensitive filtering, a fintech tenant needs PII/redaction rules. Custom rules should be expressed declaratively (regex patterns, schema extensions, policy scripts) rather than arbitrary code, so the host can audit and sandbox them.
- **Recommendation**: The host SHOULD document any custom validation rules and ensure they compose with built-in filters in a defined order.
- **Permitted presentation**: The host MAY present custom validation rules to the operator.
- **Limit**: Custom rules MUST not bypass built-in safety boundaries. Earlier rules take precedence over later ones.

### 45.2.3 Deterministic resume partial results

- **Permission**: The host MAY support partial results on deterministic resume, but only when explicitly opted in by the workflow author via a workflow-level field (`partial_results_allowed: true/false`). Some workflows (e.g., multi-step research) are fine with partial results — "here's what we found so far." Others (e.g., financial transactions) are not — partial execution is meaningless. The opt-in mechanism lets the workflow author declare intent. The resume behavior itself is deterministic — the same snapshot always produces the same continuation.
- **Recommendation**: The host SHOULD return partial results when the workflow author has opted in and partial results are available.
- **Permitted presentation**: The host MAY present partial results to the user.
- **Limit**: Partial results MUST be clearly marked as incomplete. Without explicit opt-in, the host MUST NOT return partial results automatically.

### 45.2.4 Residual limitation quantification

- **Permission**: The host MAY quantify residual model-quality limitations (e.g., hallucination rate) and expose them in operator dashboards and audit logs. Quantified metrics are operational data, not normative thresholds — the framework cannot enforce model quality, which depends on the model, not the framework. Saying "hallucination rate < 5%" in a spec implies the framework can enforce it, which it cannot. Thresholds belong in tenant-level policy, not the framework spec.
- **Recommendation**: The host SHOULD report quantified limitations in operator dashboards so operators can make informed decisions (e.g., "model A has 2% hallucination rate, model B has 8% — choose based on your use case").
- **Permitted presentation**: The host MAY present quantified limitations to the operator.
- **Limit**: Quantified limitations MUST be based on empirical data and MUST NOT be used as normative compliance thresholds. The spec requires completeness of the provenance reference structure; quantified reporting is a host implementation concern.
