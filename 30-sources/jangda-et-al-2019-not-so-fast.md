---
title: "Not So Fast: Analyzing the Performance of WebAssembly versus Native Code"
kind: source
created: "2026-08-07"
authors:
  - "Abhinav Jangda"
  - "Bobby Powers"
  - "Emery D. Berger"
  - "Arjun Guha"
published: 2019
citation_key: "jangda2019notsofast"
container: "2019 USENIX Annual Technical Conference"
edition: null
isbn: "978-1-939133-03-8"
doi: null
url: "https://www.usenix.org/conference/atc19/presentation/jangda"
accessed: "2026-08-07"
tags:
  - performance
  - webassembly
aliases: []
---

# Not So Fast: Analyzing the Performance of WebAssembly versus Native Code

## Reference

Abhinav Jangda et al. “Not So Fast: Analyzing the Performance of WebAssembly
vs. Native Code.” *USENIX ATC 2019*, pp. 107–120.
[Open-access paper](https://www.usenix.org/conference/atc19/presentation/jangda).

## Contribution

The paper challenges early near-native performance claims using substantial
SPEC CPU applications rather than small kernels.

## Method

Browsix-Wasm supplies missing Unix-like services so unmodified benchmark
applications can run in browsers. The authors compare native execution with
Chrome and Firefox Wasm and analyze generated code and platform constraints.

## Findings

The evaluated applications averaged 45% slower than native in Firefox and 55%
slower in Chrome, with larger peaks. Causes included engine code generation,
missing optimizations, bounds checks, register pressure, and platform limits.

## Relevance

“Near native” is not a requirement or portable constant. Agent WASM needs a
representative benchmark matrix spanning cold start, boundary crossings,
streaming, memory, and sustained compute on current runtimes.

## Limits

The results describe 2019 browsers, compilers, proposals, and a bespoke host
layer. They do not predict current Wasmtime, component, or edge performance.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
