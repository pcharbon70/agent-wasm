---
title: "Phase 3 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-03
  - implementation
  - contract-and-data-model
  - framework-plugin
  - manifest
  - composition
  - lifecycle-hooks
  - trust-tiers
aliases:
  - "M5-P3-3.1 Implementation"
---

# Phase 3 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 3.1 (Contract And Data Model) from
[Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[32-framework-plugin-manifests-composition-and-lifecycle-hooks.md](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
which defines the declarative manifest contract, deterministic composition
ordering, and trust-tier separation between framework plugins and individual
Extism guest modules.

## Subtask 3.1.1.1: Specify plugin identity and manifest fields

### Implementation

Defined the `FrameworkPluginManifest` structure with the following top-level fields:

| Field | Type | Description |
|-------|------|-------------|
| `manifest_version` | `ManifestVersion` | Stable string (currently "1.0") |
| `id` | `PluginId` | Lower-kebab-case unique identifier |
| `publisher` | `PublisherId` | Trusted entity responsible for contents |
| `name` | string | Human-readable name |
| `description` | string? | Optional description |
| `version` | `SemanticVersion` | Plugin semantic version |
| `homepage` | string? | Optional homepage URL |
| `license` | string? | Optional license |
| `artifacts` | `ArtifactReference[]` | Declared artifacts with digests and trust tiers |
| `actions` | `ActionDeclaration[]` | Actions exposed to agents |
| `routes` | `RouteDeclaration[]` | Signal/action-to-handler route mappings |
| `state_namespaces` | string[] | Declared state namespaces |
| `schemas` | `SchemaDeclaration[]` | Input/output/state schemas |
| `strategies` | `StrategyDeclaration[]` | Strategy declarations |
| `directives` | `DirectiveDeclaration[]` | Directive declarations |
| `schedules` | `ScheduleDeclaration[]` | Schedule declarations |
| `requested_grants` | `Capability[]` | Capabilities the plugin needs |
| `lifecycle_ownership` | `LifecycleOwnership?` | Who owns lifecycle management |

Identity and versioning constraints:
- `manifest_version` is compared as exact string match (not numeric range)
- `id` is stable, lower-kebab-case, unique within plugin registry
- `publisher` is validated against trust model in [30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- `version` parses as Semantic Version per [CONFORMANCE-VOCABULARY.md](../../CONFORMANCE-VOCABULARY.md)

### Design decisions

1. **Manifest version is independent of plugin version**: A new manifest
   version is a backward-incompatible rewrite of the contract, requiring
   a major bump in the plugin's semantic version. This prevents
   ambiguous versioning where a manifest format change could be mistaken
   for a plugin feature change.

2. **Plugin ID is lower-kebab-case**: This provides a stable, URL-safe
   identifier that is consistent with web conventions and easy to use
   in configuration files.

3. **Lifecycle ownership is optional with host default**: When absent,
   the host owns lifecycle by default. This supports operators who
   require operational flexibility for third-party plugins.

## Subtask 3.1.1.2: Define composition order and conflict checks

### Implementation

Defined deterministic composition ordering with three tie-breaking rules:

1. **Stable identifier**: Plugins ordered by `PluginId` lexicographically
2. **Semantic version**: Ties broken by descending version (newest first)
3. **Manifest digest**: Final ties broken by content-addressable manifest digest

Seven conflict checks performed after composition:

| Check | Diagnostic | Description |
|-------|-----------|-------------|
| Name conflict | `plugin.name_conflict` | Two plugins share resolved name |
| Route conflict | `plugin.route_conflict` | Two routes match same pattern at same priority |
| State namespace conflict | `plugin.namespace_conflict` | Two plugins declare same namespace |
| Schema conflict | `plugin.schema_conflict` | Conflicting schemas with same id |
| Migration conflict | `plugin.migration_conflict` | Incompatible migrations on same namespace |
| Capability conflict | `plugin.capability_conflict` | Trust model cannot satisfy all grants |
| Lifecycle conflict | `plugin.lifecycle_conflict` | Publisher-owned claims conflict with operator policy |

When any conflict check fails, the host MUST fail the entire composition
and MUST NOT partially apply any plugin.

### Design decisions

1. **Composition is atomic**: Failure of any conflict check aborts the
   entire composition. This preserves a clean registry state and
   simplifies rollback. Partial application would create inconsistent
   state that is difficult to recover from.

2. **Deterministic ordering prevents ambiguous diagnostics**: The three
   tie-breaking rules ensure that conflict diagnostics always point to
   the same pair of plugins, regardless of when or how composition is
   triggered. This makes debugging more reliable.

3. **Lifecycle ownership conflicts require operator approval**: Two
   plugins claiming `lifecycle_ownership: "publisher"` for the same
   capability without explicit operator approval cause a conflict.
   This prevents publishers from silently taking control of shared
   capabilities.

## Subtask 3.1.1.3: Separate declarative metadata, untrusted guest artifacts, and privileged host-native integrations

### Implementation

Defined three trust tiers for plugin artifacts:

| Trust Tier | Description | Execution Requirement |
|-----------|-------------|----------------------|
| `untrusted-guest` | Raw guest module bytes (e.g., WASM) | Sandboxed within Extism invocation boundary |
| `reviewed-preparation` | Logic that prepares plugin state or migrates data | Must be reviewed by operator-level entity before execution |
| `privileged-host` | Native host integrations requiring elevated privileges | Restricted to approved operations; cannot modify manifest |

Trust tier enforcement:
- `untrusted-guest`: Host treats all content as untrusted until validated
- `reviewed-preparation`: Review evidence must be recorded before execution
- `privileged-host`: Digest must match approved manifest; cannot modify manifest or elevate trust tier

Declarative metadata (manifest itself) is inspected, validated, and composed
without execution. Untrusted guest artifacts are loaded through Extism
invocation boundary. Privileged host integrations are restricted to approved
operations and logged.

### Design decisions

1. **Trust tiers are enforced at load time**: The host refuses to load
   `privileged-host` artifacts whose digest does not match a previously
   approved manifest version. This prevents supply-chain attacks that
   replace approved artifacts with modified versions.

2. **Declarative metadata is never executed**: The manifest itself is
   metadata only. This prevents manifest injection attacks where a
   malicious manifest could execute arbitrary code.

3. **Review evidence is required for preparation logic**: Before
   `reviewed-preparation` artifacts execute, the host requires recorded
   review evidence. This is the primary defense against supply-chain
   attacks on plugin state migrations.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks Contract And Data Model](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Agent manifests: [Agent Manifests Artifacts Schemas And Registries](../../60-specification/03-agent-manifests-artifacts-schemas-and-registries.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Directives: [Directives Strategies Continuations And Terminal States](../../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
- Schedules: [Sensors Schedules Timers And External Signal Ingress](../../60-specification/23-sensors-schedules-timers-and-external-signal-ingress.md)
- Migration: [Retry Timer Recovery Replay Hibernate And Migration](../../60-specification/28-retry-timer-recovery-replay-hibernate-and-migration.md)
- Storage: [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)

## Open questions

1. Should plugins support explicit dependency declarations? The current
   design relies on composition-order conflict checks rather than
   explicit dependency graphs. Could circular dependencies arise that
   are not detected by the current conflict checks?

2. How should schema conflicts be resolved? The spec requires failing
   composition when schemas conflict, but does not address whether
   schemas could be merged or aliased in some cases.

3. Can lifecycle ownership be transferred? The spec defines host,
   publisher, and shared ownership but does not address whether
   ownership can be transferred between parties.
