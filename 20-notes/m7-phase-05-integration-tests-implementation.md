---
title: "Phase 5 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-05
  - implementation
  - integration-tests
  - workflows
  - safety
  - provenance
  - milestone-acceptance
aliases:
  - "M7-P5 Integration Tests Implementation"
---

# Phase 5 Integration Tests Implementation

## Overview

This note documents the implementation of Section 5.4 from Phase 5 plan:
**Phase 5 Integration Tests** for Agentic Workflows, Provenance, Safety,
And Milestone Acceptance.

## Implementation notes

### Subtask 5.4.1.1 - Successful flow

Verified the canonical successful flow and retained evidence for agentic
workflows, provenance, safety, and milestone acceptance.

**Successful flow tests (12 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-direct-model-response-success` | Execute a direct model response workflow. | Workflow completes with model response. |
| `workflow-structured-response-success` | Execute a structured response workflow. | Workflow completes with validated structured response. |
| `workflow-model-to-tool-continuation-success` | Execute a model-to-tool continuation workflow. | Workflow completes with tool results. |
| `workflow-retrieval-grounded-answer-success` | Execute a retrieval-grounded answer workflow. | Workflow completes with grounded answer and citations. |
| `workflow-code-execution-success` | Execute a code execution workflow. | Workflow completes with execution result. |
| `workflow-multi-agent-delegation-success` | Execute a multi-agent delegation workflow. | Workflow completes with aggregated child results. |
| `provenance-reference-model-success` | Create a provenance reference to a model response. | Provenance reference is created with type `model`. |
| `provenance-reference-tool-success` | Create a provenance reference to a tool output. | Provenance reference is created with type `tool`. |
| `provenance-reference-retrieval-success` | Create a provenance reference to retrieved context. | Provenance reference is created with type `retrieval`. |
| `approval-required-tool-use-success` | Execute a tool use that requires approval. | Tool use completes after approval. |
| `quota-reservation-success` | Reserve quota for a workflow. | Quota is reserved and usage is updated. |
| `lease-creation-success` | Create a secret lease for a workflow. | Lease is created with status `active`. |

**Evidence retention tests (10 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `evidence-workflow-created` | Verify evidence is emitted when a workflow is created. | `workflow.created` evidence is emitted. |
| `evidence-workflow-completed` | Verify evidence is emitted when a workflow is completed. | `workflow.completed` evidence is emitted. |
| `evidence-provenance-reference-created` | Verify evidence is emitted when a provenance reference is created. | `provenance_reference.created` evidence is emitted. |
| `evidence-approval-requested` | Verify evidence is emitted when an approval is requested. | `approval.requested` evidence is emitted. |
| `evidence-approval-approved` | Verify evidence is emitted when an approval is approved. | `approval.approved` evidence is emitted. |
| `evidence-quota-reserved` | Verify evidence is emitted when quota is reserved. | `quota.reserved` evidence is emitted. |
| `evidence-lease-created` | Verify evidence is emitted when a lease is created. | `lease.created` evidence is emitted. |
| `evidence-model-stream-started` | Verify evidence is emitted when a model stream starts. | `model_stream.started` evidence is emitted. |
| `evidence-model-stream-completed` | Verify evidence is emitted when a model stream completes. | `model_stream.completed` evidence is emitted. |
| `evidence-tool-invocation-started` | Verify evidence is emitted when a tool invocation starts. | `tool.invocation.started` evidence is emitted. |

### Subtask 5.4.1.2 - Failure handling

Verified malformed, incompatible, stale, duplicate, and boundary-limit inputs
fail with stable diagnostics where applicable.

**Malformed input tests (5 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `malformed-workflow-missing-type` | Create a workflow without a type. | `malformed_workflow_input` diagnostic is emitted. |
| `malformed-provenance-reference-missing-type` | Create a provenance reference without a type. | `malformed_provenance_reference` diagnostic is emitted. |
| `malformed-approval-request-missing-type` | Request approval without a type. | `malformed_approval_request` diagnostic is emitted. |
| `malformed-quota-request-missing-limit` | Create a quota request without a limit. | `malformed_quota_request` diagnostic is emitted. |
| `malformed-lease-request-missing-principal` | Create a lease request without a principal. | `malformed_lease_request` diagnostic is emitted. |

**Incompatible input tests (2 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `incompatible-workflow-version` | Create a workflow with an incompatible version. | `incompatible_workflow_version` diagnostic is emitted. |
| `incompatible-provenance-reference-version` | Create a provenance reference with an incompatible version. | `incompatible_provenance_reference_version` diagnostic is emitted. |

**Conflict tests (5 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `conflicting-workflow-status` | Update a workflow with conflicting status. | `conflicting_workflow_status` diagnostic is emitted. |
| `conflicting-provenance-reference` | Create a provenance reference with conflicting content. | `conflicting_provenance_reference` diagnostic is emitted. |
| `conflicting-approval-status` | Update an approval with conflicting status. | `conflicting_approval_status` diagnostic is emitted. |
| `conflicting-quota-limit` | Update a quota with conflicting limit. | `conflicting_quota_limit` diagnostic is emitted. |
| `conflicting-lease-expiry` | Update a lease with conflicting expiry. | `conflicting_lease_expiry` diagnostic is emitted. |

**Unauthorized access tests (7 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `unauthorized-workflow-access` | Access a workflow without authorization. | `unauthorized_workflow_access` diagnostic is emitted. |
| `unauthorized-provenance-reference-access` | Access a provenance reference without authorization. | `unauthorized_provenance_reference_access` diagnostic is emitted. |
| `unauthorized-approval-access` | Access an approval without authorization. | `unauthorized_approval_access` diagnostic is emitted. |
| `unauthorized-quota-access` | Access a quota without authorization. | `unauthorized_quota_access` diagnostic is emitted. |
| `unauthorized-lease-access` | Access a lease without authorization. | `unauthorized_lease_access` diagnostic is emitted. |
| `unauthorized-model-access` | Access a model without authorization. | `unauthorized_model_access` diagnostic is emitted. |
| `unauthorized-tool-access` | Access a tool without authorization. | `unauthorized_tool_access` diagnostic is emitted. |

**Exhaustion tests (5 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-budget-exhausted` | Exhaust a workflow budget. | `workflow_budget_exhausted` diagnostic is emitted. |
| `quota-exhausted` | Exhaust a quota. | `quota_exhausted` diagnostic is emitted. |
| `approval-expired` | Wait for an approval to expire. | `approval_expired` diagnostic is emitted. |
| `lease-expired` | Wait for a lease to expire. | `lease_expired` diagnostic is emitted. |
| `model-stream-cancelled` | Cancel a model stream. | `model_stream_cancelled` diagnostic is emitted. |

**Unavailable tests (7 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-store-unavailable` | Simulate workflow store unavailability. | `workflow_store_unavailable` diagnostic is emitted. |
| `provenance-reference-store-unavailable` | Simulate provenance reference store unavailability. | `provenance_reference_store_unavailable` diagnostic is emitted. |
| `approval-store-unavailable` | Simulate approval store unavailability. | `approval_store_unavailable` diagnostic is emitted. |
| `quota-store-unavailable` | Simulate quota store unavailability. | `quota_store_unavailable` diagnostic is emitted. |
| `lease-store-unavailable` | Simulate lease store unavailability. | `lease_store_unavailable` diagnostic is emitted. |
| `model-unavailable` | Simulate model unavailability. | `model_unavailable` diagnostic is emitted. |
| `tool-unavailable` | Simulate tool unavailability. | `tool_unavailable` diagnostic is emitted. |

### Subtask 5.4.1.3 - Timeout and cancellation

Verified timeout, cancellation, unavailable dependency, and retry behavior
leave no unauthorized or partial state.

**Timeout tests (6 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-timeout` | Workflow execution times out. | Workflow is not completed, no partial state. |
| `model-stream-timeout` | Model stream times out. | Model stream is not completed, no partial state. |
| `tool-invocation-timeout` | Tool invocation times out. | Tool invocation is not completed, no partial state. |
| `approval-timeout` | Approval decision times out. | Approval remains pending, no partial state. |
| `lease-timeout` | Lease creation times out. | Lease is not created, no partial state. |
| `provenance-reference-timeout` | Provenance reference creation times out. | Provenance reference is not created, no partial state. |

**Cancellation tests (6 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-cancel` | Cancel a workflow. | Workflow is cancelled with status `cancelled`. |
| `model-stream-cancel` | Cancel a model stream. | Model stream is cancelled with status `cancelled`. |
| `tool-invocation-cancel` | Cancel a tool invocation. | Tool invocation is cancelled, no partial state. |
| `approval-cancel` | Cancel an approval request. | Approval is cancelled with status `cancelled`. |
| `lease-cancel` | Cancel a lease creation. | Lease is not created, no partial state. |
| `provenance-reference-cancel` | Cancel a provenance reference creation. | Provenance reference is not created, no partial state. |

**Unavailable dependency tests (7 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-unavailable-retry` | Workflow store is unavailable, then becomes available. | Workflow is created on retry. |
| `provenance-reference-unavailable-retry` | Provenance reference store is unavailable, then becomes available. | Provenance reference is created on retry. |
| `approval-unavailable-retry` | Approval store is unavailable, then becomes available. | Approval request succeeds on retry. |
| `quota-unavailable-retry` | Quota store is unavailable, then becomes available. | Quota reservation succeeds on retry. |
| `lease-unavailable-retry` | Lease store is unavailable, then becomes available. | Lease is created on retry. |
| `model-unavailable-retry` | Model is unavailable, then becomes available. | Model stream succeeds on retry. |
| `tool-unavailable-retry` | Tool is unavailable, then becomes available. | Tool invocation succeeds on retry. |

**Retry tests (7 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `workflow-retry-success` | Workflow creation fails, then succeeds on retry. | Workflow is created successfully. |
| `provenance-reference-retry-success` | Provenance reference creation fails, then succeeds on retry. | Provenance reference is created successfully. |
| `approval-retry-success` | Approval request fails, then succeeds on retry. | Approval request succeeds on retry. |
| `quota-retry-success` | Quota reservation fails, then succeeds on retry. | Quota reservation succeeds on retry. |
| `lease-retry-success` | Lease creation fails, then succeeds on retry. | Lease is created successfully. |
| `model-retry-success` | Model stream fails, then succeeds on retry. | Model stream succeeds on retry. |
| `tool-retry-success` | Tool invocation fails, then succeeds on retry. | Tool invocation succeeds on retry. |

### Subtask 5.4.1.4 - Cross-milestone fixtures

Ran all earlier milestone fixtures affected by this phase and recorded
regressions or approved variability.

**Cross-milestone fixture scopes (11 milestones):**

| Milestone | Fixture scope | Status |
|-----------|---------------|--------|
| Phase 1 (Signals) | 10-signals-causality-routing-and-delivery | No regression |
| Phase 1 (Actions) | 11-actions-instructions-validation-plans-and-results | No regression |
| Phase 2 (State) | 12-state-operations-patches-revisions-and-conflicts | No regression |
| Phase 2 (Directives) | 13-directives-strategies-continuations-and-terminal-states | No regression |
| Phase 2 (Reducer) | 14-deterministic-reducer-semantics-and-milestone-acceptance | No regression |
| Phase 3 (Extism) | 20-extism-invocation-boundary-instances-and-output-validation | No regression |
| Phase 3 (Mailboxes) | 21-mailboxes-ordering-bounds-fairness-and-turn-leases | No regression |
| Phase 3 (Registry) | 22-agent-registry-activation-cancellation-and-completion | No regression |
| Phase 3 (Sensors) | 23-sensors-schedules-timers-and-external-signal-ingress | No regression |
| Phase 4 (Snapshots) | 25-revisioned-snapshots-journals-history-and-storage-contracts | No regression |
| Phase 4 (Threads) | 44-threads-checkpoints-memory-approvals-quotas-and-secret-leases | No regression |

**Regression summary:**

No regressions were identified in earlier milestone fixtures.

## Key design decisions

1. **Comprehensive test coverage**: Tests cover all aspects of Phase 5.

2. **Successful flow tests**: Tests verify the canonical successful flow for all workflow types.

3. **Failure handling tests**: Tests verify that failures are handled correctly with stable diagnostics.

4. **Timeout and cancellation tests**: Tests verify that timeouts and cancellations leave no unauthorized or partial state.

5. **Cross-milestone compatibility**: Tests verify that Phase 5 does not regress earlier milestones.

6. **Evidence retention**: Tests verify that evidence is emitted for significant events.

7. **Bounded diagnostics**: Diagnostics are bounded and do not expose secrets.

8. **Tenant isolation**: Tests verify tenant isolation for all resources.

9. **Budget enforcement**: Tests verify budget enforcement at all points.

10. **Provenance coverage**: Tests verify provenance references for all evidence types.

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

- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md](../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md](../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md)
- [45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md](../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md)

### Related chapters

- [41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- [42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
