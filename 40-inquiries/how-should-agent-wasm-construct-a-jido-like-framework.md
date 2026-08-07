---
title: "How Should Agent WASM Construct a Jido-Like Framework?"
kind: inquiry
created: "2026-08-07"
status: open
tags:
  - agent-tools
  - extism
  - jido
  - runtime
  - security
  - webassembly
aliases:
  - "Jido-like Wasm framework inquiry"
---

# How Should Agent WASM Construct a Jido-Like Framework?

## Why this matters

Jido supplies a coherent vocabulary for agent state, actions, messages,
strategies, effects, live actors, durable activation, teams, and history. Its
core reducer/effect split appears portable, but its production behavior also
depends on BEAM facilities that WebAssembly and Extism do not provide.

A construction decision made too early could hide effects behind host calls,
put durable state into engine memory, confuse logical tenancy with sandbox
isolation, or bind the framework to one Extism implementation. The
[architectural synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
proposes a host-owned actor cell and durable outbox; this inquiry tests that
proposal rather than treating it as settled.

## Operational question

Can two independent Extism runtime families execute the same versioned agent
turn protocol such that:

- the same state, signal, artifact, and policy produce equivalent state patches,
  directives, errors, and strategy snapshots;
- no mutable guest state crosses agent or tenant boundaries;
- traps, deadlines, cancellation, invalid output, and host failure have defined
  commit semantics;
- committed effects survive host crashes without unbounded duplication;
- topology can be restored without persisting runtime handles;
- authorization remains host-owned even when third-party capabilities and
  strategies are installed;
- latency and state-transfer costs remain acceptable for representative agent
  workloads?

An initial success threshold should include reference Extism/Wasmtime and
Go/Wazero, a single versioned JSON protocol, at least three agent patterns
(direct reducer, FSM continuation, and tool-using loop), and deterministic
fault injection around every commit/effect boundary.

## Working hypotheses

1. A single `reduce(bytes) -> bytes` guest export is sufficient for the first
   agent protocol and is more portable than dynamic module linking.
2. Authoritative state can remain host-side without unacceptable serialization
   overhead for ordinary conversational and workflow agents.
3. Result-bearing directives can replace most synchronous network, model,
   database, and filesystem host calls.
4. A transactional state/journal/outbox commit prevents lost effects; stable
   idempotency keys bound duplicates after crashes.
5. Sharing compiled artifacts while using fresh or proven-reset instances
   avoids cross-tenant state leaks at reasonable cost.
6. Durable Pod-like topology plus reconciliation is enough for single-node
   activation without persisting engine handles.
7. Framework plugins can be declarative manifests referencing Wasm artifacts
   without making untrusted lifecycle code part of the authorization boundary.
8. The Extism profile will expose runtime differences significant enough to
   require explicit conformance exclusions and test vectors.

## Paths to explore

### Specify the turn protocol

Define canonical `AgentManifest`, `TurnRequest`, `TurnResult`, `StatePatch`,
`Directive`, `StrategySnapshot`, and error schemas. Pin JSON canonicalization,
identifier and timestamp formats, collection limits, compatibility rules, and
unknown-field behavior. Create language-independent positive and negative test
vectors.

### Implement a minimal actor host

Build mailbox serialization, revisioned snapshots, route resolution, policy
checks, Extism invocation, output validation, and terminal-state observation.
Keep guest memory disposable. Start with no effectful host functions beyond
logging to demonstrate that the reducer boundary stands alone.

### Add crash-safe effects

Commit next state, journal facts, and directive outbox in one transaction.
Exercise emit, timer, child lifecycle, and a result-bearing fake model call.
Kill the host before and after commit, effect dispatch, external success, and
result acknowledgement. Count lost and duplicate effects.

### Test state and reset isolation

Write adversarial guests that fill linear memory, set Extism variables, trap,
time out, and attempt to recover prior-call data. Test fresh instances, reset,
pooled instances, and pinned agents on both runtime families. Cross product
tenant, agent, artifact, and failure mode.

### Measure boundary cost

Benchmark cold compile, warm instantiate, full-snapshot transfer, patch output,
schema validation, and outbox commit for 1 KiB, 100 KiB, 1 MiB, and 10 MiB
states. Compare JSON with one compact encoding only after the correctness suite
is stable.

### Exercise three strategy shapes

- direct validated action and state patch;
- FSM that waits for a result-bearing directive;
- bounded tool-using reasoning loop with model access as a host effect.

Measure turn count, latency, failure recovery, state size, and the number of
synchronous capabilities each genuinely requires.

### Build manifest composition checks

Compose two capability bundles with conflicting action names, state keys,
routes, schema versions, migrations, and requested grants. Require deterministic
diagnostics before runtime loading. Separate ordinary guest code, privileged
preparation hooks, and host-native integrations.

### Reconcile durable topology

Persist a small dependency/ownership graph, activate eager and lazy nodes,
hibernate the manager, kill selected actors, and reconcile. Confirm that no
Extism handle, process identifier, socket, or monitor appears in durable state.

### Compare Extism with a WIT component

Implement the same minimal reducer once through Extism's byte protocol and once
through the Component Model when two suitable runtimes support the required
profile. Compare type safety, async effect representation, toolchain reach,
runtime consistency, and host complexity.

## Findings

### From source research

- Jido's portable semantic seam is its command boundary, not its AgentServer
  implementation.
- State operations and directives already distinguish internal transition from
  external authority request.
- Strategy continuations demonstrate that effect results can return as later
  signals without breaking the state-machine model.
- Jido plugins are framework capability bundles; Extism plug-ins are executable
  modules and cannot substitute for the manifest layer.
- Strong tenancy requires more than logical partitioning.
- Pooled mutable agents retain state, which is directly relevant to Wasm memory
  and Extism-variable reuse.
- Durable teams should persist topology and state, not live handles.
- Jido's documented directive queue does not itself supply the proposed atomic
  state-and-effect outbox.

### Not yet established

- Cross-runtime behavioral parity for the proposed protocol.
- Acceptable state serialization and schema-validation cost.
- A safe and useful synchronous host-function subset.
- Reset semantics strong enough for mutable instance pooling.
- Crash bounds on duplicate external effects.
- Whether JSON remains suitable beyond the bootstrap profile.
- Whether Extism or WIT is the better long-term interface.

## Outcome

Open. The provisional architecture is a host-owned, revisioned actor cell that
invokes disposable Extism reducers and commits state with a directive outbox.
It should not become a normative framework contract until the cross-runtime,
fault-injection, isolation, and cost experiments above pass.
