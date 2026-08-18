# Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary

Back to milestone: [README](./README.md)

- [x] 1 Phase - Define adversaries, protected assets, authenticated identities, trust zones, and the vocabulary used by every authorization decision.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 1.1 Section - Contract And Data Model

- [x] 1.1 Section - Establish contract and data model for threat model principals trust classes and grant vocabulary.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.1.1.1 Subtask - Identify malicious guest, compromised artifact, hostile input/output, confused deputy, tenant attacker, dependency compromise, operator error, and co-tenant threats.
    - [x] 1.1.1.2 Subtask - Identify host memory, state, secrets, policy, artifacts, audit evidence, external systems, availability, and model context as protected assets.
    - [x] 1.1.1.3 Subtask - Define principal forms for user, service, agent, plugin publisher, operator, effect worker, and external result source.

## 1.2 Section - Behavior And Integration

- [x] 1.2 Section - Establish behavior and integration for threat model principals trust classes and grant vocabulary.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.2.1.1 Subtask - Define untrusted guest, reviewed plugin, privileged host integration, maintenance migration, and operator trust classes.
    - [x] 1.2.1.2 Subtask - Define grants by capability, tenant, resource, purpose, operation, constraints, expiry, and delegating authority.
    - [x] 1.2.1.3 Subtask - Define authentication failure, principal mismatch, grant absence, scope conflict, expiry, revocation, and untrusted-publisher outcomes.

## 1.3 Section - Failure Evidence And Operational Notes

- [x] 1.3 Section - Establish failure evidence and operational notes for threat model principals trust classes and grant vocabulary.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to threat model principals trust classes and grant vocabulary.
    - [x] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 1.4 Section - Phase 1 Integration Tests

- [x] 1.4 Section - Define integrated verification for threat model principals trust classes and grant vocabulary across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 1.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 1.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for threat model principals trust classes and grant vocabulary.
    - [x] 1.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 1.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 1.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

