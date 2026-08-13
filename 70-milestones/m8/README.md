---
title: "Milestone 8"
kind: map
created: "2026-08-13"
tags:
  - archive-navigation
  - directory-index
aliases: []
---

# Milestone 8 (`70-milestones/m8`)

## Purpose

Implementation records for Milestone 8, covering cross-runtime equivalence,
fuzzing, crash injection, performance, and deployment.

## What belongs here

Implementation notes documenting each section of M8 phase plans, including
specification chapters produced, test IDs defined, design decisions, and open
questions.

## Index

### Subdirectories

None yet.

### Documents

- [M8-P1 Section 1.1 Contract And Data Model Implementation](m8-p1-contract-and-data-model-implementation.md)
  — documents Section 1.1 implementation from Phase 1 plan: evidence manifest
  field specifications, disposition definitions, initial runtime matrix, and
  validation rules.
- [M8-P1 Section 1.2 Behavior And Integration Implementation](m8-p1-behavior-and-integration-implementation.md)
  — documents Section 1.2 implementation: test case mapping, aggregate status
  visibility, evidence lifecycle, and release comparison.
- [M8-P1 Section 1.3 Failure Evidence And Operational Notes Implementation](m8-p1-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 1.3 implementation: failure outcomes, bounded diagnostics,
  implementation-defined choices, and deferred work.
- [M8-P1 Section 1.4 Phase 1 Integration Tests Implementation](m8-p1-integration-tests-implementation.md)
  — documents Section 1.4 implementation: canonical flow, failure flow,
  resilience flow, and regression flow tests.
- [M8-P1 Runtime Matrix](m8-p1-runtime-matrix.yaml)
  — initial runtime matrix configuration for Extism/Wasmtime and Extism/Wazero
  across supported host platforms and guest toolchains.
- [M8-P2 Section 2.1 Contract And Data Model Implementation](m8-p2-contract-and-data-model-implementation.md)
  — documents Section 2.1 implementation from Phase 2 plan: Core WebAssembly
  suite specifications, WASI suite specifications, WABT and reference interpreter
  specifications, and validation rules.
- [M8-P2 Section 2.2 Behavior And Integration Implementation](m8-p2-behavior-and-integration-implementation.md)
  — documents Section 2.2 implementation: XTP contracts, Host SDK integration
  areas, defect promotion specifications, and integration points.
- [M8-P2 Section 2.3 Failure Evidence And Operational Notes Implementation](m8-p2-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 2.3 implementation: failure outcomes, bounded diagnostics,
  implementation-defined choices, and deferred work.
- [M8-P2 Section 2.4 Phase 2 Integration Tests Implementation](m8-p2-integration-tests-implementation.md)
  — documents Section 2.4 implementation: canonical flow, failure flow,
  resilience flow, and regression flow tests.
- [M8-P3 Section 3.1 Contract And Data Model Implementation](m8-p3-contract-and-data-model-implementation.md)
  — documents Section 3.1 implementation from Phase 3 plan: TurnResult
  equivalence specifications, controlled variables, execution scenarios, and
  validation rules.
- [M8-P3 Section 3.2 Behavior And Integration Implementation](m8-p3-behavior-and-integration-implementation.md)
  — documents Section 3.2 implementation: behavior comparison, divergence
  recording format, adjudication specifications, and integration points.
- [M8-P3 Section 3.3 Failure Evidence And Operational Notes Implementation](m8-p3-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 3.3 implementation: failure outcomes, bounded diagnostics,
  implementation-defined choices, and deferred work.
- [M8-P3 Section 3.4 Phase 3 Integration Tests Implementation](m8-p3-integration-tests-implementation.md)
  — documents Section 3.4 implementation: canonical flow, failure flow,
  resilience flow, and regression flow tests.
- [M8-P4 Section 4.1 Contract And Data Model Implementation](m8-p4-contract-and-data-model-implementation.md)
  — documents Section 4.1 implementation: deterministic fuzz input generation,
  artifact mutation with wasm-smith/wasm-mutate, and nondeterministic input
  recording and replay.
- [M8-P4 Section 4.2 Behavior And Integration Implementation](m8-p4-behavior-and-integration-implementation.md)
  — documents Section 4.2 implementation: artifact and event history
  reduction with invariant preservation, instance mode comparison, and
  failure deduplication.
- [M8-P4 Section 4.3 Failure Evidence And Operational Notes Implementation](m8-p4-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 4.3 implementation: failure outcomes (malformed,
  incompatible, conflicting, unauthorized, exhausted, unavailable), bounded
  diagnostics, implementation-defined choices, and deferred work.
- [M8-P4 Section 4.4 Phase 4 Integration Tests Implementation](m8-p4-integration-tests-implementation.md)
  — documents Section 4.4 implementation: canonical flow verification, invalid
  input handling, resource handling, and earlier milestone fixture regression
  checks.
- [M8-P5 Section 5.1 Contract And Data Model Implementation](m8-p5-contract-and-data-model-implementation.md)
  — documents Section 5.1 implementation: deterministic crash injection,
  adversarial testing suites (capability, import, output, secret, tenant-residue,
  resource-exhaustion, supply-chain, audit-tampering), and performance
  measurement across representative sizes.
- [M8-P5 Section 5.2 Behavior And Integration Implementation](m8-p5-behavior-and-integration-implementation.md)
  — documents Section 5.2 implementation: runtime timing ratio comparison with
  environmental context, formal/reference model maintenance, and release
  acceptance publication.
- [M8-P5 Section 5.3 Failure Evidence And Operational Notes Implementation](m8-p5-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 5.3 implementation: failure outcomes (malformed,
  incompatible, conflicting, unauthorized, exhausted, unavailable), bounded
  diagnostics, implementation-defined choices, and deferred work.
- [M8-P5 Section 5.4 Phase 5 Integration Tests Implementation](m8-p5-integration-tests-implementation.md)
  — documents Section 5.4 implementation: canonical flow verification, invalid
  input handling, resource handling, and earlier milestone fixture regression
  checks.
- [M8-P6 Section 6.1 Contract And Data Model Implementation](m8-p6-contract-and-data-model-implementation.md)
  — documents Section 6.1 implementation: deployment artifact specifications
  (binaries, configurations, dependency manifests per platform), operational
  procedures documentation, and community handoff criteria.
- [M8-P6 Section 6.2 Behavior And Integration Implementation](m8-p6-behavior-and-integration-implementation.md)
  — documents Section 6.2 implementation: artifact packaging and integrity
  verification, deployment procedure execution on representative platforms,
  and community handoff review.
- [M8-P6 Section 6.3 Failure Evidence And Operational Notes Implementation](m8-p6-failure-evidence-and-operational-notes-implementation.md)
  — documents Section 6.3 implementation: failure outcomes (malformed,
  incompatible, conflicting, unauthorized, exhausted, unavailable), bounded
  diagnostics, implementation-defined choices, and deferred work.
- [M8-P6 Section 6.4 Phase 6 Integration Tests Implementation](m8-p6-integration-tests-implementation.md)
  — documents Section 6.4 implementation: canonical flow verification, invalid
  input handling, resource handling, and earlier milestone fixture regression
  checks.

## Maintaining this index

Index every direct file and describe its contribution. Update related maps
and inquiries when a milestone record materially changes their conclusions.
