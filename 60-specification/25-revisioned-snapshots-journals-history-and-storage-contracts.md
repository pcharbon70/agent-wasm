---
title: "Revisioned Snapshots Journals History And Storage Contracts"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-01
  - durable-state
  - snapshot
  - journal
  - history
  - storage
aliases:
  - "M4-P1 Revisioned Snapshots Journals History And Storage Contracts"
---

# Revisioned Snapshots Journals History And Storage Contracts

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-01-revisioned-snapshots-journals-history-and-storage-contracts.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It defines durable records and transactional storage boundaries for
authoritative state, history, and replay.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md),
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).

## 4.1 Contract And Data Model

### Agent snapshot

> **Normative definition.**
An agent snapshot is a durable record of agent state at a specific revision.
It includes agent snapshot identity, state-schema version, revision, artifact
version, strategy snapshot, lifecycle state, and checksum.

> **Normative definition.**

```
AgentSnapshot {
  snapshot_id: SnapshotId,
  agent_id: AgentId,
  tenant_id: TenantId,
  state_schema_version: string,
  revision: u64,
  artifact_version: string,
  strategy_snapshot: JsonObject?,
  lifecycle_state: LifecycleState,
  checksum: Bytes,
  created_at: UnixTimestamp,
  metadata: JsonObject
}

SnapshotId = string

LifecycleState {
  Pending,
  Active,
  Suspended,
  Hibernal,
  Cancelled,
  Completed,
  Terminated
}

TenantId = string
AgentId = string
UnixTimestamp = string
```

`TenantId`, `AgentId`, and `UnixTimestamp` are defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `snapshot_id` | SnapshotId | Yes | Unique snapshot identifier |
| `agent_id` | AgentId | Yes | Agent this snapshot belongs to |
| `tenant_id` | TenantId | Yes | Tenant this snapshot belongs to |
| `state_schema_version` | string | Yes | State schema version |
| `revision` | u64 | Yes | State revision number |
| `artifact_version` | string | Yes | Artifact version |
| `strategy_snapshot` | JsonObject? | No | Strategy state snapshot |
| `lifecycle_state` | LifecycleState | Yes | Current lifecycle state |
| `checksum` | Bytes | Yes | Checksum for integrity verification |
| `created_at` | UnixTimestamp | Yes | Snapshot creation time |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `snapshot_id` is unique per `(tenant_id, agent_id, revision)` tuple.
The host MUST reject duplicate snapshot IDs with `storage.snapshot.duplicate`.

> **Normative definition.**
The `lifecycle_state` field MUST be consistent with the agent's lifecycle state
in the registry.
The host MUST reject snapshots with inconsistent lifecycle states with
`storage.snapshot.lifecycle_inconsistent`.

> **Normative definition.**
The `checksum` field is a hash of the snapshot content (excluding the checksum
field itself).
The host MUST verify the checksum on every read.
If the checksum does not match, the host MUST reject the snapshot with
`storage.snapshot.corruption`.

### Append-only turn journal

> **Normative definition.**
An append-only turn journal is a sequence of facts linking signal, invocation,
prior revision, result, next revision, directives, and policy evidence.

> **Normative definition.**

```
JournalEntry {
  entry_id: EntryId,
  tenant_id: TenantId,
  agent_id: AgentId,
  signal_id: String,
  invocation_id: String,
  prior_revision: u64,
  result: TurnResult?,
  next_revision: u64,
  directives: Directive[],
  policy_evidence: PolicyEvidence
}

EntryId = string
SignalId = string
TurnResult = Defined in [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).
Directive = Defined in [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

PolicyEvidence {
  kind: PolicyEvidenceKind,
  data: JsonObject
}

PolicyEvidenceKind {
  Determinism,
  Replay,
  Audit
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `entry_id` | EntryId | Yes | Unique journal entry identifier |
| `tenant_id` | TenantId | Yes | Tenant this entry belongs to |
| `agent_id` | AgentId | Yes | Agent this entry belongs to |
| `signal_id` | String | Yes | Signal that triggered this turn |
| `invocation_id` | String | Yes | Invocation ID |
| `prior_revision` | u64 | Yes | State revision before this turn |
| `result` | TurnResult? | No | Turn result (null for failed turns) |
| `next_revision` | u64 | Yes | State revision after this turn |
| `directives` | Directive[] | Yes | Directives emitted by this turn |
| `policy_evidence` | PolicyEvidence | Yes | Policy evidence (determinism, replay, audit) |

> **Normative definition.**
The journal is append-only.
The host MUST NOT modify, delete, or reorder journal entries.
The host MUST reject any attempt to modify the journal with `storage.journal.modified`.

> **Normative definition.**
Each journal entry MUST be written atomically.
If a journal entry write fails, the host MUST NOT leave partial entries.
The host MUST retry the write or abort the turn.

> **Normative definition.**
The `policy_evidence` field is used for determinism verification, replay, and
audit purposes.
The host MUST populate this field according to the policy evidence kind:

- **Determinism**: Evidence that the turn was deterministic (e.g., canonical encoding hash).
- **Replay**: Evidence that the turn was replayed from the journal (e.g., original invocation ID).
- **Audit**: Audit evidence (e.g., compliance metadata).

### Journal separation

> **Normative definition.**
The host MUST separate the following journal types:

1. **Audit journal**: Immutable audit log of all turns.
2. **User-facing conversation thread**: User-visible conversation history.
3. **Reconstructable state projection**: Journal data used to reconstruct state.

> **Normative definition.**

```
JournalTypes {
  audit: AuditJournal,
  conversation: ConversationJournal,
  reconstruction: ReconstructionJournal
}

AuditJournal {
  entries: JournalEntry[],
  immutable: true
}

ConversationJournal {
  entries: ConversationEntry[],
  user_visible: true
}

ReconstructionJournal {
  entries: JournalEntry[],
  reconstructable: true
}

ConversationEntry {
  entry_id: EntryId,
  role: User | Assistant,
  content: String,
  timestamp: UnixTimestamp,
  signal_id: String
}
```

> **Normative definition.**
The audit journal is immutable and append-only.
The host MUST NOT modify, delete, or reorder audit journal entries.

> **Normative definition.**
The conversation journal is a filtered view of the audit journal for
user-facing display.
The host MAY omit internal directives, policy evidence, and technical metadata
from the conversation journal.

> **Normative definition.**
The reconstruction journal is a filtered view of the audit journal used to
reconstruct state.
The host MUST include all fields necessary for state reconstruction in the
reconstruction journal.

### Snapshot lifecycle

> **Normative definition.**
Snapshots follow the agent lifecycle state in the registry.
The host MUST enforce the following snapshot lifecycle rules:

1. **Pending**: No snapshots exist yet. The first active snapshot is created
   when the agent transitions to `Active`.
2. **Active**: Snapshots are created for each state revision. The latest
   snapshot is the current state.
3. **Suspended**: Snapshots are frozen. No new snapshots are created.
4. **Hibernal**: Snapshots are archived. The host MAY garbage collect old
   snapshots based on retention policy.
5. **Cancelled**: Snapshots are preserved for audit purposes. The host MUST
   NOT delete cancelled agent snapshots.
6. **Completed**: Snapshots are preserved for audit purposes. The host MUST
   NOT delete completed agent snapshots.
7. **Terminated**: Snapshots are deleted after the retention period expires.

> **Normative definition.**
The host MUST create a new snapshot when the agent state changes.
The host MUST increment the revision number for each new snapshot.
The host MUST NOT create multiple snapshots for the same revision.

### Checksum computation

> **Normative definition.**
The host MUST compute the checksum for each snapshot using a cryptographically
secure hash function (e.g., SHA-256).
The checksum MUST be computed over the serialized snapshot content, excluding
the `checksum` field itself.

> **Normative definition.**
The host MUST verify the checksum on every snapshot read.
If the checksum does not match, the host MUST reject the snapshot with
`storage.snapshot.corruption` and log the incident.

> **Normative definition.**
The host MUST compute the checksum before writing the snapshot to storage.
The host MUST NOT write snapshots with invalid checksums.

### State-schema version

> **Normative definition.**
The `state_schema_version` field identifies the schema version of the
snapshot's state payload.
The host MUST validate the state-schema version against the agent's manifest.
If the state-schema version is incompatible, the host MUST reject the snapshot
with `storage.snapshot.incompatible_schema`.

> **Normative definition.**
The host MUST support state-schema migration between compatible versions.
The host MUST NOT perform state-schema migration without explicit user consent.

### Artifact version

> **Normative definition.**
The `artifact_version` field identifies the version of the agent artifact
(reducer) that produced the snapshot.
The host MUST record the artifact version in each snapshot for audit purposes.

> **Normative definition.**
The host MUST NOT apply a snapshot produced by an incompatible artifact version.
If the artifact version is incompatible, the host MUST reject the snapshot with
`storage.snapshot.incompatible_artifact`.

## 4.2 Behavior And Integration

### Transactional storage interfaces

> **Normative definition.**
The host MUST provide the following transactional storage interfaces:

1. **Read**: Read a snapshot or journal entry by ID with isolation guarantees.
2. **Compare-and-commit**: Atomically read, validate, and write with optimistic
   conflict detection.
3. **Snapshot**: Create a new snapshot with the next revision number.
4. **Journal scan**: Scan journal entries within a revision range or time range.
5. **Checkpoint**: Mark a point in the journal for quick recovery.
6. **Retention**: Apply retention policies to old snapshots and journal entries.

> **Normative definition.**
Each storage interface MUST support the following isolation levels:

- **Snapshot isolation**: Read operations see a consistent snapshot of the data.
- **Serializable writes**: Write operations are serialized to prevent conflicts.

> **Normative definition.**
The host MUST support the following consistency guarantees:

- **Atomicity**: Each operation is atomic (all-or-nothing).
- **Consistency**: The storage is always in a consistent state.
- **Durability**: Committed data is persisted and survives failures.
- **Isolation**: Concurrent operations do not interfere with each other.

### Consistent reads

> **Normative definition.**
The host MUST provide consistent reads for the following operations:

1. **Snapshot read**: Read a snapshot by ID with version guarantee.
2. **Journal read**: Read journal entries in order with no gaps.
3. **Agent state projection**: Reconstruct agent state from the journal.

> **Normative definition.**
The host MUST reject reads for non-existent snapshots with `storage.snapshot.not_found`.
The host MUST reject reads for journal entries that have been garbage collected
with `storage.journal.garbage_collected`.

### Optimistic conflict detection

> **Normative definition.**
The host MUST use optimistic concurrency control for snapshot writes.
The host MUST detect conflicts when multiple writers attempt to write to the
same `(tenant_id, agent_id, revision)` tuple.

> **Normative definition.**
If a conflict is detected, the host MUST abort the write and return
`storage.snapshot.conflict`.
The host MUST NOT silently overwrite existing data.

> **Normative definition.**
The host MUST support retry logic for transient conflicts.
The host MUST limit the number of retries to prevent infinite loops.

### Corruption detection

> **Normative definition.**
The host MUST verify the checksum of every snapshot on read.
If the checksum does not match, the host MUST reject the read with
`storage.snapshot.corruption` and log the incident.

> **Normative definition.**
The host MUST verify the integrity of journal entries on read.
If a journal entry is corrupted, the host MUST reject the read with
`storage.journal.corruption` and log the incident.

> **Normative definition.**
The host MUST support backup and recovery from corrupted data.
The host MUST NOT allow corrupted data to propagate to state projections.

### Unavailable store

> **Normative definition.**
The host MUST handle storage backend unavailability gracefully.
If the storage backend is unavailable, the host MUST return `storage.unavailable`
and NOT perform any state changes.

> **Normative definition.**
The host MUST support retry logic for transient storage failures.
The host MUST limit the number of retries and back off exponentially.

> **Normative definition.**
If the storage backend remains unavailable after retries, the host MUST
abort the operation and release all acquired resources (leases, locks).

### Partial migration

> **Normative definition.**
The host MUST support storage backend migration without downtime.
During migration, the host MUST serve reads from the new backend and writes
to the old backend until migration is complete.

> **Normative definition.**
The host MUST verify data consistency after migration.
If migration fails, the host MUST roll back to the old backend.

> **Normative definition.**
The host MUST NOT serve reads and writes from different backends simultaneously.
The host MUST complete migration atomically.

### Backend-neutral durability

> **Normative definition.**
The host MUST define durability, isolation, atomicity, ordering, and recovery
capabilities in a backend-neutral manner.
The host MUST NOT expose backend-specific implementation details in the
specification.

> **Normative definition.**
The host MUST document the durability guarantees provided by the chosen
storage backend in the conformance profile.

> **Normative definition.**
The host MUST support pluggable storage backends.
The host MUST NOT hard-code storage backend logic in the core specification.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Hash algorithm for checksums | Use any cryptographically secure hash | SHA-256 or stronger | Must be constant within a deployment |
| State-schema migration | Deferred to host implementation | Document migration strategy | No automatic migration without consent |
| Journal retention period | Implementation-defined | Document in conformance profile | Must comply with regulatory requirements |
| Snapshot garbage collection | Implementation-defined | Document retention policy | Must preserve audit journal for cancelled/completed agents |
| Storage backend | Choose any backend | Document in conformance profile | Must support ACID transactions |
| Retry strategy | Implementation-defined | Exponential backoff | Must limit retries and back off |
| Conflict resolution | Implementation-defined | Abort and retry | Must not silently overwrite data |
