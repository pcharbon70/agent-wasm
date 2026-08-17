---
title: "Telemetry Tracing Audit Redaction Health And Operator Actions Behavior And Integration"
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
  - behavior
  - integration
aliases:
  - "M9-P3-S2 Behavior And Integration"
---

# Telemetry Tracing Audit Redaction Health And Operator Actions Behavior And Integration

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-03-telemetry-tracing-audit-redaction-health-and-operator-actions.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the behavior and integration rules for telemetry, tracing,
audit, redaction, health, and operator actions.

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
[Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model](48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md).

## 48.2 Behavior And Integration

### 48.2.1 Metrics Emission Behavior

> **Non-normative note.**
Metrics are emitted as operational events occur:

| Event | Metric Emitted |
| --- | --- |
| Signal admitted | `admission.total` incremented. |
| Signal rejected | `admission.rejected` incremented with rejection reason. |
| Signal processed | `turns.total` incremented. |
| Turn completed | `turns.duration` histogram updated. |
| Latency observed | `latency.{p50,p95,p99}` histogram updated. |
| Resource usage measured | `usage.cpu`, `usage.memory`, etc. updated. |
| Trap detected | `traps.detected` incremented with trap type. |
| Validation performed | `validation.total` incremented with success/failure. |
| State commit attempted | `commits.total` incremented. |
| Outbox message sent | `outbox.sent` incremented. |
| Effect handler invoked | `effects.invoked` incremented with outcome. |
| Retry attempted | `retries.total` incremented. |
| Agent activated | `activation.total` incremented. |
| Reconciliation event | `reconciliation.events` incremented. |
| Quota checked | `quotas.usage` updated. |

> **Non-normative note.**
Metrics are emitted asynchronously where possible to avoid impacting
operational performance.
Metric emission failures are logged but do not prevent the operational
event from completing.

### 48.2.2 Trace Propagation Behavior

> **Non-normative note.**
Traces are propagated across operational boundaries:

1. **Transport → Signal**: Trace context attached to incoming signal.
2. **Signal → Mailbox**: Trace context propagated to mailbox queue.
3. **Mailbox → Invocation**: Trace context attached to agent turn.
4. **Invocation → State Revision**: Trace context propagated to state operations.
5. **Invocation → Directive**: Trace context attached to directive creation.
6. **Directive → Attempt**: Trace context propagated to effect handler.
7. **Attempt → Provider**: Trace context propagated to downstream calls.
8. **Provider → Result Signal**: Trace context attached to result signal.
9. **Result Signal → Downstream Turn**: Trace context propagated to downstream agent.

> **Non-normative note.**
Trace context is propagated using W3C Trace Context format (`traceparent`
header) where applicable.
If trace context is missing (e.g., local execution), a new trace is started.

### 48.2.3 Log Emission Behavior

> **Non-normative note.**
Logs are emitted with the following behavior:

| Log Level | When Emitted |
| --- | --- |
| `DEBUG` | Detailed operational information (e.g., signal validation details). |
| `INFO` | Normal operational events (e.g., signal admitted, turn completed). |
| `WARN` | Abnormal but recoverable events (e.g., retry attempt, rate limit approaching). |
| `ERROR` | Failures requiring attention (e.g., validation failure, effect handler error). |

> **Non-normative note.**
Logs are emitted to:
- Standard error (stderr) by default.
- Configured log exporters (e.g., syslog, file, cloud logging).

Log emission failures are logged but do not prevent the operational event.

### 48.2.4 Audit Event Recording Behavior

> **Normative definition.**
Audit events are recorded with the following behavior:

1. Detect operator or administrative action.
2. Evaluate authorization and validation without executing the action.
3. Capture and source-redact actor, action, resource, and attempted outcome.
4. If source redaction fails, return the applicable safe redaction diagnostic
   and do not execute or publish the action's effect.
5. Durably append the `attempted` event to the immutable log.
6. If the append fails, return `audit.event.record.failed` and do not execute
   or publish the action's effect.
7. If authorization or validation denied the action, append a correlated
   `failure` event, return the original denial diagnostic, and do not execute.
8. Otherwise execute the action only after the durable append succeeds.
9. Durably append a correlated terminal `success` or `failure` event.
10. Emit recorded audit events to configured exporters, if configured.
11. Return the action result or failure diagnostic.

If the terminal append fails after an effect, the durable attempted event
remains authoritative evidence. The host MUST emit
`audit.event.record.failed`, mark audit health `unhealthy`, stop accepting new
operator or administrative actions, and reconcile the attempted event before
resuming those actions.

> **Non-normative note.**
Audit events are:
- Immutable (cannot be modified or deleted).
- Tamper-evident (cryptographic hashing or similar mechanism).
- Retained indefinitely (per retention policy).

### 48.2.5 Redaction Behavior

> **Normative definition.**
Redaction is applied at the following points:

| Point | Redaction Applied |
| --- | --- |
| Data capture | Redact credentials, secrets, PII at source before buffering or persistence. |
| Data export | Reapply redaction before export. |
| Data display | Reapply redaction in UI or CLI output. |

> **Non-normative note.**
Redaction rules are applied in the following order:
1. Credentials (API keys, tokens, passwords).
2. Secrets (secret references and values).
3. Sensitive PII (names, addresses, phone numbers, etc.).
4. Internal IDs (implementation-specific identifiers).
5. User data (not relevant to the operation).
6. Configuration (sensitive values like database connection strings).

If policy validation or any redaction step fails, the host MUST reject the
complete candidate record. It MUST NOT buffer, persist, export, display, or
include any candidate field in a fallback. It emits only the fixed safe
telemetry failure diagnostic from Section 48.1.5.

### 48.2.6 Sampling Behavior

> **Normative definition.**
Sampling is applied based on the configured sampling policy:

| Policy | Behavior |
| --- | --- |
| `always-on` | All traces/logs sampled. |
| `always-off` | No traces/logs sampled. |
| `rate-limit` | Sample until rate limit reached; drop excess. |
| `probabilistic` | Randomly sample based on probability. |
| `header-based` | Sample based on incoming headers. |

> **Normative definition.**
Trace sampling decisions are made at trace start. Log sampling decisions are
made before source-redacted records enter a buffer. Once sampled, a trace is
retained for its full duration. Unsampled candidates produce no trace or log
record. An invalid policy is rejected while the last valid policy remains in
force; without a last valid policy, the affected family is disabled. A failed
individual decision drops the candidate with `trace.sample.failed` and MUST
NOT enable `always-on` fallback. A log decision failure instead emits
`log.sample.failed`. The default rate limit resets only at UTC second
boundaries and admits the first 100 candidates in per-family capture order.

### 48.2.7 Cardinality Enforcement Behavior

> **Non-normative note.**
Cardinality limits are enforced as follows:

1. Track unique label combinations per metric family.
2. If limit exceeded:
   - Drop the metric point.
   - Emit `metrics.cardinality.exceeded`.
3. Log cardinality enforcement events at `WARN` level.

> **Non-normative note.**
Cardinality limits are the fixed values in Section 48.1.7.

### 48.2.8 Retention Enforcement Behavior

> **Non-normative note.**
Retention is enforced via background jobs:

| Data Type | Enforcement Method |
| --- | --- |
| `metrics` | Make data unavailable exactly 30 days after capture. |
| `traces` | Make data unavailable exactly 7 days after capture. |
| `logs` | Make data unavailable exactly 14 days after capture. |
| `audit-events` | No enforcement (indefinite retention). |

> **Non-normative note.**
Cleanup scheduling and storage layout are non-normative internal mechanisms.
They MAY vary only if data availability at each retention boundary and all
observable deletion evidence are identical for the same input and clock.

### 48.2.9 Access Control Enforcement Behavior

> **Non-normative note.**
Access control is enforced at the following points:

| Point | Enforcement |
| --- | --- |
| API request | Check actor role and permissions before processing request. |
| Data export | Check actor role before exporting data. |
| Operator action | Check actor role before executing action. |

> **Non-normative note.**
Access control failures produce:
- `unauthorized` diagnostic.
- Audit event recording the failed access attempt.
- No data or action is performed.

### 48.2.10 Export Behavior

> **Non-normative note.**
Data is exported to configured targets asynchronously:

1. Buffer observability data in memory or disk.
2. Batch data for efficient export (e.g., 100 spans per batch).
3. Export to configured targets (e.g., OTLP, Prometheus, StatsD).
4. Retry failed exports with exponential backoff.
5. Drop data if retry limit exceeded (with diagnostic).

> **Non-normative note.**
Export configuration includes:
- Target URL or endpoint.
- Authentication credentials (if required).
- Batch size and flush interval.
- Retry policy (max retries, backoff duration).

Buffering, batch size, and flush scheduling are non-normative internal
mechanisms. They MAY vary only if each configured target receives the same
ordered data and the same retry-limit diagnostics are emitted for the same
input and dependency outcomes.

### 48.2.11 Deletion Behavior

> **Non-normative note.**
Deletion is performed as follows:

| Data Type | Deletion Behavior |
| --- | --- |
| `metrics` | Time-based deletion via cleanup job. |
| `traces` | Time-based deletion via cleanup job or manual deletion by operator. |
| `logs` | Time-based deletion via cleanup job or manual deletion by operator. |
| `audit-events` | No deletion permitted. |

> **Non-normative note.**
Manual deletion requires operator privileges and is logged as an audit event.
Deletion is irreversible.

### 48.2.12 Health Check Behavior

> **Non-normative note.**
Health checks are performed as follows:

| Health Check | Check Method |
| --- | --- |
| `liveness` | Process alive (e.g., heartbeat, ping). |
| `readiness` | Dependencies available, queues within limits. |
| `dependency` | Downstream services respond within timeout. |
| `runtime-profile` | Runtime profile valid and functional. |
| `queue` | Queue depths within configured limits. |
| `storage` | Storage writable and accessible. |
| `scheduler` | Scheduler operational (e.g., can schedule tasks). |
| `coordinator` | Coordinator healthy (e.g., responsive to coordination requests). |

> **Non-normative note.**
Health check results are:
- Aggregated into overall health status (`healthy`, `degraded`, `unhealthy`).
- Exposed via health endpoints (HTTP, gRPC, SDK).
- Logged at `INFO` (healthy), `WARN` (degraded), `ERROR` (unhealthy).

### 48.2.13 Operator Action Execution Behavior

> **Normative definition.**
Operator actions are executed with the following behavior:

1. **Authorization**: Evaluate actor role and permissions without executing.
2. **Validation**: Evaluate action parameters without executing.
3. **Audit intent**: Durably append a source-redacted `attempted` audit event
   whether the evaluation allowed or denied the action.
4. **Redaction failure**: If source redaction fails, return the safe redaction
   diagnostic without executing the action.
5. **Audit failure**: If the append fails, return
   `audit.event.record.failed` without executing the action.
6. **Denied outcome**: If authorization or validation denied the action,
   append a correlated failure event and return the original denial diagnostic
   without execution.
7. **Execution**: Otherwise execute the action (e.g., drain, pause, resume).
8. **Audit outcome**: Append a correlated terminal audit event.
9. **Confirmation**: Return success or failure diagnostic.
10. **Logging**: Log action execution at appropriate level.

> **Non-normative note.**
Operator actions are:
- Cancelled with `operator.action.timeout` if not complete within 30 seconds.
- Limited to 10 actions per actor in each rolling 60-second interval.
- Reversible where possible (e.g., pause/resume, quarantine/release).

### 48.2.14 Failure precedence

An observability failure MUST NOT replace an operation's existing canonical
diagnostic merely because recording or export also failed. The observability
diagnostic is additional. For an operator or administrative action prevented
before any effect, the applicable safe redaction diagnostic is canonical when
audit source redaction failed, and `audit.event.record.failed` is canonical
when append of an already redacted attempted event is the reason an otherwise
allowed action cannot proceed. If authorization or validation had already
denied the action, that original diagnostic remains canonical and an audit
failure is additional. Other redaction and sampling failures govern only
publication of their candidate telemetry record and MUST NOT disclose or
translate the triggering operation's diagnostic.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Metrics emission asynchrony | Section 48.2.1 | MUST | Must emit metrics asynchronously where possible. |
| Trace context propagation format | Section 48.2.2 | MAY | Must support W3C Trace Context format. Other formats are permitted. |
| Log emission destinations | [Log Emission Behavior](#4823-log-emission-behavior) | MAY | Must emit to standard error; configured exporters are permitted. |
| Audit event immutability mechanism | [Audit Event Recording Behavior](#4824-audit-event-recording-behavior) | Internal mechanism | May vary only if audit events remain immutable and the same modifications are detected. |
| Audit precommit failure | [Audit Event Recording Behavior](#4824-audit-event-recording-behavior) | Required | Prevent the operator or administrative effect and return `audit.event.record.failed`. |
| Redaction order | Section 48.2.5 | Required | Must apply redaction in the order listed in the table. |
| Redaction failure | Section 48.2.5 | Required | Reject the complete candidate and emit only the fixed safe diagnostic. |
| Sampling decision point | Section 48.2.6 | MUST | Must make sampling decisions at trace start. |
| Sampling fallback | Section 48.2.6 | Prohibited | Retain the last valid policy or disable the family; use the family-specific failure diagnostic and never fall back to `always-on`. |
| Cardinality limit enforcement | Section 48.2.7 | MUST | Must drop excess metric points and emit `metrics.cardinality.exceeded`. |
| Retention enforcement mechanism | [Retention Enforcement Behavior](#4828-retention-enforcement-behavior) | Internal mechanism | May vary only if fixed expiration boundaries and observable deletion evidence are identical. |
| Access control check points | Section 48.2.9 | Required | Must enforce access control at all points listed in the table. |
| Export batching | [Export Behavior](#48210-export-behavior) | Internal mechanism | May vary only if ordered exports and retry-limit diagnostics are identical. |
| Manual deletion audit | Section 48.2.11 | MUST | Must log manual deletion as an audit event. |
| Health check aggregation | Section 48.2.12 | MUST | Must aggregate health checks into overall status. |
| Operator action timeout | [Operator Action Execution Behavior](#48213-operator-action-execution-behavior) | Required | Cancel each action after exactly 30 seconds. |
| Operator action rate limit | [Operator Action Execution Behavior](#48213-operator-action-execution-behavior) | Required | Accept at most 10 actions per actor in a rolling 60-second interval. |
| Failure precedence | Section 48.2.14 | Required | Preserve the operation diagnostic except when audit precommit prevents the action effect. |

## Rationale and evidence (non-normative)

Behavior and integration rules for Milestone 9 Phase 3 ensure that
telemetry, tracing, audit, redaction, health, and operator actions work
correctly and integrate with the host runtime.

Metrics, traces, logs, and audit events capture operational state
asynchronously to avoid impacting performance.
Trace context is propagated across operational boundaries using standard
formats.
Logs are emitted at appropriate levels with stable reason identifiers.
Audit events are immutable and tamper-evident for compliance.

Redaction, sampling, cardinality, retention, access control, export, and
deletion policies ensure observability data is managed securely and
efficiently.
Health checks provide operational visibility into the host's status.
Operator actions provide bounded control for incident response, maintenance,
and reconciliation.

These behaviors ensure that observability data is useful for debugging,
monitoring, and compliance without impacting operational performance or
exposing sensitive data.
