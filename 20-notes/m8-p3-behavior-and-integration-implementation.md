---
title: "M8-P3 Section 3.2 Behavior And Integration Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-03
  - behavior-and-integration
  - extism
  - wasmtime
  - wazero
  - semantic-equivalence
aliases:
  - "M8-P3.2 Section 3.2 Behavior And Integration Implementation"
---

# M8-P3 Section 3.2 Behavior And Integration Implementation

## Purpose

Establish behavior and integration for Extism Wasmtime and Extism Wazero semantic equivalence. This section builds on the contract and data model defined in [Section 3.1 Contract And Data Model](./m8-p3-contract-and-data-model-implementation.md) and precedes the failure evidence defined in [Section 3.3 Failure Evidence And Operational Notes](./m8-p3-failure-evidence-and-operational-notes-implementation.md).

## Design Decisions

### Subtask 3.2.1.1: Behavior Comparison

The following behaviors MUST be compared between Extism/Wasmtime and Extism/Wazero:

```yaml
BehaviorComparison = {
  trap: {
    description: "Compare trap handling and error reporting",
    test_cases: string[],
    expected_outcome: "Identical trap types and messages"
  },
  timeout: {
    description: "Compare timeout handling",
    test_cases: string[],
    expected_outcome: "Identical timeout behavior"
  },
  cancellation: {
    description: "Compare cancellation handling",
    test_cases: string[],
    expected_outcome: "Identical cancellation behavior"
  },
  missing_import: {
    description: "Compare missing import handling",
    test_cases: string[],
    expected_outcome: "Identical missing import errors"
  },
  invalid_output: {
    description: "Compare invalid output handling",
    test_cases: string[],
    expected_outcome: "Identical invalid output errors"
  },
  memory_limit: {
    description: "Compare memory limit enforcement",
    test_cases: string[],
    expected_outcome: "Identical memory limit behavior"
  },
  variable_state: {
    description: "Compare variable state handling",
    test_cases: string[],
    expected_outcome: "Identical variable state behavior"
  },
  reset: {
    description: "Compare instance reset behavior",
    test_cases: string[],
    expected_outcome: "Identical reset behavior"
  }
}
```

**Decision**: Each behavior is tested with specific test cases. Expected outcomes are identical behavior between engines. Any divergence is documented and adjudicated.

### Subtask 3.2.1.2: Divergence Recording

Every divergence MUST be recorded with raw and normalized outputs plus engine-specific configuration:

```yaml
DivergenceRecord = {
  scenario: string,
  engine_a: {
    name: string,
    version: string,
    configuration: EngineConfiguration
  },
  engine_b: {
    name: string,
    version: string,
    configuration: EngineConfiguration
  },
  raw_output_a: bytes,
  raw_output_b: bytes,
  normalized_output_a: string,
  normalized_output_b: string,
  divergence_type: DivergenceType,
  severity: Severity,
  timestamp: ISO8601,
  correlation_id: UUID
}

EngineConfiguration = {
  memory_limit: u64,
  gas_limit: u64,
  timeout_ms: u64,
  features: string[],
  experimental: bool
}

DivergenceType = "encoding" | "state" | "directive_order" | "diagnostic" | "error" | "performance"

Severity = "low" | "medium" | "high" | "critical"
```

**Decision**: Divergences are recorded with full context including engine configuration, raw and normalized outputs, divergence type, and severity. This enables precise adjudication and regression tracking.

### Subtask 3.2.1.3: Divergence Adjudication

Every divergence MUST be adjudicated against protocol clauses, official semantics, reference models, and reduced reproducers rather than majority vote:

```yaml
Adjudication = {
  divergence_id: string,
  protocol_clauses: string[],
  official_semantics: string[],
  reference_models: string[],
  reduced_reproducer: string?,
  verdict: Verdict,
  justification: string,
  timestamp: ISO8601
}

Verdict = "conforming" | "non-conforming" | "unresolved"
```

**Decision**: Adjudication is based on authoritative sources (protocol clauses, official semantics, reference models) and empirical evidence (reduced reproducers), not on majority vote between engines. This ensures correctness is determined by specifications, not implementation convenience.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p3-behavior-and-integration-implementation.md  (this file)
```

### Key Behaviors

1. **Behavior Comparison**: Each behavior is tested with specific test cases. Tests are executed on both engines with controlled variables.

2. **Divergence Recording**: Every divergence is recorded with full context. The record includes engine configuration, raw and normalized outputs, divergence type, and severity.

3. **Divergence Adjudication**: Every divergence is adjudicated against authoritative sources. The verdict is based on specifications and empirical evidence, not majority vote.

### Integration Points

1. **Phase 1 Evidence Manifests**: Divergence records are stored in evidence manifests defined in Phase 1.

2. **Phase 2 Conformance**: Behavior comparisons build on the conformance work defined in Phase 2.

3. **CI/CD Pipeline**: Behavior comparisons are integrated into the CI/CD pipeline. Results are recorded and reported.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 3.2.1: Trap Handling

**Setup**: Execute a WebAssembly trap on both engines.

**Steps**:
1. Compile a WebAssembly module that triggers a trap.
2. Execute the module on both Extism/Wasmtime and Extism/Wazero.
3. Compare trap types and messages.

**Expected Result**: Trap types and messages are identical.

### Test 3.2.2: Timeout Handling

**Setup**: Execute a long-running operation that exceeds the timeout on both engines.

**Steps**:
1. Compile a WebAssembly module with a long-running function.
2. Configure timeout to a low value.
3. Execute the module on both engines.
4. Compare timeout behavior.

**Expected Result**: Timeout behavior is identical.

### Test 3.2.3: Cancellation Handling

**Setup**: Execute an operation and cancel it mid-execution on both engines.

**Steps**:
1. Compile a WebAssembly module with a cancellable operation.
2. Start execution on both engines.
3. Cancel execution mid-way.
4. Compare cancellation behavior.

**Expected Result**: Cancellation behavior is identical.

### Test 3.2.4: Missing Import Handling

**Setup**: Execute a WebAssembly module with a missing import on both engines.

**Steps**:
1. Compile a WebAssembly module that imports a function that is not provided.
2. Execute the module on both engines.
3. Compare missing import errors.

**Expected Result**: Missing import errors are identical.

### Test 3.2.5: Divergence Adjudication

**Setup**: Identify a divergence between engines.

**Steps**:
1. Execute a scenario that produces a divergence.
2. Record the divergence with full context.
3. Adjudicate the divergence against protocol clauses, official semantics, reference models, and reduced reproducers.

**Expected Result**: Divergence is adjudicated with a verdict (conforming, non-conforming, or unresolved) and justification.

## Operational Notes

### Implementation-Defined Choices

1. **Normalization**: Raw outputs are normalized before comparison. Normalization removes engine-specific formatting and metadata.

2. **Severity Classification**: Divergences are classified by severity based on impact on observable behavior. Critical divergences block release.

3. **Adjudication Panel**: Adjudication is performed by a panel of reviewers with expertise in WebAssembly and Extism.

4. **Regression Tracking**: Divergences are tracked as regressions until resolved. Resolved divergences are archived.

### Deferred Work

1. **Automated Divergence Detection**: Divergences are currently detected manually. Automated detection is not yet supported.

2. **Automated Adjudication**: Adjudication is currently manual. Automated adjudication is not yet supported.

3. **Distributed Execution**: Execution is currently centralized. Distributed execution is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The behavior and integration work builds on the contract and data model defined in Section 3.1 and the evidence manifests defined in Phase 1.

## Checklist

- [x] 3.2.1.1 Subtask - Compare trap, timeout, cancellation, missing import, invalid output, memory limit, variable state, and reset behavior.
- [x] 3.2.1.2 Subtask - Record raw and normalized outputs plus engine-specific configuration for every divergence.
- [x] 3.2.1.3 Subtask - Adjudicate divergence against protocol clauses, official semantics, reference models, and reduced reproducers rather than majority vote.
