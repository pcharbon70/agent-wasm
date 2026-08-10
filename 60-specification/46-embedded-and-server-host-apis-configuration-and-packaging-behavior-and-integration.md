---
title: "Embedded And Server Host APIs Configuration And Packaging Behavior And Integration"
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
  - behavior
  - integration
aliases:
  - "M9-P1-S2 Behavior And Integration"
---

# Embedded And Server Host APIs Configuration And Packaging Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-01-embedded-and-server-host-apis-configuration-and-packaging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the behavior and integration rules for embedded and server
host APIs, configuration, and packaging.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
integration tests in
Section [Phase 1 Integration Tests](46-embedded-and-server-host-apis-configuration-and-packaging-phase-1-integration-tests.md)
and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md).

## 46.2 Behavior And Integration

### 46.2.1 Server Adapters

> **Normative definition.**
Server adapters serialize host operations over a transport without
altering protocol semantics.
The same host operation catalog and envelope format are used regardless
of transport.

> **Non-normative note.**
Server adapters map host operations to transport-specific conventions:

| Transport | Mapping |
| --- | --- |
| HTTP/REST | Each operation is an endpoint path. Method is POST for mutations, GET for queries. Envelope is JSON body. |
| gRPC | Each operation is a service method. Envelope is protobuf message. |
| WebSocket | Each operation is a message type. Envelope is JSON frame. |
| ZeroMQ | Each operation is a message command. Envelope is JSON frame. |

The adapter layer is responsible for:
- Translating between transport wire format and the canonical envelope.
- Applying transport-specific headers or metadata.
- Handling transport-level errors (timeouts, connection failures).

### 46.2.2 Configuration Sources

> **Normative definition.**
Configuration is loaded from multiple sources in precedence order.
Sources are merged so that higher-precedence values override lower-precedence
values.

Configuration sources are:

| Source | Precedence | Description |
| --- | --- | --- |
| Default values | 0 | Built-in defaults. |
| Configuration file | 10 | File-based configuration (YAML, JSON, TOML). |
| Environment variables | 20 | Environment variable overrides. |
| Command-line arguments | 30 | Explicit command-line overrides. |
| Remote configuration | 40 | Dynamic configuration from a remote source. |
| Runtime injection | 50 | Configuration injected via dependency injection. |

> **Non-normative note.**
Configuration sources are applied in order of increasing precedence.
Later sources override earlier sources for the same key.
Environment variables use the naming convention `AGENT_WASM_<SECTION>_<KEY>`
with underscores for nesting.

### 46.2.3 Configuration Validation

> **Normative definition.**
Configuration MUST be validated before `initialize()` completes.
Validation checks:

1. Schema conformance: Configuration matches the expected schema version.
2. Required fields: All required fields are present.
3. Type conformance: Field values match expected types.
4. Reference integrity: References to artifacts, agents, and secrets exist.
5. Security constraints: Secrets are properly referenced, credentials are not embedded.

Invalid configuration MUST produce a `config.validation.failed` diagnostic
and prevent initialization.

### 46.2.4 Secret References

> **Non-normative note.**
Secrets are referenced by key or path, not embedded in configuration.
Secret values are resolved at runtime by the secrets manager dependency.

Secret reference format:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | Secret store type (e.g., `vault`, `aws-secrets-manager`, `env`). |
| `path` | string | Yes | Secret path or key in the secret store. |
| `version` | string | No | Secret version. Defaults to latest. |

> **Non-normative note.**
Configuration values that require secrets are marked with a
`__secret__` prefix or use a dedicated secrets section.
The host MUST NOT log or expose secret values in diagnostics.

### 46.2.5 Profile Selection

> **Non-normative note.**
Configuration profiles are named subsets of configuration values.
Profiles enable environment-specific configuration (development, staging,
production) without duplicating configuration.

Profile selection is controlled by:

1. Explicit profile name in configuration.
2. Environment variable `AGENT_WASM_PROFILE`.
3. Default profile (usually `default`).

Profiles are applied after base configuration is loaded.
Profile values override base configuration values.

### 46.2.6 Runtime and Storage Adapters

> **Non-normative note.**
Runtime adapters wrap the Extism runtime with host-specific behavior:

| Adapter | Description |
| --- | --- |
| `extism-wasmtime` | Extism with Wasmtime runtime. |
| `extism-wazero` | Extism with Wazero runtime. |
| `chicory` | Chicory runtime (experimental). |
| `javascript` | JavaScript runtime (experimental). |

Storage adapters wrap the durable state and history storage:

| Adapter | Description |
| --- | --- |
| `sqlite` | SQLite storage. |
| `postgres` | PostgreSQL storage. |
| `redis` | Redis storage (for caching). |
| `memory` | In-memory storage (for testing). |

> **Non-normative note.**
Adapters are selected via configuration.
The host MUST expose a `capabilities.discover` operation to enumerate
available adapters.

### 46.2.7 Safe Diagnostics

> **Non-normative note.**
Diagnostics are bounded to prevent exposure of secrets, implementation
internals, or sensitive user data.

Diagnostics include:

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

Diagnostics are retrievable via the `diagnostic.get` operation with
appropriate access controls.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Server transport types | Section 46.2.1 | MAY | Must implement HTTP/REST. Other transports are permitted. |
| Configuration source types | Section 46.2.2 | MAY | Must support file and environment variable sources. |
| Configuration file formats | Section 46.2.2 | MAY | Must support JSON. YAML and TOML are permitted. |
| Configuration default precedence | Section 46.2.2 | Implementation-defined | Must document the default precedence range. |
| Configuration validation strictness | Section 46.2.3 | MAY | Must validate schema and required fields. Other checks are permitted. |
| Secret store types | Section 46.2.4 | MAY | Must support environment variable secrets. Other stores are permitted. |
| Profile selection mechanism | Section 46.2.5 | Implementation-defined | Must support environment variable selection. Explicit name is permitted. |
| Runtime adapter types | Section 46.2.6 | MAY | Must support at least one Extism runtime. Other runtimes are permitted. |
| Storage adapter types | Section 46.2.6 | MAY | Must support at least one durable storage adapter. |
| Diagnostic redaction rules | Section 46.2.7 | Required | Must redact secrets and implementation internals. |

## Rationale and evidence (non-normative)

Behavior and integration rules for Milestone 9 Phase 1 ensure that the
host API surface is implementable across multiple transports and
configuration paradigms.
Server adapters enable the same host operations to be exposed over
HTTP, gRPC, WebSocket, or other transports without protocol changes.
Configuration sources provide flexible deployment options with
well-defined precedence and validation.

Secret management and diagnostic redaction ensure that the host API
does not become a source of credential exposure or information leakage.
These rules are foundational for Phase 3 (Telemetry, Tracing, Audit)
and Phase 5 (Runbooks, SLO Evidence).
