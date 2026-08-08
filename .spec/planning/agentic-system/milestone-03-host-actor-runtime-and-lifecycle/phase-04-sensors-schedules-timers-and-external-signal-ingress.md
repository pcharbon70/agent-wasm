# Phase 4 - Sensors Schedules Timers And External Signal Ingress

Back to milestone: [README](./README.md)

- [ ] 4 Phase - Convert external events and time into validated signals without granting event sources direct access to agent state.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 4.1 Section - Contract And Data Model

- [ ] 4.1 Section - Establish contract and data model for sensors schedules timers and external signal ingress.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.1.1.1 Subtask - Define SensorDescriptor identity, source configuration reference, emitted signal schemas, grants, lifecycle, and checkpoint data.
    - [ ] 4.1.1.2 Subtask - Define schedule expressions, timezone policy, misfire behavior, jitter, next-fire calculation, and cancellation.
    - [ ] 4.1.1.3 Subtask - Define durable timer directives with stable identity, due time, completion policy, and causation.

## 4.2 Section - Behavior And Integration

- [ ] 4.2 Section - Establish behavior and integration for sensors schedules timers and external signal ingress.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.2.1.1 Subtask - Normalize sensor events, timer fires, user requests, and transport deliveries through one signal admission boundary.
    - [ ] 4.2.1.2 Subtask - Define source authentication, tenant/agent resolution, schema validation, deduplication, and mailbox admission order.
    - [ ] 4.2.1.3 Subtask - Define skipped, coalesced, replayed, late, duplicate, disabled, and failed-source outcomes.

## 4.3 Section - Failure Evidence And Operational Notes

- [ ] 4.3 Section - Establish failure evidence and operational notes for sensors schedules timers and external signal ingress.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to sensors schedules timers and external signal ingress.
    - [ ] 4.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 4.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 4.4 Section - Phase 4 Integration Tests

- [ ] 4.4 Section - Verify sensors schedules timers and external signal ingress across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 4.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 4.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for sensors schedules timers and external signal ingress.
    - [ ] 4.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 4.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 4.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

