# Phase 3 - Effect Handlers Attempts Idempotency And Result Signals

Back to milestone: [README](./README.md)

- [x] 3 Phase - Interpret committed directives through typed handlers while retaining every attempt and returning results as new signals.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 3.1 Section - Contract And Data Model

- [x] 3.1 Section - Establish contract and data model for effect handlers attempts idempotency and result signals.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.1.1.1 Subtask - Define effect-handler registration by directive kind, schema version, trust class, capability, and retry policy.
    - [x] 3.1.1.2 Subtask - Define effect attempt identity, directive identity, lease, handler version, request hash, timestamps, outcome, and external reference.
    - [x] 3.1.1.3 Subtask - Define stable idempotency keys separately from attempt and external provider identities.

## 3.2 Section - Behavior And Integration

- [x] 3.2 Section - Establish behavior and integration for effect handlers attempts idempotency and result signals.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.2.1.1 Subtask - Validate policy and payload again immediately before dispatch and bound response bytes, duration, and diagnostics.
    - [x] 3.2.1.2 Subtask - Translate success, domain failure, infrastructure failure, timeout, cancellation, and approval outcomes into causally linked result signals.
    - [x] 3.2.1.3 Subtask - Define handler crash, lease expiry, late response, duplicate response, conflicting replay, and unsupported idempotency behavior.

## 3.3 Section - Failure Evidence And Operational Notes

- [x] 3.3 Section - Establish failure evidence and operational notes for effect handlers attempts idempotency and result signals.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to effect handlers attempts idempotency and result signals.
    - [x] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 3.4 Section - Phase 3 Integration Tests

- [x] 3.4 Section - Define integrated verification for effect handlers attempts idempotency and result signals across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 3.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 3.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for effect handlers attempts idempotency and result signals.
    - [x] 3.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 3.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 3.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

