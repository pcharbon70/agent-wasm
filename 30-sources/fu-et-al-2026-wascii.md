---
title: "WASCII"
kind: source
created: "2026-08-07"
authors:
  - "Yeqi Fu"
  - "Kaihang Ji"
  - "Yuanpeng Wang"
  - "Zong Cao"
  - "Jiahao Liu"
  - "Ding Li"
  - "Yao Guo"
  - "Zhenkai Liang"
published: 2026
citation_key: "fu2026wascii"
container: "ISSTA 2026 Research Papers"
edition: null
isbn: null
doi: null
url: "https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/61/WASCII-Bridging-WebAssembly-Specifications-and-Implementations-through-LLM-Enhanced-Valid"
accessed: "2026-08-07"
tags:
  - conformance
  - differential-testing
  - testing
  - webassembly
aliases:
  - "Bridging WebAssembly Specifications and Implementations through LLM-Enhanced Validation"
---

# WASCII

## Reference

Yeqi Fu et al. “WASCII: Bridging WebAssembly Specifications and
Implementations through LLM-Enhanced Validation.” Accepted for the ISSTA 2026
research track, scheduled for October 2026.
[Official conference abstract](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/61/WASCII-Bridging-WebAssembly-Specifications-and-Implementations-through-LLM-Enhanced-Valid),
accessed 7 August 2026. Publication and DOI metadata were not yet shown.

## Contribution

WASCII converts natural-language validation requirements into a structured
“Check Tree,” aligns implementation code to it, validates generated cases by
execution in a clean-room process, and uses cross-runtime differential testing
to expose inconsistencies.

## Method

The conference abstract reports evaluation against seven major runtimes. The
LLM-assisted bridge is not trusted directly; execution validates candidate
tests before differential comparison.

## Findings

The accepted-paper abstract reports 209 differential behaviors, including 33
confirmed previously unknown conformance issues and 18 already fixed. These
figures are pre-proceedings claims at this archive's access date.

## Relevance

The Check Tree idea could make Agent WASM protocol clauses traceable to
positive and negative vectors. It also reinforces that generated tests need
execution-backed validation and independent human-readable traceability.

## Limits

Only the official abstract and conference metadata were available before the
scheduled conference. Detailed methodology, artifacts, false-positive
handling, and reproducibility should be reassessed when the paper and
proceedings appear.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
