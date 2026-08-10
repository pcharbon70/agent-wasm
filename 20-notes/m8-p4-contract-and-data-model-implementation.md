---
title: "M8-P4 Section 4.1 Contract And Data Model Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-04
  - contract-and-data-model
  - property-fuzz
  - replay
  - reduction
  - pooling
  - isolation
aliases:
  - "M8-P4.1 Section 4.1 Contract And Data Model Implementation"
---

# M8-P4 Section 4.1 Contract And Data Model Implementation

## Purpose

Establish contract and data model for property fuzzing, replay, reduction, pooling, and isolation. This section defines the fuzzing infrastructure, artifact mutation strategies, and isolation guarantees that underlie the Phase 4 implementation. See [Section 4.2 Behavior And Integration](./m8-p4-behavior-and-integration-implementation.md) for the behavior and integration work that follows.

## Design Decisions

### Subtask 4.1.1.1: Deterministic Fuzz Input Generation

Valid and invalid protocol values, signal sequences, state patches, directive results, lifecycle commands, and crash schedules MUST be generated from deterministic seeds. The generation specifications are:

```yaml
FuzzInputGeneration = {
  protocol_values: {
    description: "Generate valid and invalid protocol values",
    generator: "protocol-value-fuzzer",
    seed: u64,
    valid_ratio: f64,
    invalid_categories: string[]
  },
  signal_sequences: {
    description: "Generate signal sequences",
    generator: "signal-sequence-fuzzer",
    seed: u64,
    max_length: u32,
    distribution: string
  },
  state_patches: {
    description: "Generate state patches",
    generator: "state-patch-fuzzer",
    seed: u64,
    mutation_types: string[],
    boundary_values: bool
  },
  directive_results: {
    description: "Generate directive results",
    generator: "directive-result-fuzzer",
    seed: u64,
    valid_outcomes: string[],
    invalid_outcomes: string[]
  },
  lifecycle_commands: {
    description: "Generate lifecycle commands",
    generator: "lifecycle-command-fuzzer",
    seed: u64,
    command_types: string[],
    ordering_constraints: bool
  },
  crash_schedules: {
    description: "Generate crash schedules",
    generator: "crash-schedule-fuzzer",
    seed: u64,
    crash_points: string[],
    timing_models: string[]
  }
}
```

**Decision**: All fuzz inputs are generated from deterministic seeds to ensure reproducibility. Valid and invalid inputs are generated in configurable ratios. Boundary values are included to test edge cases.

### Subtask 4.1.1.2: Artifact Mutation with wasm-smith and wasm-mutate

wasm-smith and wasm-mutate MUST be used around representative compiled reducers with profile-aware features and application-aware result oracles. The mutation specifications are:

```yaml
ArtifactMutation = {
  wasm_smith: {
    description: "Generate valid WebAssembly modules",
    tool: "wasm-smith",
    version: string,
    features: string[],
    profiles: string[]
  },
  wasm_mutate: {
    description: "Mutate existing WebAssembly modules",
    tool: "wasm-mutate",
    version: string,
    mutation_strategies: string[],
    preserve_semantics: bool
  },
  representative_reducers: {
    description: "Compiled reducers representing different profiles",
    reducers: string[]
  },
  result_oracles: {
    description: "Application-aware result oracles for validation",
    oracles: string[]
  }
}
```

**Decision**: wasm-smith generates valid WebAssembly modules for positive testing. wasm-mutate mutates existing modules for negative testing. Representative reducers cover different feature profiles. Result oracles validate that mutations produce expected behaviors.

### Subtask 4.1.1.3: Nondeterministic Input Recording and Replay

Explicit nondeterministic inputs and imported results MUST be recorded, secrets MUST be redacted, and turns MUST be replayed across runtime families. The recording and replay specifications are:

```yaml
NondeterministicInputRecording = {
  inputs: {
    description: "Record explicit nondeterministic inputs",
    fields: string[],
    redaction: RedactionPolicy
  },
  imported_results: {
    description: "Record imported function results",
    fields: string[],
    redaction: RedactionPolicy
  },
  replay: {
    description: "Replay turns across runtime families",
    engines: string[],
    comparison: EquivalenceCheck
  }
}

RedactionPolicy = {
  secrets: "redact",
  pii: "redact",
  internal_urls: "redact",
  user_data: "redact"
}

EquivalenceCheck = {
  method: "structural",
  allowed_variability: string[]
}
```

**Decision**: Nondeterministic inputs are recorded with full context for replay. Secrets are redacted before recording. Turns are replayed across all runtime families to verify semantic equivalence.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p4-contract-and-data-model-implementation.md  (this file)
```

### Key Invariants

1. **Deterministic Generation**: All fuzz inputs are generated from deterministic seeds. This ensures reproducibility and enables regression tracking.

2. **Valid and Invalid Inputs**: Both valid and invalid inputs are generated. Invalid inputs test error handling and robustness.

3. **Profile-Aware Mutation**: Artifact mutation is aware of the feature profile being tested. Mutations that violate profile constraints are filtered.

4. **Redaction**: Secrets, PII, and internal URLs are redacted from recorded inputs and results.

5. **Cross-Engine Replay**: Turns are replayed across all runtime families to verify semantic equivalence.

### Validation Rules

The validator MUST check:

1. All fuzz inputs are generated from deterministic seeds.
2. Recorded inputs are redacted according to the redaction policy.
3. Replay results are comparable across engines.
4. Reduced artifacts preserve the violated invariant.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 4.1.1: Deterministic Fuzz Input Generation

**Setup**: Configure fuzz input generation with a fixed seed.

**Steps**:
1. Configure protocol value fuzzer with seed 12345.
2. Generate 1000 protocol values.
3. Verify outputs are deterministic (run again with same seed).
4. Verify valid/invalid ratio matches configuration.

**Expected Result**: Outputs are deterministic. Valid/invalid ratio matches configuration.

### Test 4.1.2: Artifact Mutation

**Setup**: Configure wasm-smith and wasm-mutate for artifact mutation.

**Steps**:
1. Generate valid WebAssembly modules with wasm-smith.
2. Mutate existing modules with wasm-mutate.
3. Validate mutated modules with result oracles.
4. Verify mutations preserve profile constraints.

**Expected Result**: Mutated modules are valid and preserve profile constraints.

### Test 4.1.3: Nondeterministic Input Replay

**Setup**: Record nondeterministic inputs and replay turns.

**Steps**:
1. Execute a turn with nondeterministic inputs.
2. Record inputs with redaction.
3. Replay the turn on a different engine.
4. Compare results for equivalence.

**Expected Result**: Results are equivalent across engines.

## Operational Notes

### Implementation-Defined Choices

1. **Seed Management**: Seeds are stored alongside fuzz inputs for reproducibility. Seed rotation is documented.

2. **Mutation Strategy Selection**: Mutation strategies are selected based on the reducer profile and testing objectives.

3. **Redaction Patterns**: Redaction patterns are configured per deployment. Common patterns include API keys, tokens, and internal URLs.

4. **Replay Comparison**: Structural comparison is used for replay equivalence. Allowed variability is documented per comparison.

### Deferred Work

1. **Adaptive Fuzzing**: Fuzzing is currently random. Adaptive fuzzing (guided by coverage) is not yet supported.

2. **Distributed Fuzzing**: Fuzzing is currently centralized. Distributed fuzzing is not yet supported.

3. **Automated Reduction**: Reduction is currently manual. Automated reduction is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The contract and data model build on the evidence manifests defined in [Phase 1 Section 1.1 Contract And Data Model](./m8-p1-contract-and-data-model-implementation.md) and the conformance work defined in [Phase 2 Section 2.1 Contract And Data Model](./m8-p2-contract-and-data-model-implementation.md).

## Checklist

- [x] 4.1.1.1 Subtask - Generate valid and invalid protocol values, signal sequences, state patches, directive results, lifecycle commands, and crash schedules from deterministic seeds.
- [x] 4.1.1.2 Subtask - Use wasm-smith and wasm-mutate around representative compiled reducers with profile-aware features and application-aware result oracles.
- [x] 4.1.1.3 Subtask - Record explicit nondeterministic inputs and imported results, redact secrets, and replay turns across runtime families.
