# Phase 2 - Capability Policy Attenuation Limits And Enforcement

Back to milestone: [README](./README.md)

- [ ] 2 Phase - Create host-owned policy decisions that bind every invocation and effect to minimum authority and resource budgets.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 2.1 Section - Contract And Data Model

- [ ] 2.1 Section - Establish contract and data model for capability policy attenuation limits and enforcement.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.1.1.1 Subtask - Define policy input from principal, tenant, agent, artifact, plugin, purpose, signal, requested capability, resource, and runtime context.
    - [ ] 2.1.1.2 Subtask - Define allow, deny, approval-required, attenuated, and unavailable decisions with stable reason identifiers.
    - [ ] 2.1.1.3 Subtask - Define attenuation for paths, origins, methods, models, tools, record sets, byte counts, durations, and invocation budgets.

## 2.2 Section - Behavior And Integration

- [ ] 2.2 Section - Establish behavior and integration for capability policy attenuation limits and enforcement.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.2.1.1 Subtask - Bind granted capabilities and limits into TurnRequest while retaining independent host enforcement.
    - [ ] 2.2.1.2 Subtask - Recheck policy at signal admission, action resolution, guest invocation, directive validation, effect dispatch, and result admission.
    - [ ] 2.2.1.3 Subtask - Define revocation, policy-version change, cached decision expiry, quota exhaustion, and partial dependency failure.

## 2.3 Section - Failure Evidence And Operational Notes

- [ ] 2.3 Section - Establish failure evidence and operational notes for capability policy attenuation limits and enforcement.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to capability policy attenuation limits and enforcement.
    - [ ] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [ ] 2.4 Section - Verify capability policy attenuation limits and enforcement across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 2.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for capability policy attenuation limits and enforcement.
    - [ ] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

