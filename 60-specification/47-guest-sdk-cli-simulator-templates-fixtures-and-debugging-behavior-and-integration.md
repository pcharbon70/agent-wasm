---
title: "Guest SDK CLI Simulator Templates Fixtures And Debugging Behavior And Integration"
kind: specification
created: "2026-08-10"
status: normative
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
  - behavior
  - integration
aliases:
  - "M9-P2-S2 Behavior And Integration"
---

# Guest SDK CLI Simulator Templates Fixtures And Debugging Behavior And Integration

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the behavior and integration rules for guest SDK, CLI,
simulator, templates, fixtures, and debugging.

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
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md).

## 47.2 Behavior And Integration

### 47.2.1 SDK Binding Behavior

> **Non-normative note.**
SDK bindings translate between language-specific types and the canonical
protocol envelopes defined in [Embedded And Server Host APIs](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md).

Behavior includes:
- Type conversion (e.g., Rust `String` to envelope `string`).
- Error mapping (e.g., SDK errors to diagnostic codes).
- Lifecycle management (e.g., SDK initialization to host `initialize()`).

Bindings MUST preserve protocol semantics across language boundaries.
Language-specific idioms are permitted but MUST not alter behavior.

### 47.2.2 CLI Command Execution

> **Non-normative note.**
CLI commands execute the following steps:

1. Parse arguments and flags.
2. Load configuration (if applicable).
3. Establish host connection (if required).
4. Execute command logic.
5. Format and output results.
6. Release resources.

Command execution follows these rules:
- Commands are idempotent where possible (e.g., `artifact validate`).
- Commands produce structured output (JSON or text).
- Commands exit with stable exit codes (0 = success, 1-255 = failure).
- Commands log to stderr for diagnostics and stdout for results.

### 47.2.3 Simulator Execution

> **Non-normative note.**
The simulator executes agent turns with deterministic controls:

1. Apply clock control (advance time deterministically).
2. Apply randomness control (use seeded PRNG).
3. Apply effect control (route effects to handlers).
4. Apply crash control (inject crashes at boundaries).
5. Apply policy control (evaluate policy decisions).
6. Execute turn (invoke reducer exports).
7. Capture evidence (state, journal, outbox, diagnostics).

Deterministic controls enable reproducible tests:
- Same inputs produce same outputs.
- Same crash injection produces same failure mode.
- Same policy decision produces same outcome.

### 47.2.4 Fixture Execution

> **Non-normative note.**
Fixtures execute the following lifecycle:

1. Setup: Initialize configuration, state, and fixtures.
2. Input: Submit test inputs (signals, instructions, approvals).
3. Execute: Run agent turns with configured controls.
4. Assert: Validate outputs, state changes, and diagnostics.
5. Teardown: Clean up state and retain evidence.

Fixture execution rules:
- Fixtures are isolated (no shared state between fixtures).
- Fixtures produce structured evidence records.
- Fixtures fail on assertion failure with diagnostic code.
- Fixtures pass on successful assertion with evidence reference.

### 47.2.5 Template Initialization

#### Template directory structure (non-normative)

> **Non-normative note.**
Templates initialize with the following structure:

```
template-name/
├── manifest.yaml
├── src/
│   └── main.{lang}
├── fixtures/
│   └── canonical-flow.test.{lang}
├── .gitignore
└── README.md
```

Template initialization steps:
1. Create directory structure.
2. Populate manifest with dependencies and exports.
3. Populate source file with SDK bindings and exports.
4. Populate fixture with canonical flow and failure handling.
5. Generate README with setup, run, and test instructions.

Templates MUST be executable after initialization without modification.

### 47.2.6 Debugging View Behavior

> **Non-normative note.**
Debugging views expose operational data with the following behavior:

| View | Data Exposed | Redaction Rules |
| --- | --- | --- |
| `canonical-io` | Input and output bytes | Secrets, credentials, sensitive user data. |
| `route-action` | Route and action identifiers | Implementation internals, private identifiers. |
| `patch-application` | State patches and merge results | Sensitive state fields (e.g., credentials). |
| `directives` | Directive records and attempts | Secret references, implementation details. |
| `limits` | Resource limits and usage | Implementation-specific limit values. |
| `traps` | Trap detection and handler invocation | Implementation internals. |
| `evidence` | Evidence references and status | Sensitive evidence content (if any). |

Views are accessible via CLI, SDK, or HTTP/gRPC endpoints.
Access is controlled by the host's capability model.

### 47.2.7 Compatibility Negotiation Behavior

> **Non-normative note.**
Compatibility negotiation occurs at the following points:

1. SDK initialization: SDK reports version and feature flags to host.
2. CLI connection: CLI reports version and feature flags to host.
3. Fixture composition: Fixture reports required features to host.

Negotiation behavior:
- Compatible versions proceed normally.
- Deprecated versions produce warnings and proceed.
- Incompatible versions produce errors and refuse execution.
- Missing features produce errors and refuse execution.

Negotiation results are logged and included in diagnostics.

### 47.2.8 Deprecation Behavior

> **Non-normative note.**
Deprecation follows the published policy:

| Stage | Behavior |
| --- | --- |
| `deprecated` | Warning on use. Migration path documented in diagnostic. |
| `sunset` | Error on use. Execution prevented until migration. |
| `removed` | Surface no longer available. Error on access. |

Deprecation warnings include:
- Replacement surface or command.
- Migration guide link.
- Sunset date (if applicable).

### 47.2.9 Offline Behavior

> **Non-normative note.**
Offline mode is activated when:
- Host is unreachable.
- Network connectivity is unavailable.
- Explicit `--offline` flag is set.

Offline behavior:
- `artifact build`: Build from cached dependencies. Diagnostic if dependencies not cached.
- `fixture test`: Run local fixtures without host. Diagnostic if host-required fixtures.
- `local run`: Run with simulator without host. Full functionality.
- `replay`: Replay from cached evidence. Diagnostic if evidence not cached.

Online-required commands (`artifact sign` with remote key, `fixture test` with host) are rejected with stable diagnostic.

### 47.2.10 Reproducible Build Behavior

> **Non-normative note.**
Reproducible builds follow these steps:

1. Pin dependencies by digest (not version).
2. Record source provenance in manifest.
3. Build artifact deterministically.
4. Compute build hash.
5. Verify hash matches expected value (if provided).

Build verification:
- Hash comparison: Compare build hash to expected hash.
- Dependency verification: Verify all dependencies are pinned and present.
- Source inclusion audit: Verify all sources are included and accounted for.

Reproducibility failures produce diagnostic with details.

### 47.2.11 Actionable Failure Behavior

> **Non-normative note.**
Actionable failures follow these steps:

1. Detect failure (SDK error, CLI error, simulator error, fixture error).
2. Classify failure (malformed, incompatible, unauthorized, etc.).
3. Generate diagnostic with code, message, hint, and reference.
4. Log diagnostic to stderr.
5. Return diagnostic to caller (exit code, error object, etc.).

Hints include:
- Configuration changes (e.g., "Set `AGENT_WASM_PROFILE=production`").
- Dependency updates (e.g., "Update `agent-sdk` to version 2.0.0").
- Code modifications (e.g., "Handle `tool.execution.timeout` diagnostic").
- Environment adjustments (e.g., "Ensure host is running on port 8080").

References link to:
- Documentation pages.
- Migration guides.
- Issue trackers.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| SDK binding behavior | Section 47.2.1 | Required | Must preserve protocol semantics across language boundaries. |
| CLI command execution steps | Section 47.2.2 | Required | Must include all steps listed in the CLI command execution list. |
| Simulator deterministic controls | Section 47.2.3 | Required | Must include all controls listed in the simulator controls list. |
| Fixture isolation | Section 47.2.4 | Required | Fixtures must be isolated (no shared state between fixtures). |
| Template directory structure | Section 47.2.5 | Required | Must include all files and directories listed in the template structure. |
| Debugging view redaction | Section 47.2.6 | Required | Must redact all data listed in the redaction rules table. |
| Compatibility negotiation points | Section 47.2.7 | Required | Must negotiate at all points listed in the negotiation points list. |
| Deprecation stage behavior | Section 47.2.8 | Required | Must include all behaviors listed in the deprecation stage behavior table. |
| Offline mode activation triggers | [Offline Behavior](#4729-offline-behavior) | Required | Activate when the host is unreachable, the network is unavailable, or `--offline` is set. |
| Reproducible build verification steps | Section 47.2.10 | Required | Must include all verification steps listed in the build verification list. |
| Actionable failure classification | Section 47.2.11 | Required | Must classify failures into stable diagnostic families. |

## Rationale and evidence (non-normative)

Behavior and integration rules for Milestone 9 Phase 2 ensure that SDK
bindings, CLI commands, simulators, templates, fixtures, and debugging
views work correctly and integrate with the host runtime.

SDK bindings translate between language-specific types and protocol
envelopes while preserving semantics.
CLI commands execute with stable behavior, structured output, and proper
error handling.
Simulators enable deterministic testing with configurable controls for
clock, randomness, effects, crashes, and policy.
Fixtures compose test scenarios with isolation and structured evidence
retention.
Templates provide executable starter projects for common agent patterns.
Debugging views expose operational data with proper redaction and access
controls.

Compatibility negotiation, deprecation, offline behavior, reproducible
builds, and actionable failures ensure that developers can work efficiently
while maintaining conformance and receiving clear guidance when issues arise.
