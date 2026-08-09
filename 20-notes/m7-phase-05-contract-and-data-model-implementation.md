---
title: "Phase 5 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-05
  - implementation
  - contract
  - data-model
  - workflows
  - provenance
  - safety
  - milestone-acceptance
aliases:
  - "M7-P5 Contract And Data Model Implementation"
---

# Phase 5 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 5.1 from Phase 5 plan:
**Contract And Data Model** for Agentic Workflows, Provenance, Safety,
And Milestone Acceptance.

## Implementation notes

### Subtask 5.1.1.1 - Workflow types

Defined workflow types for direct model response, structured response,
model-to-tool continuation, retrieval-grounded answer, code execution, and
multi-agent delegation.

**Workflow schema:**

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

**Workflow types:**

| Type | Description |
|------|-------------|
| `direct-model-response` | Agent receives a direct response from the model. |
| `structured-response` | Agent receives a structured response with validated fields. |
| `model-to-tool-continuation` | Agent continues after model response with tool execution. |
| `retrieval-grounded-answer` | Agent answers using retrieved context. |
| `code-execution` | Agent executes code and uses the result. |
| `multi-agent-delegation` | Agent delegates work to child agents. |

**Direct model response workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `model_address` | The `TenantQualifiedAgentAddress` of the model. | Host runtime |
| `request` | The model request (prompt, parameters). | Host runtime |
| `response` | The model response. | Host runtime |
| `usage` | The model usage (tokens, cost). | Host runtime |

**Structured response workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `schema` | The schema for the structured response. | Host runtime |
| `response` | The structured response (validated against schema). | Host runtime |
| `validation_errors` | Any validation errors (if response is invalid). | Host runtime |

**Model-to-tool continuation workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `model_response` | The model response. | Host runtime |
| `plan` | The plan (sequence of steps) extracted from the model response. | Host runtime |
| `steps` | The executed steps. | Host runtime |
| `results` | The results of each step. | Host runtime |

**Retrieval-grounded answer workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `query` | The retrieval query. | Host runtime |
| `retrieved_context` | The retrieved context. | Host runtime |
| `answer` | The answer grounded in the retrieved context. | Host runtime |
| `citations` | The citations to the retrieved context. | Host runtime |

**Code execution workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `code` | The code to execute. | Host runtime |
| `language` | The programming language. | Host runtime |
| `execution_result` | The execution result (output, errors). | Host runtime |
| `execution_time` | The execution time. | Host runtime |
| `memory_usage` | The memory usage. | Host runtime |

**Multi-agent delegation workflow:**

| Field | Content | Source |
|-------|---------|--------|
| `delegation_request` | The delegation request (task, parameters). | Host runtime |
| `child_agents` | The child agents that received the delegation. | Host runtime |
| `child_results` | The results from child agents. | Host runtime |
| `aggregated_result` | The aggregated result from child agents. | Host runtime |

### Subtask 5.1.1.2 - Approval outcomes

Defined approval-required tool use, denied approval, expired approval,
quota exhaustion, revoked secret, and cancelled model stream.

**Approval-required tool use:**

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

**Denied approval:**

| Field | Content | Source |
|-------|---------|--------|
| `approval_id` | The `ApprovalId` of the denied approval. | Host runtime |
| `reason` | The reason for denial. | Host runtime |
| `decided_at` | The ISO 8601 timestamp of the denial. | Host clock |
| `decided_by` | The `TenantQualifiedAgentAddress` that decided. | Host runtime |

**Expired approval:**

| Field | Content | Source |
|-------|---------|--------|
| `approval_id` | The `ApprovalId` of the expired approval. | Host runtime |
| `expiry_at` | The ISO 8601 timestamp of the expiry. | Host clock |
| `status` | The status (`expired`). | Host runtime |

**Quota exhaustion:**

| Field | Content | Source |
|-------|---------|--------|
| `quota_id` | The `QuotaId` of the exhausted quota. | Host runtime |
| `quota_type` | The type of quota (`tenant`, `agent`, `model`, `tool`). | Host runtime |
| `scope` | The scope of the quota. | Host runtime |
| `limit` | The quota limit. | Host runtime |
| `current_usage` | The current usage (equal to limit). | Host runtime |
| `exhausted_at` | The ISO 8601 timestamp of exhaustion. | Host clock |

**Revoked secret:**

| Field | Content | Source |
|-------|---------|--------|
| `lease_id` | The `LeaseId` of the revoked secret lease. | Host runtime |
| `principal` | The `TenantQualifiedAgentAddress` of the principal. | Host runtime |
| `resource` | The resource that was revoked. | Host runtime |
| `revoked_at` | The ISO 8601 timestamp of revocation. | Host clock |
| `revoked_by` | The `TenantQualifiedAgentAddress` that revoked the lease. | Host runtime |

**Cancelled model stream:**

| Field | Content | Source |
|-------|---------|--------|
| `stream_id` | The `StreamId` of the cancelled model stream. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `model_address` | The `TenantQualifiedAgentAddress` of the model. | Host runtime |
| `cancelled_at` | The ISO 8601 timestamp of cancellation. | Host clock |
| `cancelled_by` | The `TenantQualifiedAgentAddress` that cancelled the stream. | Host runtime |

### Subtask 5.1.1.3 - Provenance references

Verified every answer can reference model, tool, retrieval, state revision,
directive, attempt, and policy evidence without exposing hidden secrets.

**Provenance reference schema:**

| Field | Content | Source |
|-------|---------|--------|
| `reference_id` | The `ReferenceId` of the provenance reference. | Host runtime |
| `answer_id` | The `AnswerId` of the answer that references this evidence. | Host runtime |
| `reference_type` | The type of reference (`model`, `tool`, `retrieval`, `state-revision`, `directive`, `attempt`, `policy`). | Host runtime |
| `reference_target` | The target of the reference (e.g., `ModelId`, `ToolId`). | Host runtime |
| `reference_context` | The context of the reference (e.g., response content, tool output). | Host runtime |
| `created_at` | The ISO 8601 timestamp of reference creation. | Host clock |

**Reference types:**

| Type | Description |
|------|-------------|
| `model` | Reference to a model response. |
| `tool` | Reference to a tool output. |
| `retrieval` | Reference to retrieved context. |
| `state-revision` | Reference to a state revision. |
| `directive` | Reference to a directive. |
| `attempt` | Reference to an effect handler attempt. |
| `policy` | Reference to a policy decision. |

**Provenance coverage:**

Every answer in an agentic workflow MUST include provenance references that:
- Identify the source of each piece of information (model, tool, retrieval, etc.).
- Link to the original evidence without exposing hidden secrets.
- Enable audit and debugging.

**Bounded evidence:**

Provenance references MUST be bounded. They MUST NOT expose:
- Secrets or secret references.
- Internal host implementation details.
- Other agents' data or state.
- Sensitive model context (e.g., system prompts).

## Key design decisions

1. **Workflow types**: Six workflow types cover the main agentic patterns (direct response, structured response, model-to-tool, retrieval-grounded, code execution, multi-agent delegation).

2. **Approval outcomes**: Approval outcomes include pending, approved, denied, expired, and quota exhaustion.

3. **Secret revocation**: Secret leases can be revoked, invalidating the principal's access.

4. **Model stream cancellation**: Model streams can be cancelled by the agent or host.

5. **Provenance references**: Every answer includes provenance references that link to the original evidence.

6. **Bounded evidence**: Provenance references are bounded and do not expose secrets.

7. **Reference types**: Seven reference types cover all evidence sources (model, tool, retrieval, state revision, directive, attempt, policy).

8. **Milestone acceptance**: Milestone 7 acceptance requires evidence that workflows are durable, bounded, attributable, interruptible, and controlled by host policy.

9. **Safety boundaries**: Host policy enforces safety boundaries (quotas, approvals, secret access) on all workflows.

10. **Residual model-quality limitations**: The spec documents known limitations in model quality (e.g., hallucination, inconsistency) that cannot be fully eliminated by the framework.

## Open questions

1. Should workflow types be extensible (allow custom workflow types)?

2. Should approval requests support conditional approval (e.g., "approve if X")?

3. Should quota exhaustion support burst allowances (temporary overages)?

4. Should secret lease revocation support grace periods (allow in-progress operations to complete)?

5. Should model stream cancellation support partial results (return what was received before cancellation)?

6. Should provenance references support hierarchical scoping (e.g., tenant, agent, workflow)?

7. Should provenance references support deduplication (e.g., if the same model response is referenced multiple times)?

8. Should workflow types support sub-workflows (e.g., a multi-agent delegation workflow contains child workflow instances)?

9. Should milestone acceptance criteria include performance benchmarks (e.g., response time, cost)?

10. Should safety boundaries be configurable per tenant, per agent, or per workflow?

11. Should residual model-quality limitations be quantified (e.g., "model hallucination rate < 5%")?

12. Should provenance references support automatic cleanup (e.g., when the answer is deleted)?

## Cross-references

### Earlier chapters

- [41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md](../41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- [42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md](../42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)

### Related chapters (Phase 5)

- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md)
