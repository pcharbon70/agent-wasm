---
title: "Examples Runbooks SLO Evidence And Production Acceptance Behavior And Integration"
kind: specification
created: "2026-08-10"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-05
  - examples
  - runbooks
  - slo
  - evidence
  - production-acceptance
  - behavior
  - integration
aliases:
  - "M9-P5-S2 Behavior And Integration"
---

# Examples Runbooks SLO Evidence And Production Acceptance Behavior And Integration

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the behavior and integration rules for examples, runbooks,
SLOs, evidence, and production acceptance.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
integration tests in
Section [Phase 5 Integration Tests](50-examples-runbooks-slo-evidence-and-production-acceptance-phase-5-integration-tests.md)
and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md),
[Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model](48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md),
[Examples Runbooks SLO Evidence And Production Acceptance Contract And Data Model](50-examples-runbooks-slo-evidence-and-production-acceptance-contract-and-data-model.md).

## 50.2 Behavior And Integration

### 50.2.1 Example Execution Behavior

> **Non-normative note.**
Examples execute with the following behavior:

1. Clone or download example repository.
2. Install dependencies (SDK, runtime, storage backend).
3. Configure example (tenant, principal, artifact, etc.).
4. Run example (execute fixtures, submit signals, etc.).
5. Verify output (expected signals, state changes, diagnostics).
6. Retain evidence (logs, metrics, traces, audit events).

> **Non-normative note.**
Example execution is:
- Idempotent (same inputs produce same outputs).
- Reproducible (same environment produces same results).
- Verifiable (evidence can be inspected and validated).

### 50.2.2 Runbook Execution Behavior

> **Non-normative note.**
Runbooks execute with the following behavior:

1. Detect symptom (logs, metrics, traces, audit events).
2. Diagnose issue (run commands, collect data, identify root cause).
3. Remediate issue (execute commands, change configuration, escalate).
4. Verify resolution (run commands, check metrics, confirm recovery).
5. Document resolution (log actions, update runbook if needed).

> **Non-normative note.**
Runbook execution is:
- Guided (step-by-step instructions).
- Auditable (each step logged and tracked).
- Reversible (remediation steps can be undone if needed).

### 50.2.3 SLO Measurement Behavior

> **Normative definition.**
SLOs are measured with the following behavior:

1. At each UTC minute boundary, select unsampled source records in the exact
   rolling 30-day half-open window from Section 50.1.3.
2. Classify exact eligible and bad units for the objective.
3. Calculate the exact observed value, target result, and error-budget fields.
4. Persist the measurement record and ordered source-record digests.
5. Emit `slo.violation` when status first transitions into `violated`.
6. Emit `slo.budget.exhausted` when a positive budget first reaches zero or a
   zero-budget objective first transitions into `violated`.

An unavailable measurement emits `slo.measurement.unavailable`, does not count
as met or violated, and blocks production acceptance. Repeated measurements in
the same status do not repeat transition diagnostics. Recovery to `met` resets
the transition so a later violation or exhaustion emits again. There is no
deployment-selected window, percentile method, target, exclusion, or alert
threshold.

> **Normative definition.**
SLO measurement is:
- Automated (via metrics collection and calculation).
- Minute-bounded (status updated at each UTC minute boundary).
- Historical (SLO data retained for trend analysis).

### 50.2.4 Evidence Generation Behavior

> **Non-normative note.**
Evidence is generated with the following behavior:

1. Execute test scenario (fixture, load test, security audit, etc.).
2. Capture results (metrics, logs, traces, audit events, screenshots).
3. Validate results (verify expected outcomes, check for failures).
4. Package evidence (bundle results with metadata, hash for integrity).
5. Store evidence (immutable storage, tamper-evident).
6. Publish evidence (make accessible via `evidence inspect` or API).

> **Non-normative note.**
Evidence generation is:
- Automated (via test suites and tooling).
- Tamper-evident (cryptographic hashing).
- Immutable (cannot be modified after generation).

A deletion request targeting production acceptance evidence MUST be rejected
without changing availability, identity, bytes, digest, or storage. Operator
authorization, elapsed time, backend migration, and storage-tier movement do
not alter this result.

### 50.2.5 Production Acceptance Behavior

> **Non-normative note.**
Production acceptance is performed with the following behavior:

1. Verify conformance evidence (all conformance tests passing).
2. Verify SLO evidence (all SLOs met or exceeded).
3. Verify security evidence (no critical vulnerabilities, compliance achieved).
4. Verify performance evidence (load, soak, fault scenarios passed).
5. Verify runbook evidence (all runbooks executable and effective).
6. Verify example evidence (all examples executable and verified).
7. Generate production acceptance report (summary of evidence, residual risks).
8. Approve release (release manager signs off).

> **Non-normative note.**
Production acceptance is:
- Gate-based (release blocked until all evidence verified).
- Documented (report generated and retained).
- Owned (release manager approves).

### 50.2.6 Support Matrix Update Behavior

> **Non-normative note.**
Support matrix is updated with the following behavior:

1. Identify deprecated components (version sunset date reached).
2. Announce deprecation (notify users, update documentation).
3. Migrate users (assist with migration to supported version).
4. Remove unsupported components (from compatibility matrix).

> **Non-normative note.**
Support matrix updates are:
- Planned (scheduled with advance notice).
- Communicated (users notified before deprecation).
- Supported (migration assistance provided).

### 50.2.7 Residual Risk Review Behavior

> **Non-normative note.**
Residual risks are reviewed with the following behavior:

1. Schedule review (quarterly or after significant changes).
2. Collect new risk data (incident reports, security audits, performance tests).
3. Assess risks (likelihood, impact, mitigation effectiveness).
4. Update risk register (add new risks, update existing risks, close resolved risks).
5. Communicate updates (notify stakeholders, update documentation).

> **Non-normative note.**
Residual risk reviews are:
- Regular (quarterly or after significant changes).
- Comprehensive (assess all known risks).
- Actionable (updates drive mitigation improvements).

### 50.2.8 Release Execution Behavior

> **Non-normative note.**
Releases are executed with the following behavior:

1. Plan release (define scope, schedule, owners).
2. Build release (compile, test, package).
3. Review release (security review, conformance check).
4. Deploy release (deploy to production, monitor).
5. Verify release (run smoke tests, check SLOs).
6. Document release (release notes, changelog).
7. Close release (announce completion, celebrate).

> **Non-normative note.**
Release execution is:
- Governed (by release playbook).
- Owned (by release manager).
- Audited (each step logged and tracked).

Release timing and scheduling are non-normative internal process choices.
They MUST NOT omit, reorder, or change any release execution or production
acceptance step, and the same build and evidence MUST produce the same gate
decision regardless of schedule.

### 50.2.9 Evidence-retention precedence

For production acceptance evidence, Section 50.1.4 replaces Chapter 34's
general operator-deletion exception and post-retention deletion permission.
Chapter 34 continues to govern other evidence. A wrapper, runbook, release
process, or storage backend MUST preserve this classification and MUST NOT
translate a rejected deletion into a successful retention operation.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Example execution steps | Section 50.2.1 | Required | Must include all steps listed in the table. |
| Runbook execution steps | Section 50.2.2 | Required | Must include all steps listed in the table. |
| SLO measurement steps | Section 50.2.3 | Required | Must include all steps listed in the table. |
| SLO alert thresholds | [SLO Measurement Behavior](#5023-slo-measurement-behavior) | Required | Alert on target violation and when remaining error budget reaches zero. |
| SLO window and formulas | [SLO Measurement Behavior](#5023-slo-measurement-behavior) | Required | Use the fixed 30-day window, UTC minute schedule, exact source units, formulas, and transition diagnostics. |
| Unavailable SLO measurement | [SLO Measurement Behavior](#5023-slo-measurement-behavior) | Required | Emit `slo.measurement.unavailable` and block production acceptance. |
| Evidence generation steps | Section 50.2.4 | Required | Must include all steps listed in the table. |
| Production evidence deletion | Section 50.2.4 | Prohibited | Reject deletion without changing evidence or availability. |
| Production acceptance steps | Section 50.2.5 | Required | Must include all steps listed in the table. |
| Support matrix update steps | Section 50.2.6 | Required | Must include all steps listed in the table. |
| Residual risk review steps | Section 50.2.7 | Required | Must include all steps listed in the table. |
| Release execution steps | Section 50.2.8 | Required | Must include all steps listed in the table. |
| Release scheduling | [Release Execution Behavior](#5028-release-execution-behavior) | Internal mechanism | May vary only if release steps and acceptance decisions are identical. |
| Evidence-retention precedence | Section 50.2.9 | Explicit replacement | Chapter 34 deletion permissions do not apply to production acceptance evidence. |

## Rationale and evidence (non-normative)

Behavior and integration rules for Milestone 9 Phase 5 ensure that
examples, runbooks, SLOs, evidence, and production acceptance work
correctly and integrate with the host runtime.

Examples execute reproducibly with verifiable evidence.
Runbooks execute guided and auditable remediation steps.
SLOs are measured automatically and in real-time with historical data.
Evidence is generated automatically, tamper-evidently, and immutably.
Production acceptance is gate-based, documented, and owned.
Support matrix updates are planned, communicated, and supported.
Residual risk reviews are regular, comprehensive, and actionable.
Release execution is governed, owned, and audited.

These behaviors ensure that production deployments are well-documented,
measurable, and supported.
