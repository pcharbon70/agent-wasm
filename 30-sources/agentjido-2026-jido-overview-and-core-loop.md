---
title: "Jido Overview and Core Loop"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026overviewcoreloop"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/core-loop.html"
accessed: "2026-08-07"
tags:
  - agent-tools
  - jido
  - runtime
aliases: []
---

# Jido Overview and Core Loop

## Reference

AgentJido. *Home* and *Core Loop*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/core-loop.html), accessed 7 August 2026. Read with the [package overview](https://jido.hexdocs.pm/readme.html) and [Agent API](https://jido.hexdocs.pm/Jido.Agent.html).

## Contribution

The documentation defines Jido's central architectural split: an immutable agent accepts an action or instruction through `cmd`, returns a complete new agent plus directives, and an `AgentServer` owns live state, signal delivery, and effect execution.

## Findings

The canonical flow is `Signal -> AgentServer -> route -> Agent.cmd -> {agent, directives} -> DirectiveExec`. The returned agent already contains every internal state transition; directives describe external runtime work and do not mutate agent state.

Actions can be pure or effectful. Jido locates its strong purity claim at the agent/strategy command boundary, not at every action implementation. It treats AI as an optional ecosystem layer rather than a prerequisite for the agent model.

Jido instances create separately supervised and registered runtime scopes. An agent value and its live server are distinct: the former is testable data and decision logic; the latter supplies time, concurrency, identity, delivery, and lifecycle.

## Relevance

This reducer-plus-effects boundary is the strongest candidate for a portable Wasm guest interface. It also identifies the services that cannot be supplied by a guest module alone.

## Limits

These are framework documentation and API contracts, not a formal semantics. Immediate I/O inside actions weakens replayability unless a Wasm adaptation narrows the effect model.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Jido architecture map](../10-maps/jido-agent-architecture.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
