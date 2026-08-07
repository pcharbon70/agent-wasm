---
title: "Extism Plugin Calling Convention"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026eip001"
container: "Extism Improvement Proposals"
edition: "EIP-001"
isbn: null
doi: null
url: "https://github.com/extism/proposals/blob/main/EIP-001-plugin-calling-convention.md"
accessed: "2026-08-07"
tags:
  - extism
  - specification
  - webassembly
aliases: []
---

# Extism Plugin Calling Convention

## Reference

Extism Project. *Plugin Calling Convention*. EIP-001.
[Proposal](https://github.com/extism/proposals/blob/main/EIP-001-plugin-calling-convention.md),
accessed 7 August 2026.

## Contribution

EIP-001 defines the low-level offset-and-length convention that lets host and
guest exchange arbitrary bytes without placing those bytes in core Wasm
parameters or results.

## Findings

The runtime tracks `input_offset`, `input_length`, `output_offset`, and
`output_length`. Guest imports expose the input location and length, allocate
shared memory, and designate an output region. The SDK side exposes the
resulting output size and bytes.

The contemporary implementation accepts exported plug-in functions with no
parameters and either no result or one `i32` result. PDK-generated functions
normally use the `i32` as a return code while moving application data through
the shared byte buffers.

## Relevance

This is the smallest interoperability contract an Agent WASM Extism-compatible
plug-in must satisfy.

## Limits

The EIP is a concise design proposal and some symbol names reflect historical
surface evolution. Current behavior must be checked against the kernel and
runtime source. The convention gives no intrinsic schema to the byte payload.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
