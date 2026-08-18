# Phase 2 - Guest SDK CLI Simulator Templates Fixtures And Debugging

Back to milestone: [README](./README.md)

- [x] 2 Phase - Make correct plugin and agent development possible without requiring contributors to reconstruct protocol or runtime behavior.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for guest sdk cli simulator templates fixtures and debugging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.1.1.1 Subtask - Define guest SDK surfaces for manifests, exports, codecs, signals, actions, state operations, directives, strategies, diagnostics, and fixtures.
    - [x] 2.1.1.2 Subtask - Define CLI commands for profile inspection, artifact build/validate/sign, plugin compose, fixture test, local run, replay, reduce, and evidence inspection.
    - [x] 2.1.1.3 Subtask - Define a local simulator using the same host contracts with deterministic clocks, randomness, effects, crashes, and policy fixtures.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for guest sdk cli simulator templates fixtures and debugging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.2.1.1 Subtask - Provide minimal direct, FSM, tool-using, multi-agent, migration, capability, and malformed-output templates.
    - [x] 2.2.1.2 Subtask - Provide debugging views for canonical input/output, route/action resolution, patch application, directives, limits, traps, and evidence references.
    - [x] 2.2.1.3 Subtask - Define SDK/CLI compatibility negotiation, deprecation, offline behavior, reproducible builds, and actionable failures.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for guest sdk cli simulator templates fixtures and debugging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to guest sdk cli simulator templates fixtures and debugging.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Define integrated verification for guest sdk cli simulator templates fixtures and debugging across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 2.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for guest sdk cli simulator templates fixtures and debugging.
    - [x] 2.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

