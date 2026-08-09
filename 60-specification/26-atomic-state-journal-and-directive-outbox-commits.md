---
title: "Atomic State Journal And Directive-Outbox Commits"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-02
  - durable-state
  - journal
  - outbox
  - commit
aliases:
  - "M4-P2 Atomic State Journal And Directive-Outbox Commits"
---

# Atomic State Journal And Directive-Outbox Commits

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-02-atomic-state-journal-and-directive-outbox-commits.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It closes the crash gap between accepting a state transition and making its
external requests durable.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
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
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

## 2.1 Contract And Data Model

### Commit unit

> **Normative definition.**
A commit unit is the atomic transaction boundary that groups state, journal,
outbox, and lifecycle changes.
The host MUST write all components of a commit unit in a single transaction.
If any component fails to write, the host MUST abort the entire transaction.

> **Normative definition.**

```
CommitUnit {
  tenant_id: TenantId,
  expected_revision: u64,
  next_revision: u64,
  snapshot: AgentSnapshot?,
  journal_entries: JournalEntry[],
  directive_outbox_entries: OutboxEntry[],
  lifecycle_changes: LifecycleChange[]
}

LifecycleChange {
  tenant_id: TenantId,
  agent_id: AgentId,
  from_state: LifecycleState,
  to_state: LifecycleState,
  timestamp: UnixTimestamp,
  reason: String
}
```

`AgentSnapshot` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`JournalEntry` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`LifecycleState` is defined in
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).
`TenantId` and `AgentId` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `tenant_id` | TenantId | Yes | Tenant this commit unit belongs to (unique per `(tenant_id, agent_id, revision)`) |
| `expected_revision` | u64 | Yes | The revision the host expects to see before commit |
| `next_revision` | u64 | Yes | The revision after the commit |
| `snapshot` | AgentSnapshot? | No | New snapshot or patch result (null if no state change) |
| `journal_entries` | JournalEntry[] | Yes | Journal entries for this turn |
| `directive_outbox_entries` | OutboxEntry[] | Yes | Directives to be dispatched |
| `lifecycle_changes` | LifecycleChange[] | Yes | Lifecycle state changes |

> **Normative definition.**
The `expected_revision` field is used for optimistic concurrency control.
If the current revision does not match `expected_revision`, the host MUST reject
the commit with `commit.conflict`.

> **Normative definition.**
The `next_revision` field MUST be `expected_revision + 1`.
The host MUST NOT allow `next_revision` to be less than or equal to the current
revision.

### Directive outbox entry

> **Normative definition.**
A directive outbox entry is a durable record of a directive that the host
must dispatch to its target.
The host MUST write outbox entries atomically with the state journal.

> **Normative definition.**

```
OutboxEntry {
  tenant_id: TenantId,
  entry_id: EntryId,
  agent_id: AgentId,
  directive_id: DirectiveId,
  payload_hash: Bytes,
  target: DirectiveTarget,
  attempt_number: u32,
  state: OutboxState,
  created_at: UnixTimestamp,
  metadata: JsonObject
}

DirectiveId = string
DirectiveTarget {
  type: Effect | Signal | Timer | Internal,
  address: String,
  idempotency_key: String?
}

OutboxState {
  Pending,
  Leased,
  Completed,
  TerminalFailed,
  Cancelled,
  Superseded
}
```

`EntryId` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`DirectiveId` is defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md) as `Directive.id`.

`DirectiveTarget.type` and `Directive.id` from
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md)
live in separate namespaces. `Directive.id` identifies the directive for the agent
turn (assigned by the agent during reduction). `DirectiveTarget.type` identifies
the dispatch category for the host outbox layer. The relationship is:
an outbox entry with `target.type = Internal` and `address` matching a
`Directive.id` refers to an in-process directive. Outbox entries for
`Effect`, `Signal`, and `Timer` targets have their own `address` space and
do not reference `Directive.id`.

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `tenant_id` | TenantId | Yes | Tenant this outbox entry belongs to (unique per `(tenant_id, entry_id)`) |
| `entry_id` | EntryId | Yes | Unique outbox entry identifier |
| `agent_id` | AgentId | Yes | Agent this outbox entry belongs to |
| `directive_id` | DirectiveId | Yes | Directive this outbox entry represents (same as `Directive.id` from file 13 for in-process directives) |
| `payload_hash` | Bytes | Yes | Hash of the directive payload (computed before commit) |
| `target` | DirectiveTarget | Yes | Target to dispatch to |
| `attempt_number` | u32 | Yes | Next dispatch attempt number (starts at 1; incremented on each attempt, capped at `u32::MAX`) |
| `state` | OutboxState | Yes | Current outbox state |
| `created_at` | UnixTimestamp | Yes | Outbox entry creation time |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `payload_hash` field is computed from the directive payload before the
commit is written.
The host MUST NOT allow outbox entries with missing or invalid `payload_hash`.

> **Normative definition.**
The `attempt_number` field is incremented on each dispatch attempt.
The host MUST NOT allow `attempt_number` to be decremented or reset.
If `attempt_number` reaches `u32::MAX`, the host MUST mark the outbox entry as
`TerminalFailed` with `outbox.attempt_number_exhausted` and MUST NOT dispatch
it again.

> **Normative definition.**
The `state` field follows the outbox state machine defined in
[Behavior And Integration](#22-behavior-and-integration).

### Directive identity and payload hash

> **Normative definition.**
The host MUST determine the directive identity and payload hash before writing
the commit unit.
The host MUST NOT write commit units with unresolved directive identities or
payload hashes.

> **Normative definition.**
The `directive_id` field on `OutboxEntry` is the same identifier as
`Directive.id` from
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).
The agent assigns `Directive.id` during reduction.
The host MUST NOT derive a new identifier; it MUST use the agent-assigned value.

> **Normative definition.**
The payload hash is a hash of the directive payload (e.g., SHA-256).
The host MUST compute the payload hash before writing the commit unit.

### Compare-and-commit semantics

> **Normative definition.**
The host MUST use compare-and-commit semantics for all commit units.
The host MUST verify the `expected_revision` matches the current revision before
writing the commit unit.

> **Normative definition.**
The host MUST fence concurrent commit attempts with a monotonically advancing
revision.
If two commit attempts race, only the one with the higher revision succeeds.

> **Normative definition.**
The host MUST reject commit attempts with stale `expected_revision` with
`commit.conflict`.
The host MUST NOT silently overwrite committed data.

> **Normative definition.**
The host MUST support retry logic for transient conflicts.
The host MUST limit the number of retries to prevent infinite loops.

## 2.2 Behavior And Integration

### Outbox state machine

> **Normative definition.**
The host MUST enforce the following outbox state machine:

1. **Pending**: The outbox entry is created and waiting for dispatch.
2. **Leased**: The outbox entry is being dispatched (exclusive lease).
3. **Completed**: The outbox entry has been successfully dispatched.
4. **TerminalFailed**: The outbox entry has failed permanently and will not
   be retried.
5. **Cancelled**: The outbox entry has been cancelled (e.g., by agent lifecycle
   change).
6. **Superseded**: The outbox entry has been superseded by a newer entry with
   the same directive identity.

> **Normative definition.**
The host MUST NOT transition from `Completed`, `TerminalFailed`, `Cancelled`, or
`Superseded` to any other state.

> **Normative definition.**
The host MUST transition from `Pending` to `Leased` when dispatch begins.
The host MUST transition from `Leased` to `Completed` on successful dispatch.
The host MUST transition from `Leased` to `TerminalFailed` on permanent failure.
The host MUST transition from `Pending` or `Leased` to `Cancelled` on cancellation.
The host MUST transition from `Pending` to `Superseded` when a newer entry with
the same directive identity is created.

### Prevent dispatch without commit

> **Normative definition.**
The host MUST NOT dispatch an outbox entry whose originating state transition
did not commit.
The host MUST verify the outbox entry exists in a committed commit unit before
dispatching.

> **Normative definition.**
If a commit unit is rolled back, the host MUST delete the corresponding outbox
entries.
The host MUST NOT leave orphaned outbox entries.

> **Normative definition.**
The host MUST log all outbox entry deletions for audit purposes.

### Ambiguous commit resolution

> **Normative definition.**
If the host crashes or loses network connectivity during a commit, the host MAY
be left in an ambiguous state where it does not know whether the commit
succeeded.
The host MUST resolve ambiguous commits by rereading the durable revision and
directive identities before retrying.

> **Normative definition.**
To resolve an ambiguous commit, the host MUST:

1. Read the current durable revision for the agent.
2. If the current revision is greater than or equal to `next_revision`, the
   commit succeeded. The host MUST NOT retry.
3. If the current revision is less than `expected_revision`, the commit failed.
   The host MUST retry the commit.
4. If the current revision is between `expected_revision` and `next_revision`,
   the commit is ambiguous. The host MUST inspect the journal and outbox for
   the directive identities to determine the outcome.

> **Normative definition.**
If the directive identities are present in the journal and outbox, the commit
succeeded. The host MUST NOT retry.
If the directive identities are not present in the journal and outbox, the
commit failed. The host MUST retry the commit.

> **Normative definition.**
The host MUST log all ambiguous commit resolutions for audit purposes.

## 2.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for atomic state journal
and directive-outbox commits:

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
The host MUST use the following error codes for atomic state journal and
directive-outbox commits:

| Error Code | Description |
|------------|-------------|
| `commit.conflict` | Optimistic concurrency conflict (expected_revision mismatch) |
| `commit.invalid_revision` | next_revision is not expected_revision + 1 |
| `commit.missing_payload_hash` | Outbox entry missing payload hash |
| `commit.unresolved_directive` | Directive identity not determined before commit |
| `commit.orphaned_outbox` | Outbox entry without committed state transition |
| `outbox.attempt_number_exhausted` | attempt_number reached u32::MAX |
| `storage.snapshot.duplicate` | Snapshot ID already exists (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.snapshot.not_found` | Snapshot ID does not exist (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.snapshot.corruption` | Snapshot checksum verification failed (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.journal.modified` | Attempt to modify append-only journal (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.unavailable` | Storage backend unavailable (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome.
The diagnostics MUST include:

1. **Error code**: The specific error code from the table above.
2. **Context**: The operation that failed (e.g., commit write, outbox dispatch).
3. **Entity identifiers**: The tenant ID, agent ID, revision, or entry ID
   involved (without exposing sensitive data).
4. **Timestamp**: The time the error occurred.
5. **Retryable**: Whether the operation can be retried.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:

1. **Storage backend**: The chosen storage backend and its durability guarantees.
2. **Hash algorithm**: The hash algorithm used for payload hashes.
3. **Retry strategy**: The retry strategy for transient conflicts.
4. **Outbox dispatch strategy**: The dispatch strategy (at-least-once, etc.).
5. **Ambiguous commit resolution timeout**: The timeout for ambiguous commit
   resolution.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Outbox retry with backoff**: The retry strategy with exponential backoff.
2. **Outbox deduplication**: The deduplication strategy for outbox entries, using
   `DirectiveTarget.idempotency_key` when provided by the directive.
3. **Outbox compaction**: The compaction strategy for completed outbox entries.
4. **Cross-process fencing**: The fencing token strategy for multi-process
   deployments.
5. **DirectiveTarget.type to DirectiveKindName mapping**: The relationship
   between `DirectiveTarget.type` (Effect, Signal, Timer, Internal) and
   `DirectiveKindName` ("emit", "timer", "effect", "child-lifecycle",
   "approval", "topology") from
   [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 2 MAY invalidate earlier milestone assumptions:

1. **Storage requirements**: If the storage requirements exceed the capacity
   planned in earlier milestones, the capacity plan MUST be revised.
2. **Outbox growth**: If the outbox grows faster than expected, the retention
   policy and storage capacity MUST be revised.
3. **Commit latency**: If commit latency exceeds the turn timeout, the timeout
   or commit strategy MUST be revised.

> **Non-normative note.**
If any result from Phase 2 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Hash algorithm for payload hashes | Use any cryptographically secure hash | SHA-256 or stronger | Must be constant within a deployment |
| Outbox dispatch strategy | Implementation-defined | At-least-once with idempotency | Must prevent dispatch without commit |
| Ambiguous commit resolution timeout | Implementation-defined | Document in conformance profile | Must not block agent turns indefinitely |
| Outbox entry retention | Implementation-defined | Document retention policy | Must preserve audit journal for cancelled/completed agents |
| Commit retry strategy | Implementation-defined | Exponential backoff | Must limit retries and back off |

## 2.4 Phase 2 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 2 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host writes commit units atomically with
   state, journal, outbox, and lifecycle changes.
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

1. **Commit unit write**: Write a commit unit with state, journal, outbox, and
   lifecycle changes and verify all components are written atomically.
2. **Commit unit read**: Read a commit unit by revision and verify all
   components are present and consistent.
3. **Outbox dispatch**: Dispatch an outbox entry and verify the state transitions
   from `Pending` to `Leased` to `Completed`.
4. **Outbox cancellation**: Cancel an outbox entry and verify the state
   transitions from `Pending` to `Cancelled`.
5. **Outbox supersession**: Create a new outbox entry with the same directive
   identity and verify the old entry transitions to `Superseded`.
6. **Lifecycle change**: Update the agent lifecycle state and verify the
   lifecycle change is written atomically.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Malformed commit unit**: Submit a malformed commit unit and verify the
   error code and diagnostic message.
2. **Stale revision**: Submit a commit unit with a stale `expected_revision` and
   verify the `commit.conflict` error code.
3. **Invalid revision**: Submit a commit unit with `next_revision != expected_revision + 1`
   and verify the `commit.invalid_revision` error code.
4. **Missing payload hash**: Submit an outbox entry with a missing payload hash
   and verify the `commit.missing_payload_hash` error code.
5. **Orphaned outbox**: Submit an outbox entry without a corresponding state
   transition and verify the `commit.orphaned_outbox` error code.
6. **Boundary limits**: Submit input that exceeds boundary limits and verify
   the error code.

> **Normative definition.**
Each test MUST verify that the error code and diagnostic message match the
expected values.

### Transient failure recovery tests

> **Normative definition.**
The following tests MUST verify transient failure recovery:

1. **Timeout**: Simulate a timeout during commit unit write and verify the
   operation is aborted and no partial state is left.
2. **Cancellation**: Simulate a cancellation during outbox dispatch and verify
   the operation is aborted and no partial state is left.
3. **Unavailable storage**: Simulate storage backend unavailability and verify
   the operation is retried and eventually succeeds or fails with the correct
   error code.
4. **Retry behavior**: Simulate transient conflicts and verify the retry logic
   works correctly.
5. **Ambiguous commit**: Simulate a crash during commit and verify the host
   resolves the ambiguous commit correctly.

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
The Phase 2 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Commit evidence**: Evidence that commit units are written atomically with
   state, journal, outbox, and lifecycle changes.
3. **Outbox evidence**: Evidence that outbox entries are dispatched correctly
   and state transitions are enforced.
4. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
5. **Recovery evidence**: Evidence that transient failures are recovered from
   correctly.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.
