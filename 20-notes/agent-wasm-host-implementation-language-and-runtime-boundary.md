---
title: "Agent WASM Host Implementation Language and Runtime Boundary"
kind: note
created: "2026-08-10"
maturity: developing
tags:
  - agent-tools
  - elixir
  - extism
  - go
  - implementation-language
  - rust
  - rustler
  - runtime
  - security
  - webassembly
aliases:
  - "Host language comparison"
  - "Rust Go Elixir and Rustler comparison"
---

# Agent WASM Host Implementation Language and Runtime Boundary

## Executive recommendation

Use **Elixir/OTP for the authoritative host control plane and Rust for a small
Extism execution kernel**. Put the Rust kernel behind a **supervised external
Port process by default**, while designing the adapter seam so that the same
kernel can later be exposed through Rustler if measurements prove the process
boundary too expensive. Keep the pure-Go Extism/Wazero implementation as an
independent conformance runner, not as dead code and not necessarily as the
first production host.

This recommendation deliberately separates two decisions:

1. **Host language:** Elixir best matches the repository's dominant work—actor
   lifecycle, mailboxes, supervision, timers, registries, topology, effects,
   and recovery.
2. **Execution-engine language and boundary:** Rust gives direct access to the
   current Extism reference runtime and Wasmtime. A Port preserves
   operating-system fault isolation; Rustler is a lower-overhead but
   process-wide native extension and should be an evidenced optimization.

The resulting shape is:

```text
Elixir/OTP host — authoritative
  ├─ signal admission, bounded mailbox, scheduling, leases
  ├─ agent registry, supervision, timers, topology
  ├─ policy, validation, durable state/journal/outbox
  ├─ effect handlers, audit, tenant accounting
  └─ execution adapter
       ├─ default: supervised Port pool
       │    └─ Rust worker: Extism reference runtime / Wasmtime
       ├─ optional after evidence: Rustler NIF adapter
       │    └─ the same narrow Rust execution kernel
       └─ conformance: Go runner / Extism on Wazero
```

If the decision is artificially restricted to exactly one in-process label,
**Elixir/Rust through a purpose-built Rustler adapter** is the closest fit, but
it is conditional on the scheduler, crash, cancellation, packaging, and
recovery gates below. The current official Hex `extism` package should not be
used unchanged as that adapter.

This is a research recommendation, not a normative specification decision. No
representative implementation or performance benchmark was run in this pass,
so the associated inquiry remains open.

## What is actually being selected

The choice concerns the **host**, not guest plug-in languages. The draft
[architectural profile](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)
assigns authoritative state, policy, scheduling, effects, durability,
topology, tenancy, and audit to the host. A guest is a disposable deterministic
reducer. The draft
[single-agent flow](../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)
then joins admission, mailbox dequeue, lease acquisition, snapshot load,
Extism invocation, output validation, commit, directive handling, and lifecycle
evidence.

That responsibility split makes this a poor fit for a generic "which language
is fastest?" comparison. The Wasm call is only one stage. A good choice must
also make the failure and ownership model easy to preserve when the process is
overloaded, the engine traps, a node crashes, a turn is cancelled, or an effect
is retried.

The four labels need precise definitions:

- **Rust** means one Rust host process using the Rust Extism crate and Wasmtime,
  normally with Tokio and a durable database.
- **Go** means one Go host process using the independent pure-Go Extism SDK and
  Wazero. Binding `libextism` through cgo is a different, less portable variant.
- **Elixir** is a complete control-plane language but not, by itself, an
  in-process Extism engine. A serious non-NIF Elixir design therefore invokes a
  supervised Port or remote runner.
- **Elixir/Rustler** means the Elixir control plane loads a custom Rust NIF that
  embeds Extism/Wasmtime inside the BEAM address space.

This definition exposes an important fact: the official
[Extism Elixir SDK](../30-sources/extism-project-2026-elixir-sdk.md) is already
a Rustler wrapper around the Rust Extism crate. "Elixir" and "Elixir/Rustler"
are not two independent in-process engine implementations today.

## Evaluation criteria

The comparison prioritizes repository fit over language fashion:

| Criterion | Why it matters here |
| --- | --- |
| Actor and lifecycle semantics | Each durable identity has serialized turns, cancellation, children, timers, monitoring, hibernation, and restart policy. |
| Extism feature fit | The host needs constrained instances, binary input/output, timeouts, cancellation, usage, reset or disposal, and eventually selected host functions. |
| Failure containment | A guest trap should fail one turn; an engine fault should not silently corrupt authoritative state or widen the outage unnecessarily. |
| Backpressure and scheduling | Mailboxes have count, byte, age, source, tenant, priority, and fairness rules; Wasm calls are CPU work with deadlines. |
| Durability and recovery | State, journal, and directive outbox must commit atomically and recover after host or worker loss. |
| Security boundary | Native engine code, tenant data, guest output, effects, secrets, and artifact provenance have different trust levels. |
| Runtime parity | Reference Wasmtime behavior must be checked against an independent Extism/Wazero family. |
| Deployment | Cross-compilation, native dependencies, platform targets, upgrades, observability, and release rollback are production concerns. |
| Engineering complexity | The amount of custom actor infrastructure, boundary code, schema validation, and cross-language debugging affects correctness. |
| Performance | Cold/warm compilation, turn latency, throughput, memory, payload copies, and overload behavior matter, but require measurement. |

## Comparative summary

| Dimension | Rust host | Go host | Elixir host with external runner | Elixir/Rustler |
| --- | --- | --- | --- | --- |
| Actor/lifecycle fit | Capable, mostly application-built | Capable, mostly application-built | Strong OTP fit | Strong OTP fit |
| Extism path | Reference Rust runtime on Wasmtime | Independent Go runtime on Wazero | Depends on runner; Rust gives reference path | Reference Rust runtime in NIF |
| Native-engine crash scope | Whole Rust host process | No C boundary in Wazero path; whole Go host remains the process boundary | Rust worker process; BEAM can remain alive | Whole BEAM node |
| Long-call scheduling | Bounded blocking/dedicated pool plus engine cancellation | Bounded workers/goroutines plus context cancellation | OS worker pool supervised by BEAM | Dirty CPU schedulers or dedicated Rust threads inside VM |
| Mailboxes/supervision | Must define and assemble | Must define and assemble | Native conceptual fit, but explicit bounds still required | Same Elixir strengths; NIF faults bypass process isolation |
| Deployment unit | One native binary plus runtime assets | Usually one pure-Go binary plus Wasm assets | BEAM release plus Rust worker artifact | BEAM release plus per-target NIF artifact |
| Language count | One | One | Two plus a byte protocol | Two plus NIF/term boundary |
| Best role | Direct, performance-oriented reference host | Simple independent runtime and conformance oracle | Recommended authoritative control plane | Optional in-process optimization |
| Primary risk | Rebuilding a reliable actor platform | Semantic drift from reference runtime and rebuilding actor platform | IPC/release complexity and two-process operations | VM-wide crash/scheduler risk and native release matrix |

The table is qualitative. Assigning precise scores before prototypes would hide
the largest unknowns behind invented numbers.

## Rust

### Proposed shape

A Rust host would implement every control-plane responsibility in Rust and call
the `extism` crate directly. Tokio tasks could represent live work, channels
could carry commands, and a database transaction could implement the
state/journal/outbox boundary. Extism's current reference implementation already
supplies Wasmtime, epochs, fuel, memory limiting, compiled plug-ins, and pools.

### Advantages

- **Shortest engine path.** The host uses the same Rust implementation that
  defines the most complete current Extism semantics; there is no FFI or NIF
  conversion layer.
- **Fine-grained resource control.** Extism/Wasmtime exposes compilation,
  caching, memory, fuel, epoch deadlines, cancellation, and instance lifecycle
  directly. This is the strongest route for engine profiling and diagnostics.
- **Static safety at the boundary.** Ownership, lifetimes, `Send`, and `Sync`
  prevent many memory and data-race errors in safe application code, as the
  [Rust language source](../30-sources/rust-project-2026-ownership-and-concurrency.md)
  explains.
- **One implementation language and build graph.** Serialization, policy,
  storage, execution, and metrics can share types and test tooling. A native
  binary is operationally conventional.
- **Performance ceiling.** It avoids IPC and BEAM/NIF term conversion, and it
  offers direct control over allocation and pools. This is a hypothesis about
  the ceiling, not evidence about end-to-end Agent WASM performance.
- **Strong assurance ecosystem.** Rust and Wasmtime support fuzzing,
  property-based testing, sanitizers where applicable, and extensive upstream
  engine testing already recorded in this archive.

### Disadvantages

- **The actor runtime is application work.** Rust channels and tasks do not
  define supervision trees, restart intensity, monitors, durable mailboxes,
  registries, hibernation, topology reconciliation, or Jido-style lifecycle.
  Those semantics would have to be designed, integrated, and tested.
- **Async does not automatically cancel native work.** The
  [Tokio source](../30-sources/tokio-project-2026-task-runtime.md) notes that a
  running blocking closure cannot simply be aborted. Engine interruption must
  be wired through the call path, and CPU concurrency must be separately
  bounded.
- **Complexity concentrates in one process.** A fatal engine or allocator
  defect takes down the same process that owns live mailboxes and orchestration,
  even when durable state remains recoverable elsewhere.
- **Higher implementation difficulty.** Async lifetimes, cancellation,
  concurrency traits, native engine configuration, and durable transactions
  interact in the most correctness-sensitive parts of the system. Compile time
  and contributor ramp-up are practical costs.
- **No independent parity by construction.** A Rust production host still
  needs the Go/Wazero runner; using only the reference runtime cannot detect
  accidental dependence on Wasmtime behavior.

### When Rust should win

Choose Rust as the whole host if a single-language native service is a hard
constraint, the team is already strong in production async Rust, maximum direct
engine control outweighs OTP reuse, and the project is willing to build and
assure its own actor/lifecycle framework. Rust is the strongest fallback if the
Elixir/Rust operational split proves more costly than its semantic benefit.

## Go

### Proposed shape

A Go host would implement the control plane with goroutines, channels,
contexts, and a durable store, while using the official independent
[Extism Go SDK](../30-sources/extism-project-2026-go-sdk.md) on
[Wazero](../30-sources/wazero-project-2026-runtime.md).

### Advantages

- **Pure-Go engine path.** The normal Extism Go stack has no cgo dependency,
  simplifying builds, static deployment, cross-compilation, and local
  debugging.
- **Straightforward concurrency.** Goroutines, channels, fixed worker pools,
  and `context.Context` are concise tools for bounded execution, deadlines,
  and request propagation. Go's official documentation explicitly demonstrates
  admission and worker-pool patterns.
- **Independent implementation.** Wazero does not merely wrap the same
  Wasmtime library. Running production-like fixtures through it provides real
  evidence against engine-family dependence.
- **Fast development and operations.** The language, formatter, test tool,
  race detector, fuzzing, profiler, and deployment model are deliberately
  cohesive.
- **Good service ecosystem.** Networking, telemetry, databases, queues, and
  infrastructure integration are mature and usually unsurprising.

### Disadvantages

- **It is not the semantic reference.** API similarity does not prove identical
  behavior for timeouts, traps, reset, WASI, host functions, memory accounting,
  exit codes, or proposal support. The repository must pin and test a portable
  subset.
- **Goroutines are not durable actors.** A channel and goroutine can implement
  a server loop, but supervision, restart policy, persistent mailboxes,
  per-agent fencing, topology, effect recovery, and observable lifecycle remain
  application semantics.
- **The engine choice and packaging advantage are coupled.** Switching to
  `libextism`/Wasmtime for reference parity introduces cgo, C pointer rules,
  native libraries, and another release matrix, as the
  [Go source](../30-sources/go-project-2026-concurrency-context-and-cgo.md)
  makes clear.
- **Cancellation is cooperative.** Closing a context indicates that work
  should stop. The selected Wazero/Extism path must actually terminate within
  the lease and deadline contracts.
- **Runtime behavior needs measurement.** Garbage collection, payload copies,
  compiled-module caches, and high-cardinality agent state may be entirely
  acceptable, but should not be decided by language folklore.

### When Go should win

Choose Go if a static, CGO-free deployment and operational simplicity dominate,
the independent Wazero feature subset satisfies the first profile, and the team
accepts building actor semantics explicitly. Regardless of the production
choice, Go/Wazero should remain in the conformance matrix.

## Elixir without an in-VM native engine

### Proposed shape

Elixir owns signals, agents, mailbox admission, supervision, policy, storage,
effects, timers, and topology. A pool of supervised Rust Port workers accepts a
small framed byte protocol and executes Extism/Wasmtime. A remote runner is a
later deployment of the same logical boundary.

There is no credible "Elixir-only, in-process Extism" choice in the inspected
official ecosystem. The current official Elixir SDK is a Rustler NIF. Calling a
Port therefore does not weaken a pure implementation that already existed; it
makes the native boundary explicit and isolated.

### Advantages

- **Best semantic match for the control plane.** BEAM processes, mailboxes,
  links, monitors, registries, tasks, and supervisors directly model the live
  runtime characteristics that inspired the repository. Existing Jido concepts
  and possibly selected Elixir components can be reused rather than translated
  conceptually first.
- **Worker failure is containable.** A Rust panic that aborts, a native engine
  fault, or a deliberate worker kill terminates the worker process. OTP can
  observe the Port exit, fail the in-flight turn without commit, replace the
  worker, and continue or restart affected agents from durable state.
- **The protocol matches the problem.** Erlang Ports are byte-oriented and
  Extism calls are bytes-in/bytes-out. Agent WASM already requires canonical
  request/result encoding, IDs, limits, and diagnostics, so this is not an
  arbitrary RPC object model.
- **Authoritative ownership stays clear.** Rust workers can own disposable
  compiled artifacts and instances while Elixir owns state, revisions, leases,
  policy, effects, and audit.
- **Reference runtime access.** The worker is normal Rust and can use current
  Extism/Wasmtime APIs without NIF term lifetimes or dirty scheduler rules.
- **Scalable isolation profiles.** The same adapter can later run one worker per
  node, pool, tenant, trust class, or sandbox without changing reducer semantics.

### Disadvantages

- **Two languages and two process artifacts.** Builds, releases, debugging,
  telemetry correlation, protocol compatibility, and security updates cross a
  boundary.
- **IPC and copies.** Inputs and outputs are framed and copied through the Port
  boundary. The actual cost for 1 KiB through 10 MiB turn payloads is unknown.
- **Backpressure is still custom.** Elixir's normal `send/2` is non-blocking and
  puts messages into a mailbox. Agent WASM must use an admission component with
  explicit count, byte, age, source, tenant, priority, and fairness limits; raw
  process mailboxes do not satisfy the draft
  [mailbox contract](../60-specification/21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
- **Synchronous callbacks become harder.** A Wasm host function that blocks the
  Rust worker while calling back into Elixir creates a re-entrant protocol,
  deadlock, deadline, and authorization problem. The bootstrap design should
  instead pass deterministic context in and return effect directives out.
- **Distribution must be engineered.** The Rust executable still needs a
  target matrix, provenance, updates, and rollback, even though it is easier to
  treat as a normal binary than as a NIF.
- **A process boundary is not a complete sandbox.** A worker can still inherit
  the host user, filesystem, network, environment, and machine-wide resources.
  Production profiles need restricted credentials, operating-system resource
  controls, and stronger sandbox/container boundaries where the threat model
  requires them.

### Why this is the recommended baseline

The repository intentionally makes execution instances disposable and keeps
authoritative state outside them. That design turns process isolation from an
expensive afterthought into a natural boundary: if the Rust worker disappears,
the host discards the uncommitted result and retries according to policy. The
official [OTP guidance](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md)
also recommends a Port when its overhead is acceptable. That overhead has not
yet been shown to be unacceptable here.

## Elixir and Rust through Rustler

### Proposed shape

Elixir retains the same control plane, but a Rust NIF embeds the current Extism
reference runtime inside the BEAM. Rustler 0.38.0 supplies term codecs,
`ResourceArc`, panic catching, dirty-scheduler annotations, and `OwnedEnv` for
messages from native threads, as documented in the
[Rustler source note](../30-sources/rustler-project-2026-safe-rust-nifs.md).

### Advantages

- **Strong division of labor.** Elixir implements actor semantics and Rust
  implements the native execution engine each language is best positioned to
  express.
- **No operating-system IPC hop.** Small calls can cross directly through NIF
  argument decoding and binary terms. This may reduce latency and copies,
  although it must be benchmarked against a Port with representative payloads.
- **Direct reference runtime.** The adapter can track the current Extism Rust
  crate and expose exactly the controls Agent WASM needs rather than wait for a
  general-purpose language SDK.
- **Typed native handles.** `ResourceArc` can safely represent disposable
  compiled modules, execution handles, and cancellation tokens shared between
  Elixir terms and Rust threads.
- **Asynchronous native completion is possible.** A normal NIF can validate a
  small request, enqueue work to a bounded Rust pool, return immediately, and
  later send a result with `OwnedEnv`. This avoids occupying a normal BEAM
  scheduler for the full call.
- **Consumer packaging has tooling.** Rustler Precompiled 0.9.0 can distribute
  checksummed artifacts across common OS, architecture, ABI, and NIF-version
  targets, as the
  [distribution source](../30-sources/rustler-project-2026-precompiled-nif-distribution.md)
  records.

### Disadvantages

- **A native crash has node-wide scope.** Rustler catches ordinary Rust panics
  at its wrapper, but Extism, Wasmtime, Cranelift, allocators, and transitive
  dependencies contain unsafe native code. A segmentation fault, abort,
  deadlock, or memory corruption can still crash or compromise the entire BEAM.
- **Long calls cannot use a normal scheduler.** Rustler and OTP both draw the
  line around one millisecond. A direct `plugin.call` must use `DirtyCpu` or be
  dispatched to a dedicated native pool. Incorrect dirty classification or
  unbounded dirty work damages node responsiveness.
- **Dirty cancellation is not process cancellation.** Killing the calling
  Elixir process does not forcibly stop a running dirty NIF. The engine must
  observe its cancellation handle or epoch deadline, and the host must not
  reuse an instance whose stop/reset state is uncertain.
- **A native pool is not OS isolation.** Returning quickly and using
  `OwnedEnv` protects scheduler availability, but worker threads remain in the
  BEAM address space.
- **Native resources are disposable only.** `ResourceArc` lifetime follows
  references and VM garbage collection. It must not own authoritative state,
  durable leases, effects, or the only copy of audit evidence.
- **The release matrix is real.** Precompilation helps users, but maintainers
  still test every supported OS, architecture, libc/ABI, OTP NIF version, CPU
  variant, Extism/Wasmtime version, and rollback combination.
- **Cross-language debugging and profiling remain.** A turn spans BEAM process
  scheduling, Rust queues or dirty schedulers, Wasmtime, and guest code.

### Audit of the current official Extism Hex package

As of 10 August 2026, Hex lists `extism` 1.0.0, last updated 8 January
2024. The inspected source:

- compiles a Rustler NIF rather than a pure-Elixir runtime;
- pins the Rust `extism` crate at 1.0.0 and Rustler's Rust crate at 0.30.0;
- accepts string input and returns UTF-8 strings rather than arbitrary binary
  payloads;
- documents no host-function support and unfinished configuration;
- contains native cancellation functions that the public `Extism.Plugin` API
  does not expose;
- manually asserts `Send` and `Sync` for its plug-in and cancellation resource
  wrappers; and
- annotates creation and plug-in calls as ordinary NIFs, with no dirty
  scheduler or asynchronous worker dispatch.

The current reference runtime source note covers Extism 1.21.0. The package is
therefore valuable precedent, but its feature, version, API, and scheduling
gaps make it unsuitable as Agent WASM's production boundary unchanged. The
recommended work is a narrow new adapter or a substantial upstream revival—not
an assumption that official ownership implies current conformance.

### When Rustler should win

Promote Rustler from optional adapter to default only if all of the following
are true:

1. Port measurements show material end-to-end harm at representative payloads
   and concurrency, not merely a microbenchmark difference.
2. Every potentially lengthy operation uses bounded native dispatch or the
   correct dirty scheduler; ordinary scheduler latency remains within target
   under overload.
3. Engine deadlines and cancellation stop real work promptly, and uncertain
   instances are discarded.
4. Deliberate worker panic, abort, hang, and native-fault exercises demonstrate
   an acceptable operational recovery story for a BEAM-node loss.
5. The supported native build matrix is reproducible, signed or attested where
   required, and continuously exercised.
6. The product's trust and availability model explicitly accepts that a native
   engine fault crosses all actors on the node.

## Recommended boundary contract

The default Port and optional Rustler adapters should expose the same small
logical operations:

| Operation | Input | Output | Ownership rule |
| --- | --- | --- | --- |
| `prepare` | artifact bytes/digest, pinned profile, engine limits | opaque disposable compiled handle or cache result | Cache may be lost at any time. |
| `invoke` | request ID, handle/digest, export, input bytes, deadline, limits | output bytes or classified engine failure plus usage | One bounded call; no authoritative state. |
| `cancel` | request ID/cancellation token | acknowledgement and eventual terminal outcome | Host retains deadline authority. |
| `dispose` | worker/handle identity | best-effort completion | Correctness never depends on destructor timing. |
| `health` | protocol/version probe | engine, Extism, kernel, build, target, feature evidence | Used for admission and observability. |

The boundary should follow these rules:

- Elixir validates artifact admission, request schemas, tenant policy, state
  revisions, and final `TurnResult` values.
- Rust receives immutable bytes and already-resolved limits. It compiles and
  invokes; it does not decide tenant authority or execute directives.
- The bootstrap profile exposes no re-entrant Elixir callbacks from a running
  plug-in. Required deterministic lookup data is included in the request;
  effects return as directives.
- Concurrency is bounded before native execution. Elixir owns queue admission
  and fairness; the worker enforces a second hard capacity limit.
- Compiled modules may be cached. Mutable plug-in instances are fresh per turn
  or demonstrably reset; no resource is the durable agent.
- Request IDs and fencing tokens make late results harmless. A result arriving
  after cancellation, deadline, lease loss, or worker replacement is rejected.
- Worker exit, Port closure, NIF error, trap, timeout, invalid output, or host
  shutdown commits no state or effects.
- Runtime version, artifact digest, limits, duration, input/output sizes,
  termination class, and adapter kind are recorded as turn evidence.

## Why Go remains mandatory in the design

Choosing Elixir and Rust for production must not reduce "portable Extism" to
"works on Wasmtime." The independent Go/Wazero runner should execute the same
canonical fixtures, malformed requests, state-erasure cases, traps, limits,
deadlines, cancellation, and error mappings in CI and release qualification.

This is a test oracle role, not an admission that Go is second-rate. If the
Wazero path later proves sufficiently complete and its operational simplicity
dominates, it can become a production runner without changing the Elixir
control-plane contract.

## Decision gates and falsification tests

The recommendation should change if evidence contradicts its premises.

### Semantic and runtime parity

- Run identical compiled guests through direct Rust/Wasmtime, the Port adapter,
  the optional Rustler adapter, and Go/Wazero.
- Compare canonical `TurnResult`, traps, non-zero status, error buffers,
  timeouts, cancellation, memory limits, output limits, reset, and state
  erasure.
- Reject a profile feature unless the intended production and independent
  conformance paths agree or the divergence is explicitly versioned.

### Boundary performance

- Measure cold compile, warm call, sustained throughput, p50/p95/p99 latency,
  CPU, resident memory, and payload copies for at least 1 KiB, 100 KiB, 1 MiB,
  and 10 MiB request/result pairs.
- Test realistic JSON or canonical binary validation and database work, not
  only an empty NIF or echo Port microbenchmark.
- Compare one actor, many actors, one hot tenant, and fair multi-tenant load.
- Prefer the Port unless Rustler changes a product-level service objective or
  resource cost materially.

### Scheduling and overload

- Saturate execution beyond capacity and verify count/byte/tenant bounds,
  priorities, fairness, rejection, and deadline expiry.
- For Rustler, record ordinary and dirty scheduler utilization and BEAM
  responsiveness while every guest consumes its maximum CPU allowance.
- For Rust and Go, verify that native/blocking work cannot starve network,
  storage, timers, or cancellation tasks.

### Cancellation and leases

- Cancel queued, compiling, running, and returning calls.
- Lose the turn lease while native execution continues; prove the late result
  cannot commit.
- Hang a guest and verify engine interruption, worker reclamation, and bounded
  shutdown time.

### Crash scope and recovery

- Trap and panic at the guest/API layer, abort the Rust worker, kill it during
  output, and corrupt or truncate its protocol frame.
- In an isolated test environment, exercise a deliberately crashing NIF and
  record that the entire BEAM node is the recovery unit.
- After every crash point around the database transaction and outbox, verify
  exactly the allowed state/effect outcome and successful replay.

### Tenant residue and resource lifecycle

- Alternate hostile tenants through caches and pools; scan outputs, logs,
  diagnostics, memory observations, Extism variables, and guest globals for
  residue.
- Drop Elixir references and terminate callers while native work runs; prove
  resources are reclaimed without depending on nondeterministic garbage
  collection for correctness.

### Packaging and operations

- Build and run the committed matrix across Linux, macOS, and Windows where
  promised, on x86-64 and Arm64, with GNU/musl and supported OTP NIF versions
  where relevant.
- Verify offline installation, provenance, checksums/attestations, rollback,
  engine security updates, mixed-version refusal, crash dumps, tracing, and
  metrics correlation across the boundary.

### Team and delivery evidence

- Implement one vertical slice in Rust-only, Go-only, and Elixir plus the Rust
  adapter before committing the entire roadmap.
- Record change lead time, defect rate, review difficulty, debugging time, and
  operational burden as well as raw performance.

## Staged adoption

1. Define the language-neutral execution adapter and canonical fixture corpus.
2. Implement a minimal Rust core using the current pinned Extism reference
   runtime.
3. Expose it first as a framed Port worker supervised by Elixir.
4. Build one real agent flow through bounded admission, snapshot load,
   invocation, result validation, atomic state/journal/outbox commit, and effect
   result signal.
5. Run the same fixtures through Go/Wazero.
6. Add a Rustler adapter to the same Rust core only for comparison; use bounded
   native threads or correctly classified dirty CPU work.
7. Run the gates above and record the decision. If Elixir's total complexity
   loses, fall back to Rust-only; if Wazero's simplicity and parity win, consider
   Go for the runner or whole host.

## Evidence, inference, and unresolved questions

Supported directly by primary sources:

- Rust's ownership/concurrency guarantees and Tokio's blocking-task behavior;
- Go's goroutine, channel, context, cgo, and fuzzing mechanisms;
- Elixir process isolation, non-blocking mailbox send, supervisors, and process
  anti-pattern guidance;
- OTP's NIF crash scope, dirty scheduling rules, threaded-NIF option, Port
  isolation, and recommendation to prefer a Port when possible;
- Rustler 0.38.0's NIF macro, dirty flags, resources, `OwnedEnv`, and current
  Hex packaging;
- Rustler Precompiled 0.9.0's checksum and native target matrix; and
- the current official Extism Elixir SDK's public API, pinned native versions,
  source structure, and omissions.

Local inference:

- Elixir's actor facilities reduce the amount of semantic translation needed
  for this Jido-inspired host.
- A coarse Port boundary will likely preserve sufficient performance because a
  turn already includes serialization, validation, Wasm, and durable work.
- Maintaining one Rust core behind two adapters can preserve an optimization
  path without making NIF risk the initial default.

Those inferences are falsifiable. The largest unknowns are Port cost at real
payload sizes, scheduler behavior at maximum concurrency, synchronous
host-function needs, database and deployment choices, team expertise, and the
acceptable failure domain for a production node.

## Connections

- [Host implementation language map](../10-maps/agent-wasm-host-implementation-language.md)
  — routes through the options, native boundary, and evidence program.
- [Which Host Implementation Approach Should Agent WASM Use?](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
  — tracks the recommendation until prototypes and fault tests can resolve it.
- [Jido Agent Architecture and a Wasm/Extism Construction](jido-agent-architecture-and-wasm-extism-construction.md)
  — supplies the host-owned actor and reducer model being implemented.
- [Extism Plugin-System Architecture and Runtimes](extism-plugin-system-architecture-and-runtimes.md)
  — supplies the engine families, ABI, state, limit, and portability context.
- [WebAssembly Testing, Verification, and Agent Runtime Assurance](webassembly-testing-verification-and-agent-runtime-assurance.md)
  — defines the broader assurance stack for the proposed host.

## Sources

- [Rust Ownership and Concurrency](../30-sources/rust-project-2026-ownership-and-concurrency.md)
- [Tokio Task Runtime and Blocking Work](../30-sources/tokio-project-2026-task-runtime.md)
- [Go Concurrency, Context, and C Interoperation](../30-sources/go-project-2026-concurrency-context-and-cgo.md)
- [Elixir Processes, Mailboxes, and Supervision](../30-sources/elixir-project-2026-processes-and-supervision.md)
- [Erlang NIFs, Dirty Schedulers, and Ports](../30-sources/erlang-project-2026-nifs-dirty-schedulers-and-ports.md)
- [Rustler Safe Rust NIF Bridge](../30-sources/rustler-project-2026-safe-rust-nifs.md)
- [Rustler Precompiled NIF Distribution](../30-sources/rustler-project-2026-precompiled-nif-distribution.md)
- [Extism Elixir Host SDK](../30-sources/extism-project-2026-elixir-sdk.md)
- [Extism Reference Runtime](../30-sources/extism-project-2026-reference-runtime.md)
- [Extism Go SDK](../30-sources/extism-project-2026-go-sdk.md)
- [Wazero Runtime](../30-sources/wazero-project-2026-runtime.md)
- [Jido Runtime and Coordination](../30-sources/agentjido-2026-jido-runtime-and-coordination.md)
