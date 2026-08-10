---
title: "Agent WASM Host Implementation Language"
kind: map
created: "2026-08-10"
tags:
  - agent-tools
  - elixir
  - extism
  - go
  - implementation-language
  - rust
  - rustler
  - runtime
aliases:
  - "Host language map"
---

# Agent WASM Host Implementation Language

## Scope

This map connects the repository's host responsibilities to Rust, Go, Elixir,
and Elixir/Rust through Rustler. It distinguishes control-plane language from
Wasm engine language, process boundary, independent conformance runtime, and
guest SDK language.

## Start here

- [Agent WASM Host Implementation Language and Runtime Boundary](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
  — compares the four choices, audits the current Extism Elixir/Rustler path,
  recommends an Elixir control plane with a process-isolated Rust worker, and
  defines the gates that could reverse that recommendation.
- [Which Host Implementation Approach Should Agent WASM Use?](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
  — keeps the decision open until semantic, performance, scheduler, fault,
  tenant, packaging, and team evidence exists.

## Trails

### Requirements before language

- [Profile Vocabulary and Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)
  — assigns authoritative state, policy, scheduling, effects, durability,
  topology, tenancy, and audit to the host. The chapter remains draft.
- [Mailboxes, Ordering, Bounds, Fairness, and Turn Leases](../60-specification/21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
  — makes explicit why a raw channel or process mailbox is not the whole
  admission and scheduling contract.
- [Single-Agent Host Flow](../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)
  — joins the control plane and execution engine in one end-to-end turn.
- [Jido Agent Architecture](jido-agent-architecture.md) — supplies the actor,
  reducer, effect, lifecycle, durability, and topology model behind those
  responsibilities.

### Rust host path

- [Rust Ownership and Concurrency](../30-sources/rust-project-2026-ownership-and-concurrency.md)
  — static memory and concurrency safety, without an application-defined actor
  lifecycle.
- [Tokio Task Runtime and Blocking Work](../30-sources/tokio-project-2026-task-runtime.md)
  — async tasks, CPU/blocking pools, bounding, and cancellation limitations.
- [Extism Reference Runtime](../30-sources/extism-project-2026-reference-runtime.md)
  and [Wasmtime](../30-sources/bytecode-alliance-2026-wasmtime.md) — the most
  direct and complete engine path.

### Go host and independent runtime

- [Go Concurrency, Context, and C Interoperation](../30-sources/go-project-2026-concurrency-context-and-cgo.md)
  — goroutines, channels, cancellation, pure-Go benefits, and the cgo boundary.
- [Extism Go SDK](../30-sources/extism-project-2026-go-sdk.md) and
  [Wazero](../30-sources/wazero-project-2026-runtime.md) — the independent,
  CGO-free execution family and required parity oracle.

### Elixir control plane

- [Elixir Processes, Mailboxes, and Supervision](../30-sources/elixir-project-2026-processes-and-supervision.md)
  — lightweight isolated actors, message queues, links, monitors, and
  supervision, plus the need for explicit mailbox admission bounds.
- [Jido Runtime and Coordination](../30-sources/agentjido-2026-jido-runtime-and-coordination.md)
  — the existing Elixir framework semantics that make OTP alignment relevant.
- [Erlang NIFs, Dirty Schedulers, and Ports](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md)
  — the authoritative choice between in-VM native speed and external-process
  fault containment.

### Rustler and current Elixir Extism evidence

- [Rustler Safe Rust NIF Bridge](../30-sources/rustler-project-2026-safe-rust-nifs.md)
  — typed NIFs, panic catching, resources, dirty scheduling, and native-thread
  replies.
- [Rustler Precompiled NIF Distribution](../30-sources/rustler-project-2026-precompiled-nif-distribution.md)
  — checksum-backed target distribution and the remaining release matrix.
- [Extism Elixir Host SDK](../30-sources/extism-project-2026-elixir-sdk.md) —
  source audit showing that official in-process Elixir support is already a
  Rustler binding and is not current or complete enough for Agent WASM unchanged.
- [Extism Plugin System](extism-plugin-system.md) — places this binding beside
  the reference and independent runtime families.

### Evidence and decision reversal

- [WebAssembly Testing and Verification](webassembly-testing-and-verification.md)
  — cross-engine, Extism, reducer, state-machine, crash, and isolation evidence.
- [How Should Agent WASM Assure a Jido-Like Extism Runtime?](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
  — defines equivalence, replay, state/outbox, failure, and traceability gates.

## Open questions

- Does a framed Port materially affect end-to-end service objectives after
  Wasm execution, validation, and durability are included?
- Can a Rustler adapter remain responsive under worst-case dirty CPU load and
  stop real engine work before turn leases expire?
- Is a BEAM-node failure an acceptable native-engine fault domain for every
  intended trust and availability profile?
- Which synchronous host functions, if any, cannot be converted into input
  context or asynchronous directives?
- Does the independent Go/Wazero runtime support the exact first profile with
  equivalent limits, reset, cancellation, and errors?
- Which approach is safest for the actual team's expertise and release
  environment?

These questions remain in the
[host implementation inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md).
