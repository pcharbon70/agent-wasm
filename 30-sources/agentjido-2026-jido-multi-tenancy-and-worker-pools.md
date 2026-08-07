---
title: "Jido Multi-Tenancy and Worker Pools"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026tenancypools"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/multi-tenancy.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
  - security
aliases: []
---

# Jido Multi-Tenancy and Worker Pools

## Reference

AgentJido. *Multi-Tenancy* and *Worker Pools*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/multi-tenancy.html), including the [worker-pool guide](https://jido.hexdocs.pm/worker-pools.html), accessed 7 August 2026.

## Contribution

The guides distinguish hard runtime isolation from logical namespacing and document the state-reuse risks of pre-warmed agents.

## Findings

Separate Jido instances are recommended for hard or operational isolation. A shared instance partition namespaces registry identity, storage, lineage, and telemetry but remains a logical boundary, with raw process references as an escape hatch.

Worker pools bound concurrency and reduce startup latency, but checked-out agents retain state between borrowers unless explicitly reset. Asynchronous casts are especially hazardous because the pool can check an agent back in before its work completes.

## Relevance

Wasm linear memory and Extism variables also persist across calls to a reused instance. A secure design should share compiled artifacts, not mutable guest instances, across tenants; instance pools need reset proofs or fresh instantiation.

## Limits

The pool guidance describes Jido process reuse rather than engine-level Wasm pooling. The analogy is architectural and must be tested against each Extism runtime's reset and concurrency behavior.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
