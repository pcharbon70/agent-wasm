# Milestone 8 - Portability, Verification, And Performance

Turn the research assurance design into release evidence spanning standards conformance, independent Extism runtimes, fuzzing, replay, isolation, fault behavior, and performance.

Current status: planned; all phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for portability, verification, and performance.

## Dependencies And Entry Gate

- Milestones 1–7 expose stable contracts and representative workloads.
- Every earlier phase has retained integration fixtures and explicit failure expectations.

## Phase Order

1. [Phase 1 - Evidence Manifests Profiles Runtime Matrices And Traceability](phase-01-evidence-manifests-profiles-runtime-matrices-and-traceability.md)
2. [Phase 2 - Core WASI Extism And Plugin Contract Conformance](phase-02-core-wasi-extism-and-plugin-contract-conformance.md)
3. [Phase 3 - Extism Wasmtime And Extism Wazero Semantic Equivalence](phase-03-extism-wasmtime-and-extism-wazero-semantic-equivalence.md)
4. [Phase 4 - Property Fuzz Replay Reduction Pooling And Isolation](phase-04-property-fuzz-replay-reduction-pooling-and-isolation.md)
5. [Phase 5 - Fault Security Performance Formal Model And Release Acceptance](phase-05-fault-security-performance-formal-model-and-release-acceptance.md)

## Planned Artifacts

- Evidence manifest and support matrix
- Cross-runtime conformance and regression corpus
- Fault, isolation, security, performance, and formal-model release gates

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- Runtime agreement is evidence, not majority-vote truth.
- Fresh-instance behavior is the reference for pooling and reset.
- Performance gates never replace semantic correctness gates.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Evidence Manifests Profiles Runtime Matrices And Traceability](phase-01-evidence-manifests-profiles-runtime-matrices-and-traceability.md) — implements and verifies this ordered phase.
- [Phase 2 - Core WASI Extism And Plugin Contract Conformance](phase-02-core-wasi-extism-and-plugin-contract-conformance.md) — implements and verifies this ordered phase.
- [Phase 3 - Extism Wasmtime And Extism Wazero Semantic Equivalence](phase-03-extism-wasmtime-and-extism-wazero-semantic-equivalence.md) — implements and verifies this ordered phase.
- [Phase 4 - Property Fuzz Replay Reduction Pooling And Isolation](phase-04-property-fuzz-replay-reduction-pooling-and-isolation.md) — implements and verifies this ordered phase.
- [Phase 5 - Fault Security Performance Formal Model And Release Acceptance](phase-05-fault-security-performance-formal-model-and-release-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
