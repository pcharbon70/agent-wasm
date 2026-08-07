---
title: "Extism Host Function Namespaces"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026eip002"
container: "Extism Improvement Proposals"
edition: "EIP-002"
isbn: null
doi: null
url: "https://github.com/extism/proposals/blob/main/EIP-002-module-namespace-for-host-functions.md"
accessed: "2026-08-07"
tags:
  - extism
  - specification
  - webassembly
aliases: []
---

# Extism Host Function Namespaces

## Reference

Extism Project. *Module Namespace for Host Functions*. EIP-002.
[Proposal](https://github.com/extism/proposals/blob/main/EIP-002-module-namespace-for-host-functions.md),
accessed 7 August 2026.

## Contribution

EIP-002 assigns explicit Wasm import-module namespaces to built-in and
application-defined host functions.

## Findings

Extism built-ins use `extism:host/env`; user-defined host functions default to
`extism:host/user`, although a host can configure another namespace. Explicit
namespaces make dependencies visible, avoid collisions, and leave room for
other import families such as WASI.

## Relevance

The namespace split distinguishes Extism's runtime protocol from the
application capability surface and supports import auditing before a plug-in
is admitted.

## Limits

The naming is described as component-model-friendly, but these are core-Wasm
import module strings, not WIT interfaces or Component Model worlds. A name
does not express payload schemas, authorization, or behavioral semantics.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
