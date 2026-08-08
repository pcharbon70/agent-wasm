---
title: "Agent Manifests Artifacts Schemas And Registries"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-01
  - phase-03
  - artifact
  - manifest
  - schema
  - registry
aliases:
  - "M1-P3 Manifests And Artifacts"
---

# Agent Manifests Artifacts Schemas And Registries

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-03-agent-manifests-artifacts-schemas-and-registries.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It defines immutable executable artifacts and reviewable manifests that can
be resolved without instantiating guest code.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
integration tests in
Section 3.4
and a passing cross-milestone fixture run recorded in
Section 3.4.1.4.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md).

## Artifacts

### Artifact structure

An artifact is an immutable, content-addressed bundle containing:

1. One or more core-Wasm module bytes (the plug-in code).
2. One `AgentManifest` describing the artifact's capabilities.
3. Optional signature references for provenance verification.

An artifact is identified by a digest of its canonical representation.
The canonical representation is:

> **Normative definition.**

```
canonical = concatenate(
  sort_keys(manifest_json),
  sorted_module_bytes_by_name
)
digest = hash(canonical)
> **Normative definition.**

```

The hash function MUST be SHA-256 or stronger.

### Artifact digests

Artifact digests use the following format:

> **Normative definition.**

```
artifact:<algorithm>:<hex-digest>
> **Normative definition.**

```

Examples:

- `artifact:sha256:a1b2c3d4e5f6...`
- `artifact:sha512:9f8e7d6c5b4a...`

The digest algorithm MUST be recorded in the canonical representation and
used for all digest comparisons.

### Media types

The following media types are used for artifacts and manifests:

| Media type | Content |
| --- | --- |
| `application/wasm` | Core Wasm module bytes |
| `application/agent-manifest+json` | AgentManifest in canonical JSON |
| `application/agent-schema+json` | State schema in canonical JSON |
| `application/agent-artifact-manifest+json` | Artifact manifest with digest and metadata |

### Build provenance

Build provenance records the circumstances under which an artifact was
produced.
The following provenance fields are REQUIRED:

| Field | Description |
| --- | --- |
| `compiler` | Name and version of the compiler used |
| `pdk` | Name and version of the plug-in development kit |
| `source_commit` | Git commit SHA of the source code |
| `build_timestamp` | ISO 8601 timestamp of the build |
| `target_arch` | Target architecture (e.g., `wasm32-unknown-unknown`) |
| `target_features` | Wasm features enabled during compilation |

Optional fields MAY include:

- `builder`: Identity of the build system or human
- `dependencies`: List of dependency digests
- `signatures`: List of signature references

### Signature references

Signature references identify cryptographic signatures over the artifact
canonical representation.
The host MAY verify signatures at admission time.

Signature reference structure:

> **Normative definition.**

```
{
  "algorithm": "ed25519 | rsa-pss | ecdsa-p256",
  "key_id": "string",
  "signature": "base64-encoded",
  "timestamp": "ISO 8601"
}
> **Normative definition.**

```

The host MUST NOT rely on signatures for security; signatures provide
provenance and non-repudiation only.

## AgentManifest

### Manifest fields

The `AgentManifest` describes an artifact's capabilities and is REQUIRED
for all artifacts.
The following fields are REQUIRED:

| Field | Type | Description |
| --- | --- | --- |
| `artifact_digest` | `artifact:<algo>:<hex>` | Digest of this artifact |
| `protocol_version` | `string` | Host--guest protocol version |
| `manifest_version` | `string` | Manifest schema version |
| `name` | `string` | Human-readable artifact name |
| `version` | `string` | Semantic version of this artifact |
| `publisher` | `string` | Publisher identity |
| `description` | `string` | Human-readable description |
| `actions` | `Action[]` | Exported actions |
| `routes` | `Route[]` | Declared routes |
| `state_schemas` | `StateSchema[]` | Declared state schemas |
| `strategies` | `Strategy[]` | Declared strategies |
| `required_capabilities` | `Capability[]` | Required host capabilities |
| `required_features` | `string[]` | Required Wasm features beyond Core 3.0 |
| `migrations` | `Migration[]` | State migration definitions |
| `provenance` | `Provenance` | Build provenance record |

### Action definition

An action declares a named operation with input and output schemas.

> **Normative definition.**

```
Action {
  name: string,
  version: string,
  description: string,
  input_schema: SchemaRef,
  output_schema: SchemaRef,
  capabilities: Capability[],
  handlers: {
    kind: "reducer" | "host_function",
    entry: string
  }
}
> **Normative definition.**

```

Actions are resolved by the host; guest code does not invoke actions directly.

### Route definition

A route maps signal types and subjects to target actions and strategies.

> **Normative definition.**

```
Route {
  signal_type: string,
  subject_pattern: string,
  action: string,
  strategy: string,
  precedence: int,
  description: string
}
> **Normative definition.**

```

Routes are compiled by the host into a route table.
Conflicts (same signal_type + subject_pattern) are rejected at composition.

### State schema definition

A state schema defines the structure of agent state.

> **Normative definition.**

```
StateSchema {
  name: string,
  version: string,
  description: string,
  initial_state: JsonObject,
  fields: Field[],
  migrations: Migration[]
}
> **Normative definition.**

```

Schemas are validated against the initial state and field definitions.
Migrations transform state between versions.

### Strategy definition

A strategy defines transition logic for advancing agent state.

> **Normative definition.**

```
Strategy {
  name: string,
  version: string,
  description: string,
  snapshot_schema: SchemaRef,
  reducer_entry: string,
  terminal_states: string[]
}
> **Normative definition.**

```

Strategies are implemented as plug-in reducer exports.
The host invokes strategies via the `reduce` export.

### Capability definition

A capability declares a host operation that the artifact requires.

> **Normative definition.**

```
Capability {
  name: string,
  version: string,
  description: string,
  parameters: SchemaRef,
  result: SchemaRef,
  authorization: Authorization[]
}
> **Normative definition.**

```

Capabilities are granted by the host at invocation time.
The host enforces authorization independently.

### Migration definition

A migration transforms state from one version to the next.

> **Normative definition.**

```
Migration {
  from_version: string,
  to_version: string,
  transform: Transform,
  author: string,
  description: string
}
> **Normative definition.**

```

Migrations are executed by the host during state upgrades.
Guest code does not execute migrations.

## Schemas

### Schema identifiers

Schema identifiers use the following format:

> **Normative definition.**

```
schema:<tenant>/<name>:<version>
> **Normative definition.**

```

Examples:

- `schema:acme-corp/chatbot-state:1.2.0`
- `schema:acme-corp/chatbot-snapshot:0.1.0`

### Canonical schema hashing

Schema hashes are computed over the canonical JSON representation.
Canonical JSON is defined by sorting keys lexicographically, formatting
numbers without trailing zeros, and using double quotes for strings.

> **Normative definition.**

```
schema_hash = hash(canonical_json(schema))
> **Normative definition.**

```

Schema hashes are used for:

- State versioning and compatibility checks
- Snapshot identity and integrity verification
- Migration target validation

### Schema ownership

Schema ownership determines who may modify a schema.
The following ownership rules apply:

| Schema type | Owner | Modification policy |
| --- | --- | --- |
| State schema | Artifact publisher | Immutable once published; migrations required for changes |
| Snapshot schema | Host | Host-defined; artifact declares compatibility |
| Strategy schema | Artifact publisher | Immutable once published; versioned independently |

### Schema compatibility

Schema compatibility follows semantic versioning rules:

- **MAJOR** version increments indicate breaking changes.
  Implementations MUST reject inputs with a higher MAJOR version than supported.

- **MINOR** version increments indicate backward-compatible additions.
  Implementations MAY accept inputs with a higher MINOR version if additions
  are optional.

- **PATCH** version increments indicate backward-compatible fixes.
  Implementations MUST accept inputs with any PATCH version within the
  same MAJOR.MINOR range.

### Migration references

State migrations reference source and target schema versions.
Migrations are applied in version order.
Circular migration chains are rejected.

> **Normative definition.**

```
migration_chain = [
  schema:<tenant>/state:1.0.0 -> schema:<tenant>/state:1.1.0,
  schema:<tenant>/state:1.1.0 -> schema:<tenant>/state:2.0.0
]
> **Normative definition.**

```

## Registries

### Registry lookup

Registries provide lookup of artifacts and manifests by:

1. **Immutable digest:** The primary lookup key.
   Lookups by digest are deterministic and collision-resistant.

2. **Approved aliases:** Optional human-readable names or semantic versions.
   Aliases are resolved to digests at lookup time.
   Aliases MAY be expired or revoked by the registry owner.

Lookup flow:

> **Normative definition.**

```
1. Receive lookup request (digest OR alias)
2. If digest: validate format, compute hash, retrieve record
3. If alias: validate alias format, resolve to digest, retrieve record
4. Return record OR rejection diagnostic
> **Normative definition.**

```

### Registry record structure

A registry record contains:

> **Normative definition.**

```
RegistryRecord {
  digest: string,
  media_type: string,
  size_bytes: int,
  created_at: ISO 8601,
  updated_at: ISO 8601,
  aliases: string[],
  signatures: SignatureReference[],
  metadata: JsonObject
}
> **Normative definition.**

```

### Validation order

Artifact and manifest validation proceeds in the following order:

1. **Bytes integrity:** Verify module bytes decode as valid Wasm.
2. **Digest verification:** Compute digest and compare to declared digest.
3. **Signature verification:** Verify signatures if present (non-blocking).
4. **Feature profile:** Check required Wasm features against host support.
5. **Manifest structure:** Validate manifest JSON schema and field types.
6. **Manifest compatibility:** Check version fields against host supported range.
7. **Schema validation:** Validate state and snapshot schemas.
8. **Policy admission:** Check host policy (allowlist, capability grants).

Rejection at any step HALTS further validation.
Partial validation results are NOT committed.

### Cache keys

Compiled artifact cache keys include:

> **Normative definition.**

```
cache_key = hash(
  runtime_family,
  runtime_version,
  target_arch,
  target_features,
  artifact_digest,
  validation_policy
)
> **Normative definition.**

```

Cache entries are invalidated when:

- The artifact digest changes.
- The runtime family or version changes.
- The target architecture or features change.
- The validation policy changes.

Cache hits MUST be verified against the current validation policy before use.

## Implementation-defined choices and deferred work

### Implementation-defined choices

| Choice | Domain | Required documentation |
| --- | --- | --- |
| Digest algorithm | Artifacts | SHA-256, SHA-512, or stronger; documented in conformance profile |
| Signature verification | Artifacts | Which algorithms are verified; verification policy |
| Alias resolution | Registries | Resolution strategy and expiration handling |
| Registry backend | Registries | Database, storage format, and replication strategy |
| Cache invalidation policy | Caching | Invalidation triggers and TTL if used |
| Schema migration execution | Schemas | Migration execution order and rollback policy |
| Provenance storage | Provenance | Provenance retention and archival strategy |

### Deferred work

| Item | Target | Reason |
| --- | --- | --- |
| Artifact signature verification | Milestone 5 | Requires provenance and trust model |
| Registry replication | Milestone 9 | Requires production platform and deployment |
| Schema migration UI | Milestone 9 | Requires developer experience and tooling |
| Artifact dependency resolution | Milestone 5 | Requires capability and plugin system |
| Registry access control | Milestone 5 | Requires security and tenancy model |
| Schema evolution tooling | Milestone 7 | Requires AI tools and memory |
| Artifact compression | Milestone 8 | Requires portability and performance |

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter:

1. Canonical JSON representation is insufficient for large schemas; binary
   encoding is required for performance.
2. SHA-256 digest collisions are demonstrated at scale; stronger hash required.
3. Signature verification is essential for security; cannot be deferred to
   Milestone 5.
4. Alias resolution introduces ambiguity; digest-only lookup is required.
5. Schema migration execution is too complex for host; requires guest
   cooperation.

## Integration Test Expectations

This section defines the observable behavior that the Phase 3 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### Successful flow

The host MUST resolve artifacts and manifests by digest and aliases, validate
them in the specified order, and cache compiled results.
The test MUST verify that:

1. Artifact digests are computed correctly and match declared values.
2. Manifests are validated for structure, compatibility, and policy.
3. Schemas are validated for field types, initial state, and migrations.
4. Cache keys are computed correctly and cache hits are verified.
5. Provenance records are recorded and retained.

### Malformed artifacts

The host MUST reject artifacts with malformed bytes or manifests.
The test MUST verify that:

1. Invalid Wasm bytes are rejected with an `artifact.bytes.malformed` diagnostic.
2. Invalid manifest JSON is rejected with an `artifact.manifest.malformed` diagnostic.
3. Missing required manifest fields are rejected with an `artifact.manifest.missing_field` diagnostic.
4. Digest mismatches are rejected with an `artifact.digest.mismatch` diagnostic.

### Incompatible artifacts

The host MUST reject artifacts with incompatible versions or features.
The test MUST verify that:

1. Artifacts with unsupported protocol versions are rejected with an
   `artifact.compatibility.protocol_version` diagnostic.
2. Artifacts requiring unsupported Wasm features are rejected with an
   `artifact.compatibility.unsupported_feature` diagnostic.
3. Artifacts with incompatible schema versions are rejected with an
   `artifact.compatibility.schema_version` diagnostic.

### Stale artifacts

The host MUST detect and reject stale or outdated artifacts.
The test MUST verify that:

1. Artifacts with expired signatures are rejected (if signature verification is enabled).
2. Artifacts with revoked aliases are rejected with an `artifact.alias.revoked` diagnostic.
3. Cache entries with outdated validation policies are rejected.

### Duplicate artifacts

The host MUST deduplicate artifacts by digest.
The test MUST verify that:

1. Loading the same artifact twice returns the same cached instance.
2. No duplicate entries are created in the registry.
3. Cache keys are deterministic for the same artifact.

### Boundary-limit inputs

The host MUST enforce limits on artifact size and manifest complexity.
The test MUST verify that:

1. Artifacts exceeding `artifact.max_bytes` are rejected with a
   `artifact.limit.max_bytes` diagnostic.
2. Manifests with excessive actions, routes, or schemas are rejected with a
   `artifact.limit.complexity` diagnostic.
3. Schemas with excessive nesting or field count are rejected.

### Timeout and cancellation

The host MUST enforce time limits during artifact validation.
The test MUST verify that:

1. Validation exceeding `time.artifact_validation_ms` is interrupted with a
   `artifact.timeout.validation` diagnostic.
2. Cancellation during artifact loading is handled gracefully.

### Unavailable dependencies

The host MUST handle missing artifacts or registry entries.
The test MUST verify that:

1. Lookups for non-existent digests are rejected with an
   `artifact.unavailable.not_found` diagnostic.
2. Lookups for non-existent aliases are rejected with an
   `artifact.unavailable.alias_not_found` diagnostic.
3. Registry failures are reported with an
   `artifact.unavailable.registry_error` diagnostic.

### Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.

## Variability register

| Clause | Type | Selection |
| --- | --- | --- |
| Artifact structure | Required | Wasm bytes + manifest + optional signatures |
| Digest algorithm | SHOULD | SHA-256; stronger algorithms MAY be used |
| Media types | Required | Fixed by this chapter |
| Build provenance | Required | Fields fixed by this chapter |
| Signature verification | SHOULD NOT | Provenance only; not a security mechanism |
| Manifest fields | Required | Fixed by this chapter |
| Action definition | Required | Fields fixed by this chapter |
| Route definition | Required | Fields fixed by this chapter |
| State schema definition | Required | Fields fixed by this chapter |
| Strategy definition | Required | Fields fixed by this chapter |
| Capability definition | Required | Fields fixed by this chapter |
| Migration definition | Required | Fields fixed by this chapter |
| Schema identifiers | Required | Format fixed by this chapter |
| Schema hashing | Required | Canonical JSON + SHA-256 |
| Schema ownership | Required | Fixed by this chapter |
| Schema compatibility | Required | Semantic versioning rules |
| Registry lookup | Required | Digest primary; aliases optional |
| Registry record | Required | Fields fixed by this chapter |
| Validation order | Required | 8-step order fixed by this chapter |
| Cache keys | Required | Components fixed by this chapter |
| Digest algorithm choice | Implementation-defined | Documented in conformance profile |
| Signature verification policy | Implementation-defined | Documented in conformance profile |
| Alias resolution strategy | Implementation-defined | Documented in conformance profile |
| Registry backend | Implementation-defined | Documented in conformance profile |
| Cache invalidation policy | Implementation-defined | Documented in conformance profile |
| Schema migration execution | Implementation-defined | Documented in conformance profile |
| Provenance storage | Implementation-defined | Documented in conformance profile |

## Rationale and evidence (non-normative)

This chapter derives from the artifact and manifest requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

Immutable artifacts are essential for:

- Reproducibility: same digest produces same behavior.
- Security: content-addressed verification prevents tampering.
- Provenance: build records enable audit and compliance.

Reviewable manifests are essential for:

- Transparency: capabilities and routes are visible before execution.
- Validation: host can verify compatibility without instantiation.
- Composition: manifests enable conflict detection at admission.

Schemas are essential for:

- Type safety: state structure is enforced at validation time.
- Migration: state upgrades are deterministic and reversible.
- Compatibility: schema versions enable smooth upgrades.

Registries are essential for:

- Resolution: artifacts are discoverable by digest or alias.
- Caching: compiled results are reused across invocations.
- Audit: registry records provide provenance and history.
