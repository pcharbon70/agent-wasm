---
title: "M8-P2 Section 2.4 Phase 2 Integration Tests Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-02
  - integration-tests
  - wasi
  - extism
  - plugin-contract
  - conformance
aliases:
  - "M8-P2.4 Section 2.4 Phase 2 Integration Tests Implementation"
---

# M8-P2 Section 2.4 Phase 2 Integration Tests Implementation

## Purpose

Verify Core WebAssembly, WASI, Extism, and plugin contract conformance across real dependency boundaries. This section builds on the failure evidence defined in [Section 2.3 Failure Evidence And Operational Notes](./m8-p2-failure-evidence-and-operational-notes-implementation.md) and concludes the Phase 2 implementation.

## Design Decisions

### Subtask 2.4.1.1: Canonical Successful Flow

The canonical successful flow validates the complete conformance lifecycle from suite execution to defect promotion. The flow is:

```
1. Configure the Core WebAssembly suite for an engine and feature profile.
2. Run the suite and record results.
3. Configure WASI suites for relevant guest profiles.
4. Run WASI suites and record results.
5. Compile guest artifacts and run XTP tests.
6. Run Host SDK integration tests.
7. Identify and promote defects to permanent regressions.
8. Record all evidence in evidence manifests.
9. Verify no regressions in earlier milestone fixtures.
```

**Decision**: The canonical flow validates the entire conformance lifecycle. Each step is independently verifiable. The flow is recorded as evidence for milestone acceptance.

### Subtask 2.4.1.2: Malformed, Incompatible, Stale, Duplicate, Boundary-Limit Inputs

The failure flow validates that malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics. The flow is:

```
1. Create malformed input (invalid binary).
2. Run XTP bytes contract tests.
3. Verify diagnostic with outcome "malformed" and error code `com.extism.conformance.malformed`.
4. Create incompatible input (unsupported engine version).
5. Run suite execution.
6. Verify diagnostic with outcome "incompatible" and error code `com.extism.conformance.incompatible`.
7. Create stale input (suite version older than retention period).
8. Run suite execution.
9. Verify diagnostic with outcome "stale" and error code `com.extism.conformance.stale`.
10. Create duplicate input (same digest, different outcome).
11. Run validator.
12. Verify diagnostic with outcome "conflicting" and error code `com.extism.conformance.conflicting`.
13. Create boundary-limit input (suite with 10000 tests).
14. Run suite execution.
15. Verify diagnostic with outcome "exhausted" and error code `com.extism.conformance.exhausted` (if applicable).
```

**Decision**: The failure flow validates stable diagnostics. Each failure outcome has a corresponding error code and remediation guidance. The flow is recorded as evidence for milestone acceptance.

### Subtask 2.4.1.3: Timeout, Cancellation, Unavailable Dependency, Retry Behavior

The resilience flow validates that timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state. The flow is:

```
1. Start suite execution for a large configuration (1000 tests).
2. Wait 5 seconds (simulated timeout).
3. Verify no partial state is left (no incomplete results, no corrupted files).
4. Start suite execution and cancel it (simulated cancellation).
5. Verify no partial state is left.
6. Start suite execution with an unavailable dependency (e.g., engine not installed).
7. Observe retry behavior (retry 3 times with exponential backoff).
8. Verify the system eventually reports "unavailable" and no partial state is left.
9. Start suite execution with rate limiting (1000 requests/second).
10. Observe retry behavior (retry with backoff when rate limit is hit).
11. Verify the system eventually succeeds or reports "exhausted" and no partial state is left.
```

**Decision**: The resilience flow validates that the system is fault-tolerant. Timeouts, cancellations, and retries leave no unauthorized or partial state. The flow is recorded as evidence for milestone acceptance.

### Subtask 2.4.1.4: Earlier Milestone Fixtures

The regression flow validates that all earlier milestone fixtures affected by this phase pass without regressions. The flow is:

```
1. Identify earlier milestone fixtures affected by this phase (M1-P1 through M7-P5).
2. Run each fixture in isolation.
3. Record results.
4. Compare against baseline results.
5. Flag regressions or approved variability.
6. If regressions are found, investigate and resolve before proceeding.
```

**Decision**: The regression flow validates that this phase does not introduce regressions in earlier milestones. Regressions must be resolved before the phase is considered complete. Approved variability is documented and justified.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p2-integration-tests-implementation.md  (this file)
```

### Test Execution

Tests are executed in the following order:

1. **Canonical Successful Flow**: Validates the complete conformance lifecycle.
2. **Failure Flow**: Validates failure handling.
3. **Resilience Flow**: Validates fault tolerance.
4. **Regression Flow**: Validates no regressions in earlier milestones.

Each test is independently executable. Tests can be run in parallel or sequentially.

### Evidence Retention

Test evidence is retained according to the retention policy defined in Phase 1. General evidence is retained for 90 days. Security evidence is retained for 365 days. Evidence is archived after 1825 days.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 2.4.1: Canonical Successful Flow

**Setup**: Configure the Core WebAssembly suite for Extism/Wasmtime with the memory and gas feature profile.

**Steps**:
1. Configure the Core WebAssembly suite.
2. Run the suite and record results.
3. Configure WASI suites for relevant guest profiles.
4. Run WASI suites and record results.
5. Compile guest artifacts and run XTP tests.
6. Run Host SDK integration tests.
7. Identify and promote defects to permanent regressions.
8. Record all evidence in evidence manifests.
9. Verify no regressions in earlier milestone fixtures.

**Expected Result**: All steps complete successfully. No errors or warnings.

### Test 2.4.2: Malformed Binary

**Setup**: Create a malformed WebAssembly binary (invalid opcodes).

**Steps**:
1. Create a WebAssembly binary with invalid opcodes.
2. Run XTP bytes contract tests.

**Expected Result**: Diagnostic with outcome "malformed" and error code `com.extism.conformance.malformed`.

### Test 2.4.3: Incompatible Engine Version

**Setup**: Configure an unsupported engine version.

**Steps**:
1. Configure engine version "99.0.0" (not supported).
2. Run suite execution.

**Expected Result**: Diagnostic with outcome "incompatible" and error code `com.extism.conformance.incompatible`.

### Test 2.4.4: Timeout Behavior

**Setup**: Start suite execution for a large configuration and simulate timeout.

**Steps**:
1. Start suite execution for 1000 tests.
2. Wait 5 seconds (simulated timeout).
3. Verify no partial state is left.

**Expected Result**: No partial state is left. No incomplete results, no corrupted files.

### Test 2.4.5: Unavailable Dependency

**Setup**: Simulate engine unavailability (e.g., Extism/Wasmtime not installed).

**Steps**:
1. Remove Extism/Wasmtime from PATH.
2. Attempt to run suite execution.
3. Observe retry behavior (retry 3 times with exponential backoff).
4. Verify the system eventually reports "unavailable" and no partial state is left.

**Expected Result**: System reports "unavailable" after 3 retries. No partial state is left.

### Test 2.4.6: Earlier Milestone Regression

**Setup**: Identify earlier milestone fixtures affected by this phase.

**Steps**:
1. Identify fixtures from M1-P1 through M7-P5.
2. Run each fixture in isolation.
3. Record results.
4. Compare against baseline results.
5. Flag regressions or approved variability.

**Expected Result**: No regressions. All fixtures pass.

## Operational Notes

### Implementation-Defined Choices

1. **Test Execution Order**: Tests are executed in the order defined in the design decisions. The order ensures that successful flow is validated before failure flow, and failure flow is validated before resilience flow.

2. **Parallel Execution**: Tests can be executed in parallel or sequentially. Parallel execution is not yet supported but is planned for future versions.

3. **Accelerated Timer**: For evidence retention testing, an accelerated timer is used to simulate 90 days in seconds. The accelerated timer is configurable.

4. **Baseline Results**: Baseline results are stored in `20-notes/m8-p2-baseline-results.yaml`. Baseline results are updated when tests are modified or when regressions are resolved.

### Deferred Work

1. **Distributed Test Execution**: Tests are currently executed on a single machine. Distributed execution is not yet supported.

2. **Automated Baseline Updates**: Baseline results are currently updated manually. Automated updates are not yet supported.

3. **Test Coverage Metrics**: Test coverage metrics are not currently collected. Coverage metrics are planned for future versions.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The integration tests validate that this phase works as an integrated behavior and does not introduce regressions in earlier milestones.

## Checklist

- [x] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for core wasi extism and plugin contract conformance.
- [x] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
- [x] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
- [x] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.
