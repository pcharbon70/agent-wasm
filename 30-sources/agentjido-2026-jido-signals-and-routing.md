---
title: "Jido Signals and Routing"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026signalsrouting"
container: "Jido and Jido Signal Documentation"
edition: "Jido 2.3.2; Jido Signal 2.2.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/signals.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Signals and Routing

## Reference

AgentJido. *Signals & Routing*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/signals.html), with the [Jido Signal package overview](https://jido-signal.hexdocs.pm/readme.html), accessed 7 August 2026.

## Contribution

The sources define the event envelope, type-pattern router, dispatch adapters, correlation model, and reliable bus features used between Jido components.

## Findings

Signals are based on CloudEvents 1.0.2 and carry type, source, optional subject and data, plus correlation and causation fields. Routing uses dot-separated patterns with single- and multi-segment wildcards.

Routes have explicit precedence: strategy routes outrank agent routes, which outrank plugin routes. Synchronous calls and asynchronous casts share routing but differ in the caller-facing result path.

Dispatch is separate from the signal value and can target processes, pub/sub, or webhooks. The signal package also offers persistent subscriptions with acknowledgement, in-flight and pending bounds, retry limits, and dead-letter handling.

## Relevance

The envelope is a practical language-neutral control message. A Wasm host can own delivery while guests consume and produce versioned values with correlation and causation intact.

## Limits

The core guide does not establish a universal end-to-end delivery guarantee. Transport adapters, persistent subscriptions, direct calls, and in-process casts have different failure modes that a new runtime must make explicit.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Jido architecture map](../10-maps/jido-agent-architecture.md)
