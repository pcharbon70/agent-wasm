---
title: "Examples Runbooks SLO Evidence And Production Acceptance Failure Evidence And Operational Notes"
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
  - failure-evidence
  - operational-notes
aliases:
  - "M9-P5-S3 Failure Evidence And Operational Notes"
---

# Examples Runbooks SLO Evidence And Production Acceptance Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the failure evidence and operational notes for examples,
runbooks, SLOs, evidence, and production acceptance.

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
[Examples Runbooks SLO Evidence And Production Acceptance Contract And Data Model](50-examples-runbooks-slo-evidence-and-production-acceptance-contract-and-data-model.md),
[Examples Runbooks SLO Evidence And Production Acceptance Behavior And Integration](50-examples-runbooks-slo-evidence-and-production-acceptance-behavior-and-integration.md).

## 50.3 Failure Evidence And Operational Notes

### 50.3.1 Failure Outcomes

> **Normative definition.**
The following failure outcomes are relevant to examples, runbooks, SLOs,
evidence, and production acceptance.
Each outcome includes a stable diagnostic code family, cause, and behavior.

#### Example failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `example.run.failed` | Example execution fails (e.g., dependency missing, fixture fails). | Log failure at `ERROR` level. Emit diagnostic with failure details. |
| `example.verify.failed` | Example verification fails (e.g., output mismatch, evidence incomplete). | Log failure at `ERROR` level. Emit diagnostic with verification failure. |

#### Runbook failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `runbook.diagnosis.failed` | Runbook diagnosis fails (e.g., root cause not identified, commands fail). | Log failure at `ERROR` level. Emit diagnostic with diagnosis failure. Escalate to support. |
| `runbook.remediation.failed` | Runbook remediation fails (e.g., commands fail, configuration change fails). | Log failure at `ERROR` level. Emit diagnostic with remediation failure. Escalate to support. |
| `runbook.verification.failed` | Runbook verification fails (e.g., issue not resolved, metrics not recovered). | Log failure at `ERROR` level. Emit diagnostic with verification failure. Escalate to support. |

#### SLO failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `slo.violation` | A fixed-window measurement first transitions into `violated`. | Alert once for the transition and include the exact objective, window, observed value, and target. |
| `slo.budget.exhausted` | A positive budget first reaches zero or a zero-budget objective first transitions into `violated`. | Alert once for the transition, include exact budget fields, and trigger incident response. |
| `slo.measurement.unavailable` | The fixed window has zero eligible units or required source records cannot be verified. | Mark the objective unavailable, emit the diagnostic, and block production acceptance. Do not classify it as met. |

#### Evidence failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `evidence.generation.failed` | Evidence generation fails (e.g., test fails, capture fails, package fails). | Log failure at `ERROR` level. Emit diagnostic with generation failure. |
| `evidence.storage.failed` | Evidence storage fails (e.g., write fails, hash fails). | Log failure at `ERROR` level. Emit diagnostic with storage failure. |
| `evidence.tamper.detected` | Evidence tampering detected (e.g., hash mismatch, modification detected). | Log failure at `ERROR` level. Emit diagnostic with tamper detection. Alert security team. |
| `evidence.deletion.prohibited` | A deletion request targets production acceptance evidence. | Reject without changing identity, bytes, digest, storage, or availability. Emit the diagnostic even when the requester is an operator or general retention has elapsed. |

#### Production acceptance failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `acceptance.conformance.failed` | Conformance evidence verification fails (e.g., tests failing). | Block release. Log at `ERROR` level. Emit diagnostic with conformance failure. |
| `acceptance.slo.failed` | SLO evidence verification fails (e.g., SLOs not met). | Block release. Log at `ERROR` level. Emit diagnostic with SLO failure. |
| `acceptance.security.failed` | Security evidence verification fails (e.g., vulnerabilities found). | Block release. Log at `ERROR` level. Emit diagnostic with security failure. |
| `acceptance.performance.failed` | Performance evidence verification fails (e.g., load test fails). | Block release. Log at `ERROR` level. Emit diagnostic with performance failure. |

#### Support matrix failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `support.matrix.update.failed` | Support matrix update fails (e.g., deprecation announcement fails, migration fails). | Log failure at `ERROR` level. Emit diagnostic with update failure. |

#### Residual risk review failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `risk.review.failed` | Residual risk review fails (e.g., review not scheduled, risk data not collected). | Log failure at `ERROR` level. Emit diagnostic with review failure. |

#### Release failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `release.build.failed` | Release build fails (e.g., compilation fails, tests fail). | Block release. Log at `ERROR` level. Emit diagnostic with build failure. |
| `release.review.failed` | Release review fails (e.g., security review fails, conformance check fails). | Block release. Log at `ERROR` level. Emit diagnostic with review failure. |
| `release.deploy.failed` | Release deployment fails (e.g., deployment fails, smoke tests fail). | Rollback release. Log at `ERROR` level. Emit diagnostic with deployment failure. |
| `release.verify.failed` | Release verification fails (e.g., SLOs not met, smoke tests fail). | Rollback release. Log at `ERROR` level. Emit diagnostic with verification failure. |

#### Cross-chapter evidence precedence

For production acceptance evidence, `evidence.deletion.prohibited` and the
indefinite-retention rule in Section 50.1.4 explicitly replace Chapter 34's
general operator-deletion exception and post-retention availability rule.
Chapter 34 continues to govern evidence not classified as production
acceptance evidence.

### 50.3.2 Bounded Diagnostics and Evidence

> **Normative definition.**
Diagnostics are bounded to prevent exposure of secrets, implementation
internals, or sensitive user data.
Each diagnostic includes the following fields:

| Field | Content | Source |
| --- | --- | --- |
| `diagnostic` | The failure diagnostic code | Host runtime |
| `phase` | The phase that produced the diagnostic | Host runtime |
| `section` | The section that produced the diagnostic | Host runtime |
| `contract` | The contract that produced the diagnostic | Host runtime |
| `profile` | The conformance profile that produced the diagnostic | Host runtime |
| `failed_boundary` | The failed boundary | Host runtime |
| `timestamp` | The ISO 8601 timestamp | Host clock |
| `message` | A human-readable description | Host runtime |
| `hint` | Suggested remediation steps | SDK/CLI/simulator |
| `reference` | Documentation link for further guidance | SDK/CLI/simulator |

> **Normative definition.**
Diagnostics MUST NOT include:
- Raw credential values or secret references.
- Internal stack traces or implementation details.
- User data that is not relevant to the failure.
- Sensitive configuration values (e.g., database connection strings with passwords).

Evidence is retained for operational debugging and compliance auditing.
Evidence is retrievable via the `evidence inspect` CLI command or SDK
function with appropriate access controls.

### 50.3.3 Conformance Summary

> **Non-normative note.**
The following table summarizes fixed acceptance behavior and
equivalence-constrained internal mechanisms from the governing contract.

| Choice | Description | Default |
| --- | --- | --- |
| SLO target values | Target values for all SLOs. | As defined in Section 50.1.3. |
| SLO error budget values | Error budget values for all SLOs. | As defined in Section 50.1.3. |
| SLO alert thresholds | Thresholds for SLO alerts (violation, budget exhaustion). | Target violation and zero remaining error budget. |
| SLO measurement window | Window and evaluation schedule. | Rolling 30 days at each UTC minute boundary. |
| SLO calculation | Eligible units, bad units, percentile, and budget arithmetic. | Exact Section 50.1.3 formulas; no sampling or estimation. |
| Evidence storage backend | Backend for evidence storage (immutable, tamper-evident). | Internal; must preserve identical evidence bytes, immutability, and tamper detection. |
| Evidence retention period | Retention period for production acceptance evidence. | Indefinite under [Production Acceptance Evidence](50-examples-runbooks-slo-evidence-and-production-acceptance-contract-and-data-model.md#5014-production-acceptance-evidence). |
| Evidence deletion | Deletion behavior for production acceptance evidence. | Always reject with `evidence.deletion.prohibited`; Chapter 34 deletion permissions do not apply. |
| Residual risk review frequency | Frequency of residual risk reviews (quarterly, etc.). | Quarterly. |
| Release schedule | Timing of releases. | Internal; must not alter steps or acceptance decisions. |

### 50.3.4 Deferred Work

| Item | Target | Reason |
| --- | --- | --- |
| Automated SLO reporting | Milestone 9 Phase 6 | Requires integration with reporting systems (e.g., Grafana, Datadog). |
| Automated runbook execution | Milestone 9 Phase 6 | Requires integration with automation systems (e.g., Ansible, Terraform). |
| Automated evidence generation | Milestone 9 Phase 6 | Requires integration with CI/CD systems (e.g., GitHub Actions, Jenkins). |
| Automated release execution | Milestone 9 Phase 6 | Requires integration with deployment systems (e.g., Kubernetes, Terraform). |
| Residual risk automation | Milestone 9 Phase 6 | Requires integration with risk management systems. |

> **Non-normative note.**
All items deferred to Milestone 9 later phases fall under
Milestone 9 - Production Platform And Developer Experience
(planning document at `.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md`).
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### 50.3.5 Results That Would Invalidate an Earlier Milestone Assumption

> **Non-normative note.**
The following results from Phase 5 would invalidate an earlier milestone
assumption:

1. **Examples alter protocol behavior**: If examples alter the protocol
   or runtime behavior defined in earlier milestones, this would invalidate
   the assumption that examples are canonical references and do not
   introduce behavioral changes.

2. **SLOs bypass authorization**: If SLO measurement bypasses authorization
   checks (e.g., SLO data exposed without authorization), this would
   invalidate the assumption that all host outputs are subject to the
   bootstrap profile's authorization model.

3. **Evidence is mutable**: If evidence can be modified or deleted after
   generation (other than by authorized deletion of non-evidence data),
   this would invalidate the assumption that evidence is immutable and
   tamper-evident.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Failure outcome diagnostics | Section 50.3.1 | Required | Must include all diagnostics listed in the failure outcomes tables. |
| Diagnostic field set | Section 50.3.2 | Required | Must include all fields listed in the bounded diagnostics table. |
| Diagnostic redaction | Section 50.3.2 | Required | Must redact secrets, stack traces, and irrelevant user data. |
| Actionable failure fields | Section 50.3.2 | Required | Must include `hint` and `reference` fields. |
| Conformance summary | Section 50.3.3 | Required | Must preserve fixed acceptance behavior and equivalence constraints. |
| SLO failure calculation | Sections 50.3.1 and 50.3.3 | Required | Must use the fixed window, formulas, transition conditions, and unavailable outcome. |
| Evidence deletion failure | Sections 50.3.1 and 50.3.3 | Required | Must reject deletion with `evidence.deletion.prohibited` regardless of operator authority or elapsed retention. |
| Deferred work enforcement | Section 50.3.4 | MUST | Must NOT implement deferred work without evidence from the corresponding future phase. |

## Rationale and evidence (non-normative)

Failure evidence and operational notes for Milestone 9 Phase 5 ensure
that examples, runbooks, SLOs, evidence, and production acceptance
failures are observable, debuggable, and secure.
Stable diagnostic codes enable tooling to detect and handle failures
without parsing human-readable messages.
Bounded diagnostics prevent information leakage while retaining sufficient
context for operational debugging.
Actionable failures include hints and references to enable operators to
resolve issues without consulting support.

Fixed acceptance behavior and equivalence-constrained internals enable
conformance verification and interoperability.
Deferred work is explicitly identified to prevent scope creep and ensure
that future phases build on the verified foundation of Phase 5.

Invalidating assumption conditions ensure that Phase 5 does not introduce
behavioral changes that contradict earlier milestone contracts.
