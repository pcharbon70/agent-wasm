---
title: "Directives Strategies Continuations And Terminal States"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-02
  - phase-04
  - directive
  - strategy
  - continuation
  - terminal
  - model-bindings
aliases:
  - "M2-P4 Directives Strategies"
---

# Directives Strategies Continuations And Terminal States

## Status and authority

This chapter is a normative specification produced by
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
Its wire representation is the single `Directive` type defined by
[Directives](04-turn-lifecycle-protocols-and-canonical-encoding.md#directives).
This chapter adds validation, commit, execution, retry, and lifecycle semantics
to that type; it does not define a second directive representation.

> **Normative definition.**

```
DirectiveKindName = "emit" | "timer" | "effect" | "child-lifecycle" | "approval" | "topology"

CapabilityRef {
  name: string,
  version: string?
}

CausalMetadata {
  turn_id: string,
  instruction_id: string?,
  action_name: string,
  timestamp: UnixTimestamp
}
```

`RetryClass` and `ResultContract` are the wire structures defined with
`Directive` in chapter 04. `CapabilityRef` is a manifest and descriptor
reference, not an alternate wire field. `CausalMetadata` is host-derived
evidence built from the committed turn; its timestamp is copied from the
turn's signal timestamp. It MUST NOT be embedded as an additional field in the
wire directive.

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Directive identifier |
| `kind` | DirectiveKindName | Yes | Directive category |
| `payload` | JsonObject? | No | Directive-specific data |
| `capability` | string | Yes | Capability required to fulfill |
| `resource` | string? | No | Attenuated target resource |
| `destination` | string? | No | Explicit kind-specific effect target |
| `causation_id` | string | Yes | Producing initialization or invocation identity |
| `completion_signal` | CompletionSignal? | No | Signal emitted on completion |
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
Version `1.0.0` replaces `0.2.0`. It retains logical model-slot references,
fixes directive producer identity for initialization and turns, and replaces
any implied strategy authority to select a concrete provider, model,
connection, endpoint, or credential.

> **Normative definition.**

```
StrategyDescriptor {
  id: string,
  name: string,
  version: string,
  entry_state: string,
  transitions: TransitionRule[],
  state_schema: JsonSchema,
  model_slots: string[],
  timeout_ms: int?,
  max_iterations: int?
}

TransitionRule {
  from_state: string,
  signal_filter: SignalFilter?,
  state_filter: StateFilter?,
  prior_result_filter: JsonObject?,
  next_state: string,
  action: ActionRef?
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
| `model_slots` | string[] | Yes | Logical model requirements this strategy may request |
| `timeout_ms` | int? | No | Maximum strategy execution time |
| `max_iterations` | int? | No | Maximum state transitions per turn |

Every `model_slots` value MUST resolve to a model requirement in the effective
agent definition. A strategy MUST NOT identify or override a provider, model,
adapter, connection, endpoint, credential custodian, or credential handle.
Concrete selection belongs to the user-approved binding defined in
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md).

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
4. **Condition field**: Verify that no custom condition is present.

> **Normative definition.**
The `condition` field is not a member of `TransitionRule` in this specification
version. Any occurrence, including `null`, makes the strategy descriptor
ill-formed and MUST be rejected before activation with
`strategy.transition.condition_unsupported`. Accepted transitions match only
through their signal, state, and prior-result filters.

The first matching transition is executed.
If no transition matches, the strategy enters a terminal state.

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
State A → [Signal/Filters] → State B → [Signal/Filters] → State C (terminal)
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
| Terminal states | Exit state (after max iterations or a filter-matched exit transition) |
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
| `failed` | Execution failed | `running` (later admitted signal), `cancelled` |
| `cancelled` | Explicitly cancelled | (terminal) |
| `suspended` | Paused by host or user | `waiting`, `running` |

> **Normative definition.**
State transitions MUST be validated against the strategy's transition rules.
Invalid transitions MUST be rejected with a diagnostic.

> **Normative definition.**
Directive dispatch MUST NOT mutate the committed strategy snapshot directly.
A `failed` -> `running` transition may occur only in a later reducer turn whose
input signal matches an admitted transition rule. While directive attempts
remain, retry state belongs to the durable outbox attempt record. After success
or retry exhaustion, the host emits the configured completion signal; that
later signal may cause the strategy to remain running, enter `failed`, or take
another declared transition. Without such a transition, retry exhaustion does
not silently rewrite strategy state.

### Directive processing

> **Normative definition.**
The host MUST process all emitted directives in the following order:

1. **Precommit validation**: Verify every directive's wire structure,
   deterministic id, kind, capability, resource, destination, retry class, and
   result contract.
2. **Atomic commit**: Commit the state, journal, and all validated directive
   outbox entries as one unit.
3. **Scheduling**: Queue committed outbox entries in emitted array order.
4. **Execution**: Execute directives asynchronously outside the deterministic
   reducer scope.
5. **Retry**: Re-queue a failed postcommit effect attempt only as permitted by
   its retry class.
6. **Completion signal**: Emit the configured completion signal after success
   or terminal retry exhaustion.

If any directive fails precommit validation, the host MUST reject the entire
turn and commit no state, journal entry, or outbox entry. Scheduling MUST occur
only after the atomic commit is durable. Directives MUST be executed
asynchronously; the turn caller MUST NOT wait for directive completion.
Directive completion or failure is observed only through the configured
completion signal and directive diagnostics.

> **Normative definition.**
Postcommit directive execution MUST NOT alter the committed turn state or
`TurnResult`. If a postcommit attempt fails, the committed turn remains
successful and the attempt follows its fixed retry or terminal-failure path.
Directive retry MUST NOT redeliver the input signal.

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
`started_at` is copied from the signal timestamp that activated the strategy,
and `last_transitioned_at` is copied from the signal timestamp that caused the
most recent transition. The host MUST NOT insert wall-clock values into either
field.
The host MUST report suspension only after the canonical snapshot is durable.
After restart or host relocation, restoration MUST produce a byte-identical
canonical snapshot and the same subsequent transition and diagnostic behavior.
A persistence backend is internal and MAY vary only when these observations,
durability, and failure behavior are identical.

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
| `strategy.transition` | Strategy transition failures | `invalid_state`, `no_matching_rule`, `iteration_exceeded`, `condition_unsupported` |
| `strategy.loading` | Strategy descriptor loading failures | `not_found`, `invalid_descriptor` |
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

### Fixed directive and strategy policy

1. **Directive execution model**: Validation and atomic commit precede the
   asynchronous postcommit execution defined by
   [Directive processing](#directive-processing).

2. **Strategy persistence**: Persistence and restoration observations are fixed
   by [Strategy lifecycle](#strategy-lifecycle). The backend is internal under
   the byte-identical, durable, and failure-equivalent constraints there.

3. **Retry backoff**: `RetryClass.max_attempts` MUST be at least 1 and counts
   the initial attempt. `backoff_ms` MUST be non-negative and is the exact
   delay before every subsequent attempt. `jitter_ms` MUST be absent or zero.
   Any other retry class is ill-formed. No exponential, linear-growth, or
   jittered adjustment is permitted.

4. **Strategy loading**: The host MUST load the descriptor identified by
   `strategy_id` and `strategy_version` from the admitted artifact and validate
   it before activation. The host MAY use any internal loading backend only if
   it returns byte-identical canonical descriptor bytes and identical
   acceptance, rejection, and diagnostic observations. Missing descriptors
   MUST fail with `strategy.loading.not_found`; invalid descriptors MUST fail
   with `strategy.loading.invalid_descriptor`. Neither failure may create a
   snapshot or execute a transition.

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
- Expected output: directive validated and committed with the turn, then
  processed asynchronously and followed by its completion signal.
- Expected error: null.

### Directive with retry

> **Normative test scenario.**
The directive with retry integration test validates that a failing directive
is retried according to its retry class.

Expected behavior:

- Input: action emitting a directive with `max_attempts = 2`,
  `backoff_ms = 100`, and `jitter_ms = 0` that fails on its first attempt.
- Expected output: directive retried exactly once after 100 milliseconds and
  then succeeds; the committed turn is unchanged and the input signal is not
  redelivered.
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
- Expected output: null; no state, journal, or outbox entry is committed.
- Expected error: `directive.missing.missing_capability`.

### Strategy model-slot validation

> **Normative test scenario.**
The strategy model-slot integration test validates that a strategy references
only logical requirements from the effective agent definition.

Expected behavior:

- Input: one strategy with a declared logical slot and one strategy that
  attempts to embed a provider, model, endpoint, or credential reference.
- Expected output: the logical-slot strategy is accepted.
- Expected error: the concrete-selection strategy is rejected before
  activation with a bounded manifest or strategy diagnostic.

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

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
|--------|------|-----------|
| Directive kinds | Required | Six kinds fixed by this chapter |
| Strategy descriptors | Required | Fields fixed by this chapter |
| Strategy model slots | Required | Logical requirement references only; concrete selection prohibited |
| Strategy snapshots | Required | Fields fixed by this chapter |
| Strategy transitions | Required | Direct, FSM, bounded loop fixed by this chapter |
| Domain states | Required | Six states fixed by this chapter |
| Directive processing order | Required | Precommit validation, atomic commit, scheduling, execution, retry, completion |
| [Condition field](#strategy-transitions) | Required | Field prohibited; any occurrence is rejected |
| [Directive execution model](#directive-processing) | Required | Validation is precommit; execution is asynchronous and postcommit in emitted order |
| [Strategy persistence](#strategy-lifecycle) | MAY (internal backend) | Byte-identical durable restoration and failure equivalence required |
| [Retry backoff](#fixed-directive-and-strategy-policy) | Required | Constant `backoff_ms`; no jitter or growth algorithm |
| [Strategy loading](#fixed-directive-and-strategy-policy) | MAY (internal backend) | Byte-identical descriptor and outcome equivalence required |

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
