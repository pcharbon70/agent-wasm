---
title: "Extism Plug-in System Concepts"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismpluginsystem"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/plug-in-system/"
accessed: "2026-08-07"
tags:
  - extism
  - plugin-system
  - webassembly
aliases: []
---

# Extism Plug-in System Concepts

## Reference

Dylibso. *Plug-in System*. [Extism documentation](https://extism.org/docs/concepts/plug-in-system/),
accessed 7 August 2026. Read with the official
[plug-in](https://extism.org/docs/concepts/plug-in/),
[Host SDK](https://extism.org/docs/concepts/host-sdk/), and
[PDK](https://extism.org/docs/concepts/pdk/) concept pages.

## Contribution

The concept set defines Extism's roles: the host owns an extension point, a
plug-in is a Wasm module conforming to that interface, a Host SDK embeds and
manages it, and a PDK compiles guest-language code against the Extism contract.

## Findings

Extism's portability claim has two axes: plug-ins can be authored in different
languages and hosts can be written in different languages. The common meeting
point is a core Wasm module with exported plug-in functions and imported
Extism, WASI, or user host functions.

Core Wasm begins without filesystem, process-memory, database, or application
access. The host selectively supplies such capabilities through imports. That
makes the host's linker and policy configuration part of the security
boundary, not merely integration glue.

## Relevance

This source establishes the vocabulary and top-level control split used in the
Extism architecture synthesis.

## Limits

The pages are explanatory product documentation, not a formal conformance
specification. Their broad portability and safety claims require qualification
by implementation source, runtime-specific feature support, and adversarial
tests.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
