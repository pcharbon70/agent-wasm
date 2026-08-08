---
title: "RR-Reduce"
kind: source
created: "2026-08-07"
authors:
  - "Doehyun Baek"
  - "Daniel Lehmann"
  - "Ben L. Titzer"
  - "Sukyoung Ryu"
  - "Michael Pradel"
published: 2025
citation_key: "baek2025rrreduce"
container: "2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE)"
edition: null
isbn: null
doi: "10.1109/ASE63991.2025.00073"
url: "https://doi.org/10.1109/ASE63991.2025.00073"
accessed: "2026-08-07"
tags:
  - fuzzing
  - record-replay
  - testing
  - webassembly
aliases:
  - "Execution-Aware Program Reduction for WebAssembly via Record and Replay"
---

# RR-Reduce

## Reference

Doehyun Baek, Daniel Lehmann, Ben L. Titzer, Sukyoung Ryu, and Michael Pradel.
“Execution-Aware Program Reduction for WebAssembly via Record and Replay.”
*ASE 2025*, 816–827. DOI
[10.1109/ASE63991.2025.00073](https://doi.org/10.1109/ASE63991.2025.00073).

## Contribution

RR-Reduce accelerates Wasm test-case minimization by recording the failing
execution and specializing reduction toward code exercised by that trace.

## Method

The paper evaluates 28 bug-triggering programs across three engines and
compares its record/replay reduction and a hybrid configuration with prior
reducers.

## Findings

RR-Reduce produces cases averaging 1.20% of original size in 14.5 minutes and
reports a 33.15-times reduction-time speedup over the evaluated state of the
art. Its slower hybrid reaches 0.13% in 3.5 hours, reported as 3.42 times
smaller and 2.26 times faster than the comparison baseline.

## Relevance

Cross-runtime and fault-injection failures in Agent WASM will often contain
large compiled guests and long event histories. Execution-aware reduction
suggests minimizing both the module and a replayable turn/effect trace before
promoting a discovery to the regression corpus.

## Limits

Recorded execution can over-specialize a case or remove behavior needed under a
different scheduler or engine. The evaluation set is small and focused on
engine bugs, not distributed host-state failures.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
