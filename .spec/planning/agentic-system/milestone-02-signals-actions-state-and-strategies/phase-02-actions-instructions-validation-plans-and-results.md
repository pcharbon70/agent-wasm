# Phase 2 - Actions Instructions Validation Plans And Results

Back to milestone: [README](./README.md)

- [x] 2 Phase - Separate reusable operation definitions from concrete invocations and deterministic execution plans.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for actions instructions validation plans and results.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.1.1.1 Subtask - Specify ActionDescriptor metadata, input/output schemas, state access, directive kinds, required grants, and deterministic constraints.
    - [x] 2.1.1.2 Subtask - Specify Instruction identity, action reference, arguments, causal context, expected revision, and optional scheduling metadata.
    - [x] 2.1.1.3 Subtask - Define validation order for action resolution, schema, state preconditions, grants, and bounded execution parameters.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for actions instructions validation plans and results.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.2.1.1 Subtask - Define sequential and DAG plan nodes, dependencies, intermediate result references, and deterministic scheduling order.
    - [x] 2.2.1.2 Subtask - Define domain success, domain rejection, validation failure, and infrastructure failure as distinct result classes.
    - [x] 2.2.1.3 Subtask - Define how action results contribute state operations, directives, facts, diagnostics, and terminal status.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for actions instructions validation plans and results.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to actions instructions validation plans and results.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Verify actions instructions validation plans and results across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [x] 2.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for actions instructions validation plans and results.
    - [x] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

