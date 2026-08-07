---
title: "Jido Runtime and Coordination"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026runtimecoordination"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/runtime.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Runtime and Coordination

## Reference

AgentJido. *Runtime*, *Await & Coordination*, and *Multi-Agent Orchestration*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/runtime.html), including the [coordination guide](https://jido.hexdocs.pm/await.html), accessed 7 August 2026.

## Contribution

The guides describe the live actor shell around immutable agents: signal serialization, plugin phases, routing, directive draining, logical parent-child relationships, completion, cancellation, and fan-out/fan-in.

## Findings

An `AgentServer` owns one live agent, serializes its turns, queues directives, executes effects, and routes result-bearing instructions back through `cmd`. Security-sensitive preparation occurs before route execution, with runtime context kept separate from signal and action data.

Logical parent-child relationships are tracked with references and monitors but are not nested supervision trees; live agents are peers under instance supervision. Parent death behavior is an explicit domain policy. Cancellation is advisory and delivered as a signal. Completion is a terminal state, while process death is an infrastructure event.

## Relevance

These are the responsibilities of a Wasm host actor cell, not a guest. Wasm supplies isolated computation; it does not supply mailboxes, monitors, registries, supervision, or durable coordination.

## Limits

The guides assume single-node BEAM process primitives. Distributed ordering, partitions, exactly-once processing, and cross-host supervision are outside the documented model.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Jido architecture map](../10-maps/jido-agent-architecture.md)
