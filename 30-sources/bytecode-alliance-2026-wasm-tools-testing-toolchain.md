---
title: "wasm-tools Generation, Mutation, and Reduction"
kind: source
created: "2026-08-07"
authors:
  - "Bytecode Alliance"
published: null
citation_key: "bytecodealliance2026wasmtools"
container: "wasm-tools Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/bytecodealliance/wasm-tools"
accessed: "2026-08-07"
tags:
  - fuzzing
  - testing
  - tooling
  - webassembly
aliases:
  - "wasm-smith, wasm-mutate, and wasm-shrink"
---

# wasm-tools Generation, Mutation, and Reduction

## Reference

Bytecode Alliance. *wasm-tools*, especially
[`wasm-smith`](https://github.com/bytecodealliance/wasm-tools/tree/main/crates/wasm-smith),
[`wasm-mutate`](https://github.com/bytecodealliance/wasm-tools/tree/main/crates/wasm-mutate),
and
[`wasm-shrink`](https://github.com/bytecodealliance/wasm-tools/tree/main/crates/wasm-shrink).
Official repository, accessed 7 August 2026.

## Contribution

The three tools form a reusable fuzzing loop for Wasm consumers: generate
structured modules, diversify existing modules, and minimize a failure while
preserving an external interestingness predicate.

## Findings

`wasm-smith` deterministically maps arbitrary bytes to valid modules and is
designed to reach past parsers and validators into compilers and runtimes.
`wasm-mutate` applies deterministic transformations and can restrict itself to
semantics-preserving changes. `wasm-shrink` repeatedly evaluates a caller-
supplied predicate to produce a smaller reproducer.

These roles are complementary. Generation explores broad feature combinations;
mutation preserves useful structure from real seeds; reduction turns an
unwieldy discovery into a regression test. None supplies the oracle: the test
designer must define crashes, result disagreement, invariant violation, or
another observable failure.

## Relevance

Agent WASM can seed these tools with compiled reducers and protocol fixtures,
but must add an application-aware oracle that compares validated turn results
and host state rather than raw engine output alone.

## Limits

Validity is relative to a configured feature set. Semantics-preserving mutation
also depends on the transformation model and does not preserve application
metadata, signatures, or host-side protocol meaning automatically.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
