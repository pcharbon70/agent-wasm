---
title: "Actions Instructions Validation Plans And Results"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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
An action descriptor is a reusable operation definition that the artifact
declares in its manifest.
It describes the operation's input/output schemas, state access requirements,
directive kinds, required grants, and deterministic constraints.

> **Normative definition.**

```
ActionDescriptor {
  name: string,
  input_schema: JsonSchema?,
  output_schema: JsonSchema?,
  state_access: StateAccess,
  directive_kinds: DirectiveKind[],
  required_grants: GrantRef[],
  deterministic: boolean,
  timeout_ms: int?
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

GrantRef {
  principal: string?,
  capability: CapabilityRef,
  resource: string?,
  conditions: JsonObject?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Yes | Action identifier |
| `input_schema` | JsonSchema? | No | Input validation schema |
| `output_schema` | JsonSchema? | No | Output validation schema |
| `state_access` | StateAccess | Yes | State access permissions |
| `directive_kinds` | DirectiveKind[] | Yes | Allowed directive types |
| `required_grants` | GrantRef[] | Yes | Required capability grants |
| `deterministic` | boolean | Yes | Whether the action is deterministic |
| `timeout_ms` | int? | No | Execution timeout |

### Instruction

> **Normative definition.**
An instruction is a concrete invocation of an action within a turn.
It carries the action reference, arguments, causal context, expected revision,
and optional scheduling metadata.

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
The host MUST schedule plan nodes in a deterministic order.
For sequential plans, nodes are executed in the order specified.
For DAG plans, nodes are executed in topological order with ties broken
by node ID lexicographically.

The host MUST ensure that node dependencies are satisfied before execution.
A node MUST NOT execute until all its dependencies have completed successfully.

### Result classes

> **Normative definition.**
Action results fall into four distinct classes:

| Class | Description | Conditions |
|-------|-------------|------------|
| Domain success | Action completed successfully with domain logic | All validations passed, action returned success |
| Domain rejection | Action completed but domain logic rejected the operation | All validations passed, action returned rejection |
| Validation failure | Action failed validation before execution | Validation step failed |
| Infrastructure failure | Action failed due to infrastructure issues | Timeout, resource exhaustion, etc. |

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
  status: "success" | "rejection" | "validation_failure" | "infrastructure_failure",
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

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Plan optimization**: The host MAY optimize execution plans (e.g.,
   parallelize independent nodes). The optimization algorithm is
   implementation-defined.

2. **Timeout enforcement**: The host MAY enforce action execution timeouts.
   The enforcement mechanism is implementation-defined.

3. **State conflict resolution**: The host MAY implement state conflict
   resolution strategies. The strategy is implementation-defined.

4. **Result caching**: The host MAY cache action results for idempotency.
   The caching strategy is implementation-defined.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Plan optimization API**: A formal plan optimization API will be
   implemented in future milestones. The protocol is language-neutral and
   does not require plan optimization for base conformance.

2. **State conflict resolution API**: A formal state conflict resolution
   API will be implemented in future milestones. The protocol is
   language-neutral and does not require conflict resolution for base
   conformance.

3. **Result caching API**: A formal result caching API will be implemented
   in future milestones. The protocol is language-neutral and does not
   require result caching for base conformance.

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
The timeout integration test validates that an instruction exceeding the
execution timeout is rejected with a `action.timeout.deadline_exceeded` diagnostic.

Expected behavior:

- Input: valid instruction that exceeds timeout.
- Expected output: null.
- Expected error: `action.timeout.deadline_exceeded`.

### Infrastructure failure

> **Normative definition.**
The infrastructure failure integration test validates that an instruction
failing due to infrastructure issues is rejected with a `action.infrastructure.internal_error` diagnostic.

Expected behavior:

- Input: valid instruction that triggers infrastructure failure.
- Expected output: null.
- Expected error: `action.infrastructure.internal_error`.

### State conflict

> **Normative definition.**
The state conflict integration test validates that conflicting instructions
are detected and handled appropriately.

Expected behavior:

- Input: two instructions modifying same state concurrently.
- Expected output: one instruction succeeds, other is rejected.
- Expected error: `action.state.conflict` for rejected instruction.

### Cancellation

> **Normative definition.**
The cancellation integration test validates that an in-flight instruction
can be cancelled and leaves no unauthorized or partial state.

Expected behavior:

- Input: valid instruction that is cancelled mid-execution.
- Expected output: action result with cancellation status.
- Expected error: null.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 2 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Phase 3 fixtures: PASS.
- All Phase 4 fixtures: PASS.
- All Phase 5 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

| Clause | Type | Selection |
|--------|------|-----------|
| Action descriptors | Required | Declared in artifact manifest |
| Instruction structure | Required | Fields fixed by this chapter |
| Validation order | Required | 5-step order fixed by this chapter |
| Execution order | Required | Sequential or DAG fixed by this chapter |
| Result classes | Required | Four classes fixed by this chapter |
| Plan optimization | Implementation-defined | Documented in conformance profile |
| Timeout enforcement | Implementation-defined | Documented in conformance profile |
| State conflict resolution | Implementation-defined | Documented in conformance profile |
| Result caching | Implementation-defined | Documented in conformance profile |

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
- Clear dependency tracking for parallel execution.

The result classes provide:

- Distinct handling for different failure modes.
- Clear separation between domain logic and infrastructure issues.
- Stable diagnostics for debugging and monitoring.