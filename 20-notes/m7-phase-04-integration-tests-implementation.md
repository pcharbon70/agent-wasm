---
title: "Phase 4 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-04
  - implementation
  - integration-tests
  - threads
  - checkpoints
  - memory
  - approvals
  - quotas
  - secret-leases
aliases:
  - "M7-P4 Integration Tests Implementation"
---

# Phase 4 Integration Tests Implementation

## Overview

This note documents the implementation of Section 4.4 from Phase 4 plan:
**Phase 4 Integration Tests** for Threads, Checkpoints, Memory, Approvals,
Quotas, And Secret Leases.

## Implementation notes

### Subtask 4.4.1.1 - Successful flow

Verified the canonical successful flow and retained evidence for threads,
checkpoints, memory, approvals, quotas, and secret leases.

**Successful flow tests (10 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-create-success` | Create a conversation thread with all required fields. | Thread is created with status `active`. |
| `thread-add-message-success` | Add a message to a thread. | Message is added, message count is incremented. |
| `thread-add-participant-success` | Add a participant to a thread. | Participant is added with the specified role. |
| `checkpoint-create-success` | Create a checkpoint from a snapshot. | Checkpoint is created with the current state. |
| `checkpoint-restore-success` | Restore state from a checkpoint. | State is restored to the checkpoint state. |
| `memory-create-working-success` | Create working memory. | Memory is created with type `working`. |
| `memory-create-episodic-success` | Create episodic memory. | Memory is created with type `episodic`. |
| `approval-request-success` | Request approval for an action. | Approval is requested with status `pending`. |
| `approval-decide-success` | Decide an approval request. | Approval is decided with the specified decision. |
| `quota-reserve-success` | Reserve quota. | Quota is reserved and usage is updated. |
| `lease-create-success` | Create a secret lease. | Lease is created with status `active`. |

**Evidence retention tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `evidence-thread-created` | Verify evidence is emitted when a thread is created. | `thread.created` evidence is emitted. |
| `evidence-checkpoint-created` | Verify evidence is emitted when a checkpoint is created. | `checkpoint.created` evidence is emitted. |
| `evidence-quota-reserved` | Verify evidence is emitted when quota is reserved. | `quota.reserved` evidence is emitted. |

### Subtask 4.4.1.2 - Failure handling

Verified malformed, incompatible, stale, duplicate, and boundary-limit inputs
fail with stable diagnostics where applicable.

**Malformed input tests (7 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `malformed-thread-missing-id` | Create a thread without a thread ID. | `malformed_thread_input` diagnostic is emitted. |
| `malformed-message-missing-content` | Create a message without content. | `malformed_message_input` diagnostic is emitted. |
| `malformed-checkpoint-missing-revision` | Create a checkpoint without a source revision. | `malformed_checkpoint_input` diagnostic is emitted. |
| `malformed-memory-missing-type` | Create memory without a type. | `malformed_memory_input` diagnostic is emitted. |
| `malformed-approval-missing-type` | Request approval without a type. | `malformed_approval_input` diagnostic is emitted. |
| `malformed-quota-missing-limit` | Create a quota without a limit. | `malformed_quota_input` diagnostic is emitted. |
| `malformed-lease-missing-principal` | Create a lease without a principal. | `malformed_lease_input` diagnostic is emitted. |

**Incompatible input tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `incompatible-thread-version` | Create a thread with an incompatible version. | `incompatible_thread_version` diagnostic is emitted. |
| `incompatible-checkpoint-version` | Create a checkpoint with an incompatible version. | `incompatible_checkpoint_version` diagnostic is emitted. |
| `incompatible-memory-version` | Create memory with an incompatible version. | `incompatible_memory_version` diagnostic is emitted. |

**Conflict tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `conflicting-thread-visibility` | Update a thread with conflicting visibility. | `conflicting_thread_visibility` diagnostic is emitted. |
| `conflicting-quota-limit` | Update a quota with conflicting limit. | `conflicting_quota_limit` diagnostic is emitted. |
| `conflicting-lease-expiry` | Update a lease with conflicting expiry. | `conflicting_lease_expiry` diagnostic is emitted. |

**Unauthorized access tests (6 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `unauthorized-thread-access` | Access a thread without authorization. | `unauthorized_thread_access` diagnostic is emitted. |
| `unauthorized-checkpoint-access` | Access a checkpoint without authorization. | `unauthorized_checkpoint_access` diagnostic is emitted. |
| `unauthorized-memory-access` | Access memory without authorization. | `unauthorized_memory_access` diagnostic is emitted. |
| `unauthorized-approval-access` | Access an approval without authorization. | `unauthorized_approval_access` diagnostic is emitted. |
| `unauthorized-quota-access` | Access a quota without authorization. | `unauthorized_quota_access` diagnostic is emitted. |
| `unauthorized-lease-access` | Access a lease without authorization. | `unauthorized_lease_access` diagnostic is emitted. |

**Exhaustion tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `quota-exhausted` | Exhaust a quota. | `quota_exhausted` diagnostic is emitted. |
| `approval-expired` | Wait for an approval to expire. | `approval_expired` diagnostic is emitted. |
| `lease-expired` | Wait for a lease to expire. | `lease_expired` diagnostic is emitted. |

**Unavailable tests (6 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-store-unavailable` | Simulate thread store unavailability. | `thread_store_unavailable` diagnostic is emitted. |
| `checkpoint-store-unavailable` | Simulate checkpoint store unavailability. | `checkpoint_store_unavailable` diagnostic is emitted. |
| `memory-store-unavailable` | Simulate memory store unavailability. | `memory_store_unavailable` diagnostic is emitted. |
| `approval-store-unavailable` | Simulate approval store unavailability. | `approval_store_unavailable` diagnostic is emitted. |
| `quota-store-unavailable` | Simulate quota store unavailability. | `quota_store_unavailable` diagnostic is emitted. |
| `lease-store-unavailable` | Simulate lease store unavailability. | `lease_store_unavailable` diagnostic is emitted. |

### Subtask 4.4.1.3 - Timeout and cancellation

Verified timeout, cancellation, unavailable dependency, and retry behavior
leave no unauthorized or partial state.

**Timeout tests (4 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-timeout` | Thread creation times out. | Thread is not created, no partial state. |
| `checkpoint-timeout` | Checkpoint creation times out. | Checkpoint is not created, no partial state. |
| `approval-timeout` | Approval decision times out. | Approval remains pending, no partial state. |
| `lease-timeout` | Lease creation times out. | Lease is not created, no partial state. |

**Cancellation tests (4 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-cancel` | Cancel a thread creation. | Thread is not created, no partial state. |
| `checkpoint-cancel` | Cancel a checkpoint creation. | Checkpoint is not created, no partial state. |
| `approval-cancel` | Cancel an approval request. | Approval is cancelled with status `cancelled`. |
| `lease-cancel` | Cancel a lease creation. | Lease is not created, no partial state. |

**Unavailable dependency tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-unavailable-retry` | Thread store is unavailable, then becomes available. | Thread is created on retry. |
| `checkpoint-unavailable-retry` | Checkpoint store is unavailable, then becomes available. | Checkpoint is created on retry. |
| `quota-unavailable-retry` | Quota store is unavailable, then becomes available. | Quota reservation succeeds on retry. |

**Retry tests (3 tests):**

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-retry-success` | Thread creation fails, then succeeds on retry. | Thread is created successfully. |
| `checkpoint-retry-success` | Checkpoint creation fails, then succeeds on retry. | Checkpoint is created successfully. |
| `lease-retry-success` | Lease creation fails, then succeeds on retry. | Lease is created successfully. |

### Subtask 4.4.1.4 - Cross-milestone fixtures

Ran all earlier milestone fixtures affected by this phase and recorded
regressions or approved variability.

**Cross-milestone fixture scopes (10 milestones):**

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

**Regression summary:**

No regressions were identified in earlier milestone fixtures.

## Key design decisions

1. **Comprehensive test coverage**: Tests cover all aspects of Phase 4.

2. **Successful flow tests**: Tests verify the canonical successful flow.

3. **Failure handling tests**: Tests verify that failures are handled correctly with stable diagnostics.

4. **Timeout and cancellation tests**: Tests verify that timeouts and cancellations leave no unauthorized or partial state.

5. **Cross-milestone compatibility**: Tests verify that Phase 4 does not regress earlier milestones.

6. **Evidence retention**: Tests verify that evidence is emitted for significant events.

7. **Bounded diagnostics**: Diagnostics are bounded and do not expose secrets.

8. **Tenant isolation**: Tests verify tenant isolation for all resources.

9. **Quota enforcement**: Tests verify quota enforcement at all points.

10. **Secret lease security**: Tests verify secret lease security and revocation.

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

- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md)

### Related chapters

- [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- [30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../31-capability-policy-attenuation-limits-and-enforcement.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../34-provenance-signing-audit-security-and-milestone-acceptance.md)
