---
title: "Wasm-Mutate"
kind: source
created: "2026-08-07"
authors:
  - "Javier Cabrera-Arteaga"
  - "Nicholas Fitzgerald"
  - "Martin Monperrus"
  - "Benoit Baudry"
published: 2024
citation_key: "cabreraarteaga2024wasmmutate"
container: "Computers & Security 139"
edition: null
isbn: null
doi: "10.1016/j.cose.2024.103731"
url: "https://doi.org/10.1016/j.cose.2024.103731"
accessed: "2026-08-07"
tags:
  - fuzzing
  - mutation-testing
  - security
  - testing
  - webassembly
aliases:
  - "Fast and effective binary diversification for WebAssembly"
---

# Wasm-Mutate

## Reference

Javier Cabrera-Arteaga, Nicholas Fitzgerald, Martin Monperrus, and Benoit
Baudry. “Wasm-Mutate: Fast and Effective Binary Diversification for
WebAssembly.” *Computers & Security* 139 (2024): 103731. DOI
[10.1016/j.cose.2024.103731](https://doi.org/10.1016/j.cose.2024.103731).

## Contribution

The work introduces fast semantics-preserving diversification of Wasm binaries,
implemented by the `wasm-mutate` tool and motivated by security diversity and
testing.

## Method

The transformation engine combines peephole rewrites represented with equality
saturation and structural mutations. The evaluation uses 404 programs and
measures generation rate, diversity, correctness, and security applications.

## Findings

The paper reports that tens of thousands of diverse variants can be generated
within minutes. Semantics-preserving variants can stress different compiler
and runtime paths while retaining an expected result oracle.

## Relevance

For Agent WASM, compiled reducer fixtures can be diversified to expose engine
and optimizer sensitivity without changing their turn results. Artifact hashes
will change, so test identity must distinguish semantic fixture identity from
binary identity.

## Limits

Preservation is defined at the Wasm program level. Custom sections, signatures,
resource use, timing, and host-call traces may change or require separate
checks, so variants are not interchangeable production artifacts.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [wasm-tools testing toolchain](bytecode-alliance-2026-wasm-tools-testing-toolchain.md)
