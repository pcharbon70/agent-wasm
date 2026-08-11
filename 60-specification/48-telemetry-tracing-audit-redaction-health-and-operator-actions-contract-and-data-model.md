---
title: "Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model"
kind: specification
created: "2026-08-10"
status: draft
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
  - contract
  - data-model
aliases:
  - "M9-P3-S1 Contract And Data Model"
---

# Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-03-telemetry-tracing-audit-redaction-health-and-operator-actions.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the contract and data model for telemetry, tracing, audit,
redaction, health, and operator actions.

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
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md).

## 48.1 Contract And Data Model

> **Normative definition.**
The following surfaces provide host-owned operational visibility and
bounded control without turning logs or metrics into an authority bypass.

### 48.1.1 Metrics

> **Normative definition.**
The host emits metrics for the following operational areas:

| Metric Family | Description |
| --- | --- |
| `admission` | Signal and instruction admission counts, rates, and rejection reasons. |
| `mailbox` | Mailbox queue depths, throughput, and processing latency. |
| `turns` | Agent turn counts, completion status, and duration. |
| `latency` | End-to-end latency, p50/p95/p99 percentiles, and timeouts. |
| `usage` | Resource usage (CPU, memory, disk, network) per tenant and principal. |
| `traps` | Trap detection counts, types, and handler invocations. |
| `validation` | Validation counts, success/failure rates, and failed fields. |
| `commits` | State revision commit counts, merge conflicts, and retry counts. |
| `outbox` | Outbox message counts, delivery status, and retry counts. |
| `effects` | Effect handler invocation counts, outcomes, and latency. |
| `retries` | Retry counts, backoff durations, and final outcomes. |
| `activation` | Agent activation counts, activation methods, and deactivation events. |
| `reconciliation` | Reconciliation event counts, conflict counts, and resolution outcomes. |
| `quotas` | Quota usage, limits, and enforcement events. |
| `runtime` | Runtime family-specific metrics (Extism, Wazero, Wasmtime, etc.). |

> **Non-normative note.**
Metrics are emitted in OpenTelemetry-compatible format by default.
Other formats (Prometheus, StatsD, CloudWatch) are implementation-defined
but MUST expose the same semantic data.

### 48.1.2 Traces

> **Normative definition.**
Traces link the following operational spans:

| Span | Description |
| --- | --- |
| `transport` | Signal reception and protocol handling. |
| `signal` | Signal validation and causal tracking. |
| `mailbox` | Signal queuing and dispatch. |
| `invocation` | Agent turn execution and context. |
| `state-revision` | State patch application and merge. |
| `directive` | Directive creation and dispatch. |
| `attempt` | Effect handler execution and outcomes. |
| `provider` | Downstream provider calls and responses. |
| `result-signal` | Result signal emission and tracking. |
| `downstream-turn` | Downstream agent turn execution. |

> **Non-normative note.**
Traces follow OpenTelemetry conventions where applicable.
Each span includes:
- `trace_id`: Unique trace identifier.
- `span_id`: Unique span identifier.
- `parent_span_id`: Parent span identifier (if any).
- `name`: Span name.
- `start_time`: ISO 8601 timestamp.
- `end_time`: ISO 8601 timestamp (if completed).
- `attributes`: Key-value pairs for additional context (tenant, principal, artifact, etc.).
- `status`: Span status (OK, ERROR, UNSET).
- `events`: Timestamped events within the span.

### 48.1.3 Structured Logs

> **Normative definition.**
Structured logs include the following fields:

| Field | Description |
| --- | --- |
| `timestamp` | ISO 8601 timestamp. |
| `level` | Log level (DEBUG, INFO, WARN, ERROR). |
| `message` | Human-readable log message. |
| `tenant` | Tenant identifier (if applicable). |
| `principal` | Principal identifier (if applicable). |
| `artifact` | Artifact identifier (if applicable). |
| `policy` | Policy identifier (if applicable). |
| `reason` | Stable reason identifier for the log event. |
| `context` | Additional context as key-value pairs. |

> **Non-normative note.**
Logs are emitted in JSON format by default.
Other formats (text, syslog) are implementation-defined.
Logs MUST NOT include secrets, credentials, or sensitive user data.

### 48.1.4 Audit Events

> **Normative definition.**
Audit events capture the following operations:

| Operation | Description |
| --- | --- |
| `tenant.create` | Tenant creation. |
| `tenant.update` | Tenant configuration update. |
| `tenant.delete` | Tenant deletion. |
| `principal.create` | Principal creation. |
| `principal.update` | Principal configuration update. |
| `principal.delete` | Principal deletion. |
| `artifact.register` | Artifact registration. |
| `artifact.revoke` | Artifact revocation. |
| `policy.apply` | Policy application. |
| `policy.revoke` | Policy revocation. |
| `signal.submit` | Signal submission. |
| `instruction.submit` | Instruction submission. |
| `approval.grant` | Approval granted. |
| `approval.deny` | Approval denied. |
| `operator.drain` | Operator drain action. |
| `operator.pause` | Operator pause action. |
| `operator.resume` | Operator resume action. |
| `operator.retry` | Operator retry action. |
| `operator.cancel` | Operator cancel action. |
| `operator.quarantine` | Operator quarantine action. |
| `operator.reconcile` | Operator reconcile action. |
| `operator.rotate` | Operator rotate action. |
| `operator.inspect` | Operator inspect action. |

> **Non-normative note.**
Audit events include:
- `timestamp`: ISO 8601 timestamp.
- `actor`: Principal or operator who performed the action.
- `action`: Stable action identifier (e.g., `tenant.create`).
- `resource`: Resource type and identifier (e.g., `tenant:abc123`).
- `outcome`: Success or failure.
- `reason`: Reason for the action (if applicable).
- `metadata`: Additional context as key-value pairs.

Audit events MUST be immutable and tamper-evident.

### 48.1.5 Redaction Policies

> **Normative definition.**
Redaction policies define what data is redacted from observability data:

| Data Type | Redaction Rule |
| --- | --- |
| `credentials` | Redact all credential values (API keys, tokens, passwords). |
| `secrets` | Redact all secret references and values. |
| `sensitive-pii` | Redact personally identifiable information. |
| `internal-ids` | Redact internal implementation identifiers. |
| `user-data` | Redact user data not relevant to the operation. |
| `configuration` | Redact sensitive configuration values. |

> **Non-normative note.**
Redaction is applied at the source (where data is captured) and/or at the
destination (where data is exported).
Implementations MUST document which redaction level is applied.

### 48.1.6 Sampling Policies

> **Normative definition.**
Sampling policies define which traces and logs are sampled:

| Sampling Method | Description |
| --- | --- |
| `always-on` | All traces and logs are sampled. |
| `always-off` | No traces and logs are sampled. |
| `rate-limit` | Sample traces/logs based on a rate limit (e.g., 100 per second). |
| `probabilistic` | Sample traces/logs based on a probability (e.g., 10%). |
| `header-based` | Sample traces based on incoming `traceparent` or `x-b3-flags` headers. |

> **Non-normative note.**
Sampling policies are configurable per telemetry family (traces, logs, metrics).
Default sampling is `rate-limit` with a configurable limit.

### 48.1.7 Cardinality Policies

> **Normative definition.**
Cardinality policies limit the number of unique metric label combinations:

| Label Family | Maximum Cardinality |
| --- | --- |
| `tenant` | Unbounded. |
| `principal` | Unbounded. |
| `artifact` | Unbounded. |
| `operation` | Configurable (default: 1000). |
| `endpoint` | Configurable (default: 100). |
| `custom` | Configurable (default: 100). |

> **Non-normative note.**
Exceeding cardinality limits results in:
- Metric points dropped (with diagnostic).
- Label values bucketed (e.g., `custom-1234`).

### 48.1.8 Retention Policies

> **Normative definition.**
Retention policies define how long observability data is retained:

| Data Type | Default Retention | Maximum Retention |
| --- | --- | --- |
| `metrics` | 30 days | 1 year. |
| `traces` | 7 days | 30 days. |
| `logs` | 14 days | 90 days. |
| `audit-events` | Indefinite | Indefinite. |

> **Non-normative note.**
Retention policies are configurable per deployment.
Data past retention limits is deleted or archived based on deployment configuration.

### 48.1.9 Access Control

> **Normative definition.**
Access control defines who can read observability data:

| Role | Metrics | Traces | Logs | Audit Events |
| --- | --- | --- | --- | --- |
| `tenant-admin` | Own tenant data. | Own tenant data. | Own tenant data. | Own tenant data. |
| `operator` | All metrics. | All traces. | All logs. | All audit events. |
| `auditor` | All metrics. | All traces. | All logs. | All audit events. |
| `viewer` | Read-only access. | Read-only access. | Read-only access. | Read-only access. |

> **Non-normative note.**
Access control integrates with the host's capability model.
Operators and auditors require elevated privileges.

### 48.1.10 Export Policies

> **Normative definition.**
Export policies define how observability data is exported:

| Export Target | Supported Protocols |
| --- | --- |
| `otlp` | gRPC, HTTP. |
| `prometheus` | HTTP scrape. |
| `statsd` | UDP, TCP. |
| `cloudwatch` | HTTPS API. |
| `custom` | Implementation-defined. |

> **Non-normative note.**
Multiple export targets can be configured simultaneously.
Data is exported independently to each target.

### 48.1.11 Deletion Policies

> **Normative definition.**
Deletion policies define how observability data is deleted:

| Data Type | Deletion Method |
| --- | --- |
| `metrics` | Time-based deletion (after retention limit). |
| `traces` | Time-based deletion or manual deletion by operator. |
| `logs` | Time-based deletion or manual deletion by operator. |
| `audit-events` | Immutable; no deletion permitted. |

> **Non-normative note.**
Manual deletion requires operator privileges and is logged as an audit event.

### 48.1.12 Health Models

> **Normative definition.**
Health models define the following health check types:

| Health Check | Description |
| --- | --- |
| `liveness` | Is the host process alive and responsive? |
| `readiness` | Is the host ready to accept requests? |
| `dependency` | Are downstream dependencies available? |
| `runtime-profile` | Is the configured runtime profile valid and functional? |
| `queue` | Are queues within acceptable depth limits? |
| `storage` | Is storage available and writable? |
| `scheduler` | Is the scheduler operational? |
| `coordinator` | Is the coordinator healthy? |

> **Non-normative note.**
Health checks return one of:
- `healthy`: All checks pass.
- `degraded`: Some checks fail but host is operational.
- `unhealthy`: Critical checks fail; host is not operational.

Health endpoints are exposed via:
- HTTP endpoints (e.g., `/health/live`, `/health/ready`).
- gRPC endpoints.
- SDK functions.

### 48.1.13 Operator Actions

> **Normative definition.**
Operator actions provide bounded control over the host:

| Action | Description | Authorization |
| --- | --- | --- |
| `drain` | Stop accepting new requests; complete in-flight requests. | Operator role. |
| `pause` | Pause agent execution (signals queued, no turns executed). | Operator role. |
| `resume` | Resume agent execution from paused state. | Operator role. |
| `retry` | Retry failed operations (signals, instructions, directives). | Operator role. |
| `cancel` | Cancel in-flight operations (signals, instructions, turns). | Operator role. |
| `quarantine` | Quarantine tenant or artifact (isolate from other operations). | Operator role. |
| `reconcile` | Reconcile state inconsistencies. | Operator role. |
| `rotate` | Rotate credentials, tokens, or secrets. | Operator role. |
| `inspect` | Inspect operational data (traces, logs, metrics, audit events). | Operator role or auditor. |

> **Non-normative note.**
All operator actions are:
- Authorized via the host's capability model.
- Logged as audit events.
- Bounded to prevent abuse (e.g., rate limits, timeouts).
- Reversible where possible (e.g., pause/resume, quarantine/release).

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Metric family set | Section 48.1.1 | Required | Must include all metric families listed in the table. |
| Trace span set | Section 48.1.2 | Required | Must include all spans listed in the table. |
| Log fields | Section 48.1.3 | Required | Must include all fields listed in the table. |
| Audit event operations | Section 48.1.4 | Required | Must include all operations listed in the table. |
| Redaction data types | Section 48.1.5 | Required | Must redact all data types listed in the table. |
| Sampling methods | Section 48.1.6 | MAY | Must support at least `rate-limit`. Other methods are permitted. |
| Cardinality limits | Section 48.1.7 | Implementation-defined | Must document cardinality limits for all label families. |
| Retention periods | Section 48.1.8 | Implementation-defined | Must document retention periods for all data types. |
| Access control roles | Section 48.1.9 | Required | Must include all roles listed in the table. |
| Export targets | Section 48.1.10 | MAY | Must support at least `otlp`. Other targets are permitted. |
| Deletion methods | Section 48.1.11 | Required | Must include all deletion methods listed in the table. |
| Health check types | Section 48.1.12 | Required | Must include all health check types listed in the table. |
| Operator actions | Section 48.1.13 | Required | Must include all actions listed in the table. |

## Rationale and evidence (non-normative)

The contract and data model for Milestone 9 Phase 3 provides host-owned
operational visibility and bounded control without turning logs or metrics
into an authority bypass.
Metrics, traces, logs, and audit events capture the operational state of
the host for debugging, monitoring, and compliance.
Redaction, sampling, cardinality, retention, access control, export, and
deletion policies ensure observability data is managed securely and
efficiently.
Health models provide operational visibility into the host's status.
Operator actions provide bounded control for incident response, maintenance,
and reconciliation.

These surfaces enable operators to monitor, debug, and control the host
without bypassing the protocol or runtime behavior defined in earlier
milestones.
