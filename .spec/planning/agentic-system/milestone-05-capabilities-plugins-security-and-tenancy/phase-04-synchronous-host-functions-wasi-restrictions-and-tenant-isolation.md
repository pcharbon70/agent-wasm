# Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation

Back to milestone: [README](./README.md)

- [x] 4 Phase - Keep the synchronous import surface narrow and prove that logical tenancy is backed by memory, state, capability, and resource separation.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 4.1 Section - Contract And Data Model

- [x] 4.1 Section - Establish contract and data model for synchronous host functions wasi restrictions and tenant isolation.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 4.1.1.1 Subtask - Define eligibility criteria for deterministic, bounded, cancellable, retry-safe synchronous host functions.
    - [x] 4.1.1.2 Subtask - Namespace built-in Extism imports separately from application capabilities and reject undeclared imports.
    - [x] 4.1.1.3 Subtask - Default to no WASI; grant selected interfaces only through an explicit guest profile and host policy.

## 4.2 Section - Behavior And Integration

- [x] 4.2 Section - Establish behavior and integration for synchronous host functions wasi restrictions and tenant isolation.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 4.2.1.1 Subtask - Bind every host callback to invocation, tenant, principal, artifact, grants, deadline, and output limits.
    - [x] 4.2.1.2 Subtask - Define fresh, reset, pooled, and agent-pinned instance modes with fresh-instance behavior as the oracle.
    - [x] 4.2.1.3 Subtask - Test residue across tenant, agent, artifact, success, trap, timeout, cancellation, memory pressure, and Extism-variable use.

## 4.3 Section - Failure Evidence And Operational Notes

- [x] 4.3 Section - Establish failure evidence and operational notes for synchronous host functions wasi restrictions and tenant isolation.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 4.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 4.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to synchronous host functions wasi restrictions and tenant isolation.
    - [x] 4.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 4.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 4.4 Section - Phase 4 Integration Tests

- [x] 4.4 Section - Define integrated verification for synchronous host functions wasi restrictions and tenant isolation across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 4.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 4.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for synchronous host functions wasi restrictions and tenant isolation.
    - [x] 4.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 4.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 4.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

