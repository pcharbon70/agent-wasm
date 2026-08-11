---
title: "Examples Runbooks SLO Evidence And Production Acceptance Phase 5 Integration Tests"
kind: specification
created: "2026-08-10"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-05
  - examples
  - runbooks
  - slo
  - evidence
  - production-acceptance
  - integration-tests
  - phase-5
aliases:
  - "M9-P5-S4 Phase 5 Integration Tests"
---

# Examples Runbooks SLO Evidence And Production Acceptance Phase 5 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It defines the integration tests that verify examples, runbooks, SLOs,
evidence, and production acceptance across their real dependency boundaries.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires passing this test suite and
a passing cross-milestone fixture run.

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
[Compatibility Upgrades Migrations Deployment And Horizontal Coordination Contract And Data Model](49-compatibility-upgrades-migrations-deployment-and-horizontal-coordination-contract-and-data-model.md),
[Examples Runbooks SLO Evidence And Production Acceptance Contract And Data Model](50-examples-runbooks-slo-evidence-and-production-acceptance-contract-and-data-model.md),
[Examples Runbooks SLO Evidence And Production Acceptance Behavior And Integration](50-examples-runbooks-slo-evidence-and-production-acceptance-behavior-and-integration.md),
[Examples Runbooks SLO Evidence And Production Acceptance Failure Evidence And Operational Notes](50-examples-runbooks-slo-evidence-and-production-acceptance-failure-evidence-and-operational-notes.md).

## 50.4 Phase 5 Integration Tests

This section defines the observable behavior that the Phase 5 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### 50.4.1 Successful flow

Examples, runbooks, SLOs, evidence, and production acceptance MUST
execute correctly and produce expected outputs with complete evidence.
The test MUST verify that:

1. All examples execute successfully (direct-reducer, fsm-continuation,
   scheduled-workflow, tool-loop, approval, retrieval, multi-agent-fan-out-fan-in,
   migration).
2. All runbooks execute successfully (dependency-failure, queue-overload,
   stuck-turn, repeated-effect, runtime-divergence, artifact-revocation,
   tenant-incident, recovery, rollback).
3. All SLOs are measured correctly (admission, turn-latency, durability,
   effect-delay, recovery, availability, isolation, evidence-completeness).
4. All SLOs meet or exceed targets (admission >= 99.9%, turn-latency <= 500ms,
   durability = 100%, effect-delay <= 100ms, recovery <= 5 minutes,
   availability >= 99.9%, isolation = 100%, evidence-completeness = 100%).
5. All evidence types are generated correctly (slo-evidence, runbook-evidence,
   example-evidence, conformance-evidence, security-evidence, performance-evidence).
6. All evidence is immutable and tamper-evident.
7. Production acceptance is performed correctly (conformance, SLO, security,
   performance, runbook, example evidence verified).
8. Production acceptance report is generated and retained.
9. Support matrix is maintained and updated correctly.
10. Residual risks are reviewed and updated correctly.
11. Release execution is performed correctly (plan, build, review, deploy,
    verify, document, close).
12. The test records and retains:
    - Example execution results and evidence.
    - Runbook execution results and evidence.
    - SLO measurement results and compliance evidence.
    - Evidence generation results and evidence packages.
    - Production acceptance report.
    - Support matrix updates.
    - Residual risk review updates.
    - Release execution results and evidence.

### 50.4.2 Malformed and incompatible input

Examples, runbooks, SLOs, evidence, and production acceptance MUST
reject malformed and incompatible inputs with stable diagnostics.
The test MUST verify that:

1. Invalid example inputs produce `example.run.failed` diagnostic.
2. Invalid runbook symptoms produce `runbook.diagnosis.failed` diagnostic.
3. Invalid SLO metrics produce `slo.violation` diagnostic.
4. Invalid evidence inputs produce `evidence.generation.failed` diagnostic.
5. Invalid production acceptance inputs produce `acceptance.conformance.failed` diagnostic.
6. Invalid support matrix inputs produce `support.matrix.update.failed` diagnostic.
7. Invalid residual risk inputs produce `risk.review.failed` diagnostic.
8. Invalid release inputs produce `release.build.failed` diagnostic.
9. No state, journal, or outbox entries are created for the failed operations.
10. The diagnostic identifies the specific field, type, or boundary that failed.
11. The diagnostic does not expose secrets or implementation internals.

### 50.4.3 Stale and duplicate input

Examples, runbooks, SLOs, evidence, and production acceptance MUST
detect and reject stale or duplicate inputs.
The test MUST verify that:

1. Duplicate example executions with same inputs produce stable diagnostic.
2. Duplicate runbook executions with same symptom produce stable diagnostic.
3. Duplicate SLO measurements with same time window produce stable diagnostic.
4. Duplicate evidence generations with same scenario produce stable diagnostic.
5. Duplicate production acceptance executions with same evidence produce stable diagnostic.
6. No state, journal, or outbox entries are created for the rejected operations.
7. The diagnostic identifies the stale or duplicate input.

### 50.4.4 Boundary and limit inputs

Examples, runbooks, SLOs, evidence, and production acceptance MUST
enforce configured boundaries and limits.
The test MUST verify that:

1. SLO targets are enforced (e.g., admission success rate below 99.9% triggers violation).
2. SLO error budgets are enforced (e.g., budget falls below threshold triggers exhaustion).
3. Evidence storage limits are enforced (e.g., storage full triggers failure).
4. Evidence retention limits are enforced (e.g., retention period exceeded triggers deletion).
5. Release schedule limits are enforced (e.g., release frequency exceeds limit triggers rejection).
6. No state, journal, or outbox entries are created for the rejected operations.
7. The diagnostic identifies the boundary or limit that was exceeded.

### 50.4.5 Timeout, cancellation, and unavailable dependency

Examples, runbooks, SLOs, evidence, and production acceptance MUST
handle timeouts, cancellations, and unavailable dependencies gracefully
without leaving unauthorized or partial state.
The test MUST verify that:

1. Example execution timeouts produce `example.run.failed` diagnostic.
2. Runbook execution timeouts produce `runbook.diagnosis.failed` diagnostic.
3. SLO measurement timeouts produce `slo.violation` diagnostic.
4. Evidence generation timeouts produce `evidence.generation.failed` diagnostic.
5. Production acceptance timeouts produce `acceptance.conformance.failed` diagnostic.
6. Unavailable example repository produces `example.run.failed` diagnostic.
7. Unavailable runbook data produces `runbook.diagnosis.failed` diagnostic.
8. Unavailable SLO metrics produces `slo.violation` diagnostic.
9. Unavailable evidence storage produces `evidence.storage.failed` diagnostic.
10. Unavailable production acceptance gate produces `acceptance.conformance.failed` diagnostic.
11. Cancellation of example execution produces stable diagnostic.
12. Cancellation of runbook execution produces stable diagnostic.
13. Cancellation of evidence generation produces stable diagnostic.
14. Cancellation of production acceptance produces stable diagnostic.
15. The system transitions to a safe state (e.g., rolled back, paused) after failures.
16. No state, journal, or outbox entries are created for the failed operations.

### 50.4.6 Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.
The test MUST verify that:

1. All Phase 1 integration tests from Milestone 1 (Profile Vocabulary) still pass.
2. All Phase 5 integration tests from Milestone 1 (Guest SDK) still pass.
3. All Phase 3 integration tests from Milestone 3 (Agent Registry) still pass.
4. All Phase 1 integration tests from Milestone 7 (Provider-Neutral Model Requests) still pass.
5. All Phase 1 integration tests from Milestone 9 (Embedded And Server Host APIs) still pass.
6. All Phase 2 integration tests from Milestone 9 (Guest SDK, CLI, Simulator, Templates, Fixtures, And Debugging) still pass.
7. All Phase 3 integration tests from Milestone 9 (Telemetry, Tracing, Audit, Redaction, Health, And Operator Actions) still pass.
8. All Phase 4 integration tests from Milestone 9 (Compatibility, Upgrades, Migrations, Deployment, And Horizontal Coordination) still pass.
9. Any regression is recorded with:
   - The test ID and milestone.
   - The observed behavior.
   - The expected behavior.
   - The approval status (approved variability or defect).

> **Non-normative note.**
Cross-milestone fixtures ensure that Milestone 9 Phase 5 does not
introduce regressions in earlier milestone behavior.
Examples, runbooks, SLOs, evidence, and production acceptance are
additive; they MUST NOT alter the behavior of earlier milestone contracts.

### 50.4.7 Example reproducibility verification

Examples MUST execute reproducibly.
The test MUST verify that:

1. Same example inputs with same environment produce same outputs.
2. Same example fixtures produce same evidence records.
3. Reproducibility is verified via:
   - Output hash comparison.
   - Evidence record comparison.
   - Metric comparison.

### 50.4.8 Runbook effectiveness verification

Runbooks MUST effectively resolve operational issues.
The test MUST verify that:

1. Runbook diagnosis identifies correct root cause for known symptoms.
2. Runbook remediation resolves the issue.
3. Runbook verification confirms resolution.
4. Runbook execution does not introduce new issues.

### 50.4.9 SLO compliance verification

SLOs MUST be measured and met.
The test MUST verify that:

1. SLO metrics are collected correctly.
2. SLO compliance is calculated correctly.
3. SLO error budget consumption is tracked correctly.
4. SLO alerts fire correctly (violation, budget exhaustion).
5. All SLOs meet or exceed targets.

### 50.4.10 Evidence immutability verification

Evidence MUST be immutable and tamper-evident.
The test MUST verify that:

1. Evidence cannot be modified after generation.
2. Evidence cannot be deleted (except by authorized deletion of non-evidence data).
3. Evidence is tamper-evident (cryptographic hashing detects modifications).
4. Evidence generation failures produce `evidence.generation.failed` diagnostic.
5. Evidence storage failures produce `evidence.storage.failed` diagnostic.
6. Evidence tampering detection produces `evidence.tamper.detected` diagnostic.

### 50.4.11 Production acceptance gate verification

Production acceptance MUST block releases until all evidence is verified.
The test MUST verify that:

1. Conformance evidence verification succeeds when all tests pass.
2. Conformance evidence verification fails when tests fail.
3. SLO evidence verification succeeds when all SLOs met.
4. SLO evidence verification fails when SLOs not met.
5. Security evidence verification succeeds when no critical vulnerabilities.
6. Security evidence verification fails when vulnerabilities found.
7. Release blocked when any evidence verification fails.
8. Release approved when all evidence verification succeeds.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Example execution verification | Section 50.4.1 | MUST | Must verify all examples execute successfully. |
| Runbook execution verification | Section 50.4.1 | MUST | Must verify all runbooks execute successfully. |
| SLO measurement verification | Section 50.4.1 | MUST | Must verify all SLOs measured correctly. |
| SLO target compliance verification | Section 50.4.1 | MUST | Must verify all SLOs meet or exceed targets. |
| Evidence generation verification | Section 50.4.1 | MUST | Must verify all evidence types generated correctly. |
| Evidence immutability verification | Section 50.4.1 | MUST | Must verify evidence immutable and tamper-evident. |
| Production acceptance verification | Section 50.4.1 | MUST | Must verify production acceptance performed correctly. |
| Cross-milestone fixtures | Section 50.4.6 | MUST | Must include all fixtures listed in section 50.4.6. |
| Regression approval | Section 50.4.6 | Required | Must record and approve or reject any regression. |
| Example reproducibility verification | Section 50.4.7 | MUST | Must verify example reproducibility. |
| Runbook effectiveness verification | Section 50.4.8 | MUST | Must verify runbook effectiveness. |
| SLO compliance verification | Section 50.4.9 | MUST | Must verify SLO compliance. |
| Evidence immutability verification | Section 50.4.10 | MUST | Must verify evidence immutability and tamper-evidence. |
| Production acceptance gate verification | Section 50.4.11 | MUST | Must verify production acceptance gate blocks releases. |

## Rationale and evidence (non-normative)

Integration tests for Milestone 9 Phase 5 verify that examples, runbooks,
SLOs, evidence, and production acceptance work correctly across their
real dependency boundaries.
These tests prove the phase works as an integrated behavior and preserve
reproducible evidence for later milestone and release gates.

The test suite exercises:
- Successful flows with complete evidence retention.
- Malformed and incompatible inputs with stable diagnostics.
- Stale and duplicate inputs with proper rejection.
- Boundary and limit inputs with configured enforcement.
- Timeout, cancellation, and unavailable dependency handling.
- Cross-milestone fixture regression to ensure no behavioral changes.
- Example reproducibility verification.
- Runbook effectiveness verification.
- SLO compliance verification.
- Evidence immutability verification.
- Production acceptance gate verification.

Passing this test suite is a prerequisite for promoting this chapter to
`status: normative` and for advancing Milestone 9 to completion.
