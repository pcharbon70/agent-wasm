---
title: "Which Host Implementation Approach Should Agent WASM Use?"
kind: inquiry
created: "2026-08-10"
status: resolved
tags:
  - agent-tools
  - deployment
  - elixir
  - extism
  - implementation-language
  - rust
  - runtime
aliases:
  - "Host language decision"
---

# Which Host Implementation Approach Should Agent WASM Use?

## Why this matters

The archive defines a language-neutral contract with authoritative state,
bounded mailboxes, lifecycle, policy, durability, effects, topology, tenancy,
and audit. A finished product must assign those responsibilities to one
coherent implementation and operations model. The language decision also
shapes the Extism boundary, cancellation model, native failure domain, release
pipeline, and amount of actor infrastructure that must be built.

An early choice made only from language familiarity could entangle the durable
host with one Wasm engine, weaken BEAM scheduler responsiveness, or require a
late rewrite of the actor lifecycle.

## Operational question

Which product language and private Extism process boundary best fit the draft
Agent WASM contracts with acceptable:

- semantic completeness and cross-runtime equivalence;
- mailbox, scheduler, deadline, and cancellation behavior;
- state/outbox correctness through crashes;
- guest, tenant, engine, and node failure containment;
- cold/warm latency, throughput, memory, and boundary-copy cost;
- build, update, rollback, provenance, and observability burden; and
- implementation and review cost for the expected team?

The initial comparison required primary-source evidence and a concrete
packaging seam, not a claim that the product should expose several language
implementations.

## Decision

**Agent WASM is an Elixir/OTP product.** Elixir owns its public API,
configuration, supervision, mailboxes, state, policy, effects, durability,
telemetry, health, deployment, and upgrade behavior.

The reference Extism/Wasmtime engine is packaged as a small private executable
behind a supervised Erlang Port. Its Rust implementation is a supply-chain and
build detail, not a public SDK or a second product language. End users install
one Hex package, Mix release, or OCI image and do not install a Rust toolchain
or choose among host implementations.

## Evidence basis

The earlier comparative
[synthesis](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
established that:

- the dominant host duties are actor lifecycle, serialized turns,
  supervision, timers, registries, topology, effects, and recovery, all of
  which align closely with OTP;
- Rust offers the most direct implementation path to the current reference
  Extism/Wasmtime engine, but those engine duties are much narrower than the
  host control plane;
- an in-VM NIF shares the BEAM node's address space and native failure scope;
- OTP Ports provide an explicit byte-oriented OS-process boundary that matches
  Extism's coarse input/output call shape; and
- the inspected off-the-shelf Extism Hex binding did not supply the complete,
  current, bounded Agent WASM adapter required here.

The subsequent [finished-product packaging
research](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
made the direction concrete:

- Mix produces a target-specific self-contained release with ERTS and
  application `priv`, where the private worker is bundled;
- a corrected health-only probe completed its versioned Port handshake and
  ExUnit test;
- the same pair ran from an assembled production release;
- a multi-stage Docker build executed the test and release smoke gate before
  copying the release into a non-root final image; and
- the final container health call passed after the pipeline exposed and fixed
  missing builder CA certificates and runtime UTF-8 locale configuration.

This is enough to resolve the product-language question. It does not pretend
that the full engine adapter is already production-qualified.

## Selected ownership boundary

The private worker may compile, cache, instantiate, invoke, cancel, and dispose
Extism modules. It may return only candidate results and bounded diagnostics.
It does not own canonical agent state, admission, leases, policy, artifact trust,
secrets, effects, or durable commits.

The Elixir host rejects late, duplicate, wrong-artifact, lost-lease, and
wrong-revision results before a state/outbox transaction. A worker crash or
hard kill therefore discards engine work rather than transferring
authoritative ownership outside OTP.

## Remaining qualification

The choice is resolved, while these implementation claims remain open:

### Complete the vertical slice

Implement `prepare`, `invoke`, `cancel`, `dispose`, and `health` through a
versioned framed protocol. Run one agent through authenticated admission,
bounded mailbox, lease, snapshot, Extism reducer, result validation, atomic
state/journal/outbox commit, effect attempt, and result signal.

### Measure representative load

Record cold and warm behavior across representative payloads, low and saturated
concurrency, one hot tenant, fair multi-tenant traffic, success, trap, timeout,
cancellation, and oversize outcomes. Measure end-to-end latency, throughput,
CPU, memory, Port copies, BEAM scheduler latency, queue age, and recovery time.
Include validation and durable commits so an empty-call microbenchmark does not
dominate the conclusion.

### Inject failures

Kill the worker during compilation, invocation, output, and commit handoff.
Exercise guest traps, engine cancellation, native panic/abort, truncated and
oversized frames, BEAM restart, stale leases, duplicate/late replies, and pool
replacement. Verify that no forbidden state or effect commits.

### Qualify the release

Build every promised OS, architecture, and ABI on matching CI. Test offline Hex
installation, checksum and attestation verification, mixed-version refusal,
upgrades, rollback, engine security patches, logs, traces, SBOMs, and crash
evidence. Initial support should remain Linux AMD64/ARM64 until native target
evidence justifies more.

### Record engineering cost

Track implementation and review time, defect patterns, debugging burden,
worker-pool operation, and release maintenance. This can change the private
boundary design or scope, but it does not require maintaining alternate public
language platforms.

## What would reopen the language choice

A measured Port problem can justify changing framing, pooling, transport, or
the private engine component. It does not by itself invalidate Elixir/OTP as
the host. Reopen the product-language decision only if the host requirements
materially change away from supervised, stateful, concurrent coordination, or
if representative implementation evidence shows that the complete Elixir host
cannot satisfy an explicit product objective and no bounded external-worker
design can repair it.

## Outcome

Resolved: **Elixir/OTP is the authoritative host and sole public product
language.** A narrow, supervised native Extism worker is packaged inside the
release as a private Port component. Remaining work qualifies that boundary
and the supported release targets; it is not a program to build or support
parallel Rust, Go, or Rustler product platforms.
