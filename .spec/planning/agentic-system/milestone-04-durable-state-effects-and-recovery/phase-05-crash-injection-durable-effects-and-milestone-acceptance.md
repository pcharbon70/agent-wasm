# Phase 5 - Crash Injection Durable Effects And Milestone Acceptance

Back to milestone: [README](./README.md)

- [ ] 5 Phase - Prove state/effect invariants at every commit, dispatch, external-success, acknowledgement, and result-ingress boundary.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 5.1 Section - Contract And Data Model

- [ ] 5.1 Section - Establish contract and data model for crash injection durable effects and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 5.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 5.1.1.1 Subtask - Enumerate deterministic failure before invocation, after guest result, before commit, during commit, and after commit.
    - [ ] 5.1.1.2 Subtask - Enumerate failure before dispatch, after lease, after external success, before acknowledgement, and before result-signal enqueue.
    - [ ] 5.1.1.3 Subtask - Assert no directive from an uncommitted turn and no loss of a committed directive.

## 5.2 Section - Behavior And Integration

- [ ] 5.2 Section - Establish behavior and integration for crash injection durable effects and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 5.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 5.2.1.1 Subtask - Assert stable idempotency and explicitly bounded duplicate outcomes after ambiguous external success.
    - [ ] 5.2.1.2 Subtask - Restore snapshots, journals, outbox entries, timers, retries, hibernated agents, and migrations after host restart.
    - [ ] 5.2.1.3 Subtask - Publish the Milestone 4 crash matrix with durable state, allowed outcomes, evidence, and unresolved target-system limits.

## 5.3 Section - Failure Evidence And Operational Notes

- [ ] 5.3 Section - Establish failure evidence and operational notes for crash injection durable effects and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 5.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 5.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to crash injection durable effects and milestone acceptance.
    - [ ] 5.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 5.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 5.4 Section - Phase 5 Integration Tests

- [ ] 5.4 Section - Verify crash injection durable effects and milestone acceptance across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 5.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 5.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for crash injection durable effects and milestone acceptance.
    - [ ] 5.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 5.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 5.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

