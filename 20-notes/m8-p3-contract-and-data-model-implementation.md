---
title: "M8-P3 Section 3.1 Contract And Data Model Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-03
  - contract-and-data-model
  - extism
  - wasmtime
  - wazero
  - semantic-equivalence
aliases:
  - "M8-P3.1 Section 3.1 Contract And Data Model Implementation"
---

# M8-P3 Section 3.1 Contract And Data Model Implementation

## Purpose

Establish contract and data model for Extism Wasmtime and Extism Wazero semantic equivalence. This section defines the canonical TurnResult equivalence, controlled variables, and execution scenarios that underlie the semantic equivalence proof. See [Section 3.2 Behavior And Integration](./m8-p3-behavior-and-integration-implementation.md) for the behavior and integration work that follows.

## Design Decisions

### Subtask 3.1.1.1: Canonical TurnResult Equivalence

The canonical TurnResult equivalence defines when two runs produce equivalent results. The definition covers:

```yaml
TurnResultEquivalence = {
  encoding: EncodingEquivalence,
  state_patch: StatePatchEquivalence,
  directive_order: DirectiveOrderEquivalence,
  diagnostics: DiagnosticsEquivalence,
  errors: ErrorsEquivalence,
  allowed_variability: AllowedVariability[]
}

EncodingEquivalence = {
  description: "String encodings are byte-for-byte identical",
  exception: "UTF-8 normalization is permitted"
}

StatePatchEquivalence = {
  description: "State patches are semantically equivalent",
  exception: "Internal counter differences are permitted if observable behavior is identical"
}

DirectiveOrderEquivalence = {
  description: "Directive execution order is identical",
  exception: "None - order must match exactly"
}

DiagnosticsEquivalence = {
  description: "Diagnostic messages are byte-for-byte identical",
  exception: "Engine-specific metadata prefixes are permitted"
}

ErrorsEquivalence = {
  description: "Error types and messages are identical",
  exception: "Stack trace differences are permitted for trap errors"
}

AllowedVariability = {
  description: string,
  condition: string,
  justification: string
}
```

**Decision**: TurnResult equivalence is strict for encoding, state patch, directive order, diagnostics, and errors. Only minimal variability is allowed (UTF-8 normalization, internal counters, engine-specific metadata prefixes, stack traces).

### Subtask 3.1.1.2: Controlled Variables

The following variables MUST be held constant across runs to ensure semantic equivalence:

```yaml
ControlledVariables = {
  artifact: {
    description: "The same WebAssembly artifact is used",
    method: "Pin artifact digest and verify before each run"
  },
  explicit_state: {
    description: "Initial state is identical",
    method: "Initialize state from the same seed and record initial state digest"
  },
  signal: {
    description: "Signals are identical",
    method: "Use deterministic signal generation with fixed seed"
  },
  grants: {
    description: "Grant configurations are identical",
    method: "Load grants from the same configuration file"
  },
  policy: {
    description: "Policy configurations are identical",
    method: "Load policy from the same configuration file"
  },
  limits: {
    description: "Resource limits are identical",
    method: "Configure memory, gas, and call limits to the same values"
  },
  clocks: {
    description: "Clocks are synchronized",
    method: "Use monotonic clocks with fixed starting values"
  },
  randomness: {
    description: "Randomness is deterministic",
    method: "Use seeded PRNG with fixed seed for all random operations"
  },
  imported_results: {
    description: "Imported function results are identical",
    method: "Mock imported functions to return deterministic results"
  }
}
```

**Decision**: All variables are held constant to isolate semantic differences to the runtime engines. Any variable that could affect behavior is controlled and documented.

### Subtask 3.1.1.3: Execution Scenarios

The following execution scenarios MUST be executed on both Extism/Wasmtime and Extism/Wazero:

```yaml
ExecutionScenarios = {
  describe: {
    description: "Describe the artifact capabilities",
    steps: string[],
    expected_outcome: string
  },
  initialize: {
    description: "Initialize the instance",
    steps: string[],
    expected_outcome: string
  },
  direct_reduce: {
    description: "Execute a direct reduce operation",
    steps: string[],
    expected_outcome: string
  },
  fsm_continuation: {
    description: "Execute FSM continuation steps",
    steps: string[],
    expected_outcome: string
  },
  bounded_tool_loop: {
    description: "Execute bounded tool loop operations",
    steps: string[],
    expected_outcome: string
  },
  terminal_state: {
    description: "Verify terminal state handling",
    steps: string[],
    expected_outcome: string
  },
  migration: {
    description: "Verify state migration between engines",
    steps: string[],
    expected_outcome: string
  }
}
```

**Decision**: All scenarios are executed on both runtime families. Results are compared for semantic equivalence. Any divergence is documented and adjudicated.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p3-contract-and-data-model-implementation.md  (this file)
```

### Key Invariants

1. **Strict Equivalence**: TurnResult equivalence is strict for encoding, state patch, directive order, diagnostics, and errors. Only minimal variability is allowed.

2. **Controlled Variables**: All variables that could affect behavior are held constant. This isolates semantic differences to the runtime engines.

3. **Complete Coverage**: All execution scenarios are executed on both runtime families. No scenario is skipped.

4. **Traceability**: Each execution result is recorded with full traceability to the scenario, engine, and controlled variables.

### Validation Rules

The validator MUST check:

1. All controlled variables are held constant across runs.
2. TurnResult equivalence is computed correctly.
3. Divergences are documented with full provenance.
4. Adjudication is performed for each divergence.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 3.1.1: TurnResult Equivalence

**Setup**: Execute a direct reduce operation on both Extism/Wasmtime and Extism/Wazero with the same artifact, state, signal, grants, policy, limits, clocks, randomness, and imported results.

**Steps**:
1. Pin the artifact digest.
2. Initialize state from the same seed.
3. Generate signals with the same seed.
4. Load grants and policy from the same configuration files.
5. Configure limits to the same values.
6. Synchronize clocks.
7. Use seeded PRNG for randomness.
8. Mock imported functions to return deterministic results.
9. Execute the direct reduce operation on both engines.
10. Compare TurnResults for equivalence.

**Expected Result**: TurnResults are equivalent (encoding, state patch, directive order, diagnostics, errors).

### Test 3.1.2: FSM Continuation

**Setup**: Execute FSM continuation steps on both engines.

**Steps**:
1. Execute describe and initialize on both engines.
2. Execute FSM continuation steps on both engines.
3. Compare TurnResults for equivalence.

**Expected Result**: TurnResults are equivalent.

### Test 3.1.3: Migration

**Setup**: Verify state migration between engines.

**Steps**:
1. Execute describe and initialize on Extism/Wasmtime.
2. Execute FSM continuation steps on Extism/Wasmtime.
3. Export state from Extism/Wasmtime.
4. Import state into Extism/Wazero.
5. Continue execution on Extism/Wazero.
6. Compare TurnResults with native Extism/Wazero execution.

**Expected Result**: TurnResults are equivalent.

## Operational Notes

### Implementation-Defined Choices

1. **Equivalence Algorithm**: TurnResult equivalence is computed using a structural comparison algorithm. The algorithm compares encoding, state patch, directive order, diagnostics, and errors.

2. **Controlled Variable Verification**: Controlled variables are verified before each run. Any deviation causes the run to be rejected.

3. **Divergence Documentation**: Divergences are documented with full provenance including engine versions, controlled variable values, and execution scenario.

4. **Adjudication Process**: Adjudication is performed by comparing the divergence against protocol clauses, official semantics, reference models, and reduced reproducers.

### Deferred Work

1. **Automated Equivalence Checking**: Equivalence checking is currently manual. Automated checking is not yet supported.

2. **Distributed Execution**: Execution is currently centralized. Distributed execution is not yet supported.

3. **Performance Optimization**: Execution is not yet optimized for large state sizes.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The contract and data model build on the evidence manifests defined in [Phase 1 Section 1.1 Contract And Data Model](./m8-p1-contract-and-data-model-implementation.md) and the conformance work defined in [Phase 2 Section 2.1 Contract And Data Model](./m8-p2-contract-and-data-model-implementation.md).

## Checklist

- [x] 3.1.1.1 Subtask - Define canonical TurnResult equivalence for encoding, state patch meaning, directive order, diagnostics, errors, and allowed presentation variability.
- [x] 3.1.1.2 Subtask - Hold artifact, explicit state, signal, grants, policy, limits, clocks, randomness, and imported results constant across runs.
- [x] 3.1.1.3 Subtask - Execute describe, initialize, direct reduce, FSM continuation, bounded tool loop, terminal state, and migration on both families.
