---
title: "Phase 5 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-05
  - implementation
  - integration-tests
  - provenance-testing
  - evidence-testing
  - redaction-testing
  - security-exercises
  - adversarial-testing
  - cross-milestone-tests
aliases:
  - "M5-P5-5.4 Implementation"
---

# Phase 5 Integration Tests Implementation

## Overview

This note documents the implementation of Section 5.4 (Phase 5 Integration
Tests) from
[Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[34-provenance-signing-audit-security-and-milestone-acceptance.md](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
which defines the integration test objectives, scenarios, evidence
requirements, and cross-milestone compatibility checks for artifact
provenance, evidence recording, evidence redaction, security exercises,
adversarial isolation exercises, and threat-to-control matrix publication.

## Subtask 5.4.1.1: Verify canonical successful flow and retained evidence

### Implementation

Defined test objectives for the canonical successful flow:

**Test objectives:**
1. **Artifact admission**: Artifact passes all admission checks and is
   recorded in dependency cache and registry
2. **Evidence recording**: All required evidence events are created
   (admitted, rejected, invocation started/completed/failed, grant
   approved/denied, isolation violation, residue detected, policy revision)
3. **Evidence redaction**: Redaction is applied correctly per access
   policy; unredacted records retained for operator access
4. **Threat-to-control matrix**: Matrix published with all required rows
   and fields

**Successful flow tests:**
- **Artifact admission**: Submit valid artifact with valid signature;
  verify `artifact.admitted` evidence created with correct fields
- **Evidence recording**: Trigger invocation; verify `invocation.started`,
  `invocation.completed`, and `grant.approved` evidence created
- **Evidence redaction**: Query evidence with tenant-scoped consumer;
  verify secrets and tenant-sensitive fields are redacted
- **Threat-to-control matrix**: Verify matrix contains all threats from
  threat model and all test results

### Design decisions

1. **Tests verify observable contracts, not private structure**: Tests
   are defined in terms of external behavior (evidence records, redaction
   results) rather than internal implementation details. This ensures
   tests remain valid across implementation changes.

2. **All evidence event types are tested**: The ten evidence event types
   are all tested, ensuring comprehensive coverage of the evidence recording
   system.

3. **Redaction is tested with tenant-scoped consumer**: The test verifies
   that tenant-scoped consumers can view their own prompts but cannot
   view secrets or tenant-sensitive fields.

4. **Evidence retention is tested**: Tests verify that evidence records
   are retained for the configured retention period and are not deleted
   prematurely.

## Subtask 5.4.1.2: Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs

### Implementation

Defined failure handling tests for all failure outcomes:

| Failure | Test Trigger | Expected Diagnostic |
|---------|-------------|-------------------|
| Malformed admission | Invalid `ArtifactAdmissionRequest` | `artifact.admission.malformed` |
| Digest mismatch | Artifact digest does not match recorded digest | `artifact.digest-mismatch` |
| Signature invalid | Invalid signature | `artifact.signature-invalid` |
| Publisher untrusted | Unknown signing identity | `artifact.publisher-untrusted` |
| Publisher hint advisory | Mismatched `publisher_hint` | `artifact.publisher-hint-mismatch` (advisory) |
| Build provenance invalid | Invalid build record | `artifact.build-provenance-invalid` |
| Dependency unresolved | Unresolved dependency | `artifact.dependency-unresolved` |
| Compiler incompatible | Incompatible compiler/PDK | `artifact.compiler-incompatible` |
| Revoked | Revoked artifact or publisher | `artifact.revoked` |
| Admission failed | General admission failure | `artifact.admission.failed` |
| Evidence integrity violation | Corrupted evidence record | `evidence.integrity-violation` |

Additional failure tests from security and adversarial exercises:
- `invocation.failed` with `capability-policy-violation`
- `tenant.isolation.violation`
- `residue.detected`

Each test MUST verify that error code and diagnostic message match expected values.

### Design decisions

1. **Tests cover all admission failure outcomes**: The ten admission
   failure outcomes plus additional security and adversarial outcomes
   are all tested, ensuring comprehensive coverage of the failure domain.

2. **Error codes and diagnostics are verified together**: Tests verify
   both the error code and the diagnostic message, ensuring that
   implementations provide meaningful error information.

3. **Bounded diagnostics are verified**: Tests verify that diagnostics
   do not expose secrets, internal implementation details, or
   tenant-specific state beyond `tenant_id`.

4. **Stable diagnostics**: Test diagnostics are verified to be stable
   across implementations. Error codes follow a stable naming convention
   and diagnostic messages are human-readable and actionable.

## Subtask 5.4.1.3: Verify timeout, cancellation, unavailable dependency, and retry behavior

### Implementation

Defined tests for timeout, cancellation, dependency, and retry behavior:

| Test | Trigger | Expected Outcome |
|------|---------|-----------------|
| Admission timeout | Admission request exceeds `deadline_ms` | Reject with `artifact.admission.failed`; no state persists |
| Cancellation during admission | Request cancelled mid-admission | Roll back partial state; no evidence record created |
| Invocation timeout | Invocation exceeds host-configured timeout | Record `invocation.failed` with `failure_type: timeout`; clean up instance |
| Invocation cancellation | Invocation cancelled by operator | Record `invocation.failed` with `failure_type: cancelled`; clean up instance |
| Dependency unavailable | Dependency artifact not available at resolution time | Reject admission with `artifact.dependency-unresolved` |
| Dependency revocation during invocation | Dependency revoked mid-invocation | Detect retained capabilities; revoke them; record `tenant.isolation.violation` |
| Retry with idempotent request | Same request retried after transient failure | Retry succeeds with same result; no duplicate evidence records |
| Retry with non-idempotent request | Non-idempotent request retried after transient failure | Retry may produce different result; evidence records are not deduplicated |

Each test MUST verify that no unauthorized or partial state persists after
timeout, cancellation, dependency failure, or retry.

### Design decisions

1. **Timeout and cancellation leave no partial state**: This is consistent
   with the atomic state journal invariant from
   [26-atomic-state-journal-and-directive-outbox-commits.md](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md).
   Partial state from timed-out or cancelled operations must not leak into
   the system state.

2. **Retry behavior depends on idempotency**: Tests distinguish between
   idempotent and non-idempotent requests. Idempotent requests can be safely
   retried; non-idempotent requests require careful handling to avoid
   duplicate evidence records.

3. **Dependency revocation during invocation is critical**: If a dependency
   is revoked while an artifact is invoking it, the system must detect
   retained capabilities and revoke them. This prevents artifacts from
   retaining capabilities beyond their authorized lifetime.

## Subtask 5.4.1.4: Run cross-milestone fixtures and record regressions

### Implementation

Defined four cross-milestone compatibility tests:

| Milestone | Fixture Source | Regression Check |
|-----------|---------------|-----------------|
| 1 | [Guest SDK Contracts Fixtures And Milestone Acceptance](../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md) | All M1 fixtures pass |
| 2 | Phase 1-5 plans under [Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/) | All M2 fixtures pass |
| 3 | Phase 1-5 plans under [Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/) | All M3 fixtures pass |
| 4 | Phase 1-5 plans under [Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/) | All M4 fixtures pass |

If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Design decisions

1. **Cross-milestone tests are mandatory**: The phase cannot be promoted
   to `status: normative` without passing cross-milestone fixtures.
   This ensures M5 does not introduce regressions in earlier milestones.

2. **Regressions trigger mandatory revision**: If a regression is
   detected, the affected milestone MUST be revised and re-validated.
   This prevents accumulating technical debt.

3. **Fixture sources are explicitly documented**: Each milestone's
   fixtures are traced to their source chapter or planning directory.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 34.1: [Provenance Signing Audit Security And Milestone Acceptance Contract And Data Model](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.2: [Provenance Signing Audit Security And Milestone Acceptance Behavior And Integration](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.3: [Provenance Signing Audit Security And Milestone Acceptance Failure Evidence And Operational Notes](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Guest SDK: [Guest SDK Contracts Fixtures And Milestone Acceptance](../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should integration tests include performance benchmarks for evidence
   recording and redaction? The spec defines functional tests but does
   not address performance requirements for evidence record creation or
   redaction query latency.

2. How should security exercise test evidence be stored and retrieved?
   The spec requires recording test evidence but does not specify the
   storage format or retrieval mechanism for security exercise reports.

3. Can integration tests be run in parallel? The spec does not address
   whether the successful flow tests can be run in parallel or must
   be run sequentially.
