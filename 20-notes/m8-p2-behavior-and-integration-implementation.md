---
title: "M8-P2 Section 2.2 Behavior And Integration Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-02
  - behavior-and-integration
  - wasi
  - extism
  - plugin-contract
  - conformance
aliases:
  - "M8-P2.2 Section 2.2 Behavior And Integration Implementation"
---

# M8-P2 Section 2.2 Behavior And Integration Implementation

## Purpose

Establish behavior and integration for Core WebAssembly, WASI, Extism, and plugin contract conformance. This section builds on the contract and data model defined in [Section 2.1 Contract And Data Model](./m8-p2-contract-and-data-model-implementation.md) and precedes the failure evidence defined in [Section 2.3 Failure Evidence And Operational Notes](./m8-p2-failure-evidence-and-operational-notes-implementation.md).

## Design Decisions

### Subtask 2.2.1.1: XTP Test Execution

Compiled guest artifacts MUST be run through XTP (Extism Test Protocol) for the following contracts:

```yaml
XtpContracts = {
  exports: {
    description: "Verify exported functions and memory",
    tests: string[],
    expected_outcomes: string[]
  },
  bytes: {
    description: "Verify binary format and validation",
    tests: string[],
    expected_outcomes: string[]
  },
  state: {
    description: "Verify instance state and lifecycle",
    tests: string[],
    expected_outcomes: string[]
  },
  error: {
    description: "Verify error handling and reporting",
    tests: string[],
    expected_outcomes: string[]
  },
  mock_host: {
    description: "Verify mock host integration",
    tests: string[],
    expected_outcomes: string[]
  },
  timeout: {
    description: "Verify timeout handling",
    tests: string[],
    expected_outcomes: string[]
  },
  malformed_input: {
    description: "Verify malformed input handling",
    tests: string[],
    expected_outcomes: string[]
  }
}
```

**Decision**: XTP tests validate the Extism plugin contract at the binary level. Each contract has a set of tests and expected outcomes. The tests are run against each engine and feature profile.

### Subtask 2.2.1.2: Host SDK Integration

Equivalent native Host SDK integration cases MUST be run for:

```yaml
HostSdkIntegration = {
  callbacks: {
    description: "Verify real callbacks",
    tests: string[],
    expected_outcomes: string[]
  },
  cancellation: {
    description: "Verify cancellation",
    tests: string[],
    expected_outcomes: string[]
  },
  manifests: {
    description: "Verify manifest parsing and validation",
    tests: string[],
    expected_outcomes: string[]
  },
  limits: {
    description: "Verify limit enforcement",
    tests: string[],
    expected_outcomes: string[]
  },
  lifecycle: {
    description: "Verify instance lifecycle",
    tests: string[],
    expected_outcomes: string[]
  }
}
```

**Decision**: Host SDK integration tests validate the Extism host SDK at the API level. Each integration area has a set of tests and expected outcomes. The tests are run against the native host SDK.

### Subtask 2.2.1.3: Defect Promotion

Upstream or project defects MUST be promoted into minimized permanent regressions with source and profile provenance:

```yaml
DefectPromotion = {
  source: {
    description: "Source of the defect",
    url: string?,
    issue_number: string?,
    author: string?,
    date: ISO8601
  },
  profile: {
    description: "Profile that exposes the defect",
    engine: string,
    feature_profile: string,
    guest_profile: string?
  },
  regression: {
    description: "Minimized regression test",
    artifact_digest: Digest,
    test_case: string,
    expected_outcome: string,
    actual_outcome: string,
    status: "open" | "closed"
  }
}
```

**Decision**: Defects are promoted to permanent regressions to prevent reintroduction. Each regression includes source provenance, profile provenance, and a minimized test case. The regression is tracked until fixed.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p2-behavior-and-integration-implementation.md  (this file)
```

### Key Behaviors

1. **XTP Test Execution**: Compiled guest artifacts are run through XTP for each contract. The tests validate the Extism plugin contract at the binary level.

2. **Host SDK Integration**: Native Host SDK integration cases are run for each integration area. The tests validate the Extism host SDK at the API level.

3. **Defect Promotion**: Upstream or project defects are promoted to permanent regressions. Each regression includes source and profile provenance.

### Integration Points

1. **Phase 1 Evidence Manifests**: XTP and Host SDK test results are recorded in evidence manifests defined in Phase 1.

2. **Core WebAssembly Suite**: XTP tests are run alongside the Core WebAssembly suite. Results are correlated to identify engine-specific behavior.

3. **WASI Suites**: Host SDK integration tests are run alongside WASI suites. Results are correlated to identify WASI-specific behavior.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 2.2.1: XTP Exports Contract

**Setup**: Compile a guest artifact with exported functions and memory.

**Steps**:
1. Compile a guest artifact with exported functions and memory.
2. Run XTP exports contract tests.
3. Verify exported functions and memory are accessible.

**Expected Result**: All exports contract tests pass.

### Test 2.2.2: XTP Timeout Contract

**Setup**: Compile a guest artifact with a long-running function.

**Steps**:
1. Compile a guest artifact with a long-running function.
2. Run XTP timeout contract tests.
3. Verify timeout is enforced and reported correctly.

**Expected Result**: All timeout contract tests pass.

### Test 2.2.3: Host SDK Callbacks

**Setup**: Configure the Host SDK with a real callback.

**Steps**:
1. Configure the Host SDK with a real callback.
2. Run Host SDK callbacks integration tests.
3. Verify callbacks are invoked correctly.

**Expected Result**: All callbacks integration tests pass.

### Test 2.2.4: Host SDK Limits

**Setup**: Configure the Host SDK with memory and gas limits.

**Steps**:
1. Configure the Host SDK with memory and gas limits.
2. Run Host SDK limits integration tests.
3. Verify limits are enforced correctly.

**Expected Result**: All limits integration tests pass.

### Test 2.2.5: Defect Promotion

**Setup**: Identify an upstream or project defect.

**Steps**:
1. Identify an upstream or project defect.
2. Create a minimized regression test.
3. Record source and profile provenance.
4. Promote the defect to a permanent regression.

**Expected Result**: Defect is promoted to a permanent regression with full provenance.

## Operational Notes

### Implementation-Defined Choices

1. **XTP Version**: The latest stable version of XTP is used. Older versions are supported for reproducibility.

2. **Host SDK Version**: The latest stable version of the Host SDK is used. Older versions are supported for reproducibility.

3. **Defect Minimization**: Defects are minimized to the smallest test case that reproduces the issue. This makes the regression easier to understand and maintain.

4. **Regression Tracking**: Regressions are tracked in the issue tracker. They are reviewed periodically and removed when fixed.

### Deferred Work

1. **Automated Defect Detection**: Defects are currently identified manually. Automated detection is not yet supported.

2. **Automated Regression Creation**: Regression tests are currently created manually. Automated creation is not yet supported.

3. **Distributed Test Execution**: Test execution is centralized. Distributed execution is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The behavior and integration work builds on the contract and data model defined in Section 2.1 and the evidence manifests defined in Phase 1.

## Checklist

- [x] 2.2.1.1 Subtask - Run compiled guest artifacts through XTP for exports, bytes, state, error, mock-host, timeout, and malformed-input contracts.
- [x] 2.2.1.2 Subtask - Run equivalent native Host SDK integration cases for real callbacks, cancellation, manifests, limits, and lifecycle.
- [x] 2.2.1.3 Subtask - Promote upstream or project defects into minimized permanent regressions with source and profile provenance.
