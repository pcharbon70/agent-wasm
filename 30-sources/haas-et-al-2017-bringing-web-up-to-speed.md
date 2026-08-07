---
title: "Bringing the Web Up to Speed with WebAssembly"
kind: source
created: "2026-08-07"
authors:
  - "Andreas Haas"
  - "Andreas Rossberg"
  - "Derek L. Schuff"
  - "Ben L. Titzer"
  - "Michael Holman"
  - "Dan Gohman"
  - "Luke Wagner"
  - "Alon Zakai"
  - "J. F. Bastien"
published: 2017
citation_key: "haas2017wasm"
container: "Proceedings of PLDI 2017"
edition: null
isbn: "978-1-4503-4988-8"
doi: "10.1145/3062341.3062363"
url: "https://doi.org/10.1145/3062341.3062363"
accessed: "2026-08-07"
tags:
  - language-design
  - webassembly
aliases: []
---

# Bringing the Web Up to Speed with WebAssembly

## Reference

Andreas Haas et al. “Bringing the Web Up to Speed with WebAssembly.”
*PLDI 2017*, pp. 185–200. DOI [10.1145/3062341.3062363](https://doi.org/10.1145/3062341.3062363).

## Contribution

The founding design paper motivates Wasm as safe, fast, portable low-level code
and presents its compact encoding, validation, formal semantics, and early
multi-browser implementation experience.

## Method

The authors derive design constraints from earlier web execution technologies,
describe the abstract machine and type system, and report prototype size,
compilation, and execution measurements from browser-vendor implementations.

## Findings

Structured control flow and explicit types enable single-pass validation and
streaming compilation. Wasm is deliberately an abstraction over common
hardware rather than a source language, object format, or operating-system
interface. Safety depends on validation, isolated runtime state, checked linear
memory, constrained indirect calls, and the embedder boundary.

## Relevance

The paper explains which properties are architectural and which belong to an
embedding. Agent WASM should preserve that separation instead of placing agent
policy into the core execution model.

## Limits

The evaluation predates mature WASI, components, current proposals, standalone
runtimes, and modern workloads. Its early performance results are historical,
not a current runtime comparison.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
