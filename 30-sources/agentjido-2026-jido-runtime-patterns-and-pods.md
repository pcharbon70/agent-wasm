---
title: "Jido Runtime Patterns and Pods"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026runtimepatternspods"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/runtime-patterns.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Runtime Patterns and Pods

## Reference

AgentJido. *Choosing a Runtime Pattern* and *Pods*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/runtime-patterns.html), including the [Pods guide](https://jido.hexdocs.pm/pods.html), accessed 7 August 2026.

## Contribution

The guides separate lifecycle selection from tenancy and define Pods as durable, named, declarative multi-agent topology.

## Findings

Jido distinguishes a live agent, a tracked live child, a durable keyed agent, and a durable named team. A partition namespaces any of those choices but does not determine lifecycle.

A Pod is an ordinary agent with reserved plugin state containing a topology of nodes and links. Dependencies and ownership determine reconcile order; nodes can activate eagerly or lazily; nested pods recurse. Durable state stores topology and member checkpoints, never live process identifiers or monitors. Reconciliation repairs the live shape after thaw.

## Relevance

This is a direct model for Wasm orchestration: persist an artifact-and-identity graph, instantiate execution cells on demand, and reconcile runtime handles from durable intent.

## Limits

The documented Pod model is single-instance and single-node, not a distributed consensus or cluster scheduler. Cycles are rejected, but broader partial-failure and split-brain semantics remain outside scope.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Jido architecture map](../10-maps/jido-agent-architecture.md)
