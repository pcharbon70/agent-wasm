---
title: "An Empirical Study of Bugs in WebAssembly Compilers"
kind: source
created: "2026-08-07"
authors:
  - "Alan Romano"
  - "Xinyue Liu"
  - "Yonghwi Kwon"
  - "Weihang Wang"
published: 2021
citation_key: "romano2021wasmbugs"
container: "2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE)"
edition: null
isbn: null
doi: "10.1109/ASE51524.2021.9678776"
url: "https://doi.org/10.1109/ASE51524.2021.9678776"
accessed: "2026-08-07"
tags:
  - compilers
  - empirical-study
  - testing
  - webassembly
aliases: []
---

# An Empirical Study of Bugs in WebAssembly Compilers

## Reference

Alan Romano, Xinyue Liu, Yonghwi Kwon, and Weihang Wang. “An Empirical
Study of Bugs in WebAssembly Compilers.” *ASE 2021*, 42–54. DOI
[10.1109/ASE51524.2021.9678776](https://doi.org/10.1109/ASE51524.2021.9678776).

## Research question

The paper asks how WebAssembly compiler bugs manifest, how they are found and
fixed, and how they differ across prominent source-to-Wasm toolchains.

## Method

The authors qualitatively classify 146 Emscripten bugs and quantitatively study
1,316 bugs from AssemblyScript, Binaryen, Emscripten, and wasm-bindgen. Their
dimensions include lifecycle, impact, triggering inputs, and fixes.

## Findings

The study establishes the compiler pipeline as a separate defect surface from
the runtime. Front ends, glue generation, optimization, linking, and source-
language interoperability can corrupt behavior even when the resulting module
validates and the engine executes it correctly.

The authors' taxonomy and corpus support test generation targeted at recurring
compiler failure patterns instead of relying only on generic random bytes.

## Relevance

Agent WASM must identify guest compiler and PDK versions in every artifact and
run reducer-level golden tests after compilation. Cross-runtime agreement
cannot detect a compiler that produced the same wrong module for both engines.

## Limits

Issue trackers reflect reported and triaged defects, not all defects. The study
predates current Component Model, WASI, and Extism toolchains, so its categories
transfer more reliably than its project-specific frequencies.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
