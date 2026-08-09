---
title: "Crash Injection Durable Effects And Milestone Acceptance"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-05
  - durable-state
  - crash-injection
  - milestone-acceptance
  - recovery
aliases:
  - "M4-P5 Crash Injection Durable Effects And Milestone Acceptance"
---

# Crash Injection Durable Effects And Milestone Acceptance

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-05-crash-injection-durable-effects-and-milestone-acceptance.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It proves state/effect invariants at every commit, dispatch, external-success,
acknowledgement, and result-ingress boundary.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
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
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).

## 5.1 Contract And Data Model

### Failure enumeration

> **Normative definition.**
The host MUST enumerate deterministic failure points at every durable boundary.
Failure points are categorized by their position relative to the commit
boundary:

1. **Before invocation**: Failure before the Extism guest is invoked.
2. **After guest result**: Failure after the guest returns a result but before
   the result is validated.
3. **Before commit**: Failure after the state transition is computed but before
   the commit is written.
4. **During commit**: Failure while writing the state journal, outbox, and
   related durable records.
5. **After commit**: Failure after the commit is durable but before the turn
   is acknowledged.

> **Normative definition.**
Failure points are also categorized by their position relative to the external
dispatch boundary:

1. **Before dispatch**: Failure before the effect handler is dispatched.
2. **After lease**: Failure after the attempt lease is acquired but before
   the external provider is contacted.
3. **After external success**: Failure after the external provider returns
   success but before the result is acknowledged.
4. **Before acknowledgement**: Failure after the result is validated but before
   the acknowledgement is sent to the external provider.
5. **Before result-signal enqueue**: Failure after the acknowledgement is sent
   but before the result signal is enqueued in the agent's mailbox.

> **Normative definition.**
Recovery strategies are documented in section 5.2. Failure points before an
operation starts (e.g., "before invocation", "before dispatch") have no recovery
strategy because there is nothing to recover from. Failure points after an
operation completes (e.g., "after commit", "after acknowledgement") are handled
by crash recovery on host restart. Failure points during an operation (e.g.,
"before commit", "during commit", "during dispatch") are also handled by crash
recovery, which reconstructs state from the durable store.

### State invariants

> **Normative definition.**
The host MUST maintain the following invariants at every durable boundary:

1. **No uncommitted directive delivery**: No directive from an uncommitted turn
   MAY be delivered to the agent.
2. **No committed directive loss**: Every committed directive MUST be delivered
   to the agent at least once.
3. **State revision monotonicity**: State revisions MUST be monotonically
   increasing.
4. **Outbox completeness**: Every directive that requires external dispatch
   MUST have a corresponding outbox entry before the commit is acknowledged.

> **Normative definition.**
These invariants are enforced by the commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

### Crash recovery data model

> **Normative definition.**
The host MUST persist the following records for crash recovery:

1. **Snapshots**: State snapshots at each committed revision.
2. **Journal entries**: State journal entries for each committed turn.
3. **Outbox entries**: Directive-outbox entries for each committed directive.
4. **Timers**: Timer records for each scheduled timer.
5. **Retries**: Retry records for each retrying directive.
6. **Hibernate records**: Hibernate records for each hibernated agent.
7. **Migration records**: Migration records for each in-progress or completed
   migration.

> **Normative definition.**

```
CrashRecoveryState {
  snapshot_id: SnapshotId,
  journal_revision: u64,
  outbox_entries: OutboxEntry[],
  timers: TimerRecord[],
  retries: RetryRecord[],
  hibernate_records: HibernateRecord[],
  migration_records: MigrationRecord[]
}

SnapshotId = Defined in [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
OutboxEntry = Defined in [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
TimerRecord = Defined in [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).
RetryRecord = Defined in [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).
HibernateRecord = Defined in [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).
MigrationRecord = Defined in [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).
```

> **Normative definition.**
The `CrashRecoveryState` is reconstructed from the durable store on host
restart.
The host MUST verify the consistency of all records before resuming normal
operation.

## 5.2 Behavior And Integration

### Idempotency after ambiguous external success

> **Normative definition.**
After an ambiguous external success (where the host does not know whether the
external provider received the result), the host MUST:

1. **Check idempotency key**: Query the external provider for any existing
   result using the idempotency key.
2. **Return cached result**: If a result exists, return it without re-dispatching.
3. **Cache result**: If no result exists, cache the result locally and mark
   the attempt as `Completed` with `attempt.ambiguous_success_cached`.

> **Normative definition.**
The host MUST NOT re-dispatch an attempt that has already been successfully
processed by the external provider.
The idempotency key MUST be sent with every dispatch to enable the external
provider to detect and reject duplicates.

### Crash recovery behavior

> **Normative definition.**
On host restart, the host MUST perform the following recovery steps:

1. **Load snapshots**: Load the latest valid snapshot from the durable store.
2. **Replay journal**: Replay journal entries from the snapshot revision to
   the latest committed revision.
3. **Restore outbox**: Load all outbox entries that have not been acknowledged.
4. **Restore timers**: Load all timers that have not expired and re-schedule
   them.
5. **Restore retries**: Load all retries that have not expired and re-schedule
   them.
6. **Restore hibernated agents**: Load all hibernated agents and verify their
   hibernate records are valid.
7. **Restore migrations**: Load all in-progress migrations and verify their
   state is consistent.

> **Normative definition.**
Each recovery step MUST be logged with a diagnostic message identifying the
recovered entity and its state.

> **Normative definition.**
If any recovery step fails, the host MUST:

1. Log the failure with the error code and diagnostic message.
2. Mark the affected entity as `Failed` (e.g., `outbox.pending_ack_failed`,
   `timer.recovery_failed`, etc.).
3. Continue recovering other entities.
4. Report all failures to the operator via bounded diagnostics.

### Crash matrix

> **Normative definition.**
The host MUST publish a crash matrix documenting the durable state, allowed
outcomes, and evidence for each failure point enumerated in section 5.1.

> **Normative definition.**
The crash matrix MUST include:

1. **Failure point**: The specific failure point (e.g., "before commit", "after
   external success").
2. **Durable state**: The state of all durable records after the failure.
3. **Allowed outcomes**: The set of outcomes that are allowed after the failure
   (e.g., "retry", "abort", "rollback").
4. **Evidence**: The test evidence that verifies the outcome.
5. **Unresolved limits**: Any limits or open questions that have not been
   resolved.

> **Normative definition.**
The crash matrix is published in the Phase 5 integration test evidence (section
5.4).

## 5.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for crash injection durable
effects and milestone acceptance:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current schema version or
   handler version.
3. **Conflicting**: Multiple writers attempt to write to the same record
   (optimistic concurrency conflict).
4. **Unauthorized**: The caller does not have permission to perform the operation.
5. **Exhausted**: The system is out of resources (e.g., storage capacity, retry
   budget).
6. **Unavailable**: The storage backend is unavailable.
7. **Crash before commit**: The host crashes before the commit is written.
8. **Crash during commit**: The host crashes during the commit write.
9. **Crash after commit**: The host crashes after the commit is written.
10. **Crash before acknowledgement**: The host crashes before acknowledging
    external success.
11. **Crash after acknowledgement**: The host crashes after acknowledging
    external success.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for crash injection durable effects
and milestone acceptance:

| Error Code | Description |
|------------|-------------|
| `commit.before_failure` | Host crash before commit |
| `commit.during_failure` | Host crash during commit |
| `commit.after_failure` | Host crash after commit |
| `dispatch.before_failure` | Host crash before dispatch |
| `dispatch.after_lease_failure` | Host crash after lease acquisition |
| `dispatch.after_external_success_failure` | Host crash after external success |
| `dispatch.before_ack_failure` | Host crash before acknowledgement |
| `dispatch.after_ack_failure` | Host crash after acknowledgement |
| `attempt.timeout` | Attempt dispatch timed out |
| `attempt.max_retries_exceeded` | Maximum retry attempts exceeded |
| `attempt.conflicting_replay` | Replayed attempt produced different result |
| `recovery.snapshot_invalid` | Snapshot is invalid or corrupt |
| `recovery.journal_gap` | Journal has gaps that cannot be recovered |
| `recovery.outbox_inconsistent` | Outbox entries are inconsistent with state |
| `recovery.timer_expired` | Timer expired during recovery |
| `recovery.retry_expired` | Retry expired during recovery |
| `recovery.hibernate_invalid` | Hibernate record is invalid |
| `recovery.migration_incomplete` | Migration is incomplete |
| `storage.snapshot.duplicate` | Snapshot ID already exists (see
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.unavailable` | Storage backend unavailable (see
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `commit.conflict` | Optimistic concurrency conflict (see
  [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)) |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome.
The diagnostics MUST include:

1. **Error code**: The specific error code from the table above.
2. **Context**: The operation that failed (e.g., commit, dispatch, recovery).
3. **Entity identifiers**: The tenant ID, agent ID, or record ID involved
   (without exposing sensitive data).
4. **Timestamp**: The time the error occurred.
5. **Retryable**: Whether the operation can be retried.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:

1. **Crash injection framework**: The framework used for crash injection testing.
2. **Recovery timeout**: The maximum time allowed for crash recovery.
3. **Outbox ack retry policy**: The retry policy for outbox acknowledgement.
4. **Snapshot frequency**: The frequency of snapshot creation.
5. **Journal compaction**: The strategy for journal compaction.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Crash injection automation**: Automated crash injection testing.
2. **Recovery metrics**: Metrics for crash recovery performance.
3. **Crash matrix automation**: Automated crash matrix generation.
4. **Milestone acceptance automation**: Automated milestone acceptance testing.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 5 MAY invalidate earlier milestone assumptions:

1. **Storage capacity**: If the storage capacity for crash recovery exceeds the
   capacity planned in earlier milestones, the capacity plan MUST be revised.
2. **Recovery time**: If the recovery time exceeds the turn timeout, the timeout
   or recovery strategy MUST be revised.
3. **Outbox size**: If the outbox size exceeds the capacity planned in earlier
   milestones, the capacity plan MUST be revised.

> **Non-normative note.**
If any result from Phase 5 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Crash injection framework | Implementation-defined | Document in conformance profile | Must support deterministic failure injection |
| Recovery timeout | Implementation-defined | Document in conformance profile | Must not exceed turn timeout |
| Outbox ack retry policy | Implementation-defined | Document in conformance profile | Must be bounded |
| Snapshot frequency | Implementation-defined | Document in conformance profile | Must balance durability and performance |
| Journal compaction | Implementation-defined | Document in conformance profile | Must preserve audit trail |
| Backoff strategy | Implementation-defined | Exponential backoff | Must be bounded |

## 5.4 Phase 5 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 5 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host handles commits, dispatches, external
   successes, acknowledgements, and result ingestion successfully.
2. **Crash durability**: The host persists durable state correctly across crashes
   at every enumerated failure point (before/during/after commit, dispatch,
   acknowledgement).
3. **Recovery completeness**: The host recovers all durable records (snapshots,
   journals, outbox, timers, retries, hibernated agents, migrations) correctly
   after a crash.
4. **Cross-milestone compatibility**: The phase does not introduce regressions
   in earlier milestones.

> **Normative definition.**
Each integration test MUST exercise observable contracts rather than private
implementation structure.

### Successful flow tests

> **Normative definition.**
The following tests MUST verify the canonical successful flow:

1. **Commit success**: Commit a turn and verify the state journal, outbox, and
   related records are durable.
2. **Dispatch success**: Dispatch an effect and verify the attempt state
   transitions from `Pending` to `InProgress` to `Completed`.
3. **External success**: Receive external success and verify the result is
   acknowledged and cached.
4. **Acknowledgement success**: Send acknowledgement and verify the outbox
   entry is marked as acknowledged.
5. **Result ingestion**: Ingest a result signal and verify the agent's mailbox
   is updated.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Commit before crash**: Simulate a crash before commit and verify no state
   is persisted.
2. **Commit during crash**: Simulate a crash during commit and verify the
   state is recovered correctly.
3. **Commit after crash**: Simulate a crash after commit and verify the state
   is durable.
4. **Dispatch before crash**: Simulate a crash before dispatch and verify no
   attempt is created.
5. **Dispatch after lease crash**: Simulate a crash after lease acquisition and
   verify the lease is released.
6. **External success ambiguity**: Simulate an ambiguous external success and
   verify the result is cached and not re-dispatched.
7. **Acknowledgement before crash**: Simulate a crash before acknowledgement and
   verify the outbox entry is retried.
8. **Acknowledgement after crash**: Simulate a crash after acknowledgement and
   verify the outbox entry is marked as acknowledged.

> **Normative definition.**
Each test MUST verify that the error code and diagnostic message match the
expected values.

### Recovery after transient failure tests

> **Normative definition.**
The following tests MUST verify recovery after transient failures (simulating
a crash during the transient failure):

1. **Retry timeout with crash**: Simulate a retry timeout followed by a host
   crash, then verify on restart that the attempt is marked as `Failed` with
   `attempt.timeout` and no partial state remains.
2. **Retry cancellation with crash**: Simulate a retry cancellation followed by
   a host crash, then verify on restart that the attempt is marked as `Cancelled`
   and no partial state remains.
3. **Storage unavailable with crash**: Simulate a storage unavailability followed
   by a host crash, then verify on restart that the operation is marked as
   `Failed` with `storage.unavailable` and no partial state remains.
4. **Timer missed fire with crash**: Simulate a timer missed fire followed by a
   host crash, then verify on restart that the missed-fire policy is applied
   and no partial state remains.

> **Normative definition.**
Each test MUST verify that no unauthorized or partial state is left after the
failure.

### Cross-milestone compatibility tests

> **Normative definition.**
The following tests MUST verify cross-milestone compatibility:

1. **Milestone 1 fixtures**: Run all Milestone 1 fixtures and verify no
   regressions. Milestone 1 fixtures are defined in
   [Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md).
2. **Milestone 2 fixtures**: Run all Milestone 2 fixtures and verify no
   regressions. Milestone 2 fixtures are defined in the Phase 1-5 plans under
   [Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/).
3. **Milestone 3 fixtures**: Run all Milestone 3 fixtures and verify no
   regressions. Milestone 3 fixtures are defined in the Phase 1-5 plans under
   [Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/).
4. **Milestone 4 phase 1-4 fixtures**: Run all Milestone 4 phase 1-4 fixtures
   and verify no regressions. Milestone 4 phase 1-4 fixtures are defined in
   the Phase 1-5 plans under
   [Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/).

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 5 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Commit durability evidence**: Evidence that commits are durable across
   crashes.
3. **Dispatch durability evidence**: Evidence that dispatches are durable across
   crashes.
4. **Recovery evidence**: Evidence that crash recovery restores all durable
   records correctly.
5. **Idempotency evidence**: Evidence that ambiguous external successes do not
   cause duplicate dispatches.
6. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
7. **Crash matrix**: The published crash matrix with durable state, allowed
   outcomes, evidence, and unresolved target-system limits.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.
