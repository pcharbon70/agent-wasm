---
title: "Guest SDK CLI Simulator Templates Fixtures And Debugging Failure Evidence And Operational Notes"
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
  - failure-evidence
  - operational-notes
aliases:
  - "M9-P2-S3 Failure Evidence And Operational Notes"
---

# Guest SDK CLI Simulator Templates Fixtures And Debugging Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the failure evidence and operational notes for guest SDK,
CLI, simulator, templates, fixtures, and debugging.

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
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Behavior And Integration](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-behavior-and-integration.md).

## 47.3 Failure Evidence And Operational Notes

### 47.3.1 Failure Outcomes

> **Normative definition.**
The following failure outcomes are relevant to guest SDK, CLI, simulator,
templates, fixtures, and debugging.
Each outcome includes a stable diagnostic code family, cause, and behavior.

#### SDK failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `sdk.initialization.failed` | SDK initialization fails (missing dependency, incompatible version). | Reject initialization. Emit diagnostic with dependency name and version. |
| `sdk.binding.invalid` | SDK binding type conversion fails (unsupported type, invalid value). | Reject operation. Emit diagnostic with type and value. |
| `sdk.error.mapping.failed` | SDK error cannot be mapped to diagnostic code. | Map to `sdk.error.unknown`. Emit diagnostic with original error. |
| `sdk.lifecycle.failed` | SDK lifecycle operation fails (e.g., `shutdown()` fails). | Continue with degraded behavior. Emit diagnostic with lifecycle stage. |

#### CLI failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `cli.argument.invalid` | CLI argument is invalid (missing required, invalid value, conflicting). | Reject command. Emit diagnostic with argument name and validation error. |
| `cli.configuration.failed` | CLI configuration loading fails (missing file, invalid schema). | Reject command. Emit diagnostic with configuration source and error. |
| `cli.host.connection.failed` | CLI cannot connect to host (unreachable, authentication failure). | Reject command. Emit diagnostic with host address and error. Retry if transient. |
| `cli.output.format.invalid` | CLI output format is unsupported (e.g., invalid `--format` value). | Reject command. Emit diagnostic with format and supported formats. |
| `cli.offline.mode.rejected` | Command requires host but offline mode is active. | Reject command. Emit diagnostic with command name and required capability. |

#### Simulator failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `simulator.clock.invalid` | Clock control is invalid (e.g., negative time advance). | Reject control. Emit diagnostic with control name and value. |
| `simulator.randomness.invalid` | Randomness control is invalid (e.g., non-seeded PRNG). | Reject control. Emit diagnostic with control name and validation error. |
| `simulator.crash.injection.failed` | Crash injection fails (e.g., invalid boundary). | Skip injection. Emit diagnostic with boundary and error. Continue execution. |
| `simulator.policy.evaluation.failed` | Policy evaluation fails (e.g., policy not loaded, invalid decision). | Use default policy (deny). Emit diagnostic with policy name and error. |

#### Template failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `template.initialization.failed` | Template initialization fails (e.g., directory creation fails, file write fails). | Reject initialization. Emit diagnostic with template name and error. Clean up partial state. |
| `template.dependency.missing` | Template dependency is missing (e.g., SDK not installed, manifest invalid). | Reject initialization. Emit diagnostic with dependency name and resolution steps. |
| `template.executable.failed` | Template is not executable after initialization (e.g., source syntax error, fixture fails). | Reject template. Emit diagnostic with template name and validation error. |

#### Fixture failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `fixture.setup.failed` | Fixture setup fails (e.g., configuration invalid, state initialization fails). | Skip fixture. Emit diagnostic with fixture name and setup step. |
| `fixture.input.invalid` | Fixture input is invalid (e.g., signal schema mismatch, instruction format error). | Skip fixture. Emit diagnostic with fixture name and input validation error. |
| `fixture.assertion.failed` | Fixture assertion fails (e.g., expected output mismatch, state change not applied). | Fail fixture. Emit diagnostic with fixture name, assertion, expected, and actual. |
| `fixture.teardown.failed` | Fixture teardown fails (e.g., cleanup fails, evidence retention fails). | Continue execution. Emit diagnostic with fixture name and teardown step. |

#### Debugging view failures

| Diagnostic | Cause | Behavior |
| --- | --- | --- |
| `debug.view.unavailable` | Debugging view is unavailable (e.g., not enabled, feature not supported). | Reject access. Emit diagnostic with view name and availability status. |
| `debug.view.access.denied` | Debugging view access is denied (e.g., insufficient capability). | Reject access. Emit diagnostic with view name and required capability. |
| `debug.view.data.redaction.failed` | Debugging view data redaction fails (e.g., secret not redacted, internal data exposed). | Reject view. Emit diagnostic with view name and redaction rule. |

### 47.3.2 Bounded Diagnostics and Evidence

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
| `hint` | Suggested remediation steps | SDK/CLI/simulator |
| `reference` | Documentation link for further guidance | SDK/CLI/simulator |

> **Non-normative note.**
Diagnostics MUST NOT include:
- Raw credential values or secret references.
- Internal stack traces or implementation details.
- User data that is not relevant to the failure.
- Sensitive configuration values (e.g., database connection strings with passwords).

Evidence is retained for operational debugging and compliance auditing.
Evidence is retrievable via the `evidence inspect` CLI command or SDK
function with appropriate access controls.

### 47.3.3 Implementation-Defined Choices

> **Non-normative note.**
The following choices are implementation-defined and must be documented
in the conformance profile.

| Choice | Description | Default |
| --- | --- | --- |
| SDK language support | SDK languages to support. | At least one language. |
| CLI command set | CLI commands to include. | All commands listed in Section 47.1.2. |
| Simulator controls | Simulator controls to support. | All controls listed in Section 47.1.3. |
| Fixture composition format | Fixture composition formats to support. | YAML/JSON. |
| Template patterns | Template patterns to include. | `direct` and `fsm`. |
| Debugging view access methods | Debugging view access methods to support. | CLI and SDK. |
| Compatibility negotiation fields | Compatibility negotiation fields to include. | All fields listed in Section 47.1.7. |
| Deprecation policy durations | Deprecation policy stage durations. | `deprecated`: 6 months, `sunset`: 3 months. |
| Offline capabilities | Offline capabilities to support. | `artifact build`, `fixture test`, `local run`, `replay`. |
| Actionable failure hint generation | How hints are generated (manual, automated). | Manual. |

### 47.3.4 Deferred Work

| Item | Target | Reason |
| --- | --- | --- |
| Multi-language SDK support | Milestone 9 Phase 2 | Requires language-specific SDK development and testing |
| Remote debugger integration | Milestone 9 Phase 3 | Requires telemetry and tracing infrastructure |
| CI/CD pipeline templates | Milestone 9 Phase 4 | Requires compatibility and upgrade infrastructure |
| Documentation site generation | Milestone 9 Phase 5 | Requires developer experience and tooling |

> **Non-normative note.**
All items deferred to Milestone 9 later phases fall under
Milestone 9 - Production Platform And Developer Experience
(planning document at `.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md`).
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### 47.3.5 Results That Would Invalidate an Earlier Milestone Assumption

> **Non-normative note.**
The following results from Phase 2 would invalidate an earlier milestone
assumption:

1. **SDK bindings alter protocol semantics**: If SDK bindings alter the
   protocol envelopes or behavior defined in earlier milestones, this
   would invalidate the assumption defined in
   [Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
   that SDKs preserve protocol semantics across language boundaries.

2. **CLI commands bypass host validation**: If CLI commands bypass host
   validation or execute without host connection when required, this
   would invalidate the assumption defined in
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   that all host inputs are validated against the bootstrap profile.

3. **Simulator produces non-deterministic results**: If simulator controls
   do not produce deterministic results (e.g., clock advances non-deterministically,
   randomness is not seeded), this would invalidate the assumption that
   tests are reproducible and evidence is reliable.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Failure outcome diagnostics | Section 47.3.1 | Required | Must include all diagnostics listed in the failure outcomes tables. |
| Diagnostic field set | Section 47.3.2 | Required | Must include all fields listed in the bounded diagnostics table. |
| Diagnostic redaction | Section 47.3.2 | Required | Must redact secrets, stack traces, and irrelevant user data. |
| Actionable failure fields | Section 47.3.2 | Required | Must include `hint` and `reference` fields. |
| Implementation-defined choices documentation | Section 47.3.3 | Required | Must document all implementation-defined choices in the conformance profile. |
| Deferred work enforcement | Section 47.3.4 | MUST | Must NOT implement deferred work without evidence from the corresponding future phase. |

## Rationale and evidence (non-normative)

Failure evidence and operational notes for Milestone 9 Phase 2 ensure
that SDK, CLI, simulator, template, fixture, and debugging view failures
are observable, debuggable, and secure.
Stable diagnostic codes enable tooling to detect and handle failures
without parsing human-readable messages.
Bounded diagnostics prevent information leakage while retaining sufficient
context for operational debugging.
Actionable failures include hints and references to enable developers
to resolve issues without consulting support.

Implementation-defined choices are documented to enable conformance
verification and interoperability.
Deferred work is explicitly identified to prevent scope creep and ensure
that future phases build on the verified foundation of Phase 2.

Invalidating assumption conditions ensure that Phase 2 does not introduce
behavioral changes that contradict earlier milestone contracts.
