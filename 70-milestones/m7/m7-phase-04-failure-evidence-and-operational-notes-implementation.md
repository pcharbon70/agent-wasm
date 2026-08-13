---
title: "Phase 4 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-04
  - implementation
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
aliases:
  - "M7-P4 Failure Evidence And Operational Notes Implementation"
---

# Phase 4 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 4.3 from Phase 4 plan:
**Failure Evidence And Operational Notes** for Threads, Checkpoints, Memory,
Approvals, Quotas, And Secret Leases.

## Implementation notes

### Subtask 4.3.1.1 - Failure outcomes

Defined malformed, incompatible, conflicting, unauthorized, exhausted, and
unavailable outcomes relevant to threads, checkpoints, memory, approvals,
quotas, and secret leases.

**Malformed outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_thread_input` | The thread input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_thread_input` diagnostic. |
| `malformed_message_input` | The message input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_message_input` diagnostic. |
| `malformed_checkpoint_input` | The checkpoint input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_checkpoint_input` diagnostic. |
| `malformed_memory_input` | The memory input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_memory_input` diagnostic. |
| `malformed_approval_input` | The approval input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_approval_input` diagnostic. |
| `malformed_quota_input` | The quota input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_quota_input` diagnostic. |
| `malformed_lease_input` | The lease input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_lease_input` diagnostic. |

**Incompatible outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_thread_version` | The thread version is incompatible with the host version. | Reject the input and emit an `incompatible_thread_version` diagnostic. |
| `incompatible_checkpoint_version` | The checkpoint version is incompatible with the host version. | Reject the input and emit an `incompatible_checkpoint_version` diagnostic. |
| `incompatible_memory_version` | The memory version is incompatible with the host version. | Reject the input and emit an `incompatible_memory_version` diagnostic. |

**Conflicting outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_thread_visibility` | The thread visibility is conflicting with the current visibility. | Reject the input and emit a `conflicting_thread_visibility` diagnostic. |
| `conflicting_quota_limit` | The quota limit is conflicting with the current limit. | Reject the input and emit a `conflicting_quota_limit` diagnostic. |
| `conflicting_lease_expiry` | The lease expiry is conflicting with the current expiry. | Reject the input and emit a `conflicting_lease_expiry` diagnostic. |

**Unauthorized outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_thread_access` | The agent is not authorized to access the thread. | Reject the request and emit an `unauthorized_thread_access` diagnostic. |
| `unauthorized_checkpoint_access` | The agent is not authorized to access the checkpoint. | Reject the request and emit an `unauthorized_checkpoint_access` diagnostic. |
| `unauthorized_memory_access` | The agent is not authorized to access the memory. | Reject the request and emit an `unauthorized_memory_access` diagnostic. |
| `unauthorized_approval_access` | The agent is not authorized to access the approval. | Reject the request and emit an `unauthorized_approval_access` diagnostic. |
| `unauthorized_quota_access` | The agent is not authorized to access the quota. | Reject the request and emit an `unauthorized_quota_access` diagnostic. |
| `unauthorized_lease_access` | The agent is not authorized to access the lease. | Reject the request and emit an `unauthorized_lease_access` diagnostic. |

**Exhausted outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `quota_exhausted` | The quota is exhausted. | Reject the request and emit a `quota_exhausted` diagnostic. |
| `approval_expired` | The approval request has expired. | Reject the request and emit an `approval_expired` diagnostic. |
| `lease_expired` | The secret lease has expired. | Reject the request and emit a `lease_expired` diagnostic. |

**Unavailable outcomes:**

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `thread_store_unavailable` | The thread store is unavailable. | Retry the request or reject and emit a `thread_store_unavailable` diagnostic. |
| `checkpoint_store_unavailable` | The checkpoint store is unavailable. | Retry the request or reject and emit a `checkpoint_store_unavailable` diagnostic. |
| `memory_store_unavailable` | The memory store is unavailable. | Retry the request or reject and emit a `memory_store_unavailable` diagnostic. |
| `approval_store_unavailable` | The approval store is unavailable. | Retry the request or reject and emit an `approval_store_unavailable` diagnostic. |
| `quota_store_unavailable` | The quota store is unavailable. | Retry the request or reject and emit a `quota_store_unavailable` diagnostic. |
| `lease_store_unavailable` | The lease store is unavailable. | Retry the request or reject and emit a `lease_store_unavailable` diagnostic. |

### Subtask 4.3.1.2 - Bounded diagnostics and evidence emission

Defined bounded diagnostics and evidence emission that identify the phase
contract, profile, and failed boundary without exposing secrets.

**Bounded diagnostics schema:**

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic_id` | The `DiagnosticId` of the diagnostic. | Host runtime |
| `diagnostic_code` | The diagnostic code (e.g., `malformed_thread_input`, `quota_exhausted`). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-04`). | Host runtime |
| `section` | The section identifier (`4.1`, `4.2`, `4.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `thread.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `profile` | The profile identifier (if applicable). | Host runtime |
| `message` | A human-readable message describing the diagnostic. | Host runtime |
| `details` | Additional details about the diagnostic (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the diagnostic. | Host clock |

**Evidence emission schema:**

| Field | Content | Source |
|-------|---------|--------|
| `evidence_id` | The `EvidenceId` of the evidence. | Host runtime |
| `evidence_type` | The evidence type (`thread.created`, `thread.deleted`, `checkpoint.created`, `checkpoint.restored`, `memory.created`, `memory.promoted`, `memory.deleted`, `approval.requested`, `approval.decided`, `approval.expired`, `quota.reserved`, `quota.consumed`, `quota.released`, `quota.reconciled`, `lease.created`, `lease.accessed`, `lease.renewed`, `lease.revoked`). | Host runtime |
| `thread_id` | The `ThreadId` of the thread (if applicable). | Host runtime |
| `checkpoint_id` | The `CheckpointId` of the checkpoint (if applicable). | Host runtime |
| `memory_id` | The `MemoryId` of the memory (if applicable). | Host runtime |
| `approval_id` | The `ApprovalId` of the approval (if applicable). | Host runtime |
| `quota_id` | The `QuotaId` of the quota (if applicable). | Host runtime |
| `lease_id` | The `LeaseId` of the lease (if applicable). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-04`). | Host runtime |
| `section` | The section identifier (`4.1`, `4.2`, `4.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `thread.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `details` | Additional details about the evidence (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the evidence. | Host clock |

**Evidence types:**

| Evidence type | Description |
|---------------|-------------|
| `thread.created` | Emitted when a thread is created. |
| `thread.deleted` | Emitted when a thread is deleted. |
| `checkpoint.created` | Emitted when a checkpoint is created. |
| `checkpoint.restored` | Emitted when a checkpoint is restored. |
| `memory.created` | Emitted when memory is created. |
| `memory.promoted` | Emitted when memory is promoted. |
| `memory.deleted` | Emitted when memory is deleted. |
| `approval.requested` | Emitted when an approval is requested. |
| `approval.decided` | Emitted when an approval is decided. |
| `approval.expired` | Emitted when an approval expires. |
| `quota.reserved` | Emitted when quota is reserved. |
| `quota.consumed` | Emitted when quota is consumed. |
| `quota.released` | Emitted when quota is released. |
| `quota.reconciled` | Emitted when quota is reconciled. |
| `lease.created` | Emitted when a secret lease is created. |
| `lease.accessed` | Emitted when a secret lease is accessed. |
| `lease.renewed` | Emitted when a secret lease is renewed. |
| `lease.revoked` | Emitted when a secret lease is revoked. |

### Subtask 4.3.1.3 - Implementation-defined choices

Documented implementation-defined choices, deferred work, and any result that
would invalidate an earlier milestone assumption.

**Implementation-defined choices:**

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Thread visibility default | `private` | MUST be documented in host configuration. |
| Memory confidence defaults | As stated in Section 44.1 | MUST be documented in host configuration. |
| Checkpoint schema migration | Forward migration only | MUST be documented in host configuration. |
| Approval routing strategy | `any` | MUST be documented in host configuration. |
| Quota reconciliation interval | 1 hour | MUST be documented in host configuration. |
| Secret lease non-exportability | `true` | MUST be documented in host configuration. |
| Approval expiry default | 24 hours | MUST be documented in host configuration. |
| Memory retention default | `permanent` | MUST be documented in host configuration. |

**Deferred work:**

| Item | Description | Priority |
|------|-------------|----------|
| Parallel approvals | Support parallel approvals (e.g., require N out of M approvers). | Medium |
| Quota burst allowance | Support burst allowances (temporary overages). | Low |
| Secret lease rotation | Support secret rotation without invalidating leases. | Medium |
| Memory predictive promotion | Support predictive promotion based on usage patterns. | Low |
| Approval conditional decisions | Support conditional decisions (e.g., "approve if X"). | Medium |
| Quota predictive scaling | Support predictive scaling based on usage patterns. | Low |
| Secret lease auto-renewal | Support automatic renewal of secret leases. | Low |
| Approval auto-approval | Support auto-approval for low-risk requests. | Medium |
| Memory hierarchical scoping | Support hierarchical scoping for memory references. | Low |
| Quota shared pools | Support shared quota pools for multiple agents. | Medium |

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

1. Should approval requests support parallel approvals (e.g., require N out of M approvers)?

2. Should quotas support burst allowances (temporary overages)?

3. Should secret leases support hierarchical scoping?

4. Should approval requests support conditional decisions (e.g., "approve if X")?

5. Should quotas support predictive scaling (e.g., increase limit based on usage patterns)?

6. Should secret leases support automatic renewal?

7. Should approval requests support time-boxed decisions (e.g., "approve for 1 hour")?

8. Should quotas support shared pools (e.g., multiple agents sharing a quota)?

9. Should secret leases support secret rotation?

10. Should approval requests support auto-approval for low-risk requests?

11. Should quotas support per-request cost tracking (e.g., track cost per tool execution)?

12. Should secret leases support secret versioning (e.g., rotate secrets without invalidating leases)?

## Cross-references

### Earlier chapters

- [10-signals-causality-routing-and-delivery.md](../../60-specification/10-signals-causality-routing-and-delivery.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [29-crash-injection-durable-effects-and-milestone-acceptance.md](../../60-specification/29-crash-injection-durable-effects-and-milestone-acceptance.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

### Related chapters (Phase 4)

- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md)
