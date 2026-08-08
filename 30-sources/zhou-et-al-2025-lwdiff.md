---
title: "LWDIFF"
kind: source
created: "2026-08-07"
authors:
  - "Shiyao Zhou"
  - "Jincheng Wang"
  - "He Ye"
  - "Hao Zhou"
  - "Claire Le Goues"
  - "Xiapu Luo"
published: 2025
citation_key: "zhou2025lwdiff"
container: "2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)"
edition: null
isbn: null
doi: "10.1109/ICSE55347.2025.00233"
url: "https://doi.org/10.1109/ICSE55347.2025.00233"
accessed: "2026-08-07"
tags:
  - differential-testing
  - fuzzing
  - runtime
  - testing
  - webassembly
aliases:
  - "LLM-Assisted Differential Testing Framework for WebAssembly Runtimes"
---

# LWDIFF

## Reference

Shiyao Zhou, Jincheng Wang, He Ye, Hao Zhou, Claire Le Goues, and Xiapu Luo.
“LWDIFF: An LLM-Assisted Differential Testing Framework for WebAssembly
Runtimes.” *ICSE 2025*, 153–164. DOI
[10.1109/ICSE55347.2025.00233](https://doi.org/10.1109/ICSE55347.2025.00233).

## Contribution

LWDIFF uses an LLM to extract specification knowledge and propose mutation
operators spanning decoding, validation, and execution, then relies on
cross-runtime execution rather than the model to decide whether behaviors
diverge.

## Method

Generated and mutated cases are executed across eight runtimes. Differential
results are filtered and submitted to maintainers for confirmation.

## Findings

The paper reports 31 confirmed bugs, 25 of them previously unknown. Its design
is important because the probabilistic component proposes tests while a
deterministic execution harness supplies the evidence.

## Relevance

LLMs could derive Agent WASM negative cases from protocol schemas and prose,
but generated cases should enter the same reproducible, cross-runtime,
application-aware oracle as hand-authored vectors. Model judgment must not be
the conformance verdict.

## Limits

Specification extraction may omit or distort rules, and runtime consensus can
agree on the same defect. Confirmed bug counts do not establish completeness or
the marginal value of the LLM over equally funded manual operator design.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
