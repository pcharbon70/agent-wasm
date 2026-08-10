---
title: "Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model"
kind: specification
created: "2026-08-10"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-02
  - guest-sdk
  - cli
  - simulator
  - templates
  - fixtures
  - debugging
  - contract
  - data-model
aliases:
  - "M9-P2-S1 Contract And Data Model"
---

# Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the contract and data model for guest SDK, CLI, simulator,
templates, fixtures, and debugging.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
integration tests in
Section [Phase 2 Integration Tests](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-phase-2-integration-tests.md)
and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md).

## 47.1 Contract And Data Model

> **Normative definition.**
The following surfaces make correct plugin and agent development possible
without requiring contributors to reconstruct protocol or runtime behavior.

### 47.1.1 Guest SDK Surfaces

> **Normative definition.**
The guest SDK provides language-specific bindings for the following protocol
surfaces:

| Surface | Description |
| --- | --- |
| `manifest` | Artifact manifest composition and validation. |
| `exports` | Plugin export definitions (describe, initialize, reduce, migrate). |
| `codecs` | Canonical JSON encoding/decoding, binary encoding support. |
| `signals` | Signal creation, validation, and causal tracking. |
| `actions` | Action definition, validation, and deterministic execution plans. |
| `state-operations` | State patch creation, application, and conflict resolution. |
| `directives` | Directive creation, validation, and attempt tracking. |
| `strategies` | Strategy selection, FSM state transitions, and planning outputs. |
| `diagnostics` | Diagnostic emission with bounded evidence. |
| `fixtures` | Integration test fixture composition and assertion. |

> **Non-normative note.**
SDK languages are implementation-defined.
The SDK MUST provide type-safe bindings for the protocol surfaces above.
Language-specific conventions (e.g., Rust traits, TypeScript interfaces,
Python protocols) are permitted but MUST expose the same semantic contract.

### 47.1.2 CLI Commands

> **Normative definition.**
The CLI provides the following commands for development, testing, and
evidence collection:

| Command | Description |
| --- | --- |
| `profile inspect` | Inspect bootstrap profile and conformance capabilities. |
| `artifact build` | Build artifact from manifest and source. |
| `artifact validate` | Validate artifact manifest and provenance. |
| `artifact sign` | Sign artifact with configured key. |
| `plugin compose` | Compose plugin from manifest and exports. |
| `fixture test` | Run integration test fixtures. |
| `local run` | Run agent locally with deterministic clocks and effects. |
| `replay` | Replay historical signals and state revisions. |
| `reduce` | Execute reducer exports with test inputs. |
| `evidence inspect` | Inspect milestone acceptance evidence. |

> **Non-normative note.**
CLI commands follow standard conventions:
- Flags for options (e.g., `--output`, `--verbose`).
- Subcommands for operations (e.g., `artifact build`, `artifact validate`).
- Exit codes for success (0) and failure (1-255).
- JSON or text output formats selectable via `--format`.

### 47.1.3 Local Simulator

> **Normative definition.**
The local simulator uses the same host contracts as production but with
deterministic controls:

| Control | Description |
| --- | --- |
| `clock` | Deterministic clock for time-based operations. |
| `randomness` | Seeded randomness for non-deterministic operations. |
| `effects` | Configurable effect handlers (pass-through, mock, fail). |
| `crashes` | Configurable crash injection at specific boundaries. |
| `policy` | Configurable policy decisions (approve, deny, attenuate). |

> **Non-normative note.**
The simulator is intended for local development and testing.
It MUST expose the same failure modes and diagnostic codes as production.
Deterministic controls enable reproducible tests without relying on
production infrastructure.

### 47.1.4 Fixture Composition

> **Normative definition.**
Fixtures compose test scenarios from the following components:

| Component | Description |
| --- | --- |
| `setup` | Pre-test configuration and state initialization. |
| `input` | Test inputs (signals, instructions, approvals). |
| `expected` | Expected outputs, state changes, and diagnostics. |
| `assertion` | Validation logic for outputs and evidence. |
| `teardown` | Post-test cleanup and evidence retention. |

> **Non-normative note.**
Fixtures are language-agnostic and may be composed via:
- YAML/JSON test definitions.
- SDK function calls.
- CLI command sequences.

Fixtures MUST produce structured evidence records for milestone acceptance.

### 47.1.5 Template Structure

> **Normative definition.**
Templates provide starter projects for common agent patterns:

| Pattern | Description |
| --- | --- |
| `direct` | Direct strategy with simple input/output. |
| `fsm` | FSM tool-loop with bounded iterations. |
| `tool-using` | Tool-using strategy with retrieval and code execution. |
| `multi-agent` | Multi-agent with fan-out/fan-in delegation. |
| `migration` | State migration with schema evolution. |
| `capability` | Capability-gated operations with policy enforcement. |
| `malformed-output` | Malformed output handling and recovery. |

> **Non-normative note.**
Templates include:
- Manifest with dependencies and exports.
- SDK bindings for the target language.
- Fixture for canonical flow and failure handling.
- README with setup, run, and test instructions.

### 47.1.6 Debugging Views

> **Normative definition.**
Debugging views expose the following operational data:

| View | Description |
| --- | --- |
| `canonical-io` | Canonical input and output bytes. |
| `route-action` | Route resolution and action selection. |
| `patch-application` | State patch application and merge results. |
| `directives` | Directive creation, dispatch, and attempt tracking. |
| `limits` | Resource limits and usage measurement. |
| `traps` | Trap detection and handler invocation. |
| `evidence` | Evidence references and milestone acceptance status. |

> **Non-normative note.**
Debugging views are accessible via:
- CLI commands (e.g., `agent inspect --debug`).
- SDK functions (e.g., `debug.view('directives')`).
- HTTP/gRPC endpoints (e.g., `/debug/directives`).

Views MUST NOT expose secrets, implementation internals, or sensitive
user data beyond what is permitted by the diagnostic redaction rules.

### 47.1.7 SDK/CLI Compatibility Negotiation

> **Normative definition.**
SDK and CLI MUST negotiate compatibility with the host via:

| Field | Description |
| --- | --- |
| `protocol_version` | Supported protocol version range. |
| `feature_flags` | Supported feature flags (e.g., `binary-encoding`, `streaming`). |
| `sdk_version` | SDK version for deprecation warnings. |

> **Non-normative note.**
Compatibility negotiation occurs at:
- SDK initialization.
- CLI connection to host.
- Fixture composition.

Incompatible versions MUST produce a stable diagnostic and prevent
execution until resolved.

### 47.1.8 Deprecation Policy

> **Non-normative note.**
Deprecation follows a published policy:

| Stage | Duration | Behavior |
| --- | --- | --- |
| `deprecated` | 6 months | Warning on use. Migration path documented. |
| `sunset` | 3 months | Error on use. Migration required. |
| `removed` | N/A | Surface no longer available. |

Deprecation notices include:
- Replacement surface or command.
- Migration guide and timeline.
- Contact for questions or exceptions.

### 47.1.9 Offline Behavior

> **Non-normative note.**
SDK and CLI MUST support offline operation for:

| Capability | Offline Behavior |
| --- | --- |
| `artifact build` | Build from cached dependencies. |
| `fixture test` | Run local fixtures without host. |
| `local run` | Run with simulator without host. |
| `replay` | Replay from cached evidence. |

Offline mode produces a diagnostic indicating reduced functionality.
Operations requiring host connectivity (e.g., `artifact sign` with remote
key, `fixture test` with host) are rejected with a stable diagnostic.

### 47.1.10 Reproducible Builds

> **Non-normative note.**
Artifact builds MUST be reproducible:

| Requirement | Description |
| --- | --- |
| `deterministic` | Same inputs produce same artifact bytes. |
| `source-included` | Source provenance recorded in manifest. |
| `dependency-pin` | Dependencies pinned by digest, not version. |

Reproducibility is verified via:
- Build hash comparison.
- Dependency digest verification.
- Source inclusion audit.

### 47.1.11 Actionable Failures

> **Normative definition.**
Failures MUST produce actionable diagnostics with:

| Field | Description |
| --- | --- |
| `code` | Stable diagnostic code. |
| `message` | Human-readable description. |
| `hint` | Suggested remediation steps. |
| `reference` | Documentation link for further guidance. |

> **Non-normative note.**
Actionable failures enable developers to resolve issues without
consulting support.
Hints include:
- Configuration changes.
- Dependency updates.
- Code modifications.
- Environment adjustments.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| SDK languages | Section 47.1.1 | MAY | Must support at least one language. Other languages are permitted. |
| CLI command set | Section 47.1.2 | Required | Must include all commands listed in the CLI commands table. |
| Simulator controls | Section 47.1.3 | Required | Must include all controls listed in the simulator table. |
| Fixture composition format | Section 47.1.4 | MAY | Must support YAML/JSON. SDK function calls and CLI sequences are permitted. |
| Template patterns | Section 47.1.5 | MAY | Must include `direct` and `fsm` templates. Other patterns are permitted. |
| Debugging view access methods | Section 47.1.6 | MAY | Must support CLI and SDK access. HTTP/gRPC endpoints are permitted. |
| Compatibility negotiation fields | Section 47.1.7 | Required | Must include all fields listed in the compatibility table. |
| Deprecation policy durations | Section 47.1.8 | Implementation-defined | Must document the duration for each deprecation stage. |
| Offline capabilities | Section 47.1.9 | MAY | Must support at least `artifact build` and `fixture test` offline. |
| Reproducible build verification | Section 47.1.10 | Required | Must verify determinism, source inclusion, and dependency pinning. |
| Actionable failure fields | Section 47.1.11 | Required | Must include all fields listed in the actionable failures table. |

## Rationale and evidence (non-normative)

The contract and data model for Milestone 9 Phase 2 makes correct plugin
and agent development possible without requiring contributors to reconstruct
protocol or runtime behavior.
The guest SDK provides language-specific bindings for the protocol surfaces.
The CLI provides development, testing, and evidence collection commands.
The local simulator enables deterministic testing with configurable controls.
Templates provide starter projects for common agent patterns.
Fixtures compose test scenarios with structured evidence retention.
Debugging views expose operational data for troubleshooting.

These surfaces are foundational for Phase 3 (Telemetry, Tracing, Audit),
Phase 4 (Compatibility, Upgrades), and Phase 5 (Examples, Runbooks).
They enable developers to build, test, and debug agents efficiently while
maintaining conformance with the protocol and runtime behavior.
