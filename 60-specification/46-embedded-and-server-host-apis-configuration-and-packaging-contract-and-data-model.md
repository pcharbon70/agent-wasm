---
title: "Embedded And Server Host APIs Configuration And Packaging Contract And Data Model"
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
  - contract
  - data-model
aliases:
  - "M9-P1-S1 Contract And Data Model"
---

# Embedded And Server Host APIs Configuration And Packaging Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-01-embedded-and-server-host-apis-configuration-and-packaging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the contract and data model for embedded and server host APIs,
configuration, and packaging.

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
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

## 46.1 Contract And Data Model

> **Normative definition.**
The following operations are the complete host API surface for Milestone 9.
They are independent of transport and identify the behavior contract that
server adapters, embedded hosts, and SDKs MUST implement.

### 46.1.1 Host Operations

> **Normative definition.**
Each host operation is a logical request--response or request--stream boundary.
Operations are identified by a stable, human-readable name and a canonical
envelope format.

| Operation | Direction | Purpose |
| --- | --- | --- |
| `artifact.register` | Host-owned | Register an artifact for use by agents. |
| `artifact.inspect` | Host query | Return artifact metadata and provenance without loading state. |
| `artifact.list` | Host query | Enumerate artifacts with optional filters and pagination. |
| `agent.create` | Host-owned | Create a new agent with a manifest and initial state. |
| `agent.inspect` | Host query | Return agent identity, status, and configuration. |
| `agent.list` | Host query | Enumerate agents with optional filters and pagination. |
| `agent.update` | Host-owned | Update agent configuration, manifest bindings, or state migrations. |
| `agent.delete` | Host-owned | Cancel and remove an agent. |
| `signal.submit` | Host-owned | Submit an input signal for processing. |
| `signal.list` | Host query | Enumerate signals with optional filters and pagination. |
| `instruction.submit` | Host-owned | Submit a plan or instruction for execution. |
| `instruction.list` | Host query | Enumerate pending or completed instructions. |
| `history.list` | Host query | Enumerate state revisions, journal entries, or directive records. |
| `cancel.request` | Host-owned | Request cancellation of an in-flight turn. |
| `hibernate.request` | Host-owned | Freeze an agent and release runtime resources. |
| `thaw.request` | Host-owned | Restore a hibernated agent to active state. |
| `topology.query` | Host query | Return pod, host, or agent placement information. |
| `topology.update` | Host-owned | Adjust placement or topology configuration. |
| `capabilities.list` | Host query | Enumerate available capabilities and feature flags. |
| `capabilities.discover` | Host query | Return dynamic capability discovery results. |
| `approval.request` | Host-owned | Submit a user-approval request. |
| `approval.list` | Host query | Enumerate pending or completed approval requests. |
| `event.list` | Host query | Enumerate host lifecycle events. |
| `diagnostic.get` | Host query | Retrieve bounded diagnostic records without exposing secrets. |

> **Normative definition.**
Each operation MUST include the following envelope fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `request_id` | string | Yes | Unique request identifier for idempotency and tracing. |
| `version` | string | Yes | Protocol version for compatibility negotiation. |
| `timestamp` | string | Yes | ISO 8601 timestamp of request creation. |
| `operation` | string | Yes | Operation name from the host operations table. |
| `payload` | object | Yes | Operation-specific request or response data. |
| `correlation_id` | string | No | Optional correlation identifier for multi-step workflows. |

> **Non-normative note.**
The envelope design separates transport from protocol semantics.
Server adapters (HTTP, gRPC, WebSocket) serialize the envelope without
altering its structure or semantics.

### 46.1.2 Pagination Envelope

> **Normative definition.**
List operations MUST support pagination with the following envelope:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | No | Maximum number of results. Default and maximum are implementation-defined. |
| `cursor` | string | No | Opaque cursor for continuation. First request omits cursor. |
| `items` | array | Yes | List of results. |
| `next_cursor` | string | No | Cursor for the next page. Absent if no more pages. |
| `total` | integer | No | Approximate total count. Absent if not computed. |

> **Non-normative note.**
Implementations MAY use offset-based or cursor-based pagination.
Cursor-based pagination is recommended for large datasets.

### 46.1.3 Idempotency

> **Normative definition.**
Idempotent operations MUST support an `Idempotency-Key` header or field
in the envelope.
Identical requests with the same idempotency key MUST produce the same
result without re-executing side effects.

The host MUST reject duplicate idempotency keys with a `request.idempotent_duplicate`
diagnostic after the original request completes, unless the original request
is still in-flight.

### 46.1.4 Error Envelope

> **Normative definition.**
Error responses MUST use the following envelope structure:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `error_code` | string | Yes | Stable diagnostic code family. |
| `message` | string | Yes | Human-readable error description. |
| `details` | object | No | Operation-specific error details. |
| `request_id` | string | Yes | Correlation to the original request. |
| `timestamp` | string | Yes | ISO 8601 timestamp of error occurrence. |

### 46.1.5 Embedded Lifecycle Interfaces

> **Normative definition.**
Embedded hosts MUST expose the following lifecycle operations:

| Operation | Description |
| --- | --- |
| `configure(config)` | Apply configuration from a configuration source. |
| `initialize()` | Load configuration, establish dependencies, and prepare for operation. |
| `ready()` | Return readiness status. Host is ready when all dependencies are available. |
| `drain()` | Begin graceful shutdown. Reject new requests, complete in-flight operations. |
| `shutdown()` | Release all resources and terminate. |
| `cancel()` | Cancel all in-flight operations immediately. |
| `health()` | Return health check status for monitoring. |

> **Non-normative note.**
The embedded lifecycle interface is independent of the server lifecycle.
Server hosts wrap the embedded lifecycle with transport-specific startup
and shutdown behavior.

### 46.1.6 Dependency Injection

> **Normative definition.**
Embedded hosts MUST accept dependency injection for the following components:

| Dependency | Type | Required | Description |
| --- | --- | --- | --- |
| `storage` | Storage adapter | Yes | Durable state and history storage. |
| `runtime` | Extism runtime adapter | Yes | Wasm execution environment. |
| `transport` | Transport adapter | No | Server transport implementation. |
| `telemetry` | Telemetry adapter | No | Metrics, tracing, and logging. |
| `secrets` | Secrets manager | No | Secure credential and secret storage. |

> **Non-normative note.**
Dependencies are injected at `initialize()` time.
The host MUST NOT modify dependencies after initialization without
explicit `configure()` calls.

### 46.1.7 Configuration Data Model

> **Normative definition.**
Configuration is a hierarchical set of key-value pairs with the following
structure:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `version` | integer | Yes | Configuration schema version. |
| `source` | string | Yes | Configuration source identifier. |
| `precedence` | integer | Yes | Precedence level. Higher values override lower values. |
| `values` | object | Yes | Configuration key-value pairs. |
| `secrets` | object | No | Secret references. Values are resolved at runtime. |
| `profiles` | array | No | Named configuration profiles for environment selection. |

> **Non-normative note.**
Configuration sources are merged in precedence order.
Later sources with the same key override earlier sources.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Host operations surface | Section 46.1.1 | Required | Must include all operations listed in the host operations table. |
| Envelope fields | Section 46.1.1 | Required | Must include all fields listed in the envelope table. |
| Pagination strategy | Section 46.1.2 | MAY | Must support cursor-based pagination. Offset-based is permitted. |
| Pagination default limit | Section 46.1.2 | Implementation-defined | Must document the default and maximum limit values. |
| Idempotency key storage duration | Section 46.1.3 | Implementation-defined | Must document the duration for which idempotency keys are retained. |
| Dependency injection scope | Section 46.1.6 | Required | Must accept all required dependencies. Optional dependencies are permitted. |
| Configuration source count | Section 46.1.7 | Implementation-defined | Must document the maximum number of configuration sources supported. |
| Configuration precedence range | Section 46.1.7 | Implementation-defined | Must document the precedence range and ordering. |

## Rationale and evidence (non-normative)

The contract and data model for Milestone 9 Phase 1 establishes the
foundational interface surface that packages the verified runtime from
Milestones 1-8.
This chapter defines operations, envelopes, and lifecycle interfaces
independent of transport, enabling server adapters, embedded hosts, and
SDKs to implement the same behavior contract.

Configuration and packaging boundaries ensure that the runtime is deployable
as a framework platform with stable host APIs, SDKs, and local tooling.
These interfaces are the foundation for Phase 2 (Guest SDK, CLI, Simulator),
Phase 3 (Telemetry, Tracing), Phase 4 (Compatibility, Upgrades), and
Phase 5 (Examples, Runbooks).
