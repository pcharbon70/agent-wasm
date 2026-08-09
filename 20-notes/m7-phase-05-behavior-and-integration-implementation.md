---
title: "Phase 5 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-05
  - implementation
  - behavior
  - integration
  - workflows
  - safety
  - provenance
  - milestone-acceptance
aliases:
  - "M7-P5 Behavior And Integration Implementation"
---

# Phase 5 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 5.2 from Phase 5 plan:
**Behavior And Integration** for Agentic Workflows, Provenance, Safety,
And Milestone Acceptance.

## Implementation notes

### Subtask 5.2.1.1 - Hostile output validation

Verified hostile model/tool output is validated before state, model context,
downstream tool, or user-facing admission.

**Hostile output validation:**

| Validation point | Description | Enforcement |
|------------------|-------------|-------------|
| `state_admission` | Validate output before writing to agent state. | Host enforces schema validation, length limits, and content filters. |
| `model_context_admission` | Validate output before injecting into model context. | Host enforces token limits, schema validation, and content filters. |
| `downstream_tool_admission` | Validate output before passing to downstream tools. | Host enforces input schema validation, length limits, and content filters. |
| `user_facing_admission` | Validate output before presenting to users. | Host enforces content filters, redaction, and PII detection. |

**Hostile output characteristics:**

| Characteristic | Description | Example |
|----------------|-------------|---------|
| `schema_violation` | Output violates the expected schema. | Missing required fields, invalid types. |
| `length_exceeded` | Output exceeds length limits. | Response longer than token limit. |
| `content_filter_violation` | Output violates content filters. | Hate speech, PII, secrets. |
| `circular_reference` | Output contains circular references. | Self-referential data structures. |
| `injection_attempt` | Output contains injection attempts. | SQL injection, XSS, command injection. |
| `resource_exhaustion` | Output attempts to exhaust resources. | Extremely large data structures. |

**Validation behaviors:**

| Behavior | Description |
|----------|-------------|
| `rejected` | Output is rejected and not admitted. |
| `sanitized` | Output is sanitized (e.g., truncated, filtered) and admitted. |
| `admitted` | Output is admitted as-is. |

**Hostile output handling:**

1. **Detection**: The host detects hostile output characteristics.
2. **Classification**: The host classifies the hostile output (schema violation, length exceeded, etc.).
3. **Action**: The host takes action based on the classification:
   - Reject the output.
   - Sanitize the output.
   - Admit the output (if safe).
4. **Logging**: The host logs the hostile output detection and action for audit.

**Hostile output evidence:**

| Evidence type | Description |
|---------------|-------------|
| `hostile_output.detected` | Emitted when hostile output is detected. |
| `hostile_output.rejected` | Emitted when hostile output is rejected. |
| `hostile_output.sanitized` | Emitted when hostile output is sanitized. |
| `hostile_output.admitted` | Emitted when hostile output is admitted. |

### Subtask 5.2.1.2 - Loop termination and deterministic resume

Verified loops terminate under budgets and resume deterministically from
durable strategy snapshots and result signals.

**Loop termination:**

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

**Deterministic resume:**

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

**Loop termination behaviors:**

| Behavior | Description |
|----------|-------------|
| `terminated_normal` | The workflow terminated normally (completed or failed). |
| `terminated_budget` | The workflow terminated due to budget exhaustion. |
| `terminated_cancelled` | The workflow was cancelled. |
| `terminated_error` | The workflow terminated due to an error. |

**Deterministic resume behaviors:**

| Behavior | Description |
|----------|-------------|
| `resume_success` | The workflow resumed successfully from the snapshot. |
| `resume_failed` | The workflow failed to resume from the snapshot. |
| `resume_not_needed` | The workflow did not need to resume (completed or failed). |

### Subtask 5.2.1.3 - Milestone 7 workflow corpus

Published the Milestone 7 workflow corpus, provenance coverage, safety
boundaries, cost evidence, and residual model-quality limitations.

**Milestone 7 workflow corpus:**

| Workflow type | Description | Coverage |
|---------------|-------------|----------|
| `direct-model-response` | Agent receives a direct response from the model. | 100% |
| `structured-response` | Agent receives a structured response with validated fields. | 100% |
| `model-to-tool-continuation` | Agent continues after model response with tool execution. | 100% |
| `retrieval-grounded-answer` | Agent answers using retrieved context. | 100% |
| `code-execution` | Agent executes code and uses the result. | 100% |
| `multi-agent-delegation` | Agent delegates work to child agents. | 100% |

**Provenance coverage:**

| Reference type | Description | Coverage |
|----------------|-------------|----------|
| `model` | Reference to a model response. | 100% |
| `tool` | Reference to a tool output. | 100% |
| `retrieval` | Reference to retrieved context. | 100% |
| `state-revision` | Reference to a state revision. | 100% |
| `directive` | Reference to a directive. | 100% |
| `attempt` | Reference to an effect handler attempt. | 100% |
| `policy` | Reference to a policy decision. | 100% |

**Safety boundaries:**

| Boundary | Description | Enforcement |
|----------|-------------|-------------|
| `quotas` | Enforce tenant/agent/model/tool quotas. | Host enforces at reservation, consumption, release, reconciliation. |
| `approvals` | Require approval for sensitive operations. | Host enforces approval workflow with eligible approvers, decision options, expiry, escalation. |
| `secrets` | Protect secrets with non-exportability and audit logging. | Host enforces secret lease lifecycle with creation, access, renewal, expiry, revocation, deletion. |
| `hostile output` | Validate and filter hostile output. | Host enforces validation at state, model context, downstream tool, and user-facing admission points. |
| `budgets` | Enforce workflow budgets (iterations, tools, time, cost, tokens). | Host enforces at workflow execution with deterministic resume from snapshots. |

**Cost evidence:**

| Cost metric | Description | Measurement |
|-------------|-------------|-------------|
| `model_cost` | Cost of model invocations. | Tracked per workflow, per tenant, per agent. |
| `tool_cost` | Cost of tool invocations. | Tracked per workflow, per tenant, per agent. |
| `storage_cost` | Cost of storage (snapshots, journals, etc.). | Tracked per tenant, per agent. |
| `total_cost` | Total cost of all resources. | Sum of model, tool, and storage costs. |

**Residual model-quality limitations:**

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

## Key design decisions

1. **Hostile output validation**: Validation at four points (state, model context, downstream tool, user-facing) ensures safety at every admission boundary.

2. **Budget enforcement**: Five budget constraints (iterations, tools, time, cost, tokens) prevent resource exhaustion.

3. **Deterministic resume**: Snapshots and result signals enable workflows to resume deterministically after failure or interruption.

4. **Workflow corpus coverage**: All six workflow types are fully covered by the spec and tests.

5. **Provenance coverage**: All seven reference types are fully covered, enabling audit and debugging.

6. **Safety boundaries**: Five safety boundaries (quotas, approvals, secrets, hostile output, budgets) enforce host policy.

7. **Cost evidence**: Cost metrics are tracked per workflow, per tenant, and per agent for observability.

8. **Residual limitations**: Known model-quality limitations are documented with mitigations.

9. **Bounded evidence**: All evidence is bounded and does not expose secrets.

10. **Tenant isolation**: All resources are scoped to tenant boundaries.

## Open questions

1. Should workflow budgets be configurable per tenant, per agent, or per workflow?

2. Should hostile output validation support custom validation rules?

3. Should deterministic resume support partial results (return what was completed before failure)?

4. Should the workflow corpus include benchmark workflows (e.g., standard test cases)?

5. Should provenance coverage be quantified (e.g., "95% of answers have full provenance")?

6. Should safety boundaries be configurable per workflow type?

7. Should cost evidence include projections (e.g., estimated cost for upcoming workflows)?

8. Should residual model-quality limitations include quantitative metrics (e.g., "hallucination rate < 5%")?

9. Should workflows support checkpointing to external storage (e.g., S3)?

10. Should hostile output detection use ML-based approaches (e.g., toxicity classifiers)?

11. Should budget exhaustion support grace periods (allow in-progress operations to complete)?

12. Should provenance references support automatic cleanup (e.g., when the answer is deleted)?

## Cross-references

### Earlier chapters

- [41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md](../41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- [42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md](../42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)

### Related chapters (Phase 5)

- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md)
