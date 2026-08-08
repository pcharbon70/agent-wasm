# Phase 2 - Core WASI Extism And Plugin Contract Conformance

Back to milestone: [README](./README.md)

- [ ] 2 Phase - Layer official standards suites and compiled Extism plugin tests beneath application semantics without confusing their scopes.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 2.1 Section - Contract And Data Model

- [ ] 2.1 Section - Establish contract and data model for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.1.1.1 Subtask - Pin and run the official Core WebAssembly suite for each enabled engine feature profile.
    - [ ] 2.1.1.2 Subtask - Run only selected WASI suites for guest profiles that actually import those interfaces and preserve skips/expected failures.
    - [ ] 2.1.1.3 Subtask - Use WABT and reference/specification interpreters to inspect and adjudicate reduced semantic failures.

## 2.2 Section - Behavior And Integration

- [ ] 2.2 Section - Establish behavior and integration for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.2.1.1 Subtask - Run compiled guest artifacts through XTP for exports, bytes, state, error, mock-host, timeout, and malformed-input contracts.
    - [ ] 2.2.1.2 Subtask - Run equivalent native Host SDK integration cases for real callbacks, cancellation, manifests, limits, and lifecycle.
    - [ ] 2.2.1.3 Subtask - Promote upstream or project defects into minimized permanent regressions with source and profile provenance.

## 2.3 Section - Failure Evidence And Operational Notes

- [ ] 2.3 Section - Establish failure evidence and operational notes for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to core wasi extism and plugin contract conformance.
    - [ ] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [ ] 2.4 Section - Verify core wasi extism and plugin contract conformance across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 2.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for core wasi extism and plugin contract conformance.
    - [ ] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

