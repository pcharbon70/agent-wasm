---
title: "M8-P2 Section 2.3 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-02
  - failure-evidence
  - operational-notes
  - wasi
  - extism
  - plugin-contract
  - conformance
aliases:
  - "M8-P2.3 Section 2.3 Failure Evidence And Operational Notes Implementation"
---

# M8-P2 Section 2.3 Failure Evidence And Operational Notes Implementation

## Purpose

Establish failure evidence and operational notes for Core WebAssembly, WASI, Extism, and plugin contract conformance. This section builds on the behavior and integration defined in [Section 2.2 Behavior And Integration](./m8-p2-behavior-and-integration-implementation.md) and precedes the integration tests defined in [Section 2.4 Phase 2 Integration Tests](./m8-p2-integration-tests-implementation.md).

## Design Decisions

### Subtask 2.3.1.1: Failure Outcomes

The following failure outcomes are defined for Core WebAssembly, WASI, Extism, and plugin contract conformance:

| Outcome | Definition | Trigger Condition |
|---------|------------|-------------------|
| **malformed** | The input is invalid and cannot be processed. | Invalid binary, missing required exports, incompatible interface. |
| **incompatible** | The input is valid but incompatible with the current configuration. | Unsupported engine version, missing required features, incompatible WASI version. |
| **stale** | The input is valid but has exceeded the retention period. | Artifact version older than retention period, divergence record older than review period. |
| **conflicting** | The input conflicts with existing evidence or configuration. | Duplicate test result with different outcome, conflicting feature profile. |
| **unauthorized** | The input is valid but the actor lacks permission. | Missing authentication, insufficient privileges, unauthorized suite access. |
| **exhausted** | The system is unable to process the input due to resource constraints. | Disk space full, memory limit exceeded, rate limit hit, timeout exceeded. |
| **unavailable** | A required dependency is unavailable. | Engine not installed, suite not available, WABT not installed, reference interpreter not available. |

**Decision**: Failure outcomes are categorized by their trigger condition. Each outcome has a corresponding error code and diagnostic message.

### Subtask 2.3.1.2: Diagnostic Emission

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

FailureOutcome = "malformed" | "incompatible" | "stale" | "conflicting" | "unauthorized" | "exhausted" | "unavailable"

ErrorCode = string

Remediation = {
  action: string,
  documentation: string?,
  contact: string?
}
```

**Decision**: Diagnostics are bounded to prevent information leakage. Secrets, PII, and internal URLs are redacted. The correlation ID enables traceability across system components.

### Subtask 2.3.1.3: Implementation-Defined Choices

The following implementation-defined choices are documented:

| Choice | Decision | Rationale |
|--------|----------|-----------|
| **Error Code Format** | Use reverse-DNS notation (e.g., `com.extism.conformance.malformed`) | Consistent with industry standards, globally unique. |
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
  m8-p2-failure-evidence-and-operational-notes-implementation.md  (this file)
```

### Key Behaviors

1. **Failure Detection**: Failures are detected during suite execution, XTP test execution, Host SDK integration testing, and defect promotion. Each failure is categorized according to the outcome table.

2. **Diagnostic Emission**: When a failure is detected, a diagnostic is emitted with the outcome, error code, message, and remediation. Secrets are redacted before emission.

3. **Diagnostic Storage**: Diagnostics are stored in an append-only log. The log is rotated when it exceeds a configurable size (default: 100 MB).

4. **Remediation Guidance**: Each diagnostic includes remediation guidance. The guidance links to phase documentation for detailed instructions.

### Integration Points

1. **Validator**: The validator emits diagnostics for malformed, incompatible, and conflicting inputs.

2. **Suite Execution**: Suite execution emits diagnostics for unavailable dependencies and resource exhaustion.

3. **CI/CD Pipeline**: Diagnostics are captured and reported in CI/CD pipeline logs.

4. **Monitoring**: Diagnostics are forwarded to the monitoring system for alerting and analysis.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 2.3.1: Malformed Binary

**Setup**: Create a malformed WebAssembly binary (invalid opcodes).

**Steps**:
1. Create a WebAssembly binary with invalid opcodes.
2. Run XTP bytes contract tests.

**Expected Result**: Diagnostic with outcome "malformed" and error code `com.extism.conformance.malformed`.

### Test 2.3.2: Incompatible Engine Version

**Setup**: Configure an unsupported engine version.

**Steps**:
1. Configure engine version "99.0.0" (not supported).
2. Run suite execution.

**Expected Result**: Diagnostic with outcome "incompatible" and error code `com.extism.conformance.incompatible`.

### Test 2.3.3: Conflicting Test Results

**Setup**: Create two test results with the same digest but different outcomes.

**Steps**:
1. Create test result A with outcome "pass".
2. Create test result B with outcome "fail" and same digest.
3. Run validator on test result B.

**Expected Result**: Diagnostic with outcome "conflicting" and error code `com.extism.conformance.conflicting`.

### Test 2.3.4: Unauthorized Suite Access

**Setup**: Attempt to run a suite without authentication.

**Steps**:
1. Attempt to run a suite without authentication.
2. Observe the error.

**Expected Result**: Diagnostic with outcome "unauthorized" and error code `com.extism.conformance.unauthorized`.

### Test 2.3.5: Resource Exhaustion

**Setup**: Simulate disk space exhaustion.

**Steps**:
1. Fill disk with dummy data until no space remains.
2. Attempt to run suite execution.
3. Restore disk space.

**Expected Result**: Diagnostic with outcome "exhausted" and error code `com.extism.conformance.exhausted`. No partial state is left.

### Test 2.3.6: Engine Unavailable

**Setup**: Simulate engine unavailability (e.g., Extism/Wasmtime not installed).

**Steps**:
1. Remove Extism/Wasmtime from PATH.
2. Attempt to run suite execution.
3. Restore Extism/Wasmtime to PATH.

**Expected Result**: Diagnostic with outcome "unavailable" and error code `com.extism.conformance.unavailable`.

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

No earlier milestone assumptions are invalidated by this phase. The failure evidence and operational notes build on the contract and data model defined in Section 2.1 and the behavior and integration defined in Section 2.2.

## Checklist

- [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to core wasi extism and plugin contract conformance.
- [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
- [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.
