---
title: "Profile Vocabulary And Architectural Boundaries"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-01
  - phase-01
  - architecture
  - profile
  - contract
aliases:
  - "M1-P1 Profile Vocabulary"
---

# Profile Vocabulary And Architectural Boundaries

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-01-profile-vocabulary-and-architectural-boundaries.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It establishes the language-neutral vocabulary and responsibility split for a
Jido-inspired agent system built on WebAssembly and Extism.
It applies to all later milestones within Milestone 1 and provides the
foundation for milestones 2 through 9.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
integration tests in
Section 1.4
and a passing cross-milestone fixture run recorded in
Section 1.4.1.4.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

## Vocabulary

### System participants

> **Normative definition.**
The following terms identify the participants of this system.
Definitions are language-neutral and apply across all supported runtime families.

- **Host:** The embedding process that owns authoritative state, policy,
  scheduling, effects, durability, topology, and audit evidence.
  The host is outside Wasm linear memory and runs in the selected host language.
  The host is the sole authority for tenant identity, artifact admission,
  capability grants, turn scheduling, outbox commit, and effect execution.

- **Engine:** The Wasm execution engine that compiles, instantiates, and runs
  Wasm modules.
  An engine provides module validation, compilation, linear memory, tables,
  imports, exports, traps, and configurable resource limits.
  The engine is a facility of the host, not an independent actor.

- **Extism runtime:** One of the hosted implementations of the Extism plug-in
  protocol, namely the Rust reference runtime on Wasmtime or the independent
  Go runtime on Wazero.
  An Extism runtime wraps an engine with the shared Extism kernel, allocator,
  input/output/error bookkeeping, and the configurable policy fields defined
  by the Extism manifest.

- **Plug-in:** A core-Wasm module that exports at least one Extism-shaped
  no-argument function and imports the Extism kernel functions it uses.
  A plug-in implements portable decision logic, such as an agent reducer,
  action handler, or strategy.
  A plug-in is untrusted by default.
  Its authority derives from the host-granted capabilities, not from its own
  declarations.

- **Agent:** A logical identity composed of a versioned definition, a
  versioned state, installed capability references, strategy configuration,
  routes, and lifecycle policy.
  An agent definition is a metadata artifact.
  An agent instance is a live execution context with a mailbox, current state
  snapshot, turn lease, and active children.
  The agent identity and durable state live in the host.
  The agent decision logic lives in one or more plug-ins.

- **Action:** A named operation with input schema, output schema, metadata,
  and a host-resolved implementation reference.
  An action is a declarative contract, not an invocation.

- **Strategy:** A replaceable transition policy that advances an agent from
  one state to the next in response to an instruction.
  Strategies share a stable snapshot schema with the agent and emit
  state patches, directives, and a terminal or intermediate status.
  A strategy is implemented as a plug-in reducer export.

- **Directive:** A typed capability request emitted by a strategy.
  A directive is data asking the host to perform an effect.
  A directive is not itself an effect.
  Directives are placed in a durable outbox and executed by trusted
  host effect handlers under authorization.

- **Signal:** A versioned envelope that carries a causal record, a type,
  a source, a subject, and domain payload.
  A signal is the single ingress path for API calls, timers, sensors,
  child events, and effect results.
  Signal transport semantics are separate from the signal envelope.

- **Effect:** An observable action performed by the host on behalf of an
  agent.
  Effects include external I/O, state changes in other systems,
  downstream signals, and approval requests.
  Effects are authorized, attempted, recorded, and retried by the host.

- **Artifact:** An immutable, content-addressed bundle of plug-in bytes,
  manifest, schema, and provenance metadata.
  An artifact is identified by its digest and referenced by version.

### Derived and relation terms

> **Normative definition.**
The following terms describe relationships and operations on the participants.

- **Turn:** One serialized invocation of a plug-in reducer for one agent,
  starting from a stable snapshot and producing a new state patch,
  a list of directives, and a strategy snapshot.
  A turn is the atomic unit of agent computation.

- **Manifest:** A capability bundle description listing package identity,
  protocol and schema versions, actions, routes, state namespaces,
  migration ownership, requested host capabilities, schedules, sensors,
  trusted lifecycle-hook classes, and dependencies.

- **Reducer:** The primary plug-in export that accepts a turn request,
  applies the strategy, and returns a turn result.
  The reducer is the portable decision boundary.

- **Route:** A host-resolved mapping from signal type and subject to a
  target action and strategy.
  Routes are declared in manifests and compiled by trusted host policy.

- **Capability:** A host-granted authority to perform a specific operation
  on a specific resource under a specific principal, purpose, and deadline.
  Capabilities are attenuated per invocation.

- **State patch:** A typed, host-validated structural update to agent state.
  State patches are applied during commit, not during computation.

- **Outbox:** The durable append-log of committed directives awaiting
  host execution.
  The outbox is the boundary between decision and effect.

## Ownership

> **Normative definition.**
The following ownership assignments are mandatory for every implementation
of this profile.

| Concern | Owner | Rationale |
| --- | --- | --- |
| Authoritative agent state | Host | State must survive guest trap, reset, and instance eviction. |
| State schemas and initial-state functions | Host | Schema enforcement and initial values are policy decisions. |
| State revision and snapshot storage | Host | Revisions provide optimistic concurrency and replay. |
| Policy and authorization | Host | Untrusted guests must not supply the only check that authorizes their own actions. |
| Turn scheduling and serialization | Host | One committed turn advances one revision at a time per agent. |
| Capability grants | Host | Grants are attenuated per invocation and enforced independently. |
| Effect execution | Host | Effects are authority-bearing and must pass through trusted handlers. |
| Durable outbox commit | Host | The atomic commit of state, journal, and outbox is a host responsibility. |
| Topology and identity registry | Host | Durable nodes reference identities and digests; live handles are disposable. |
| Audit and provenance evidence | Host | Guest diagnostics may enrich but cannot replace host-owned records. |
| Tenant isolation boundaries | Host | Namespacing alone is not isolation. |
| Deterministic decision behavior | Guest | The reducer computes the next state and requested effects from stable input. |
| Disposable scratch state within a turn | Guest | Per-call scratch, caches, and temporary buffers are safe in guest memory. |
| Strategy snapshot within a turn | Guest | Strategy-local state lives in a reserved namespace and is returned to the host. |

A guest plug-in MUST NOT claim ownership of any concern assigned to the host.
A host implementation MUST NOT delegate any host-owned concern to guest
decision logic as its sole authorization check.

## Host--Guest Interface

> **Normative definition.**
The host invokes a plug-in through the reducer export.
The reducer is the only mandatory plug-in export for this bootstrap profile.

- **`describe(protocol_version) -> AgentManifest`:** Returns schemas, routes,
  actions, strategy metadata, required capabilities, state versions, and
  protocol versions.
  Results MAY be cached by the host.

- **`initialize(init_request) -> TurnResult`:** Calculates initial state and
  startup requests without acquiring external resources.

- **`reduce(turn_request) -> TurnResult`:** Handles signals or explicit
  instructions.
  The reducer receives a value snapshot, not a handle to authoritative
  mutable state.

- **`migrate(migration_request) -> MigrationResult`:** Transforms durable
  snapshots under a separately authorized maintenance path.

The host MUST validate every reducer input against the manifest-declared
schemas before invocation.
The host MUST validate every reducer output against the manifest-declared
schemas and policy constraints before committing.
A trap, timeout, schema violation, or policy rejection on output commits
nothing for that turn.

## Variability and limits

See [Variability register](#variability-register).

## Static semantics

### Profile adoption

A system adopts this profile when it satisfies all of the following:

1. The host owns all concerns assigned to the host in the
   [Ownership](#ownership) table.
2. Guest plug-ins expose only the reducer exports listed in
   [Host--Guest Interface](#host--guest-interface).
3. The host enforces schema validation on both inputs and outputs.
4. The host maintains a durable outbox between state commit and effect
   execution.
5. Guest trap, timeout, or output failure commits nothing for that turn.

### Manifest composition

The host composes manifests into an effective agent definition outside
guest memory.
Composition MUST detect route conflicts, state-key conflicts, migration
ownership conflicts, and capability conflicts before execution.

## Elaboration

### One complete turn

The host executes one turn as follows:

1. Accept a signal and authenticate its transport identity.
2. Resolve tenant, agent identity, artifact digest, and policy.
3. Validate and canonicalize the signal; preserve correlation and causation.
4. Acquire a per-agent turn lease so only one revision is advanced at a time.
5. Load the snapshot and associated journal revision.
6. Resolve the route and authorize the target action in trusted host policy.
7. Acquire a clean Extism execution instance for the pinned artifact.
8. Invoke `reduce` with deadline, fuel or equivalent budget, memory limit,
   and the minimum host-function set.
9. Treat trap, timeout, invalid encoding, oversize output, or schema failure
   as a failed turn; do not commit state or effects.
10. Validate the expected revision, patch, strategy snapshot, directive types,
    destinations, and capability grants.
11. Atomically commit the next state, journal facts, and directive outbox.
12. Release the turn lease and acknowledge the input according to its
    delivery contract.
13. Drain outbox entries through idempotent effect handlers.
14. Convert result-bearing effects, timer fires, child lifecycle events,
    and sensor events into new signals.

### State and pooling

Authoritative agent state MUST NOT live in Wasm linear memory, Extism
variables, or a long-lived plugin instance.
Compiled artifacts and verified metadata MAY be shared widely.
Mutable instances SHOULD be fresh per turn or provably reset.

### Effects

Asynchronous or durable effect requests are the preferred pattern.
Synchronous host functions are an explicitly granted exception for
operations whose result is required in the current turn and that can be
bounded, cancelled, and safely retried.

## Diagnostics and conformance

See [Failure modes](#failure-modes).

## Variability register

| Clause | Type | Selection |
| --- | --- | --- |
| Ownership assignments | Required | Fixed by this chapter. |
| Reducer exports | Required | `describe`, `initialize`, `reduce`, `migrate`. |
| State location | Required | Host-owned; never in guest memory. |
| Turn serialization | Required | One committed turn per agent at a time. |
| Outbox commit | Required | Atomic state+journal+outbox commit. |
| Failure on trap/timeout | Required | Nothing committed for that turn. |
| Initial Wasm feature set | Required | Core Wasm 3.0; exclusions listed in Section 1.2. |
| WASI surface | Required | No WASI for bootstrap; explicit selection later (Section 1.2). |
| Extism runtime family | MAY | Wasmtime (reference) or Wazero (independent) at release. |
| Synchronous host functions | SHOULD NOT | Preferred pattern is directive continuation. |
| Guest state in Extism variables | SHOULD NOT | Treated as disposable cache at best. |
| Instance pooling across tenants | SHOULD NOT | Must prove state erasure; not a default. |

## Rationale and evidence (non-normative)

This vocabulary and boundary model derives from the Jido architecture
analysis in
[Jido Agent Architecture and Wasm/Extism Construction](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md),
the Extism plugin-system analysis in
[Extism Plugin-System Architecture and Runtimes](../20-notes/extism-plugin-system-architecture-and-runtimes.md),
and the WebAssembly foundations synthesis in
[WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md).

The reducer-only export surface avoids dynamic linking assumptions across
Extism runtimes and makes the protocol versionable as data.
The atomic outbox commit closes the crash gap between accepting a state
transition and attempting external effects.
The ownership table prevents untrusted guests from supplying the only
authorization check for their own actions.
