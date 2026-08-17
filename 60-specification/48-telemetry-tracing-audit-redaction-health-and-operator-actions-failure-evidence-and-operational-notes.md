---
title: "Telemetry Tracing Audit Redaction Health And Operator Actions Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-10"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-03
  - telemetry
  - tracing
  - audit
  - redaction
  - health
  - operator-actions
  - failure-evidence
  - operational-notes
aliases:
  - "M9-P3-S3 Failure Evidence And Operational Notes"
---

# Telemetry Tracing Audit Redaction Health And Operator Actions Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-03-telemetry-tracing-audit-redaction-health-and-operator-actions.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the failure evidence and operational notes for telemetry,
tracing, audit, redaction, health, and operator actions.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
integration tests in
Section [Phase 3 Integration Tests](48-telemetry-tracing-audit-redaction-health-and-operator-actions-phase-3-integration-tests.md)
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
[Telemetry Tracing Audit Redaction Health And Operator Actions Behavior And Integration](48-telemetry-tracing-audit-redaction-health-and-operator-actions-behavior-and-integration.md).

## 48.3 Failure Evidence And Operational Notes

### 48.3.1 Failure Outcomes

> **Normative definition.**
The following failure outcomes are relevant to telemetry, tracing, audit,
redaction, health, and operator actions.
Each outcome includes a stable diagnostic code family, cause, and behavior.

#### Metrics failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `metrics.emit.failed` | Metric emission input is malformed, including an invalid label name, value, or combination, or emission otherwise fails. | Reject the malformed point or log the emission failure at `ERROR` level. Continue the operational event. |
| `metrics.cardinality.exceeded` | Metric cardinality limit exceeded. | Drop metric point. Log at `WARN` level. |
| `metrics.export.failed` | Metric export fails (e.g., network error, authentication failure). | Retry with backoff. Log at `ERROR` level if retry limit exceeded. |

#### Trace failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `trace.propagation.failed` | Trace context propagation fails (e.g., missing context, invalid format). | Start new trace. Log at `DEBUG` level. |
| `trace.sample.failed` | A trace sampling policy is invalid or an individual trace decision fails. | Reject invalid policy and retain the last valid policy, or disable traces if none exists. Drop a candidate whose individual decision fails. Never enable `always-on` fallback. |
| `trace.export.failed` | Trace export fails (e.g., network error, authentication failure). | Retry with backoff. Log at `ERROR` level if retry limit exceeded. |

#### Log failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `log.emit.failed` | Log emission fails (e.g., stderr error, exporter unavailable). | Continue operational event. Log failure at `ERROR` level. |
| `log.sample.failed` | A log sampling policy is invalid or an individual log decision fails. | Reject invalid policy and retain the last valid policy, or disable logs if none exists. Drop a candidate whose individual decision fails. Never enable `always-on` fallback. |
| `log.redaction.failed` | Log redaction fails (e.g., sensitive data not redacted). | Reject the complete log candidate. Emit only the fixed safe telemetry failure diagnostic without candidate-derived fields. |

#### Audit failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `audit.event.record.failed` | Required immutable audit append fails. | Before an operator or administrative effect, reject the action with no effect. After an already recorded attempt and executed effect, stop new audited actions, mark audit health unhealthy, and reconcile before resuming. |
| `audit.event.export.failed` | Audit event export fails (e.g., network error, authentication failure). | Retry with backoff. Log at `ERROR` level if retry limit exceeded. |

#### Redaction failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `redaction.policy.invalid` | Redaction policy is invalid (e.g., unknown data type, invalid rule). | Reject the policy and retain the last valid policy. If none exists, disable the affected telemetry family. Do not admit candidate data. |
| `redaction.apply.failed` | Redaction application fails (e.g., data type not recognized). | Reject the complete candidate record and emit only the fixed safe telemetry failure diagnostic. Do not skip a field or data type. |

#### Health check failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `health.check.timeout` | Health check times out (e.g., dependency unavailable). | Mark health check as `unhealthy`. Log at `ERROR` level. |
| `health.check.dependency.failed` | Health check dependency fails (e.g., storage unavailable). | Mark health check as `unhealthy`. Log at `ERROR` level. |
| `health.check.runtime-profile.failed` | Runtime profile health check fails. | Mark health check as `unhealthy`. Log at `ERROR` level. |

#### Operator action failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `operator.action.unauthorized` | Operator action authorization fails (e.g., insufficient role). | Reject action. Log at `WARN` level. Emit `unauthorized` diagnostic. |
| `operator.action.invalid` | Operator action parameters invalid (e.g., unknown tenant ID). | Reject action. Log at `WARN` level. Emit diagnostic with validation error. |
| `operator.action.timeout` | Operator action times out (e.g., drain exceeds 30 seconds). | Cancel action. Log at `ERROR` level. Emit diagnostic with timeout. |
| `operator.action.rate-limited` | Operator action rate limit exceeded. | Reject action. Log at `WARN` level. Emit diagnostic with retry-after. |
| `operator.action.execution.failed` | Operator action execution fails (e.g., drain fails, pause fails). | Log at `ERROR` level. Emit diagnostic with execution error. |

#### Failure precedence

An observability failure is additional to an existing canonical operation
diagnostic and MUST NOT translate or replace it. If mandatory audit precommit
prevents an operator or administrative action before any effect, the safe
redaction diagnostic is canonical for source-redaction failure and
`audit.event.record.failed` is canonical for append failure after successful
redaction when the action was otherwise allowed. An authorization or
validation denial remains canonical if it occurred first; failure to audit
that denied attempt is additional. Other redaction and sampling failures
classify only the rejected telemetry candidate.

### 48.3.2 Bounded Diagnostics and Evidence

> **Non-normative note.**
Diagnostics are bounded to prevent exposure of secrets, implementation
internals, or sensitive user data.
Each ordinary diagnostic includes the following fields:

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

The safe telemetry failure diagnostic used when redaction or sampling cannot
be trusted is the exact reduced schema in Section 48.1.5. It MUST NOT be
expanded with `message`, `hint`, `reference`, identifiers, or any field derived
from the rejected candidate.

> **Non-normative note.**
Diagnostics MUST NOT include:
- Raw credential values or secret references.
- Internal stack traces or implementation details.
- User data that is not relevant to the failure.
- Sensitive configuration values (e.g., database connection strings with passwords).

Evidence is retained for operational debugging and compliance auditing.
Evidence is retrievable via the `evidence inspect` CLI command or SDK
function with appropriate access controls.

### 48.3.3 Conformance Summary

> **Non-normative note.**
The following table summarizes fixed behavior, explicitly permitted formats,
and equivalence-constrained internal mechanisms from the governing contract.

| Choice | Description | Default |
| --- | --- | --- |
| Metric format | Metric export format (OTLP, Prometheus, StatsD, etc.). | OTLP. |
| Trace format | Trace context format (W3C Trace Context, etc.). | W3C Trace Context. |
| Log format | Log output format (JSON, text, syslog, etc.). | JSON. |
| Audit immutability mechanism | Mechanism for audit event immutability (hashing, append-only log, etc.). | Internal; must provide identical immutability and tamper detection. |
| Redaction levels | Redaction levels applied (source, destination, display). | Source and destination. |
| Sampling policy | Default sampling policy (`always-on`, `always-off`, `rate-limit`, etc.). | First 100 candidates in each UTC-aligned one-second family bucket. |
| Sampling failure fallback | Behavior when policy or decision fails. | Retain last valid policy or disable family; drop failed candidate; never `always-on`. |
| Redaction failure behavior | Behavior when policy validation or application fails. | Reject complete candidate and emit only safe reduced diagnostic. |
| Audit append failure | Behavior when mandatory audit intent cannot be persisted. | Reject action before effect; stop audited actions on terminal append failure pending reconciliation. |
| Cardinality limits | Cardinality limits per label family. | Fixed as defined in Section 48.1.7. |
| Retention periods | Retention periods per data type. | Fixed as defined in Section 48.1.8. |
| Export targets | Supported export targets. | OTLP required; Prometheus, StatsD, and CloudWatch independently optional. |
| Health check endpoints | Health check endpoint configuration (HTTP, gRPC, etc.). | HTTP. |
| Operator action timeout | Timeout for every operator action. | 30 seconds. |
| Operator action rate limit | Per-actor operator action limit. | 10 actions per rolling 60 seconds. |

### 48.3.4 Deferred Work

| Item | Target | Reason |
| --- | --- | --- |
| Real-time alerting | Milestone 9 Phase 4 | Requires integration with alerting systems (e.g., PagerDuty, Slack). |
| Custom metric definitions | Milestone 9 Phase 4 | Requires extensibility for user-defined metrics. |
| Distributed tracing across tenants | Milestone 9 Phase 4 | Requires multi-tenant tracing infrastructure. |
| Audit event compression | Milestone 9 Phase 5 | Requires compression algorithms for storage efficiency. |
| Health check customization | Milestone 9 Phase 5 | Requires user-defined health check logic. |
| Operator action automation | Milestone 9 Phase 5 | Requires workflow automation for common operator tasks. |

> **Non-normative note.**
All items deferred to Milestone 9 later phases fall under
Milestone 9 - Production Platform And Developer Experience
(planning document at `.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md`).
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### 48.3.5 Results That Would Invalidate an Earlier Milestone Assumption

> **Non-normative note.**
The following results from Phase 3 would invalidate an earlier milestone
assumption:

1. **Observability data bypasses authorization**: If observability data
   (logs, metrics, traces) exposes data without authorization checks, this
   would invalidate the assumption defined in
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   that all host inputs and outputs are subject to the bootstrap profile's
   authorization model.

2. **Operator actions bypass protocol validation**: If operator actions
   (e.g., drain, pause, resume) bypass protocol or runtime validation, this
   would invalidate the assumption that all host operations are validated
   against the bootstrap profile.

3. **Audit events are mutable**: If audit events can be modified or deleted
   (other than by authorized deletion of non-audit data), this would
   invalidate the assumption that audit events are immutable and tamper-evident.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Failure outcome diagnostics | Section 48.3.1 | Required | Must include all diagnostics listed in the failure outcomes tables. |
| Diagnostic field set | Section 48.3.2 | Required | Must include all fields listed in the bounded diagnostics table. |
| Diagnostic redaction | Section 48.3.2 | Required | Must redact secrets, stack traces, and irrelevant user data. |
| Actionable failure fields | Section 48.3.2 | Required | Must include `hint` and `reference` fields. |
| Safe telemetry failure fields | Section 48.3.2 | Required exception | Must contain only the reduced Section 48.1.5 fields and no candidate-derived value. |
| Redaction and sampling failure | Section 48.3.1 | Required | Must reject the candidate; must not skip redaction or enable `always-on`. |
| Audit record failure | Section 48.3.1 | Required | Must prevent an audited action when the required pre-effect append fails. |
| Conformance summary | Section 48.3.3 | Required | Must preserve fixed behavior and equivalence constraints. |
| Deferred work enforcement | Section 48.3.4 | MUST | Must NOT implement deferred work without evidence from the corresponding future phase. |

## Rationale and evidence (non-normative)

Failure evidence and operational notes for Milestone 9 Phase 3 ensure
that telemetry, tracing, audit, redaction, health, and operator action
failures are observable, debuggable, and secure.
Stable diagnostic codes enable tooling to detect and handle failures
without parsing human-readable messages.
Bounded diagnostics prevent information leakage while retaining sufficient
context for operational debugging.
Actionable failures include hints and references to enable operators to
resolve issues without consulting support.

Fixed behavior and explicitly bounded internal mechanisms enable conformance
verification and interoperability.
Deferred work is explicitly identified to prevent scope creep and ensure
that future phases build on the verified foundation of Phase 3.

Invalidating assumption conditions ensure that Phase 3 does not introduce
behavioral changes that contradict earlier milestone contracts.
