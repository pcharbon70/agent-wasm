---
title: "Actions Instructions Validation Plans And Results"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-02
  - phase-02
  - action
  - instruction
  - validation
  - plan
  - result
aliases:
  - "M2-P2 Actions Instructions"
---

# Actions Instructions Validation Plans And Results

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/phase-02-actions-instructions-validation-plans-and-results.md)
of
[Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/README.md)
--
Signals, Actions, State, And Strategies.
It separates reusable operation definitions from concrete invocations
and deterministic execution plans.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Signal Envelopes Causality Routing And Delivery Vocabulary](10-signals-causality-routing-and-delivery.md).

## 2.1 Contract And Data Model

### ActionDescriptor

> **Normative definition.**
`ActionDescriptor` is the single manifest type defined by
[Action descriptor](03-agent-manifests-artifacts-schemas-and-registries.md#action-descriptor).
Its schema references are resolved to JSON Schemas before instruction
validation. This chapter does not define or accept a second action shape.

The base profile requires `deterministic: true`. A descriptor with
`deterministic: false` is incompatible with deterministic reducer execution
and MUST be rejected at artifact admission.

### Instruction

> **Normative definition.**
An instruction is a concrete invocation of an action within a turn.
It carries the action reference, arguments, causal context, and optional
scheduling metadata. The enclosing `TurnRequest` carries the expected state
revision.
This is the `Instruction` wire type defined by
[Instruction](04-turn-lifecycle-protocols-and-canonical-encoding.md#instruction);
the definition below is an exact restatement and does not introduce a second
representation or conversion.

> **Normative definition.**

```
Instruction {
  action: ActionRef,
  arguments: JsonObject?,
  idempotency_key: string?,
  context_refs: ContextRef[],
  scheduling: Scheduling?
}

ActionRef {
  name: string,
  version: string?
}

ContextRef {
  source: "signal" | "state" | "directive",
  id: string,
  field_path: string?
}

Scheduling {
  delay_ms: int?,
  schedule_id: string?
}
```

| Field | Type | Required | Source | Purpose |
|-------|------|----------|--------|---------|
| `action` | ActionRef | Yes | Sender | Action to execute |
| `arguments` | JsonObject? | No | Sender | Action arguments |
| `idempotency_key` | string? | No | Sender | Idempotency identifier |
| `context_refs` | ContextRef[] | Yes | Sender | Referenced signal/state/directive |
| `scheduling` | Scheduling? | No | Sender | Scheduling metadata |

### Validation order

> **Normative definition.**
The host MUST validate instructions in the following order:

1. Action resolution: verify the action exists and is declared in the manifest.
2. Schema validation: validate arguments against the action's input schema.
3. State preconditions: verify state access permissions and preconditions.
4. Grant verification: verify required grants are present and valid.
5. Bounded execution parameters: verify timeout, size limits, and other constraints.

> **Normative definition.**
If validation fails at any step, the host MUST reject the instruction with
a diagnostic identifying the failed step and the reason.

## 2.2 Behavior And Integration

### Execution plans

> **Normative definition.**
An execution plan describes the order and dependencies of action executions
within a turn.
Plans MAY be sequential or DAG-shaped based on action dependencies.

> **Normative definition.**

```
ExecutionPlan {
  nodes: PlanNode[],
  order: ExecutionOrder
}

PlanNode {
  id: string,
  action: ActionRef,
  arguments: JsonObject?,
  dependencies: string[],
  result_ref: string?
}

ExecutionOrder {
  type: "sequential" | "dag",
  nodes: string[]
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `nodes` | PlanNode[] | Yes | Plan nodes |
| `order` | ExecutionOrder | Yes | Execution order |

### Plan node fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Node identifier |
| `action` | ActionRef | Yes | Action to execute |
| `arguments` | JsonObject? | No | Action arguments |
| `dependencies` | string[] | Yes | Dependent node IDs |
| `result_ref` | string? | No | Reference to node result for downstream nodes |

### Deterministic scheduling

> **Normative definition.**
The host MUST schedule and execute plan nodes one at a time in a deterministic
order.
For sequential plans, nodes are executed in the order specified.
For DAG plans, nodes are executed in topological order with ties broken
by node ID lexicographically.

The host MUST ensure that node dependencies are satisfied before execution.
A node MUST NOT execute until all its dependencies have completed successfully.
Parallel execution and plan reordering are not permitted.

### Action timeout enforcement

> **Normative definition.**
When an `ActionDescriptor` supplies `timeout_ms`, the action deadline is the
earlier of the turn deadline and `timeout_ms` milliseconds after that action
starts. Without `timeout_ms`, the turn deadline is the action deadline.

The host MUST stop an action that reaches its effective deadline, discard all
of that node's result contributions, and terminate the plan without executing
later nodes. If the descriptor timeout is strictly earlier than the turn
deadline, the diagnostic is `action.timeout.deadline_exceeded`; otherwise it
is `identity.limit.time.turn_ms`. The interruption mechanism is internal and
MAY vary only when deadline classification, node execution, outputs,
diagnostics, and absence of partial effects are identical.

### Result classes

> **Normative definition.**
Action results fall into five distinct classes:

| Class | Description | Conditions |
|-------|-------------|------------|
| Domain success | Action completed successfully with domain logic | All validations passed, action returned success |
| Domain rejection | Action completed but domain logic rejected the operation | All validations passed, action returned rejection |
| Validation failure | Action failed validation before execution | Validation step failed |
| Infrastructure failure | Action failed due to infrastructure issues | Timeout, resource exhaustion, etc. |
| Cancellation | Action was interrupted by an authenticated cancellation request | No result contribution is committed |

### Result contributions

> **Normative definition.**
Action results contribute to the following turn outputs:

- **State operations**: Actions MAY produce state patches that modify agent state.
- **Directives**: Actions MAY produce directives for host processing.
- **Facts**: Actions MAY produce facts for strategy state updates.
- **Diagnostics**: Actions MAY produce diagnostics for host recording.
- **Terminal status**: Actions MAY produce terminal domain status.

> **Normative definition.**

```
ActionResult {
  node_id: string,
  status: "success" | "rejection" | "validation_failure" | "infrastructure_failure" | "cancelled",
  state_patch: StatePatch?,
  directives: Directive[],
  facts: JsonObject?,
  diagnostics: Diagnostic[],
  domain_status: DomainStatus?
}
```

## 2.3 Failure Evidence And Operational Notes

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
| `action.resolution` | Action resolution failures | `not_found`, `invalid_version` |
| `action.schema` | Schema validation failures | `type_mismatch`, `required_field_missing` |
| `action.state` | State access failures | `permission_denied`, `precondition_failed` |
| `action.grant` | Grant verification failures | `missing_grant`, `expired_grant` |
| `action.timeout` | Execution timeout | `deadline_exceeded` |
| `action.infrastructure` | Infrastructure failures | `resource_exhausted`, `internal_error` |

### Failure modes

| Mode | Description | Conditions |
|------|-------------|------------|
| Malformed | Invalid instruction structure | Failed JSON parsing or schema validation |
| Incompatible | Action version incompatible with artifact | Action version not supported |
| Conflicting | Multiple instructions modify same state | State conflict detected |
| Unauthorized | Missing required grants | Grant verification failed |
| Exhausted | Resource limits exceeded | Size limits, timeout, etc. |
| Unavailable | Action or dependency unavailable | Action not found or resource unavailable |

### Fixed execution policy and governing references

1. **Plan optimization**: Execution order and the prohibition on parallel plan
   execution are fixed by [Deterministic scheduling](#deterministic-scheduling).

2. **Timeout enforcement**: Effective deadlines and timeout failure behavior
   are fixed by [Action timeout enforcement](#action-timeout-enforcement).

3. **State conflict resolution**: Conflict detection and patch rejection are
   governed by [Conflict detection](12-state-operations-patches-revisions-and-conflicts.md#conflict-detection).

4. **Result caching**: The host MUST NOT reuse a cached `ActionResult` in place
   of invoking an eligible plan node. During one plan attempt, each eligible
   node is invoked at most once in fixed order. Nodes after a failed, timed-out,
   or cancelled node are skipped and are not executions. Any staged
   contribution from the interrupted plan is discarded; idempotency does not
   permit re-execution within that attempt.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Plan optimization API**: A future versioned extension may define a plan
   optimization API. The base protocol remains sequential and prohibits
   reordering.

2. **State conflict inspection API**: A future API may expose conflict evidence
   and the fixed patch-id ordering. It may not select a different winner.

3. **Result evidence cache API**: A future API may cache result evidence for
   inspection. It may not substitute a cached result for node invocation.

## 2.4 Phase 2 Integration Tests

### Successful execution

> **Normative definition.**
The successful execution integration test validates that a valid instruction
is executed successfully and produces the expected outputs.

Expected behavior:

- Input: valid instruction with matching action.
- Expected output: action result with success status.
- Expected error: null.

### Action not found

> **Normative definition.**
The action not found integration test validates that an instruction referencing
a non-existent action is rejected with a `action.resolution.not_found` diagnostic.

Expected behavior:

- Input: valid instruction with non-existent action.
- Expected output: null.
- Expected error: `action.resolution.not_found`.

### Schema mismatch

> **Normative definition.**
The schema mismatch integration test validates that an instruction with
invalid arguments is rejected with a `action.schema.type_mismatch` diagnostic.

Expected behavior:

- Input: valid instruction with invalid arguments.
- Expected output: null.
- Expected error: `action.schema.type_mismatch`.

### State access denied

> **Normative definition.**
The state access denied integration test validates that an instruction
attempting unauthorized state access is rejected with a `action.state.permission_denied` diagnostic.

Expected behavior:

- Input: valid instruction with unauthorized state access.
- Expected output: null.
- Expected error: `action.state.permission_denied`.

### Missing grant

> **Normative definition.**
The missing grant integration test validates that an instruction without
required grants is rejected with a `action.grant.missing_grant` diagnostic.

Expected behavior:

- Input: valid instruction with missing grants.
- Expected output: null.
- Expected error: `action.grant.missing_grant`.

### Timeout

> **Normative definition.**
The timeout integration test validates both descriptor-local and turn-limit
classification.

Expected behavior:

- Input A: valid instruction whose positive descriptor `timeout_ms` is
  strictly shorter than the remaining turn ceiling and is exhausted.
- Expected A: null with `action.timeout.deadline_exceeded`.
- Input B: valid instruction for which the turn ceiling is earlier than or
  equal to the descriptor timeout and is exhausted.
- Expected B: null with `identity.limit.time.turn_ms`.

### Infrastructure failure

> **Normative definition.**
The infrastructure failure integration test validates that an instruction
failing due to infrastructure issues is rejected with a `action.infrastructure.internal_error` diagnostic.

Expected behavior:

- Input: valid instruction that triggers infrastructure failure.
- Expected output: null.
- Expected error: `action.infrastructure.internal_error`.

### Serialized state updates

> **Normative definition.**
The serialized-state integration test validates that concurrent signal
submissions cannot produce concurrent reducer patches for one agent.

Expected behavior:

- Input: two FIFO-ordered mailbox entries whose actions update the same state
  path.
- Expected output: the first turn loads revision `n` and commits `n + 1`; only
  then does the second turn load `n + 1` and commit `n + 2`.
- Expected error: null; no patch conflict arbitration occurs.

### Cancellation

> **Normative definition.**
The cancellation integration test validates that an in-flight instruction
can be cancelled and leaves no unauthorized or partial state.

Expected behavior:

- Input: valid instruction that is cancelled mid-execution.
- Expected output: action result with `status: "cancelled"`; later nodes are
  skipped and no staged contribution commits.
- Expected error: null.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 2 to verify
no regressions.

Expected behavior:

- All Milestone 1 fixtures: PASS.
- All earlier Milestone 2 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
|--------|------|-----------|
| [Action descriptors](03-agent-manifests-artifacts-schemas-and-registries.md#action-descriptor) | Required | One manifest type; this chapter defines no alternate shape |
| Instruction structure | Required | Fields fixed by this chapter |
| Validation order | Required | 5-step order fixed by this chapter |
| [Plan shape](#execution-plans) | MAY | Sequential or DAG-shaped; both execute one node at a time in fixed order |
| Result classes | Required | Five classes fixed by this chapter |
| [Result contributions](#result-contributions) | MAY | Actions may contribute patches, directives, facts, diagnostics, or terminal status within the fixed result schema |
| [Plan optimization](#deterministic-scheduling) | Required | Sequential deterministic execution; no parallel execution or reordering |
| [Timeout enforcement](#action-timeout-enforcement) | MAY (internal interruption mechanism) | Descriptor-local expiry uses `action.timeout`; turn-limit expiry uses `identity.limit.time.turn_ms` |
| [Concurrent state requests](12-state-operations-patches-revisions-and-conflicts.md#conflict-detection) | Required | Ordinary turns load state only after acquiring the lease; prebuilt same-base maintenance patches serialize and later ones are stale |
| [Result caching](#fixed-execution-policy-and-governing-references) | Required | Cached substitution prohibited; each eligible node is invoked at most once per plan attempt |

## Rationale and evidence (non-normative)

This chapter derives from the turn protocol requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The action descriptor model provides:

- Reusable operation definitions that can be referenced by multiple instructions.
- Clear separation between operation metadata and concrete invocations.
- Deterministic constraints that enable predictable execution.

The instruction model provides:

- A concrete invocation mechanism for actions.
- Causal context for distributed debugging and replay.
- Optional scheduling metadata for deferred execution.

The validation order provides:

- Early rejection of invalid instructions.
- Clear error reporting for debugging.
- Consistent behavior across implementations.

The execution plan model provides:

- Deterministic scheduling of action executions.
- Support for both sequential and DAG-shaped dependencies.
- Clear dependency tracking for deterministic sequential execution.

The result classes provide:

- Distinct handling for different failure modes.
- Clear separation between domain logic and infrastructure issues.
- Stable diagnostics for debugging and monitoring.
