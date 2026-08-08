---
title: "Security and Correctness in Wasmtime"
kind: source
created: "2026-08-07"
authors:
  - "Nick Fitzgerald"
published: "2022-09-13"
citation_key: "fitzgerald2022securitycorrectness"
container: "Bytecode Alliance"
edition: null
isbn: null
doi: null
url: "https://bytecodealliance.org/articles/security-and-correctness-in-wasmtime"
accessed: "2026-08-07"
tags:
  - fuzzing
  - security
  - testing
  - verification
  - webassembly
aliases: []
---

# Security and Correctness in Wasmtime

## Reference

Nick Fitzgerald. “Security and Correctness in Wasmtime.” *Bytecode Alliance*,
13 September 2022.
[Official article](https://bytecodealliance.org/articles/security-and-correctness-in-wasmtime).

## Contribution

The article explains the engineering argument behind Wasmtime's combination of
memory-safe implementation, ubiquitous fuzzing, formal verification, and
disposable runtime instances.

## Findings

Wasmtime fuzzes malformed bytes as well as structured valid modules generated
by `wasm-smith`. Its oracles compare optimized with unoptimized execution,
Wasmtime with V8 or the specification interpreter, and compiler results with a
symbolic register-allocation checker. Continuous jobs run through OSS-Fuzz,
while feature development also uses targeted fuzzing.

The article carefully limits the claim: fuzzing supplies statistical evidence
over exercised inputs, whereas a proof can quantify over all modeled inputs but
only for the modeled component and assumptions. Disposable instances reduce
the amount of mutable state that must be returned to a safe baseline.

## Relevance

The same complementarity should guide Agent WASM: tests and fuzzing for broad
behavior, small formal models for state/effect invariants, and fresh instances
until reset and pooling are independently demonstrated safe.

## Limits

This is a project-maintainer account, not an independent evaluation. It
describes the assurance strategy as of 2022 and does not prove that every
configuration or target architecture receives equal coverage.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
