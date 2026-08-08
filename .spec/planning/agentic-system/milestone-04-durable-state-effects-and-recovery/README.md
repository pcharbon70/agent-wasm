# Milestone 4 - Durable State, Effects, And Recovery

Make agent state transitions, history, directives, external effects, and activation recoverable across host crashes without claiming impossible exactly-once external behavior.

Current status: planned; all phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for durable state, effects, and recovery.

## Dependencies And Entry Gate

- Milestone 3 can execute and observe a complete in-memory turn.
- Storage remains replaceable behind language-neutral transactional contracts.

## Phase Order

1. [Phase 1 - Revisioned Snapshots Journals History And Storage Contracts](phase-01-revisioned-snapshots-journals-history-and-storage-contracts.md)
2. [Phase 2 - Atomic State Journal And Directive-Outbox Commits](phase-02-atomic-state-journal-and-directive-outbox-commits.md)
3. [Phase 3 - Effect Handlers Attempts Idempotency And Result Signals](phase-03-effect-handlers-attempts-idempotency-and-result-signals.md)
4. [Phase 4 - Retry Timer Recovery Replay Hibernate And Migration](phase-04-retry-timer-recovery-replay-hibernate-and-migration.md)
5. [Phase 5 - Crash Injection Durable Effects And Milestone Acceptance](phase-05-crash-injection-durable-effects-and-milestone-acceptance.md)

## Planned Artifacts

- Transactional state, journal, snapshot, and outbox interfaces
- Effect attempt, result, replay, and migration records
- Crash matrix and durable recovery acceptance corpus

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- Committed directives are delivered at least once.
- Stable idempotency keys bound duplicate risk where targets cooperate.
- Exactly-once state revision is distinct from external-effect delivery.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Revisioned Snapshots Journals History And Storage Contracts](phase-01-revisioned-snapshots-journals-history-and-storage-contracts.md) — implements and verifies this ordered phase.
- [Phase 2 - Atomic State Journal And Directive-Outbox Commits](phase-02-atomic-state-journal-and-directive-outbox-commits.md) — implements and verifies this ordered phase.
- [Phase 3 - Effect Handlers Attempts Idempotency And Result Signals](phase-03-effect-handlers-attempts-idempotency-and-result-signals.md) — implements and verifies this ordered phase.
- [Phase 4 - Retry Timer Recovery Replay Hibernate And Migration](phase-04-retry-timer-recovery-replay-hibernate-and-migration.md) — implements and verifies this ordered phase.
- [Phase 5 - Crash Injection Durable Effects And Milestone Acceptance](phase-05-crash-injection-durable-effects-and-milestone-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
