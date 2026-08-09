# Phase 4 - Retry Timer Recovery Replay Hibernate And Migration

Back to milestone: [README](./README.md)

- [x] 4 Phase - Make delayed work, runtime deactivation, state reconstruction, and schema evolution explicit durable operations.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 4.1 Section - Contract And Data Model

- [ ] 4.1 Section - Establish contract and data model for retry timer recovery replay hibernate and migration.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.1.1.1 Subtask - Define retry classification, bounded attempts, backoff, jitter, deadline, terminal failure, and operator intervention.
    - [ ] 4.1.1.2 Subtask - Persist timers and missed-fire policy independently of live schedulers.
    - [ ] 4.1.1.3 Subtask - Define replay from journal/checkpoint with artifact, schema, policy, and nondeterministic-result references.

## 4.2 Section - Behavior And Integration

- [x] 4.2 Section - Establish behavior and integration for retry timer recovery replay hibernate and migration.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.2.1.1 Subtask - Define hibernate as durable checkpoint plus actor deactivation and thaw as validated activation from durable state.
    - [ ] 4.2.1.2 Subtask - Define migration authorization, source/target schema, artifact compatibility, checkpoint, rollback, and audit records.
    - [ ] 4.2.1.3 Subtask - Define corrupt history, missing artifact, incompatible migration path, expired retry, and duplicate timer recovery.

## 4.3 Section - Failure Evidence And Operational Notes

- [x] 4.3 Section - Establish failure evidence and operational notes for retry timer recovery replay hibernate and migration.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to retry timer recovery replay hibernate and migration.
    - [ ] 4.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 4.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 4.4 Section - Phase 4 Integration Tests

- [x] 4.4 Section - Verify retry timer recovery replay hibernate and migration across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [x] 4.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 4.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for retry timer recovery replay hibernate and migration.
    - [ ] 4.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 4.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 4.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

