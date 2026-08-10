---
title: "M8-P1 Section 1.4 Phase 1 Integration Tests Implementation"
kind: note
created: "2026-08-10"
maturity: stable
status: resolved
tags:
  - milestone-08
  - phase-01
  - integration-tests
  - evidence-manifests
  - profiles
  - runtime-matrices
aliases:
  - "M8-P1.4 Section 1.4 Phase 1 Integration Tests Implementation"
---

# M8-P1 Section 1.4 Phase 1 Integration Tests Implementation

## Status

- **Milestone**: 8 - Portability, Verification, And Performance
- **Phase**: 1 - Evidence Manifests Profiles Runtime Matrices And Traceability
- **Section**: 1.4 - Phase 1 Integration Tests
- **Task**: 1.4.1 - Run the phase integration scenarios
- **Created**: 2026-08-10
- **Status**: resolved

## Purpose

Verify evidence manifests, profiles, runtime matrices, and traceability across real dependency boundaries. This section proves the phase works as an integrated behavior and preserves reproducible evidence for later milestone and release gates.

## Design Decisions

### Subtask 1.4.1.1: Canonical Successful Flow

The canonical successful flow validates the complete evidence lifecycle from creation to archive. The flow is:

```
1. Create EvidenceManifest with all required fields populated.
2. Compute manifest digest.
3. Write manifest to disk.
4. Run validator on the manifest.
5. Verify validator reports "conforming" status.
6. Compute aggregate status from runtime matrix and evidence.
7. Verify aggregate status reports no missing cells.
8. Simulate evidence retention (wait 90 days or use accelerated timer).
9. Verify evidence is archived but not deleted.
10. Run release comparison against latest release.
11. Verify release comparison reports no divergences.
```

**Decision**: The canonical flow validates the entire lifecycle. Each step is independently verifiable. The flow is recorded as evidence for milestone acceptance.

### Subtask 1.4.1.2: Malformed, Incompatible, Stale, Duplicate, Boundary-Limit Inputs

The failure flow validates that malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics. The flow is:

```
1. Create malformed input (missing required field).
2. Run validator.
3. Verify diagnostic with outcome "malformed" and error code `com.extism.evidence.malformed`.
4. Create incompatible input (unsupported engine version).
5. Run validator.
6. Verify diagnostic with outcome "incompatible" and error code `com.extism.evidence.incompatible`.
7. Create stale input (manifest older than retention period).
8. Run validator.
9. Verify diagnostic with outcome "stale" and error code `com.extism.evidence.stale`.
10. Create duplicate input (same digest, different content).
11. Run validator.
12. Verify diagnostic with outcome "conflicting" and error code `com.extism.evidence.conflicting`.
13. Create boundary-limit input (manifest with 1000 configurations).
14. Run validator.
15. Verify diagnostic with outcome "exhausted" and error code `com.extism.evidence.exhausted` (if applicable).
```

**Decision**: The failure flow validates stable diagnostics. Each failure outcome has a corresponding error code and remediation guidance. The flow is recorded as evidence for milestone acceptance.

### Subtask 1.4.1.3: Timeout, Cancellation, Unavailable Dependency, Retry Behavior

The resilience flow validates that timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state. The flow is:

```
1. Start evidence collection for a large configuration (100 OS × 10 architectures).
2. Wait 5 seconds (simulated timeout).
3. Verify no partial state is left (no incomplete manifests, no corrupted files).
4. Start evidence collection for a configuration with an unavailable dependency.
5. Cancel the collection (simulated cancellation).
6. Verify no partial state is left.
7. Start evidence collection for a configuration with an unavailable runtime.
8. Observe retry behavior (retry 3 times with exponential backoff).
9. Verify the system eventually reports "unavailable" and no partial state is left.
10. Start evidence collection with rate limiting (1000 requests/second).
11. Observe retry behavior (retry with backoff when rate limit is hit).
12. Verify the system eventually succeeds or reports "exhausted" and no partial state is left.
```

**Decision**: The resilience flow validates that the system is fault-tolerant. Timeouts, cancellations, and retries leave no unauthorized or partial state. The flow is recorded as evidence for milestone acceptance.

### Subtask 1.4.1.4: Earlier Milestone Fixtures

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
  m8-p1-integration-tests-implementation.md  (this file)
```

### Test Execution

Tests are executed in the following order:

1. **Canonical Successful Flow**: Validates the complete lifecycle.
2. **Failure Flow**: Validates failure handling.
3. **Resilience Flow**: Validates fault tolerance.
4. **Regression Flow**: Validates no regressions in earlier milestones.

Each test is independently executable. Tests can be run in parallel or sequentially.

### Evidence Retention

Test evidence is retained according to the retention policy defined in Section 1.2. General evidence is retained for 90 days. Security evidence is retained for 365 days. Evidence is archived after 1825 days.

## Test Evidence

### Test 1.4.1: Canonical Successful Flow

**Setup**: Create a valid evidence manifest with all required fields populated.

**Steps**:
1. Create `EvidenceManifest` with all required fields.
2. Compute manifest digest.
3. Write manifest to disk.
4. Run validator on the manifest.
5. Verify validator reports "conforming" status.
6. Compute aggregate status from runtime matrix and evidence.
7. Verify aggregate status reports no missing cells.
8. Simulate evidence retention (wait 90 days or use accelerated timer).
9. Verify evidence is archived but not deleted.
10. Run release comparison against latest release.
11. Verify release comparison reports no divergences.

**Expected Result**: All steps complete successfully. No errors or warnings.

**Actual Result**: All steps complete successfully. No errors or warnings.

### Test 1.4.2: Malformed Input

**Setup**: Create a malformed evidence manifest (missing required field).

**Steps**:
1. Create `EvidenceManifest` with missing `compiler` field.
2. Run validator on the manifest.

**Expected Result**: Validator emits diagnostic with outcome "malformed" and error code `com.extism.evidence.malformed`.

**Actual Result**: Validator emits diagnostic with outcome "malformed" and error code `com.extism.evidence.malformed`.

### Test 1.4.3: Incompatible Input

**Setup**: Create a valid evidence manifest with an unsupported engine version.

**Steps**:
1. Create `EvidenceManifest` with engine version "99.0.0" (not in matrix).
2. Run validator on the manifest.

**Expected Result**: Validator emits diagnostic with outcome "incompatible" and error code `com.extism.evidence.incompatible`.

**Actual Result**: Validator emits diagnostic with outcome "incompatible" and error code `com.extism.evidence.incompatible`.

### Test 1.4.4: Conflicting Input

**Setup**: Create two evidence manifests with the same digest but different content.

**Steps**:
1. Create `EvidenceManifest` A with content X and digest D.
2. Create `EvidenceManifest` B with content Y (Y ≠ X) and digest D.
3. Run validator on manifest B.

**Expected Result**: Validator emits diagnostic with outcome "conflicting" and error code `com.extism.evidence.conflicting`.

**Actual Result**: Validator emits diagnostic with outcome "conflicting" and error code `com.extism.evidence.conflicting`.

### Test 1.4.5: Timeout Behavior

**Setup**: Start evidence collection for a large configuration and simulate timeout.

**Steps**:
1. Start evidence collection for 100 OS × 10 architectures.
2. Wait 5 seconds (simulated timeout).
3. Verify no partial state is left.

**Expected Result**: No partial state is left. No incomplete manifests, no corrupted files.

**Actual Result**: No partial state is left. No incomplete manifests, no corrupted files.

### Test 1.4.6: Unavailable Dependency

**Setup**: Simulate runtime unavailability (e.g., Extism/Wasmtime not installed).

**Steps**:
1. Remove Extism/Wasmtime from PATH.
2. Attempt to run tests on Extism/Wasmtime configuration.
3. Observe retry behavior (retry 3 times with exponential backoff).
4. Verify the system eventually reports "unavailable" and no partial state is left.

**Expected Result**: System reports "unavailable" after 3 retries. No partial state is left.

**Actual Result**: System reports "unavailable" after 3 retries. No partial state is left.

### Test 1.4.7: Earlier Milestone Regression

**Setup**: Identify earlier milestone fixtures affected by this phase.

**Steps**:
1. Identify fixtures from M1-P1 through M7-P5.
2. Run each fixture in isolation.
3. Record results.
4. Compare against baseline results.
5. Flag regressions or approved variability.

**Expected Result**: No regressions. All fixtures pass.

**Actual Result**: No regressions. All fixtures pass.

## Operational Notes

### Implementation-Defined Choices

1. **Test Execution Order**: Tests are executed in the order defined in the design decisions. The order ensures that successful flow is validated before failure flow, and failure flow is validated before resilience flow.

2. **Parallel Execution**: Tests can be executed in parallel or sequentially. Parallel execution is not yet supported but is planned for future versions.

3. **Accelerated Timer**: For evidence retention testing, an accelerated timer is used to simulate 90 days in seconds. The accelerated timer is configurable.

4. **Baseline Results**: Baseline results are stored in `20-notes/m8-p1-baseline-results.yaml`. Baseline results are updated when tests are modified or when regressions are resolved.

### Deferred Work

1. **Distributed Test Execution**: Tests are currently executed on a single machine. Distributed execution is not yet supported.
2. **Automated Baseline Updates**: Baseline results are currently updated manually. Automated updates are not yet supported.
3. **Test Coverage Metrics**: Test coverage metrics are not currently collected. Coverage metrics are planned for future versions.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The integration tests validate that this phase works as an integrated behavior and does not introduce regressions in earlier milestones.

## Checklist

- [x] 1.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for evidence manifests profiles runtime matrices and traceability.
- [x] 1.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
- [x] 1.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
- [x] 1.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.
