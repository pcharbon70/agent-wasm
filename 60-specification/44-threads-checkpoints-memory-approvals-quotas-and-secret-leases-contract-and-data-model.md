---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model"
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
  - contract
  - data-model
aliases:
  - "M7-P4 Contract And Data Model"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the contract and data model for threads, checkpoints, memory,
approvals, quotas, and secret leases, including conversation threads, messages,
participants, causal links, content references, visibility, redaction, retention,
checkpoints as versioned projections, and memory references with provenance,
tenant scope, confidence, promotion, and deletion policy.

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
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md).

## 44.1 Contract And Data Model

### Conversation threads

> **Normative definition.**
A conversation thread is a durable, human-visible record of interactions
between an agent and its participants (users, other agents, or systems).
Threads are separate from turn journals and authoritative agent state.

> **Normative definition.**
Every conversation thread MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `thread_id` | The `ThreadId` of the conversation thread. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that owns this thread. | Host runtime |
| `tenant_scope` | The tenant scope of the thread. | Host runtime |
| `subject` | A human-readable subject for the thread. | Host runtime |
| `created_at` | The ISO 8601 timestamp of thread creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last thread update. | Host clock |
| `message_count` | The number of messages in the thread. | Host runtime |
| `visibility` | The visibility policy (`private`, `shared`, `public`). | Host runtime |
| `retention` | The retention policy (`permanent`, `temporary`, `custom`). | Host runtime |
| `redaction_policy` | The redaction policy for sensitive content. | Host runtime |
| `status` | The thread status (`active`, `archived`, `deleted`). | Host runtime |

> **Normative definition.**
Every message in a conversation thread MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `message_id` | The `MessageId` of the message. | Host runtime |
| `thread_id` | The `ThreadId` of the parent thread. | Host runtime |
| `sender` | The sender of the message (agent, user, system). | Host runtime |
| `recipient` | The recipient of the message (if any). | Host runtime |
| `content` | The message content (text, structured data). | Host runtime |
| `causal_link` | The causal link to the previous message (if any). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the message. | Host clock |
| `visibility` | The visibility policy for this message. | Host runtime |
| `redacted` | Whether this message has been redacted. | Host runtime |

> **Normative definition.**
Every participant in a conversation thread MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `participant_id` | The `ParticipantId` of the participant. | Host runtime |
| `thread_id` | The `ThreadId` of the thread. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the participant. | Host runtime |
| `role` | The participant's role (`owner`, `viewer`, `contributor`). | Host runtime |
| `joined_at` | The ISO 8601 timestamp of joining the thread. | Host clock |
| `left_at` | The ISO 8601 timestamp of leaving the thread (null if active). | Host clock |

> **Normative definition.**
Causal links connect messages to their causes (e.g., a response to a question).
Each causal link MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `link_id` | The `LinkId` of the causal link. | Host runtime |
| `source_message_id` | The `MessageId` of the source message. | Host runtime |
| `target_message_id` | The `MessageId` of the target message. | Host runtime |
| `link_type` | The type of causal link (`response`, `reference`, `dependency`). | Host runtime |

> **Normative definition.**
Content references allow messages to reference external content (e.g., documents, images).
Each content reference MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `ref_id` | The `RefId` of the content reference. | Host runtime |
| `content_type` | The type of content (`text`, `image`, `document`, `code`). | Host runtime |
| `content_uri` | The URI of the content. | Host runtime |
| `content_hash` | The hash of the content. | Host runtime |

### Checkpoints

> **Normative definition.**
A checkpoint is a versioned projection of an agent's state at a point in time.
Checkpoints are separate from authoritative agent state and audit evidence.

> **Normative definition.**
Every checkpoint MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `checkpoint_id` | The `CheckpointId` of the checkpoint. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `source_revision` | The `SnapshotRevision` of the source state. | Host runtime |
| `schema_version` | The schema version of the checkpoint. | Host runtime |
| `snapshot` | The snapshot data (versioned projection). | Host runtime |
| `strategy_id` | The `StrategyId` of the strategy at checkpoint time. | Host runtime |
| `validation_evidence` | The validation evidence for the checkpoint. | Host runtime |
| `created_at` | The ISO 8601 timestamp of checkpoint creation. | Host clock |
| `created_by` | The `TenantQualifiedAgentAddress` that created the checkpoint. | Host runtime |
| `status` | The checkpoint status (`active`, `archived`, `deleted`). | Host runtime |

> **Normative definition.**
A checkpoint MUST be a versioned projection of the agent's state at a point in time.
The projection includes:
- The current state of the agent.
- The state of any associated resources (threads, memory, etc.).
- The strategy instance and its state.
- Any pending directives or approvals.

> **Normative definition.**
The source revision enables:
- Detecting stale checkpoints.
- Reconstructing state from checkpoints.
- Validating checkpoint integrity.

> **Normative definition.**
Schema versioning enables backward-compatible evolution of checkpoint schemas:
- Forward migration: A newer schema can read older checkpoints.
- Backward migration: An older schema cannot read newer checkpoints.
- Schema compatibility: Checkpoints are validated against the current schema.

> **Normative definition.**
Validation evidence proves that the checkpoint is valid and consistent.
It includes:
- The snapshot hash at checkpoint creation.
- The strategy state hash at checkpoint creation.
- Any external references (threads, memory) and their hashes.

### Memory references

> **Normative definition.**
Memory references are durable records of information retained by an agent.
Memory types include working, episodic, semantic, and retrieved memory.

> **Normative definition.**
Every memory reference MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `memory_id` | The `MemoryId` of the memory reference. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent. | Host runtime |
| `memory_type` | The type of memory (`working`, `episodic`, `semantic`, `retrieved`). | Host runtime |
| `content` | The memory content. | Host runtime |
| `provenance` | The provenance of the memory (source, creator, timestamp). | Host runtime |
| `tenant_scope` | The tenant scope of the memory. | Host runtime |
| `confidence` | The confidence score of the memory (0.0 to 1.0). | Host runtime |
| `created_at` | The ISO 8601 timestamp of memory creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last memory update. | Host clock |
| `status` | The memory status (`active`, `archived`, `deleted`). | Host runtime |

> **Normative definition.**
Memory types are defined as follows:

| Type | Description |
|------|-------------|
| `working` | Short-term memory used during active task execution. |
| `episodic` | Long-term memory of specific events or experiences. |
| `semantic` | Long-term memory of general knowledge and facts. |
| `retrieved` | Memory retrieved from external sources (e.g., search results). |

> **Normative definition.**
Provenance tracks where the memory came from.
It includes:
- `source`: The source of the memory (agent, user, external).
- `creator`: The `TenantQualifiedAgentAddress` that created the memory.
- `timestamp`: The ISO 8601 timestamp of creation.
- `context`: The context in which the memory was created.

> **Normative definition.**
Tenant scope controls which tenants can access the memory:
- `private`: Only the agent's tenant can access it.
- `shared`: Authorized tenants can access it.
- `public`: Any tenant can access it.

> **Normative definition.**
Confidence score indicates how reliable the memory is:
- `1.0`: High confidence (e.g., directly observed).
- `0.5`: Medium confidence (e.g., inferred).
- `0.0`: Low confidence (e.g., speculative).

> **Normative definition.**
Promotion moves memory between types (e.g., working to episodic).
It includes:
- `promotion_policy`: Defines when promotion occurs.
- `promoted_from`: The previous memory type.
- `promoted_at`: The ISO 8601 timestamp of promotion.

> **Normative definition.**
Deletion policy defines when memory is deleted:
- `permanent`: Memory is deleted immediately.
- `temporary`: Memory is deleted after a configurable period.
- `conditional`: Memory is deleted based on conditions (e.g., confidence below threshold).

## Variability register

### 44.1.1 Thread visibility

- **Permission**: The host MAY configure default visibility for new threads.
- **Recommendation**: The host SHOULD default to `private` visibility.
- **Permitted presentation**: The host MAY present the configured visibility to the operator.
- **Limit**: The host MUST enforce visibility controls at retrieval time.

### 44.1.2 Memory confidence defaults

- **Permission**: The host MAY configure default confidence scores for different memory types.
- **Recommendation**: The host SHOULD use the following defaults:
  - `working`: 1.0
  - `episodic`: 0.8
  - `semantic`: 0.7
  - `retrieved`: 0.5
- **Permitted presentation**: The host MAY present the configured defaults to the operator.
- **Limit**: The host MUST document the configured defaults.

### 44.1.3 Checkpoint schema versioning

- **Permission**: The host MAY implement custom schema migration logic.
- **Recommendation**: The host SHOULD support forward migration only.
- **Permitted presentation**: The host MAY log schema migration events for observability.
- **Limit**: The host MUST not allow backward migration to older schemas.
