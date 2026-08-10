---
title: "Embedded And Server Host APIs Configuration And Packaging Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-10"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-01
  - host-api
  - configuration
  - packaging
  - failure-evidence
  - operational-notes
aliases:
  - "M9-P1-S3 Failure Evidence And Operational Notes"
---

# Embedded And Server Host APIs Configuration And Packaging Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-01-embedded-and-server-host-apis-configuration-and-packaging.md)
of
[Milestone 9](../../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the failure evidence and operational notes for embedded
and server host APIs, configuration, and packaging.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
integration tests in
Section [Phase 1 Integration Tests](46-embedded-and-server-host-apis-configuration-and-packaging-phase-1-integration-tests.md)
and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Embedded And Server Host APIs Configuration And Packaging Behavior And Integration](46-embedded-and-server-host-apis-configuration-and-packaging-behavior-and-integration.md).

## 46.3 Failure Evidence And Operational Notes

### 46.3.1 Failure Outcomes

> **Normative definition.**
The following failure outcomes are relevant to embedded and server host
APIs, configuration, and packaging.
Each outcome includes a stable diagnostic code family, cause, and host
behavior.

#### Configuration failures

| Diagnostic | Cause | Host behavior |
| --- | --- | --- |
| `config.validation.failed` | Configuration does not match schema, required fields are missing, or types are invalid. | Reject initialization. Emit diagnostic with validation errors. |
| `config.secret.resolve.failed` | Secret reference cannot be resolved (missing key, invalid path, access denied). | Reject initialization. Emit diagnostic with secret path. Do NOT expose secret value. |
| `config.profile.unknown` | Referenced profile does not exist. | Reject initialization. Emit diagnostic with profile name. Fall back to default profile if available. |
| `config.load.failed` | Configuration source is unreachable or unreadable. | Reject initialization. Emit diagnostic with source name. Retry if remote source. |

#### Initialization failures

| Diagnostic | Cause | Host behavior |
| --- | --- | --- |
| `init.dependency.missing` | Required dependency is not provided (e.g., storage, runtime). | Reject initialization. Emit diagnostic with dependency name. |
| `init.dependency.unavailable` | Required dependency is provided but unreachable or unhealthy. | Reject initialization. Emit diagnostic with dependency name and error. Retry if transient. |
| `init.artifact.register.failed` | Artifact registration fails (invalid manifest, schema mismatch, signature verification failure). | Reject initialization. Emit diagnostic with artifact digest and error. |
| `init.ready.timeout` | Host does not become ready within the configured timeout. | Reject readiness. Emit diagnostic with timeout duration. Retry if dependencies are transient. |

#### Operation failures

| Diagnostic | Cause | Host behavior |
| --- | --- | --- |
| `request.idempotent_duplicate` | Duplicate idempotency key for a completed request. | Reject request. Emit diagnostic with original request ID. Do NOT re-execute side effects. |
| `request.pagination.invalid` | Pagination cursor is invalid or expired. | Reject request. Emit diagnostic with cursor. Return first page if cursor is missing. |
| `request.operation.unknown` | Operation name is not recognized. | Reject request. Emit diagnostic with operation name. Return list of valid operations if `capabilities.discover` is supported. |
| `request.envelope.malformed` | Request envelope is missing required fields or has invalid structure. | Reject request. Emit diagnostic with missing field names. |
| `agent.create.failed` | Agent creation fails (manifest not found, schema validation error, state initialization error). | Reject creation. Emit diagnostic with agent identity and error. Do NOT create partial agent state. |
| `agent.delete.in_use` | Agent is hibernated or has in-flight turns. | Reject deletion. Emit diagnostic with agent status. Require explicit force flag to override. |
| `signal.submit.invalid` | Signal does not match expected schema or causal constraints. | Reject submission. Emit diagnostic with signal ID and error. Do NOT create state or journal entries. |
| `topology.update.conflict` | Topology update conflicts with existing placement or lease. | Reject update. Emit diagnostic with conflict details. Return current topology. |
| `approval.request.timeout` | Approval request does not receive response within configured timeout. | Cancel approval request. Emit diagnostic with timeout duration. Proceed with default disposition if configured. |
| `diagnostic.get.unauthorized` | Requester does not have permission to retrieve diagnostics. | Reject request. Emit diagnostic with requester identity. Do NOT expose diagnostic content. |

#### Transport failures

| Diagnostic | Cause | Host behavior |
| --- | --- | --- |
| `transport.server.start.failed` | Server adapter cannot bind to configured address or port. | Reject startup. Emit diagnostic with address and error. Retry if port is transient. |
| `transport.connection.lost` | Client connection is lost during request processing. | Cancel request. Emit diagnostic with request ID. Do NOT leave partial state. |
| `transport.timeout` | Request exceeds configured timeout. | Cancel request. Emit diagnostic with timeout duration. Release resources. |
| `transport.rate_limit.exceeded` | Request rate exceeds configured limit. | Reject request. Emit diagnostic with current rate and limit. Return retry-after header or equivalent. |

### 46.3.2 Bounded Diagnostics and Evidence

> **Non-normative note.**
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

> **Non-normative note.**
Diagnostics MUST NOT include:
- Raw credential values or secret references.
- Internal stack traces or implementation details.
- User data that is not relevant to the failure.
- Sensitive configuration values (e.g., database connection strings with passwords).

Evidence is retained for operational debugging and compliance auditing.
Evidence is retrievable via the `diagnostic.get` operation with appropriate
access controls.

### 46.3.3 Implementation-Defined Choices

> **Non-normative note.**
The following choices are implementation-defined and must be documented
in the conformance profile.

| Choice | Description | Default |
| --- | --- | --- |
| Pagination default limit | Default number of results per page. | 100 |
| Pagination maximum limit | Maximum number of results per page. | 1000 |
| Idempotency key retention duration | Duration for which idempotency keys are retained. | 24 hours |
| Configuration validation strictness | Whether to reject configuration with warnings or errors. | Reject with errors. |
| Secret store retry count | Number of retries for secret resolution. | 3 |
| Secret store retry backoff | Backoff strategy for secret resolution retries. | Exponential with jitter. |
| Initialization timeout | Duration to wait for host to become ready. | 30 seconds |
| Request timeout | Duration to wait for request completion. | 60 seconds |
| Rate limit window | Time window for rate limit calculation. | 1 second |
| Rate limit maximum | Maximum number of requests per window. | 1000 |

### 46.3.4 Deferred Work

| Item | Target | Reason |
| --- | --- | --- |
| Dynamic configuration reload | Milestone 9 Phase 4 | Requires compatibility and upgrade infrastructure |
| Multi-tenant configuration isolation | Milestone 9 Phase 4 | Requires production platform and deployment |
| Configuration diff and merge UI | Milestone 9 Phase 5 | Requires developer experience and tooling |
| Configuration audit logging | Milestone 9 Phase 3 | Requires telemetry and tracing infrastructure |

> **Non-normative note.**
All items deferred to Milestone 9 later phases fall under
Milestone 9 - Production Platform And Developer Experience
(planning document at `.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md`).
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### 46.3.5 Results That Would Invalidate an Earlier Milestone Assumption

> **Non-normative note.**
The following results from Phase 1 would invalidate an earlier milestone
assumption:

1. **Host operations expose secrets**: If host operations expose raw
   credentials, secret values, or implementation internals, this would
   invalidate the assumption defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant and credentials are
   separated from state.

2. **Configuration injection bypasses validation**: If configuration
   injection bypasses schema validation or required field checks, this
   would invalidate the assumption defined in
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   that all host inputs are validated against the bootstrap profile.

3. **Server adapters alter protocol semantics**: If server adapters
   alter the canonical envelope structure or operation semantics, this
   would invalidate the assumption that transport is independent of
   protocol (this section's core design principle).

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Failure outcome diagnostics | Section 46.3.1 | Required | Must include all diagnostics listed in the failure outcomes tables. |
| Diagnostic field set | Section 46.3.2 | Required | Must include all fields listed in the bounded diagnostics table. |
| Diagnostic redaction | Section 46.3.2 | Required | Must redact secrets, stack traces, and irrelevant user data. |
| Implementation-defined choices documentation | Section 46.3.3 | Required | Must document all implementation-defined choices in the conformance profile. |
| Deferred work enforcement | Section 46.3.4 | MUST | Must NOT implement deferred work without evidence from the corresponding future phase. |

## Rationale and evidence (non-normative)

Failure evidence and operational notes for Milestone 9 Phase 1 ensure
that embedded and server host APIs, configuration, and packaging failures
are observable, debuggable, and secure.
Stable diagnostic codes enable tooling to detect and handle failures
without parsing human-readable messages.
Bounded diagnostics prevent information leakage while retaining sufficient
context for operational debugging.

Implementation-defined choices are documented to enable conformance
verification and interoperability.
Deferred work is explicitly identified to prevent scope creep and ensure
that future phases build on the verified foundation of Phase 1.
