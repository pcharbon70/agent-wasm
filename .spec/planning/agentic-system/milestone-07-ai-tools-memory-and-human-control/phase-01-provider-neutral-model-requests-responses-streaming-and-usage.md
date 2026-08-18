# Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage

Back to milestone: [README](./README.md)

- [x] 1 Phase - Represent model access as policy-governed durable effects with portable requests, bounded results, and provider-specific details behind adapters.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence requirements are reviewable without relying on a
  host-language implementation detail.

## 1.1 Section - Contract And Data Model

- [x] 1.1 Section - Establish contract and data model for provider-neutral model requests responses streaming and usage.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.1.1 Task - Complete the contract and data model work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.1.1.1 Subtask - Define model request identity, provider/model constraints, messages, structured-output schema, tool availability, sampling controls, deadline, budget, and trace context.
    - [x] 1.1.1.2 Subtask - Define response text, structured value, tool requests, finish reason, usage, provider references, safety metadata, and diagnostics.
    - [x] 1.1.1.3 Subtask - Separate durable request/result records from redacted prompt and content payload storage.

## 1.2 Section - Behavior And Integration

- [x] 1.2 Section - Establish behavior and integration for provider-neutral model requests responses streaming and usage.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.2.1.1 Subtask - Define provider adapter registration, capability mapping, model resolution, streaming normalization, cancellation, and retry classification.
    - [x] 1.2.1.2 Subtask - Convert final success or failure into causally linked signals while treating partial stream events as bounded observations.
    - [x] 1.2.1.3 Subtask - Define unavailable model, quota exhaustion, malformed structured output, tool-call mismatch, safety refusal, timeout, late response, and ambiguous billing outcomes.

## 1.3 Section - Failure Evidence And Operational Notes

- [x] 1.3 Section - Establish failure evidence and operational notes for provider-neutral model requests responses streaming and usage.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 1.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized specification-authoring and commit boundary.

    - [x] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to provider-neutral model requests responses streaming and usage.
    - [x] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 1.4 Section - Phase 1 Integration Tests

- [x] 1.4 Section - Define integrated verification for provider-neutral model requests responses streaming and usage across its real dependency boundaries.

  This section defines the integrated-behavior scenarios and reproducible
  evidence required by later milestone and release gates.

  - [x] 1.4.1 Task - Define the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 1.4.1.1 Subtask - Define a scenario for the canonical successful flow and retained evidence for provider-neutral model requests responses streaming and usage.
    - [x] 1.4.1.2 Subtask - Define scenarios in which malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 1.4.1.3 Subtask - Define scenarios in which timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 1.4.1.4 Subtask - Identify all earlier milestone fixtures affected by this phase and define how to record regressions or approved variability.

