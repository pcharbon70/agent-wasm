# Directives, Strategies, Continuations, and Terminal States

```spec-meta
id: agent_wasm.directives
kind: contract
status: active
summary: External directives as data, serializable strategies, continuations, and terminal behavior.
surface:
  - "lib/agent_wasm/directives/**/*.ex"
  - "test/agent_wasm/directives/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.user_owned_external_bindings
```

## Source Traceability

- [Directives, Strategies, Continuations, and Terminal States](../../../60-specification/13-directives-strategies-continuations-and-terminal-states.md)

## Requirements

```spec-requirements
- id: agent_wasm.directives.effect_data
  statement: Emit, timer, effect, child-lifecycle, approval, and topology requests shall be represented as validated directives rather than guest-side effects.
  priority: must
  stability: stable
- id: agent_wasm.directives.strategy_snapshot
  statement: Direct, FSM, and bounded-loop strategies shall use explicit serializable snapshots and logical model-slot references.
  priority: must
  stability: stable
- id: agent_wasm.directives.terminal
  statement: Completed and cancelled states shall reject ordinary continuation and preserve bounded diagnostics and evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.directives.implementation_frontier
  covers:
    - agent_wasm.directives.effect_data
    - agent_wasm.directives.strategy_snapshot
    - agent_wasm.directives.terminal
  reason: Directive validation, strategy snapshots, and terminal-state enforcement are not implemented.
```
