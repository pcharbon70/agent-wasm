---
title: "How Should Agent WASM Use WebAssembly?"
kind: inquiry
created: "2026-08-07"
status: open
tags:
  - agent-tools
  - runtime
  - security
  - webassembly
aliases: []
---

# How Should Agent WASM Use WebAssembly?

## Why this matters

WebAssembly supplies portable computation and a narrow host boundary, while
agents require controlled access to powerful tools, untrusted inputs, secrets,
networks, files, and persistent state. An incorrect boundary could make the
system unsafe; an overly restrictive or unstable one could erase Wasm's
portability and performance advantages.

The [foundational synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
shows that core isolation, WASI capabilities, Component Model typing, runtime
resource controls, and agent output safety are distinct concerns.

## Operational question

Which pinned WebAssembly language profile, component/host interface,
implementation set, capability model, resource controls, and evidence contract
can execute representative agent tools with:

- no unauthorized host effects under the stated threat model;
- bounded CPU, memory, wall time, storage, network, and output;
- safe cancellation and cleanup;
- typed, size-limited, provenance-bearing results;
- reproducible artifact and policy identity;
- interoperable execution on at least two independent runtimes; and
- measured cold and warm performance suitable for the target workloads?

## Working hypotheses

1. A pinned Component Model and WASI 0.3 profile will reduce private ABI work,
   but its preview maturity requires explicit compatibility gates.
2. Wasmtime is the most complete first reference implementation for server
   experiments, while WAMR or WasmEdge can test whether the design remains
   portable beyond a server-class Cranelift runtime.
3. Capability grants must bind artifact, principal, purpose, and invocation;
   a component's import names alone are insufficient authorization.
4. Epoch interruption plus host-side async deadlines will fit production
   latency, while fuel will remain necessary for deterministic tests and
   replay-sensitive budgets.
5. Tool output must cross a typed untrusted-data boundary with validation and
   provenance before entering model context.
6. Some threat classes will require a process or stronger outer sandbox even
   when Wasm remains the inner portability boundary.

## Paths to explore

### Specify the profile

- Pin Core 3.0 features and explicitly classify every proposal dependency
  using the [proposal registry](../30-sources/webassembly-community-group-2026-proposals.md).
- Compare a core-module ABI with a pinned
  [Component Model](../30-sources/webassembly-community-group-2026-component-model.md)
  profile.
- Select the minimum [WASI 0.3](../30-sources/webassembly-wasi-subgroup-2026-wasi-0-3.md)
  packages and define agent-specific WIT interfaces for remaining authority.

### Build conformance probes

- Run official suites plus malformed, adversarial, and differential cases.
- Exercise identical components on Wasmtime and a second independent runtime.
- Test forbidden imports, path traversal, origin restrictions, oversized
  values, traps, infinite loops, blocked host calls, cancellation, and cleanup.

### Measure realistic tools

- Small pure transforms, filesystem-scoped tools, HTTP clients, streaming
  tools, stateful tools, CPU-heavy analysis, and memory-heavy parsing.
- Record cold compilation, cached compilation, instantiation, first result,
  steady-state throughput, boundary cost, memory, and tail latency.

### Test agent-specific failure modes

- Seed environment, file, and network canaries following the
  [MCP-SandboxScan](../30-sources/tan-et-al-2026-mcp-sandboxscan.md) evidence model.
- Treat all outputs as untrusted following the boundary lesson from
  [RLBox](../30-sources/narayan-et-al-2020-rlbox.md).
- Test pooled/snapshotted instances for residual secrets and cross-principal
  state.
- Decide whether speculative-execution defenses or an outer process boundary
  are required using [Swivel](../30-sources/narayan-et-al-2021-swivel.md) as
  comparative evidence.

## Findings

- Core Wasm supplies no ambient authority, but all useful authority and most
  operational limits remain host responsibilities.
- Component and WASI interfaces improve portability and typing but do not
  themselves authorize calls or make outputs trustworthy.
- Runtime architecture varies enough that one implementation cannot establish
  portability or performance.
- Historical research invalidates blanket claims that Wasm is automatically
  near-native, makes unsafe guests memory-safe, or closes microarchitectural
  channels.
- Formal methods, differential testing, and generated specification artifacts
  have repeatedly found defects in Wasm definitions and implementations.
- [Extism](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
  demonstrates a pragmatic portable core-module ABI and four engine families,
  while leaving typed schemas, authorization, provenance, and runtime parity
  to an outer design and conformance program.

## Outcome

Open. The research narrows the architecture and defines an evaluation program,
but no implementation profile should become normative until the experiments,
threat model, and two-runtime conformance gate are complete. Follow the
[topic map](../10-maps/webassembly-foundations-and-ecosystem.md) for the current
evidence trail.
