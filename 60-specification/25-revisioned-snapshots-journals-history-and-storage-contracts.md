---
title: "Revisioned Snapshots Journals History And Storage Contracts"
kind: specification
created: "2026-08-09"
status: normative
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

This chapter is a normative specification produced by
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

## 1.1 Contract And Data Model

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

`TurnResult` is defined in [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).
`Directive` is defined in
[Directives](04-turn-lifecycle-protocols-and-canonical-encoding.md#directives),
with processing semantics in
[Directive processing](13-directives-strategies-continuations-and-terminal-states.md#directive-processing).

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
Journal compaction is limited to rewriting the physical storage representation.
After compaction, every logical journal entry MUST remain available with
byte-identical canonical content, the same entry identity and order, and the
same query, audit, reconstruction, and replay behavior. Compaction MUST NOT
delete, merge, summarize, or replace a logical audit-journal entry.

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
  agent_id: AgentId,
  signal_id: String,
  role: User | Assistant,
  content: String,
  timestamp: UnixTimestamp,
  directives: Directive[]
}
```

`ConversationEntry` is derived from `JournalEntry` by projecting the following fields:
- `entry_id` from `JournalEntry.entry_id`
- `agent_id` from `JournalEntry.agent_id`
- `signal_id` from `JournalEntry.signal_id`
- `role` derived from `JournalEntry.directives` (User or Assistant based on directive type)
- `content` derived from `JournalEntry.directives` (filtered for user-facing content)
- `timestamp` from `JournalEntry.timestamp` (or host-provided timestamp)
- `directives` from `JournalEntry.directives` (filtered for user-facing directives)

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

## 1.2 Behavior And Integration

### Transactional storage interfaces

> **Normative definition.**
The host MUST provide the following transactional storage interfaces:

1. **Read**: Read a snapshot or journal entry by ID with isolation guarantees.
2. **Compare-and-commit**: Atomically read, validate, and write with optimistic
   conflict detection.
3. **Snapshot**: Create a new snapshot with the next revision number.
4. **Journal scan**: Scan journal entries within a revision range or time range.
5. **Checkpoint**: Mark a point in the journal for quick recovery.
6. **Retention**: Apply retention policies to eligible snapshots and derived
   projections while preserving every logical audit-journal entry indefinitely.

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
Every committed logical audit-journal entry MUST remain readable. An unavailable
entry is corruption or storage unavailability, not a permitted retention outcome,
and MUST use `storage.journal.corruption` or `storage.unavailable`, respectively.

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
The host MUST verify the integrity of journal entries on read.
If a journal entry is corrupted, the host MUST reject the read with
`storage.journal.corruption` and log the incident.

> **Normative definition.**
The host MUST support backup and recovery from corrupted data.
The host MUST NOT allow corrupted data to propagate to state projections.

### Unavailable store

> **Normative definition.**
The host MUST handle storage backend unavailability gracefully.
If the storage backend is unavailable, the host MUST return
`storage.unavailable` and MUST NOT perform any state changes.

> **Normative definition.**
The host MUST support retry logic for transient storage failures.
The host MUST limit the number of retries and back off exponentially.

> **Normative definition.**
If the storage backend remains unavailable after retries, the host MUST
abort the operation and release all acquired resources (leases, locks).

### Partial migration

> **Normative definition.**
The host MUST support storage backend migration without downtime.
The host MUST perform migration in phases:

1. **Preparation**: Provision the new backend and verify connectivity.
2. **Data replication**: Copy data from the old backend to the new backend.
3. **Cutover**: Atomically switch all reads and writes to the new backend.
4. **Verification**: Verify data consistency on the new backend.
5. **Cleanup**: Decommission the old backend after the retention period.

> **Normative definition.**
The host MUST verify data consistency after migration.
If migration fails at any phase, the host MUST roll back to the old backend.

> **Normative definition.**
The host MUST NOT serve reads and writes from different backends simultaneously
except during the data replication phase, where reads MUST be served from the
old backend and writes MUST be served from both backends (with the new backend
as the source of truth).

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

## 1.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for revisioned snapshots
journals history and storage contracts:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current schema version or
   artifact version.
3. **Conflicting**: Multiple writers attempt to write to the same revision
   (optimistic concurrency conflict).
4. **Unauthorized**: The caller does not have permission to perform the operation.
5. **Exhausted**: The system is out of resources (e.g., storage capacity, retry
   budget).
6. **Unavailable**: The storage backend is unavailable.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for revisioned snapshots journals
history and storage contracts:

| Error Code | Description |
|------------|-------------|
| `storage.snapshot.duplicate` | Snapshot ID already exists |
| `storage.snapshot.not_found` | Snapshot ID does not exist |
| `storage.snapshot.corruption` | Snapshot checksum verification failed |
| `storage.snapshot.lifecycle_inconsistent` | Snapshot lifecycle state inconsistent with registry |
| `storage.snapshot.incompatible_schema` | State schema version incompatible |
| `storage.snapshot.incompatible_artifact` | Artifact version incompatible |
| `storage.snapshot.conflict` | Optimistic concurrency conflict |
| `storage.journal.modified` | Attempt to modify append-only journal |
| `storage.journal.corruption` | Journal entry checksum verification failed |
| `storage.unavailable` | Storage backend unavailable |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome using exactly
the `Diagnostic` top-level structure in
[Diagnostics](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics).
The domain error from the table above is `code`, `severity` is `error`, and
`details` contains `phase`, `contract`, `profile`, `failed_boundary`, `context`,
`entity_identifiers`, `timestamp`, and `retryable`. Entity identifiers contain
only the applicable tenant, agent, snapshot, or entry identifiers.

| Family | Domain codes |
|--------|--------------|
| `identity.validation.storage_contract` | `storage.journal.modified` |
| `identity.compatibility.storage_contract` | `storage.snapshot.lifecycle_inconsistent`, `storage.snapshot.incompatible_schema`, `storage.snapshot.incompatible_artifact` |
| `identity.conflict.storage_contract` | `storage.snapshot.duplicate`, `storage.snapshot.conflict` |
| `identity.resource.storage_contract` | `storage.snapshot.not_found`, `storage.unavailable` |
| `identity.storage.storage_contract` | `storage.snapshot.corruption`, `storage.journal.corruption` |

No additional top-level diagnostic member is permitted.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:
Each selection is one of the alternatives or bounded domains stated below.
Observable checksum values, retention availability, retry timing, and storage
resource consumption may differ according to the recorded selections.

1. **Storage backend**: A transactional database, an object store paired with a
   durable journal, or an append-only durable log, with its durability
   guarantees.
2. **Hash algorithm**: SHA-256, SHA-384, SHA-512, or BLAKE3 for checksums.
3. **Retention period**: Snapshot retention where the snapshot lifecycle permits
   deletion, plus retention of derived conversation and reconstruction
   projections. Audit-journal entries have no finite retention period.
4. **Retry strategy**: No retry, fixed-delay retry, or exponential-backoff retry
   for transient failures, subject to the governing attempt and duration limits.
5. **Garbage collection**: Reference counting, mark-and-sweep, or
   lifecycle-triggered deletion for snapshots and
   derived projections whose governing lifecycle permits deletion. Logical
   audit-journal entries are never garbage collected.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **State-schema migration**: The migration strategy between compatible schema
   versions.
2. **Storage backend migration**: The migration strategy between storage
   backends.
3. **Journal compaction optimization**: Alternative physical compaction
   techniques that preserve the fixed logical behavior defined above.
4. **Snapshot compression**: The compression strategy for old snapshots.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 1 MAY invalidate earlier milestone assumptions:

1. **Storage requirements**: If the storage requirements exceed the capacity
   planned in earlier milestones, the capacity plan MUST be revised.
2. **Journal growth**: If the journal grows faster than expected, storage
   capacity or the physical compaction strategy MUST be revised without
   deleting or changing logical audit-journal entries.
3. **Checksum algorithm**: If the chosen checksum algorithm has known weaknesses,
   the algorithm MUST be changed.

> **Non-normative note.**
If any result from Phase 1 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## 1.4 Phase 1 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 1 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host creates, reads, updates, and deletes
   eligible snapshots correctly while creating, reading, and physically
   compacting journal storage without deleting logical audit-journal entries.
2. **Failure handling**: The host handles malformed, incompatible, stale,
   duplicate, and boundary-limit inputs correctly.
3. **Transient failure recovery**: The host recovers from timeout, cancellation,
   unavailable dependency, and retry behavior without leaving unauthorized or
   partial state.
4. **Cross-milestone compatibility**: The phase does not introduce regressions
   in earlier milestones.

> **Normative definition.**
Each integration test MUST exercise observable contracts rather than private
implementation structure.

### Successful flow tests

> **Normative definition.**
The following tests MUST verify the canonical successful flow:

1. **Snapshot creation**: Create a snapshot with valid data and verify it is
   stored correctly.
2. **Snapshot read**: Read a snapshot by ID and verify the data matches.
3. **Snapshot update**: Update a snapshot and verify the new revision is stored.
4. **Journal write**: Write a journal entry and verify it is stored correctly.
5. **Journal scan**: Scan journal entries within a revision range and verify
   the results.
6. **Snapshot deletion**: Delete a snapshot and verify it is removed.
7. **Journal compaction**: Compact the physical journal representation and
   verify that every logical entry remains byte-identical, in the same order,
   and produces identical audit, query, reconstruction, and replay results.
8. **Audit-journal retention**: Apply the shortest supported snapshot and
   derived-projection retention periods and verify that every logical
   audit-journal entry remains readable and unchanged.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Malformed input**: Submit malformed input and verify the error code and
   diagnostic message.
2. **Incompatible schema**: Submit a snapshot with an incompatible schema
   version and verify the error code.
3. **Incompatible artifact**: Submit a snapshot with an incompatible artifact
   version and verify the error code.
4. **Stale revision**: Submit a snapshot with a stale revision and verify the
   error code.
5. **Duplicate snapshot**: Submit a snapshot with a duplicate ID and verify
   the error code.
6. **Boundary limits**: Submit input that exceeds boundary limits and verify
   the error code.

> **Normative definition.**
Each test MUST verify the exact Chapter 04 diagnostic shape, assigned family,
domain `code`, `severity: "error"`, message, and required bounded details.

### Transient failure recovery tests

> **Normative definition.**
The following tests MUST verify transient failure recovery:

1. **Timeout**: Simulate a timeout during snapshot creation and verify the
   operation is aborted and no partial state is left.
2. **Cancellation**: Simulate a cancellation during journal write and verify
   the operation is aborted and no partial state is left.
3. **Unavailable storage**: Simulate storage backend unavailability and verify
   the operation is retried and eventually succeeds or fails with the correct
   error code.
4. **Retry behavior**: Simulate transient failures and verify the retry logic
   works correctly.

> **Normative definition.**
Each test MUST verify that no unauthorized or partial state is left after the
failure.

### Cross-milestone compatibility tests

> **Normative definition.**
The following tests MUST verify cross-milestone compatibility:

1. **Milestone 1 fixtures**: Run all Milestone 1 fixtures and verify no
   regressions.
2. **Milestone 2 fixtures**: Run all Milestone 2 fixtures and verify no
   regressions.
3. **Milestone 3 fixtures**: Run all Milestone 3 fixtures and verify no
   regressions.

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 1 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Replay results**: Evidence that canonical re-encoding and replay produce
   identical results.
3. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
4. **Recovery evidence**: Evidence that transient failures are recovered from
   correctly.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.

## Variability register

The register below indexes profile selections and other variability governed by
the linked clauses. It does not independently license variation.

> **Non-normative note.**

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| [Hash algorithm for checksums](#checksum-computation) | Use any cryptographically secure hash | SHA-256 or stronger | Must be constant within a deployment |
| [State-schema migration](#state-schema-version) | Deferred to host implementation | Document migration strategy | No automatic migration without consent |
| [Snapshot and derived-projection retention](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must not delete snapshots whose lifecycle requires preservation or any logical audit-journal entry |
| [Snapshot and derived-projection garbage collection](#implementation-defined-choices) | Implementation-defined | Document retention policy | Must preserve every logical audit-journal entry indefinitely |
| [Journal compaction](#append-only-turn-journal) | Internal mechanism | Physical rewrite only | Must preserve byte-identical logical entries, identity, order, queries, audit, reconstruction, and replay |
| [Storage backend](#backend-neutral-durability) | Choose any backend | Document in conformance profile | Must support ACID transactions |
| [Retry strategy](#unavailable-store) | Implementation-defined | Exponential backoff | Must limit retries and back off |
| [Conflict resolution](#optimistic-conflict-detection) | Required | Abort and retry | Must not silently overwrite data |
