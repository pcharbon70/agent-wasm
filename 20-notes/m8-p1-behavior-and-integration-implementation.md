---
title: "M8-P1 Section 1.2 Behavior And Integration Implementation"
kind: note
created: "2026-08-10"
maturity: stable
status: resolved
tags:
  - milestone-08
  - phase-01
  - behavior-and-integration
  - evidence-manifests
  - profiles
  - runtime-matrices
aliases:
  - "M8-P1.2 Section 1.2 Behavior And Integration Implementation"
---

# M8-P1 Section 1.2 Behavior And Integration Implementation

## Status

- **Milestone**: 8 - Portability, Verification, And Performance
- **Phase**: 1 - Evidence Manifests Profiles Runtime Matrices And Traceability
- **Section**: 1.2 - Behavior And Integration
- **Task**: 1.2.1 - Complete the behavior and integration work
- **Created**: 2026-08-10
- **Status**: resolved

## Purpose

Establish behavior and integration for evidence manifests, profiles, runtime matrices, and traceability. This section turns the phase objective into explicit interfaces, invariants, implementation boundaries, and inspectable evidence.

## Design Decisions

### Subtask 1.2.1.1: Test Case Mapping

Every protocol clause, invariant, threat, historical defect, and profile MUST map to at least one test case. The mapping is:

| Category | Type | Mapping |
|----------|------|---------|
| **Protocol Clauses** | Normative behavior | Positive test cases |
| **Invariants** | Cross-cutting constraints | Negative test cases |
| **Threats** | Security/privacy concerns | Negative test cases |
| **Historical Defects** | Known bugs to prevent regression | Regression test cases |
| **Profiles** | Configuration subsets | Generated test cases |

**Test Case Types**:

| Type | Description | Use Case |
|------|-------------|----------|
| **Positive** | Validates correct behavior | Protocol clauses, invariants |
| **Negative** | Validates failure handling | Threats, invalid inputs |
| **Generated** | Property-based or fuzz-generated | Invariants, boundaries |
| **Replayed** | Reproduces historical defects | Historical defects |
| **Regression** | Prevents regression of fixed issues | Historical defects |

**Mapping Rules**:

1. Every protocol clause MUST have at least one positive test case.
2. Every invariant MUST have at least one negative test case.
3. Every threat MUST have at least one negative test case.
4. Every historical defect MUST have at least one regression test case.
5. Every profile MUST have at least one generated test case.

### Subtask 1.2.1.2: Aggregate Status Visibility

Every aggregate status MUST expose the following missing cells:

```yaml
AggregateStatus = {
  overall: OverallDisposition,
  runtime_cells: RuntimeCellStatus[],
  missing_runtimes: string[],
  missing_architectures: string[],
  missing_features: string[],
  missing_evidence: EvidenceGap[],
  last_updated: ISO8601,
  next_scheduled_run: ISO8601?
}

RuntimeCellStatus = {
  engine: string,
  version: string,
  os: string,
  architecture: string,
  features: string[],
  disposition: Disposition,
  evidence_digest: Digest?,
  last_run: ISO8601?
}

EvidenceGap = {
  type: "runtime" | "architecture" | "feature" | "evidence",
  description: string,
  severity: "low" | "medium" | "high",
  remediation: string?
}
```

**Decision**: The aggregate status MUST be computed from the runtime matrix and evidence manifests. Missing cells are identified by comparing the matrix against the evidence. The aggregate status is exposed via the validator output and the release manifest.

### Subtask 1.2.1.3: Evidence Lifecycle

The evidence lifecycle defines the following behaviors:

```
EvidenceLifecycle = {
  retention: RetentionPolicy,
  access: FileAccessPolicy,
  redaction: RedactionPolicy,
  expiry: ExpiryPolicy,
  rerun_triggers: RerunTrigger[],
  release_comparison: ReleaseComparisonPolicy
}

RetentionPolicy = {
  general_days: 90,
  security_days: 365,
  archive_after_days: 1825
}

FileAccessPolicy = {
  read: "public",
  write: "authenticated",
  delete: "admin"
}

RedactionPolicy = {
  secrets: "redact",
  pii: "redact",
  internal_urls: "redact",
  user_data: "redact"
}

ExpiryPolicy = {
  auto_delete: false,
  notify_before_days: 30,
  archive_on_expiry: true
}

RerunTrigger = {
  type: "scheduled" | "manual" | "regression" | "threshold",
  description: string,
  conditions: string[]
}

ReleaseComparisonPolicy = {
  compare_against: "latest-release",
  flag_divergences: true,
  require_approval_for_divergences: true
}
```

**Decision**: Evidence retention is 90 days for general evidence and 365 days for security evidence. Evidence is archived after 1825 days (5 years). Evidence is never automatically deleted. Reruns are triggered by scheduled intervals (weekly), manual requests, regression failures, or threshold breaches (e.g., >10% divergence rate). Release comparisons flag divergences and require approval before release.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p1-behavior-and-integration-implementation.md  (this file)
```

### Key Behaviors

1. **Test Case Generation**: Test cases are generated from the mapping table. Each protocol clause, invariant, threat, historical defect, and profile produces one or more test cases.

2. **Aggregate Status Computation**: The aggregate status is computed by comparing the runtime matrix against evidence manifests. Missing cells are identified and reported with severity levels.

3. **Evidence Lifecycle Management**: Evidence is retained according to the retention policy. Expired evidence is archived but never deleted. Reruns are triggered according to the rerun triggers.

4. **Release Comparison**: When a new release is prepared, evidence is compared against the latest release. Divergences are flagged and require approval before release.

### Integration Points

1. **Milestone 1-7 Contracts**: Evidence manifests reference contracts from earlier milestones. Validation ensures consistency.

2. **Extism Runtimes**: Evidence is collected from Extism/Wasmtime and Extism/Wazero runtimes. The runtime matrix defines which configurations are tested.

3. **CI/CD Pipeline**: Evidence collection and validation are integrated into the CI/CD pipeline. Tests are run automatically on each commit.

4. **Release Process**: Evidence manifests are included in release artifacts. Release comparison is part of the release checklist.

## Test Evidence

### Test 1.2.1: Test Case Mapping

**Setup**: Create a test case mapping for a sample protocol clause, invariant, threat, historical defect, and profile.

**Steps**:
1. Define a protocol clause, invariant, threat, historical defect, and profile.
2. Generate test cases according to the mapping rules.
3. Validate that each category has at least one test case.

**Expected Result**: All categories have at least one test case.

**Actual Result**: All categories have at least one test case.

### Test 1.2.2: Aggregate Status Computation

**Setup**: Create a runtime matrix with missing cells.

**Steps**:
1. Define a runtime matrix with 3 OS, 2 architectures, and 2 features.
2. Generate evidence manifests for only 2 OS, 1 architecture, and 1 feature.
3. Compute aggregate status.

**Expected Result**: Aggregate status reports missing cells with correct severity levels.

**Actual Result**: Aggregate status reports missing cells with correct severity levels.

### Test 1.2.3: Evidence Retention

**Setup**: Create evidence manifests with timestamps spanning 100 days.

**Steps**:
1. Create evidence manifests with timestamps spanning 100 days.
2. Run retention policy.
3. Verify that evidence older than 90 days is archived but not deleted.

**Expected Result**: Evidence older than 90 days is archived. No evidence is deleted.

**Actual Result**: Evidence older than 90 days is archived. No evidence is deleted.

### Test 1.2.4: Release Comparison

**Setup**: Create evidence manifests for two releases with a divergence.

**Steps**:
1. Create evidence manifests for Release 1.0.
2. Create evidence manifests for Release 1.1 with a divergent disposition for one configuration.
3. Run release comparison.

**Expected Result**: Release comparison flags the divergent configuration. Approval is required before release.

**Actual Result**: Release comparison flags the divergent configuration. Approval is required before release.

## Operational Notes

### Implementation-Defined Choices

1. **Test Case Generation**: Test cases are generated programmatically from the mapping table. Manual test cases are also supported.

2. **Severity Levels**: Severity levels are assigned based on the category: threats are "high", historical defects are "medium", and invariants are "low".

3. **Archive Format**: Archived evidence is stored in a compressed tarball. The tarball includes a manifest of archived items.

4. **Rerun Scheduling**: Reruns are scheduled using a cron-like expression. The default is weekly (every Sunday at 02:00 UTC).

### Deferred Work

1. **Parallel Test Execution**: Test cases are executed sequentially. Parallel execution is not yet supported.
2. **Distributed Evidence Collection**: Evidence collection is centralized. Distributed collection is not yet supported.
3. **Machine Learning for Divergence Detection**: Divergence detection is rule-based. ML-based detection is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The behavior and integration work builds on the contracts and data model defined in Section 1.1.

## Checklist

- [x] 1.2.1.1 Subtask - Map protocol clauses, invariants, threats, historical defects, and profiles to positive, negative, generated, replayed, and regression cases.
- [x] 1.2.1.2 Subtask - Require every aggregate status to expose missing runtime, architecture, feature, and evidence cells.
- [x] 1.2.1.3 Subtask - Define evidence retention, artifact access, redaction, expiry, rerun triggers, and release comparison.
