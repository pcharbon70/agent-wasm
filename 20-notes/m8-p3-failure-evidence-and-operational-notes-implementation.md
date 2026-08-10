---
title: "M8-P3 Section 3.3 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-03
  - failure-evidence
  - operational-notes
  - extism
  - wasmtime
  - wazero
  - semantic-equivalence
aliases:
  - "M8-P3.3 Section 3.3 Failure Evidence And Operational Notes Implementation"
---

# M8-P3 Section 3.3 Failure Evidence And Operational Notes Implementation

## Purpose

Establish failure evidence and operational notes for Extism Wasmtime and Extism Wazero semantic equivalence. This section builds on the behavior and integration defined in [Section 3.2 Behavior And Integration](./m8-p3-behavior-and-integration-implementation.md) and precedes the integration tests defined in [Section 3.4 Phase 3 Integration Tests](./m8-p3-integration-tests-implementation.md).

## Design Decisions

### Subtask 3.3.1.1: Failure Outcomes

The following failure outcomes are defined for Extism Wasmtime and Extism Wazero semantic equivalence:

| Outcome | Definition | Trigger Condition |
|---------|------------|-------------------|
| **malformed** | The input is invalid and cannot be processed. | Invalid WebAssembly binary, missing required exports, incompatible artifact format. |
| **incompatible** | The input is valid but incompatible with the current configuration. | Unsupported engine version, missing required features. |
| **stale** | The input is valid but has exceeded the retention period. | Artifact version older than retention period, divergence record older than review period. |
| **conflicting** | The input conflicts with existing evidence or configuration. | Duplicate divergence record with different verdict, conflicting controlled variables. |
| **unauthorized** | The input is valid but the actor lacks permission. | Missing authentication, insufficient privileges, unauthorized access to engine binaries. |
| **exhausted** | The system is unable to process the input due to resource constraints. | Disk space full, memory limit exceeded, rate limit hit, timeout exceeded, gas limit exceeded. |
| **unavailable** | A required dependency is unavailable. | Engine binary not installed, artifact not available, reference interpreter not available. |

**Decision**: Failure outcomes are categorized by their trigger condition. Each outcome has a corresponding error code and diagnostic message.

### Subtask 3.3.1.2: Diagnostic Emission

Every failure MUST emit bounded diagnostics that identify the phase contract, profile, and failed boundary without exposing secrets. The diagnostic format is:

```yaml
Diagnostic = {
  outcome: FailureOutcome,
  error_code: ErrorCode,
  message: string,
  phase_contract: string?,
  profile: string?,
  failed_boundary: string?,
  divergence_id: string?,
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

### Subtask 3.3.1.3: Implementation-Defined Choices

The following implementation-defined choices are documented:

| Choice | Decision | Rationale |
|--------|----------|-----------|
| **Error Code Format** | Use reverse-DNS notation (e.g., `com.extism.equivalence.malformed`) | Consistent with industry standards, globally unique. |
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
  m8-p3-failure-evidence-and-operational-notes-implementation.md  (this file)
```

### Key Behaviors

1. **Failure Detection**: Failures are detected during behavior comparison, divergence recording, and adjudication. Each failure is categorized according to the outcome table.

2. **Diagnostic Emission**: When a failure is detected, a diagnostic is emitted with the outcome, error code, message, and remediation. Secrets are redacted before emission.

3. **Diagnostic Storage**: Diagnostics are stored in an append-only log. The log is rotated when it exceeds a configurable size (default: 100 MB).

4. **Remediation Guidance**: Each diagnostic includes remediation guidance. The guidance links to phase documentation for detailed instructions.

### Integration Points

1. **Validator**: The validator emits diagnostics for malformed, incompatible, and conflicting inputs.

2. **Behavior Comparison**: Behavior comparison emits diagnostics for unavailable dependencies and resource exhaustion.

3. **CI/CD Pipeline**: Diagnostics are captured and reported in CI/CD pipeline logs.

4. **Monitoring**: Diagnostics are forwarded to the monitoring system for alerting and analysis.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 3.3.1: Malformed Artifact

**Setup**: Create a malformed WebAssembly artifact (invalid opcodes).

**Steps**:
1. Create a WebAssembly binary with invalid opcodes.
2. Attempt to execute on both engines.

**Expected Result**: Diagnostic with outcome "malformed" and error code `com.extism.equivalence.malformed`.

### Test 3.3.2: Incompatible Engine Version

**Setup**: Configure an unsupported engine version.

**Steps**:
1. Configure engine version "99.0.0" (not supported).
2. Attempt to execute behavior comparison.

**Expected Result**: Diagnostic with outcome "incompatible" and error code `com.extism.equivalence.incompatible`.

### Test 3.3.3: Conflicting Divergence Record

**Setup**: Create two divergence records with the same ID but different verdicts.

**Steps**:
1. Create divergence record A with verdict "conforming".
2. Create divergence record B with verdict "non-conforming" and same ID.
3. Attempt to store divergence record B.

**Expected Result**: Diagnostic with outcome "conflicting" and error code `com.extism.equivalence.conflicting`.

### Test 3.3.4: Unauthorized Access

**Setup**: Attempt to execute behavior comparison without authentication.

**Steps**:
1. Attempt to execute behavior comparison without authentication.
2. Observe the error.

**Expected Result**: Diagnostic with outcome "unauthorized" and error code `com.extism.equivalence.unauthorized`.

### Test 3.3.5: Resource Exhaustion

**Setup**: Simulate disk space exhaustion.

**Steps**:
1. Fill disk with dummy data until no space remains.
2. Attempt to execute behavior comparison.
3. Restore disk space.

**Expected Result**: Diagnostic with outcome "exhausted" and error code `com.extism.equivalence.exhausted`. No partial state is left.

### Test 3.3.6: Engine Unavailable

**Setup**: Simulate engine unavailability (e.g., Extism/Wasmtime binary not installed).

**Steps**:
1. Remove Extism/Wasmtime binary from PATH.
2. Attempt to execute behavior comparison.
3. Restore Extism/Wasmtime binary to PATH.

**Expected Result**: Diagnostic with outcome "unavailable" and error code `com.extism.equivalence.unavailable`.

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

No earlier milestone assumptions are invalidated by this phase. The failure evidence and operational notes build on the contract and data model defined in Section 3.1 and the behavior and integration defined in Section 3.2.

## Checklist

- [x] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to extism wasmtime and extism wazero semantic equivalence.
- [x] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
- [x] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.
