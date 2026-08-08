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

## Behavior And Integration

### Pinned Core WebAssembly feature set

> **Normative implementation-defined choice.**
This profile pins Core Wasm 3.0 as the minimum feature set.
The host MUST reject any module that requires features not included in this
pin unless an explicit, versioned extension is declared in the artifact
manifest and accepted by the host policy.

The bootstrap feature set includes:

| Feature | Status | Agent impact |
| --- | --- | --- |
| Core Wasm 3.0 (released 2026-07-28) | Required | Portable typed machine, validation, execution, traps |
| Reference types | Included in 3.0 | Function references for callbacks and delegation |
| Saturating float-to-int conversions | Included in 3.0 | Safe float handling in decision logic |
| Sign extension operations | Included in 3.0 | Correct integer semantics across languages |
| Multi-memory | Included in 3.0 | Multiple linear memories per module |
| Memory64 | Included in 3.0 | Large-state agents beyond 4 GiB |
| Tail calls | Included in 3.0 | Deep recursion without stack overflow |
| Exception handling | Included in 3.0 | Structured error propagation |
| Threads | Excluded from bootstrap | Requires host synchronization primitives |
| Stack switching | Excluded from bootstrap | Not yet stable in any production runtime |
| Wide arithmetic | Excluded from bootstrap | Niche; not required for agent decision logic |
| Garbage collection | Excluded from bootstrap | Not part of Core 3.0; Component Model direction |

Extensions beyond this pin MAY be adopted through the manifest version
declaration process described in
[Milestone 1 Phase 3](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-03-agent-manifests-artifacts-schemas-and-registries.md).

### WASI profile declaration

> **Normative definition.**
The bootstrap agent profile imports **no WASI**.
All host interaction occurs through the Extism kernel and explicitly granted
custom host functions under `extism:host/user`.

Guest plug-ins for this profile MUST NOT import from
`wasi_snapshot_preview1`, `wasi_cli_preview`, `wasi_fs_preview`,
`wasi_http_preview`, or any other WASI namespace.
Hosts MUST NOT configure WASI imports for bootstrap-profile plug-ins.

This declaration is deliberate.
Ambient filesystem, network, environment, clock, and secret access through
WASI bypasses typed framework policy and audit.
WASI interfaces MAY be adopted for later profiles through the manifest
version declaration process once:

1. The specific WASI 0.3 interfaces needed are identified;
2. Each interface is evaluated for capability equivalence with a host-function
   alternative;
3. The host implements per-invocation attenuation for any adopted interface;
4. Cross-runtime parity for the adopted interface is verified.

### Extism ABI and runtime families

> **Normative definition.**
This profile adopts the Extism plug-in calling convention as the bootstrap
application protocol.
The portable center is:

- Plug-in exports use no core-Wasm parameters and return no result or one
  `i32` status.
- Application input and output travel as byte buffers through an
  offset-and-length convention.
- Built-in imports live under `extism:host/env`; application host functions
  default to `extism:host/user`.
- An internal Wasm kernel, `extism-runtime.wasm`, implements the resettable
  allocator and input, output, and error bookkeeping.

The host MUST use the Extism kernel for all memory allocation, input/output
setting, and error reporting between the application and the guest module.

### Supported runtime families

> **Normative definition.**
The following runtime families are supported for this profile.
Conformance requires passing the Phase 1 integration test suite on at least
one member of each listed family.

| Family | Engine | Language | Status | Notes |
| --- | --- | --- | --- | --- |
| Reference | Wasmtime 41+ | Rust | Primary | Fullest Extism feature set; fuel, epochs, instance pools |
| Independent | Wazero | Go | Primary | Pure Go; no CGO; context-based cancellation |
| JavaScript | Host JS engine | TypeScript | Deferred | Environment-dependent WASI, workers, and limits |
| Java | Chicory | Java | Exploratory | Experimental parity; not a production target yet |

The JavaScript and Chicory families are deferred for the bootstrap profile.
They MUST NOT be claimed as conformance targets until differential tests
prove equivalent behavior for the pinned feature set.

The primary families are:

- **Extism/Wasmtime (Rust reference runtime):** Uses Wasmtime's linker, store,
  Cranelift compilation, caching, pooling support, resource limiter, fuel,
  epoch interruption, and WASI Preview 1 support.
  Provides Extism HTTP, variables, hashing, path preopens, compiled plug-ins,
  instance pools, coredumps, and memory dumps.

- **Extism/Wazero (Go SDK):** Pure Go implementation over Wazero.
  Supports WASI Preview 1, maps manifest page limits into Wazero configuration,
  and uses contexts for timeout and cancellation.
  Compilation caches let multiple instances share compiled modules.

### Supported target architectures

> **Normative definition.**
The following architectures are supported for bootstrap deployment.
Host implementations MUST build for these targets; plug-in artifacts MUST
target the same architectures.

| Architecture | Bits | Supported runtimes |
| --- | --- | --- |
| `x86_64` | 64 | Reference, Independent |
| `aarch64` | 64 | Reference, Independent |

Additional architectures MAY be added when both primary runtime families
provide equivalent support and conformance evidence.

## Failure modes

### Malformed

The input, manifest, or artifact fails to decode or violates required
structural rules.
The host MUST reject the input without executing any decision logic and MUST
return a `profile.vocabulary.malformed` diagnostic identifying the specific
field or schema that failed validation.

### Incompatible

The artifact declares a protocol version, feature set, or capability
requirement outside the host's accepted profile.
The host MUST reject the artifact at admission time and MUST return a
`profile.vocabulary.incompatible` diagnostic identifying the version or
feature mismatch.

### Conflicting

Manifest composition detects route conflicts, state-key conflicts, migration
ownership conflicts, or capability conflicts.
The host MUST reject the composition and MUST return a
`profile.vocabulary.conflicting` diagnostic identifying the conflicting
declarations.

### Unauthorized

A guest plug-in requests a capability not granted by the current invocation,
or a directive targets an action not authorized by host policy.
The host MUST reject the request without executing it and MUST return a
`profile.vocabulary.unauthorized` diagnostic identifying the requested and
granted capability scope.

### Exhausted

A resource limit is reached: memory pages, heap allocations, call depth,
output size, string length, collection size, or configuration bytes.
The host MUST reject the operation and MUST return a
`profile.vocabulary.exhausted` diagnostic identifying the limit and the
invocation context.

### Unavailable

A required dependency is unavailable: artifact not found in registry,
dependency plug-in missing, host function not installed, or external
service unreachable at the time of the turn.
The host MUST reject the turn and MUST return a
`profile.vocabulary.unavailable` diagnostic identifying the missing
dependency.

### Diagnostics contract

> **Normative definition.**
Every diagnostic emitted under this profile MUST contain:

1. A stable family code of the form `profile.vocabulary.<category>`.
2. The phase, contract, and profile to which the diagnostic applies.
3. The specific boundary or field that failed.
4. A human-readable description that does not expose secrets, credentials,
   or implementation-internal state.

Diagnostics MUST NOT contain: secrets, raw guest memory contents, host
process identifiers, internal stack traces, or unredacted configuration
values.

## Implementation-defined choices and deferred work

### Implementation-defined choices

The following choices are permitted but MUST be documented in the
implementation's conformance profile:

| Choice | Domain | Required documentation |
| --- | --- | --- |
| Compilation cache strategy | Engine | Cache key, invalidation, and hit-rate policy |
| Instance pool size and eviction | Engine | Maximum instances, eviction trigger, reset semantics |
| Fuel unit definition | Engine | Mapping from fuel to wall-clock time and determinism guarantees |
| Timeout enforcement mechanism | Engine | Epoch, wall-clock, or hybrid; latency characteristics |
| Output buffer copy strategy | Host | Zero-copy where possible; bounds enforcement point |
| Directive outbox storage backend | Host | Database, log format, and retention policy |
| Artifact admission policy | Host | Hash verification, signature verification, revocation |
| Diagnostic redaction rules | Host | Exact redaction list and override mechanism |

### Deferred work

The following items are explicitly deferred to later phases or milestones:

| Item | Target | Reason |
| --- | --- | --- |
| Component Model / WIT interface adoption | Milestone 8 | Requires stable phase-2 specification |
| WASI 0.3 interface selection | Milestone 5 | Requires capability model to be defined first |
| JavaScript runtime conformance | Milestone 8 | Environment variability requires later testing |
| Chicory runtime conformance | Milestone 8 | Experimental parity; incomplete |
| Multi-memory profiling and optimization | Milestone 4 | Requires durable state model first |
| Memory64 large-state agent support | Milestone 4 | Requires state model and pagination policy |
| Thread-based parallel turns | Milestone 6 | Requires multi-agent coordination model |
| Synchronous host function catalog | Milestone 5 | Requires capability and security model |
| Artifact signing and provenance chain | Milestone 5 | Requires trust model and plugin system |
| Instance pooling state-erasure proof | Milestone 5 | Requires tenancy and security model |

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter and would require normative revision:

1. Two primary runtimes cannot implement equivalent timeout, cancellation,
   or memory-limit behavior for the pinned feature set.
2. Reducer serialization dominates realistic turn latency for the target
   state sizes, requiring a non-Extism bootstrap ABI.
3. Common agent strategies require so many synchronous host calls that the
   directive continuation model becomes unusable.
4. Snapshot-plus-patch transfer cannot support the required state scale
   without unsafe shared mutable memory.
5. A stable Component Model interface provides materially stronger
   portability with less application protocol than Extism for the target
   deployment.

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
