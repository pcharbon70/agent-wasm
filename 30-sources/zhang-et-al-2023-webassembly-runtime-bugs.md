---
title: "Characterizing and Detecting WebAssembly Runtime Bugs"
kind: source
created: "2026-08-07"
authors:
  - "Yixuan Zhang"
  - "Shangtong Cao"
  - "Haoyu Wang"
  - "Zhenpeng Chen"
  - "Xiapu Luo"
  - "Dongliang Mu"
  - "Yun Ma"
  - "Gang Huang"
  - "Xuanzhe Liu"
published: 2023
citation_key: "zhang2023wasmruntimebugs"
container: "ACM Transactions on Software Engineering and Methodology 33(2)"
edition: null
isbn: null
doi: "10.1145/3624743"
url: "https://doi.org/10.1145/3624743"
accessed: "2026-08-07"
tags:
  - empirical-study
  - fuzzing
  - runtime
  - testing
  - webassembly
aliases: []
---

# Characterizing and Detecting WebAssembly Runtime Bugs

## Reference

Yixuan Zhang et al. “Characterizing and Detecting WebAssembly Runtime Bugs.”
*ACM Transactions on Software Engineering and Methodology* 33, no. 2 (2023):
1–29. DOI [10.1145/3624743](https://doi.org/10.1145/3624743).

## Research question

The study characterizes real runtime defects and asks whether a taxonomy-driven
framework can find new ones.

## Method

The authors manually analyze 311 bugs, derive 31 categories, and build detection
strategies from the observed triggers and symptoms. The final evaluation
applies the framework to seven runtimes.

## Findings

The evaluation reports 60 newly found bugs, of which 13 were confirmed and nine
fixed by publication. The taxonomy spans parsing and validation, execution,
APIs, platform and architecture behavior, resource management, and other
runtime-specific paths.

The result supports directed generation based on empirical failure modes, while
the large gap between generated reports and confirmed fixes also reinforces
the need to reduce, deduplicate, and manually validate findings.

## Relevance

Agent WASM's engine matrix should be informed by observed bug families and
should preserve runtime version, target architecture, features, and embedding
configuration with every failure.

## Limits

Public issue data and project selection introduce reporting bias. Confirmation
counts are a lower bound, and older runtime versions may not represent present
implementations.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Testing and verification map](../10-maps/webassembly-testing-and-verification.md)
