---
title: "Phase 3 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-03
  - implementation
  - behavior-and-integration
  - lifecycle-operations
  - composition-gates
  - failure-semantics
aliases:
  - "M5-P3-3.2 Implementation"
---

# Phase 3 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 3.2 (Behavior And Integration) from
[Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[32-framework-plugin-manifests-composition-and-lifecycle-hooks.md](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
which defines lifecycle operations, the composition and authorization gates
that must complete before loading executable artifacts, and the failure
semantics for framework plugin composition.

## Subtask 3.2.1.1: Define lifecycle operations

### Implementation

Defined nine lifecycle operations forming a directed acyclic graph of valid
transitions:

| Operation | Description | Preconditions |
|-----------|-------------|---------------|
| install | Validate manifest, resolve grants, compose, record in registry | None (metadata-only) |
| validate | Re-validate manifest and artifacts against declared digests | Installed |
| approve | Require explicit approval for publisher-owned or privileged artifacts | Validated |
| enable | Load executable artifacts into runtime | Installed, validated, approved |
| disable | Unload executable artifacts, freeze state | Enabled |
| upgrade | Validate new manifest, resolve new grants, compose new version | Installed/Enabled |
| migrate | Apply migration artifacts in declared order | Upgraded |
| rollback | Undo migration artifacts or restore previous version | Migrated |
| remove | Unregister plugin, unload artifacts, archive state | Disabled |

The lifecycle operations form a directed acyclic graph. The host MUST reject
any transition that does not correspond to an edge in the valid transition
graph. Each completed transition is recorded as evidence in the plugin's
lifecycle audit log.

### Design decisions

1. **Install is metadata-only, separate from enable**: This is the critical
   security separation. Install validates the manifest without loading any
   executable code. Enable loads artifacts only after install, validate,
   and approve have succeeded. This prevents unauthorized code execution.

2. **Lifecycle is a DAG, not a linear sequence**: The directed acyclic
   graph allows multiple paths (e.g., install -> enable -> disable ->
   enable) while preventing invalid transitions (e.g., enable without
   install). This provides flexibility while maintaining safety.

3. **Each transition is audited**: Recording each completed transition
   in the lifecycle audit log provides a complete history of plugin
   state changes for forensic analysis and compliance auditing.

## Subtask 3.2.1.2: Require composition and authorization before loading executable artifacts

### Implementation

Defined six conditions that MUST all be satisfied before loading any
executable artifact:

1. Manifest validated against data model defined in section 3.1
2. All artifacts resolved against declared digests
3. Composition completed successfully with no unresolved conflicts
4. All `requested_grants` resolved against trust model
5. Authorization for requested lifecycle operation obtained per `lifecycle_ownership`
6. For `privileged-host` artifacts, review evidence recorded

If any condition is not satisfied, the host MUST fail the lifecycle operation
with appropriate diagnostic. The host MUST NOT leave plugin in partially-loaded state.

### Design decisions

1. **Gate is enforced at host runtime boundary**: The gate cannot be
   bypassed by any plugin or external system. This is the primary
   defense against supply-chain attacks.

2. **No partial loading**: If any condition fails, the operation is
   aborted completely. This prevents inconsistent state where some
   artifacts are loaded but others are not.

3. **Review evidence is required for privileged artifacts**: Before
   `privileged-host` artifacts execute, the host requires recorded
   review evidence. This is the primary defense against supply-chain
   attacks on plugin state migrations.

## Subtask 3.2.1.3: Define failure semantics

### Implementation

Defined twelve failure outcomes for framework plugin composition:

| Failure | Error Code | Description |
|---------|-----------|-------------|
| Malformed | `plugin.malformed_manifest` | Manifest does not conform to schema |
| Incompatible | `plugin.incompatible_version` | References unsupported version |
| Conflicting | `plugin.conflict` | Composition conflict detected (general) |
| Unauthorized | `plugin.unauthorized` | Caller lacks required trust class |
| Exhausted | `plugin.exhausted` | Required resources exhausted |
| Unavailable | `plugin.unavailable` | Required dependency unavailable |
| Missing dependency | `plugin.missing_dependency` | Referenced artifact or capability missing |
| Version conflict | `plugin.version_conflict` | Requested version conflicts with installed |
| Circular dependency | `plugin.circular_dependency` | Circular dependency among plugins |
| Ambiguous route | `plugin.ambiguous_route` | Two routes match same pattern at same priority |
| Orphaned state | `plugin.orphaned_state` | Plugin has active state references after removal |
| Revoked publisher | `plugin.revoked_publisher` | Publisher's trust class revoked |

Each failure outcome is mapped to a specific error code and bounded
diagnostic that identifies the phase contract, profile, and failed
boundary without exposing secrets.

Additional behavior:
- **Missing dependency**: Host aborts operation and emits diagnostic.
  If install, plugin NOT recorded in registry. If upgrade, previous
  version remains installed and enabled.
- **Version conflict**: Host aborts operation. Two versions of same
  plugin cannot be installed simultaneously unless conformance profile
  explicitly permits it.
- **Circular dependency**: Host aborts composition and emits diagnostic
  identifying all plugins in cycle. Deterministic cycle detection
  algorithm required.
- **Ambiguous route**: Host aborts composition. No plugin contributing
  to ambiguous route can be loaded.
- **Orphaned state**: Host aborts remove operation. Plugin cannot be
  removed until all active references to its state namespaces resolved.
- **Revoked publisher**: Host immediately disables all plugins authored
  by revoked publisher. No lifecycle operations allowed until trust
  class restored.

### Design decisions

1. **Failure is atomic**: When any conflict check fails, the entire
   composition fails. No partial application occurs. This preserves
   a clean registry state and simplifies rollback.

2. **Revoked publisher is immediately enforced**: When a publisher's
   trust class is revoked, all their plugins are immediately disabled.
   This is the most disruptive failure mode and requires clear
   revocation procedures.

3. **Diagnostics identify the specific failure**: Each error code is
   accompanied by a diagnostic that identifies the phase contract,
   profile, and failed boundary. This enables operators to diagnose
   and resolve failures without exposing secrets.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks Contract And Data Model](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.3: [Framework Plugin Manifests Composition And Lifecycle Hooks Failure Evidence And Operational Notes](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.4: [Framework Plugin Manifests Composition And Lifecycle Hooks Phase 3 Integration Tests](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Agent manifests: [Agent Manifests Artifacts Schemas And Registries](../../60-specification/03-agent-manifests-artifacts-schemas-and-registries.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Directives: [Directives Strategies Continuations And Terminal States](../../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
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
