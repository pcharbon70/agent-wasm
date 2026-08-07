---
title: "Retrofitting Fine-Grain Isolation in the Firefox Renderer"
kind: source
created: "2026-08-07"
authors:
  - "Shravan Narayan"
  - "Craig Disselkoen"
  - "Tal Garfinkel"
  - "Nathan Froyd"
  - "Eric Rahm"
  - "Sorin Lerner"
  - "Hovav Shacham"
  - "Deian Stefan"
published: 2020
citation_key: "narayan2020rlbox"
container: "29th USENIX Security Symposium"
edition: null
isbn: "978-1-939133-17-5"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity20/presentation/narayan"
accessed: "2026-08-07"
tags:
  - security
  - webassembly
aliases:
  - "RLBox"
---

# Retrofitting Fine-Grain Isolation in the Firefox Renderer

## Reference

Shravan Narayan et al. “Retrofitting Fine Grain Isolation in the Firefox
Renderer.” *USENIX Security 2020*, pp. 699–716.
[Open-access paper](https://www.usenix.org/conference/usenixsecurity20/presentation/narayan).

## Contribution

RLBox provides a framework for retrofitting fine-grained sandboxing around
native libraries and tracking untrusted values through the C++ type system.

## Method

The authors sandbox media, image, compression, and font libraries with
software-fault or process isolation, evaluate overhead, and integrate a
Wasm-based sandbox for Graphite into production Firefox.

## Findings

Isolation is only half the integration problem: host code must treat outputs,
pointers, callbacks, and state from the sandbox as untrusted. Static taint-like
types and explicit validation reduce boundary mistakes. The evaluated overhead
was modest and transient for the targeted browser workloads.

## Relevance

Agent tool output is adversarial input to the orchestrator and language model.
An Agent WASM boundary needs typed, validated values and provenance, not just
guest memory isolation.

## Limits

RLBox targets C++ library retrofits in Firefox, not autonomous agent tools,
WASI components, or distributed capability policy. Its results are workload-
and integration-specific.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
