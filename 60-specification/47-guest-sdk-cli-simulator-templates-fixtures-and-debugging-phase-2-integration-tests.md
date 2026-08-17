---
title: "Guest SDK CLI Simulator Templates Fixtures And Debugging Phase 2 Integration Tests"
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
  - integration-tests
  - phase-2
aliases:
  - "M9-P2-S4 Phase 2 Integration Tests"
---

# Guest SDK CLI Simulator Templates Fixtures And Debugging Phase 2 Integration Tests

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It defines the integration tests that verify guest SDK, CLI, simulator,
templates, fixtures, and debugging across their real dependency boundaries.

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
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Behavior And Integration](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-behavior-and-integration.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Failure Evidence And Operational Notes](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-failure-evidence-and-operational-notes.md).

## 47.4 Phase 2 Integration Tests

This section defines the observable behavior that the Phase 2 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### 47.4.1 Successful flow

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
execute correctly and produce expected outputs with complete evidence.
The test MUST verify that:

1. SDK bindings translate between language-specific types and canonical
   protocol envelopes without altering semantics.
2. CLI commands execute successfully with proper argument parsing,
   configuration loading, host connection, and output formatting.
3. Simulator executes agent turns with deterministic clock, randomness,
   effects, crashes, and policy controls.
4. Templates initialize correctly with proper directory structure, manifest,
   source, fixture, and README.
5. Fixtures execute successfully with setup, input, execution, assertion,
   and teardown steps.
6. Debugging views expose operational data without exposing secrets or
   implementation internals.
7. Compatibility negotiation succeeds between SDK/CLI and host.
8. The test records and retains:
   - SDK binding test results and evidence.
   - CLI command execution logs and output.
   - Simulator deterministic control results.
   - Template initialization structure and executability.
   - Fixture execution evidence and assertions.
   - Debugging view data and redaction results.

### 47.4.2 Malformed and incompatible input

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
reject malformed and incompatible inputs with stable diagnostics.
The test MUST verify that:

1. SDK type conversion failures produce `sdk.binding.invalid` diagnostic.
2. SDK error mapping failures produce `sdk.error.mapping.failed` diagnostic.
3. CLI argument validation failures produce `cli.argument.invalid` diagnostic.
4. CLI configuration loading failures produce `cli.configuration.failed` diagnostic.
5. CLI host connection failures produce `cli.host.connection.failed` diagnostic.
6. Simulator clock control failures produce `simulator.clock.invalid` diagnostic.
7. Simulator randomness control failures produce `simulator.randomness.invalid` diagnostic.
8. Simulator crash injection failures produce `simulator.crash.injection.failed` diagnostic.
9. Template initialization failures produce `template.initialization.failed` diagnostic.
10. Template dependency failures produce `template.dependency.missing` diagnostic.
11. Fixture setup failures produce `fixture.setup.failed` diagnostic.
12. Fixture input validation failures produce `fixture.input.invalid` diagnostic.
13. Debugging view availability failures produce `debug.view.unavailable` diagnostic.
14. Debugging view access failures produce `debug.view.access.denied` diagnostic.
15. No state, journal, or outbox entries are created for the failed operations.
16. The diagnostic identifies the specific field, type, or boundary that failed.
17. The diagnostic does not expose secrets or implementation internals.

### 47.4.3 Stale and duplicate input

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
detect and reject stale or duplicate inputs.
The test MUST verify that:

1. SDK lifecycle operations with invalid stage produce `sdk.lifecycle.failed` diagnostic.
2. CLI commands with expired session tokens produce `cli.host.connection.failed` diagnostic.
3. Simulator controls with invalid values are rejected with stable diagnostic.
4. Template re-initialization with existing directory produces diagnostic and cleanup.
5. Fixture re-execution with same inputs produces same evidence (idempotent).
6. Debugging view requests with stale session tokens produce `debug.view.access.denied` diagnostic.
7. No state, journal, or outbox entries are created for the rejected operations.
8. The diagnostic identifies the stale or duplicate input.

### 47.4.4 Boundary and limit inputs

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
enforce configured boundaries and limits.
The test MUST verify that:

1. SDK operations exceeding resource limits produce stable diagnostic.
2. CLI commands exceeding output size limits produce stable diagnostic.
3. Simulator controls exceeding configured bounds are rejected.
4. Template dependencies exceeding version constraints produce diagnostic.
5. Fixture inputs exceeding schema limits produce diagnostic.
6. Debugging view data exceeding size limits are truncated with diagnostic.
7. No state, journal, or outbox entries are created for the rejected operations.
8. The diagnostic identifies the boundary or limit that was exceeded.

### 47.4.5 Timeout, cancellation, and unavailable dependency

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
handle timeouts, cancellations, and unavailable dependencies gracefully
without leaving unauthorized or partial state.
The test MUST verify that:

1. SDK operations that timeout are cancelled and resources are released.
2. CLI commands that timeout are cancelled with `cli.host.connection.failed` diagnostic.
3. Simulator execution that times out is cancelled with diagnostic.
4. Template initialization that times out is cancelled with diagnostic and cleanup.
5. Fixture execution that times out is cancelled with diagnostic and teardown.
6. Debugging view requests that timeout are cancelled with diagnostic.
7. Unavailable host produces `cli.host.connection.failed` diagnostic.
8. Unavailable simulator dependency produces `simulator.*.failed` diagnostic.
9. Unavailable template dependency produces `template.dependency.missing` diagnostic.
10. Retry behavior is correct for transient failures (e.g., CLI host connection).
11. The system transitions to a safe state (e.g., drained, shut down) after repeated failures.
12. No state, journal, or outbox entries are created for the failed operations.

### 47.4.6 Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.
The test MUST verify that:

1. All Phase 1 integration tests from Milestone 1 (Profile Vocabulary) still pass.
2. All Phase 5 integration tests from Milestone 1 (Guest SDK) still pass.
3. All Phase 3 integration tests from Milestone 3 (Agent Registry) still pass.
4. All Phase 1 integration tests from Milestone 7 (Provider-Neutral Model Requests) still pass.
5. All Phase 1 integration tests from Milestone 9 (Embedded And Server Host APIs) still pass.
6. Any regression is recorded with:
   - The test ID and milestone.
   - The observed behavior.
   - The expected behavior.
   - The approval status (approved variability or defect).

> **Non-normative note.**
Cross-milestone fixtures ensure that Milestone 9 Phase 2 does not
introduce regressions in earlier milestone behavior.
The SDK, CLI, simulator, templates, fixtures, and debugging views are
additive; they MUST NOT alter the behavior of earlier milestone contracts.

### 47.4.7 Deterministic reproducibility

The simulator and templates MUST produce deterministic, reproducible results.
The test MUST verify that:

1. Same simulator inputs with same deterministic controls produce same outputs.
2. Same template initialization produces same directory structure and files.
3. Same fixture inputs produce same evidence records.
4. Same debugging view requests produce same data (excluding timestamps).
5. Reproducibility is verified via:
   - Output hash comparison.
   - File content comparison.
   - Evidence record comparison.

### 47.4.8 Offline behavior

The SDK, CLI, simulator, templates, fixtures, and debugging views MUST
support offline operation for configured capabilities.
The test MUST verify that:

1. `artifact build` CLI command works offline with cached dependencies.
2. `fixture test` CLI command works offline with local fixtures.
3. `local run` CLI command works offline with simulator.
4. `replay` CLI command works offline with cached evidence.
5. Online-required commands (`artifact sign` with remote key) are rejected
   with stable diagnostic when offline.
6. Offline mode is activated correctly (unreachable host, network unavailable,
   explicit `--offline` flag).
7. Offline mode produces diagnostic indicating reduced functionality.

### 47.4.9 Compatibility negotiation

The SDK, CLI, and fixtures MUST negotiate compatibility with the host.
The test MUST verify that:

1. Compatible SDK/CLI versions proceed normally.
2. Deprecated SDK/CLI versions produce warnings and proceed for 6 months.
3. Sunset SDK/CLI versions produce errors and refuse execution for 3 months
   before removal.
4. An incompatible protocol version that is not merely in a deprecation stage
   produces a stable error and refuses execution.
5. Missing features produce errors and refuse execution.
6. Compatibility negotiation results are logged and included in diagnostics.

### 47.4.10 Reproducible builds

Artifact builds MUST be reproducible.
The test MUST verify that:

1. Same inputs produce same artifact bytes (deterministic).
2. Source provenance is recorded in manifest.
3. Dependencies are pinned by digest, not version.
4. Build hash matches expected value.
5. Dependency verification succeeds (all dependencies pinned and present).
6. Source inclusion audit succeeds (all sources included and accounted for).

### 47.4.11 Actionable failures

Failures MUST produce actionable diagnostics with hints and references.
The test MUST verify that:

1. Each failure diagnostic includes `hint` field with remediation steps.
2. Each failure diagnostic includes `reference` field with documentation link.
3. Hints are specific and actionable (e.g., "Set `AGENT_WASM_PROFILE=production`").
4. References link to relevant documentation, migration guides, or issue trackers.
5. Actionable failures enable developers to resolve issues without consulting support.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| SDK language tested | Section 47.4.1 | MUST | Must test at least one SDK language. |
| CLI commands tested | Section 47.4.1 | MUST | Must test all commands listed in Section 47.1.2. |
| Simulator controls tested | Section 47.4.1 | MUST | Must test all controls listed in Section 47.1.3. |
| Template patterns tested | Section 47.4.1 | MUST | Must test `direct` and `fsm` templates. |
| Fixture composition format tested | Section 47.4.1 | MUST | Must test YAML/JSON fixture composition. |
| Debugging views tested | Section 47.4.1 | MUST | Must test all views listed in Section 47.1.6. |
| Cross-milestone fixtures | Section 47.4.6 | MUST | Must include all fixtures listed in section 47.4.6. |
| Regression approval | Section 47.4.6 | Required | Must record and approve or reject any regression. |
| Deterministic reproducibility verification | Section 47.4.7 | MUST | Must verify determinism via output hash, file content, and evidence record comparison. |
| Offline capabilities tested | Section 47.4.8 | MUST | Must test all offline capabilities listed in section 47.1.9. |
| Compatibility negotiation tested | Section 47.4.9 | MUST | Must test compatible, deprecated, sunset, incompatible, and missing-feature scenarios. |
| Reproducible build verification | Section 47.4.10 | MUST | Must verify determinism, source inclusion, and dependency pinning. |
| Actionable failure fields | Section 47.4.11 | MUST | Must verify `hint` and `reference` fields are present and actionable. |

## Rationale and evidence (non-normative)

Integration tests for Milestone 9 Phase 2 verify that SDK, CLI, simulator,
template, fixture, and debugging view functionality works correctly across
their real dependency boundaries.
These tests prove the phase works as an integrated behavior and preserve
reproducible evidence for later milestone and release gates.

The test suite exercises:
- Successful flows with complete evidence retention.
- Malformed and incompatible inputs with stable diagnostics.
- Stale and duplicate inputs with proper rejection.
- Boundary and limit inputs with configured enforcement.
- Timeout, cancellation, and unavailable dependency handling.
- Cross-milestone fixture regression to ensure no behavioral changes.
- Deterministic reproducibility for simulator, templates, fixtures, and debugging views.
- Offline behavior for configured capabilities.
- Compatibility negotiation between SDK/CLI and host.
- Reproducible builds with determinism, source inclusion, and dependency pinning.
- Actionable failures with hints and references.

Passing this test suite is a prerequisite for promoting this chapter to
`status: normative` and for advancing Milestone 9 to Phase 3.
