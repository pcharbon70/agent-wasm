# Phase 1 - Profile Vocabulary And Architectural Boundaries

Back to milestone: [README](./README.md)

- [x] 1 Phase - Freeze the shared terminology, responsibility split, and supported bootstrap profile before defining wire contracts.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 1.1 Section - Contract And Data Model

- [x] 1.1 Section - Establish contract and data model for profile vocabulary and architectural boundaries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.1.1.1 Subtask - Define host, engine, Extism runtime, plug-in, agent, action, strategy, directive, signal, effect, and artifact terms.
    - [x] 1.1.1.2 Subtask - Assign state, policy, scheduling, effects, topology, and evidence ownership to the host.
    - [x] 1.1.1.3 Subtask - Assign deterministic decision behavior and disposable scratch state to the guest.

## 1.2 Section - Behavior And Integration

- [x] 1.2 Section - Establish behavior and integration for profile vocabulary and architectural boundaries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.2.1.1 Subtask - Pin the initial Core WebAssembly feature set and record every excluded proposal.
    - [x] 1.2.1.2 Subtask - Declare whether each guest profile imports no WASI or an explicit selected WASI surface.
    - [x] 1.2.1.3 Subtask - Pin the Extism ABI, reference Wasmtime family, independent Wazero family, and supported target architectures.

## 1.3 Section - Failure Evidence And Operational Notes

- [x] 1.3 Section - Establish failure evidence and operational notes for profile vocabulary and architectural boundaries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to profile vocabulary and architectural boundaries.
    - [x] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 1.4 Section - Phase 1 Integration Tests

- [x] 1.4 Section - Define integrated verification for profile vocabulary and architectural boundaries across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 1.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 1.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for profile vocabulary and architectural boundaries.
    - [x] 1.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 1.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 1.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

