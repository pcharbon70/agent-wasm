---
title: "Notes"
kind: map
created: "2026-08-07"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Notes index"
---

# Notes (`20-notes`)

## Purpose

Notes develop ideas, arguments, models, and cross-source synthesis in the
authors' own words.

## What belongs here

Put durable conceptual work here. Keep source-specific claims in source notes,
open workbenches in inquiries, and session evidence in the journal.

## Index

### Subdirectories

- None yet.

### Documents

- [Extism Plugin-System Architecture and Runtimes](extism-plugin-system-architecture-and-runtimes.md)
  — detailed synthesis of Extism's ABI, kernel, call lifecycle, state,
  manifest, capabilities, PDK/SDK split, runtime families, and Agent WASM
  implications.
- [Jido Agent Architecture and a Wasm/Extism Construction](jido-agent-architecture-and-wasm-extism-construction.md)
  — abstracts Jido into decision, messaging, runtime, lifecycle, composition,
  and durability planes, then proposes a host-owned actor runtime around
  portable Extism reducers.
- [WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
  — deep synthesis of the standards stack, runtime architectures, research
  evidence, layered security model, provisional architecture, and evaluation
  program for agent tools.
- [WebAssembly Testing, Verification, and Agent Runtime Assurance](webassembly-testing-verification-and-agent-runtime-assurance.md)
  — surveys conformance suites, plug-in frameworks, fuzzing, differential
  methods, replay, reduction, formal work, and a layered assurance design for
  the Jido-like Extism host.
- [Phase 1 Contract And Data Model Implementation](m7-phase-01-contract-and-data-model-implementation.md)
  — documents Section 1.1 implementation from Phase 1 plan: model request
  identity, provider constraints, response normalization, streaming, and
  usage tracking.
- [Phase 1 Behavior And Integration Implementation](m7-phase-01-behavior-and-integration-implementation.md)
  — documents Section 1.2 implementation: provider adapter behavior,
  capability mapping, signal conversion, cancellation, retry classification,
  and outcome definitions.
- [Phase 1 Failure Evidence And Operational Notes Implementation](m7-phase-01-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 1.3 implementation: failure outcomes, bounded
  diagnostics, evidence emission, implementation-defined choices, and
  deferred work.
- [Phase 1 Integration Tests Implementation](m7-phase-01-integration-tests-implementation.md)
  — documents Section 1.4 implementation: successful flow tests, failure
  handling tests, timeout and cancellation tests, and cross-milestone
  compatibility tests.
- [Phase 2 Contract And Data Model Implementation](m7-phase-02-contract-and-data-model-implementation.md)
  — documents Section 2.1 implementation from Phase 2 plan: tool descriptor
  identity and properties, retrieval request and result schema, and
  code-execution request and result schema.
- [Phase 2 Behavior And Integration Implementation](m7-phase-02-behavior-and-integration-implementation.md)
  — documents Section 2.2 implementation: tool resolution, catalog policy
  filtering, execution through durable effect attempts, and outcome
  definitions.
- [Phase 2 Failure Evidence And Operational Notes Implementation](m7-phase-02-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 2.3 implementation: failure outcomes, bounded
  diagnostics, evidence emission, implementation-defined choices, and
  deferred work.
- [Phase 2 Integration Tests Implementation](m7-phase-02-integration-tests-implementation.md)
  — documents Section 2.4 implementation: successful flow tests, failure
  handling tests, timeout and cancellation tests, and cross-milestone
  compatibility tests.
- [Phase 3 Contract And Data Model Implementation](m7-phase-03-contract-and-data-model-implementation.md)
  — documents Section 3.1 implementation from Phase 3 plan: direct strategy
  behavior, FSM strategy states and transitions, bounded tool-loop state,
  iteration budgets, and snapshot migration.
- [Phase 3 Behavior And Integration Implementation](m7-phase-03-behavior-and-integration-implementation.md)
  — documents Section 3.2 implementation: planning strategy outputs, budget
  enforcement, and failure behavior for invalid snapshots, non-progress loops,
  repeated tool requests, contradictory plans, missing results, model drift,
  and forced termination.
- [Phase 3 Failure Evidence And Operational Notes Implementation](m7-phase-03-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 3.3 implementation: failure outcomes, bounded diagnostics,
  evidence emission, implementation-defined choices, deferred work, and
  results that would invalidate earlier milestone assumptions.
- [Phase 3 Integration Tests Implementation](m7-phase-03-integration-tests-implementation.md)
  — documents Section 3.4 implementation: successful flow tests, failure
  handling tests, timeout and cancellation tests, and cross-milestone
  compatibility tests.
- [Phase 4 Contract And Data Model Implementation](m7-phase-04-contract-and-data-model-implementation.md)
  — documents Section 4.1 implementation from Phase 4 plan: conversation
  threads, messages, participants, causal links, content references, visibility,
  redaction, retention, checkpoints as versioned projections, and memory
  references with provenance, tenant scope, confidence, promotion, and
  deletion policy.
- [Phase 4 Behavior And Integration Implementation](m7-phase-04-behavior-and-integration-implementation.md)
  — documents Section 4.2 implementation: approval requests workflow, quota
  enforcement, and secret lease lifecycle.
- [Phase 4 Failure Evidence And Operational Notes Implementation](m7-phase-04-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 4.3 implementation: failure outcomes, bounded
  diagnostics, evidence emission, implementation-defined choices, and
  deferred work.
- [Phase 4 Integration Tests Implementation](m7-phase-04-integration-tests-implementation.md)
  — documents Section 4.4 implementation: successful flow tests, failure
  handling tests, timeout and cancellation tests, and cross-milestone
  compatibility tests.
- [Phase 5 Contract And Data Model Implementation](m7-phase-05-contract-and-data-model-implementation.md)
  — documents Section 5.1 implementation from Phase 5 plan: workflow types
  (direct-model-response, structured-response, model-to-tool-continuation,
  retrieval-grounded-answer, code-execution, multi-agent-delegation), approval
  outcomes (approval-required, denied, expired), quota exhaustion, revoked
  secret, cancelled model stream, and provenance references (model, tool,
  retrieval, state-revision, directive, attempt, policy).
- [Phase 5 Behavior And Integration Implementation](m7-phase-05-behavior-and-integration-implementation.md)
  — documents Section 5.2 implementation: hostile output validation, loop
  termination under budgets, deterministic resume from snapshots, and the
  Milestone 7 workflow corpus with provenance coverage, safety boundaries,
  cost evidence, and residual model-quality limitations.
- [Phase 5 Failure Evidence And Operational Notes Implementation](m7-phase-05-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 5.3 implementation: failure outcomes, bounded
  diagnostics, evidence emission, implementation-defined choices, deferred
  work, and results that would invalidate earlier milestone assumptions.
- [Phase 5 Integration Tests Implementation](m7-phase-05-integration-tests-implementation.md)
  — documents Section 5.4 implementation: successful flow tests, failure
  handling tests, timeout and cancellation tests, and cross-milestone
  compatibility tests.

## Maintaining this index

Index every direct note and describe its contribution. Update related maps and
inquiries when a note materially changes their conclusions.
