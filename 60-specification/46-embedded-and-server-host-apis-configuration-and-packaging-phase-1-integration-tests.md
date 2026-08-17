---
title: "Embedded And Server Host APIs Configuration And Packaging Phase 1 Integration Tests"
kind: specification
created: "2026-08-10"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-01
  - host-api
  - configuration
  - packaging
  - integration-tests
  - phase-1
aliases:
  - "M9-P1-S4 Phase 1 Integration Tests"
---

# Embedded And Server Host APIs Configuration And Packaging Phase 1 Integration Tests

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-01-embedded-and-server-host-apis-configuration-and-packaging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It defines the integration tests that verify embedded and server host APIs,
configuration, and packaging across their real dependency boundaries.

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
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Embedded And Server Host APIs Configuration And Packaging Behavior And Integration](46-embedded-and-server-host-apis-configuration-and-packaging-behavior-and-integration.md),
[Embedded And Server Host APIs Configuration And Packaging Failure Evidence And Operational Notes](46-embedded-and-server-host-apis-configuration-and-packaging-failure-evidence-and-operational-notes.md).

## 46.4 Phase 1 Integration Tests

This section defines the observable behavior that the Phase 1 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### 46.4.1 Successful flow

The host MUST accept well-formed requests, execute operations, and return
canonical responses with complete evidence.
The test MUST verify that:

1. Each host operation from the operations catalog (Section 46.1.1) is
   callable with a valid envelope.
2. Configuration is loaded from defaults, file, and environment sources at
   precedence 0, 10, and 20 and merged correctly; each implemented optional
   source is also verified at its fixed precedence.
3. Secrets are resolved from the secrets manager without exposure in
   diagnostics or logs.
4. Profiles are selected and applied correctly.
5. Runtime and storage adapters are initialized and functional.
6. Server adapters serialize operations over the configured transport
   without altering protocol semantics.
7. Pagination defaults to 100 results, accepts limits from 1 through 1000,
   and returns correct cursors for continuation.
8. Idempotent operations with the same key produce the same result
   without re-executing side effects.
9. The host transitions through lifecycle states (configure, initialize,
   ready, drain, shutdown) correctly.
10. The test records and retains:
    - The request envelope and its identifiers.
    - The response envelope and its structure.
    - The configuration sources and precedence order applied.
    - The secret resolution results (without exposing values).
    - The adapter initialization status.
    - The lifecycle state transitions and timestamps.

### 46.4.2 Malformed and incompatible input

The host MUST reject inputs that fail to decode or violate required
structural rules.
The test MUST verify that:

1. Each malformed input family produces a stable diagnostic code.
2. Missing required envelope fields produce `request.envelope.malformed`
   diagnostic.
3. Invalid operation names produce `request.operation.unknown` diagnostic.
4. Invalid pagination cursors produce `request.pagination.invalid`
   diagnostic.
5. Invalid configuration schemas produce `config.validation.failed`
   diagnostic.
6. Missing required configuration fields produce `config.validation.failed`
   diagnostic.
7. Configuration using a source class outside defaults, files, environment,
   command-line, remote, and runtime injection produces
   `config.validation.failed`.
8. Unresolvable secret references produce `config.secret.resolve.failed`
   diagnostic.
9. No state, journal, or outbox entries are created for the failed
   operations.
10. The diagnostic identifies the specific field or schema that failed.
11. The diagnostic, logs, traces, metrics, and evidence do not expose secret
    values or reference paths, keys, versions, or resolved-store metadata; the
    diagnostic may identify only the containing configuration field location
    and store type.

### 46.4.3 Stale and duplicate input

The host MUST detect and reject stale or duplicate inputs.
The test MUST verify that:

1. A request with an expired pagination cursor produces
   `request.pagination.invalid` diagnostic.
2. An equivalent request reusing a completed request's key within 24 hours
   returns the original result and original request ID without re-executing
   side effects or emitting an error diagnostic.
3. An equivalent request reusing an in-flight request's key is correlated to
   the in-flight operation.
4. A non-equivalent request reusing a retained key is rejected with
   `request.idempotent_duplicate`, identifying the original request ID.
5. Reuse after the 24-hour retention interval is processed as a new request.
6. No state, journal, or outbox entries are created for the rejected
   non-equivalent request.

### 46.4.4 Boundary and limit inputs

The host MUST enforce configured boundaries and limits.
The test MUST verify that:

1. A request with `limit: 1001` is rejected with
   `request.pagination.invalid` diagnostic.
2. A request exceeding the rate limit is rejected with
   `transport.rate_limit.exceeded` diagnostic.
3. A request exceeding the timeout is cancelled with
   `transport.timeout` diagnostic.
4. The rate limit window and maximum are configurable.
5. The timeout duration is configurable.
6. No state, journal, or outbox entries are created for the rejected
   requests.
7. The diagnostic identifies the boundary or limit that was exceeded.

### 46.4.5 Timeout, cancellation, and unavailable dependency

The host MUST handle timeouts, cancellations, and unavailable dependencies
gracefully without leaving unauthorized or partial state.
The test MUST verify that:

1. A request that times out is cancelled and resources are released.
2. A cancellation request interrupts an in-flight operation.
3. An unavailable dependency (e.g., storage, runtime) prevents
   initialization with `init.dependency.unavailable` diagnostic.
4. A missing dependency prevents initialization with
   `init.dependency.missing` diagnostic.
5. A readiness timeout produces `init.ready.timeout` diagnostic.
6. No state, journal, or outbox entries are created for the failed
   operations.
7. The diagnostic identifies the dependency or boundary that failed.
8. Retry behavior is correct for transient failures (e.g., secret
   resolution, remote configuration).
9. The host transitions to a safe state (e.g., drained, shut down) after
   repeated failures.
10. A Chapter 44 credential-custody failure returned through a host API retains
    its exact Chapter 44 diagnostic and is not translated into
    `config.secret.resolve.failed`.

### 46.4.6 Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.
The test MUST verify that:

1. All Phase 1 integration tests from Milestone 1 (Profile Vocabulary)
   still pass.
2. All Phase 3 integration tests from Milestone 1 (Agent Manifests)
   still pass.
3. All Phase 3 integration tests from Milestone 3 (Agent Registry)
   still pass.
4. All Phase 1 integration tests from Milestone 7 (Provider-Neutral
   Model Requests) still pass.
5. Any regression is recorded with:
   - The test ID and milestone.
   - The observed behavior.
   - The expected behavior.
   - The approval status (approved variability or defect).

> **Non-normative note.**
Cross-milestone fixtures ensure that Milestone 9 Phase 1 does not
introduce regressions in earlier milestone behavior.
The host API surface is additive; it MUST NOT alter the behavior of
earlier milestone contracts.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Transport types tested | Section 46.4 | MUST | Must test at least HTTP/REST. Other transports are permitted. |
| Configuration sources tested | Section 46.4 | MUST | Must test defaults, files, and environment variables; must also test each optional command-line, remote, or runtime-injection source that the implementation supports. |
| Secret store types tested | Section 46.4 | MUST | Must test environment variable secrets. Other stores are permitted. |
| Secret-reference non-exposure | Sections 46.4.1, 46.4.2, and 46.4.5 | MUST | Must verify values, paths, keys, versions, and resolved-store metadata are absent from every host output and wrapper. |
| Runtime adapters tested | Section 46.4 | MUST | Must test at least one Extism runtime. |
| Storage adapters tested | Section 46.4 | MUST | Must test at least one durable storage adapter. |
| Cross-milestone fixtures | Section 46.4.6 | MUST | Must include all fixtures listed in section 46.4.6. |
| Regression approval | Section 46.4.6 | Required | Must record and approve or reject any regression. |

## Rationale and evidence (non-normative)

Integration tests for Milestone 9 Phase 1 verify that the host API surface,
configuration, and packaging work correctly across their real dependency
boundaries.
These tests prove the phase works as an integrated behavior and preserve
reproducible evidence for later milestone and release gates.

The test suite exercises:
- Successful flows with complete evidence retention.
- Malformed and incompatible inputs with stable diagnostics.
- Stale and duplicate inputs with idempotency enforcement.
- Boundary and limit inputs with configured enforcement.
- Timeout, cancellation, and unavailable dependency handling.
- Cross-milestone fixture regression to ensure no behavioral changes.

Passing this test suite is a prerequisite for promoting this chapter to
`status: normative` and for advancing Milestone 9 to Phase 2.
