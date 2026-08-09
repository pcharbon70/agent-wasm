---
title: "Retry Timer Recovery Replay Hibernate And Migration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-04
  - durable-state
  - retry
  - timer
  - recovery
  - replay
  - hibernate
  - migration
aliases:
  - "M4-P4 Retry Timer Recovery Replay Hibernate And Migration"
---

# Retry Timer Recovery Replay Hibernate And Migration

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-04-retry-timer-recovery-replay-hibernate-and-migration.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It makes delayed work, runtime deactivation, state reconstruction, and schema
evolution explicit durable operations.

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
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

## 4.1 Contract And Data Model

### Retry classification

> **Normative definition.**
A retry is a durable operation that re-attempts a failed directive dispatch
after a bounded number of attempts with exponential backoff and jitter.
The host MUST classify retries into the following categories:

1. **Transient**: The failure is likely to resolve on retry (e.g., network error).
2. **Permanent**: The failure will not resolve on retry (e.g., invalid payload).
3. **Operator-intervention**: The failure requires human intervention (e.g.,
   approval timeout).

> **Normative definition.**

```
RetryRecord {
  attempt_id: AttemptId,
  tenant_id: TenantId,
  agent_id: AgentId,
  retry_number: u32,
  max_retries: u32,
  backoff_ms: u64,
  jitter_ms: u64,
  next_retry_at: UnixTimestamp,
  deadline: UnixTimestamp?,
  classification: RetryClassification,
  state: RetryState,
  metadata: JsonObject
}

RetryClassification = Transient | Permanent | OperatorIntervention
RetryState = Pending | InProgress | Completed | Failed | Cancelled | Expired | TerminalFailed
```

`AttemptId`, `TenantId`, and `AgentId` are defined in
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `attempt_id` | AttemptId | Yes | Attempt this retry is for |
| `tenant_id` | TenantId | Yes | Tenant this retry belongs to |
| `agent_id` | AgentId | Yes | Agent this retry belongs to |
| `retry_number` | u32 | Yes | Current retry number (starts at 1) |
| `max_retries` | u32 | Yes | Maximum number of retries |
| `backoff_ms` | u64 | Yes | Base backoff duration in milliseconds |
| `jitter_ms` | u64 | Yes | Additional random jitter in milliseconds |
| `next_retry_at` | UnixTimestamp | Yes | Next retry time |
| `deadline` | UnixTimestamp? | No | Deadline for all retries (null if no deadline) |
| `classification` | RetryClassification | Yes | Retry classification |
| `state` | RetryState | Yes | Current retry state |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `retry_number` field represents the count of attempts including the one in
progress. The host MUST increment `retry_number` before dispatching each attempt.
The host MUST NOT dispatch an attempt if `retry_number` would exceed `max_retries`.
If `retry_number` reaches `max_retries` and the attempt fails, the host MUST
mark the retry as `TerminalFailed` with `retry.max_retries_exceeded`.

> **Normative definition.**
The `next_retry_at` field is computed as
`current_time + backoff_ms * 2^(retry_number - 1) + random(jitter_ms)`.
The host MUST use the computed `next_retry_at` for scheduling retries.
This gives a base delay of `backoff_ms` for the first retry, `2 * backoff_ms` for
the second, and so on, with up to `jitter_ms` milliseconds of additional random
jitter applied to each delay.

> **Normative definition.**
The `deadline` field is optional.
If set, the host MUST mark all pending retries for the attempt as `Expired`
with `retry.deadline_exceeded` when the deadline passes.

### Timer persistence

> **Normative definition.**
A timer is a durable record of a delayed signal that the host MUST fire at a
specific time.
The host MUST persist timers independently of live schedulers.
If the host crashes, the host MUST recover timers from the durable store on
restart.

> **Normative definition.**

```
TimerRecord {
  timer_id: TimerId,
  tenant_id: TenantId,
  agent_id: AgentId,
  signal: SignalEnvelope,
  fire_at: UnixTimestamp,
  repeat_interval: u64?,
  repeat_count: u32?,
  state: TimerState,
  metadata: JsonObject
}

TimerId = string
SignalEnvelope = Defined in [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
TimerState = Pending | InProgress | Fired | Cancelled | Expired | MissedFire
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `timer_id` | TimerId | Yes | Unique timer identifier |
| `tenant_id` | TenantId | Yes | Tenant this timer belongs to |
| `agent_id` | AgentId | Yes | Agent this timer belongs to |
| `signal` | SignalEnvelope | Yes | Signal to fire |
| `fire_at` | UnixTimestamp | Yes | Time to fire the timer |
| `repeat_interval` | u64? | No | Repeat interval in milliseconds (null if one-shot) |
| `repeat_count` | u32? | No | Number of repeats (null if unlimited) |
| `state` | TimerState | Yes | Current timer state |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST persist timers atomically with the commit unit that created them.
If a commit unit is rolled back, the host MUST delete the corresponding timers.

> **Normative definition.**
The host MUST recover timers from the durable store on restart.
The host MUST fire timers that have not yet fired and have not expired.
The host MUST mark timers that have expired as `Expired` with `timer.expired`.

### Missed-fire policy

> **Normative definition.**
The host MUST define a missed-fire policy for timers that fail to fire at the
scheduled time.
The host MUST support the following missed-fire policies:

1. **Fire immediately**: Fire the timer as soon as possible after the host
   restarts.
2. **Skip**: Skip the timer and do not fire it.
3. **Retry**: Retry the timer according to the retry policy.

> **Normative definition.**
The missed-fire policy is configured per timer and is stored in the `metadata`
field of the `TimerRecord`.

> **Normative definition.**
The host MUST mark a timer as `MissedFire` with `timer.missed_fire` when the
timer's `fire_at` time has passed and the timer has not been fired within a
reasonable grace period. The grace period is implementation-defined but MUST
be documented in the conformance profile. The host MUST then apply the
missed-fire policy (fire immediately, skip, or retry) based on the timer's
configuration.

### Replay

> **Normative definition.**
Replay is the process of reconstructing agent state from the journal and
snapshots.
The host MUST support replay from the journal/checkpoint with artifact, schema,
policy, and nondeterministic-result references.

> **Normative definition.**

```
ReplayRecord {
  replay_id: ReplayId,
  tenant_id: TenantId,
  agent_id: AgentId,
  start_revision: u64,
  end_revision: u64,
  artifact_version: string,
  state_schema_version: string,
  policy_version: string,
  state: ReplayState,
  nondeterministic_results: NondeterministicResult[],
  metadata: JsonObject
}

ReplayId = string
ReplayState = Pending | InProgress | Completed | Failed
NondeterministicResult {
  revision: u64,
  result_hash: Bytes,
  reference: String?
}
```

`TenantId`, `AgentId`, and `u64` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `replay_id` | ReplayId | Yes | Unique replay identifier |
| `tenant_id` | TenantId | Yes | Tenant this replay belongs to |
| `agent_id` | AgentId | Yes | Agent this replay belongs to |
| `start_revision` | u64 | Yes | Start revision for the replay |
| `end_revision` | u64 | Yes | End revision for the replay |
| `artifact_version` | string | Yes | Artifact version used for the replay |
| `state_schema_version` | string | Yes | State schema version used for the replay |
| `policy_version` | string | Yes | Policy version used for the replay |
| `state` | ReplayState | Yes | Current replay state |
| `nondeterministic_results` | NondeterministicResult[] | Yes (empty list allowed) | Nondeterministic results from the replay (empty if all results were deterministic) |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST replay the journal from `start_revision` to `end_revision`.
The host MUST reconstruct the agent state at `end_revision`.
The host MUST verify the reconstructed state matches the snapshot at
`end_revision` (if available).

> **Normative definition.**
The `nondeterministic_results` field records results that are nondeterministic
(e.g., random numbers, timestamps).
The host MUST reference the original nondeterministic results for replay
consistency.

## 4.2 Behavior And Integration

### Hibernate and thaw

> **Normative definition.**
Hibernate is the process of deactivating an agent's runtime actor while
preserving its durable state.
Thaw is the process of reactivating an agent's runtime actor from its
durable state.

> **Normative definition.**

```
HibernateRecord {
  hibernate_id: HibernateId,
  tenant_id: TenantId,
  agent_id: AgentId,
  state_snapshot_id: SnapshotId,
  journal_checkpoint: u64,
  state: HibernateState,
  metadata: JsonObject
}

HibernateId = string
SnapshotId = Defined in [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
HibernateState = Pending | InProgress | Completed | Failed | Thawed
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `hibernate_id` | HibernateId | Yes | Unique hibernate record identifier |
| `tenant_id` | TenantId | Yes | Tenant this hibernate record belongs to |
| `agent_id` | AgentId | Yes | Agent this hibernate record belongs to |
| `state_snapshot_id` | SnapshotId | Yes | Snapshot ID for the hibernated state |
| `journal_checkpoint` | u64 | Yes | Journal checkpoint for the hibernated state |
| `state` | HibernateState | Yes | Current hibernate state |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST create a snapshot and journal checkpoint before deactivating the
agent's runtime actor.
The host MUST verify the snapshot and journal checkpoint are durable before
deactivating the runtime actor.

> **Normative definition.**
The host MUST reactivate the agent's runtime actor from the snapshot and
journal checkpoint.
The host MUST verify the snapshot and journal checkpoint are valid before
reactivating the runtime actor.

### Migration authorization

> **Normative definition.**
Migration is the process of evolving an agent's state schema or artifact
version.
The host MUST require migration authorization before performing migration.

> **Normative definition.**

```
MigrationRecord {
  migration_id: MigrationId,
  tenant_id: TenantId,
  agent_id: AgentId,
  source_schema_version: string,
  target_schema_version: string,
  source_artifact_version: string,
  target_artifact_version: string,
  authorization: MigrationAuthorization,
  state: MigrationState,
  checkpoint_snapshot_id: SnapshotId?,
  rollback_snapshot_id: SnapshotId?,
  metadata: JsonObject
}

MigrationId = string
MigrationAuthorization = OperatorApproved | Automated
MigrationState = Pending | InProgress | Completed | Failed | RolledBack
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `migration_id` | MigrationId | Yes | Unique migration record identifier |
| `tenant_id` | TenantId | Yes | Tenant this migration record belongs to |
| `agent_id` | AgentId | Yes | Agent this migration record belongs to |
| `source_schema_version` | string | Yes | Source state schema version |
| `target_schema_version` | string | Yes | Target state schema version |
| `source_artifact_version` | string | Yes | Source artifact version |
| `target_artifact_version` | string | Yes | Target artifact version |
| `authorization` | MigrationAuthorization | Yes | Migration authorization |
| `state` | MigrationState | Yes | Current migration state |
| `checkpoint_snapshot_id` | SnapshotId? | No | Snapshot ID for the migration checkpoint |
| `rollback_snapshot_id` | SnapshotId? | No | Snapshot ID for the migration rollback |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST verify migration authorization before performing migration.
Operator-approved migrations require explicit human approval.
Automated migrations require the migration path to be pre-approved.

> **Normative definition.**
The host MUST create a checkpoint snapshot before migration.
The host MUST store the checkpoint snapshot ID in the `checkpoint_snapshot_id`
field.

> **Normative definition.**
The host MUST create a rollback snapshot before migration.
The host MUST store the rollback snapshot ID in the `rollback_snapshot_id`
field.

### Audit records

> **Normative definition.**
The host MUST emit an audit record for every migration event.
Audit records MUST include:

1. `migration_id`: The migration record ID.
2. `event_type`: The migration event type (e.g., `authorization`, `checkpoint`,
   `completed`, `rolled_back`).
3. `actor_id`: The ID of the actor that performed the event.
4. `timestamp`: The time the event occurred.
5. `details`: Additional event details.

> **Normative definition.**
The host MUST retain audit records for the lifetime of the migration record.
Audit records MUST NOT be mutable after creation.

### Recovery from failure

> **Normative definition.**
The host MUST define recovery behavior for the following failure scenarios:

1. **Corrupt history**: If the journal is corrupt, the host MUST reconstruct
   state from the nearest valid snapshot and replay valid journal entries.
2. **Missing artifact**: If the artifact is missing, the host MUST reject
   the operation with `artifact.missing`.
3. **Incompatible migration path**: If the migration path is incompatible,
   the host MUST reject the migration with `migration.incompatible_path`.
4. **Expired retry**: If a retry's `next_retry_at` has passed and the retry has
   not been attempted within a reasonable grace period, the host MUST mark the
   retry as `Expired` with `retry.expired`. This applies when the retry scheduler
   has not dispatched the retry within a tolerance window after `next_retry_at`.
5. **Duplicate timer**: If a duplicate timer is detected, the host MUST
   reject the duplicate with `timer.duplicate`.

> **Normative definition.**
Each recovery action MUST be accompanied by an audit record.
Recovery actions MUST NOT leave partial or unauthorized state.

## 4.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for retry, timer, recovery,
replay, hibernate, and migration:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current schema version or
   handler version.
3. **Conflicting**: Multiple writers attempt to write to the same record
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
The host MUST use the following error codes for retry, timer, recovery, replay,
hibernate, and migration:

| Error Code | Description |
|------------|-------------|
| `retry.max_retries_exceeded` | Maximum retry attempts exceeded |
| `retry.deadline_exceeded` | Retry deadline exceeded |
| `retry.expired` | Retry expired |
| `retry.timeout` | Retry dispatch timed out |
| `timer.expired` | Timer expired |
| `timer.duplicate` | Duplicate timer detected |
| `timer.missed_fire` | Timer missed scheduled fire time |
| `replay.conflicting_result` | Replayed result conflicts with original |
| `replay.snapshot_mismatch` | Reconstructed state does not match snapshot |
| `hibernate.checkpoint_failed` | Hibernate checkpoint creation failed |
| `hibernate.thaw_failed` | Thaw activation failed |
| `migration.authorization_required` | Migration requires operator approval |
| `migration.incompatible_path` | Migration path is incompatible |
| `migration.checkpoint_failed` | Migration checkpoint creation failed |
| `migration.rollback_failed` | Migration rollback failed |
| `artifact.missing` | Required artifact is missing |
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
2. **Context**: The operation that failed (e.g., retry dispatch, timer fire,
   replay, hibernate, migration).
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

1. **Retry default policy**: The default retry policy for retries.
2. **Missed-fire default policy**: The default missed-fire policy for timers.
3. **Hibernate timeout**: The maximum time allowed for hibernate operations.
4. **Thaw timeout**: The maximum time allowed for thaw operations.
5. **Migration timeout**: The maximum time allowed for migration operations.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Migration strategy**: The migration strategy (canary, blue-green, etc.).
2. **Hibernate persistence**: The hibernate persistence strategy.
3. **Replay optimization**: The replay optimization strategy.
4. **Retry metrics**: The retry metrics and monitoring.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 4 MAY invalidate earlier milestone assumptions:

1. **Storage capacity**: If the storage capacity for retries, timers, and
   migrations exceeds the capacity planned in earlier milestones, the capacity
   plan MUST be revised.
2. **Retry budget**: If the retry budget exceeds the turn timeout, the timeout
   or retry policy MUST be revised.
3. **Migration complexity**: If migration complexity exceeds the complexity
   planned in earlier milestones, the complexity plan MUST be revised.

> **Non-normative note.**
If any result from Phase 4 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## 4.4 Phase 4 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 4 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host handles retries, timers, recovery,
   replay, hibernate, and migration successfully.
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

1. **Retry classification**: Classify a retry as transient, permanent, or
   operator-intervention and verify the classification.
2. **Retry dispatch**: Dispatch a retry and verify the attempt state transitions
   from `Pending` to `InProgress` to `Completed`.
3. **Timer creation**: Create a timer and verify the timer is persisted.
4. **Timer fire**: Fire a timer and verify the signal is delivered.
5. **Replay**: Replay a journal and verify the reconstructed state matches the
   snapshot.
6. **Hibernate**: Hibernate an agent and verify the state is preserved.
7. **Thaw**: Thaw an agent and verify the state is restored.
8. **Migration**: Migrate an agent and verify the migration is completed.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Retry max retries exceeded**: Attempt to exceed the maximum retry attempts
   and verify the `retry.max_retries_exceeded` error code.
2. **Retry deadline exceeded**: Attempt to exceed the retry deadline and verify
   the `retry.deadline_exceeded` error code.
3. **Timer expired**: Attempt to fire an expired timer and verify the
   `timer.expired` error code.
4. **Timer duplicate**: Attempt to create a duplicate timer and verify the
   `timer.duplicate` error code.
5. **Replay conflicting result**: Attempt a conflicting replay and verify the
   `replay.conflicting_result` error code.
6. **Hibernate checkpoint failed**: Simulate a hibernate checkpoint failure and
   verify the `hibernate.checkpoint_failed` error code.
7. **Thaw failed**: Simulate a thaw failure and verify the `hibernate.thaw_failed`
   error code.
8. **Migration authorization required**: Attempt a migration without
   authorization and verify the `migration.authorization_required` error code.
9. **Migration incompatible path**: Attempt a migration with an incompatible
   path and verify the `migration.incompatible_path` error code.
10. **Artifact missing**: Attempt an operation with a missing artifact and verify
    the `artifact.missing` error code.

> **Normative definition.**
Each test MUST verify that the error code and diagnostic message match the
expected values.

### Transient failure recovery tests

> **Normative definition.**
The following tests MUST verify transient failure recovery:

1. **Retry timeout**: Simulate a retry timeout and verify the attempt is marked
   as `Failed` with `retry.timeout`.
2. **Retry cancellation**: Simulate a retry cancellation and verify the attempt
   is marked as `Cancelled`.
3. **Storage unavailable**: Simulate a storage unavailability and verify the
   operation is marked as `Failed` with `storage.unavailable`.
4. **Timer missed fire**: Simulate a timer missed fire and verify the missed-fire
   policy is applied.

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

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 4 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Retry evidence**: Evidence that retries are classified and dispatched
   correctly.
3. **Timer evidence**: Evidence that timers are created, fired, and recovered
   correctly.
4. **Replay evidence**: Evidence that replay reconstructs state correctly.
5. **Hibernate evidence**: Evidence that hibernate preserves state correctly.
6. **Thaw evidence**: Evidence that thaw restores state correctly.
7. **Migration evidence**: Evidence that migration is authorized and completed
   correctly.
8. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
9. **Recovery evidence**: Evidence that transient failures are recovered from
   correctly.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Retry default policy | Implementation-defined | Document in conformance profile | Must not exceed turn timeout |
| Missed-fire default policy | Implementation-defined | Document in conformance profile | Must be one of fire_immediately, skip, retry |
| Hibernate timeout | Implementation-defined | Document in conformance profile | Must be bounded |
| Thaw timeout | Implementation-defined | Document in conformance profile | Must be bounded |
| Migration timeout | Implementation-defined | Document in conformance profile | Must be bounded |
| Backoff strategy | Implementation-defined | Exponential backoff | Must be bounded |
| State schema versioning | Implementation-defined | Document in conformance profile | Must support migration |
| Artifact versioning | Implementation-defined | Document in conformance profile | Must support migration |
