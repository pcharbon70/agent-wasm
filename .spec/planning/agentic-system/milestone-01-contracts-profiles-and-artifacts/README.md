# Milestone 1 - Contracts, Profiles, And Artifacts

Establish the language-neutral vocabulary, compatibility rules, artifact model, and byte-level host–guest protocol on which every later runtime feature depends.

Specification-plan status: phases 1-5 complete. Runtime implementation and
conformance are tracked separately in the
[package-local SpecLed workspace](../../../../src/.spec/README.md).

## Purpose

Provide the ordered, section-sized specification work and evidence requirements
needed to define this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for contracts, profiles, and artifacts.

## Dependencies And Entry Gate

- The Jido, Extism, WebAssembly, and assurance research notes are the design baseline.
- No runtime code or persistence implementation is required to begin.

## Phase Order

1. [Phase 1 - Profile Vocabulary And Architectural Boundaries](phase-01-profile-vocabulary-and-architectural-boundaries.md)
2. [Phase 2 - Stable Identities Versions Errors And Limits](phase-02-stable-identities-versions-errors-and-limits.md)
3. [Phase 3 - Agent Manifests Artifacts Schemas And Registries](phase-03-agent-manifests-artifacts-schemas-and-registries.md)
4. [Phase 4 - Turn Lifecycle Protocols And Canonical Encoding](phase-04-turn-lifecycle-protocols-and-canonical-encoding.md)
5. [Phase 5 - Guest SDK Contracts Fixtures And Milestone Acceptance](phase-05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)

## Planned Artifacts

- Agent runtime profile and compatibility policy
- Artifact, manifest, schema, and identity contract catalog
- Turn protocol and canonical JSON fixture catalog

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until its specification artifact and
  traceability record exist.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-scenario section.
- Author and commit one section at a time.

## Shared Assumptions And Defaults

- Extism bytes-in/bytes-out is the bootstrap ABI.
- Canonical JSON is the first inspectable encoding.
- Authoritative agent state and policy remain host-owned.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

This is a runtime and conformance gate; the specification-plan status above
does not claim that it has passed.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Profile Vocabulary And Architectural Boundaries](phase-01-profile-vocabulary-and-architectural-boundaries.md) — defines and traces this ordered phase.
- [Phase 2 - Stable Identities Versions Errors And Limits](phase-02-stable-identities-versions-errors-and-limits.md) — defines and traces this ordered phase.
- [Phase 3 - Agent Manifests Artifacts Schemas And Registries](phase-03-agent-manifests-artifacts-schemas-and-registries.md) — defines and traces this ordered phase.
- [Phase 4 - Turn Lifecycle Protocols And Canonical Encoding](phase-04-turn-lifecycle-protocols-and-canonical-encoding.md) — defines and traces this ordered phase.
- [Phase 5 - Guest SDK Contracts Fixtures And Milestone Acceptance](phase-05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md) — defines and traces this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
