---
title: "State Operations Patches Revisions And Conflicts"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-02
  - phase-03
  - state
  - operation
  - patch
  - revision
  - conflict
aliases:
  - "M2-P3 State Operations"
---

# State Operations Patches Revisions And Conflicts

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/phase-03-state-operations-patches-revisions-and-conflicts.md)
of
[Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/README.md)
--
Signals, Actions, State, And Strategies.
It defines safe internal state transitions against host-owned snapshots
and optimistic revisions.

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
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md).

## 3.1 Contract And Data Model

### Patch and StateOperation

> **Normative definition.**
This chapter defines the internal patch model used by the host for atomic
state application with revision tracking and precondition enforcement.
It converts from the wire format `StatePatch` defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#state-patch)
before application.

### StateOperation

> **Normative definition.**
A state operation is a deterministic mutation or observation of agent state
within a turn. The containing patch identity supplies duplicate suppression;
individual operations such as `append` and `increment` are not idempotent.
Each operation acts on a canonical path and carries an optional precondition
for optimistic concurrency control.

> **Normative definition.**
Only the following operation kinds are specified; their deterministic semantics
MUST be explicit.

- **replace**: Replace the complete state object. Valid only at the root path.
- **set**: Write a value at a path. Overwrites any existing value.
- **delete**: Remove a value at a path. No-op if path does not exist.
- **merge**: Merge a partial object into an existing object at a path.
- **append**: Append a value to an array at a path.
- **increment**: Add a numeric delta to a numeric value at a path.
- **test**: Verify a precondition without modifying state. Fails if precondition not met. Unlike other operations, `test` does not carry a `value` field and is used purely for precondition checking without side effects.

> **Normative definition.**

```
StateOperation {
  type: "replace" | "set" | "delete" | "merge" | "append" | "increment" | "test",
  path: CanonicalPath,
  value: JsonValue?,
  delta: number?,
  precondition: Precondition?,
  schema_version: string?
}

CanonicalPath = string

Precondition {
  type: "exists" | "not_exists" | "version_matches",
  expected: JsonValue?,
  message: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `type` | string | Yes | Operation kind |
| `path` | CanonicalPath | Yes | Target canonical JSON Pointer |
| `value` | JsonValue? | Conditional | Value to replace/set/merge/append |
| `delta` | number? | Conditional | Numeric delta for increment |
| `precondition` | Precondition? | No | Optimistic concurrency check |
| `schema_version` | string? | No | Expected state schema version |

### Patch

> **Normative definition.**
A patch is an ordered sequence of state operations applied atomically
within a turn.
Every patch MUST name its expected base revision and optional state-schema version
to enable optimistic concurrency control.

> **Normative definition.**

```
Patch {
  id: string,
  base_revision: int,
  state_schema_version: string?,
  operations: StateOperation[],
  created_at: UnixTimestamp,
  producer_id: string,
  authorized_principal: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Patch identifier |
| `base_revision` | int | Yes | Expected revision sequence number before patch |
| `state_schema_version` | string? | No | Expected state schema version |
| `operations` | StateOperation[] | Yes | Ordered sequence of operations |
| `created_at` | timestamp | Yes | Patch creation timestamp |
| `producer_id` | string | Yes | Producing invocation or maintenance-request identity |
| `authorized_principal` | string? | Yes | Accepted-ingress principal; null only for host-generated work |

When converting a reducer-produced wire `StatePatch` to this internal `Patch`,
the host MUST set `base_revision` to the integer
`TurnRequest.agent.expected_state_revision`, set `state_schema_version` from
the admitted reducer descriptor, set `created_at` from the input signal's
canonical timestamp, set `producer_id` to the producing invocation id, and set
`authorized_principal` from the persisted accepted-ingress principal.

The wire fields convert to operations in the Chapter 04 application order:

1. A non-null `replace` produces one `replace` operation at root path `""` and
   no other operation.
2. Otherwise, each `delete` JSON Pointer produces one `delete` operation in
   array order.
3. A non-null `merge` produces one `merge` operation at root path `""`.
4. Each `set` entry produces one `set` operation in array order.

`append`, `increment`, and `test` are available only to separately authorized
host maintenance requests in protocol `1.0.0`; no reducer wire field silently
maps to them. The canonical patch id is:

> **Normative definition.**

```
patch_id = "patch:sha256:" + lowercase_hex(SHA-256(canonical_json([
  base_revision,
  state_schema_version,
  operations,
  created_at,
  producer_id,
  authorized_principal
])))
```

The patch's `id` MUST equal `patch_id`. The id is excluded from its own
preimage. Host-originated maintenance patches use the maintenance-request
identity for `producer_id`, the authenticated caller for
`authorized_principal`, and the admitted maintenance-request timestamp for
`created_at`, then use the same id construction.

### Path constraints

> **Normative definition.**
Canonical paths are JSON Pointers. The root path is the empty string. A
non-root path MUST begin with `/`; `~` and `/` within a segment MUST use the
RFC 6901 escapes `~0` and `~1`, and every other `~` escape is invalid. Paths
MUST NOT exceed 1000 Unicode scalar values or 50 decoded segments. The root is
valid only for `replace` and `merge`.

| Constraint | Limit | Purpose |
|------------|-------|---------|
| Maximum path length | 1000 characters | Prevent path explosion |
| Escape syntax | RFC 6901 `~0` and `~1` only | Ensure one canonical path spelling |
| Minimum segments | 0 (root) | Root is restricted to replace and merge |
| Maximum segments | 50 | Prevent deep nesting |

### Namespace ownership

> **Normative definition.**
The first decoded JSON Pointer segment selects a namespace only when it is
`user` or `config`; every other path, including `/counter`, belongs to the
default `agent` namespace. The host MUST authorize the namespace against the
accepted `authorized_principal`, the producing action's `state_access`, and
the turn grants before commit. `producer_id` is provenance and MUST NOT be used
as the caller principal.

The following namespace ownership rules apply by default:

| Namespace | Authorized principal | Description |
|-----------|---------------------|-------------|
| `agent` (default) | Host commit pipeline after action/grant validation | Agent-owned internal state |
| `user` | Authenticated user principal | User-owned data |
| `config` | Separately authorized host maintenance principal | Agent configuration |

> **Normative definition.**
Implementations MAY define additional namespaces.
Every additional namespace MUST have one documented authorized principal class
and MUST use the same precommit ownership enforcement as the default
namespaces.
The `Unauthorized` diagnostic family applies when a patch targets a namespace
not authorized for the accepted principal, action, and grants. A null
`authorized_principal` is valid only for host-generated work and never
authorizes the `user` namespace.

### Patch-size limits

> **Normative definition.**
Patches are subject to the following size limits:

- Maximum operations per patch: 100
- Maximum patch size: 64 KiB
- Maximum value size per operation: 16 KiB
- Maximum path depth: 50 segments

| Limit | Value | Purpose |
|-------|-------|---------|
| Max operations/patch | 100 | Prevent oversized patches |
| Max patch size | 64 KiB | Bound memory usage |
| Max value size | 16 KiB | Prevent single-value abuse |
| Max path depth | 50 segments | Prevent deep nesting |

### Revision

> **Normative definition.**
A revision is a monotonically increasing, cryptographically-verifiable state snapshot
identifier.
Each revision captures the complete agent state at a point in time and enables
optimistic concurrency control.

> **Normative definition.**

```
Revision {
  id: string,
  sequence_number: int,
  state_hash: string,
  timestamp: UnixTimestamp,
  previous_revision: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Revision identifier (hash) |
| `sequence_number` | int | Yes | Monotonic sequence number |
| `state_hash` | string | Yes | Cryptographic hash of state |
| `timestamp` | UnixTimestamp | Yes | Revision creation timestamp |
| `previous_revision` | string? | Yes | Parent revision ID; null for initialization |

## 3.2 Behavior And Integration

### Patch validation

> **Normative definition.**
The host MUST validate patches in the following order before application:

1. **Size check**: Verify patch size does not exceed limits.
2. **Structure validation**: Verify patch structure conforms to the Patch schema.
3. **Schema check**: Verify `state_schema_version` matches if provided.
4. **Revision check**: Verify the patch's `base_revision` matches the current
   revision sequence number.
5. **Operation validation**: Verify each operation's type, path, and value.
6. **Precondition check**: Verify each operation's precondition against current state.

> **Normative definition.**
If validation fails at any step, the host MUST reject the patch with a diagnostic
identifying the failed step and the reason.

### Patch application

> **Normative definition.**
Upon successful validation, the host MUST apply patch operations in order:

1. Capture before-state snapshot for evidence.
2. Apply each operation sequentially.
3. Compute after-state hash.
4. Generate new revision with incremented sequence number.
5. Emit before/after state evidence.
6. Update current state revision.

> **Normative definition.**
Operations MUST be applied atomically; partial application is not permitted.
If an operation fails mid-application, the host MUST rollback to before-state.

### Next-revision calculation

> **Normative definition.**
The host MUST calculate the next revision as follows:

- `sequence_number` = current_sequence_number + 1
- `state_hash` = SHA-256(canonical_json(current_state))
- `timestamp` = current_timestamp
- `previous_revision` = current_revision_id
- `id` = SHA-256(canonical_json([sequence_number, state_hash, previous_revision]))

`canonical_json` is defined by
[Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).
SHA-256 digest bytes MUST be represented as lowercase hexadecimal.

### State initialization

> **Normative definition.**
The host MUST support full-snapshot initialization for new agents:

1. Accept a complete state object as initial value.
2. Compute initial state hash.
3. Create initial revision with `sequence_number = 1` and
   `previous_revision = null`.
4. Compute `id` as
   `SHA-256(canonical_json([1, state_hash, null]))` and set the initial
   revision as current.

> **Normative definition.**
Migration from legacy state formats MUST produce a full-snapshot initialization
followed by patch-based ordinary turns.

### Conflict detection

> **Normative definition.**
Ordinary reducer patches are serialized by the mailbox and current turn lease.
The host loads the current revision only after lease acquisition, so a later
ordinary turn observes the prior turn's commit rather than producing a patch
against its old base. Only the patch produced by the turn holding the current
fencing token is eligible for validation and commit. Prebuilt maintenance
patches MUST acquire the same lease and enter one FIFO single-writer queue.

> **Normative definition.**
If multiple prebuilt maintenance patches name the same base revision, their
FIFO queue order determines the first eligible patch. After it commits, every
later patch naming the old revision is rejected with `state.revision.stale`.
An ordinary turn or maintenance request that lacks the current lease is
rejected by the turn-lease contract; patch-id ordering MUST NOT choose a
winner. Equal patch ids are duplicate input and are rejected with
`state.revision.duplicate`.

### Deterministic behavior

> **Normative definition.**
All state operations MUST be deterministic:

- Operations MUST produce identical results given identical inputs and one
  application.
- Operation order MUST be deterministic (sequential within a patch).
- State hash computation MUST be deterministic.
- Revision sequence numbers MUST be monotonically increasing.

## 3.3 Failure Evidence And Operational Notes

### Diagnostics

> **Normative definition.**
All diagnostics emitted by the host MUST conform to the `Diagnostic` type
defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics).

Diagnostics MUST identify the phase contract, profile, and failed boundary
without exposing secrets or implementation internal state.

### Diagnostic families

| Family | Purpose | Example codes |
|--------|---------|---------------|
| `state.patch` | Patch validation failures | `malformed`, `incompatible` |
| `state.operation` | Operation validation failures | `unknown_type`, `invalid_path`, `precondition_failed` |
| `state.revision` | Revision-related failures | `stale`, `duplicate`, `sequence_error` |
| `state.schema` | Schema validation failures | `version_mismatch`, `type_error` |
| `state.size` | Size limit violations | `patch_too_large`, `value_too_large`, `path_too_deep` |
| `state.rollback` | Rollback failures | `irreversible`, `corruption_detected` |

### Failure modes

| Mode | Description | Conditions |
|------|-------------|------------|
| Malformed | Invalid patch or operation structure | Failed JSON parsing or schema validation |
| Incompatible | State schema version incompatible | Schema version mismatch |
| Conflicting | Concurrent turn ownership | Request does not hold the current turn lease |
| Unauthorized | Missing write permissions | Path namespace ownership violated |
| Exhausted | Size limits exceeded | Patch, value, or path too large |
| Unavailable | State initialization required | Agent has no initial state |
| Stale | Patch targets outdated revision | base_revision does not match current |
| Precondition failed | Operation precondition not met | test operation or conditional check fails |

### Fixed revision storage policy and governing references

1. **Hash algorithm**: State and revision identifiers use the fixed SHA-256
   calculations in [Next-revision calculation](#next-revision-calculation).

2. **Concurrent request serialization**: Mailbox FIFO and the current turn
   lease provide the fixed single-writer order under
   [Conflict detection](#conflict-detection). Patch ids never select a winner.

3. **Snapshot frequency**: The host MUST materialize one canonical full-state
   snapshot for every committed revision before making that revision current.
   Snapshot persistence is part of the atomic patch commit. A snapshot write
   failure MUST emit `identity.storage.write_failed`, publish no revision, and
   leave the prior state current.

4. **State compression**: The host MAY compress only the internal storage
   representation of a snapshot. Decompression MUST produce bytes identical
   to the canonical uncompressed snapshot; hashes MUST be computed from the
   uncompressed bytes. Compression MUST NOT change snapshot availability,
   commit behavior, diagnostics, or protocol output, and its format is not a
   profile selection.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **State diff API**: A formal state diff API will be implemented in future milestones. The protocol is language-neutral and does not require state diffs for base conformance.

2. **State history API**: A formal state history API will be implemented in future milestones. The protocol is language-neutral and does not require state history for base conformance.

3. **State branching API**: A formal state branching API will be implemented in future milestones. The protocol is language-neutral and does not require state branching for base conformance.

4. **State merge API**: A formal state merge API will be implemented in future milestones. The protocol is language-neutral and does not require state merge for base conformance.

## 3.4 Phase 3 Integration Tests

### Successful state update

> **Normative definition.**
The successful state update integration test validates that a valid patch
is applied successfully and produces the expected state and revision.

Expected behavior:

- Input: valid patch with matching base_revision.
- Expected output: new revision with updated state hash.
- Expected error: null.

### Patch with multiple operations

> **Normative definition.**
The patch with multiple operations integration test validates that a patch
with multiple operations is applied atomically.

Expected behavior:

- Input: valid patch with 10 operations (set, delete, merge, append, increment, test).
- Expected output: new revision reflecting all operations.
- Expected error: null.

### State initialization

> **Normative definition.**
The state initialization integration test validates that a new agent can be
initialized with a full state snapshot.

Expected behavior:

- Input: full state snapshot for new agent.
- Expected output: initial revision with `sequence_number = 1` and
  `previous_revision = null`.
- Expected error: null.

### Stale revision rejection

> **Normative definition.**
The stale revision rejection integration test validates that a patch targeting
an outdated revision is rejected.

Expected behavior:

- Input: patch with base_revision older than current revision.
- Expected output: null.
- Expected error: `state.revision.stale`.

### Same-base request serialization

> **Normative definition.**
The same-base request test validates that two prebuilt maintenance patches
naming one revision are serialized before patch application.

Expected behavior:

- Input: two authorized prebuilt maintenance patches with the same
  `base_revision`, submitted to the FIFO maintenance queue.
- Expected output: the FIFO-earlier patch acquires the lease and commits; the
  later patch is rejected before application.
- Expected error: `state.revision.stale` for the later request.

### Precondition failure

> **Normative definition.**
The precondition failure integration test validates that an operation with
a failed precondition is rejected.

Expected behavior:

- Input: patch with test operation that fails precondition.
- Expected output: null.
- Expected error: `state.operation.precondition_failed`.

### Size limit enforcement

> **Normative definition.**
The size limit enforcement integration test validates that patches exceeding
size limits are rejected.

Expected behavior:

- Input: patch exceeding 64 KiB size limit.
- Expected output: null.
- Expected error: `state.size.patch_too_large`.

### Path validation

> **Normative definition.**
The path validation integration test validates that operations with invalid
paths are rejected.

Expected behavior:

- Input: operation with an invalid JSON Pointer escape, a non-root path without
  a leading slash, or a root path used by a non-root operation.
- Expected output: null.
- Expected error: `state.operation.invalid_path`.

### Rollback on partial failure

> **Normative definition.**
The rollback on partial failure integration test validates that a patch is
rolled back if an operation fails mid-application.

Expected behavior:

- Input: patch where middle operation fails.
- Expected output: state unchanged, no new revision.
- Expected error: `state.rollback.irreversible` or operation-specific error.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 3 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.
- All existing Phase 3 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
|--------|------|-----------|
| State operations | Required | Seven kinds fixed by this chapter; reducer wire patches map only to replace, delete, merge, and set |
| Patch structure | Required | Fields fixed by this chapter |
| [Patch identity](#patch) | Required | SHA-256 over the canonical non-self-referential patch fields |
| [Wire-to-internal bridge](#patch) | Required | Expected revision, schema version, JSON Pointer operations, producer id, and accepted principal map exactly |
| Path constraints | Required | Canonical JSON Pointer format fixed by this chapter |
| Namespace ownership | Required | Default namespaces fixed by this chapter |
| [Additional namespaces](#namespace-ownership) | MAY | Additional namespaces require explicit ownership and the same authorization checks |
| Patch-size limits | Required | Limits fixed by this chapter |
| Revision structure | Required | Fields fixed by this chapter |
| Validation order | Required | 6-step order fixed by this chapter |
| [Hash algorithm](#next-revision-calculation) | Required | SHA-256 over canonical JSON |
| [Concurrent request serialization](#conflict-detection) | Required | Ordinary turns load after lease acquisition; FIFO and lease order serialize prebuilt maintenance patches and later same-base patches are stale |
| [Snapshot frequency](#fixed-revision-storage-policy-and-governing-references) | Required | One canonical full-state snapshot per committed revision |
| [State compression](#fixed-revision-storage-policy-and-governing-references) | MAY (internal) | Permitted only under byte-identical and failure-equivalent behavior |

## Rationale and evidence (non-normative)

This chapter derives from the state management requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The state operation model provides:

- Deterministic mutations with patch-level duplicate suppression.
- Canonical paths with namespace ownership for clear state boundaries.
- Optional preconditions for optimistic concurrency control.

The patch model provides:

- Atomic application of multiple operations.
- Base revision tracking for conflict detection.
- Schema version tracking for forward compatibility.

The revision model provides:

- Monotonically increasing sequence numbers for ordering.
- Cryptographic state hashes for integrity verification.
- Linked-list structure for state history traversal.
- Deterministic revision IDs independent of wall-clock time.

The size limits provide:

- Protection against resource exhaustion attacks.
- Bounded memory and storage usage.
- Predictable performance characteristics.

The conflict detection provides:

- Early rejection of concurrent modifications.
- Clear diagnostics for debugging and monitoring.
- Foundation for future conflict resolution strategies.
