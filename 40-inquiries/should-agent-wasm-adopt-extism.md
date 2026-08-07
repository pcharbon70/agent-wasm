---
title: "Should Agent WASM Adopt Extism?"
kind: inquiry
created: "2026-08-07"
status: open
tags:
  - agent-tools
  - extism
  - plugin-system
  - runtime
  - security
  - webassembly
aliases: []
---

# Should Agent WASM Adopt Extism?

## Why this matters

Extism already supplies a language-neutral core-Wasm calling convention,
guest PDKs, host SDKs, an explicit capability boundary, resource settings, and
several engine implementations. Adopting it could remove substantial private
ABI and tooling work. It could also bind Agent WASM to a byte-oriented
interface with runtime-specific behavior just as the Component Model and WASI
move toward typed, async interfaces.

The [architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
shows that Extism's shared kernel standardizes call memory, while most policy
and operational behavior is independently implemented around Wasmtime, Wazero,
JavaScript engines, or Chicory.

## Operational question

Does a pinned Extism profile provide a secure, portable, observable, and
performant Agent WASM plug-in contract on at least two independent production
runtime families, with less long-term complexity than a direct Component
Model/WIT design?

An affirmative answer requires evidence that:

- the same admitted artifact and policy have equivalent observable behavior;
- all agent authority is explicit, least-privilege, and auditable;
- CPU, wall time, memory, I/O, variables, output, and cleanup are bounded;
- fresh-instance and pooling semantics prevent cross-principal leakage;
- payload schemas and untrusted results are validated outside the guest;
- artifact identity includes provenance beyond an optional digest; and
- cold and warm performance fits representative agent tool workloads.

## Working hypotheses

1. Extism will be a faster and more portable prototype substrate than a custom
   core-Wasm ABI.
2. The reference Wasmtime runtime and Go/Wazero SDK will expose enough
   independent implementation behavior for a meaningful conformance gate.
3. A browser/JavaScript profile will need different WASI, worker, timeout, and
   filesystem requirements from the server profile.
4. Extism manifests can carry deployment constraints but cannot replace the
   Agent WASM authorization, provenance, and output-policy envelope.
5. Fresh instances will be required between principals until variable, guest
   memory, reset, cancellation, and pool hygiene are proven.
6. Rich typed, streaming, resource, or async interfaces may make direct WIT
   adoption cheaper than extending the bytes protocol.

## Paths to explore

### Pin a candidate profile

- Exact Extism, PDK, engine, and SDK versions.
- Accepted core-Wasm features and guest toolchains.
- No WASI initially; only `extism:host/env` plus an allowlisted
  `extism:host/user` surface.
- In-memory modules with mandatory SHA-256 plus an outer signature/provenance
  record; no manifest URL or filesystem registration in production.
- Explicit maximum pages, variable bytes, input/output bytes, HTTP bytes,
  deadline, host-call budget, and aggregate effects.
- A canonical structured payload and error envelope.

### Build differential conformance probes

Run the same artifacts on reference Wasmtime and Go/Wazero first, then the
JavaScript profile and Chicory where applicable:

- valid calls, empty input/output, non-zero status, Extism errors, traps, and
  missing functions;
- invalid pointers, stale handles, oversized allocations, page growth, and
  output invalidation;
- variables across calls, explicit reset, new instances, compiled instances,
  and pools;
- guest globals and linear memory across the same lifecycle boundaries;
- infinite loops, fuel exhaustion, deadline expiry, cancellation during guest
  code, and cancellation during host calls;
- multi-module linking, initialization functions, WASI exits, and failed
  imports;
- allowed-host wildcards, redirects, DNS changes, response limits, and custom
  network functions; and
- filesystem traversal, symlinks, read-only mappings, and no-WASI behavior.

### Measure the data path

- Module validation/compilation and instance creation, cold and cached.
- One-byte, 1 KiB, 1 MiB, and maximum payload round trips.
- Serialization separately from host/kernel/guest copies.
- Host-function latency and nested memory operations.
- Throughput and tail latency for fresh, reused, and pooled instances.
- Resident memory and retained state after normal calls, traps, timeouts, and
  cancellation.

### Compare with the Component Model

Implement one representative typed tool in both Extism and WIT. Include
records, errors, streaming or async work, resources, generated bindings,
versioning, and policy instrumentation. Compare code size, runtime coverage,
boundary validation, ergonomics, and migration cost.

### Threat-model the host boundary

- Bind host functions to artifact, principal, tenant, purpose, invocation,
  budget, and cancellation token.
- Treat every guest result as untrusted and provenance-bearing before it enters
  model context.
- Test reentrancy, confused-deputy paths, stale memory views, concurrent user
  data, and host work that survives guest termination.
- Decide which workloads require an outer process, container, VM, or hardware
  boundary.

## Findings

- Extism's portable invariant is the kernel-backed byte-buffer ABI, not a
  single shared engine implementation.
- Many host-language SDKs use the same `libextism`/Wasmtime runtime and cannot
  count as independent conformance evidence.
- Go/Wazero and JavaScript are independent implementations; Chicory is a
  promising but explicitly experimental fourth family.
- The manifest controls useful built-ins and limits but does not authorize
  arbitrary host functions or represent artifact provenance.
- Call-memory reset, Extism variables, and guest-module state have different
  lifetimes.
- Current JavaScript prose says reset ends variable lifetime while source
  appears to preserve the variable map; this needs an executable parity test.
- Source inspection exposes other likely parity gaps, including JavaScript
  worker/WASI constraints and unfinished Chicory variable-limit enforcement.

## Outcome

Open. Extism is suitable for a controlled prototype and differential
evaluation, but the evidence does not yet justify making it the normative
Agent WASM interface. Follow the
[Extism topic map](../10-maps/extism-plugin-system.md) for the evidence trail
and the [broader WASM inquiry](how-should-agent-wasm-use-webassembly.md) for the
standards-level decision.
