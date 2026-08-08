---
title: "WarpDiff"
kind: source
created: "2026-08-07"
authors:
  - "Shuyao Jiang"
  - "Ruiying Zeng"
  - "Zihao Rao"
  - "Jiazhen Gu"
  - "Yangfan Zhou"
  - "Michael R. Lyu"
published: 2023
citation_key: "jiang2023warpdiff"
container: "2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)"
edition: null
isbn: null
doi: "10.1109/ASE56229.2023.00088"
url: "https://doi.org/10.1109/ASE56229.2023.00088"
accessed: "2026-08-07"
tags:
  - differential-testing
  - performance
  - runtime
  - testing
  - webassembly
aliases:
  - "Revealing Performance Issues in Server-Side WebAssembly Runtimes Via Differential Testing"
---

# WarpDiff

## Reference

Shuyao Jiang et al. “Revealing Performance Issues in Server-Side WebAssembly
Runtimes Via Differential Testing.” *ASE 2023*, 661–672. DOI
[10.1109/ASE56229.2023.00088](https://doi.org/10.1109/ASE56229.2023.00088).

## Contribution

WarpDiff applies differential testing to performance rather than only semantic
correctness. It looks for abnormal runtime timing ratios across engines and
then analyzes outliers.

## Method

The evaluation executes 123 LLVM test-suite programs on five server-side Wasm
runtimes. A statistical differential oracle ranks inconsistent performance for
investigation.

## Findings

The paper reports seven confirmed performance issues. Its main methodological
contribution is using independent runtimes as relative evidence when no single
absolute timing oracle exists.

## Relevance

Agent WASM can use ratio-based alerts for cold compilation, instantiation, and
turn execution across Extism runtime families. Performance disagreement must
remain separate from semantic disagreement and should trigger investigation,
not automatically fail conformance.

## Limits

Timing is sensitive to hardware, load, compiler tiering, cache state, and
runtime defaults. The LLVM programs are not representative of stateful agent
turns, serialization, policy checks, or host effects.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
