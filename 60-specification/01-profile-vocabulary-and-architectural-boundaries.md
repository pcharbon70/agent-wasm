---
title: "Profile Vocabulary And Architectural Boundaries"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-01
  - phase-01
  - architecture
  - profile
  - contract
  - model-bindings
  - credential-custody
aliases:
  - "M1-P1 Profile Vocabulary"
---

# Profile Vocabulary And Architectural Boundaries

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-01-profile-vocabulary-and-architectural-boundaries.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It establishes the language-neutral vocabulary and responsibility split for a
Jido-inspired agent system built on WebAssembly and Extism.
It applies to all later milestones within Milestone 1 and provides the
foundation for milestones 2 through 9.

Version `1.0.0` replaces `0.2.0`. It retains the model-selection and
credential-custody ownership boundaries and aligns the host--guest export
signatures with protocol version `1.0.0`.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
 Promotion to `status: normative` requires evidence from the Phase 1
 integration tests in
 Section Integration Test Expectations
 and a passing cross-milestone fixture run recorded in
 the cross-milestone fixture regression test case within that section.

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
  capability grants, turn scheduling, outbox commit, and effect orchestration.
  A typed external operation MAY be performed by an independently
  authenticated credential custodian without transferring its credential to
  the host.

- **Credential custodian:** A user-controlled service that holds or obtains
  provider or external-service authentication material and executes a narrowly typed operation
  after independent scope validation. It returns bounded results and a
  verifiable receipt, never credential bytes. It is outside the host process,
  native Port process, and Wasm guest in the
  `separated-credential-custody` profile defined by
  [Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md).

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
  versioned state, installed capability references, logical model
  requirements, strategy configuration, routes, and lifecycle policy.
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

- **Effect:** An observable action orchestrated by the host on behalf of an
  agent.
  Effects include external I/O, state changes in other systems,
  downstream signals, and approval requests.
  Effects are authorized, orchestrated, attempted, recorded, and retried by
  the host. A registered custodian MAY perform the credential-bearing portion
  of a typed external effect.

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
| State schemas and initial-state admission | Host | Schema enforcement and acceptance of initial values are policy decisions. |
| State revision and snapshot storage | Host | Revisions provide optimistic concurrency and replay. |
| Policy and authorization | Host | Untrusted guests must not supply the only check that authorizes their own actions. |
| Turn scheduling and serialization | Host | One committed turn advances one revision at a time per agent. |
| Capability grants | Host | Grants are attenuated per invocation and enforced independently. |
| Effect authorization and orchestration | Host | Effects are authority-bearing and must pass through trusted handlers. |
| Concrete model binding | Installing user or authorized tenant operator; stored and enforced by host | Agent and publisher declare requirements but do not choose provider accounts. |
| Raw credential custody | User-controlled custodian for separated-custody profile | Host, native Port, and guest processes need only sender-constrained handles and receipts. |
| Durable outbox commit | Host | The atomic commit of state, journal, and outbox is a host responsibility. |
| Topology and identity registry | Host | Durable nodes reference identities and digests; live handles are disposable. |
| Audit and provenance evidence | Host | Guest diagnostics may enrich but cannot replace host-owned records. |
| Tenant isolation boundaries | Host | Namespacing alone is not isolation. |
| Deterministic decision behavior | Guest | The reducer computes the next state and requested effects from stable input. |
| Initial-state and migration candidate calculation | Guest | Pure exports calculate candidates; the host authorizes, validates, and commits them. |
| Disposable scratch state within a turn | Guest | Per-call scratch, caches, and temporary buffers are safe in guest memory. |
| Strategy snapshot within a turn | Guest | Strategy-local state lives in a reserved namespace and is returned to the host. |

A guest plug-in MUST NOT claim ownership of any concern assigned to the host.
A host implementation MUST NOT delegate any host-owned concern to guest
decision logic as its sole authorization check.

## Host--Guest Interface

> **Normative definition.**
The host invokes a plug-in through four required protocol exports.
The `reduce` export is the primary decision boundary, but `describe`,
`initialize`, and `migrate` are also mandatory for this bootstrap profile.

- **`describe(DescribeRequest) -> DescribeResponse`:** Returns schemas, routes,
  actions, strategy metadata, logical model requirements, required
  capabilities, state versions, and protocol versions.
  Results MAY be cached by the host.

- **`initialize(InitializeRequest) -> InitializeResponse`:** Calculates initial
  state and startup requests without acquiring external resources.

- **`reduce(TurnRequest) -> TurnResult`:** Handles signals or explicit
  instructions.
  The reducer receives a value snapshot, not a handle to authoritative
  mutable state.

- **`migrate(MigrationRequest) -> MigrationResult`:** Transforms durable
  snapshots under a separately authorized maintenance path.

These are logical signatures. At the core-Wasm boundary all four exports use
the no-argument Extism calling convention and exchange the named values as
canonical JSON byte buffers under
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#exports).

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

1. Receive a `SignalSubmission`, authenticate its transport context, and
   record its immutable `received_at` timestamp.
2. Validate canonical structure, size, future-time rejection, and the fixed
   signal TTL.
3. Compute logical signal identity and reject a previously accepted duplicate.
4. Resolve one route, authorize its source, take the fixed candidate snapshot,
   and select one target instance.
5. Atomically persist `AcceptedSignalEnvelope`, including the selected target
   and any round-robin cursor advance.
6. Acquire the selected agent's turn lease so only one revision advances at a
   time.
7. Load the snapshot and associated journal revision.
8. Project and validate the accepted record as one canonical `TurnRequest`.
9. Acquire a clean Extism execution instance for the pinned artifact.
10. Invoke `reduce` with deadline, fuel or equivalent budget, memory limit,
   and the minimum host-function set.
11. Treat trap, timeout, invalid encoding, oversize output, or schema failure
   as a failed turn; do not commit state or effects.
12. Validate the expected revision, patch, strategy snapshot, directive types,
    destinations, and capability grants.
13. Atomically commit the next state, journal facts, and directive outbox.
14. Release the turn lease and mark the one delivery attempt successful or
    failed; do not redeliver it automatically.
15. Drain outbox entries through idempotent effect handlers.
16. Convert result-bearing effects, timer fires, child lifecycle events,
    and sensor events into new signals.

### State and pooling

Authoritative agent state MUST NOT live in Wasm linear memory, Extism
variables, or a long-lived plugin instance.
Guests MAY use Extism variables only as disposable within-turn scratch that is
cleared before another turn or tenant uses the instance.
Compiled artifacts and verified metadata MAY be shared widely.
Mutable instances SHOULD be fresh per turn or provably reset.

### Effects

Asynchronous or durable effect requests are the preferred pattern.
Synchronous host functions SHOULD NOT be used unless their result is required
in the current turn. They are an explicitly granted exception only for
operations whose result is required in the current turn and that can be
bounded, cancelled, and safely retried.

## Diagnostics and conformance

See [Failure modes](#failure-modes).

## Behavior And Integration

### Pinned Core WebAssembly feature set

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

## Failure Evidence And Operational Notes

### Failure modes

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
`identity.limit.<limit_identifier>` diagnostic identifying the named limit and
the invocation context. Failures independent of a named limit use the
`identity.resource` family instead.

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

## Fixed semantics, internal mechanisms, and deferred work

### Internal mechanisms

The host MAY use compilation caches, instance pools, zero-copy buffer paths,
or any durable outbox backend only when the mechanism preserves the same
artifact identity, limits, timeout classification, tenant isolation, output
bytes, commit behavior, and diagnostics required by this profile. These are
internal mechanisms, not profile-selected observable semantics.

Pooled instances MUST satisfy the reset and tenant-erasure requirements in
[State and pooling](#state-and-pooling). Timeout enforcement MUST produce the
fixed limit outcome defined by
[Limit enforcement](02-stable-identities-versions-errors-and-limits.md#limit-enforcement).
Artifact admission is governed by
[Validation order](03-agent-manifests-artifacts-schemas-and-registries.md#validation-order),
and diagnostic recording is governed by
[Diagnostic recording policy](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md#diagnostic-recording-policy).

### Deferred work

The following items are explicitly deferred to later phases or milestones:

| Item | Target | Reason |
| --- | --- | --- |
| Component Model / WIT interface adoption | Milestone 8 | Requires Phase 2 of Milestone 8 (Core WASI/Extism/Plugin Contract Conformance) to be stable |
| WASI 0.3 interface selection | Milestone 5 | Requires capability model to be defined first |
| JavaScript runtime conformance | Milestone 8 | Environment variability requires later testing; see also [Cross-runtime identity equivalence](02-stable-identities-versions-errors-and-limits.md) and [Chicory runtime conformance](01-profile-vocabulary-and-architectural-boundaries.md) (same file) |
| Chicory runtime conformance | Milestone 8 | Experimental parity; incomplete |
| Multi-memory profiling and optimization | Milestone 4 | Requires durable state model first |
| Memory64 large-state agent support | Milestone 4 | Requires state model and pagination policy; large-state runtime memory |
| Thread-based parallel turns | Milestone 6 | Requires multi-agent coordination model |
| Synchronous host function catalog | Milestone 5 | Requires capability and security model |
| Artifact signing and provenance chain | Milestone 5 | Requires trust model and plugin system |
| Instance pooling state-erasure proof | Milestone 5 | Requires tenancy and security model |

> **Non-normative note.**
> All items deferred to Milestone 8 fall under
> Milestone 8 - Portability, Verification, And Performance
> (planning document at `.spec/planning/agentic-system/milestone-08-portability-verification-and-performance/README.md`).
> The Milestone 8 boundary principle: Milestone 8 addresses portability,
> verification, and performance of the system as built by Milestones 1-7.
> Milestone 9 addresses production platform, developer experience, and
> operational tooling built on top of that verified system.

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
    without unsafe shared mutable memory; this is the large-state runtime
    concern also addressed by Memory64 support deferred to Milestone 4
    and compression deferred to Milestone 8 (artifact compression in
    [Agent Manifests](03-agent-manifests-artifacts-schemas-and-registries.md),
    compression for large payloads in [Turn Lifecycle](04-turn-lifecycle-protocols-and-canonical-encoding.md)).
5. A stable Component Model interface provides materially stronger
    portability with less application protocol than Extism for the target
    deployment; addressed by Component Model / WIT interface adoption
    deferred to Milestone 8.

## Integration Test Expectations

This section defines the observable behavior that the Phase 1 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### Successful flow

The host MUST validate a well-formed submission, persist its accepted-ingress
record and fixed target, invoke the plug-in reducer with the exact projection,
validate the output, commit the state+journal+outbox atomically, release the
turn lease, and record the one delivery outcome.
The test MUST record and retain:

1. The submission, accepted-ingress record, `received_at`, delivery identity,
   and causal identifiers.
2. The artifact digest and manifest version used.
3. The protocol version and schema versions validated.
4. The route identity, selector mode and state, selected target, and action.
5. The capability grants supplied to the guest.
6. The resource limits and measured usage.
7. The prior and committed state revisions.
8. The directive identifiers and their disposition.
9. The trace context and timestamps.
10. The diagnostic family code (none for success).

### Malformed input

The host MUST reject inputs that fail to decode or violate required
structural rules.
The test MUST verify that:

1. Each malformed input family produces a `profile.vocabulary.malformed`
   diagnostic.
2. No state, journal, or outbox entries are created for the failed turn.
3. The turn lease is released even on failure.
4. The diagnostic identifies the specific field or schema that failed.
5. The diagnostic does not expose secrets or implementation internals.

### Incompatible input

The host MUST reject artifacts that declare a protocol version, feature
set, or capability requirement outside the accepted profile.
The test MUST verify that:

1. An artifact with an unsupported protocol version is rejected at
   admission with a `profile.vocabulary.incompatible` diagnostic.
2. An artifact requiring an excluded Wasm feature is rejected with the
   same diagnostic family.
3. The diagnostic identifies the version or feature mismatch.

### Stale input

The host MUST detect and reject stale state revisions.
The test MUST verify that:

1. A turn request with a state revision older than the current committed
   revision is rejected.
2. The rejection diagnostic identifies the stale revision and the
   expected revision.

### Duplicate input

The host MUST deduplicate signal invocations according to its delivery
contract.
The test MUST verify that:

1. A duplicate signal with the same correlation and causation identifiers
   is identified and handled according to the delivery contract.
2. No duplicate state revisions are created.
3. No duplicate outbox entries are created.

### Boundary-limit inputs

The host MUST enforce size, depth, and collection limits.
The test MUST verify that:

1. Input exceeding declared size limits is rejected with a
   `identity.limit.input.max_bytes` diagnostic.
2. Output exceeding declared size limits is rejected with
   `identity.limit.output.max_bytes`.
3. Nested structures exceeding depth limits are rejected with
   `identity.limit.state.max_depth`.
4. Collections exceeding size limits are rejected with
   `identity.limit.collection.max_items`.

### Timeout behavior

The host MUST enforce call deadlines.
The test MUST verify that:

1. A reducer that exceeds its deadline is interrupted.
2. No state, journal, or outbox entries are created for the timed-out turn.
3. The turn lease is released.
4. The diagnostic is `identity.limit.time.turn_ms`.

### Cancellation behavior

The host MUST support turn cancellation.
The test MUST verify that:

1. A cancellation signal interrupts an in-progress turn.
2. No state, journal, or outbox entries are created for the cancelled turn.
3. The turn lease is released.

### Unavailable dependency

The host MUST handle missing dependencies gracefully.
The test MUST verify that:

1. A missing artifact is rejected with a `profile.vocabulary.unavailable`
   diagnostic.
2. A missing capability grant is rejected with a
   `profile.vocabulary.unauthorized` diagnostic.
3. No partial state is committed.

### Retry behavior

The host MUST retry failed post-commit effect attempts according to their
idempotency contract. This rule does not permit retry or redelivery of the
input signal; signal delivery is governed by
[Redelivery criteria](10-signals-causality-routing-and-delivery.md#redelivery-criteria).
The test MUST verify that:

1. Effects with at-least-once semantics are retried until success or
   maximum attempts.
2. Idempotency keys prevent duplicate external delivery.
3. No unauthorized state is visible during retry.

### Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
| --- | --- | --- |
| Ownership assignments | Required | Fixed by this chapter. |
| Concrete model selection | Required | User or authorized tenant operator binds logical slots outside artifacts. |
| Credential custody | Required for end-user distributions | Separated-custody profile keeps raw provider and external-service credentials outside host, Port, and guest processes. |
| Required exports | Required | `describe`, `initialize`, `reduce`, `migrate`. |
| State location | Required | Host-owned; never in guest memory. |
| Turn serialization | Required | One committed turn per agent at a time. |
| [Signal ingress and target selection](10-signals-causality-routing-and-delivery.md#submission-evaluation-order) | Required | Fixed TTL, route, selector, accepted-record, and guest-projection behavior. |
| Outbox commit | Required | Atomic state+journal+outbox commit. |
| Failure on trap/timeout | Required | Nothing committed for that turn. |
| Initial Wasm feature set | Required | Core Wasm 3.0; exclusions listed in Section 1.2. |
| WASI surface | Required | No WASI for bootstrap; explicit selection later (Section 1.2). |
| Extism runtime family | Required | Wasmtime (reference) and Wazero (independent) at release. |
| [Internal mechanisms](#internal-mechanisms) | MAY (internal) | Caches, pools, copying, and storage may vary only under observational equivalence. |
| [Effect retry](#retry-behavior) | Required | Post-commit effect attempts may retry; input signals are never redelivered automatically. |
| [Synchronous host functions](#effects) | SHOULD NOT | Use only for bounded current-turn results; prefer directive continuation. |
| [Guest scratch state](#state-and-pooling) | MAY | Extism variables are disposable within-turn scratch and must be cleared before reuse. |
| [Mutable instances](#state-and-pooling) | SHOULD | Fresh per turn or provably reset with tenant state erasure. |

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
