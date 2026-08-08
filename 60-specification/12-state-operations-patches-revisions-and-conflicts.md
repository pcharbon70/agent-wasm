---
title: "State Operations Patches Revisions And Conflicts"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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

### StateOperation

> **Normative definition.**
A state operation is a deterministic, idempotent mutation or observation
of agent state within a turn.
Each operation acts on a canonical path and carries an optional precondition
for optimistic concurrency control.

> **Normative definition.**
Only the following operation kinds are specified; their deterministic semantics
MUST be explicit.

- **set**: Write a value at a path. Overwrites any existing value.
- **delete**: Remove a value at a path. No-op if path does not exist.
- **merge**: Merge a partial object into an existing object at a path.
- **append**: Append a value to an array at a path.
- **increment**: Add a numeric delta to a numeric value at a path.
- **test**: Verify a precondition without modifying state. Fails if precondition not met.

> **Normative definition.**

```
StateOperation {
  type: "set" | "delete" | "merge" | "append" | "increment" | "test",
  path: CanonicalPath,
  value: JsonValue?,
  delta: number?,
  precondition: Precondition?,
  schema_version: string?
}

CanonicalPath {
  segments: string[],
  namespace: string
}

Precondition {
  type: "exists" | "not_exists" | "version_matches" | "custom",
  expected: JsonValue?,
  message: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `type` | string | Yes | Operation kind |
| `path` | CanonicalPath | Yes | Target path with namespace |
| `value` | JsonValue? | Conditional | Value to set/merge/append |
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
  base_revision: string,
  state_schema_version: string?,
  operations: StateOperation[],
  created_at: timestamp,
  created_by: string
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Patch identifier |
| `base_revision` | string | Yes | Expected state revision before patch |
| `state_schema_version` | string? | No | Expected state schema version |
| `operations` | StateOperation[] | Yes | Ordered sequence of operations |
| `created_at` | timestamp | Yes | Patch creation timestamp |
| `created_by` | string | Yes | Patch originator identifier |

### Path constraints

> **Normative definition.**
Canonical paths MUST conform to the following constraints:

- Paths MUST use dot-separated segments (e.g., `agent.state.counter`).
- Segments MUST be non-empty strings.
- Segments MUST match `^[a-zA-Z_][a-zA-Z0-9_]*$`.
- Paths MUST not exceed 1000 characters.
- Paths MUST include a namespace prefix (e.g., `agent.`, `user.`).

| Constraint | Limit | Purpose |
|------------|-------|---------|
| Maximum path length | 1000 characters | Prevent path explosion |
| Segment regex | `^[a-zA-Z_][a-zA-Z0-9_]*$` | Enforce canonical naming |
| Minimum segments | 1 (namespace) | Ensure namespace ownership |
| Maximum segments | 50 | Prevent deep nesting |

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
  timestamp: timestamp,
  previous_revision: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Revision identifier (hash) |
| `sequence_number` | int | Yes | Monotonic sequence number |
| `state_hash` | string | Yes | Cryptographic hash of state |
| `timestamp` | timestamp | Yes | Revision creation timestamp |
| `previous_revision` | string? | Yes | Parent revision ID |

## 3.2 Behavior And Integration

### Patch validation

> **Normative definition.**
The host MUST validate patches in the following order before application:

1. **Structure validation**: Verify patch structure conforms to the Patch schema.
2. **Revision check**: Verify the patch's `base_revision` matches the current state revision.
3. **Operation validation**: Verify each operation's type, path, and value.
4. **Precondition check**: Verify each operation's precondition against current state.
5. **Size check**: Verify patch size does not exceed limits.
6. **Schema check**: Verify `state_schema_version` matches if provided.

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
- `state_hash` = hash(current_state)
- `timestamp` = current_timestamp
- `previous_revision` = current_revision_id
- `id` = hash(sequence_number || state_hash || timestamp)

### State initialization

> **Normative definition.**
The host MUST support full-snapshot initialization for new agents:

1. Accept a complete state object as initial value.
2. Compute initial state hash.
3. Create initial revision with `sequence_number = 0`.
4. Set initial revision as current state revision.

> **Normative definition.**
Migration from legacy state formats MUST produce a full-snapshot initialization
followed by patch-based ordinary turns.

### Conflict detection

> **Normative definition.**
The host MUST detect conflicts when:

- Two patches target the same `base_revision` concurrently.
- A patch's `base_revision` does not match current state revision.
- A patch's precondition fails against current state.

> **Normative definition.**
Upon conflict detection, the host MUST reject the conflicting patch and emit
a diagnostic with the conflict type and details.

### Deterministic behavior

> **Normative definition.**
All state operations MUST be deterministic:

- Operations MUST produce identical results given identical inputs.
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
| `state.patch` | Patch validation failures | `malformed`, `incompatible`, `conflict` |
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
| Conflicting | Concurrent patch application | Same base_revision targeted |
| Unauthorized | Missing write permissions | Path namespace ownership violated |
| Exhausted | Size limits exceeded | Patch, value, or path too large |
| Unavailable | State initialization required | Agent has no initial state |
| Stale | Patch targets outdated revision | base_revision does not match current |
| Precondition failed | Operation precondition not met | test operation or conditional check fails |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Hash algorithm**: The host MAY choose the hash algorithm for state and revision computation (e.g., SHA-256, SHA-3). The algorithm MUST be documented in the conformance profile.

2. **Conflict resolution**: The host MAY implement conflict resolution strategies (e.g., last-writer-wins, custom merge functions). The strategy is implementation-defined.

3. **Snapshot frequency**: The host MAY choose how frequently to emit full-state snapshots (e.g., every N revisions, on-demand). The frequency is implementation-defined.

4. **State compression**: The host MAY compress state snapshots for storage efficiency. The compression algorithm is implementation-defined.

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
- Expected output: initial revision with sequence_number = 0.
- Expected error: null.

### Stale revision rejection

> **Normative definition.**
The stale revision rejection integration test validates that a patch targeting
an outdated revision is rejected.

Expected behavior:

- Input: patch with base_revision older than current revision.
- Expected output: null.
- Expected error: `state.revision.stale`.

### Conflicting patch rejection

> **Normative definition.**
The conflicting patch rejection integration test validates that two concurrent
patches targeting the same revision result in one being rejected.

Expected behavior:

- Input: two patches with same base_revision submitted concurrently.
- Expected output: one patch succeeds, other is rejected.
- Expected error: `state.patch.conflict` for rejected patch.

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

- Input: operation with invalid path (e.g., empty segment, invalid characters).
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
- All Phase 3 fixtures: PASS.
- All Phase 4 fixtures: PASS.
- All Phase 5 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

| Clause | Type | Selection |
|--------|------|-----------|
| State operations | Required | Six kinds fixed by this chapter |
| Patch structure | Required | Fields fixed by this chapter |
| Path constraints | Required | Canonical path format fixed by this chapter |
| Patch-size limits | Required | Limits fixed by this chapter |
| Revision structure | Required | Fields fixed by this chapter |
| Validation order | Required | 6-step order fixed by this chapter |
| Hash algorithm | Implementation-defined | Documented in conformance profile |
| Conflict resolution | Implementation-defined | Documented in conformance profile |
| Snapshot frequency | Implementation-defined | Documented in conformance profile |
| State compression | Implementation-defined | Documented in conformance profile |

## Rationale and evidence (non-normative)

This chapter derives from the state management requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The state operation model provides:

- Deterministic, idempotent mutations that enable predictable state transitions.
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

The size limits provide:

- Protection against resource exhaustion attacks.
- Bounded memory and storage usage.
- Predictable performance characteristics.

The conflict detection provides:

- Early rejection of concurrent modifications.
- Clear diagnostics for debugging and monitoring.
- Foundation for future conflict resolution strategies.
