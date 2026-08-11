# Milestone 9 - Production Platform And Developer Experience

Package the runtime as an operable framework platform with stable host APIs, SDKs, local tooling, observability, upgrades, deployment guidance, and production acceptance evidence.

Current status: Phase 4 complete; all other phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for production platform and developer experience.

## Dependencies And Entry Gate

- Milestone 8 release gates pass for the supported runtime and architecture matrix.
- The stable contracts from Milestones 1–7 have explicit compatibility policies.

## Phase Order

1. [Phase 1 - Embedded And Server Host APIs Configuration And Packaging](phase-01-embedded-and-server-host-apis-configuration-and-packaging.md)
2. [Phase 2 - Guest SDK CLI Simulator Templates Fixtures And Debugging](phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md)
3. [Phase 3 - Telemetry Tracing Audit Redaction Health And Operator Actions](phase-03-telemetry-tracing-audit-redaction-health-and-operator-actions.md)
4. [Phase 4 - Compatibility Upgrades Migrations Deployment And Horizontal Coordination](phase-04-compatibility-upgrades-migrations-deployment-and-horizontal-coordination.md)
5. [Phase 5 - Examples Runbooks SLO Evidence And Production Acceptance](phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md)

## Planned Artifacts

- Embedded/server host API and configuration catalog
- Guest SDK, CLI, simulator, templates, and debugging plan
- Operations, upgrade, deployment, runbook, and SLO acceptance package

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- The platform exposes framework and operator surfaces, not a generic end-user web UI.
- Deployment starts single-node and adds replaceable horizontal coordination seams.
- Provider, storage, transport, and deployment technologies remain replaceable.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Embedded And Server Host APIs Configuration And Packaging](phase-01-embedded-and-server-host-apis-configuration-and-packaging.md) — implements and verifies this ordered phase.
- [Phase 2 - Guest SDK CLI Simulator Templates Fixtures And Debugging](phase-02-guest-sdk-cli-simulator-templates-fixtures-and-debugging.md) — implements and verifies this ordered phase.
- [Phase 3 - Telemetry Tracing Audit Redaction Health And Operator Actions](phase-03-telemetry-tracing-audit-redaction-health-and-operator-actions.md) — implements and verifies this ordered phase.
- [Phase 4 - Compatibility Upgrades Migrations Deployment And Horizontal Coordination](phase-04-compatibility-upgrades-migrations-deployment-and-horizontal-coordination.md) — implements and verifies this ordered phase.
- [Phase 5 - Examples Runbooks SLO Evidence And Production Acceptance](phase-05-examples-runbooks-slo-evidence-and-production-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
