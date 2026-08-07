---
title: "Extism Chicory SDK"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026chicorysdk"
container: "Extism Source Repository"
edition: "experimental"
isbn: null
doi: null
url: "https://github.com/extism/chicory-sdk"
accessed: "2026-08-07"
tags:
  - embedded-systems
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism Chicory SDK

## Reference

Extism Project. *Chicory SDK*.
[Source repository](https://github.com/extism/chicory-sdk), accessed 7 August
2026.

## Contribution

The Chicory SDK is an independent, zero-native-dependency Java implementation
of Extism over the JVM-native Chicory Wasm runtime.

## Findings

It instantiates the shared kernel, links Extism built-ins and user functions,
supports multi-module dependency linking, provides Extism HTTP adapters, and
can add Chicory's WASI Preview 1 implementation. A machine factory lets hosts
select Chicory execution machinery, including cached AOT compilation paths in
the codebase.

The implementation is attractive where loading `libextism` is undesirable,
including Android-oriented environments.

## Relevance

It supplies a fourth engine family and tests whether the Extism protocol works
in a managed, JVM-native deployment.

## Limits

The project explicitly labels itself and Chicory experimental and directs
users seeking the established Java route to the native Java SDK. Its feature,
performance, proposal, limit, timeout, and WASI parity must be established
before production use.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
