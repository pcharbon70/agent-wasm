---
title: "Framework Plugin Manifests Composition And Lifecycle Hooks"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-05
  - phase-03
  - framework-plugin
  - manifest
  - composition
  - lifecycle-hooks
aliases:
  - "M5-P3 Framework Plugin Manifests Composition And Lifecycle Hooks"
---

# Framework Plugin Manifests Composition And Lifecycle Hooks

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
--
Capabilities, Plugins, Security, And Tenancy.
It defines the declarative manifest contract, deterministic composition
ordering, and the trust-tier separation between framework plugins and
individual Extism guest modules.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

## 3.1 Contract And Data Model

### Identity and versioning

> **Normative definition.**
The host MUST treat every framework plugin as a uniquely named, semantically
versioned, and publisher-attributed artifact independent of the Extism guest
modules it may contain.

> **Normative definition.**

```
PluginId = string
PublisherId = string
SemanticVersion = {
  major: u32,
  minor: u32,
  patch: u32,
  pre_release: string?
}

FrameworkPluginManifest {
  manifest_version: ManifestVersion,
  id: PluginId,
  publisher: PublisherId,
  name: string,
  description: string?,
  version: SemanticVersion,
  homepage: string?,
  license: string?,
  artifacts: ArtifactReference[],
  actions: ActionDeclaration[],
  routes: RouteDeclaration[],
  state_namespaces: string[],
  schemas: SchemaDeclaration[],
  strategies: StrategyDeclaration[],
  directives: DirectiveDeclaration[],
  schedules: ScheduleDeclaration[],
  requested_grants: Capability[],
  lifecycle_ownership: LifecycleOwnership?
}

ManifestVersion = "1.0"
```

> **Normative definition.**
The `manifest_version` field is a stable string.
The host MUST reject any manifest whose `manifest_version` is not
recognised.
The host MUST compare `manifest_version` as an exact string match,
not as a numeric range.

> **Non-normative note.**
The manifest version is independent of the plugin's semantic version.
A new manifest version is a backward-incompatible rewrite of the contract
itself and requires a major bump in the plugin's semantic version.

> **Normative definition.**
The `id` field is a stable, lower-kebab-case identifier that uniquely
identifies the plugin within the host's plugin registry.
Two plugins with the same `id` are mutually exclusive and one MUST
always override the other through the host's precedence rules.

> **Normative implementation-defined choice.**
The host defines the exact rules used to validate the `id` format.
The host MUST document this format in its conformance profile and reject
identifiers that do not match it.

> **Normative definition.**
The `publisher` field is the identifier of the trusted entity responsible
for the plugin's contents.
The host MUST validate `publisher` against the trust model defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

> **Normative definition.**
The `version` field is parsed as a Semantic Version and MUST conform to the
pattern defined by [Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).
The host MUST reject manifests whose `version` does not parse as a valid
semantic version.

> **Non-normative note.**
Semantic versioning enables the host to detect breaking changes,
backwards-compatible extensions, and patch-level hot fixes without
ambiguous heuristics.

### Artifacts

> **Normative definition.**
The `artifacts` field is an ordered list of artifact references that the
plugin declares.
Each artifact reference MUST include a stable artifact identifier, a
content-addressable digest, and a declared trust tier.

> **Normative definition.**

```
ArtifactReference {
  artifact_id: ArtifactId,
  digest: Digest,
  trust_tier: ArtifactTrustTier,
  size_bytes: u64?,
  media_type: string?
}

ArtifactId = string
Digest = {
  algorithm: HashAlgorithm,
  value: bytes
}

HashAlgorithm = "sha256" | "sha384" | "sha512"

ArtifactTrustTier = "untrusted-guest" | "reviewed-preparation" | "privileged-host"
```

> **Normative definition.**
The `trust_tier` field classifies each artifact into exactly one of three
tiers:

1. **`untrusted-guest`**: Raw guest module bytes (e.g., WASM).
   The host MUST treat all content as untrusted until validated
   against its schema and sandboxed within the Extism invocation boundary.
2. **`reviewed-preparation`**: Logic that prepares plugin state or
   migrates data.
   The host MUST review this logic before execution.
3. **`privileged-host`**: Native host integrations that require elevated
   privileges.
   The host MUST restrict these artifacts to approved operations
   and MUST NOT allow them to modify the plugin manifest itself.

> **Normative definition.**
The host MUST refuse to load any `privileged-host` artifact whose digest
does not match a digest previously recorded in an approved manifest
version.

> **Non-normative note.**
This tier separation is the primary mechanism for ensuring that the
plugin host cannot be subverted through an untrusted guest module.
Review gates and privilege boundaries are defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Actions

> **Normative definition.**
The `actions` field is an ordered list of action declarations that the
plugin exposes to agents.
Each action MUST have a unique name within the plugin and a stable
identifier.

> **Normative definition.**

```
ActionDeclaration {
  action_id: string,
  name: string,
  description: string?,
  input_schema: SchemaId?,
  output_schema: SchemaId?,
  capabilities_requested: Capability[],
  trust_tier: ArtifactTrustTier?,
  lifecycle_hooks: LifecycleHook[]?
}
```

> **Normative definition.**
The `action_id` field is stable across plugin versions.
The `name` field is human-readable and MAY change across versions,
but only if every previous version of the name is preserved in the
plugin's `aliases` frontmatter entry.

> **Normative definition.**
Each action's `capabilities_requested` field is the subset of the
plugin's top-level `requested_grants` that this specific action requires.
An action MUST NOT request capabilities outside of the plugin's
`requested_grants`.

> **Non-normative note.**
Scoping capabilities per action enables finer-grained policy decisions
during evaluation, as defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Routes

> **Normative definition.**
The `routes` field is an ordered list of route declarations that map
signal patterns or action invocations to plugin handlers.
The host MUST enforce that routes are unambiguous after composition.

> **Normative definition.**

```
RouteDeclaration {
  route_id: string,
  pattern: RoutePattern,
  target_action: string,
  priority: u32,
  capabilities_required: Capability[]?
}

RoutePattern = SignalPattern | ActionPattern

SignalPattern = {
  signal_kind: string,
  signal_subject: string?,
  signal_filter: JsonObject?
}

ActionPattern = {
  action_name: string,
  action_input_filter: JsonObject?
}
```

> **Normative definition.**
The `pattern` field describes the signal or action that triggers the
route.
The host MUST ensure that no two routes with the same priority match
the same pattern for the same signal kind.
When ambiguous routing is detected, the host MUST fail composition
with the diagnostic `ambiguous-route`.

> **Normative implementation-defined choice.**
The host defines how priority conflicts are resolved when two routes
match the same pattern with different priorities.
The host MUST document this resolution in its conformance profile.

> **Non-normative note.**
A deterministic route resolution prevents non-deterministic behavior in
multi-plugin environments where overlapping patterns are common.

### State namespaces

> **Normative definition.**
The `state_namespaces` field is a list of namespace identifiers that the
plugin declares for its internal state.
Each namespace MUST be unique within the plugin and MUST not collide
with namespaces declared by other installed plugins.

> **Normative definition.**

```
StateNamespace {
  namespace_id: string,
  description: string?,
  schema: SchemaId?,
  migration: MigrationDeclaration?
}
```

> **Normative definition.**
The host MUST reject plugin composition when any declared `namespace_id`
collides with an existing namespace in the registry.
The host MUST resolve collisions by name precedence within the plugin's
own declarations first, then by the global composition order defined in
[Composition order](#composition-order).

> **Non-normative note.**
State namespace isolation prevents plugins from inadvertently reading or
writing each other's data, a critical security property in multi-tenant
environments.

### Schemas

> **Normative definition.**
The `schemas` field is an ordered list of schema declarations that the
plugin uses for input validation, output structuring, and state storage.

> **Normative definition.**

```
SchemaDeclaration {
  schema_id: SchemaId,
  version: SemanticVersion,
  format: SchemaFormat,
  definition: JsonObject
}

SchemaId = string
SchemaFormat = "jsonschema" | "custom"
```

> **Normative definition.**
The host MUST validate each schema against its declared `format` before
composing the plugin.
Schemas that fail validation MUST cause the composition to fail with
the diagnostic `schema-validation-failed`.

> **Normative definition.**
Two plugins MUST NOT declare schemas with the same `schema_id` and
conflicting `definition` values.
When conflicting schemas are detected, the host MUST fail composition
with the diagnostic `schema-conflict`.

> **Non-normative note.**
Shared schema identifiers enable plugins to interoperate on a common
data contract.
Conflict detection ensures that such interop does not silently corrupt
data.

### Strategies

> **Normative definition.**
The `strategies` field is an ordered list of strategy declarations that
the plugin contributes to the agent's decision-making process.
Strategies replaceable by the host through the directive mechanism
defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

> **Normative definition.**

```
StrategyDeclaration {
  strategy_id: string,
  name: string,
  description: string?,
  priority: u32,
  capabilities_required: Capability[]?
}
```

> **Normative definition.**
The host MUST enforce that strategy `strategy_id` values are unique
within the plugin and do not conflict with strategies from other
installed plugins after composition.

### Directives

> **Normative definition.**
The `directives` field is an ordered list of directive declarations that
the plugin requests the host to consider during turn execution.
Directives are governed by
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

> **Normative definition.**

```
DirectiveDeclaration {
  directive_id: string,
  name: string,
  description: string?,
  capabilities_required: Capability[]?
}
```

> **Normative definition.**
The host MUST validate that each directive's `capabilities_required`
field is a subset of the plugin's `requested_grants`.

### Schedules

> **Normative definition.**
The `schedules` field is an ordered list of schedule declarations that
the plugin requests the host to manage.
Schedules are converted into signals by
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md).

> **Normative definition.**

```
ScheduleDeclaration {
  schedule_id: string,
  name: string,
  description: string?,
  interval_ms: u64,
  capabilities_required: Capability[]?
}
```

> **Normative definition.**
The host MUST enforce that `interval_ms` is a positive integer and that
no two active schedules with the same `schedule_id` exist simultaneously.

> **Non-normative note.**
Schedule management is delegated to the host's signal ingress subsystem
to keep the plugin runtime decoupled from time handling.

### Requested grants

> **Normative definition.**
The `requested_grants` field is an ordered list of capabilities the
plugin declares it needs.
These grants are evaluated against the trust model defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
and the attenuation policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

> **Normative definition.**

```
Capability = string
```

> **Normative definition.**
The host MUST deny plugin installation when any requested grant is
unresolvable under the current trust model.
The host MUST emit the diagnostic `grant-unresolvable` in this case.

> **Non-normative note.**
Requested grants are declarative.
The actual enforcement of these grants occurs at each policy evaluation
boundary as described in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Lifecycle ownership

> **Normative definition.**
The `lifecycle_ownership` field declares which entity owns the plugin's
lifecycle management operations.
When absent, the host owns the lifecycle by default.

> **Normative definition.**

```
LifecycleOwnership = "host" | "publisher" | "shared"
```

> **Normative definition.**
When `lifecycle_ownership` is `"host"`, the host retains exclusive
authority over install, enable, disable, upgrade, migrate, and remove
operations.
When `lifecycle_ownership` is `"publisher"`, the host MUST require
explicit publisher-signed approval for every lifecycle transition.
When `lifecycle_ownership` is `"shared"`, the host and publisher share
authority according to the rules defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).

> **Non-normative note.**
Lifecycle ownership controls who can promote or demote a plugin in the
registry.
Publishers who require strict control over their plugins SHOULD declare
`"publisher"` ownership; operators who need operational flexibility
SHOULD require `"host"` ownership for all third-party plugins.

## Composition order and conflict checks

### Composition order

> **Normative definition.**
The host MUST compose plugins in a deterministic, globally consistent
order determined by the following tie-breaking rules:

1. **Stable identifier**: Plugins are ordered by their `PluginId` in
   lexicographic order.
2. **Semantic version**: Ties are broken by descending semantic version
   (newest first).
3. **Manifest digest**: Final ties are broken by the content-addressable
   digest of the manifest.

> **Normative definition.**
The host MUST record the composition order as evidence and include it
in any diagnostic emitted during composition failure.

> **Non-normative note.**
A deterministic composition order ensures that conflict diagnostics
always point to the same pair of plugins, regardless of when or how
composition is triggered.

### Conflict checks

> **Normative definition.**
The host MUST perform the following conflict checks after composition,
in this order:

1. **Name conflict**: No two plugins may declare the same `name` after
   alias resolution.
2. **Route conflict**: No two routes across plugins may match the same
   signal pattern with the same priority.
3. **State namespace conflict**: No two plugins may declare the same
   `namespace_id`.
4. **Schema conflict**: No two plugins may declare schemas with the same
   `schema_id` and conflicting definitions.
5. **Migration conflict**: No two plugins may declare migrations that
   operate on the same namespace in incompatible ways.
6. **Capability conflict**: No two plugins may request capabilities that
   the trust model cannot simultaneously satisfy.
7. **Lifecycle ownership conflict**: No two plugins may claim
   `lifecycle_ownership: "publisher"` for the same capability without
   explicit operator approval.

> **Normative definition.**
When any conflict check fails, the host MUST fail the entire composition
with the specific diagnostic for the failing check.
The host MUST NOT partially apply any plugin whose composition fails.

> **Normative definition.**

| Diagnostic | Trigger |
|------------|---------|
| `name-conflict` | Two plugins share a resolved name |
| `route-conflict` | Two routes match the same pattern at the same priority |
| `namespace-conflict` | Two plugins declare the same namespace |
| `schema-conflict` | Two plugins declare conflicting schemas with the same id |
| `migration-conflict` | Two migrations target the same namespace incompatibly |
| `capability-conflict` | Trust model cannot satisfy all requested grants |
| `lifecycle-conflict` | Publisher-owned lifecycle claims conflict with operator policy |

> **Non-normative note.**
Failure to partially apply means that if any single conflict is detected,
none of the candidate plugins are installed.
This preserves a clean registry state and simplifies rollback.

## Trust-tier separation

### Declarative metadata

> **Normative definition.**
The manifest itself is declarative metadata.
It is inspected, validated, and composed without execution.
Declarative metadata includes:

1. All top-level fields defined in this section.
2. All schema declarations.
3. All route and action declarations.

> **Normative definition.**
Declarative metadata MAY be loaded by any agent or operator with read
access to the plugin registry.
Declarative metadata MUST NOT be executed directly by the runtime.

### Untrusted guest artifacts

> **Normative definition.**
All `untrusted-guest` artifacts are raw guest module bytes that the host
MUST treat as untrusted input.
The host MUST load them through the Extism invocation boundary defined
in
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)
and MUST validate all output before admitting it to the turn.

> **Normative definition.**
The host MUST sandbox `untrusted-guest` artifacts within the boundaries
established by
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).

> **Non-normative note.**
This tier ensures that even a malicious or compromised plugin cannot
escalate privileges through its guest module bytes.

### Reviewed preparation logic

> **Normative definition.**
All `reviewed-preparation` artifacts MUST be reviewed by an entity with
operator-level trust before execution.
The host MUST record the review evidence before allowing the artifact
to be loaded.

> **Normative definition.**
The review process MUST verify that the artifact:

1. Does not contain code paths that bypass the Extism invocation
   boundary.
2. Does not attempt to modify the plugin manifest.
3. Operates only on the plugin's declared state namespaces.
4. Requests only the capabilities declared in its `capabilities_required`.

> **Non-normative note.**
Review gates are the primary defense against supply-chain attacks on
plugin state migrations.

### Privileged host integrations

> **Normative definition.**
All `privileged-host` artifacts MUST be restricted to approved operations
defined by the host's conformance profile.
The host MUST log every invocation of a `privileged-host` artifact and
MUST NOT allow it to modify the plugin manifest or its own trust tier.

> **Normative definition.**
The host MUST reject any `privileged-host` artifact that attempts to:

1. Modify the plugin manifest after approval.
2. Elevate its own trust tier.
3. Access state namespaces declared by other plugins.
4. Request capabilities not declared in the manifest.

> **Non-normative note.**
Privileged artifacts are the highest-risk tier and require the strictest
controls.
Operators SHOULD minimize the number of plugins that declare
`privileged-host` artifacts.

## 3.2 Behavior And Integration

This section defines the runtime behavior of framework plugin manifests
composition and lifecycle hooks, including the ordered lifecycle
operations, the composition and authorization gates that must complete
before loading executable artifacts, and the specific failure scenarios
that the host MUST detect and report.

### Lifecycle operations

> **Normative definition.**
The following lifecycle operations are defined for framework plugins.
Each operation MUST complete all composition and authorization steps
before loading executable artifacts.

1. **install**: The host validates the manifest, resolves grants,
   composes the plugin, and records it in the registry without loading
   any artifacts.
2. **validate**: The host re-validates the manifest and all artifacts
   against their declared digests.
3. **approve**: The host requires explicit approval for plugins with
   `lifecycle_ownership: "publisher"` or for any `privileged-host`
   artifacts.
4. **enable**: The host loads executable artifacts into the runtime
   after install, validate, and approve have succeeded.
5. **disable**: The host unloads executable artifacts and freezes the
   plugin's state.
6. **upgrade**: The host validates the new manifest, resolves the new
   grants, and composes the new version.
   Migration is handled by
   [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).
7. **migrate**: The host applies migration artifacts in declared order,
   validated against their source namespaces and target schemas.
8. **rollback**: The host undoes migration artifacts in reverse order
   or restores the previous plugin version.
9. **remove**: The host unregisters the plugin, unloads artifacts,
   and archives its state according to
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

> **Normative definition.**
The lifecycle operations form a directed acyclic graph of valid
transitions.
The host MUST reject any transition that does not correspond to an
edge in the valid transition graph.
The host MUST record each completed transition as evidence in the
plugin's lifecycle audit log.

> **Non-normative note.**
The separation between install (metadata-only) and enable (artifact
loading) is critical: it ensures that no code runs before the manifest
is fully validated and authorized.
This separation is the primary mechanism for enforcing the trust-tier
model defined in [Trust-tier separation](#trust-tier-separation).

### Composition and authorization before artifact loading

> **Normative definition.**
The host MUST NOT load any executable artifact for a framework plugin
until the following conditions are all satisfied:

1. The manifest has been validated against the data model defined in
   [Contract And Data Model](#31-contract-and-data-model).
2. All artifacts have been resolved against their declared digests.
3. Composition has completed successfully with no unresolved conflicts
   as defined in
   [Composition order and conflict checks](#composition-order-and-conflict-checks).
4. All `requested_grants` have been resolved against the trust model
   defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
5. Authorization for the requested lifecycle operation has been obtained
   according to the `lifecycle_ownership` field defined in
   [Lifecycle ownership](#lifecycle-ownership).
6. For any `privileged-host` artifacts, the review evidence defined in
   [Reviewed preparation logic](#reviewed-preparation-logic) has been
   recorded.

> **Normative definition.**
If any condition above is not satisfied, the host MUST fail the lifecycle
operation with the appropriate diagnostic from
[Failure semantics](#failure-semantics).
The host MUST NOT leave the plugin in a partially-loaded state.

> **Non-normative note.**
This gate ensures that even if an operator or external system triggers
an enable operation prematurely, the host will refuse to load
unauthorized or unvalidated code.
The gate is enforced at the host runtime boundary and cannot be bypassed
by any plugin.

### Failure semantics

> **Normative definition.**
The host MUST define the following failure outcomes for framework plugin
manifests composition and lifecycle hooks:

1. **Malformed**: The manifest does not conform to the declared schema.
2. **Incompatible**: The manifest references a manifest version or
   schema format the host does not support.
3. **Conflicting**: A conflict check fails during composition.
4. **Unauthorized**: The publisher or operator lacks the trust class
   required for the requested lifecycle operation.
5. **Exhausted**: The host cannot allocate resources for the plugin
   (e.g., state namespace exhaustion, route table overflow).
6. **Unavailable**: A required dependency (artifact, grant, or operator
   approval) is unavailable.
7. **Missing dependency**: A referenced artifact or capability is not
   present in the registry.
8. **Version conflict**: A requested plugin version conflicts with an
   already-installed version of the same plugin.
9. **Circular dependency**: Two or more plugins depend on each other's
   lifecycle in a way that prevents resolution.
10. **Ambiguous route**: Two routes match the same pattern with the
    same priority.
11. **Orphaned state**: A plugin is removed while its state namespaces
    still have active references.
12. **Revoked publisher**: The publisher's trust class has been
    revoked.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and bounded
diagnostic that identifies the phase contract, profile, and failed
boundary without exposing secrets.

> **Normative definition.**

| Error Code | Description |
|------------|-------------|
| `plugin.malformed_manifest` | The manifest does not conform to the schema |
| `plugin.incompatible_version` | The manifest references an unsupported version |
| `plugin.conflict` | A composition conflict was detected |
| `plugin.unauthorized` | The caller lacks the required trust class |
| `plugin.exhausted` | Required resources are exhausted |
| `plugin.unavailable` | A required dependency is unavailable |
| `plugin.missing_dependency` | A referenced artifact or capability is missing |
| `plugin.version_conflict` | The requested version conflicts with an installed version |
| `plugin.circular_dependency` | Circular dependency detected among plugins |
| `plugin.ambiguous_route` | Two routes match the same pattern at the same priority |
| `plugin.orphaned_state` | A plugin has active state references after removal |
| `plugin.revoked_publisher` | The publisher's trust class has been revoked |

### Missing dependency

> **Normative definition.**
When the host detects a missing dependency during any lifecycle operation,
the host MUST abort the operation and emit the diagnostic
`plugin.missing_dependency`.
The diagnostic MUST identify the specific dependency that was missing,
the operation that was attempted, and the phase in which the dependency
was expected to be resolved.

> **Normative definition.**
The host MUST NOT leave any partial state for the operation that was
attempted.
If the operation was an install, the plugin MUST NOT be recorded in the
registry.
If the operation was an upgrade, the previous version of the plugin
MUST remain installed and enabled.

> **Non-normative note.**
Missing dependency is the most common failure mode during plugin
installation.
Operators SHOULD monitor for this diagnostic and ensure that dependency
artifacts are available before attempting plugin installation.

### Version conflict

> **Normative definition.**
When the host detects a version conflict during any lifecycle operation,
the host MUST abort the operation and emit the diagnostic
`plugin.version_conflict`.
The diagnostic MUST identify the requested version, the installed
version, and the operation that was attempted.

> **Normative definition.**
The host MUST NOT allow two versions of the same plugin to be installed
simultaneously unless the host's conformance profile explicitly permits
it.
The host's conformance profile MUST document the versioning policy.

> **Non-normative note.**
Version conflicts typically indicate an operator error (e.g., attempting
to install an older version over a newer one) or a supply-chain issue
(e.g., a registry returning a stale artifact).
The diagnostic SHOULD be informative enough to help the operator
diagnose the root cause.

### Circular dependency

> **Normative definition.**
When the host detects a circular dependency during composition, the host
MUST abort the composition and emit the diagnostic
`plugin.circular_dependency`.
The diagnostic MUST identify all plugins involved in the cycle, in the
order they form the cycle.

> **Normative definition.**
The host MUST use a deterministic cycle detection algorithm (e.g.,
depth-first search with coloring) to detect circular dependencies.
The host MUST record the cycle detection evidence in the lifecycle audit
log.

> **Non-normative note.**
Circular dependencies typically arise when two plugins declare
lifecycle hooks that depend on each other's state.
The host's composition order defined in
[Composition order and conflict checks](#composition-order-and-conflict-checks)
prevents most circular dependencies, but lifecycle hooks can create
cycles that are not detectable during composition alone.

### Ambiguous route

> **Normative definition.**
When the host detects an ambiguous route during composition, the host
MUST abort the composition and emit the diagnostic
`plugin.ambiguous_route`.
The diagnostic MUST identify both routes, the pattern they match, and
the priority at which the ambiguity occurs.

> **Normative definition.**
The host MUST NOT load any plugin that contributes to an ambiguous route.
The host MUST require the operator to resolve the ambiguity before
enabling either plugin.

> **Non-normative note.**
Ambiguous routes are a composition-time error, not a runtime error.
The host's route resolution logic defined in
[Routes](#routes) ensures that routes are unambiguous before any
plugin is enabled.

### Orphaned state

> **Normative definition.**
When the host detects orphaned state during a remove operation, the
host MUST abort the remove operation and emit the diagnostic
`plugin.orphaned_state`.
The diagnostic MUST identify the state namespaces that still have
active references and the operations that reference them.

> **Normative definition.**
The host MUST refuse to remove a plugin until all active references to
its state namespaces have been resolved.
The host MUST provide the operator with a mechanism to inspect the
active references and resolve them.

> **Non-normative note.**
Orphaned state typically arises when an agent or another plugin holds a
reference to a state namespace that belongs to the plugin being removed.
The operator MUST resolve these references before the plugin can be
removed.
If the references cannot be resolved, the operator MAY force-remove the
plugin, but the host MUST log the force-removal as evidence.

### Revoked publisher

> **Normative definition.**
When the host detects a revoked publisher, the host MUST immediately
disable all plugins authored by the revoked publisher and emit the
diagnostic `plugin.revoked_publisher`.
The diagnostic MUST identify the revoked publisher, the plugins affected,
and the revocation evidence.

> **Normative definition.**
The host MUST NOT allow any lifecycle operation on a plugin authored by
a revoked publisher until the publisher's trust class has been restored.
The host MUST log every attempt to perform a lifecycle operation on a
plugin authored by a revoked publisher as evidence.

> **Non-normative note.**
The revoked publisher behavior is the most disruptive: it requires the
host to take immediate action against all of an author's plugins, which
is why the trust model in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
emphasises revocation procedures.
Operators SHOULD define clear revocation procedures and communicate them
to publishers before publishing plugins.

## Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented
in the conformance profile:

1. **Plugin registry backend**: The storage mechanism for plugin
   manifests and artifacts (in-memory, database, filesystem, etc.).
2. **Route pattern matching**: The exact algorithm used to match
   signal and action patterns against routes.
3. **State namespace isolation**: The mechanism used to isolate plugin
   state namespaces (separate databases, table prefixes, in-memory
   maps, etc.).
4. **Review evidence storage**: The mechanism used to store review
   evidence for `reviewed-preparation` artifacts.
5. **Schedule resolution**: The mechanism used to convert schedule
   declarations into signals (timer threads, event loops, etc.).
6. **Lifecycle approval workflow**: The mechanism used to obtain
   operator approval for lifecycle transitions.
7. **Composition order tie-breaking**: The exact implementation of
   the tie-breaking rules defined in
   [Composition order](#composition-order).
8. **Conflict resolution priority**: The exact priority resolution
   when two routes match the same pattern with different priorities.

## Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Dynamic plugin discovery**: Runtime discovery of new plugin
   manifests without a host restart.
2. **Plugin marketplace**: A centralized or federated registry for
   plugin distribution.
3. **Plugin analytics**: Usage telemetry for plugin composition and
   lifecycle events.
4. **Plugin hot-reload**: Live swapping of plugin versions without
   downtime.
5. **Plugin sandboxing improvements**: Additional isolation layers
   beyond the Extism boundary for `privileged-host` artifacts.

## Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 3 MAY invalidate earlier milestone
assumptions:

1. **Composition latency**: If manifest composition latency exceeds
   the turn timeout, the timeout or composition batching strategy MUST
   be revised.
2. **Route table capacity**: If the route table exceeds the capacity
   planned in earlier milestones, the capacity plan MUST be revised.
3. **State namespace exhaustion**: If namespace allocation exhausts
   the planned capacity, the allocation strategy MUST be revised.
4. **Privileged artifact surface**: If the surface area of privileged
   artifacts is larger than planned, the trust model in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   MUST be revised.

> **Non-normative note.**
If any result from Phase 3 invalidates an earlier milestone assumption,
the affected milestone MUST be revised and re-validated.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Plugin registry backend | Implementation-defined | Document in conformance profile | Must support manifest storage and artifact digests |
| Route pattern matching | Implementation-defined | Document in conformance profile | Must enforce unambiguous resolution |
| State namespace isolation | Implementation-defined | Document in conformance profile | Must prevent cross-plugin state access |
| Review evidence storage | Implementation-defined | Document in conformance profile | Must persist review decisions |
| Schedule resolution | Implementation-defined | Document in conformance profile | Must convert schedules to signals deterministically |
| Lifecycle approval workflow | Implementation-defined | Document in conformance profile | Must support publisher and operator approval |
| Composition order tie-breaking | Implementation-defined | Document in conformance profile | Must produce a deterministic global order |
| Conflict resolution priority | Implementation-defined | Document in conformance profile | Must resolve route priority conflicts explicitly |
| Trust tier enforcement | Implementation-defined | Document in conformance profile | Must enforce all three trust tier rules |
| Manifest version validation | Implementation-defined | Document in conformance profile | Must reject unsupported manifest versions |

## 3.3 Failure Evidence And Operational Notes

This section establishes the failure outcomes, bounded diagnostics, evidence
requirements, implementation-defined choices, deferred work, and potential
invalidation results for framework plugin manifests composition and
lifecycle hooks.

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for framework plugin
manifests composition and lifecycle hooks. Each outcome represents a
distinct failure mode that the host MUST detect, classify, and report
without exposing secrets to unprivileged callers.

1. **Malformed**: The manifest does not conform to the declared schema
   or data model defined in [Contract And Data Model](#31-contract-and-data-model).
2. **Incompatible**: The manifest references a manifest version, schema
   format, or trust tier that the host does not support.
3. **Conflicting**: A conflict check fails during composition as defined
   in [Composition order and conflict checks](#composition-order-and-conflict-checks).
4. **Unauthorized**: The caller lacks the trust class required for the
   requested lifecycle operation as defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
5. **Exhausted**: The host cannot allocate resources for the plugin,
   including state namespace exhaustion, route table overflow, or
   capability grant exhaustion.
6. **Unavailable**: A required dependency is unavailable, including
   missing artifacts, unresolved grants, or pending operator approval.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code, a bounded
diagnostic message, and the phase boundary at which the failure was
detected. The diagnostic MUST identify the phase contract, the conformance
profile, and the failed boundary without exposing secrets, internal
state, or information accessible only to privileged callers.

> **Non-normative note.**
These six failure outcomes cover the primary failure modes for framework
plugin manifests composition and lifecycle hooks. Additional failure
outcomes are defined in the failure semantics subsection of
[Behavior And Integration](#32-behavior-and-integration), including
missing dependency, version conflict, circular dependency, ambiguous
route, orphaned state, and revoked publisher. Implementations SHOULD
emit diagnostics for all twelve failure outcomes to provide operators
with comprehensive failure visibility.

### Bounded diagnostics and evidence

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome. Each
diagnostic MUST contain:

1. The failure outcome category (malformed, incompatible, conflicting,
   unauthorized, exhausted, or unavailable).
2. The specific error code from the error code table.
3. The phase boundary at which the failure was detected.
4. The affected plugin identifier, if applicable.
5. A human-readable description of the failure.
6. The evidence required to reproduce or investigate the failure.

> **Normative definition.**
The host MUST NOT include the following information in diagnostics:

1. Internal implementation details, such as memory addresses, stack
   traces, or intermediate computation results.
2. Secrets, such as cryptographic keys, tokens, or passwords.
3. Information about other plugins or operators that the caller does
   not have permission to inspect.
4. Internal state of the host runtime, such as resource allocation
   tables or scheduler state.

> **Non-normative note.**
Bounded diagnostics prevent information leakage while still providing
operators with enough information to diagnose and resolve failures.
The evidence requirements ensure that operators can reproduce failures
in a controlled environment for debugging.

> **Normative definition.**
The host MUST record evidence for each failure outcome in the plugin's
lifecycle audit log. The evidence MUST include:

1. The timestamp of the failure.
2. The caller identity and trust class.
3. The requested lifecycle operation.
4. The failure outcome and error code.
5. The affected plugin identifier.
6. The phase boundary at which the failure was detected.
7. The diagnostic message.

> **Non-normative note.**
The lifecycle audit log provides a complete record of all failure
outcomes for forensic analysis, compliance auditing, and operational
monitoring. Operators SHOULD monitor the lifecycle audit log for
patterns that indicate systemic issues, such as repeated malformed
manifests from a specific publisher.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented
in the conformance profile. These choices affect how the host detects
and reports failure outcomes, but do not affect the normative failure
semantics defined in this section.

1. **Plugin registry backend**: The storage mechanism for plugin
   manifests and artifacts (in-memory, database, filesystem, etc.).
2. **Route pattern matching**: The exact algorithm used to match
   signal and action patterns against routes.
3. **State namespace isolation**: The mechanism used to isolate plugin
   state namespaces (separate databases, table prefixes, in-memory
   maps, etc.).
4. **Review evidence storage**: The mechanism used to store review
   evidence for `reviewed-preparation` artifacts.
5. **Schedule resolution**: The mechanism used to convert schedule
   declarations into signals (timer threads, event loops, etc.).
6. **Lifecycle approval workflow**: The mechanism used to obtain
   operator approval for lifecycle transitions.
7. **Composition order tie-breaking**: The exact implementation of
   the tie-breaking rules defined in
   [Composition order](#composition-order).
8. **Conflict resolution priority**: The exact priority resolution
   when two routes match the same pattern with different priorities.
9. **Diagnostic formatting**: The exact format of diagnostic messages
   (JSON, YAML, plain text, etc.).
10. **Audit log retention**: The retention policy for lifecycle audit
    log entries (TTL, archival, deletion, etc.).

> **Non-normative note.**
These implementation-defined choices allow host implementations to
optimize for their specific deployment environments while maintaining
normative conformance. Operators SHOULD review the conformance profile
to understand how the host implements these choices.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations.
These items are not part of the Phase 3 scope and MUST NOT be considered
normative obligations for Phase 3 conformance.

1. **Dynamic plugin discovery**: Runtime discovery of new plugin
   manifests without a host restart.
2. **Plugin marketplace**: A centralized or federated registry for
   plugin distribution.
3. **Plugin analytics**: Usage telemetry for plugin composition and
   lifecycle events.
4. **Plugin hot-reload**: Live swapping of plugin versions without
   downtime.
5. **Plugin sandboxing improvements**: Additional isolation layers
   beyond the Extism boundary for `privileged-host` artifacts.
6. **Cross-plugin dependency management**: Explicit dependency
   declarations between plugins and automatic resolution.
7. **Plugin compatibility matrix**: Automated verification that
   plugins are compatible before composition.

> **Non-normative note.**
Deferred work items are documented for awareness and to prevent scope
creep. Host implementations MAY choose to implement any or all of these
items as extensions beyond the Phase 3 scope.

### Results that could invalidate earlier milestones

> **Non-normative note.**
The following results from Phase 3 MAY invalidate earlier milestone
assumptions. If any of these results are observed during Phase 3
integration tests, the affected earlier milestone MUST be revised and
re-validated before Phase 3 can be promoted to `status: normative`.

1. **Composition latency**: If manifest composition latency exceeds
   the turn timeout defined in
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
   the timeout or composition batching strategy MUST be revised.
2. **Route table capacity**: If the route table exceeds the capacity
   planned in earlier milestones, the capacity plan MUST be revised.
3. **State namespace exhaustion**: If namespace allocation exhausts
   the planned capacity, the allocation strategy MUST be revised.
4. **Privileged artifact surface**: If the surface area of privileged
   artifacts is larger than planned, the trust model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   MUST be revised.
5. **Lifecycle operation ordering**: If the lifecycle operation ordering
   defined in [Lifecycle operations](#lifecycle-operations) proves
   insufficient for the observed deployment patterns, the ordering
   MUST be revised.

> **Non-normative note.**
If any result from Phase 3 invalidates an earlier milestone assumption,
the affected milestone MUST be revised and re-validated. The revision
process is governed by
[Specification Authority](../SPECIFICATION-AUTHORITY.md) and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

## 3.4 Phase 3 Integration Tests

This section defines the integration test scenarios, objectives, evidence
requirements, and cross-milestone compatibility checks for framework plugin
manifests composition and lifecycle hooks.
These tests prove the phase works as an integrated behavior and preserve
reproducible evidence for later milestone and release gates.

> **Non-normative note.**
> Integration tests verify observable contracts rather than private
> implementation structure.
> Tests that exercise only private implementation structure MUST be
> classified as implementation tests, not integration tests, and MUST
> NOT appear in this section.

### Test objectives

> **Normative definition.**
> The integration tests for this phase MUST verify the following objectives:

1. **Canonical successful flow**: Every lifecycle operation completes
   end-to-end without error when the manifest, artifacts, grants, and
   dependencies are all valid and available.
2. **Failure handling**: Every failure outcome defined in
   [Failure semantics](#failure-semantics) is detected, classified, and
   reported with a stable diagnostic when the triggering condition is
   present.
3. **Lifecycle enforcement**: The lifecycle transition graph defined in
   [Lifecycle operations](#lifecycle-operations) is enforced, and no
   unauthorized or partially-loaded state persists after any failure.
4. **Trust-tier separation**: Every trust tier rule defined in
   [Trust-tier separation](#trust-tier-separation) is enforced at
   runtime, and no artifact is loaded outside its declared tier.
5. **Cross-milestone compatibility**: All fixtures from earlier
   milestones that interact with the plugin registry remain functional
   after this phase is integrated.

> **Normative definition.**
> If any test objective cannot be verified with the available test
> harness, the objective MUST be recorded as a gap, and the gap MUST
> be documented in the Phase 3 integration test evidence report.
> The phase MUST NOT be promoted to `status: normative` with unresolved
> test objectives.

### Successful flow tests

> **Normative definition.**
> The following successful flow tests MUST be executed and pass for Phase
> 3 integration evidence.
> Each test MUST capture the observable outcome (registry state, audit
> log entries, diagnostics) as evidence.

> **Normative definition.**
>

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `P3-SUCCESS-01` | Valid manifest passes schema validation | Manifest is accepted; no diagnostic emitted |
| `P3-SUCCESS-02` | Composition with lexicographic order is deterministic | Plugins are composed in stable identifier order |
| `P3-SUCCESS-03` | Semantic version tie-breaking selects newest | Higher semantic version takes precedence |
| `P3-SUCCESS-04` | Manifest digest tie-breaking is stable | Equal identifiers and versions are ordered by digest |
| `P3-SUCCESS-05` | Trust tier untrusted-guest is sandboxed through Extism | Guest module bytes are loaded only through the invocation boundary |
| `P3-SUCCESS-06` | Trust tier reviewed-preparation requires review evidence | Artifact is loaded only after review evidence is recorded |
| `P3-SUCCESS-07` | Trust tier privileged-host is restricted to approved operations | Artifact is invoked only via the approved operation set |
| `P3-SUCCESS-08` | install operation completes without loading artifacts | Plugin is in the registry; no artifacts are loaded into the runtime |
| `P3-SUCCESS-09` | enable operation loads artifacts after install, validate, and approve | All artifacts are loaded into the runtime and the plugin is active |
| `P3-SUCCESS-10` | disable operation unloads artifacts and freezes state | All artifacts are unloaded; state is frozen but preserved |
| `P3-SUCCESS-11` | upgrade operation composes new version and migrates state | New version is installed; migration artifacts are applied |
| `P3-SUCCESS-12` | rollback operation restores previous version | Previous version is restored; migration artifacts are undone in reverse |
| `P3-SUCCESS-13` | remove operation unregisters plugin and archives state | Plugin is removed from the registry; state is archived per the storage contract |
| `P3-SUCCESS-14` | Route resolution is unambiguous for all configured routes | All routes resolve to exactly one target; no diagnostic emitted |
| `P3-SUCCESS-15` | State namespaces are isolated between plugins | Cross-plugin state access is prevented |
| `P3-SUCCESS-16` | Schedule declarations generate signals deterministically | Schedule signals are emitted at the configured intervals |
| `P3-SUCCESS-17` | Lifecycle ownership "host" allows host-only transitions | Publisher cannot trigger lifecycle transitions |
| `P3-SUCCESS-18` | Lifecycle ownership "publisher" requires publisher-signed approval | Host requires explicit publisher signature for each transition |
| `P3-SUCCESS-19` | Lifecycle ownership "shared" follows shared authority rules | Transitions follow the shared authority rules defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md) |
| `P3-SUCCESS-20` | Grant resolution succeeds for all requested grants | All requested grants are resolved; no `grant-unresolvable` diagnostic |

> **Non-normative note.**
> Test IDs are stable across Phase 3 revisions.
> New successful flow tests MUST use the next available ID in the
> `P3-SUCCESS-XX` sequence.
> Existing test IDs MUST NOT be reassigned or deleted.

#### Manifest validation

> **Normative definition.**
> Tests `P3-SUCCESS-01` through `P3-SUCCESS-04` verify that manifest
> validation succeeds for well-formed manifests.
> The host MUST accept every field defined in
> [Contract And Data Model](#31-contract-and-data-model) when the
> values conform to their declared types and constraints.

> **Non-normative note.**
> Manifest validation is the first gate in the install operation.
> A manifest that passes validation is guaranteed to be structurally
> correct but is not yet authorized for artifact loading.

#### Composition order

> **Normative definition.**
> Tests `P3-SUCCESS-02` through `P3-SUCCESS-04` verify that composition
> order is deterministic and consistent with the rules defined in
> [Composition order](#composition-order).

> **Non-normative note.**
> Deterministic composition order ensures that conflict diagnostics
> always identify the same plugins, regardless of the order in which
> they were submitted.

#### Trust tier enforcement

> **Normative definition.**
> Tests `P3-SUCCESS-05` through `P3-SUCCESS-07` verify that trust tier
> rules are enforced at runtime.
> Each test MUST confirm that artifacts are loaded through the mechanism
> defined for their tier.

> **Non-normative note.**
> Trust tier enforcement is the primary defense against supply-chain
> attacks.
> Tests in this category MUST be designed to detect any bypass of the
> tier boundaries.

#### Lifecycle operations

> **Normative definition.**
> Tests `P3-SUCCESS-08` through `P3-SUCCESS-13` and `P3-SUCCESS-17`
> through `P3-SUCCESS-19` verify that every lifecycle operation
> completes successfully under normal conditions.
> Each test MUST verify the post-condition of the operation, including
> registry state, audit log entries, and artifact loading status.

> **Non-normative note.**
> Lifecycle operations are the primary user-facing interface for plugin
> management.
> Operators rely on these operations to install, update, and remove
> plugins.
> Tests MUST verify both the happy path and the observability of each
> operation's outcome.

### Failure handling tests

> **Normative definition.**
> The following failure handling tests MUST be executed and pass for Phase
> 3 integration evidence.
> Each test MUST capture the specific diagnostic emitted, the registry
> state after failure, and the absence of unauthorized or partially-loaded
> artifacts.

> **Normative definition.**
>

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P3-FAIL-01` | Malformed manifest with missing required field | `plugin.malformed_manifest` |
| `P3-FAIL-02` | Malformed manifest with invalid semantic version | `plugin.malformed_manifest` |
| `P3-FAIL-03` | Incompatible manifest with unsupported manifest_version | `plugin.incompatible_version` |
| `P3-FAIL-04` | Stale manifest with expired artifact digest | `plugin.missing_dependency` |
| `P3-FAIL-05` | Duplicate plugin id with existing installed plugin | `plugin.version_conflict` |
| `P3-FAIL-06` | Boundary-limit: manifest with maximum number of actions | Diagnostic depends on host capacity policy |
| `P3-FAIL-07` | Boundary-limit: manifest with maximum number of routes | Diagnostic depends on host capacity policy |
| `P3-FAIL-08` | Conflicting name between two plugins | `plugin.conflict` |
| `P3-FAIL-09` | Conflicting route pattern at same priority | `plugin.ambiguous_route` |
| `P3-FAIL-10` | Conflicting state namespace between plugins | `plugin.conflict` |
| `P3-FAIL-11` | Conflicting schema definitions with same schema_id | `plugin.schema-conflict` |
| `P3-FAIL-12` | Unauthorized lifecycle transition by caller without required trust class | `plugin.unauthorized` |
| `P3-FAIL-13` | Resource exhaustion: state namespace allocation fails | `plugin.exhausted` |
| `P3-FAIL-14` | Unresolvable grant under current trust model | `plugin.missing_dependency` |
| `P3-FAIL-15` | Circular dependency between two plugins | `plugin.circular_dependency` |
| `P3-FAIL-16` | Orphaned state prevents remove operation | `plugin.orphaned_state` |
| `P3-FAIL-17` | Revoked publisher prevents all lifecycle operations | `plugin.revoked_publisher` |

> **Non-normative note.**
> Tests `P3-FAIL-06` and `P3-FAIL-07` are boundary-limit tests.
> The exact diagnostic emitted depends on the host's capacity policy,
> which is implementation-defined.
> Tests in this category MUST verify that the host does not exceed its
> declared capacity in any way, including silently degrading behavior.

#### Malformed inputs

> **Normative definition.**
> Tests `P3-FAIL-01` through `P3-FAIL-03` verify that malformed inputs
> are detected during manifest validation and produce the
> `plugin.malformed_manifest` or `plugin.incompatible_version` diagnostic.

> **Non-normative note.**
> Malformed inputs are the most common failure mode during initial
> plugin development.
> Diagnostics for malformed inputs MUST be informative enough to help
> plugin authors identify and fix the issue.

#### Incompatible inputs

> **Normative definition.**
> Tests `P3-FAIL-03` through `P3-FAIL-04` verify that incompatible inputs
> are detected and produce the appropriate diagnostic.

> **Non-normative note.**
> Incompatible inputs include manifests that reference features the host
> does not support, and artifacts whose digests do not match any
> previously approved version.

#### Stale inputs

> **Normative definition.**
> Tests `P3-FAIL-04` verify that stale inputs, including manifests that
> reference artifact digests that have been rotated or revoked, are
> detected and produce the `plugin.missing_dependency` diagnostic.

> **Non-normative note.**
> Stale inputs typically arise when an operator attempts to install a
> plugin whose artifacts have been updated in the registry without
> updating the manifest.

#### Duplicate inputs

> **Normative definition.**
> Tests `P3-FAIL-05` verify that duplicate plugin identifiers are
> detected and produce the `plugin.version_conflict` diagnostic.

> **Non-normative note.**
> Duplicate plugin identifiers indicate either an operator error or a
> supply-chain issue.
> The diagnostic MUST identify the conflicting version.

#### Boundary-limit inputs

> **Normative definition.**
> Tests `P3-FAIL-06` and `P3-FAIL-07` verify that boundary-limit inputs
> are handled without resource exhaustion or silent degradation.

> **Non-normative note.**
> Boundary-limit tests exercise the host's capacity policies.
> These tests MUST be designed to detect any bypass of capacity limits,
> including resource exhaustion, integer overflow, or memory corruption.

### Lifecycle enforcement tests

> **Normative definition.**
> The following lifecycle enforcement tests MUST be executed and pass for
> Phase 3 integration evidence.
> Each test MUST verify that the lifecycle transition graph is enforced
> and that no unauthorized or partially-loaded state persists after any
> failure.

> **Normative definition.**
>

| Test ID | Description | Expected outcome |
|---------|-------------|------------------|
| `P3-LIFE-01` | Invalid transition `remove` from `disabled` state | Transition rejected with diagnostic |
| `P3-LIFE-02` | Invalid transition `approve` before `install` | Transition rejected with diagnostic |
| `P3-LIFE-03` | Invalid transition `enable` before `approve` | Transition rejected with diagnostic |
| `P3-LIFE-04` | `disable` followed by `enable` reloads artifacts correctly | Artifacts are reloaded without error |
| `P3-LIFE-05` | `upgrade` followed by `rollback` restores previous state | Previous version is active with all state preserved |
| `P3-LIFE-06` | `enable` without prior `validate` is refused | Operation fails with `plugin.missing_dependency` |
| `P3-LIFE-07` | `enable` without prior `approve` is refused for publisher-owned plugin | Operation fails with `plugin.unauthorized` |
| `P3-LIFE-08` | `remove` with active state references is refused | Operation fails with `plugin.orphaned_state` |
| `P3-LIFE-09` | `upgrade` with missing artifact digest is refused | Operation fails with `plugin.missing_dependency` |
| `P3-LIFE-10` | `rollback` on a plugin with no upgrade history is refused | Operation fails with diagnostic identifying no upgrade history |
| `P3-LIFE-11` | Concurrent `upgrade` and `remove` on same plugin is serialized | Only one operation completes; the other is rejected or queued |
| `P3-LIFE-12` | `disable` while an agent invocation is in progress completes gracefully | In-progress invocation completes or is cancelled cleanly |

> **Non-normative note.**
> Lifecycle enforcement tests verify that the host does not enter an
> inconsistent state under any sequence of operations.
> These tests MUST be designed to detect state corruption, race
> conditions, and resource leaks.

### Cross-milestone compatibility tests

> **Normative definition.**
> The following cross-milestone compatibility tests MUST be executed and
> pass for Phase 3 integration evidence.
> These tests run fixtures from earlier milestones and verify that the
> integration of Phase 3 does not introduce regressions.

> **Normative definition.**
>

| Test ID | Earlier milestone fixture | Interaction point | Expected outcome |
|---------|---------------------------|-------------------|------------------|
| `P3-CROSS-01` | [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md) | Routes emit signals through the signal envelope | Signals are delivered to the correct destination |
| `P3-CROSS-02` | [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md) | Plugin actions are invoked during turn execution | Turn completes without protocol violations |
| `P3-CROSS-03` | [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md) | Plugin lifecycle transitions during host flow | Host flow completes without milestone rejection |
| `P3-CROSS-04` | [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md) | Plugin artifacts are stored and retrieved | Artifacts are stored and retrieved without corruption |
| `P3-CROSS-05` | [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md) | Guest modules are invoked through the Extism boundary | Output is validated and admitted to the turn |
| `P3-CROSS-06` | [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md) | Plugin state is accessed during agent lifecycle | Agent lifecycle proceeds without registry errors |
| `P3-CROSS-07` | [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md) | Plugin grants are evaluated against the trust model | Grant evaluation produces correct decisions |
| `P3-CROSS-08` | [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md) | Plugin capabilities are attenuated and enforced | Capabilities are attenuated per policy |
| `P3-CROSS-09` | [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md) | Plugin migration artifacts are applied | Migration completes without data loss |
| `P3-CROSS-10` | [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md) | Plugin state is archived on remove | State is archived per the storage contract |
| `P3-CROSS-11` | [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md) | Plugin schedules generate signals | Signals are generated at the configured intervals |
| `P3-CROSS-12` | [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md) | Plugin directives and strategies are loaded | Directives and strategies are available to the agent |

> **Non-normative note.**
> Cross-milestone compatibility tests are the final gate before Phase 3
> can be promoted to `status: normative`.
> Any regression in a cross-milestone test MUST be documented in the
> Phase 3 integration test evidence report and resolved before
> promotion.
> If a regression is approved as acceptable variability, the approval
> MUST be recorded in the test evidence report with an explicit
> rationale.

### Integration test evidence requirements

> **Normative definition.**
> The Phase 3 integration test evidence report MUST include the following:

1. **Test execution summary**: The date, environment, and version of
   the host implementation used for testing.
2. **Test results**: For each test, the result (pass, fail, or gap),
   the observable outcome captured, and the diagnostic emitted, if any.
3. **Registry state snapshots**: Registry state snapshots before and
   after each lifecycle operation test, to verify that no unauthorized
   or partially-loaded state persists.
4. **Audit log entries**: Lifecycle audit log entries for each
   completed lifecycle operation and failure, to verify that all
   transitions are recorded.
5. **Cross-milestone regression report**: For each cross-milestone
   test, the result, the interaction point, and any observed regression.
6. **Gap report**: For each test objective that could not be verified,
   the reason for the gap, the impact on conformance, and the
   proposed resolution.
7. **Approved variability**: For each approved variability (e.g.,
   cross-milestone regression approved as acceptable), the rationale,
   the scope of impact, and the expected resolution timeline.

> **Normative definition.**
> The Phase 3 integration test evidence report MUST be stored in
> [50-journal/](../50-journal/) or a location documented in the
> repository's index, and MUST be linked from this specification chapter
> for traceability.

> **Non-normative note.**
> The integration test evidence report is the primary artifact for
> promoting Phase 3 to `status: normative`.
> Operators and reviewers SHOULD use the report to verify that Phase 3
> has been implemented correctly and does not introduce regressions.
> The report MUST be updated whenever new tests are added or existing
> tests are modified.
