# Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors

Back to milestone: [README](./README.md)

- [x] 2 Phase - Expose external abilities through typed catalogs and effect handlers rather than ambient guest authority.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for tool catalogs retrieval code execution and connectors.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.1.1.1 Subtask - Define ToolDescriptor identity, version, schemas, capability, side-effect class, idempotency, timeout, result limits, and provenance requirements.
    - [x] 2.1.1.2 Subtask - Define retrieval requests and results with tenant scope, query, filters, ranking metadata, citations, and bounded content references.
    - [x] 2.1.1.3 Subtask - Define code-execution requests with immutable environment, inputs, capability policy, resource budget, output artifacts, and isolation class.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for tool catalogs retrieval code execution and connectors.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.2.1.1 Subtask - Resolve tools from approved framework plugins and policy-filter the catalog before presenting it to a strategy or model.
    - [x] 2.2.1.2 Subtask - Execute tools, retrieval, code, and connectors through durable effect attempts with normalized result signals.
    - [x] 2.2.1.3 Subtask - Define unknown tool, schema mismatch, denied capability, stale catalog, unsafe output, sandbox failure, partial connector success, and provenance loss.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for tool catalogs retrieval code execution and connectors.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to tool catalogs retrieval code execution and connectors.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Define integrated verification for tool catalogs retrieval code execution and connectors across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 2.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for tool catalogs retrieval code execution and connectors.
    - [x] 2.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

