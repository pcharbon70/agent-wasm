---
title: "Directives Strategies Continuations And Terminal States"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-02
  - phase-04
  - directive
  - strategy
  - continuation
  - terminal
aliases:
  - "M2-P4 Directives Strategies"
---

# Directives Strategies Continuations And Terminal States

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/phase-04-directives-strategies-continuations-and-terminal-states.md)
of
[Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/README.md)
--
Signals, Actions, State, And Strategies.
It defines external requests and replaceable decision policies without
hiding mutable runtime authority in the guest.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md).

## 4.1 Contract And Data Model

### Directive

> **Normative definition.**
A directive is an external request emitted by an action during a turn.
The host processes the directive after the turn completes, outside the
deterministic reducer scope.

> **Normative definition.**

```
Directive {
  id: string,
  kind: DirectiveKindName,
  payload: JsonObject?,
  requested_capability: CapabilityRef,
  causal_metadata: CausalMetadata,
  completion_signal: string?,
  retry_class: RetryClass?,
  result_contract: ResultContract?
}

DirectiveKindName = "emit" | "timer" | "effect" | "child-lifecycle" | "approval" | "topology"

CausalMetadata {
  turn_id: string,
  instruction_id: string?,
  action_name: string,
  timestamp: timestamp
}

CapabilityRef {
  name: string,
  version: string?
}

RetryClass {
  max_attempts: int,
  backoff_ms: int,
  jitter_ms: int?
}

ResultContract {
  expected_fields: string[],
  schema_version: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Directive identifier |
| `kind` | DirectiveKindName | Yes | Directive category |
| `payload` | JsonObject? | No | Directive-specific data |
| `requested_capability` | CapabilityRef | Yes | Capability required to fulfill |
| `causal_metadata` | CausalMetadata | Yes | Turn causality context |
| `completion_signal` | string? | No | Signal emitted on completion |
| `retry_class` | RetryClass? | No | Retry policy for unfulfilled directives |
| `result_contract` | ResultContract? | No | Expected result structure |

### Directive kinds

> **Normative definition.**
Directives are classified into six kinds based on the external action they request:

| Kind | Description | Example |
|------|-------------|---------|
| `emit` | Emit an external event or notification | Send email, publish message |
| `timer` | Schedule a delayed signal | Set reminder, poll after delay |
| `effect` | Modify external state through a capability | Write to database, call API |
| `child-lifecycle` | Manage child agent lifecycle | Spawn, pause, resume, terminate child |
| `approval` | Request user or external approval | Approve transaction, confirm action |
| `topology` | Modify agent topology | Add/remove agent, change routing |

> **Normative definition.**
Each directive kind requires the capability listed in the action's
`directive_kinds` field (see
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)).

### StrategyDescriptor

> **Normative definition.**
A strategy descriptor defines a replaceable decision policy for an agent.
Strategies are versioned, bounded, and serializable to enable hot-replacement
without state corruption.

> **Normative definition.**

```
StrategyDescriptor {
  id: string,
  name: string,
  version: string,
  entry_state: string,
  transitions: TransitionRule[],
  state_schema: JsonSchema,
  timeout_ms: int?,
  max_iterations: int?
}

TransitionRule {
  from_state: string,
  signal_filter: SignalFilter?,
  state_filter: StateFilter?,
  prior_result_filter: JsonObject?,
  next_state: string,
  action: ActionRef?,
  condition: string?
}

SignalFilter {
  type: string?,
  source: string?,
  match: JsonObject?
}

StateFilter {
  path: string,
  operator: "equals" | "not_equals" | "exists" | "not_exists",
  expected: JsonValue?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Strategy identifier |
| `name` | string | Yes | Human-readable strategy name |
| `version` | string | Yes | Strategy version (semantic versioning) |
| `entry_state` | string | Yes | Initial state name |
| `transitions` | TransitionRule[] | Yes | State transition rules |
| `state_schema` | JsonSchema | Yes | State data schema |
| `timeout_ms` | int? | No | Maximum strategy execution time |
| `max_iterations` | int? | No | Maximum state transitions per turn |

### StrategySnapshot

> **Normative definition.**
A strategy snapshot captures the current continuation state of a running
strategy.
Snapshots are serializable and portable across hosts.

> **Normative definition.**

```
StrategySnapshot {
  strategy_id: string,
  strategy_version: string,
  current_state: string,
  state_data: JsonObject,
  iteration: int,
  started_at: timestamp,
  last_transitioned_at: timestamp
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `strategy_id` | string | Yes | Strategy identifier |
| `strategy_version` | string | Yes | Strategy version |
| `current_state` | string | Yes | Current state name |
| `state_data` | JsonObject | Yes | State data |
| `iteration` | int | Yes | Current iteration count |
| `started_at` | timestamp | Yes | Strategy start timestamp |
| `last_transitioned_at` | timestamp | Yes | Last transition timestamp |

### Type definitions

> **Normative definition.**
The following types are used across this chapter.

- **timestamp**: ISO 8601 UTC datetime string (e.g., `2026-08-08T10:00:00Z`).
  Defined in [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

- **JsonValue**: Any valid JSON value (string, number, boolean, null, object, array).

- **JsonObject**: A JSON object (key-value pairs).

- **JsonSchema**: A JSON Schema document (draft-07 or later).

- **ActionRef**: Defined in
  [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md).

## 4.2 Behavior And Integration

### Strategy transitions

> **Normative definition.**
Strategies transition between states based on explicit signal, state, and
prior result inputs.
Three strategy transition models are specified:

1. **Direct**: Single-step strategy with one transition from entry to exit.
2. **FSM (Finite State Machine)**: Multi-state strategy with conditional transitions.
3. **Bounded Loop**: Repeating strategy with iteration limit.

> **Normative definition.**
Each transition evaluates:

1. **Signal filter**: Match against incoming signal type, source, and payload.
2. **State filter**: Match against current state data.
3. **Prior result filter**: Match against previous action result.
4. **Condition**: Evaluate custom condition expression (if provided).

> **Normative definition.**
The `condition` field on `TransitionRule` is an implementation-defined expression language.
Implementations MUST document the expression syntax and evaluation model in their conformance profile.
The expression MUST evaluate to a boolean given the current signal, state data, and prior result.
If the expression cannot be evaluated (e.g., syntax error, undefined variable), the transition MUST NOT match.

The first matching transition is executed.
If no transition matches, the strategy enters a terminal state.

> **Non-normative note.**
A common expression syntax is JSONPath-like predicates (e.g., `$.state.counter > 5`) or simple comparison operators.
Implementations are free to choose any syntax as long as it is documented.

### Direct strategy

> **Normative definition.**
A direct strategy executes a single action and transitions to a terminal state.

> **Non-normative diagram.**

```
Direct Strategy Flow:
Entry State → [Signal] → Execute Action → Exit State (terminal)
```

| Property | Value |
|----------|-------|
| Max iterations | 1 |
| Terminal states | Exit state |
| Use case | Simple action execution |

### FSM strategy

> **Normative definition.**
A finite state machine strategy transitions through multiple states based on
signals and state conditions.

> **Non-normative diagram.**

```
FSM Strategy Flow:
State A → [Signal/Condition] → State B → [Signal/Condition] → State C (terminal)
```

| Property | Value |
|----------|-------|
| Max iterations | `max_iterations` or unlimited |
| Terminal states | States with no outgoing transitions |
| Use case | Multi-step workflows, approval chains |

### Bounded loop strategy

> **Normative definition.**
A bounded loop strategy repeats a state transition up to a maximum iteration count.

> **Normative definition.**
Bounded loop strategies MUST set `max_iterations` on the `StrategyDescriptor`.
Strategies without `max_iterations` are classified as FSM strategies.

> **Non-normative diagram.**

```
Bounded Loop Strategy Flow:
Loop State → [Signal] → Execute Action → Loop State (if iterations < max) → Exit State (terminal)
```

| Property | Value |
|----------|-------|
| Max iterations | `max_iterations` (required) |
| Terminal states | Exit state (after max iterations or condition met) |
| Use case | Polling, retry loops, iterative refinement |

### Domain states

> **Normative definition.**
Agents and strategies exist in the following domain states independently of
actor activation:

| State | Description | Transitions to |
|-------|-------------|----------------|
| `waiting` | Awaiting signal or input | `running`, `cancelled` |
| `running` | Actively executing | `completed`, `failed`, `suspended`, `cancelled` |
| `completed` | Successfully finished | (terminal) |
| `failed` | Execution failed | `running` (retry), `cancelled` |
| `cancelled` | Explicitly cancelled | (terminal) |
| `suspended` | Paused by host or user | `waiting`, `running` |

> **Normative definition.**
State transitions MUST be validated against the strategy's transition rules.
Invalid transitions MUST be rejected with a diagnostic.

> **Normative definition.**
The `failed` → `running` transition is triggered by the directive retry mechanism.
When a directive fails and its `RetryClass.max_attempts` has not been exceeded,
the host transitions the strategy back to `running` to retry the directive.
If `max_attempts` is exceeded, the strategy transitions to `failed` and remains there
unless explicitly cancelled.

### Directive processing

> **Normative definition.**
After a turn completes, the host MUST process all emitted directives in
the following order:

1. **Validation**: Verify each directive's structure and required capability.
2. **Scheduling**: Queue directives for execution based on kind.
3. **Execution**: Execute directives outside the deterministic reducer scope.
4. **Completion signal**: Emit completion signal if specified.
5. **Retry**: Re-queue directives that failed based on retry class.

> **Normative definition.**
Directive execution MUST NOT affect the turn's state or results.
If a directive fails, the turn is still considered successful.

### Strategy lifecycle

> **Normative definition.**
A strategy follows the lifecycle:

1. **Activation**: Host loads strategy descriptor and creates initial snapshot.
2. **Execution**: Host processes signals through strategy transitions.
3. **Suspension**: Host saves snapshot and pauses strategy (optional).
4. **Resumption**: Host restores snapshot and continues processing.
5. **Termination**: Strategy reaches terminal state or is cancelled.

> **Normative definition.**
Strategy snapshots MUST be persisted before suspension and restored before
resumption.
Snapshots MUST include all fields defined in `StrategySnapshot`.

### Terminal state transitions

> **Normative definition.**
The host MUST reject the following terminal state transitions:

- Transition from a terminal state to a non-terminal state.
- Transition to an unknown state.
- Transition that exceeds `max_iterations` in bounded loop strategies.
- Transition that exceeds `timeout_ms` in time-bounded strategies.

> **Normative definition.**
Rejected transitions MUST emit a diagnostic identifying the failed boundary.

## 4.3 Failure Evidence And Operational Notes

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
| `directive.missing` | Missing directive handling | `unknown_kind`, `missing_capability` |
| `directive.execution` | Directive execution failures | `unauthorized`, `timeout`, `retry_exhausted` |
| `strategy.snapshot` | Strategy snapshot issues | `incompatible_version`, `corruption` |
| `strategy.transition` | Strategy transition failures | `invalid_state`, `no_matching_rule`, `iteration_exceeded` |
| `strategy.termination` | Terminal state issues | `already_terminal`, `timeout_exceeded` |
| `strategy.conflicting` | Concurrent strategy modifications | `concurrent_modification` |
| `continuation.invalid` | Invalid continuation | `missing_snapshot`, `invalid_state_data` |

### Failure modes

| Mode | Description | Conditions |
|------|-------------|------------|
| Malformed | Invalid directive or strategy structure | Failed JSON parsing or schema validation |
| Incompatible | Strategy version incompatible with snapshot | Strategy version mismatch |
| Conflicting | Concurrent strategy modifications | Same strategy modified by multiple actors |
| Unauthorized | Missing capability for directive | Required capability not granted |
| Exhausted | Resource limits exceeded | Iteration limit, timeout, or memory limit |
| Unavailable | Strategy or snapshot unavailable | Strategy not found or snapshot corrupted |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Directive execution model**: The host MAY choose to execute directives synchronously or asynchronously. The execution model is implementation-defined.

2. **Strategy persistence**: The host MAY choose how to persist strategy snapshots (e.g., in-memory, database, file system). The persistence mechanism is implementation-defined.

3. **Retry backoff**: The host MAY implement custom retry backoff strategies (e.g., linear, exponential, jittered). The backoff algorithm is implementation-defined.

4. **Strategy loading**: The host MAY choose how to load and validate strategy descriptors (e.g., from file, database, or remote source). The loading mechanism is implementation-defined.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Strategy composition API**: A formal strategy composition API will be implemented in future milestones. The protocol is language-neutral and does not require strategy composition for base conformance.

2. **Strategy debugging API**: A formal strategy debugging API will be implemented in future milestones. The protocol is language-neutral and does not require strategy debugging for base conformance.

3. **Strategy monitoring API**: A formal strategy monitoring API will be implemented in future milestones. The protocol is language-neutral and does not require strategy monitoring for base conformance.

## 4.4 Phase 4 Integration Tests

### Successful directive emission

> **Normative test scenario.**
The successful directive emission integration test validates that a valid
directive is emitted and processed.

Expected behavior:

- Input: action emitting a valid `emit` directive.
- Expected output: directive processed, completion signal emitted.
- Expected error: null.

### Directive with retry

> **Normative test scenario.**
The directive with retry integration test validates that a failing directive
is retried according to its retry class.

Expected behavior:

- Input: action emitting directive that fails on first attempt.
- Expected output: directive retried up to `max_attempts`, eventually succeeds.
- Expected error: null.

### FSM strategy transition

> **Normative test scenario.**
The FSM strategy transition integration test validates that a finite state
machine strategy transitions correctly.

Expected behavior:

- Input: strategy with multiple states and signal-triggered transitions.
- Expected output: strategy transitions through states in order, reaches terminal state.
- Expected error: null.

### Bounded loop strategy

> **Normative test scenario.**
The bounded loop strategy integration test validates that a bounded loop
strategy respects iteration limits.

Expected behavior:

- Input: bounded loop strategy with `max_iterations = 5`.
- Expected output: strategy executes 5 iterations, reaches terminal state.
- Expected error: null.

### Strategy suspension and resumption

> **Normative test scenario.**
The strategy suspension and resumption integration test validates that a
strategy can be suspended and resumed with preserved state.

Expected behavior:

- Input: running strategy, suspended, then resumed.
- Expected output: strategy continues from last transition state.
- Expected error: null.

### Terminal state rejection

> **Normative test scenario.**
The terminal state rejection integration test validates that transitions
from terminal states are rejected.

Expected behavior:

- Input: strategy in terminal state with incoming signal.
- Expected output: null.
- Expected error: `strategy.termination.already_terminal`.

### Invalid continuation rejection

> **Normative test scenario.**
The invalid continuation rejection integration test validates that a
continuation with invalid state data is rejected.

Expected behavior:

- Input: continuation with state data not matching `state_schema`.
- Expected output: null.
- Expected error: `continuation.invalid`.

### Incompatible strategy version

> **Normative test scenario.**
The incompatible strategy version integration test validates that a strategy
snapshot from an incompatible version is rejected.

Expected behavior:

- Input: snapshot from strategy version 1.0.0, loaded strategy version 2.0.0.
- Expected output: null.
- Expected error: `strategy.snapshot.incompatible_version`.

### Directive without capability

> **Normative test scenario.**
The directive without capability integration test validates that a directive
requiring an ungranted capability is rejected.

Expected behavior:

- Input: action emitting directive requiring ungranted capability.
- Expected output: null.
- Expected error: `directive.missing.missing_capability`.

### Cross-milestone fixture regression

> **Normative test scenario.**
All earlier milestone fixtures MUST be re-run after Phase 4 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Phase 3 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.
- All Milestone 2 Phase 3 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

| Clause | Type | Selection |
|--------|------|-----------|
| Directive kinds | Required | Six kinds fixed by this chapter |
| Strategy descriptors | Required | Fields fixed by this chapter |
| Strategy snapshots | Required | Fields fixed by this chapter |
| Strategy transitions | Required | Direct, FSM, bounded loop fixed by this chapter |
| Domain states | Required | Six states fixed by this chapter |
| Directive processing order | Required | Validation, scheduling, execution, completion, retry |
| Directive execution model | Implementation-defined | Documented in conformance profile |
| Strategy persistence | Implementation-defined | Documented in conformance profile |
| Retry backoff | Implementation-defined | Documented in conformance profile |
| Strategy loading | Implementation-defined | Documented in conformance profile |

## Rationale and evidence (non-normative)

This chapter derives from the decision policy and external interaction
requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The directive model provides:

- External requests that do not affect deterministic reducer scope.
- Capability-based access control for external actions.
- Retry policies for unfulfilled directives.

The strategy model provides:

- Replaceable decision policies with versioned descriptors.
- Serializable snapshots for suspension and resumption.
- Three transition models: direct, FSM, and bounded loop.

The domain state model provides:

- Explicit state tracking independent of actor activation.
- Clear lifecycle transitions for agents and strategies.
- Foundation for persistence and recovery.

The terminal state enforcement provides:

- Protection against invalid state transitions.
- Clear diagnostics for debugging and monitoring.
- Guarantee of strategy termination.
