---
title: "Examples Runbooks SLO Evidence And Production Acceptance Contract And Data Model"
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
  - contract
  - data-model
aliases:
  - "M9-P5-S1 Contract And Data Model"
---

# Examples Runbooks SLO Evidence And Production Acceptance Contract And Data Model

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the contract and data model for examples, runbooks, SLOs,
evidence, and production acceptance.

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
.

## 50.1 Contract And Data Model

> **Normative definition.**
The following surfaces demonstrate that developers and operators can build,
deploy, observe, recover, and upgrade representative systems using only
supported surfaces.

### 50.1.1 Maintained Examples

> **Normative definition.**
The following examples are maintained and serve as canonical references:

| Example | Description |
| --- | --- |
| `direct-reducer` | Direct reducer with simple input/output. |
| `fsm-continuation` | FSM continuation with state transitions. |
| `scheduled-workflow` | Scheduled workflow with time-based triggers. |
| `tool-loop` | Tool loop with retrieval and code execution. |
| `approval` | Approval workflow with human-in-the-loop. |
| `retrieval` | Retrieval-augmented generation with external knowledge. |
| `multi-agent-fan-out-fan-in` | Multi-agent fan-out/fan-in with delegation. |
| `migration` | State migration with schema evolution. |

> **Non-normative note.**
Examples include:
- Complete source code (SDK bindings, manifest, fixtures).
- README with setup, run, and test instructions.
- Evidence records from fixture execution.
- Links to relevant specification chapters.

### 50.1.2 Runbooks

> **Normative definition.**
The following runbooks are maintained for operational procedures:

| Runbook | Description |
| --- | --- |
| `dependency-failure` | Handle downstream dependency failures. |
| `queue-overload` | Handle mailbox or outbox queue overload. |
| `stuck-turn` | Handle agent turns that are stuck or unresponsive. |
| `repeated-effect` | Handle effect handlers that produce repeated outcomes. |
| `runtime-divergence` | Handle runtime divergence between nodes. |
| `artifact-revocation` | Handle artifact revocation or security incidents. |
| `tenant-incident` | Handle tenant-specific incidents or data issues. |
| `recovery` | Recover host state from backup or checkpoint. |
| `rollback` | Rollback host or upgrade to previous version. |

> **Non-normative note.**
Runbooks include:
- Symptom detection (logs, metrics, traces, audit events).
- Diagnosis steps (commands to run, data to collect).
- Remediation steps (commands to execute, configuration changes).
- Verification steps (commands to confirm resolution).
- Escalation criteria (when to escalate to support).

### 50.1.3 Service Level Objectives (SLOs)

> **Normative definition.**
The following service level objectives are maintained:

| Objective | Description | Target | Error Budget |
| --- | --- | --- | --- |
| `admission` | Signal and instruction admission success rate. | 99.9% | 0.1%. |
| `turn-latency` | Agent turn completion latency (p95). | < 500ms. | 50ms. |
| `durability` | State durability (no data loss across restarts). | 100%. | 0%. |
| `effect-delay` | Effect handler execution delay (p95). | < 100ms. | 10ms. |
| `recovery` | Recovery time after host failure. | < 5 minutes. | 1 minute. |
| `availability` | Host availability (ready to accept requests). | 99.9%. | 0.1%. |
| `isolation` | Tenant isolation (no cross-tenant data leakage). | 100%. | 0%. |
| `evidence-completeness` | Evidence completeness for milestone acceptance. | 100%. | 0%. |

> **Normative definition.**
Every SLO measurement uses the half-open rolling window `[T - 30 days, T)`,
where `T` is a UTC minute boundary. The host computes one measurement at every
UTC minute boundary. Events exactly at the start are included; events exactly
at `T` are deferred to the next measurement. Durations use integer
nanoseconds. Counts and durations MUST NOT be sampled or estimated.

> **Normative definition.**
Each SLO measurement record contains `objective`, `window_start`, `window_end`,
`eligible_units`, `bad_units`, `observed_value`, `target`,
`error_budget_total`, `error_budget_consumed`, `error_budget_remaining`,
`status`, and the ordered digests of its source records. `status` is `met`,
`violated`, or `unavailable`. Zero eligible units produce `unavailable`, not a
successful measurement, and block production acceptance. Source digests are
ordered by ascending source timestamp and then ascending digest bytes;
duplicate source records remain duplicate entries.

> **Normative definition.**
The exact objective calculations are:

| Objective | Eligible and bad units | Observed value and target comparison |
| --- | --- | --- |
| `admission` | Eligible units are all completed signal and instruction admission decisions; bad units are rejected decisions other than caller cancellation before validation. | `(eligible_units - bad_units) / eligible_units`; `met` when at least `0.999`. |
| `turn-latency` | Eligible units are completed turns with valid start and completion timestamps; bad units are turns whose duration is at least 500,000,000 ns. | Sort eligible durations ascending and select rank `ceil(0.95 * eligible_units)`, using one-based ranks; `met` when the selected duration is strictly less than 500,000,000 ns. |
| `durability` | Eligible units are acknowledged durable state commits; bad units are eligible commits detected missing or digest-mismatched after restart, recovery, or integrity verification. | `(eligible_units - bad_units) / eligible_units`; `met` only at exactly `1`. |
| `effect-delay` | Eligible units are effects with both durable-ready and execution-start timestamps; bad units have delay at least 100,000,000 ns. | Nearest-rank p95 as defined for `turn-latency`; `met` when strictly less than 100,000,000 ns. |
| `recovery` | Eligible units are completed host-failure recovery episodes; bad units are episodes lasting at least 300,000,000,000 ns. | Maximum eligible recovery duration; `met` when strictly less than 300,000,000,000 ns. |
| `availability` | Eligible units are nanoseconds during which the deployment is scheduled to serve; bad units are eligible nanoseconds in which readiness is not `healthy`. Maintenance remains eligible. Readiness is piecewise constant from each durable readiness transition until the next; absence of a known state at the window start makes the measurement unavailable. | `(eligible_units - bad_units) / eligible_units`; `met` when at least `0.999`. |
| `isolation` | Eligible units are completed tenant-boundary access attempts and required isolation probes; bad units are unauthorized cross-tenant reads, writes, disclosures, or effects. | `(eligible_units - bad_units) / eligible_units`; `met` only at exactly `1`. |
| `evidence-completeness` | Eligible units are required evidence slots for each production-acceptance candidate evaluated in the window; bad units are absent, invalid, unverifiable, or inaccessible required records. | `(eligible_units - bad_units) / eligible_units`; `met` only at exactly `1`. |

For `admission` and `availability`, budget consumed in percentage points is
exactly `100 * bad_units / eligible_units` and budget remaining is
`max(0, 0.1 - consumed)`. For
`turn-latency`, `effect-delay`, and `recovery`, budget consumed is
`max(0, observed_duration - target_duration)` and remaining is respectively
`max(0, 50 ms - consumed)`, `max(0, 10 ms - consumed)`, or
`max(0, 1 minute - consumed)`. A strict duration target is violated when the
observed duration equals its target. The three zero-budget objectives have
`error_budget_total`, `error_budget_consumed`, and `error_budget_remaining`
equal to zero. They are exhausted only when their status is `violated`, not
while it is `met`.

> **Non-normative note.**
SLOs are measured via:
- Metrics (e.g., admission success rate, turn latency percentiles).
- Health checks (e.g., availability, recovery).
- Audit events (e.g., evidence completeness).

SLOs are reported in:
- SLO status page (web UI).
- SLO API endpoints (HTTP/gRPC).
- SLO reports (generated on demand or periodically).

### 50.1.4 Production Acceptance Evidence

> **Normative definition.**
Production acceptance evidence includes:

| Evidence Type | Description |
| --- | --- |
| `slo-evidence` | SLO compliance evidence (metrics, health checks, audit events). |
| `runbook-evidence` | Runbook execution evidence (symptoms, diagnosis, remediation). |
| `example-evidence` | Example execution evidence (source, output, tests). |
| `conformance-evidence` | Conformance test suite evidence (all tests passing). |
| `security-evidence` | Security audit evidence (vulnerabilities, compliance). |
| `performance-evidence` | Performance test evidence (load, soak, fault scenarios). |

> **Normative definition.**
Every production acceptance evidence record and its canonical bytes MUST be
retained indefinitely and MUST NOT be deleted. A host MAY migrate, replicate,
or change the storage tier or backend only when the evidence identity,
canonical bytes, digest, tenant isolation, authorization, and retrieval
behavior remain unchanged. A deletion request for production acceptance
evidence MUST be rejected without modifying the evidence.

This rule explicitly replaces the operator-deletion exception and finite
post-retention availability permitted for general evidence by
[Host-owned evidence recording](34-provenance-signing-audit-security-and-milestone-acceptance.md#host-owned-evidence-recording).
For every record classified as production acceptance evidence, an operator
action, elapsed retention period, storage-tier change, or backend migration
does not authorize deletion or unavailability. Chapter 34 continues to govern
evidence that is not production acceptance evidence.

> **Non-normative note.**
Evidence is:
- Immutable (cannot be modified after generation).
- Tamper-evident (cryptographic hashing).
- Retained indefinitely (per retention policy).
- Accessible via `evidence inspect` CLI command or SDK function.

### 50.1.5 Support Matrix

> **Normative definition.**
The support matrix defines supported configurations:

| Component | Supported Versions | Notes |
| --- | --- | --- |
| `host` | Current and previous major version. | Older versions deprecated after 6 months. |
| `protocol` | Current and previous minor version. | Older versions deprecated after 3 months. |
| `manifest` | Current and previous patch version. | Older versions deprecated after 1 month. |
| `guest-sdk` | Current and previous major version. | Older versions deprecated after 6 months. |
| `runtime` | All runtimes listed in compatibility matrix. | See compatibility matrix for details. |
| `storage` | All storages listed in compatibility matrix. | See compatibility matrix for details. |
| `provider` | All providers listed in compatibility matrix. | See compatibility matrix for details. |

> **Non-normative note.**
Support matrix is updated with each release.
Deprecated versions are marked with:
- Deprecation date.
- Sunset date.
- Migration path.

### 50.1.6 Residual Risks

> **Normative definition.**
The following residual risks are documented for production deployments:

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `runtime-divergence` | Low. | High. | Fencing, leader election. |
| `queue-overload` | Medium. | Medium. | Rate limiting, backpressure. |
| `effect-repeated` | Low. | Medium. | Idempotency keys, deduplication. |
| `evidence-loss` | Low. | High. | Backup, replication. |
| `upgrade-failure` | Low. | High. | Checkpoints, rollback. |

> **Non-normative note.**
Residual risks are reviewed quarterly or after significant changes.
Mitigations are updated as new risks are identified or existing risks change.

### 50.1.7 Release Ownership

> **Normative definition.**
The following roles own release processes:

| Role | Responsibilities |
| --- | --- |
| `release-manager` | Coordinate release schedule, approve releases. |
| `security-reviewer` | Review security implications, approve security releases. |
| `operations-engineer` | Execute deployment, monitor post-release. |
| `developer` | Write code, run tests, create release notes. |
| `product-manager` | Define release scope, prioritize features. |

> **Non-normative note.**
Release ownership is documented in:
- Release playbook.
- Incident response plan.
- Communication templates.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Example set | Section 50.1.1 | Required | Must include all examples listed in the table. |
| Runbook set | Section 50.1.2 | Required | Must include all runbooks listed in the table. |
| SLO set | Section 50.1.3 | Required | Must include all SLOs listed in the table. |
| SLO targets | [Service Level Objectives](#5013-service-level-objectives-slos) | Required | Must use every target exactly as listed in the SLO table. |
| SLO error budgets | [Service Level Objectives](#5013-service-level-objectives-slos) | Required | Must use every error budget exactly as listed in the SLO table. |
| SLO measurement window | [Service Level Objectives](#5013-service-level-objectives-slos) | Required | Use the exact rolling 30-day half-open window at every UTC minute boundary. |
| SLO formulas | [Service Level Objectives](#5013-service-level-objectives-slos) | Required | Use the exact eligible units, bad units, nearest-rank percentile, strict comparisons, and budget formulas. |
| Evidence types | Section 50.1.4 | Required | Must include all evidence types listed in the table. |
| Evidence retention | [Production Acceptance Evidence](#5014-production-acceptance-evidence) | Fixed requirement | Retain canonical evidence indefinitely; reject deletion; storage mechanisms may vary only with identical evidence and retrieval behavior. |
| Evidence-deletion precedence | [Production Acceptance Evidence](#5014-production-acceptance-evidence) | Explicit replacement | Chapter 34 operator and post-retention deletion permissions do not apply to production acceptance evidence. |
| Support matrix components | Section 50.1.5 | Required | Must include all components listed in the table. |
| Residual risks | Section 50.1.6 | Required | Must include all risks listed in the table. |
| Release ownership roles | Section 50.1.7 | Required | Must include all roles listed in the table. |

## Rationale and evidence (non-normative)

The contract and data model for Milestone 9 Phase 5 demonstrates that
developers and operators can build, deploy, observe, recover, and upgrade
representative systems using only supported surfaces.
Maintained examples serve as canonical references for common agent patterns.
Runbooks provide operational procedures for common failure scenarios.
SLOs define measurable service objectives for production deployments.
Production acceptance evidence validates that the system meets conformance,
security, and performance requirements.
Support matrix defines supported configurations for production deployments.
Residual risks document known risks and mitigations.
Release ownership defines roles and responsibilities for release processes.

These surfaces ensure that production deployments are well-documented,
measurable, and supported.
