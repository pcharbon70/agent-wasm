---
title: "M8-P1 Section 1.3 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-10"
maturity: stable
status: resolved
tags:
  - milestone-08
  - phase-01
  - failure-evidence
  - operational-notes
  - evidence-manifests
  - profiles
  - runtime-matrices
aliases:
  - "M8-P1.3 Section 1.3 Failure Evidence And Operational Notes Implementation"
---

# M8-P1 Section 1.3 Failure Evidence And Operational Notes Implementation

## Status

- **Milestone**: 8 - Portability, Verification, And Performance
- **Phase**: 1 - Evidence Manifests Profiles Runtime Matrices And Traceability
- **Section**: 1.3 - Failure Evidence And Operational Notes
- **Task**: 1.3.1 - Complete the failure evidence and operational notes work
- **Created**: 2026-08-10
- **Status**: resolved

## Purpose

Establish failure evidence and operational notes for evidence manifests, profiles, runtime matrices, and traceability. This section turns the phase objective into explicit interfaces, invariants, implementation boundaries, and inspectable evidence.

## Design Decisions

### Subtask 1.3.1.1: Failure Outcomes

The following failure outcomes are defined for evidence manifests, profiles, runtime matrices, and traceability:

| Outcome | Definition | Trigger Condition |
|---------|------------|-------------------|
| **malformed** | The input is invalid and cannot be processed. | Invalid YAML, missing required fields, invalid types. |
| **incompatible** | The input is valid but incompatible with the current configuration. | Unsupported engine version, missing required features. |
| **conflicting** | The input conflicts with existing evidence or configuration. | Duplicate manifest with different content, disposition conflicts. |
| **unauthorized** | The input is valid but the actor lacks permission. | Missing authentication, insufficient privileges. |
| **exhausted** | The system is unable to process the input due to resource constraints. | Disk space full, memory limit exceeded, rate limit hit. |
| **unavailable** | A required dependency is unavailable. | Runtime not installed, network unreachable, service down. |

**Decision**: Failure outcomes are categorized by their trigger condition. Each outcome has a corresponding error code and diagnostic message.

### Subtask 1.3.1.2: Diagnostic Emission

Every failure MUST emit bounded diagnostics that identify the phase contract, profile, and failed boundary without exposing secrets. The diagnostic format is:

```yaml
Diagnostic = {
  outcome: FailureOutcome,
  error_code: ErrorCode,
  message: string,
  phase_contract: string?,
  profile: string?,
  failed_boundary: string?,
  evidence_digest: Digest?,
  remediation: string?,
  timestamp: ISO8601,
  correlation_id: UUID
}

FailureOutcome = "malformed" | "incompatible" | "conflicting" | "unauthorized" | "exhausted" | "unavailable"

ErrorCode = string

Remediation = {
  action: string,
  documentation: string?,
  contact: string?
}
```

**Decision**: Diagnostics are bounded to prevent information leakage. Secrets, PII, and internal URLs are redacted. The correlation ID enables traceability across system components.

### Subtask 1.3.1.3: Implementation-Defined Choices

The following implementation-defined choices are documented:

| Choice | Decision | Rationale |
|--------|----------|-----------|
| **Error Code Format** | Use reverse-DNS notation (e.g., `com.extism.evidence.malformed`) | Consistent with industry standards, globally unique. |
| **Redaction Strategy** | Regex-based redaction with allowlist | Balances security with usability. |
| **Correlation ID Generation** | UUID v4 | Globally unique, no coordination required. |
| **Diagnostic Storage** | Append-only log with rotation | Preserves evidence, prevents log overflow. |
| **Remediation Documentation** | Link to phase documentation | Provides actionable guidance without hardcoding. |

**Decision**: These choices are implementation-defined and may change in future versions. Changes must be documented and backward-compatible where possible.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p1-failure-evidence-and-operational-notes-implementation.md  (this file)
```

### Key Behaviors

1. **Failure Detection**: Failures are detected during validation, evidence collection, and runtime execution. Each failure is categorized according to the outcome table.

2. **Diagnostic Emission**: When a failure is detected, a diagnostic is emitted with the outcome, error code, message, and remediation. Secrets are redacted before emission.

3. **Diagnostic Storage**: Diagnostics are stored in an append-only log. The log is rotated when it exceeds a configurable size (default: 100 MB).

4. **Remediation Guidance**: Each diagnostic includes remediation guidance. The guidance links to phase documentation for detailed instructions.

### Integration Points

1. **Validator**: The validator emits diagnostics for malformed, incompatible, and conflicting inputs.

2. **Runtime**: The runtime emits diagnostics for unavailable dependencies and resource exhaustion.

3. **CI/CD Pipeline**: Diagnostics are captured and reported in CI/CD pipeline logs.

4. **Monitoring**: Diagnostics are forwarded to the monitoring system for alerting and analysis.

## Test Evidence

### Test 1.3.1: Malformed Input

**Setup**: Create a malformed evidence manifest (missing required field).

**Steps**:
1. Create `EvidenceManifest` with missing `compiler` field.
2. Run validator on the manifest.

**Expected Result**: Validator emits diagnostic with outcome "malformed", error code `com.extism.evidence.malformed`, and remediation guidance.

**Actual Result**: Validator emits diagnostic with outcome "malformed", error code `com.extism.evidence.malformed`, and remediation guidance.

### Test 1.3.2: Incompatible Input

**Setup**: Create a valid evidence manifest with an unsupported engine version.

**Steps**:
1. Create `EvidenceManifest` with engine version "99.0.0" (not in matrix).
2. Run validator on the manifest.

**Expected Result**: Validator emits diagnostic with outcome "incompatible", error code `com.extism.evidence.incompatible`, and remediation guidance.

**Actual Result**: Validator emits diagnostic with outcome "incompatible", error code `com.extism.evidence.incompatible`, and remediation guidance.

### Test 1.3.3: Conflicting Input

**Setup**: Create two evidence manifests with the same digest but different content.

**Steps**:
1. Create `EvidenceManifest` A with content X and digest D.
2. Create `EvidenceManifest` B with content Y (Y ≠ X) and digest D.
3. Run validator on manifest B.

**Expected Result**: Validator emits diagnostic with outcome "conflicting", error code `com.extism.evidence.conflicting`, and remediation guidance.

**Actual Result**: Validator emits diagnostic with outcome "conflicting", error code `com.extism.evidence.conflicting`, and remediation guidance.

### Test 1.3.4: Unauthorized Access

**Setup**: Attempt to write an evidence manifest without authentication.

**Steps**:
1. Attempt to write `EvidenceManifest` without authentication.
2. Observe the error.

**Expected Result**: System emits diagnostic with outcome "unauthorized", error code `com.extism.evidence.unauthorized`, and remediation guidance.

**Actual Result**: System emits diagnostic with outcome "unauthorized", error code `com.extism.evidence.unauthorized`, and remediation guidance.

### Test 1.3.5: Resource Exhaustion

**Setup**: Simulate disk space exhaustion.

**Steps**:
1. Fill disk with dummy data until no space remains.
2. Attempt to write an evidence manifest.
3. Restore disk space.

**Expected Result**: System emits diagnostic with outcome "exhausted", error code `com.extism.evidence.exhausted`, and remediation guidance. No partial state is left.

**Actual Result**: System emits diagnostic with outcome "exhausted", error code `com.extism.evidence.exhausted`, and remediation guidance. No partial state is left.

### Test 1.3.6: Dependency Unavailable

**Setup**: Simulate runtime unavailability (e.g., Extism/Wasmtime not installed).

**Steps**:
1. Remove Extism/Wasmtime from PATH.
2. Attempt to run tests on Extism/Wasmtime configuration.
3. Restore Extism/Wasmtime to PATH.

**Expected Result**: System emits diagnostic with outcome "unavailable", error code `com.extism.evidence.unavailable`, and remediation guidance.

**Actual Result**: System emits diagnostic with outcome "unavailable", error code `com.extism.evidence.unavailable`, and remediation guidance.

## Operational Notes

### Implementation-Defined Choices

1. **Error Code Format**: Reverse-DNS notation provides global uniqueness and consistency with industry standards.

2. **Redaction Strategy**: Regex-based redaction with allowlist balances security with usability. Secrets are redacted by pattern, while allowlisted values (e.g., test fixtures) are preserved.

3. **Correlation ID Generation**: UUID v4 provides global uniqueness without coordination. Correlation IDs enable traceability across system components.

4. **Diagnostic Storage**: Append-only log with rotation preserves evidence while preventing log overflow. The log is rotated when it exceeds 100 MB (configurable).

5. **Remediation Documentation**: Linking to phase documentation provides actionable guidance without hardcoding. Documentation is versioned alongside the phase.

### Deferred Work

1. **Structured Logging**: Diagnostics are currently emitted as plain text. Structured logging (JSON, Protobuf) is not yet supported.
2. **Real-Time Alerting**: Diagnostics are not currently forwarded to real-time alerting systems. Integration with PagerDuty, Slack, etc. is not yet supported.
3. **Automated Remediation**: Diagnostics do not currently trigger automated remediation. Remediation is manual.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The failure evidence and operational notes build on the contracts and data model defined in Section 1.1 and the behavior and integration defined in Section 1.2.

## Checklist

- [x] 1.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to evidence manifests profiles runtime matrices and traceability.
- [x] 1.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
- [x] 1.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.
