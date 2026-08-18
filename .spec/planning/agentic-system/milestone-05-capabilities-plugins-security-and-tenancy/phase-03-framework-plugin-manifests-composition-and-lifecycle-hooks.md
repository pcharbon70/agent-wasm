# Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks

Back to milestone: [README](./README.md)

- [x] 3 Phase - Compose Jido-style capability bundles without confusing framework plugins with individual Extism modules.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 3.1 Section - Contract And Data Model

- [x] 3.1 Section - Establish contract and data model for framework plugin manifests composition and lifecycle hooks.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.1.1.1 Subtask - Specify plugin identity, semantic version, publisher, artifacts, actions, routes, state namespaces, schemas, strategies, directives, schedules, and requested grants.
    - [x] 3.1.1.2 Subtask - Define deterministic composition order and conflict checks for names, routes, state, schemas, migrations, capabilities, and lifecycle ownership.
    - [x] 3.1.1.3 Subtask - Separate declarative metadata, untrusted guest artifacts, reviewed preparation logic, and privileged host-native integrations.

## 3.2 Section - Behavior And Integration

- [x] 3.2 Section - Establish behavior and integration for framework plugin manifests composition and lifecycle hooks.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.2.1.1 Subtask - Define install, validate, approve, enable, disable, upgrade, migrate, rollback, and remove lifecycle operations.
    - [x] 3.2.1.2 Subtask - Require composition and authorization to complete before loading executable artifacts.
    - [x] 3.2.1.3 Subtask - Define missing dependency, version conflict, circular dependency, ambiguous route, orphaned state, and revoked publisher behavior.

## 3.3 Section - Failure Evidence And Operational Notes

- [x] 3.3 Section - Establish failure evidence and operational notes for framework plugin manifests composition and lifecycle hooks.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to framework plugin manifests composition and lifecycle hooks.
    - [x] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 3.4 Section - Phase 3 Integration Tests

- [x] 3.4 Section - Define integrated verification for framework plugin manifests composition and lifecycle hooks across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 3.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 3.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for framework plugin manifests composition and lifecycle hooks.
    - [x] 3.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 3.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 3.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

