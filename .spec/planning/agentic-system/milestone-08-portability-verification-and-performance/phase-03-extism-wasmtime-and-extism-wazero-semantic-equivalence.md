# Phase 3 - Extism Wasmtime And Extism Wazero Semantic Equivalence

Back to milestone: [README](./README.md)

- [ ] 3 Phase - Prove the pinned agent protocol has one observable meaning across two genuinely independent Extism runtime families.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 3.1 Section - Contract And Data Model

- [ ] 3.1 Section - Establish contract and data model for extism wasmtime and extism wazero semantic equivalence.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.1.1.1 Subtask - Define canonical TurnResult equivalence for encoding, state patch meaning, directive order, diagnostics, errors, and allowed presentation variability.
    - [ ] 3.1.1.2 Subtask - Hold artifact, explicit state, signal, grants, policy, limits, clocks, randomness, and imported results constant across runs.
    - [ ] 3.1.1.3 Subtask - Execute describe, initialize, direct reduce, FSM continuation, bounded tool loop, terminal state, and migration on both families.

## 3.2 Section - Behavior And Integration

- [ ] 3.2 Section - Establish behavior and integration for extism wasmtime and extism wazero semantic equivalence.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.2.1.1 Subtask - Compare trap, timeout, cancellation, missing import, invalid output, memory limit, variable state, and reset behavior.
    - [ ] 3.2.1.2 Subtask - Record raw and normalized outputs plus engine-specific configuration for every divergence.
    - [ ] 3.2.1.3 Subtask - Adjudicate divergence against protocol clauses, official semantics, reference models, and reduced reproducers rather than majority vote.

## 3.3 Section - Failure Evidence And Operational Notes

- [ ] 3.3 Section - Establish failure evidence and operational notes for extism wasmtime and extism wazero semantic equivalence.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to extism wasmtime and extism wazero semantic equivalence.
    - [ ] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 3.4 Section - Phase 3 Integration Tests

- [ ] 3.4 Section - Verify extism wasmtime and extism wazero semantic equivalence across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 3.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 3.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for extism wasmtime and extism wazero semantic equivalence.
    - [ ] 3.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 3.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 3.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

