---
title: "Jido Persistence and Storage"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026persistencestorage"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/storage.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Persistence and Storage

## Reference

AgentJido. *Persistence & Storage*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/storage.html), accessed 7 August 2026.

## Contribution

The guide defines Jido's hibernate/thaw lifecycle and unified checkpoint-plus-journal storage contract.

## Findings

A Thread is an append-only log with monotonic sequence; a checkpoint is a serialized state snapshot containing a `{thread_id, thread_rev}` pointer rather than the full log. Late external metadata is appended as a follow-up fact rather than mutating history.

Hibernate flushes the journal before writing the checkpoint. Thaw loads and restores the checkpoint, loads the thread, and checks its revision. Storage exposes checkpoint CRUD and thread append/load/delete with optimistic concurrency. ETS, filesystem, and callback-based Redis adapters occupy different durability tiers.

Pods reuse ordinary checkpoints: durable topology survives, while live processes, monitors, and child handles are reconstructed.

## Relevance

The model transfers cleanly to a language-neutral host store. Snapshot format versioning, schema migration, and artifact identity must be added for guest portability.

## Limits

The guide does not promise an atomic transaction spanning state, journal, and arbitrary external directive effects. That gap matters for crash-safe Wasm execution.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
