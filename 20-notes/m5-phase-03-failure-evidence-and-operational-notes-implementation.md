---
title: "Phase 3 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-03
  - implementation
  - failure-evidence-and-operational-notes
  - plugin-diagnostics
  - lifecycle-audit
  - bounded-diagnostics
aliases:
  - "M5-P3-3.3 Implementation"
---

# Phase 3 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 3.3 (Failure Evidence And Operational Notes) from
[Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[32-framework-plugin-manifests-composition-and-lifecycle-hooks.md](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
which consolidates failure outcomes, bounded diagnostics, evidence
requirements, implementation-defined choices, deferred work, and potential
invalidation results for framework plugin manifests composition.

## Subtask 3.3.1.1: Define failure outcomes (consolidated)

### Implementation

Consolidated the six primary failure outcomes defined throughout the chapter:

| Outcome | Canonical Definition | Relevant Error Codes |
|---------|---------------------|---------------------|
| Malformed | Manifest does not conform to declared schema | `plugin.malformed_manifest` |
| Incompatible | References unsupported manifest version, schema format, or trust tier | `plugin.incompatible_version` |
| Conflicting | Composition conflict check fails | `plugin.conflict`, `plugin.name_conflict`, `plugin.route_conflict`, `plugin.namespace_conflict`, `plugin.schema_conflict`, `plugin.migration_conflict`, `plugin.capability_conflict`, `plugin.lifecycle_conflict` |
| Unauthorized | Caller lacks trust class for requested lifecycle operation | `plugin.unauthorized` |
| Exhausted | Host cannot allocate resources (state namespace exhaustion, route table overflow, capability grant exhaustion) | `plugin.exhausted` |
| Unavailable | Required dependency unavailable (missing artifacts, unresolved grants, pending operator approval) | `plugin.unavailable`, `plugin.missing_dependency` |

Additional failure outcomes from Behavior And Integration:
- `plugin.version_conflict`: Requested version conflicts with installed version
- `plugin.circular_dependency`: Circular dependency among plugins
- `plugin.ambiguous_route`: Two routes match same pattern at same priority
- `plugin.orphaned_state`: Plugin has active state references after removal
- `plugin.revoked_publisher`: Publisher's trust class revoked
- `plugin.schema_validation_failed`: Schema validation check failed
- `plugin.grant_unresolvable`: Requested grant cannot be resolved

### Design decisions

1. **Six primary outcomes are exhaustive**: The six primary failure
   outcomes (malformed, incompatible, conflicting, unauthorized,
   exhausted, unavailable) cover all failure modes. Additional outcomes
   (version conflict, circular dependency, etc.) are subtypes or
   specific cases of these primary outcomes.

2. **Canonical definitions are referenced, not duplicated**: The
   consolidated section references the canonical definitions in
   Behavior And Integration rather than re-defining them. This
   avoids duplication and ensures consistency.

3. **Error codes are stable and namespaced**: All error codes use
   the `plugin.*` prefix, making it easy for operators to filter
   diagnostics by domain.

## Subtask 3.3.1.2: Define bounded diagnostics and evidence

### Implementation

Defined bounded diagnostics for plugin failures. Each diagnostic MUST
contain:

1. Failure outcome category (malformed, incompatible, conflicting,
   unauthorized, exhausted, or unavailable)
2. Specific error code from error code table
3. Phase boundary at which failure was detected
4. Affected plugin identifier (if applicable)
5. Human-readable description of failure
6. Evidence required to reproduce or investigate failure

Prohibited content in diagnostics:
- Internal implementation details (memory addresses, stack traces,
  intermediate computation results)
- Secrets (cryptographic keys, tokens, passwords)
- Information about other plugins or operators not accessible to caller
- Internal state of host runtime (resource allocation tables, scheduler state)

Evidence recording requirements:
Each failure outcome MUST be recorded in plugin's lifecycle audit log
with:
1. Timestamp of failure
2. Caller identity and trust class
3. Requested lifecycle operation
4. Failure outcome and error code
5. Affected plugin identifier
6. Phase boundary at which failure detected
7. Diagnostic message

### Design decisions

1. **Diagnostics are bounded by prohibition**: Rather than listing
   what to include, the spec explicitly prohibits what to exclude
   (internal details, secrets, cross-plugin information). This is
   more flexible for implementations and avoids accidentally omitting
   required fields.

2. **Evidence is structured for forensic analysis**: The required
   evidence fields enable operators to reproduce failures in a
   controlled environment for debugging. The lifecycle audit log
   provides a complete record of all failure outcomes.

3. **Cross-plugin information is restricted**: Diagnostics do not
   expose information about other plugins or operators that the
   caller does not have permission to inspect. This prevents
   information leakage in multi-tenant or multi-publisher scenarios.

## Subtask 3.3.1.3: Document implementation-defined choices and deferred work

### Implementation

**Implementation-defined choices** (must be documented in conformance profile):
1. Plugin registry backend (in-memory, database, filesystem, etc.)
2. Route pattern matching algorithm
3. State namespace isolation mechanism
4. Review evidence storage mechanism
5. Schedule resolution mechanism (timer threads, event loops, etc.)
6. Lifecycle approval workflow mechanism
7. Composition order tie-breaking implementation
8. Conflict resolution priority when routes match same pattern with different priorities
9. Diagnostic formatting (JSON, YAML, plain text, etc.)
10. Audit log retention policy

**Deferred work**:
1. Dynamic plugin discovery: Runtime discovery of new plugin manifests without host restart
2. Plugin marketplace: Centralized or federated registry for plugin distribution
3. Plugin analytics: Usage telemetry for plugin composition and lifecycle events
4. Plugin hot-reload: Live swapping of plugin versions without downtime
5. Plugin sandboxing improvements: Additional isolation layers beyond Extism boundary for `privileged-host` artifacts
6. Cross-plugin dependency management: Explicit dependency declarations between plugins and automatic resolution
7. Plugin compatibility matrix: Automated verification that plugins are compatible before composition

**Results invalidating earlier milestones**:
1. Composition latency exceeding turn timeout
2. Route table exceeding capacity planned in earlier milestones
3. State namespace exhaustion exceeding planned capacity
4. Privileged artifact surface larger than planned (requires trust model revision)
5. Lifecycle operation ordering insufficient for observed deployment patterns

### Design decisions

1. **Implementation-defined choices are operational, not normative**:
   The normative contract (what must happen) is fully specified; only
   the mechanism (how it happens) is left to implementations. This
   ensures conformance while allowing flexibility.

2. **Deferred work is clearly separated from normative obligations**:
   The deferred items are explicitly marked as non-normative. This
   prevents scope creep and makes it clear what is required for M5
   promotion.

3. **Invalidation results are observable conditions**: Each invalidation
   trigger is a measurable condition (latency, capacity, size) that can
   be monitored during integration testing.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks Contract And Data Model](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.2: [Framework Plugin Manifests Composition And Lifecycle Hooks Behavior And Integration](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.4: [Framework Plugin Manifests Composition And Lifecycle Hooks Phase 3 Integration Tests](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Agent manifests: [Agent Manifests Artifacts Schemas And Registries](../60-specification/03-agent-manifests-artifacts-schemas-and-registries.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Directives: [Directives Strategies Continuations And Terminal States](../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
- Migration: [Retry Timer Recovery Replay Hibernate And Migration](../60-specification/28-retry-timer-recovery-replay-hibernate-and-migration.md)
- Storage: [Revisioned Snapshots Journals History And Storage Contracts](../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)

## Open questions

1. Should diagnostics include a severity level? The current design
   only includes failure outcome category and error code. A severity
   level (info, warning, error, critical) would help operators prioritize
   responses.

2. How should plugin registry backend choices affect conformance? The
   spec allows in-memory, database, or filesystem backends but does
   not specify whether certain features (e.g., concurrent access,
   durability guarantees) require specific backend types.

3. Can deferred work items be promoted to later milestones without
   specification changes? The spec lists deferred work but does not
   address whether these items can be implemented as extensions without
   becoming normative.
