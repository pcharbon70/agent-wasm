---
title: "Stable Identities Versions Errors And Limits"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-01
  - phase-02
  - identity
  - version
  - error
  - limit
aliases:
  - "M1-P2 Stable Identities"
---

# Stable Identities Versions Errors And Limits

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-02-stable-identities-versions-errors-and-limits.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It defines values that remain stable across retries, storage, runtime families,
upgrades, and diagnostics.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
 integration tests in
 Section Integration Test Expectations
 and a passing cross-milestone fixture run recorded in
 the cross-milestone fixture regression test case within that section.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

## Identities

### Identity types

> **Normative definition.**
The following identity types are used throughout this profile.
Each identity has a canonical text representation, a generation ownership
rule, a uniqueness scope, and comparison rules.

- **Tenant:** The top-level isolation boundary.
  A tenant identifies a logical or organizational unit that owns or
  consumes agent services.
  Tenants are scoped to the host deployment.

- **Principal:** An identity with authority to invoke actions or receive
  signals.
  A principal may be a user, a service account, or another agent.
  Principals are scoped to a tenant.

- **Agent type:** A versioned definition of an agent's decision logic,
  state schema, and strategy.
  Agent types are scoped to a tenant and identified by a stable name plus
  version.

- **Agent instance:** A live execution context for a specific agent type.
  Agent instances are scoped to a tenant and identified by a unique
  identifier within the agent type.

- **Artifact:** An immutable, content-addressed bundle of plug-in bytes,
  manifest, schema, and provenance metadata.
  Artifacts are globally scoped and identified by their digest.

- **Invocation:** One turn of agent computation.
  Invocations are scoped to an agent instance and identified by a
  host-assigned monotonically increasing positive integer.

- **Initialization:** One calculation of initial state for a newly created
  agent instance. Initializations are scoped one-to-one to an agent instance.

- **Signal:** A versioned envelope carrying a causal record.
  Signals are scoped to a tenant and identified by the tuple of type, source,
  subject, correlation identifier, and canonical timestamp.

- **Directive:** A typed capability request emitted by initialization or a
  turn. Directives are scoped to their producing initialization or invocation
  and array position.

- **Attempt:** One execution of an effect handler for a directive.
  Attempts are scoped to a directive and identified by a monotonically
  increasing counter.

- **Trace:** A host-owned record of a turn's execution.
  Traces are scoped to an invocation and identified by the invocation
  identifier.

### Canonical text representations

> **Normative definition.**
Every identity has a canonical text representation for use in diagnostics,
audit logs, and durable storage.
The representation MUST be deterministic for the same identity value and
MUST NOT expose secrets or implementation-internal state.

| Identity type | Canonical form | Example |
| --- | --- | --- |
| Tenant | `tenant:<name>` | `tenant:acme-corp` |
| Principal | `principal:<tenant>/<name>` | `principal:acme-corp/svc-api` |
| Agent type | `agent:<tenant>/<name>:<version>` | `agent:acme-corp/chatbot:1.2.0` |
| Agent instance | `agent:<tenant>/<name>/u-<counter>` | `agent:acme-corp/chatbot/u-7` |
| Artifact | `artifact:<digest-algorithm>:<hex-digest>` | `artifact:sha256:a1b2c3d4...` |
| Invocation | `inv:<agent-instance>:<counter>` | `inv:agent:acme-corp/chatbot/u-7:9` |
| Initialization | `init:<agent-instance>` | `init:agent:acme-corp/chatbot/u-7` |
| Signal | `signal:sha256:<hex-digest>` | `signal:sha256:a1b2c3d4...` |
| Directive | `directive:<producer>:<kind>:<index>` | `directive:inv:agent:acme-corp/chatbot/u-7:9:effect:0` |
| Attempt | `attempt:<directive>:<counter>` | `attempt:directive:inv:agent:acme-corp/chatbot/u-7:9:effect:0:1` |
| Trace | `trace:<invocation>` | `trace:inv:agent:acme-corp/chatbot/u-7:9` |

### Generation ownership

> **Normative definition.**
Generation ownership determines which component is responsible for
creating each identity.

| Identity type | Generator | Storage | Rationale |
| --- | --- | --- | --- |
| Tenant | Host | Registry | Top-level boundary; host-owned |
| Principal | Host | Registry | Authority boundary; host-owned |
| Agent type | Host (from manifest) | Registry | Definition; host validates and stores |
| Agent instance | Host | Registry | Live context; host-owned |
| Artifact | Guest (then host) | Digest store | Guest produces; host verifies and indexes |
| Invocation | Host | Turn log | Turn orchestration; host-owned |
| Initialization | Host | Registry | Fresh-agent initialization; host-owned |
| Signal | Host (or external) | Signal bus | Ingress point; host validates and routes |
| Directive | Guest (via reducer) | Outbox | Decision output; host commits and drains |
| Attempt | Host (effect handler) | Effect log | Execution record; host-owned |
| Trace | Host | Audit log | Turn evidence; host-owned |

> **Normative definition.**
Tenant, principal, and agent-type names are admitted canonical input rather
than generated opaque identifiers. For each `(tenant, agent type)`, the host
MUST assign agent-instance counters as positive monotonically increasing
integers and MUST NOT reuse a counter. For each agent instance, invocation
counters use the same positive monotonic and non-reuse rule. Directive ids use
the producing initialization or invocation, kind, and zero-based array index;
attempt ids use a positive monotonically increasing per-directive counter;
trace identity is derived from invocation identity; artifact and signal
identities use their fixed digest and tuple derivations. An initialization
identity is derived from the canonical agent-instance identity and is created
exactly once for that instance.

The canonical signal identity is `signal:sha256:` followed by the lowercase
hexadecimal SHA-256 digest of canonical JSON encoding of
`[tenant_id, type, source, subject, correlation_id, timestamp]`. Hashing the
array avoids delimiter ambiguity among tuple components.

### Uniqueness scope

> **Normative definition.**
Uniqueness scope defines the namespace in which an identity must be unique.

| Identity type | Uniqueness scope | Enforcement point |
| --- | --- | --- |
| Tenant | Deployment | Host registry |
| Principal | Tenant | Host registry |
| Agent type | Tenant (name + version) | Host registry |
| Agent instance | Tenant (agent type + instance-id) | Host registry |
| Artifact | Global (digest) | Digest store |
| Invocation | Agent instance (counter) | Host turn manager |
| Initialization | Agent instance | Host registry |
| Signal | Tenant (type + source + subject + correlation + timestamp) | Signal bus |
| Directive | Producer identity (kind + index) | Host outbox |
| Attempt | Directive (counter) | Host effect handler |
| Trace | Invocation | Host audit log |

### Comparison rules

> **Normative definition.**
Identity comparison is lexical on the canonical text representation.
Comparison MUST be case-sensitive and MUST treat all characters equally.
Two identities are equal if and only if their canonical text representations
are byte-for-byte identical.

### Temporal identity

> **Normative definition.**
The following temporal types are used throughout this profile.

| Type | Representation | Example |
| --- | --- | --- |
| Timestamp | ISO 8601 UTC | `2026-08-10T12:34:56Z` |
| UnixTimestamp | ISO 8601 UTC | `2026-08-10T12:34:56Z` |

All temporal fields use ISO 8601 UTC format. The host MUST store timestamps
in UTC and MUST NOT include timezone offsets.

> **Normative definition.**

```
UnixTimestamp = string
```

## Versions

### Version fields

> **Normative definition.**
The following version fields are used throughout this profile.
All version fields use semantic versioning (MAJOR.MINOR.PATCH) unless
otherwise specified.

- **Protocol version:** Identifies the host--guest application protocol.
  Incremented for breaking changes to the reducer interface or message
  formats.

- **Manifest version:** Identifies the capability bundle schema.
  Incremented for breaking changes to manifest structure or semantics.

- **State-schema version:** Identifies the agent state schema.
  Incremented for breaking changes to state structure or required fields.

- **Strategy version:** Identifies the strategy implementation.
  Incremented for breaking changes to strategy behavior or snapshot schema.

- **Capability version:** Identifies a capability bundle.
  Incremented for breaking changes to capability interface or behavior.

- **Artifact version:** Identifies an artifact within its content-addressed
  identity.
  Artifacts are immutable; versioning applies to the manifest reference,
  not the artifact itself.

### Version compatibility rules

> **Normative definition.**
Version compatibility follows semantic versioning rules:

- **MAJOR** version increments indicate breaking changes.
  Implementations MUST reject inputs with a higher MAJOR version than
  supported.

- **MINOR** version increments indicate backward-compatible additions.
  Implementations MAY accept inputs with a higher MINOR version if the
  additions are optional and do not affect core behavior.

- **PATCH** version increments indicate backward-compatible bug fixes.
  Implementations MUST accept inputs with any PATCH version within the
  same MAJOR.MINOR range.

### Version negotiation

> **Normative definition.**
Version negotiation occurs at artifact admission and turn initiation.

1. The host queries the artifact's declared protocol version via
   `describe`.
2. The host compares the declared version against its supported range.
3. If incompatible, the host rejects the artifact with an
   `identity.version.incompatible` diagnostic.
4. If compatible, the host proceeds with the declared version.

## Errors

### Error categories

> **Normative definition.**
Errors are categorized by their root cause and failure domain.
Each error category has a stable family code and diagnostic template.

| Category | Family code | Description |
| --- | --- | --- |
| Decode | `identity.decode` | Input fails to parse or violates encoding rules |
| Validation | `identity.validation` | Input parses but violates structural or semantic rules |
| Compatibility | `identity.compatibility` | Artifact or input uses unsupported version or feature |
| Authorization | `identity.authorization` | Principal lacks authority for the requested operation |
| Conflict | `identity.conflict` | Manifest composition or state update detects conflict |
| Trap | `identity.trap` | Guest plug-in execution trapped or violated memory safety |
| Limit | `identity.limit` | A named implementation limit, including a duration ceiling, was exhausted |
| Cancellation | `identity.cancellation` | Turn or effect cancelled by host or principal |
| Resource | `identity.resource` | Runtime allocation or execution facility failed independently of a named limit |
| Storage | `identity.storage` | Durable state or journal operation failed |
| Effect | `identity.effect` | Effect handler execution failed or returned invalid result |

### Error structure

> **Normative definition.**
Every error diagnostic MUST contain:

1. A stable family code of the form `identity.<category>.<subcode>`.
2. The identity or identities involved in the error.
3. A human-readable description that does not expose secrets.
4. The phase or contract to which the error applies.
5. Optional remediation guidance.

Example:

> **Normative conformance example.**

```
{
  "family": "identity.compatibility.protocol_version",
  "agent_type": "agent:acme-corp/chatbot:1.2.0",
  "declared": "2.0.0",
  "supported": "1.0.0",
  "description": "Artifact declares protocol version 2.0.0, but host supports 1.0.0. MAJOR version mismatch.",
  "remediation": "Update host to support protocol 2.0.0 or use an artifact compatible with 1.0.0."
}
```

## Limits

### Limit categories

> **Normative definition.**
Limits bound resource consumption and prevent abuse.
Each limit has a stable identifier and a default value.
Hosts MAY configure a lower positive ceiling than a listed default, but MUST
NOT configure a higher ceiling for the base profile. The effective ceiling is
an implementation limit and MUST be disclosed in the conformance profile.

| Limit identifier | Scope | Default | Description |
| --- | --- | --- | --- |
| `input.max_bytes` | Turn request | 1 MiB | Maximum input size per turn |
| `output.max_bytes` | Turn result | 1 MiB | Maximum output size per turn |
| `state.max_bytes` | Agent state | 10 MiB | Maximum agent state size |
| `state.max_depth` | Nested state | 32 | Maximum nesting depth |
| `collection.max_items` | Arrays/objects | 1000 | Maximum items in collection |
| `string.max_length` | Strings | 1 MiB | Maximum string length |
| `memory.max_pages` | Wasm memory | 64 | Maximum Wasm memory pages (64 KiB each) |
| `time.turn_ms` | Turn duration | 5000 | Maximum turn duration in milliseconds |
| `time.host_function_ms` | Host function | 1000 | Maximum host function duration in milliseconds |
| `host_calls.max_count` | Guest invocation | 1000 | Maximum synchronous host-function calls per invocation |
| `diagnostic.max_bytes` | Diagnostic text | 4 KiB | Maximum diagnostic text size |
| `artifact.max_bytes` | Artifact bundle | 64 MiB | Maximum admitted artifact size |
| `manifest.max_actions` | Agent manifest | 256 | Maximum action descriptors |
| `manifest.max_routes` | Agent manifest | 256 | Maximum route declarations |
| `manifest.max_schemas` | Agent manifest | 64 | Maximum state-schema declarations |
| `schema.max_depth` | One schema | 32 | Maximum schema nesting depth |
| `schema.max_fields` | One schema | 1000 | Maximum declared schema fields |
| `time.artifact_validation_ms` | Artifact admission | 5000 | Maximum artifact-validation duration in milliseconds |

### Limit enforcement

> **Normative definition.**
Limits are enforced at the host boundary.
Exceeding a limit is NOT ordinary invalidity; the input would otherwise
conform.
The host MUST reject the operation with a
`identity.limit.<limit_identifier>` diagnostic and disclose the relevant
limit in the implementation profile.

### Limit identifiers in diagnostics

> **Normative definition.**
When a limit is exceeded, the diagnostic MUST include:

1. The limit identifier that was exceeded.
2. The declared or configured value of the limit.
3. The actual value that exceeded the limit (if available).
4. The identity or context in which the limit was checked.

## Compatibility diagnostics

### Unknown fields

> **Normative definition.**
Unknown fields in authoritative structures (turn requests, turn results,
directives) are rejected by default.
Silent fallback is unsafe for authority-bearing requests.

The host MUST reject unknown fields in authoritative structures. A later
versioned protocol MAY define an explicit non-authoritative extension point;
that permission does not apply to any other structure or field.

### Unknown versions

> **Normative definition.**
Unknown versions in version fields (protocol, manifest, state-schema, etc.)
are treated as compatibility errors.
The host MUST reject the input with an
`identity.compatibility.unknown_version` diagnostic.

### Deprecation

> **Normative definition.**
Deprecated features MAY be accepted with a warning diagnostic.
The warning MUST:

1. Identify the deprecated feature and its replacement.
2. State the deadline after which the feature will be rejected.
3. Include the `identity.deprecated` family code.

Deprecated features MUST NOT be used in new artifacts or manifests.
Hosts SHOULD notify artifact publishers of upcoming deprecations.

## Fixed choices, implementation limits, and deferred work

### Fixed choices and internal mechanisms

Initialization, invocation, directive, attempt, artifact, and trace identities
use the fixed generation and derivation rules in this chapter and their
governing protocol chapters. Unknown authoritative fields are rejected. Diagnostic redaction is
governed by
[Diagnostic recording policy](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md#diagnostic-recording-policy).

Trace retention and outbox storage are internal mechanisms. They MAY vary only
when identity, required durability, availability, protocol output, and failure
diagnostics remain identical. Relevant retention and configured limit ceilings
MUST be disclosed in the conformance profile.

### Deferred work

| Item | Target | Reason |
| --- | --- | --- |
| Cross-tenant identity isolation | Milestone 5 | Requires tenancy and security model |
| Principal delegation | Milestone 6 | Requires multi-agent coordination |
| Limit override via policy | Milestone 5 | Requires capability and policy model |
| Deprecation lifecycle automation | Milestone 9 | Requires production platform and tooling |
| Identity revocation | Milestone 5 | Requires security and tenancy model |
| Cross-runtime identity equivalence | Milestone 8 | Requires portability and verification; depends on JavaScript and Chicory runtime conformance deferred in [Profile Vocabulary](01-profile-vocabulary-and-architectural-boundaries.md) |

> **Non-normative note.**
> All items deferred to Milestone 8 fall under
> Milestone 8 - Portability, Verification, And Performance
> (planning document at `.spec/planning/agentic-system/milestone-08-portability-verification-and-performance/README.md`).
> The Milestone 8 boundary principle: Milestone 8 addresses portability,
> verification, and performance of the system as built by Milestones 1-7.
> Milestone 9 addresses production platform, developer experience, and
> operational tooling built on top of that verified system.

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter:

1. Canonical text representations collide across runtime families due to
   encoding differences.
2. Semantic versioning is insufficient for the required version negotiation
   granularity.
3. Limit defaults are too restrictive or too permissive for target workloads,
   requiring dynamic limit computation.
4. Unknown field rejection breaks critical backward compatibility without
   acceptable migration path.
5. Identity generation strategy cannot produce unique identifiers at the
   required scale or throughput.

## Integration Test Expectations

This section defines the observable behavior that the Phase 2 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### Successful flow

The host MUST generate stable identities for all components of a successful
turn and emit diagnostics with correct family codes and structures.
The test MUST verify that:

1. Each identity type is generated according to its generation ownership
   rule.
2. Canonical text representations are deterministic and follow the
   specified format.
3. Signal and delivery identities use the same SHA-256 tuple digest with their
   respective canonical prefixes.
4. Version negotiation succeeds for compatible artifacts.
5. Diagnostics include all required fields (family code, identities,
   description, phase, optional remediation).
6. Limit identifiers are included in limit-exceeded diagnostics.

### Malformed identity inputs

The host MUST reject inputs with malformed identities.
The test MUST verify that:

1. Invalid canonical forms are rejected with an
   `identity.decode.invalid_format` diagnostic.
2. Missing required identity fields are rejected with an
   `identity.validation.missing_field` diagnostic.
3. Duplicate identities in the same scope are rejected with an
   `identity.conflict.duplicate` diagnostic.

### Incompatible versions

The host MUST reject artifacts with incompatible versions.
The test MUST verify that:

1. Artifacts with higher MAJOR versions are rejected with an
   `identity.compatibility.protocol_version` diagnostic.
2. Artifacts with unknown version fields are rejected with an
   `identity.compatibility.unknown_version` diagnostic.
3. Artifacts using deprecated features emit warnings (if accepted) and
   include the `identity.deprecated` family code.

### Stale identities

The host MUST detect and reject stale or outdated identities.
The test MUST verify that:

1. Invocations with out-of-order counters are rejected.
2. Artifacts with expired digests are rejected.
3. Signals older than the fixed TTL are rejected with
   `signal.expired.timestamp_too_old`, while a signal exactly at the boundary
   remains eligible for acceptance.

### Duplicate identities

The host MUST deduplicate identities according to their uniqueness scope.
The test MUST verify that:

1. Duplicate signals with the same tenant, type, source, subject, correlation
   identifier, and canonical timestamp are identified.
2. Duplicate invocations with the same counter are rejected.
3. No duplicate state revisions are created.

### Boundary-limit inputs

The host MUST enforce limits and emit limit diagnostics.
The test MUST verify that:

1. Inputs exceeding `input.max_bytes` are rejected with a
   `identity.limit.input.max_bytes` diagnostic.
2. Outputs exceeding `output.max_bytes` are rejected with the corresponding
   `identity.limit.output.max_bytes` diagnostic.
3. Nested structures exceeding `state.max_depth` are rejected with
   `identity.limit.state.max_depth`.
4. Collections exceeding `collection.max_items` are rejected with
   `identity.limit.collection.max_items`.
5. Strings exceeding `string.max_length` are rejected with
   `identity.limit.string.max_length`.
6. Memory exceeding `memory.max_pages` is rejected with
   `identity.limit.memory.max_pages`.
7. Turns exceeding `time.turn_ms` are rejected with an
   `identity.limit.time.turn_ms` diagnostic.

### Timeout and cancellation

The host MUST enforce time limits and support cancellation.
The test MUST verify that:

1. Turns exceeding `time.turn_ms` are interrupted and emit a
   `identity.limit.time.turn_ms` diagnostic.
2. Cancellation signals interrupt in-progress turns and emit an
   `identity.cancellation.requested` diagnostic.
3. No partial state is committed for timed-out or cancelled turns.

### Resource exhaustion

The host MUST detect and report resource exhaustion.
The test MUST verify that:

1. Heap allocation failures are reported with an
   `identity.resource.heap_exhausted` diagnostic.
2. Call depth limits are enforced with an
   `identity.resource.depth_exceeded` diagnostic.
3. Storage failures are reported with an
   `identity.storage.write_failed` diagnostic.

### Effect failures

The host MUST handle effect handler failures gracefully.
The test MUST verify that:

1. Effect handlers that trap are reported with an
   `identity.effect.trap` diagnostic.
2. Effect handlers that return invalid results are reported with an
   `identity.effect.invalid_result` diagnostic.
3. Retry logic respects idempotency keys and does not create duplicate
   external delivery.

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
| Identity types | Required | Fixed by this chapter, including initialization identity. |
| Canonical representations | Required | Format and rules fixed by this chapter. |
| Generation ownership | Required | Fixed by this chapter. |
| Uniqueness scope | Required | Fixed by this chapter. |
| Comparison rules | Required | Lexical on canonical form. |
| Version fields | Required | Semantic versioning for all fields. |
| Version compatibility | Required | MAJOR break, MINOR additive, PATCH fix. |
| Error categories | Required | 11 categories fixed by this chapter. |
| Limit categories | Required | 18 named limits fixed by this chapter. |
| [Configured limit ceilings](#limit-categories) | Implementation limit | Defaults are fixed; lower positive ceilings are disclosed in the conformance profile. |
| Unknown field policy | Required | Reject for authoritative structures; only explicit versioned non-authoritative extension points may differ. |
| Higher MINOR versions | MAY | Accept only when additions are optional and do not affect core behavior. |
| Deprecated features | MAY | Accepted uses emit the fixed warning diagnostic. |
| Deprecation notification | SHOULD | Notify publishers of upcoming deprecations. |
| [Trace and outbox mechanisms](#fixed-choices-and-internal-mechanisms) | MAY (internal) | Variation cannot change identity, durability, output, or failure behavior. |

## Rationale and evidence (non-normative)

This chapter derives from the identity and versioning requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

Stable identities are essential for:

- Audit and provenance: traceable records of who did what and when.
- Diagnostics: precise error reporting without ambiguity.
- Durability: identity persistence across host restarts and upgrades.
- Coordination: causal tracking across multi-agent workflows.

Versioning is essential for:

- Backward compatibility: smooth upgrades without breaking existing agents.
- Feature evolution: additive changes without version bumps.
- Deprecation: graceful retirement of outdated features.

Limit enforcement is essential for:

- Resource governance: prevent abuse and ensure fair sharing.
- Predictability: bounded resource consumption for SLA compliance.
- Security: prevent denial-of-service via resource exhaustion.
