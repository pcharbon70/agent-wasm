---
title: "Jido AI Runtime"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026airuntime"
container: "Jido AI v2.3.0 Documentation"
edition: "2.3.0"
isbn: null
doi: null
url: "https://jido-ai.hexdocs.pm/readme.html"
accessed: "2026-08-07"
tags:
  - agent-tools
  - jido
  - runtime
aliases: []
---

# Jido AI Runtime

## Reference

AgentJido. *Jido.AI*. [Jido AI v2.3.0 documentation](https://jido-ai.hexdocs.pm/readme.html), accessed 7 August 2026.

## Contribution

The package adds model routing, reasoning strategies, tool registration, request concurrency, retries, and observability above the Jido core.

## Findings

Jido AI projects structured Jido actions into model-callable tools and supplies ReAct and other reasoning strategies. Model access, routing, retrieval, quota, request lifecycle, and provider behavior are runtime-layer concerns. The core Jido package remains useful without AI.

Tool results can update structured agent state, allowing subsequent request construction to read an explicit projection instead of scraping conversational text.

## Relevance

An Agent Wasm core should not bake a model provider into the guest ABI. Model calls should be host-governed capabilities or durable request/result effects, while a reasoning strategy may remain portable guest logic.

## Limits

The package overview establishes component roles but is not a complete account of every strategy's algorithm or provider-level security and delivery semantics.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
