# Phase 2 - Core WASI Extism And Plugin Contract Conformance

Back to milestone: [README](./README.md)

- [x] 2 Phase - Layer official standards suites and compiled Extism plugin tests beneath application semantics without confusing their scopes.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.1.1.1 Subtask - Pin and run the official Core WebAssembly suite for each enabled engine feature profile.
    - [x] 2.1.1.2 Subtask - Run only selected WASI suites for guest profiles that actually import those interfaces and preserve skips/expected failures.
    - [x] 2.1.1.3 Subtask - Use WABT and reference/specification interpreters to inspect and adjudicate reduced semantic failures.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.2.1.1 Subtask - Run compiled guest artifacts through XTP for exports, bytes, state, error, mock-host, timeout, and malformed-input contracts.
    - [x] 2.2.1.2 Subtask - Run equivalent native Host SDK integration cases for real callbacks, cancellation, manifests, limits, and lifecycle.
    - [x] 2.2.1.3 Subtask - Promote upstream or project defects into minimized permanent regressions with source and profile provenance.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for core wasi extism and plugin contract conformance.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to core wasi extism and plugin contract conformance.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Define integrated verification for core wasi extism and plugin contract conformance across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 2.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for core wasi extism and plugin contract conformance.
    - [x] 2.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

