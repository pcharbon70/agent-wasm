---
title: "Extism Plug-in Language and PDK Guide"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismpluginquickstart"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/quickstart/plugin-quickstart/"
accessed: "2026-08-07"
tags:
  - extism
  - plugin-system
  - webassembly
aliases: []
---

# Extism Plug-in Language and PDK Guide

## Reference

Dylibso. *Write a Plug-in*. [Extism documentation](https://extism.org/docs/quickstart/plugin-quickstart/),
accessed 7 August 2026.

## Contribution

The guide records the supported guest-language toolchains and shows how each
PDK lowers idiomatic source functions into the Extism export and memory
conventions.

## Findings

The documented PDK languages are Rust, JavaScript/TypeScript, Go, C#, F#, C,
Haskell, Zig, and AssemblyScript. Rust can target `wasm32-unknown-unknown` when
it needs no WASI. The documented JavaScript and Go guest toolchains currently
require WASI; .NET and Haskell also use WASI-oriented toolchains. C, Zig, and
AssemblyScript examples can produce smaller core modules without WASI.

Across languages, an exported function ultimately takes no core-Wasm
parameters, communicates through Extism memory, and returns zero or an `i32`
status. Macros, annotations, compiler drivers, and PDK helpers hide different
amounts of that ABI.

## Relevance

Guest language choice changes module size, startup requirements, WASI imports,
runtime initialization, and portability even though the public Host SDK call
looks the same.

## Limits

The quickstart is a current toolchain guide, not a compatibility guarantee.
Compiler and PDK versions, required Wasm proposals, and WASI dependencies must
be captured per artifact.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
