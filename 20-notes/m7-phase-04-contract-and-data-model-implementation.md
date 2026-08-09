---
title: "Phase 4 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-04
  - implementation
  - contract
  - data-model
  - threads
  - checkpoints
  - memory
aliases:
  - "M7-P4 Contract And Data Model Implementation"
---

# Phase 4 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 4.1 from Phase 4 plan:
**Contract And Data Model** for Threads, Checkpoints, Memory, Approvals,
Quotas, And Secret Leases.

## Implementation notes

### Subtask 4.1.1.1 - Conversation threads

Defined conversation threads, messages, participants, causal links, content
references, visibility, redaction, and retention separately from turn journals.

**Conversation thread schema:**

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

**Message schema:**

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

**Participant schema:**

| Field | Content | Source |
|-------|---------|--------|
| `participant_id` | The `ParticipantId` of the participant. | Host runtime |
| `thread_id` | The `ThreadId` of the thread. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the participant. | Host runtime |
| `role` | The participant's role (`owner`, `viewer`, `contributor`). | Host runtime |
| `joined_at` | The ISO 8601 timestamp of joining the thread. | Host clock |
| `left_at` | The ISO 8601 timestamp of leaving the thread (null if active). | Host clock |

**Causal links:**

Causal links connect messages to their causes (e.g., a response to a question).
Each causal link includes:
- `link_id`: The `LinkId` of the causal link.
- `source_message_id`: The `MessageId` of the source message.
- `target_message_id`: The `MessageId` of the target message.
- `link_type`: The type of causal link (`response`, `reference`, `dependency`).

**Content references:**

Content references allow messages to reference external content (e.g., documents, images).
Each content reference includes:
- `ref_id`: The `RefId` of the content reference.
- `content_type`: The type of content (`text`, `image`, `document`, `code`).
- `content_uri`: The URI of the content.
- `content_hash`: The hash of the content.

**Visibility:**

Visibility controls who can see a thread or message.
- `private`: Only the owner and explicit participants can see it.
- `shared`: Participants and authorized agents can see it.
- `public`: Anyone with the thread ID can see it.

**Redaction:**

Redaction removes sensitive content from messages.
- `redaction_policy`: Defines what content is redacted.
- `redacted_fields`: The fields that have been redacted.
- `redacted_by`: The agent that performed the redaction.

**Retention:**

Retention controls how long threads and messages are kept.
- `permanent`: Thread is kept indefinitely.
- `temporary`: Thread is deleted after a configurable period.
- `custom`: Thread is deleted according to a custom policy.

### Subtask 4.1.1.2 - Checkpoints

Defined checkpoints as versioned projections with source revision, schema,
artifact, strategy, and validation evidence.

**Checkpoint schema:**

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

**Versioned projection:**

A checkpoint is a versioned projection of the agent's state at a point in time.
It includes:
- The current state of the agent.
- The state of any associated resources (threads, memory, etc.).
- The strategy instance and its state.
- Any pending directives or approvals.

**Source revision:**

The source revision tracks which snapshot revision the checkpoint was created from.
This enables:
- Detecting stale checkpoints.
- Reconstructing state from checkpoints.
- Validating checkpoint integrity.

**Schema version:**

The schema version enables backward-compatible evolution of checkpoint schemas.
- Forward migration: A newer schema can read older checkpoints.
- Backward migration: An older schema cannot read newer checkpoints.
- Schema compatibility: Checkpoints are validated against the current schema.

**Validation evidence:**

Validation evidence proves that the checkpoint is valid and consistent.
It includes:
- The snapshot hash at checkpoint creation.
- The strategy state hash at checkpoint creation.
- Any external references (threads, memory) and their hashes.

### Subtask 4.1.1.3 - Memory references

Defined working, episodic, semantic, and retrieved memory references with
provenance, tenant scope, confidence, promotion, and deletion policy.

**Memory reference schema:**

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

**Memory types:**

- **Working memory**: Short-term memory used during active task execution.
- **Episodic memory**: Long-term memory of specific events or experiences.
- **Semantic memory**: Long-term memory of general knowledge and facts.
- **Retrieved memory**: Memory retrieved from external sources (e.g., search results).

**Provenance:**

Provenance tracks where the memory came from.
- `source`: The source of the memory (agent, user, external).
- `creator`: The `TenantQualifiedAgentAddress` that created the memory.
- `timestamp`: The ISO 8601 timestamp of creation.
- `context`: The context in which the memory was created.

**Tenant scope:**

Tenant scope controls which tenants can access the memory.
- `private`: Only the agent's tenant can access it.
- `shared`: Authorized tenants can access it.
- `public`: Any tenant can access it.

**Confidence:**

Confidence score indicates how reliable the memory is.
- `1.0`: High confidence (e.g., directly observed).
- `0.5`: Medium confidence (e.g., inferred).
- `0.0`: Low confidence (e.g., speculative).

**Promotion:**

Promotion moves memory between types (e.g., working to episodic).
- `promotion_policy`: Defines when promotion occurs.
- `promoted_from`: The previous memory type.
- `promoted_at`: The ISO 8601 timestamp of promotion.

**Deletion policy:**

Deletion policy defines when memory is deleted.
- `permanent`: Memory is deleted immediately.
- `temporary`: Memory is deleted after a configurable period.
- `conditional`: Memory is deleted based on conditions (e.g., confidence below threshold).

## Key design decisions

1. **Separate from turn journals**: Threads, checkpoints, and memory are separate from authoritative agent state and audit evidence.

2. **Versioned checkpoints**: Checkpoints are versioned projections that enable state reconstruction and validation.

3. **Memory types**: Four memory types (working, episodic, semantic, retrieved) support different use cases.

4. **Provenance tracking**: All memory references include provenance for traceability.

5. **Tenant scope enforcement**: Memory references are scoped to tenant boundaries.

6. **Confidence scoring**: Memory references include confidence scores for reliability assessment.

7. **Promotion and deletion**: Memory can be promoted between types and deleted according to policies.

8. **Visibility and redaction**: Threads and messages support visibility controls and redaction for sensitive content.

9. **Retention policies**: Threads support configurable retention policies.

10. **Causal links**: Messages can be causally linked for traceability.

## Open questions

1. Should working memory be automatically promoted to episodic memory?

2. Should semantic memory be shared across agents in the same tenant?

3. Should retrieved memory have a lower confidence score by default?

4. Should checkpoints be compressed to save storage?

5. Should memory promotion be configurable per agent?

6. Should retention policies be enforced automatically or manually?

7. Should redaction be applied at creation time or retrieval time?

8. Should causal links be bidirectional or unidirectional?

9. Should memory references support hierarchical scoping?

10. Should checkpoints support incremental updates or only full snapshots?

11. Should memory confidence scores be updated dynamically?

12. Should deleted memory be permanently removed or soft-deleted?

## Cross-references

### Earlier chapters

- [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- [26-atomic-state-journal-and-directive-outbox-commits.md](../26-atomic-state-journal-and-directive-outbox-commits.md)
- [27-effect-handlers-attempts-idempotency-and-result-signals.md](../27-effect-handlers-attempts-idempotency-and-result-signals.md)
- [30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../31-capability-policy-attenuation-limits-and-enforcement.md)

### Related chapters (Phase 4)

- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md](../44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md)
