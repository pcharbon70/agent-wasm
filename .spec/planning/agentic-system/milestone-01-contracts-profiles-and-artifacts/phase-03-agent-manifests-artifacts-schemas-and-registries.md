# Phase 3 - Agent Manifests Artifacts Schemas And Registries

Back to milestone: [README](./README.md)

- [x] 3 Phase - Define immutable executable artifacts and reviewable manifests that can be resolved without instantiating guest code.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 3.1 Section - Contract And Data Model

- [x] 3.1 Section - Establish contract and data model for agent manifests artifacts schemas and registries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.1.1.1 Subtask - Specify artifact digests, media types, build provenance, compiler/PDK metadata, required Wasm features, and signature references.
    - [x] 3.1.1.2 Subtask - Specify AgentManifest fields for exported protocol versions, actions, routes, state schemas, strategies, directives, and requested capabilities.
    - [x] 3.1.1.3 Subtask - Define schema identifiers, canonical schema hashing, ownership, compatibility, and migration references.

## 3.2 Section - Behavior And Integration

- [x] 3.2 Section - Establish behavior and integration for agent manifests artifacts schemas and registries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.2.1.1 Subtask - Define artifact and manifest registry lookup by immutable digest plus approved aliases.
    - [x] 3.2.1.2 Subtask - Define validation order for bytes, digest, signature, feature profile, manifest, schemas, and policy admission.
    - [x] 3.2.1.3 Subtask - Define cache keys that include runtime, target, feature profile, artifact digest, and validation policy.

## 3.3 Section - Failure Evidence And Operational Notes

- [x] 3.3 Section - Establish failure evidence and operational notes for agent manifests artifacts schemas and registries.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 3.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to agent manifests artifacts schemas and registries.
    - [x] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 3.4 Section - Phase 3 Integration Tests

- [x] 3.4 Section - Define integrated verification for agent manifests artifacts schemas and registries across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 3.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 3.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for agent manifests artifacts schemas and registries.
    - [x] 3.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 3.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 3.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

