---
title: "Bringing the WebAssembly Standard Up to Speed with SpecTec"
kind: source
created: "2026-08-07"
authors:
  - "Dongjun Youn"
  - "Shin Wonho"
  - "Jaehyun Lee"
  - "Sukyoung Ryu"
  - "Joachim Breitner"
  - "Philippa Gardner"
  - "Sam Lindley"
  - "Matija Pretnar"
  - "Xiaojia Rao"
  - "Conrad Watt"
  - "Andreas Rossberg"
published: 2024
citation_key: "youn2024spectec"
container: "Proceedings of PLDI 2024"
edition: null
isbn: null
doi: "10.1145/3656440"
url: "https://doi.org/10.1145/3656440"
accessed: "2026-08-07"
tags:
  - formal-methods
  - specification
  - webassembly
aliases: []
---

# Bringing the WebAssembly Standard Up to Speed with SpecTec

## Reference

Dongjun Youn et al. “Bringing the WebAssembly Standard Up to Speed with
SpecTec.” *PLDI 2024*. DOI [10.1145/3656440](https://doi.org/10.1145/3656440).

## Contribution

SpecTec is a domain-specific language intended to make formal Wasm semantics a
single source for generated prose specification and executable artifacts.

## Method

The authors encode Wasm 2.0, generate a typeset specification and meta-level
interpreter, run applicable official tests, and replay historical and current
proposal errors.

## Findings

The generated interpreter passed all applicable official tests. SpecTec caught
historical specification defects and ten errors across five proposals prepared
for the next language version. The paper argues that redundant handwritten
rules no longer scale with the language.

## Relevance

Agent WASM should consider executable generation and cross-artifact consistency
early if it defines its own component profiles, capabilities, or conformance
rules. A validator is helpful, but generated shared semantics can prevent a
larger class of drift.

## Limits

At publication, theorem-prover and test-generation backends were future work.
Passing existing tests does not by itself prove the generated semantics or
every proposal correct.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
