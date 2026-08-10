---
title: "Agentic Workflows Provenance Safety And Milestone Acceptance Contract And Data Model"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-05
  - workflows
  - provenance
  - safety
  - milestone-acceptance
  - contract
  - data-model
  - model-bindings
  - credential-custody
aliases:
  - "M7-P5 Contract And Data Model"
---

# Agentic Workflows Provenance Safety And Milestone Acceptance Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-05-agentic-workflows-provenance-safety-and-milestone-acceptance.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the contract and data model for agentic workflows, provenance,
safety, and milestone acceptance, including workflow types (direct model
response, structured response, model-to-tool continuation, retrieval-grounded
answer, code execution, multi-agent delegation), approval outcomes
(approval-required, denied, expired), quota exhaustion, revoked credential use,
cancelled model stream, and provenance references (model, tool, retrieval,
state revision, directive, attempt, policy).

Version `0.2.0` replaces direct provider/model request fields and
host-accessible revoked-secret semantics with logical model slots, pinned
binding references, and use-only credential lease outcomes.

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
[Agentic Workflows Provenance Safety And Milestone Acceptance Behavior And Integration](45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md),
[Agentic Workflows Provenance Safety And Milestone Acceptance Failure Evidence And Operational Notes](45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md).

## 45.1 Contract And Data Model

### Workflow types

> **Normative definition.**
A workflow is a bounded sequence of steps that an agent executes to produce
an answer or take an action. Workflows are separate from authoritative agent
state and audit evidence.

> **Normative definition.**
Every workflow MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `workflow_id` | The `WorkflowId` of the workflow. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `tenant_scope` | The tenant scope of the workflow. | Host runtime |
| `workflow_type` | The type of workflow (`direct-model-response`, `structured-response`, `model-to-tool-continuation`, `retrieval-grounded-answer`, `code-execution`, `multi-agent-delegation`). | Host runtime |
| `status` | The workflow status (`active`, `completed`, `cancelled`, `failed`). | Host runtime |
| `created_at` | The ISO 8601 timestamp of workflow creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last workflow update. | Host clock |
| `completed_at` | The ISO 8601 timestamp of workflow completion (null if not completed). | Host clock |

> **Normative definition.**
Workflow types are defined as follows:

| Type | Description |
|------|-------------|
| `direct-model-response` | Agent receives a direct response from the model. |
| `structured-response` | Agent receives a structured response with validated fields. |
| `model-to-tool-continuation` | Agent continues after model response with tool execution. |
| `retrieval-grounded-answer` | Agent answers using retrieved context. |
| `code-execution` | Agent executes code and uses the result. |
| `multi-agent-delegation` | Agent delegates work to child agents. |

#### Direct model response workflow

> **Normative definition.**
A direct model response workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `model_slot` | Logical model requirement used by the workflow. | Host runtime |
| `binding_id` | User-approved model binding identity. | Host runtime |
| `binding_revision` | Pinned model binding revision. | Host runtime |
| `request_id` | Durable materialized model request reference. | Host runtime |
| `response` | The model response. | Host runtime |
| `usage` | The model usage (tokens, cost). | Host runtime |

#### Structured response workflow

> **Normative definition.**
A structured response workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `schema` | The schema for the structured response. | Host runtime |
| `response` | The structured response (validated against schema). | Host runtime |
| `validation_errors` | Any validation errors (if response is invalid). | Host runtime |

#### Model-to-tool continuation workflow

> **Normative definition.**
A model-to-tool continuation workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `model_response` | The model response. | Host runtime |
| `plan` | The plan (sequence of steps) extracted from the model response. | Host runtime |
| `steps` | The executed steps. | Host runtime |
| `results` | The results of each step. | Host runtime |

#### Retrieval-grounded answer workflow

> **Normative definition.**
A retrieval-grounded answer workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `query` | The retrieval query. | Host runtime |
| `retrieved_context` | The retrieved context. | Host runtime |
| `answer` | The answer grounded in the retrieved context. | Host runtime |
| `citations` | The citations to the retrieved context. | Host runtime |

#### Code execution workflow

> **Normative definition.**
A code execution workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `code` | The code to execute. | Host runtime |
| `language` | The programming language. | Host runtime |
| `execution_result` | The execution result (output, errors). | Host runtime |
| `execution_time` | The execution time. | Host runtime |
| `memory_usage` | The memory usage. | Host runtime |

#### Multi-agent delegation workflow

> **Normative definition.**
A multi-agent delegation workflow includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `delegation_request` | The delegation request (task, parameters). | Host runtime |
| `child_agents` | The child agents that received the delegation. | Host runtime |
| `child_results` | The results from child agents. | Host runtime |
| `aggregated_result` | The aggregated result from child agents. | Host runtime |

### Approval outcomes

> **Normative definition.**
Approval-required tool use includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `tool_use_id` | The `ToolUseId` of the tool use. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `tool_id` | The `ToolId` of the tool. | Host runtime |
| `approval_request_id` | The `ApprovalId` of the approval request. | Host runtime |
| `status` | The approval status (`pending`, `approved`, `denied`). | Host runtime |
| `created_at` | The ISO 8601 timestamp of approval request creation. | Host clock |
| `decided_at` | The ISO 8601 timestamp of the approval decision (null if pending). | Host clock |
| `decided_by` | The `TenantQualifiedAgentAddress` that decided the approval (null if pending). | Host runtime |

> **Normative definition.**
A denied approval includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `approval_id` | The `ApprovalId` of the denied approval. | Host runtime |
| `reason` | The reason for denial. | Host runtime |
| `decided_at` | The ISO 8601 timestamp of the denial. | Host clock |
| `decided_by` | The `TenantQualifiedAgentAddress` that decided. | Host runtime |

> **Normative definition.**
An expired approval includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `approval_id` | The `ApprovalId` of the expired approval. | Host runtime |
| `expiry_at` | The ISO 8601 timestamp of the expiry. | Host clock |
| `status` | The status (`expired`). | Host runtime |

> **Normative definition.**
Quota exhaustion includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `quota_id` | The `QuotaId` of the exhausted quota. | Host runtime |
| `quota_type` | The type of quota (`tenant`, `agent`, `model`, `tool`). | Host runtime |
| `scope` | The scope of the quota. | Host runtime |
| `limit` | The quota limit. | Host runtime |
| `current_usage` | The current usage (equal to limit). | Host runtime |
| `exhausted_at` | The ISO 8601 timestamp of exhaustion. | Host clock |

> **Normative definition.**
Revoked credential use includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `lease_fingerprint` | Non-authority-bearing fingerprint of the revoked credential lease. | Host runtime |
| `custodian_id` | Registered credential custodian identity. | Host runtime |
| `principal` | The `TenantQualifiedAgentAddress` of the principal. | Host runtime |
| `resource` | The resource that was revoked. | Host runtime |
| `model_binding_id` | Associated model binding identity, if applicable. | Host runtime |
| `model_binding_revision` | Associated model binding revision, if applicable. | Host runtime |
| `revoked_at` | The ISO 8601 timestamp of revocation. | Host clock |
| `revoked_by` | The `TenantQualifiedAgentAddress` that revoked the lease. | Host runtime |

The record MUST NOT contain a credential, authentication header, opaque handle
reference, custodian endpoint, or provider request body.

> **Normative definition.**
Cancelled model stream includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `stream_id` | The `StreamId` of the cancelled model stream. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `model_slot` | Logical model slot used by the stream. | Host runtime |
| `binding_id` | Pinned user-approved model binding. | Host runtime |
| `binding_revision` | Pinned binding revision. | Host runtime |
| `cancelled_at` | The ISO 8601 timestamp of cancellation. | Host clock |
| `cancelled_by` | The `TenantQualifiedAgentAddress` that cancelled the stream. | Host runtime |

### Provenance references

> **Normative definition.**
Every answer in an agentic workflow MUST include provenance references that
link to the original evidence (model, tool, retrieval, state revision,
directive, attempt, policy) without exposing hidden secrets.

> **Normative definition.**
Every provenance reference MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `reference_id` | The `ReferenceId` of the provenance reference. | Host runtime |
| `answer_id` | The `AnswerId` of the answer that references this evidence. | Host runtime |
| `reference_type` | The type of reference (`model`, `tool`, `retrieval`, `state-revision`, `directive`, `attempt`, `policy`). | Host runtime |
| `reference_target` | The target of the reference (e.g., `ModelId`, `ToolId`). | Host runtime |
| `reference_context` | The context of the reference (e.g., response content, tool output). | Host runtime |
| `created_at` | The ISO 8601 timestamp of reference creation. | Host clock |

> **Normative definition.**
Provenance reference types are defined as follows:

| Type | Description |
|------|-------------|
| `model` | Reference to a model response. |
| `tool` | Reference to a tool output. |
| `retrieval` | Reference to retrieved context. |
| `state-revision` | Reference to a state revision. |
| `directive` | Reference to a directive. |
| `attempt` | Reference to an effect handler attempt. |
| `policy` | Reference to a policy decision. |

> **Normative definition.**
Provenance references MUST be bounded. They MUST NOT expose:
- Secrets or secret references.
- Internal host implementation details.
- Other agents' data or state.
- Sensitive model context (e.g., system prompts).

## Variability register

### 45.1.1 Workflow type extensibility

- **Permission**: The host MAY support custom workflow types beyond the six defined.
- **Recommendation**: The host SHOULD document any custom workflow types.
- **Permitted presentation**: The host MAY present custom workflow types to the operator.
- **Limit**: Custom workflow types MUST follow the same contract as built-in types.

### 45.1.2 Provenance reference deduplication

- **Permission**: The host MAY deduplicate provenance references (e.g., if the same model response is referenced multiple times).
- **Recommendation**: The host SHOULD deduplicate provenance references when possible.
- **Permitted presentation**: The host MAY present deduplication statistics to the operator.
- **Limit**: Deduplication MUST not lose any reference information.

### 45.1.3 Safety boundary configurability

- **Permission**: The host MAY configure safety boundaries per tenant, with per-agent override support for sandbox/power agent patterns.
- **Recommendation**: The host SHOULD support tenant-level configuration by default. Per-agent override lets tenants run agents with tighter limits (e.g., a sandbox agent at 50% of tenant budget). Per-workflow configuration is not supported — workflow types are internal implementation categories, not security boundaries.
- **Permitted presentation**: The host MAY present the configured safety boundaries to the operator.
- **Limit**: Safety boundaries MUST be enforced at all times.
