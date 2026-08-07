---
title: "Extism Java SDK"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026javasdk"
container: "Extism Source Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/extism/java-sdk"
accessed: "2026-08-07"
tags:
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism Java SDK

## Reference

Extism Project. *Extism Java SDK*.
[Source repository](https://github.com/extism/java-sdk), accessed 7 August
2026.

## Contribution

The established Java Host SDK is a Java API over the native Extism shared
library.

## Findings

Users install `libextism` separately and add the Java package. Plug-in
construction, calls, state, configuration, and Java host functions map onto
the reference C API. The actual Wasm engine is therefore Wasmtime inside the
Rust runtime, not a JVM-native engine.

## Relevance

This distinguishes Java language ergonomics from execution-engine identity.
It is the mature Java route when native libraries are acceptable.

## Limits

The deployment inherits native target availability, FFI/JNA boundaries, and
the reference runtime's Wasmtime semantics. It is not suitable for every
Android or native-library-restricted environment.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
