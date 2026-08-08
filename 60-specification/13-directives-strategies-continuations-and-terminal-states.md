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
  kind: DirectiveKind,
  payload: JsonObject?,
  requested_capability: CapabilityRef,
  causal_metadata: CausalMetadata,
  completion_signal: string?,
  retry_class: RetryClass?,
  result_contract: ResultContract?
}

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
| `kind` | DirectiveKind | Yes | Directive category |
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
