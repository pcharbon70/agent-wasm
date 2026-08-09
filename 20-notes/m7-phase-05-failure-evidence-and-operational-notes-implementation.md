---
title: "Phase 5 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-05
  - implementation
  - failure-evidence
  - diagnostics
  - workflows
  - safety
  - provenance
  - milestone-acceptance
aliases:
  - "M7-P5 Failure Evidence And Operational Notes Implementation"
---

# Phase 5 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 5.3 from Phase 5 plan:
**Failure Evidence And Operational Notes** for Agentic Workflows, Provenance,
Safety, And Milestone Acceptance.

## Implementation notes

### Subtask 5.3.1.1 - Failure outcomes

Defined malformed, incompatible, conflicting, unauthorized, exhausted, and
unavailable outcomes relevant to agentic workflows, provenance, safety, and
milestone acceptance.

**Malformed outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_workflow_input` | The workflow input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_workflow_input` diagnostic. |
| `malformed_provenance_reference` | The provenance reference is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_provenance_reference` diagnostic. |
| `malformed_approval_request` | The approval request is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_approval_request` diagnostic. |
| `malformed_quota_request` | The quota request is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_quota_request` diagnostic. |
| `malformed_lease_request` | The lease request is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_lease_request` diagnostic. |

**Incompatible outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_workflow_version` | The workflow version is incompatible with the host version. | Reject the input and emit an `incompatible_workflow_version` diagnostic. |
| `incompatible_provenance_reference_version` | The provenance reference version is incompatible with the host version. | Reject the input and emit an `incompatible_provenance_reference_version` diagnostic. |

**Conflicting outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_workflow_status` | The workflow status is conflicting with the current status. | Reject the input and emit a `conflicting_workflow_status` diagnostic. |
| `conflicting_provenance_reference` | The provenance reference is conflicting with existing references. | Reject the input and emit a `conflicting_provenance_reference` diagnostic. |
| `conflicting_approval_status` | The approval status is conflicting with the current status. | Reject the input and emit a `conflicting_approval_status` diagnostic. |
| `conflicting_quota_limit` | The quota limit is conflicting with the current limit. | Reject the input and emit a `conflicting_quota_limit` diagnostic. |
| `conflicting_lease_expiry` | The lease expiry is conflicting with the current expiry. | Reject the input and emit a `conflicting_lease_expiry` diagnostic. |

**Unauthorized outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_workflow_access` | The agent is not authorized to access the workflow. | Reject the request and emit an `unauthorized_workflow_access` diagnostic. |
| `unauthorized_provenance_reference_access` | The agent is not authorized to access the provenance reference. | Reject the request and emit an `unauthorized_provenance_reference_access` diagnostic. |
| `unauthorized_approval_access` | The agent is not authorized to access the approval. | Reject the request and emit an `unauthorized_approval_access` diagnostic. |
| `unauthorized_quota_access` | The agent is not authorized to access the quota. | Reject the request and emit an `unauthorized_quota_access` diagnostic. |
| `unauthorized_lease_access` | The agent is not authorized to access the lease. | Reject the request and emit an `unauthorized_lease_access` diagnostic. |
| `unauthorized_model_access` | The agent is not authorized to access the model. | Reject the request and emit an `unauthorized_model_access` diagnostic. |
| `unauthorized_tool_access` | The agent is not authorized to access the tool. | Reject the request and emit an `unauthorized_tool_access` diagnostic. |

**Exhausted outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `workflow_budget_exhausted` | The workflow budget is exhausted. | Terminate the workflow and emit a `workflow_budget_exhausted` diagnostic. |
| `quota_exhausted` | The quota is exhausted. | Reject the request and emit a `quota_exhausted` diagnostic. |
| `approval_expired` | The approval request has expired. | Reject the request and emit an `approval_expired` diagnostic. |
| `lease_expired` | The secret lease has expired. | Reject the request and emit a `lease_expired` diagnostic. |
| `model_stream_cancelled` | The model stream has been cancelled. | Terminate the model stream and emit a `model_stream_cancelled` diagnostic. |

**Unavailable outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `workflow_store_unavailable` | The workflow store is unavailable. | Retry the request or reject and emit a `workflow_store_unavailable` diagnostic. |
| `provenance_reference_store_unavailable` | The provenance reference store is unavailable. | Retry the request or reject and emit a `provenance_reference_store_unavailable` diagnostic. |
| `approval_store_unavailable` | The approval store is unavailable. | Retry the request or reject and emit an `approval_store_unavailable` diagnostic. |
| `quota_store_unavailable` | The quota store is unavailable. | Retry the request or reject and emit a `quota_store_unavailable` diagnostic. |
| `lease_store_unavailable` | The lease store is unavailable. | Retry the request or reject and emit a `lease_store_unavailable` diagnostic. |
| `model_unavailable` | The model is unavailable. | Retry the request or reject and emit a `model_unavailable` diagnostic. |
| `tool_unavailable` | The tool is unavailable. | Retry the request or reject and emit a `tool_unavailable` diagnostic. |

### Subtask 5.3.1.2 - Bounded diagnostics and evidence emission

Defined bounded diagnostics and evidence emission that identify the phase
contract, profile, and failed boundary without exposing secrets.

**Bounded diagnostics schema:**

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic_id` | The `DiagnosticId` of the diagnostic. | Host runtime |
| `diagnostic_code` | The diagnostic code (e.g., `malformed_workflow_input`, `workflow_budget_exhausted`). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-05`). | Host runtime |
| `section` | The section identifier (`5.1`, `5.2`, `5.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `workflow.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `profile` | The profile identifier (if applicable). | Host runtime |
| `message` | A human-readable message describing the diagnostic. | Host runtime |
| `details` | Additional details about the diagnostic (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the diagnostic. | Host clock |

**Evidence emission schema:**

| Field | Content | Source |
|-------|---------|--------|
| `evidence_id` | The `EvidenceId` of the evidence. | Host runtime |
| `evidence_type` | The evidence type (e.g., `workflow.created`, `workflow.budget_exhausted`, `hostile_output.detected`). | Host runtime |
| `workflow_id` | The `WorkflowId` of the workflow (if applicable). | Host runtime |
| `provenance_reference_id` | The `ReferenceId` of the provenance reference (if applicable). | Host runtime |
| `approval_id` | The `ApprovalId` of the approval (if applicable). | Host runtime |
| `quota_id` | The `QuotaId` of the quota (if applicable). | Host runtime |
| `lease_id` | The `LeaseId` of the lease (if applicable). | Host runtime |
| `model_id` | The `ModelId` of the model (if applicable). | Host runtime |
| `tool_id` | The `ToolId` of the tool (if applicable). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-05`). | Host runtime |
| `section` | The section identifier (`5.1`, `5.2`, `5.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `workflow.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `details` | Additional details about the evidence (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the evidence. | Host clock |

**Evidence types:**

| Evidence type | Description |
|---------------|-------------|
| `workflow.created` | Emitted when a workflow is created. |
| `workflow.completed` | Emitted when a workflow is completed. |
| `workflow.failed` | Emitted when a workflow fails. |
| `workflow.cancelled` | Emitted when a workflow is cancelled. |
| `workflow.budget_exhausted` | Emitted when a workflow budget is exhausted. |
| `provenance_reference.created` | Emitted when a provenance reference is created. |
| `hostile_output.detected` | Emitted when hostile output is detected. |
| `hostile_output.rejected` | Emitted when hostile output is rejected. |
| `hostile_output.sanitized` | Emitted when hostile output is sanitized. |
| `hostile_output.admitted` | Emitted when hostile output is admitted. |
| `approval.requested` | Emitted when an approval is requested. |
| `approval.approved` | Emitted when an approval is approved. |
| `approval.rejected` | Emitted when an approval is rejected. |
| `approval.expired` | Emitted when an approval expires. |
| `quota.reserved` | Emitted when quota is reserved. |
| `quota.consumed` | Emitted when quota is consumed. |
| `quota.exhausted` | Emitted when quota is exhausted. |
| `lease.created` | Emitted when a secret lease is created. |
| `lease.revoked` | Emitted when a secret lease is revoked. |
| `lease.expired` | Emitted when a secret lease expires. |
| `model_stream.started` | Emitted when a model stream starts. |
| `model_stream.completed` | Emitted when a model stream completes. |
| `model_stream.cancelled` | Emitted when a model stream is cancelled. |
| `model_stream.failed` | Emitted when a model stream fails. |
| `tool.invocation.started` | Emitted when a tool invocation starts. |
| `tool.invocation.completed` | Emitted when a tool invocation completes. |
| `tool.invocation.failed` | Emitted when a tool invocation fails. |

### Subtask 5.3.1.3 - Implementation-defined choices

Documented implementation-defined choices, deferred work, and any result that
would invalidate an earlier milestone assumption.

**Implementation-defined choices:**

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Workflow budget defaults | As stated in Section 45.2 | MUST be documented in host configuration. |
| Hostile output validation rules | Built-in rules only | MUST be documented in host configuration. |
| Deterministic resume behavior | Resume from last snapshot | MUST be documented in host configuration. |
| Provenance reference deduplication | Enabled | MUST be documented in host configuration. |
| Safety boundary configurability | Tenant-level | MUST be documented in host configuration. |
| Cost tracking granularity | Per workflow, per tenant, per agent | MUST be documented in host configuration. |
| Residual limitation reporting | Empirical data only | MUST be documented in host configuration. |

**Deferred work:**

| Item | Description | Priority |
|------|-------------|----------|
| Custom workflow types | Support custom workflow types beyond the six defined. | Medium |
| Custom validation rules | Support custom validation rules for hostile output. | Medium |
| Partial results on resume | Support partial results on deterministic resume. | Low |
| Quantified residual limitations | Quantify residual model-quality limitations (e.g., hallucination rate). | Low |
| ML-based hostile output detection | Use ML-based approaches for hostile output detection (e.g., toxicity classifiers). | Medium |
| External storage checkpointing | Support checkpointing to external storage (e.g., S3). | Low |
| Budget grace periods | Support budget grace periods (allow in-progress operations to complete). | Low |
| Provenance reference cleanup | Support automatic cleanup of provenance references when answers are deleted. | Low |
| Benchmark workflows | Include benchmark workflows (e.g., standard test cases) in the workflow corpus. | Medium |
| Quantified provenance coverage | Quantify provenance coverage (e.g., "95% of answers have full provenance"). | Low |

**Results that would invalidate earlier milestone assumptions:**

| Result | Description | Impact |
|--------|-------------|--------|
| None yet | No results have been identified that invalidate earlier milestone assumptions. | None |

## Key design decisions

1. **Bounded diagnostics**: Diagnostics are bounded and do not expose secrets.

2. **Evidence emission**: Every significant event emits bounded evidence for observability and debugging.

3. **Implementation-defined choices**: Implementation-defined choices are documented in host configuration.

4. **Deferred work**: Deferred work is tracked with priority and description.

5. **Milestone assumption validation**: Results that invalidate earlier milestone assumptions are tracked and documented.

6. **Diagnostic codes**: Diagnostic codes are standardized and consistent across phases.

7. **Evidence types**: Evidence types are standardized and consistent across phases.

8. **Contract identification**: Diagnostics and evidence identify the contract and section that failed.

9. **Boundary identification**: Diagnostics and evidence identify the failed boundary.

10. **Profile identification**: Diagnostics and evidence identify the profile (if applicable).

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

- [10-signals-causality-routing-and-delivery.md](../10-signals-causality-routing-and-delivery.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [29-crash-injection-durable-effects-and-milestone-acceptance.md](../29-crash-injection-durable-effects-and-milestone-acceptance.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../34-provenance-signing-audit-security-and-milestone-acceptance.md)

### Related chapters (Phase 5)

- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md](../45-agentic-workflows-provenance-safety-and-milestone-acceptance-phase-5-integration-tests.md)
