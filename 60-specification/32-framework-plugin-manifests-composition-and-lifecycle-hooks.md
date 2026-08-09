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

## Lifecycle operations

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

> **Non-normative note.**
The separation between install (metadata-only) and enable (artifact
loading) is critical: it ensures that no code runs before the manifest
is fully validated and authorized.

## Failure semantics

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

### Missing dependency, version conflict, circular dependency, ambiguous route, orphaned state, revoked publisher behavior

> **Non-normative note.**
Each of the failure modes above has specific recovery semantics:

- **Missing dependency**: The host MUST abort the install and record
  which dependency was missing.
- **Version conflict**: The host MUST abort the install and record
  the conflicting version.
- **Circular dependency**: The host MUST abort the install and report
  all plugins in the cycle.
- **Ambiguous route**: The host MUST abort the composition and report
  both conflicting routes.
- **Orphaned state**: The host MUST refuse removal until all references
  are resolved.
- **Revoked publisher**: The host MUST immediately disable all plugins
  authored by the revoked publisher.

> **Non-normative note.**
The revoked publisher behavior is the most disruptive: it requires the
host to take immediate action against all of an author's plugins, which
is why the trust model in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
emphasises revocation procedures.

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
