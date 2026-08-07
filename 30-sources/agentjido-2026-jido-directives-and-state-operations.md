---
title: "Jido Directives and State Operations"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026directivesstateops"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/directives.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Directives and State Operations

## Reference

AgentJido. *Directives* and *State Operations*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/directives.html), including the [directive API](https://jido.hexdocs.pm/Jido.Agent.Directive.html), accessed 7 August 2026.

## Contribution

The guides distinguish internal state transitions from externally interpreted effects and catalog the runtime command vocabulary.

## Findings

State operations are applied by the strategy before `cmd` returns. Directives pass through to the runtime. Built-ins cover emission, errors, generic tasks, tracked child agents and adoption, sensors, timers and cron, continuation instructions, child and self termination.

Directive execution is open to custom types through `Jido.AgentServer.DirectiveExec`. Its outcomes include success, asynchronous work, and hard stop; a hard stop drops queued directives and can orphan in-flight work.

Normal workflow completion is represented in agent state rather than by process termination. That separates a domain outcome from runtime liveness.

## Relevance

This is the basis for a typed effect algebra at the Wasm boundary. State patches can be validated and committed before the host interprets capability requests.

## Limits

Jido's in-process queue is not a transactional outbox. A durable cross-process implementation must add effect identifiers, commit ordering, replay, and idempotency rules.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
