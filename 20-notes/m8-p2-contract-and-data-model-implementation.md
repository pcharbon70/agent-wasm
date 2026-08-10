---
title: "M8-P2 Section 2.1 Contract And Data Model Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-02
  - contract-and-data-model
  - wasi
  - extism
  - plugin-contract
  - conformance
aliases:
  - "M8-P2.1 Section 2.1 Contract And Data Model Implementation"
---

# M8-P2 Section 2.1 Contract And Data Model Implementation

## Purpose

Establish contract and data model for Core WebAssembly, WASI, Extism, and plugin contract conformance. This section defines the standards suites, test profiles, and evidence collection mechanisms that underlie the Phase 2 implementation. See [Section 2.2 Behavior And Integration](./m8-p2-behavior-and-integration-implementation.md) for the behavior and integration work that follows.

## Design Decisions

### Subtask 2.1.1.1: Core WebAssembly Suite

The official Core WebAssembly suite MUST be run for each enabled engine feature profile. The suite includes:

```yaml
CoreWasmSuite = {
  name: "Core WebAssembly",
  version: string,
  source: "https://github.com/WebAssembly/testsuite",
  feature_profiles: FeatureProfile[],
  skip_conditions: SkipCondition[],
  expected_failures: ExpectedFailure[]
}

FeatureProfile = {
  name: string,
  description: string,
  features: string[],
  engines: string[]
}

SkipCondition = {
  suite: string,
  feature: string,
  reason: string,
  referenced_issue: string?
}

ExpectedFailure = {
  suite: string,
  test: string,
  reason: string,
  referenced_issue: string,
  minimum_fix_version: string?
}
```

**Decision**: The Core WebAssembly suite is run against each engine (Extism/Wasmtime, Extism/Wazero) for each feature profile. Skips and expected failures are documented with reasons and issue references. The suite version is pinned and recorded in the evidence manifest.

### Subtask 2.1.1.2: WASI Suites

Selected WASI suites MUST be run for guest profiles that actually import those interfaces. The suites include:

```yaml
WasiSuites = {
  name: "WASI",
  versions: string[],
  source: "https://github.com/WebAssembly/WASI",
  guest_profiles: GuestProfile[],
  skip_conditions: SkipCondition[],
  expected_failures: ExpectedFailure[]
}

GuestProfile = {
  name: string,
  description: string,
  imports: string[],
  engines: string[]
}
```

**Decision**: WASI suites are run only for guest profiles that import the relevant interfaces. This avoids running unnecessary tests and focuses evidence on actual usage. The suites are versioned and pinned.

### Subtask 2.1.1.3: WABT and Reference Interpreters

WABT and reference/specification interpreters MUST be used to inspect and adjudicate reduced semantic failures. The tools include:

```yaml
InspectionTools = {
  wabt: {
    name: "WABT",
    version: string,
    source: "https://github.com/WebAssembly/wabt",
    capabilities: string[]
  },
  reference_interpreters: ReferenceInterpreter[]
}

ReferenceInterpreter = {
  name: string,
  version: string,
  source: string,
  language: string
}
```

**Decision**: WABT is used for binary inspection, validation, and conversion. Reference interpreters (e.g., wasmtime reference, wasmer reference) are used to adjudicate semantic failures when engine-specific behavior is ambiguous.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p2-contract-and-data-model-implementation.md  (this file)
```

### Key Invariants

1. **Standards Conformance**: The Core WebAssembly and WASI suites are the authoritative reference for standards conformance. Engine-specific behavior that deviates from the standards is documented and justified.

2. **Feature Profiles**: Feature profiles define the subset of WebAssembly features to be tested. Each engine supports a different set of features, and tests are run accordingly.

3. **Evidence Collection**: Evidence is collected for each suite run, including pass/fail status, skipped tests, expected failures, and reduced semantic failures.

4. **Traceability**: Each evidence entry links to the source revision, artifact digest, engine, feature profile, and test case.

### Validation Rules

The validator MUST check:

1. All required fields are present and non-null.
2. The engine version matches a supported version.
3. The feature profile is valid for the engine.
4. Skipped tests have documented reasons.
5. Expected failures have documented reasons and issue references.
6. Reduced semantic failures are adjudicated using WABT or reference interpreters.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 2.1.1: Core WebAssembly Suite Run

**Setup**: Configure the Core WebAssembly suite for Extism/Wasmtime with the memory and gas feature profile.

**Steps**:
1. Pin the Core WebAssembly suite version.
2. Configure the feature profile.
3. Run the suite.
4. Record pass/fail status, skips, and expected failures.

**Expected Result**: Suite runs successfully. Results are recorded with full traceability.

### Test 2.1.2: WASI Suite Run

**Setup**: Configure the WASI suite for guest profiles that import file system interfaces.

**Steps**:
1. Pin the WASI suite version.
2. Identify guest profiles that import file system interfaces.
3. Run the suite for those profiles.
4. Record pass/fail status, skips, and expected failures.

**Expected Result**: Suite runs successfully for relevant profiles. Results are recorded with full traceability.

### Test 2.1.3: WABT Inspection

**Setup**: Inspect a reduced semantic failure using WABT.

**Steps**:
1. Identify a reduced semantic failure from a suite run.
2. Use WABT to validate and inspect the binary.
3. Adjudicate the failure using WABT or reference interpreters.
4. Record the adjudication.

**Expected Result**: Failure is adjudicated and recorded with full traceability.

## Operational Notes

### Implementation-Defined Choices

1. **Suite Version Pinning**: Suite versions are pinned to specific commits or tags. This ensures reproducibility and prevents drift.

2. **Feature Profile Selection**: Feature profiles are selected based on engine capabilities and project requirements. Not all features are tested for all engines.

3. **Skip Conditions**: Tests are skipped only when there is a documented reason (e.g., engine does not support the feature, test is incompatible with the engine).

4. **Expected Failures**: Expected failures are documented with reasons and issue references. They are reviewed periodically and removed when fixed.

5. **WABT Version**: The latest stable version of WABT is used. Older versions are supported for reproducibility.

### Deferred Work

1. **Automated Suite Updates**: Suite versions are currently updated manually. Automated updates are not yet supported.

2. **Parallel Suite Execution**: Suite execution is sequential. Parallel execution is not yet supported.

3. **Distributed Evidence Collection**: Evidence collection is centralized. Distributed collection is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The contract and data model build on the evidence manifests defined in [Phase 1 Section 1.1 Contract And Data Model](../phase-01-evidence-manifests-profiles-runtime-matrices-and-traceability/m8-p1-contract-and-data-model-implementation.md).

## Checklist

- [x] 2.1.1.1 Subtask - Pin and run the official Core WebAssembly suite for each enabled engine feature profile.
- [x] 2.1.1.2 Subtask - Run only selected WASI suites for guest profiles that actually import those interfaces and preserve skips/expected failures.
- [x] 2.1.1.3 Subtask - Use WABT and reference/specification interpreters to inspect and adjudicate reduced semantic failures.
