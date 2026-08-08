# Milestone 5 - Capabilities, Plugins, Security, And Tenancy

Add host-owned authorization, composable framework plugins, artifact trust, resource governance, and defensible tenant isolation around untrusted guest code.

Current status: planned; all phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for capabilities, plugins, security, and tenancy.

## Dependencies And Entry Gate

- Milestone 4 supplies durable attempts, audit facts, and recovery semantics.
- The host can identify artifact, tenant, principal, agent, purpose, and invocation.

## Phase Order

1. [Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
2. [Phase 2 - Capability Policy Attenuation Limits And Enforcement](phase-02-capability-policy-attenuation-limits-and-enforcement.md)
3. [Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
4. [Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
5. [Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)

## Planned Artifacts

- Threat, principal, grant, and capability vocabulary
- Framework plugin composition and trust contracts
- Artifact provenance, audit, isolation, and adversarial acceptance corpus

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- Authorization is always re-enforced by the host.
- Framework plugins are capability bundles, not merely Extism modules.
- No network, filesystem, environment, clock, model, or secret authority is ambient.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md) — implements and verifies this ordered phase.
- [Phase 2 - Capability Policy Attenuation Limits And Enforcement](phase-02-capability-policy-attenuation-limits-and-enforcement.md) — implements and verifies this ordered phase.
- [Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md) — implements and verifies this ordered phase.
- [Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md) — implements and verifies this ordered phase.
- [Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](phase-05-provenance-signing-audit-security-and-milestone-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
