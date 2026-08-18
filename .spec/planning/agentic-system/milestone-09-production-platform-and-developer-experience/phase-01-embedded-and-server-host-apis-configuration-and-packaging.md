# Phase 1 - Embedded And Server Host APIs Configuration And Packaging

Back to milestone: [README](./README.md)

- [x] 1 Phase - Expose the verified runtime through stable embedded and server shapes with explicit startup, shutdown, configuration, and deployment boundaries.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 1.1 Section - Contract And Data Model

- [x] 1.1 Section - Establish contract and data model for embedded and server host apis configuration and packaging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.1.1.1 Subtask - Define host operations for artifact/plugin registration, agent create/inspect, signal/instruction submit, history, cancel, hibernate/thaw, topology, capabilities, approvals, and event retrieval.
    - [x] 1.1.1.2 Subtask - Define canonical request, response, job, event, pagination, idempotency, error, and capability-discovery envelopes independent of transport.
    - [x] 1.1.1.3 Subtask - Define embedded lifecycle interfaces for configuration, dependency injection, startup, readiness, drain, cancellation, shutdown, and resource cleanup.

## 1.2 Section - Behavior And Integration

- [x] 1.2 Section - Establish behavior and integration for embedded and server host apis configuration and packaging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.2.1.1 Subtask - Define server adapters over the same host operation catalog without placing protocol semantics in transports.
    - [x] 1.2.1.2 Subtask - Define configuration sources, precedence, validation, secret references, profile selection, runtime/storage adapters, and safe diagnostics.
    - [x] 1.2.1.3 Subtask - Define package boundaries for host core, Extism adapters, storage, transports, providers, CLI, test kit, and optional integrations.

## 1.3 Section - Failure Evidence And Operational Notes

- [x] 1.3 Section - Establish failure evidence and operational notes for embedded and server host apis configuration and packaging.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to embedded and server host apis configuration and packaging.
    - [x] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 1.4 Section - Phase 1 Integration Tests

- [x] 1.4 Section - Define integrated verification for embedded and server host apis configuration and packaging across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 1.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 1.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for embedded and server host apis configuration and packaging.
    - [x] 1.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 1.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 1.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

