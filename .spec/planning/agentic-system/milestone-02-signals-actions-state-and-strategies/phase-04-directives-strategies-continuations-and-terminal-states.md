# Phase 4 - Directives Strategies Continuations And Terminal States

Back to milestone: [README](./README.md)

- [x] 4 Phase - Define external requests and replaceable decision policies without hiding mutable runtime authority in the guest.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 4.1 Section - Contract And Data Model

- [x] 4.1 Section - Establish contract and data model for directives strategies continuations and terminal states.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [x] 4.1.1.1 Subtask - Specify Directive identity, kind, payload schema, requested capability, causal metadata, completion signal, retry class, and result contract.
    - [x] 4.1.1.2 Subtask - Separate internal state operations from emit, timer, effect, child-lifecycle, approval, and topology directives.
    - [x] 4.1.1.3 Subtask - Specify StrategyDescriptor and StrategySnapshot with versioned, bounded, serializable continuation state.

## 4.2 Section - Behavior And Integration

- [x] 4.2 Section - Establish behavior and integration for directives strategies continuations and terminal states.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [x] 4.2.1.1 Subtask - Define direct, FSM, and bounded loop strategy transitions over explicit signal, state, and prior result inputs.
    - [x] 4.2.1.2 Subtask - Define waiting, running, completed, failed, cancelled, and suspended domain states independently of actor activation.
    - [x] 4.2.1.3 Subtask - Define unknown directive, incompatible strategy snapshot, invalid continuation, and terminal-state transition rejection.

## 4.3 Section - Failure Evidence And Operational Notes

- [x] 4.3 Section - Establish failure evidence and operational notes for directives strategies continuations and terminal states.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [x] 4.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to directives strategies continuations and terminal states.
    - [x] 4.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 4.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 4.4 Section - Phase 4 Integration Tests

- [x] 4.4 Section - Verify directives strategies continuations and terminal states across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [x] 4.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 4.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for directives strategies continuations and terminal states.
    - [x] 4.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 4.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 4.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

