# Phase 1 - Evidence Manifests Profiles Runtime Matrices And Traceability

Back to milestone: [README](./README.md)

- [ ] 1 Phase - Define exactly what a passing result means and bind every support claim to reproducible configuration and evidence.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 1.1 Section - Contract And Data Model

- [ ] 1.1 Section - Establish contract and data model for evidence manifests profiles runtime matrices and traceability.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 1.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 1.1.1.1 Subtask - Specify evidence fields for source revision, artifact digest, compiler, PDK, optimizer, Extism SDK/kernel, engine, OS, architecture, features, host protocol, storage, policy, limits, seed, and oracle.
    - [ ] 1.1.1.2 Subtask - Define supported, experimental, excluded, skipped, expected-failure, quarantined, divergent, and conforming dispositions.
    - [ ] 1.1.1.3 Subtask - Define the initial matrix for Extism/Wasmtime and Extism/Wazero across supported host platforms and guest toolchains.

## 1.2 Section - Behavior And Integration

- [ ] 1.2 Section - Establish behavior and integration for evidence manifests profiles runtime matrices and traceability.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 1.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 1.2.1.1 Subtask - Map protocol clauses, invariants, threats, historical defects, and profiles to positive, negative, generated, replayed, and regression cases.
    - [ ] 1.2.1.2 Subtask - Require every aggregate status to expose missing runtime, architecture, feature, and evidence cells.
    - [ ] 1.2.1.3 Subtask - Define evidence retention, artifact access, redaction, expiry, rerun triggers, and release comparison.

## 1.3 Section - Failure Evidence And Operational Notes

- [ ] 1.3 Section - Establish failure evidence and operational notes for evidence manifests profiles runtime matrices and traceability.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 1.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to evidence manifests profiles runtime matrices and traceability.
    - [ ] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 1.4 Section - Phase 1 Integration Tests

- [ ] 1.4 Section - Verify evidence manifests profiles runtime matrices and traceability across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 1.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 1.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for evidence manifests profiles runtime matrices and traceability.
    - [ ] 1.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 1.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 1.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

