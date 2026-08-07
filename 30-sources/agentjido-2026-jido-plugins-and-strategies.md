---
title: "Jido Plugins and Strategies"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026pluginsstrategies"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/plugins.html"
accessed: "2026-08-07"
tags:
  - jido
  - plugin-system
  - runtime
aliases: []
---

# Jido Plugins and Strategies

## Reference

AgentJido. *Plugins* and *Strategies*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/plugins.html), including the [strategy guide](https://jido.hexdocs.pm/strategies.html), accessed 7 August 2026.

## Contribution

The sources define two orthogonal extension axes: plugins package capabilities and lifecycle hooks, while strategies determine how instructions advance an agent.

## Findings

A plugin specification bundles actions, state schema and key, configuration, signal patterns and routes, schedules, and optional owned processes. Plugin state is namespaced but not physically sandboxed. Ordered hooks prepare inbound signals, authorize resolved actions, prepare outbound emissions, and transform only synchronous caller views.

Strategies share a command/init/tick/snapshot contract. Direct execution, finite-state machines, behavior trees, and LLM loops can therefore expose a stable status/result snapshot while retaining different internal state. The FSM strategy uses a runtime instruction directive to keep the transition function pure across effectful work.

## Relevance

Jido plugins should become manifests that compose routes, schemas, hooks, and code artifacts; they should not be equated one-for-one with Extism modules. Strategies are especially well suited to portable guest reducers.

## Limits

Plugin order and route precedence can create non-local behavior. Security hooks implemented by untrusted Wasm cannot be trusted to authorize themselves; a portable design needs trust tiers.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
