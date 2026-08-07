---
title: "Mechanising and Verifying the WebAssembly Specification"
kind: source
created: "2026-08-07"
authors:
  - "Conrad Watt"
published: 2018
citation_key: "watt2018mechanising"
container: "Proceedings of CPP 2018"
edition: null
isbn: "978-1-4503-5586-5"
doi: "10.1145/3167082"
url: "https://doi.org/10.1145/3167082"
accessed: "2026-08-07"
tags:
  - formal-methods
  - webassembly
aliases: []
---

# Mechanising and Verifying the WebAssembly Specification

## Reference

Conrad Watt. “Mechanising and Verifying the WebAssembly Specification.”
*CPP 2018*. DOI [10.1145/3167082](https://doi.org/10.1145/3167082).

## Contribution

The paper presents an Isabelle mechanization, verified executable interpreter
and type checker, and mechanized type-soundness proof for early WebAssembly.

## Method

Watt formalizes syntax, typing, and reduction in Isabelle; proves preservation
and progress-style results; extracts executable artifacts; and differentially
fuzzes the interpreter against industry implementations.

## Findings

Mechanization exposed defects and ambiguities in the handwritten official
specification and influenced its development. The work demonstrates both the
value of Wasm's formal design and the gap between readable prose rules and a
maintained machine-checked source of truth.

## Relevance

Agent WASM should distinguish normative text, executable models, tests, and
implementations, then cross-check them rather than treating any one executable
artifact as infallible.

## Limits

The mechanization targets an early language version and does not cover today's
full Core 3.0, Component Model, WASI, or host capability policy.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
