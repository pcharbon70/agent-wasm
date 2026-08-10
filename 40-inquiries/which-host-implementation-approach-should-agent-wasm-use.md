---
title: "Which Host Implementation Approach Should Agent WASM Use?"
kind: inquiry
created: "2026-08-10"
status: open
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
  - "Host language decision"
---

# Which Host Implementation Approach Should Agent WASM Use?

## Why this matters

The archive defines a language-neutral host with authoritative state, bounded
mailboxes, lifecycle, policy, durability, effects, topology, tenancy, and
audit, but an implementation must eventually assign those responsibilities to
concrete runtimes. The host-language decision also selects an Extism engine
path, cancellation model, native failure domain, packaging matrix, and amount
of actor infrastructure that must be built.

An early choice made only from language familiarity could entangle the durable
host with one Wasm engine, weaken BEAM scheduler responsiveness, or require a
late rewrite of the actor lifecycle.

## Operational question

Which combination of host language, Extism implementation, and native process
boundary can satisfy the draft Agent WASM contracts with acceptable:

- semantic completeness and cross-runtime equivalence;
- mailbox, scheduler, deadline, and cancellation behavior;
- state/outbox correctness through crashes;
- guest, tenant, engine, and node failure containment;
- cold/warm latency, throughput, memory, and boundary-copy cost;
- build, update, rollback, provenance, and observability burden; and
- implementation and review cost for the expected team?

The answer requires one representative vertical slice and fault evidence, not
only API comparison or microbenchmarks.

## Working hypotheses

1. **Elixir/OTP is the strongest control-plane fit.** Its processes,
   supervisors, registries, timers, and message model should reduce the amount
   of novel actor infrastructure required for a Jido-inspired host.
2. **Rust is the strongest reference execution kernel.** Direct use of the
   current Extism/Wasmtime implementation should provide the fullest limits,
   cancellation, caching, and engine evidence.
3. **A supervised Rust Port is the safest initial boundary.** It matches the
   byte-oriented turn protocol and contains native engine faults outside the
   BEAM. The extra process and copy cost is acceptable unless representative
   measurements show otherwise.
4. **Rustler is an optional optimization, not the default assumption.** A
   purpose-built adapter may be worthwhile, but only after dirty-scheduler or
   native-pool behavior, cancellation, crash scope, and packaging pass explicit
   gates. The current official Extism Hex package is insufficient unchanged.
5. **Go/Wazero remains necessary.** Its independent Extism implementation is
   the best available oracle against accidental Wasmtime dependence and may
   later become a production runner if its portable subset and deployment
   advantages win.
6. **Rust-only and Go-only remain valid fallbacks.** They should win if the
   measured and organizational cost of a two-language Elixir/Rust system
   exceeds the value of OTP alignment.

## Paths to explore

### Implement one boundary-neutral vertical slice

Define a small execution protocol for `prepare`, `invoke`, `cancel`, `dispose`,
and `health`. Run one agent through authenticated admission, bounded mailbox,
lease, snapshot, Extism reducer, result validation, atomic
state/journal/outbox commit, effect attempt, and result signal.

Keep authoritative state and effects outside every engine adapter. Ensure a
late or duplicated native result cannot cross a lost lease or revision fence.

### Compare four execution paths

Use the same artifact and fixtures with:

1. direct Rust/Extism/Wasmtime;
2. Elixir through a supervised Rust Port;
3. Elixir through a bounded Rustler adapter; and
4. Go/Extism/Wazero.

Compare canonical outputs and failure classes before comparing performance.

### Measure representative load

Record cold and warm behavior for 1 KiB, 100 KiB, 1 MiB, and 10 MiB inputs and
outputs; low and saturated concurrency; a hot tenant and fair multi-tenant
traffic; successful, trapped, timed-out, cancelled, and oversize turns.

Measure end-to-end p50/p95/p99 latency, throughput, CPU, memory, copies,
ordinary/dirty BEAM scheduler latency, queue age, and recovery time. Include
schema validation and durable transactions so a boundary microbenchmark does
not dominate the conclusion artificially.

### Inject failures

Kill the runner during compile, invocation, output, and commit handoff. Exercise
guest traps, engine cancellation, Rust panic/abort, a deliberately crashing NIF
inside an isolated harness, truncated Port frames, BEAM restart, stale leases,
and duplicate/late replies. Verify no forbidden state or effect commits.

### Qualify releases

Build the promised OS, architecture, libc/ABI, and OTP matrix. Test offline
installation, artifact provenance, checksums or attestations, mixed-version
refusal, upgrades, rollback, engine security patches, logs, traces, and crash
evidence.

### Record engineering cost

Track implementation time, review difficulty, defect density, debugging time,
and operational complexity for each prototype. Team evidence can reverse a
technically attractive language choice.

## Findings

The comparative
[synthesis](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
finds:

- Rust has the cleanest reference-engine path but requires the host to assemble
  the full actor and supervision model.
- Go has the simplest independent, pure-Go engine deployment but also requires
  application-defined actor semantics and a pinned parity profile.
- Elixir has the closest control-plane semantics but no independent pure-Elixir
  Extism engine in the inspected official stack.
- The official [Extism Elixir SDK](../30-sources/extism-project-2026-elixir-sdk.md)
  is itself a Rustler NIF, pins Extism 1.0.0, exposes string I/O, omits public
  host functions and cancellation, and does lengthy work on normal NIFs.
- Rustler 0.38.0 provides valuable safe wrappers, resources, dirty scheduling,
  and asynchronous thread-to-BEAM messaging, but OTP still assigns a faulty
  NIF the whole VM as its failure scope.
- OTP explicitly recommends a Port when its overhead is acceptable, and a Port
  is naturally compatible with Extism's coarse byte-buffer contract.

No performance, scheduler, packaging, or fault-injection prototype has yet
tested the provisional recommendation.

## Outcome

Open. The current recommendation is an Elixir/OTP authoritative host with a
narrow Rust Extism worker behind a supervised Port, an adapter seam for a gated
Rustler optimization, and Go/Wazero as an independent conformance runner.

Resolve this inquiry only after the semantic, load, cancellation, crash,
tenant-residue, release, and engineering-cost evidence above is recorded. If
Port overhead or two-language operations violate the product envelope, compare
Rust-only against Go-only using the same fixtures rather than promoting
Rustler without re-running its node-failure gates.
