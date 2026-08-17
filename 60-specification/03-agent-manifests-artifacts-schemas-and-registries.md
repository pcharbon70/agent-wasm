---
title: "Agent Manifests Artifacts Schemas And Registries"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-01
  - phase-03
  - artifact
  - manifest
  - schema
  - registry
  - model-requirements
aliases:
  - "M1-P3 Manifests And Artifacts"
---

# Agent Manifests Artifacts Schemas And Registries

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-03-agent-manifests-artifacts-schemas-and-registries.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It defines immutable executable artifacts and reviewable manifests that can
be resolved without instantiating guest code.

Version `1.0.0` replaces the `0.2.0` manifest contract. It unifies action
metadata in one `ActionDescriptor` and retains logical model requirements and
model-slot declarations; concrete providers, models, endpoints, connections,
and credentials remain deployment configuration and are not artifact
declarations.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
 integration tests in
 Section Integration Test Expectations
 and a passing cross-milestone fixture run recorded in
 the cross-milestone fixture regression test case within that section.

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
digest_manifest = remove_fields(
  manifest_json,
  ["artifact_digest", "provenance.signatures"]
)
canonical = concatenate_length_prefixed(
  utf8("agent-wasm-artifact-v1"),
  utf8("sha256"),
  canonical_json(digest_manifest),
  for each module in ascending UTF-8 name order:
    utf8(module.name),
    module.bytes
)
digest = SHA-256(canonical)
artifact_digest = "artifact:sha256:" + lowercase_hex(digest)
```

Every component in `concatenate_length_prefixed` is preceded by its unsigned
64-bit big-endian byte length. The module name participates in the preimage.
`canonical_json` is defined by
[Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).

The base profile MUST use SHA-256. `artifact_digest` and signature references
are excluded from the digest preimage so digest and signature calculation are
not self-referential. They remain admission metadata bound to the calculated
digest. An explicit versioned extension is required for another digest
algorithm or preimage format.

### Artifact digests

Artifact digests use the following format:

> **Normative definition.**

```
artifact:<algorithm>:<hex-digest>
```

Examples:

- `artifact:sha256:a1b2c3d4e5f6...`

The digest algorithm MUST be `sha256` for the base profile and MUST be used for
all digest comparisons.

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
The following provenance fields MUST be present:

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

Signature references identify cryptographic signatures over the calculated
artifact digest bytes.
The host MUST verify every supplied signature at admission time. An unsigned
artifact remains structurally valid unless an explicit admission policy
requires a signature. An unsupported signature algorithm is incompatible and
a failed signature is invalid; neither case may admit the artifact.

Signature reference structure:

> **Normative definition.**

```
{
  "algorithm": "ed25519 | rsa-pss | ecdsa-p256",
  "key_id": "string",
  "signature": "base64-encoded",
  "timestamp": "ISO 8601",
  "expires_at": "ISO 8601 | null"
}
```

`timestamp` is the canonical signing time and MUST NOT be later than artifact
admission time. When `expires_at` is non-null, it MUST be later than
`timestamp`; admission at or after `expires_at` MUST reject the artifact with
`artifact.signature.expired`. A null `expires_at` means the signature has no
metadata expiry. Key revocation and trust policy may still reject a
cryptographically valid unexpired signature, but MUST NOT classify it as
expired.

Signature verification establishes artifact integrity and publisher-key
provenance only. It MUST NOT by itself authorize capabilities, establish
publisher trust, or replace policy admission.

## AgentManifest

### Manifest fields

The `AgentManifest` describes an artifact's capabilities and MUST accompany
all artifacts.
The following fields MUST be present:

| Field | Type | Description |
| --- | --- | --- |
| `artifact_digest` | `artifact:sha256:<hex>` | Digest of this artifact |
| `protocol_version` | `string` | Host--guest protocol version |
| `manifest_version` | `string` | Manifest schema version |
| `name` | `string` | Human-readable artifact name |
| `version` | `string` | Semantic version of this artifact |
| `publisher` | `string` | Publisher identity |
| `description` | `string` | Human-readable description |
| `actions` | `ActionDescriptor[]` | Exported action contracts |
| `routes` | `Route[]` | Declared routes |
| `state_schemas` | `StateSchema[]` | Declared state schemas |
| `strategies` | `Strategy[]` | Declared strategies |
| `model_requirements` | `ModelRequirement[]` | Logical model slots and portable capability requirements |
| `required_capabilities` | `Capability[]` | Required host capabilities |
| `required_features` | `string[]` | Required Wasm features beyond Core 3.0 |
| `migrations` | `Migration[]` | State migration definitions |
| `provenance` | `Provenance` | Build provenance record |

For this contract, `manifest_version` and `protocol_version` MUST both be
`1.0.0`. Other versions require successful compatibility negotiation before
the manifest is admitted.

### Action descriptor

An action descriptor is the single manifest representation of a named
operation. Chapter 11 imports this type directly and does not define a second
action representation.

> **Normative definition.**

```
ActionDescriptor {
  name: string,
  version: string,
  description: string,
  input_schema: SchemaRef?,
  output_schema: SchemaRef?,
  state_access: StateAccess,
  directive_kinds: DirectiveKind[],
  required_grants: GrantRef[],
  deterministic: bool,
  timeout_ms: int?,
  handler: {
    kind: "reducer" | "host_function",
    entry: string
  }
}

StateAccess {
  read: string[],
  write: string[],
  delete: string[]
}

DirectiveKind {
  type: string,
  required_capabilities: CapabilityRef[]
}

CapabilityRef {
  name: string,
  version: string?
}

GrantRef {
  principal: string?,
  capability: CapabilityRef,
  resource: string?,
  conditions: JsonObject?
}
```

Every field is required except fields marked nullable. `deterministic` MUST be
`true` in the base profile. `timeout_ms`, when present, MUST be positive and
MUST NOT exceed `time.turn_ms`. Every `StateAccess` entry is an exact canonical
JSON Pointer under Chapter 12; wildcards and implementation-specific path
languages are invalid. Every `DirectiveKind.type` MUST be one of Chapter 13's
six directive kinds. Actions are resolved by the host; guest code does not
invoke actions directly.

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
  terminal_states: string[],
  model_slots: string[]
}
> **Normative definition.**

```

Strategies are implemented as plug-in reducer exports.
The host invokes strategies via the `reduce` export.
Every value in `model_slots` MUST identify one entry in the manifest's
`model_requirements` field.
An empty list declares that the strategy does not request model access.

### Model requirement definition

A model requirement declares what an agent needs from a model without
selecting a vendor or credential-bearing connection.

> **Normative definition.**

```
ModelRequirement {
  slot_id: string,
  description: string,
  required_features: ModelFeature[],
  min_context_tokens: u64,
  min_output_tokens: u64,
  optional: bool
}

ModelFeature = "text-generation" | "streaming" | "tool-calling" |
               "structured-output"
```

The `slot_id` values MUST be unique within the manifest.
The manifest MUST NOT place a concrete provider, model identifier, adapter,
endpoint, connection identifier, authentication header, secret, or credential
handle in a model requirement or any other model-selection field.
The end user binds each required slot to a compatible model connection under
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md).
An optional requirement MAY remain unbound, but an attempt to use its slot
while unbound fails at runtime.
An artifact with a non-empty `model_requirements` field MUST include
`ModelAccess` in `required_capabilities`. An untrusted guest artifact MUST NOT
request `CredentialUse`, `SecretRead`, or `SecretWrite`; authenticated effect
workers receive any use-only authority independently at dispatch.

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

Migrations are orchestrated by the host during state upgrades. After separate
maintenance authorization, the host invokes the artifact's pure `migrate`
export, validates its `MigrationResult`, and atomically commits or rejects the
candidate state. Guest code computes the candidate transformation but never
authorizes or commits a migration.

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

Schema hashes are computed over the
[Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).

> **Normative definition.**

```
schema_hash = lowercase_hex(SHA-256(canonical_json(schema)))
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
3. **Signature verification:** Validate signing and expiry timestamps and
   verify every supplied signature; missing signatures are acceptable unless
   explicit admission policy requires one, but unsupported, expired, or failed
   signatures are a rejection.
4. **Feature profile:** Check required Wasm features against host support.
5. **Manifest structure:** Validate manifest JSON schema and field types.
6. **Manifest compatibility:** Check version fields against host supported range.
7. **Schema validation:** Validate state and snapshot schemas.
8. **Policy admission:** Check host policy (allowlist, capability grants).

Rejection at any step HALTS further validation.
Partial validation results are NOT committed.

### Artifact admission limits

Artifact admission uses the named defaults in
[Limit categories](02-stable-identities-versions-errors-and-limits.md#limit-categories):
`artifact.max_bytes`, `manifest.max_actions`, `manifest.max_routes`,
`manifest.max_schemas`, `schema.max_depth`, `schema.max_fields`, and
`time.artifact_validation_ms`. A host may configure only a lower positive
ceiling under the governing implementation-limit rule. Exhaustion MUST use
`identity.limit.<limit_identifier>`.

### Cache keys

Compiled artifact cache keys include:

> **Normative definition.**

```
cache_key = lowercase_hex(SHA-256(canonical_json([
  runtime_family,
  runtime_version,
  target_arch,
  target_features,
  artifact_digest,
  validation_policy
])))
```

Cache entries are invalidated when:

- The artifact digest changes.
- The runtime family or version changes.
- The target architecture or features change.
- The validation policy changes.

Cache hits MUST be verified against the current validation policy before use.

## Fixed choices, internal mechanisms, and deferred work

### Fixed choices and internal mechanisms

The base artifact digest is the SHA-256 construction in
[Artifact structure](#artifact-structure). Every supplied signature is
verified. An alias MUST resolve to exactly one currently approved digest;
missing, expired, revoked, or ambiguous aliases are rejected. Cache entries
are invalidated only by the fixed triggers in [Cache keys](#cache-keys); a
time-based cache eviction MAY discard an entry but MUST NOT change admission
or resolution results.

Registry, cache, and provenance-storage backends are internal mechanisms and
MAY vary only when canonical bytes, alias results, admission order,
availability guarantees, and diagnostics are identical. Migration execution
uses the authorized guest calculation and host-owned atomic validation and
commit defined in [Migration definition](#migration-definition).

### Deferred work

| Item | Target | Reason |
| --- | --- | --- |
| Registry replication | Milestone 9 | Requires production platform and deployment |
| Schema migration UI | Milestone 9 | Requires developer experience and tooling |
| Artifact dependency resolution | Milestone 5 | Requires capability and plugin system |
| Registry access control | Milestone 5 | Requires security and tenancy model |
| Schema evolution tooling | Milestone 7 | Requires AI tools and memory |
| Artifact compression | Milestone 8 | Requires portability and performance; complements compression for large payloads in [Turn Lifecycle](04-turn-lifecycle-protocols-and-canonical-encoding.md) and large-state runtime memory in [Memory64 support](01-profile-vocabulary-and-architectural-boundaries.md) |

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter:

1. Canonical JSON representation is insufficient for large schemas; binary
    encoding is required for performance; addressed by Binary encoding deferred to
    [Milestone 8](04-turn-lifecycle-protocols-and-canonical-encoding.md) (Binary encoding row).
2. SHA-256 digest collisions are demonstrated at scale; a versioned digest
   extension is required.
3. Alias resolution introduces ambiguity; digest-only lookup is required.
4. Schema migration execution is too complex for host; requires additional guest
    cooperation.

> **Non-normative note.**
> All items deferred to Milestone 8 fall under
> Milestone 8 - Portability, Verification, And Performance
> (planning document at `.spec/planning/agentic-system/milestone-08-portability-verification-and-performance/README.md`).
> The Milestone 8 boundary principle: Milestone 8 addresses portability,
> verification, and performance of the system as built by Milestones 1-7.
> Milestone 9 addresses production platform, developer experience, and
> operational tooling built on top of that verified system.

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
   Replacing only `artifact_digest` or signature references MUST NOT change the
   digest preimage; changing any included manifest field, module name, or module
   byte MUST change the calculated digest.
2. Manifests are validated for structure, compatibility, and policy.
3. Schemas are validated for field types, initial state, and migrations.
4. Cache keys are computed correctly and cache hits are verified.
5. Provenance records are recorded and retained.
6. Every model slot is unique, portable, and free of concrete provider,
   endpoint, or credential material.
7. Every supplied signature is verified and any unsupported or invalid
   signature rejects admission. A signature with non-null `expires_at` is
   accepted strictly before that instant and rejected at or after it.

### Malformed artifacts

The host MUST reject artifacts with malformed bytes or manifests.
The test MUST verify that:

1. Invalid Wasm bytes are rejected with an `artifact.bytes.malformed` diagnostic.
2. Invalid manifest JSON is rejected with an `artifact.manifest.malformed` diagnostic.
3. Missing required manifest fields are rejected with an `artifact.manifest.missing_field` diagnostic.
4. Digest mismatches are rejected with an `artifact.digest.mismatch` diagnostic.
5. Concrete provider, model, endpoint, authentication, or credential fields in
   a model requirement are rejected with an
   `artifact.manifest.forbidden_model_selection` diagnostic.

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

1. Artifacts admitted at or after a non-null signature `expires_at` are
   rejected with `artifact.signature.expired`; a null `expires_at` is not
   expired by age alone.
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

1. Artifacts exceeding `artifact.max_bytes` are rejected with
   `identity.limit.artifact.max_bytes`.
2. Manifests exceeding the action, route, or schema ceilings are rejected with
   `identity.limit.manifest.max_actions`,
   `identity.limit.manifest.max_routes`, or
   `identity.limit.manifest.max_schemas`, respectively.
3. Schemas exceeding the nesting or field ceilings are rejected with
   `identity.limit.schema.max_depth` or `identity.limit.schema.max_fields`.

### Timeout and cancellation

The host MUST enforce time limits during artifact validation.
The test MUST verify that:

1. Validation exceeding `time.artifact_validation_ms` is interrupted with
   `identity.limit.time.artifact_validation_ms`.
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

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
| --- | --- | --- |
| Artifact structure | Required | Wasm bytes + manifest + optional signatures |
| Digest algorithm | Required | SHA-256 with the fixed length-prefixed preimage |
| Media types | Required | Fixed by this chapter |
| Build provenance | Required | Fields fixed by this chapter |
| [Optional provenance fields](#build-provenance) | MAY | Builder, dependency, and signature metadata may accompany required provenance |
| Signature verification | Required when supplied | Every supplied signature is verified; unsigned artifacts require no signature absent explicit policy |
| [Signature metadata expiry](#signature-references) | MAY per signature | Null never expires by age; non-null expires exactly at `expires_at` |
| Manifest fields | Required | Fixed by this chapter |
| Action descriptor | Required | Single manifest type imported by Chapter 11; fields fixed by this chapter |
| Route definition | Required | Fields fixed by this chapter |
| State schema definition | Required | Fields fixed by this chapter |
| Strategy definition | Required | Fields fixed by this chapter |
| Model requirement definition | Required | Logical slots and portable feature constraints; concrete selection prohibited |
| [Optional model requirements](#model-requirement-definition) | MAY | Optional slots may remain unbound but fail if used while unbound |
| Capability definition | Required | Fields fixed by this chapter |
| Migration definition | Required | Fields fixed by this chapter |
| Schema identifiers | Required | Format fixed by this chapter |
| Schema hashing | Required | Canonical JSON + SHA-256 |
| Schema ownership | Required | Fixed by this chapter |
| Schema compatibility | Required | Semantic versioning rules |
| [Higher MINOR schema versions](#schema-compatibility) | MAY | Accept only optional additions |
| Registry lookup | Required | Digest primary; aliases optional |
| [Alias expiration and revocation](#registry-lookup) | MAY | Registry owners may expire or revoke aliases without changing digest identity |
| Registry record | Required | Fields fixed by this chapter |
| Validation order | Required | 8-step order fixed by this chapter |
| [Artifact admission limits](#artifact-admission-limits) | Implementation limits | Fixed defaults; only lower positive disclosed ceilings are permitted |
| Cache keys | Required | Components fixed by this chapter |
| [Digest construction](#artifact-structure) | Required | SHA-256 over the fixed non-self-referential preimage |
| [Signature verification](#signature-references) | Required when supplied | Unsupported or failed signatures reject admission |
| [Alias resolution](#registry-lookup) | Required | Resolve to exactly one approved digest or reject |
| [Registry, cache, and provenance backends](#fixed-choices-and-internal-mechanisms) | MAY (internal) | Observable admission and resolution behavior remains identical |
| [Cache invalidation](#cache-keys) | Required | Fixed semantic triggers; time-based eviction may only discard reusable work |
| [Schema migration execution](#migration-definition) | Required | Authorized guest calculation followed by host validation and atomic commit |

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
