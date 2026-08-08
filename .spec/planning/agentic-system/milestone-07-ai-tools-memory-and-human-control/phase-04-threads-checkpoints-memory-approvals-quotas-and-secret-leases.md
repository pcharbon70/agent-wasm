# Phase 4 - Threads Checkpoints Memory Approvals Quotas And Secret Leases

Back to milestone: [README](./README.md)

- [ ] 4 Phase - Add durable human-visible history and governed memory without conflating it with authoritative agent state or audit evidence.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 4.1 Section - Contract And Data Model

- [ ] 4.1 Section - Establish contract and data model for threads checkpoints memory approvals quotas and secret leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.1.1.1 Subtask - Define conversation threads, messages, participants, causal links, content references, visibility, redaction, and retention separately from turn journals.
    - [ ] 4.1.1.2 Subtask - Define checkpoints as versioned projections with source revision, schema, artifact, strategy, and validation evidence.
    - [ ] 4.1.1.3 Subtask - Define working, episodic, semantic, and retrieved memory references with provenance, tenant scope, confidence, promotion, and deletion policy.

## 4.2 Section - Behavior And Integration

- [ ] 4.2 Section - Establish behavior and integration for threads checkpoints memory approvals quotas and secret leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.2.1.1 Subtask - Define approval requests, eligible approvers, decision options, expiry, escalation, and causally linked approval-result signals.
    - [ ] 4.2.1.2 Subtask - Define tenant/agent/model/tool quotas and durable reservation, consumption, release, and reconciliation records.
    - [ ] 4.2.1.3 Subtask - Define secret leases by principal, purpose, resource, expiry, non-exportability, audit reference, and revocation behavior.

## 4.3 Section - Failure Evidence And Operational Notes

- [ ] 4.3 Section - Establish failure evidence and operational notes for threads checkpoints memory approvals quotas and secret leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 4.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 4.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to threads checkpoints memory approvals quotas and secret leases.
    - [ ] 4.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 4.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 4.4 Section - Phase 4 Integration Tests

- [ ] 4.4 Section - Verify threads checkpoints memory approvals quotas and secret leases across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 4.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 4.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for threads checkpoints memory approvals quotas and secret leases.
    - [ ] 4.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 4.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 4.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

