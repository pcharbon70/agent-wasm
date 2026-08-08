# Phase 2 - Child Lifecycle Cancellation Monitoring And Restart Policy

Back to milestone: [README](./README.md)

- [ ] 2 Phase - Provide explicit host-owned substitutes for actor spawning, monitoring, cancellation propagation, and supervised restart.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 2.1 Section - Contract And Data Model

- [ ] 2.1 Section - Establish contract and data model for child lifecycle cancellation monitoring and restart policy.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.1.1.1 Subtask - Define child-create directives with artifact, manifest, initial state, owner, lifecycle policy, grants, and deterministic request identity.
    - [ ] 2.1.1.2 Subtask - Define accepted, activated, initialized, completed, failed, cancelled, terminated, and orphaned child events.
    - [ ] 2.1.1.3 Subtask - Define cancellation scope, reason, deadline, propagation direction, acknowledgement, and hard-stop behavior.

## 2.2 Section - Behavior And Integration

- [ ] 2.2 Section - Establish behavior and integration for child lifecycle cancellation monitoring and restart policy.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.2.1.1 Subtask - Define monitor subscriptions and durable lifecycle notifications without persisting live monitor handles.
    - [ ] 2.2.1.2 Subtask - Define never, bounded-retry, restart-on-infrastructure-failure, and operator-approved restart policies.
    - [ ] 2.2.1.3 Subtask - Define create/terminate races, parent loss, initialization failure, restart exhaustion, duplicate lifecycle events, and grant revocation.

## 2.3 Section - Failure Evidence And Operational Notes

- [ ] 2.3 Section - Establish failure evidence and operational notes for child lifecycle cancellation monitoring and restart policy.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to child lifecycle cancellation monitoring and restart policy.
    - [ ] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [ ] 2.4 Section - Verify child lifecycle cancellation monitoring and restart policy across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 2.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for child lifecycle cancellation monitoring and restart policy.
    - [ ] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

