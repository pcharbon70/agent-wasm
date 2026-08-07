---
title: "Extism Host Functions"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismhostfunctions"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/host-functions/"
accessed: "2026-08-07"
tags:
  - extism
  - plugin-system
  - security
aliases: []
---

# Extism Host Functions

## Reference

Dylibso. *Host Functions*. [Extism documentation](https://extism.org/docs/concepts/host-functions/),
accessed 7 August 2026.

## Contribution

The page defines the mechanism by which a host injects application functions
as Wasm imports, giving a plug-in capabilities beyond Extism's built-ins.

## Findings

A host function has a name, core-Wasm parameter and result types, and optional
opaque user data. Complex values are normally represented by 64-bit offsets
into Extism-managed memory, which the host reads and writes through a
`CurrentPlugin` view. The guest must declare matching imports and every import
must be satisfied at instantiation.

User data must outlive the associated plug-in. If plug-ins are pooled or
shared across threads, the data and callback implementation must be safe for
concurrent access.

## Relevance

Host functions are Extism's application capability boundary. For agents, they
would mediate databases, credentials, model calls, tool dispatch, state, and
other privileged effects.

## Limits

Core Wasm value signatures do not describe semantic authorization or rich
payload schemas. A narrow import name can still implement broad authority, and
the host must validate pointers, lengths, structured inputs, outputs, caller
identity, and reentrancy behavior.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
