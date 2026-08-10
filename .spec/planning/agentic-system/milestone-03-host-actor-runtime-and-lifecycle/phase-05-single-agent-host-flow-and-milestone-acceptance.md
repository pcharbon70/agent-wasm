# Phase 5 - Single-Agent Host Flow And Milestone Acceptance

Back to milestone: [README](./README.md)

- [x] 5 Phase - Connect admission, mailbox, activation, Extism invocation, validation, lifecycle, and observable results in one single-node runtime.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 5.1 Section - Contract And Data Model

- [x] 5.1 Section - Establish contract and data model for single-agent host flow and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 5.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [x] 5.1.1.1 Subtask - Implement the reference flow from authenticated signal through routing, lease, snapshot load, reducer call, result validation, and in-memory commit.
    - [x] 5.1.1.2 Subtask - Return no state change or directive execution after trap, timeout, cancellation, invalid output, stale revision, or policy rejection.
    - [x] 5.1.1.3 Subtask - Exercise direct action, FSM waiting/resume, timer-driven transition, sensor-driven transition, cancellation, and terminal completion.

## 5.2 Section - Behavior And Integration

- [x] 5.2 Section - Establish behavior and integration for single-agent host flow and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 5.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [x] 5.2.1.1 Subtask - Exercise overload, duplicate delivery, expired signal, lease loss, shutdown, reactivation, and initialization failure.
    - [x] 5.2.1.2 Subtask - Record host-owned turn evidence with identities, artifact/profile, limits, revisions, route, result, usage, and failure disposition.
    - [x] 5.2.1.3 Subtask - Define the Milestone 3 exit report and the precise durability gaps intentionally deferred to Milestone 4.

## 5.3 Section - Failure Evidence And Operational Notes

- [x] 5.3 Section - Establish failure evidence and operational notes for single-agent host flow and milestone acceptance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 5.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [x] 5.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to single-agent host flow and milestone acceptance.
    - [x] 5.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 5.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 5.4 Section - Phase 5 Integration Tests

- [x] 5.4 Section - Verify single-agent host flow and milestone acceptance across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [x] 5.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 5.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for single-agent host flow and milestone acceptance.
    - [x] 5.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 5.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 5.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

