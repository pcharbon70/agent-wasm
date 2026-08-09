---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-04
  - threads
  - checkpoints
  - memory
  - approvals
  - quotas
  - secret-leases
  - integration-tests
aliases:
  - "M7-P4 Integration Tests"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It defines the integration tests that verify threads, checkpoints, memory,
approvals, quotas, and secret leases across their real dependency boundaries.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
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
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md).

## 44.4 Integration Tests

### Successful flow tests

> **Normative definition.**
The following tests verify the canonical successful flow for threads, checkpoints,
memory, approvals, quotas, and secret leases:

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

> **Normative definition.**
The following tests verify evidence retention:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `evidence-thread-created` | Verify evidence is emitted when a thread is created. | `thread.created` evidence is emitted. |
| `evidence-thread-archived` | Verify evidence is emitted when a thread is archived. | `thread.archived` evidence is emitted. |
| `evidence-thread-message-added` | Verify evidence is emitted when a message is added. | `thread.message_added` evidence is emitted. |
| `evidence-checkpoint-created` | Verify evidence is emitted when a checkpoint is created. | `checkpoint.created` evidence is emitted. |
| `evidence-checkpoint-restored` | Verify evidence is emitted when a checkpoint is restored. | `checkpoint.restored` evidence is emitted. |
| `evidence-memory-created` | Verify evidence is emitted when memory is created. | `memory.created` evidence is emitted. |
| `evidence-memory-promoted` | Verify evidence is emitted when memory is promoted. | `memory.promoted` evidence is emitted. |
| `evidence-approval-requested` | Verify evidence is emitted when an approval is requested. | `approval.requested` evidence is emitted. |
| `evidence-approval-approved` | Verify evidence is emitted when an approval is approved. | `approval.approved` evidence is emitted. |
| `evidence-approval-rejected` | Verify evidence is emitted when an approval is rejected. | `approval.rejected` evidence is emitted. |
| `evidence-quota-reserved` | Verify evidence is emitted when quota is reserved. | `quota.reserved` evidence is emitted. |
| `evidence-quota-consumed` | Verify evidence is emitted when quota is consumed. | `quota.consumed` evidence is emitted. |
| `evidence-quota-exhausted` | Verify evidence is emitted when quota is exhausted. | `quota.exhausted` evidence is emitted. |
| `evidence-lease-created` | Verify evidence is emitted when a lease is created. | `lease.created` evidence is emitted. |
| `evidence-lease-revoked` | Verify evidence is emitted when a lease is revoked. | `lease.revoked` evidence is emitted. |

### Failure handling tests

> **Normative definition.**
The following tests verify malformed input handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `malformed-thread-missing-id` | Create a thread without a thread ID. | `malformed_thread_input` diagnostic is emitted. |
| `malformed-message-missing-content` | Create a message without content. | `malformed_message_input` diagnostic is emitted. |
| `malformed-checkpoint-missing-revision` | Create a checkpoint without a source revision. | `malformed_checkpoint_input` diagnostic is emitted. |
| `malformed-memory-missing-type` | Create memory without a type. | `malformed_memory_input` diagnostic is emitted. |
| `malformed-approval-missing-type` | Request approval without a type. | `malformed_approval_input` diagnostic is emitted. |
| `malformed-quota-missing-limit` | Create a quota without a limit. | `malformed_quota_input` diagnostic is emitted. |
| `malformed-lease-missing-principal` | Create a lease without a principal. | `malformed_lease_input` diagnostic is emitted. |

> **Normative definition.**
The following tests verify incompatible input handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `incompatible-thread-version` | Create a thread with an incompatible version. | `incompatible_thread_version` diagnostic is emitted. |
| `incompatible-checkpoint-version` | Create a checkpoint with an incompatible version. | `incompatible_checkpoint_version` diagnostic is emitted. |
| `incompatible-memory-version` | Create memory with an incompatible version. | `incompatible_memory_version` diagnostic is emitted. |

> **Normative definition.**
The following tests verify conflict handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `conflicting-thread-visibility` | Update a thread with conflicting visibility. | `conflicting_thread_visibility` diagnostic is emitted. |
| `conflicting-quota-limit` | Update a quota with conflicting limit. | `conflicting_quota_limit` diagnostic is emitted. |
| `conflicting-lease-expiry` | Update a lease with conflicting expiry. | `conflicting_lease_expiry` diagnostic is emitted. |

> **Normative definition.**
The following tests verify unauthorized access handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `unauthorized-thread-access` | Access a thread without authorization. | `unauthorized_thread_access` diagnostic is emitted. |
| `unauthorized-checkpoint-access` | Access a checkpoint without authorization. | `unauthorized_checkpoint_access` diagnostic is emitted. |
| `unauthorized-memory-access` | Access memory without authorization. | `unauthorized_memory_access` diagnostic is emitted. |
| `unauthorized-approval-access` | Access an approval without authorization. | `unauthorized_approval_access` diagnostic is emitted. |
| `unauthorized-quota-access` | Access a quota without authorization. | `unauthorized_quota_access` diagnostic is emitted. |
| `unauthorized-lease-access` | Access a lease without authorization. | `unauthorized_lease_access` diagnostic is emitted. |

> **Normative definition.**
The following tests verify exhaustion handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `quota-exhausted` | Exhaust a quota. | `quota_exhausted` diagnostic is emitted. |
| `approval-expired` | Wait for an approval to expire. | `approval_expired` diagnostic is emitted. |
| `lease-expired` | Wait for a lease to expire. | `lease_expired` diagnostic is emitted. |

> **Normative definition.**
The following tests verify unavailable dependency handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-store-unavailable` | Simulate thread store unavailability. | `thread_store_unavailable` diagnostic is emitted. |
| `checkpoint-store-unavailable` | Simulate checkpoint store unavailability. | `checkpoint_store_unavailable` diagnostic is emitted. |
| `memory-store-unavailable` | Simulate memory store unavailability. | `memory_store_unavailable` diagnostic is emitted. |
| `approval-store-unavailable` | Simulate approval store unavailability. | `approval_store_unavailable` diagnostic is emitted. |
| `quota-store-unavailable` | Simulate quota store unavailability. | `quota_store_unavailable` diagnostic is emitted. |
| `lease-store-unavailable` | Simulate lease store unavailability. | `lease_store_unavailable` diagnostic is emitted. |

### Timeout and cancellation tests

> **Normative definition.**
The following tests verify timeout handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-timeout` | Thread creation times out. | Thread is not created, no partial state. |
| `checkpoint-timeout` | Checkpoint creation times out. | Checkpoint is not created, no partial state. |
| `approval-timeout` | Approval decision times out. | Approval remains pending, no partial state. |
| `lease-timeout` | Lease creation times out. | Lease is not created, no partial state. |

> **Normative definition.**
The following tests verify cancellation handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-cancel` | Cancel a thread creation. | Thread is not created, no partial state. |
| `checkpoint-cancel` | Cancel a checkpoint creation. | Checkpoint is not created, no partial state. |
| `approval-cancel` | Cancel an approval request. | Approval is cancelled with status `cancelled`. |
| `lease-cancel` | Cancel a lease creation. | Lease is not created, no partial state. |

> **Normative definition.**
The following tests verify unavailable dependency handling with retry:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-unavailable-retry` | Thread store is unavailable, then becomes available. | Thread is created on retry. |
| `checkpoint-unavailable-retry` | Checkpoint store is unavailable, then becomes available. | Checkpoint is created on retry. |
| `quota-unavailable-retry` | Quota store is unavailable, then becomes available. | Quota reservation succeeds on retry. |

> **Normative definition.**
The following tests verify retry handling:

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `thread-retry-success` | Thread creation fails, then succeeds on retry. | Thread is created successfully. |
| `checkpoint-retry-success` | Checkpoint creation fails, then succeeds on retry. | Checkpoint is created successfully. |
| `lease-retry-success` | Lease creation fails, then succeeds on retry. | Lease is created successfully. |

### Cross-milestone fixture scopes

> **Normative definition.**
The following earlier milestone fixtures are affected by this phase:

| Milestone | Fixture scope | Expected status |
|-----------|---------------|-----------------|
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

> **Normative definition.**
No regressions are expected in earlier milestone fixtures.
If any regression is identified, it MUST be documented and reported to the
milestone maintainer.
