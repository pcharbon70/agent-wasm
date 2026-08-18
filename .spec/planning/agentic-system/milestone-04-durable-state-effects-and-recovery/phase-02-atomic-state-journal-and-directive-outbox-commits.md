# Phase 2 - Atomic State Journal And Directive-Outbox Commits

Back to milestone: [README](./README.md)

- [x] 2 Phase - Close the crash gap between accepting a state transition and making its external requests durable.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for atomic state journal and directive-outbox commits.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.1.1.1 Subtask - Specify one commit unit containing expected revision, next snapshot or patch result, journal facts, directive outbox entries, and lifecycle changes.
    - [x] 2.1.1.2 Subtask - Require directive identities and payload hashes to be determined before commit.
    - [x] 2.1.1.3 Subtask - Define compare-and-commit semantics with a monotonically advancing agent revision and fencing token.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for atomic state journal and directive-outbox commits.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.2.1.1 Subtask - Define pending, leased, completed, terminal-failed, cancelled, and superseded outbox states.
    - [x] 2.2.1.2 Subtask - Prevent dispatch of an outbox entry whose originating state transition did not commit.
    - [x] 2.2.1.3 Subtask - Define ambiguous commit resolution by rereading durable revision and directive identities before retrying.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for atomic state journal and directive-outbox commits.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to atomic state journal and directive-outbox commits.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Define integrated verification for atomic state journal and directive-outbox commits across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 2.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for atomic state journal and directive-outbox commits.
    - [x] 2.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

