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
Each failure point MUST have a corresponding recovery strategy documented in
section 5.2.

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
