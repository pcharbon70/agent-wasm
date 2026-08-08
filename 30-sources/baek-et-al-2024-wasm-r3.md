---
title: "Wasm-R3"
kind: source
created: "2026-08-07"
authors:
  - "Doehyun Baek"
  - "Jakob Getz"
  - "Yusung Sim"
  - "Daniel Lehmann"
  - "Ben L. Titzer"
  - "Sukyoung Ryu"
  - "Michael Pradel"
published: 2024
citation_key: "baek2024wasmr3"
container: "Proceedings of the ACM on Programming Languages 8 (OOPSLA2)"
edition: null
isbn: null
doi: "10.1145/3689787"
url: "https://doi.org/10.1145/3689787"
accessed: "2026-08-07"
tags:
  - record-replay
  - testing
  - webassembly
aliases:
  - "Record-Reduce-Replay for Realistic and Standalone WebAssembly Benchmarks"
---

# Wasm-R3

## Reference

Doehyun Baek et al. “Wasm-R3: Record-Reduce-Replay for Realistic and Standalone
WebAssembly Benchmarks.” *Proceedings of the ACM on Programming Languages* 8,
OOPSLA2 (2024): 2156–2182. DOI
[10.1145/3689787](https://doi.org/10.1145/3689787).

## Contribution

Wasm-R3 captures the interaction of a real Wasm application with its host,
reduces that record, and emits a standalone module that replays the observed
execution across engines.

## Method

The system instruments applications, records host interactions, reduces traces
while preserving behavior, and packages replay logic. The evaluation derives a
27-application benchmark suite from realistic web applications.

## Findings

The paper reports a 99.53% trace-size reduction and a 9.98% replay benchmark
size reduction while retaining standalone, cross-engine workloads. It addresses
a central differential-testing obstacle: realistic programs commonly depend on
browser or host APIs unavailable in another engine.

## Relevance

Agent WASM can adapt the record/replay idea to Extism imports and directive
results. A captured turn could become a portable engine fixture, provided
secrets are redacted and nondeterministic inputs are made explicit.

## Limits

Replaying a recorded interaction explores one observed path and can hide live
host races, authorization behavior, crashes, and external effect semantics.
Recorded production inputs also create privacy and provenance obligations.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
