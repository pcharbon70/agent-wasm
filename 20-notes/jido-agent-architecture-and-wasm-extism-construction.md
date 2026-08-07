---
title: "Jido Agent Architecture and a Wasm/Extism Construction"
kind: note
created: "2026-08-07"
maturity: developing
tags:
  - agent-tools
  - extism
  - jido
  - plugin-system
  - runtime
  - security
  - webassembly
aliases:
  - "Jido architecture above Elixir"
  - "Jido on Wasm and Extism"
---

# Jido Agent Architecture and a Wasm/Extism Construction

## Executive conclusion

Jido is best understood above Elixir as a **stateful event-processing and
effect-interpretation framework**. An agent is a versioned state machine. A
signal selects an instruction. A strategy advances the machine. The result is
a complete new state plus typed descriptions of work for a runtime. The live
runtime supplies identity, serialization, scheduling, supervision, I/O,
durability, and coordination.

That division is unusually compatible with WebAssembly:

- the agent, action, route, and strategy logic can be compiled into portable
  Wasm reducers;
- the mailbox, registry, timers, storage, network, model providers, monitoring,
  and directive interpreter must remain host services;
- Extism can provide a pragmatic bytes-in/bytes-out module boundary and
  cross-language guest toolchains;
- Jido's capability plugins must remain a framework-level composition concept,
  not be collapsed into Extism's term “plug-in,” which denotes an executable
  Wasm module.

The recommended construction is therefore not “port OTP into Wasm.” It is a
host-owned actor runtime that invokes Wasm decision modules for one serialized
turn at a time. Authoritative state stays outside guest memory. A successful
guest return is validated and committed together with a durable directive
outbox. Only then does the host execute authorized effects and return their
results as new signals.

The most important adaptation is stricter than Jido itself: although Jido
allows actions to perform immediate I/O, a durable Wasm profile should prefer
effect requests and continuations. Synchronous host functions should be a
small, explicitly granted exception for operations whose result is required in
the current turn.

## Research question, scope, and method

The question is: **which Jido abstractions survive removal of Elixir and the
BEAM, and how should those abstractions be divided between a Wasm/Extism guest
and a portable host runtime?**

The analysis uses Jido 2.3.2, Jido Action 2.3.2, Jido Signal 2.2.2, and Jido AI
2.3.0 as observed on 7 August 2026. It reads the official architectural guides,
package documentation, API contracts, and tagged source. The primary evidence
is recorded in the connected [source notes](../10-maps/jido-agent-architecture.md#primary-evidence).

This note deliberately abstracts away syntax, macros, structs, processes, and
module dispatch. It retains only responsibilities, dataflows, invariants,
failure semantics, and extension points. The proposed Wasm design is an
architectural inference, not a claim that Jido currently supports Wasm.

## Jido's architecture above Elixir

### The minimal semantic loop

Jido's canonical flow is:

```text
signal
  -> preparation and route resolution
  -> instruction/action
  -> strategy command
  -> complete next agent state + state operations + directives
  -> runtime effect interpretation
  -> result signal or external delivery
```

The [overview and core-loop documentation](../30-sources/agentjido-2026-jido-overview-and-core-loop.md)
establishes two invariants:

1. the agent returned from the command boundary is already a complete value;
2. directives describe external work and do not later mutate that returned
   value behind the caller's back.

This is a reducer with an effect algebra. It resembles Elm or Redux more than
an object whose methods hide mutation. The live runtime is an interpreter for
the effect values produced by that reducer.

### Five planes

The component list becomes clearer when grouped by responsibility rather than
package or module name.

| Plane | Jido concepts | Responsibility |
| --- | --- | --- |
| Decision | Agent, Action, Instruction, StateOp, Strategy | Validate an operation and calculate the next state and requested effects. |
| Messaging | Signal, Router, Dispatch, correlation/causation | Normalize events, select work, and carry results between actors and integrations. |
| Runtime | AgentServer, DirectiveExec, Sensor runtime, Scheduler, Await | Serialize turns, execute effects, manage time and external connections, expose completion. |
| Lifecycle | Jido instance, registry, parent references, InstanceManager, worker pool | Own identity, activation, monitoring, restart, hibernate/thaw, concurrency, and reuse. |
| Composition and durability | Plugin, Pod, Thread, Checkpoint, Storage, partition | Package capabilities, describe teams, record history and snapshots, and namespace tenants. |

AI sits above these planes. Jido AI supplies model-facing strategies and
providers, but it consumes the same actions, state, signals, and runtime
contracts. The [AI package](../30-sources/agentjido-2026-jido-ai-runtime.md)
therefore supports a useful design principle: an agent framework is not
synonymous with an LLM loop.

## Component semantics

### Agent: durable decision identity

An agent is an identity, metadata, validated state, installed capabilities,
strategy configuration, routes, and schedules. As a value it has no mailbox,
clock, storage connection, or independent thread of execution. This separation
lets its decision logic be tested without starting the runtime.

At a language-neutral level, an agent definition should contain:

- a stable type and version;
- a state schema and initial-state function;
- route and action declarations;
- a selected strategy and its schema;
- installed capability bundles;
- optional migrations between state versions.

An agent instance adds an instance identifier, tenant or partition, state
revision, current snapshot, lifecycle policy, and artifact digest.

### Action and instruction: operation definition versus invocation

The [action architecture](../30-sources/agentjido-2026-jido-actions.md) separates
four ideas that are often conflated:

- **Action:** named operation, schemas, metadata, and implementation.
- **Instruction:** normalized action reference plus parameters, context, and
  execution settings.
- **Executor:** timeout, retry, cancellation, compensation, and telemetry
  policy.
- **Plan:** a dependency graph of instructions and parallel phases.

This matters for agent tools. A model-visible tool definition is only a
projection of action metadata; it is not authorization to invoke the action,
an execution policy, or a workflow graph.

### State operation: internal transition vocabulary

Simple action results deep-merge an update into state. State operations make
non-trivial transitions explicit: replace state, delete keys, and set or delete
nested paths. A strategy applies these operations before returning the next
agent value.

In a portable design, state operations are not arbitrary guest memory writes.
They are a typed patch language checked against the current revision and state
schema. The host may reject a patch that touches a reserved namespace, exceeds
size limits, or conflicts with the version loaded at the start of the turn.

### Directive: external effect vocabulary

The [directive contract](../30-sources/agentjido-2026-jido-directives-and-state-operations.md)
includes signal emission, task and agent spawning, adoption and termination,
sensor control, delayed and recurring scheduling, continuation instructions,
and explicit stops. Custom effect handlers extend the vocabulary.

A directive is not itself an effect. It is data asking a trusted interpreter
to perform an effect. This distinction supports:

- centralized authorization;
- deterministic tests of decision logic;
- logging before execution;
- retries and idempotency;
- alternative interpreters for local tests, production, or simulation.

The last three properties are only latent in an in-memory queue. A durable
Wasm runtime should make them explicit with an outbox.

### Signal and router: the control-message fabric

Jido signals use a CloudEvents-derived envelope with stable type, source,
subject, data, correlation, and causation. Strategy, agent, and plugin routes
have explicit precedence. Dispatch destinations are configuration rather than
properties that must be embedded in the signal itself. These details are
captured in the [signals source note](../30-sources/agentjido-2026-jido-signals-and-routing.md).

At the architectural level, signals provide three things:

1. a language-neutral envelope around domain payloads;
2. a causal record for multi-step and multi-agent work;
3. a single ingress path for API calls, timers, sensors, child events, and
   effect results.

Transport semantics are separate. A direct call, a local asynchronous cast,
a broker subscription, and a webhook do not magically share delivery
guarantees just because they carry the same envelope.

### Strategy: replaceable transition policy

Strategies determine how instructions advance the agent. Direct execution,
finite-state machines, behavior trees, plans, and ReAct-style reasoning can all
share a stable snapshot of status, completion, result, and details. Strategy
state lives in a reserved namespace and may advance through initialization,
commands, and scheduled ticks.

The finite-state strategy demonstrates the core pattern: when a transition
requires effectful work, it emits a result-bearing instruction directive and
waits. The runtime executes the work and feeds the result back into the state
machine. That continuation style is a particularly good fit for durable Wasm.

### Framework plugin: a capability bundle

A Jido plugin packages actions, namespaced state and schema, configuration,
routes, schedules, lifecycle hooks, and sometimes owned runtime services. Its
ordered hooks can verify or canonicalize inbound messages, authorize the
resolved action, prepare outbound signals, and transform the synchronous
caller view. The [plugin and strategy documentation](../30-sources/agentjido-2026-jido-plugins-and-strategies.md)
also warns that state namespacing is not a sandbox.

The word “plugin” is overloaded:

| Term | Meaning |
| --- | --- |
| Jido plugin | A framework-level capability manifest and lifecycle extension. |
| Extism plug-in | A loadable core-Wasm executable obeying Extism's calling convention. |

One Jido-style plugin could reference zero, one, or many Extism modules. One
Extism module could implement an entire agent, several actions, or only a
strategy. Equating the terms would make packaging dictate architecture.

### AgentServer: live actor cell

The [runtime documentation](../30-sources/agentjido-2026-jido-runtime-and-coordination.md)
shows that AgentServer is the live shell around the value. It serializes signal
processing, holds the current state, runs preparation hooks, resolves routes,
calls the strategy, drains directives, tracks children and asynchronous work,
and exposes synchronous and asynchronous ingress.

Its parent-child graph is logical rather than a nested supervision tree. Live
agents are runtime peers, with monitored relationships and explicit parent
death policy. Completion is stored state; process death is an infrastructure
event. Cancellation is a signal the agent may handle, not an unconditional
thread kill.

These are actor-runtime semantics. They are not provided by the Wasm core
specification or Extism.

### Sensors and scheduler: event-source adapters

Sensors bridge long-lived external sources into signals. Their runtime owns
connections, subscriptions, timers, monitoring, and cleanup; their decision
callback transforms an event into new state and emitted signals. Schedules
also re-enter the agent through the ordinary signal path. The
[sensor and scheduler source](../30-sources/agentjido-2026-jido-sensors-and-scheduling.md)
documents intentional gaps such as absent sensor backpressure and non-replayed
missed cron ticks.

This decomposition keeps external liveness out of the agent value. It also
indicates that a Wasm sensor should normally be a payload transformer embedded
inside a host connector, not a guest that owns a socket indefinitely.

### Instance, partition, and worker pool: three different boundaries

A Jido instance owns a supervision and registry scope and is the stronger
operational boundary. A partition provides logical namespacing inside an
instance. A worker pool bounds concurrency and amortizes startup. The
[multi-tenancy and pool guidance](../30-sources/agentjido-2026-jido-multi-tenancy-and-worker-pools.md)
is explicit that partitions are not hard isolation and pooled agents retain
state unless reset.

This distinction must survive in a Wasm design:

- tenant namespace is an identity and storage concern;
- sandbox instance is a memory and capability concern;
- execution pool is a capacity and latency concern.

Using one identifier or one pool to stand in for all three invites data leaks.

### InstanceManager and Pod: durable activation and topology

Jido distinguishes live agents, tracked live children, durable keyed agents,
and durable named teams. A Pod stores a graph of nodes plus ownership and
dependency edges, activates nodes eagerly or lazily, and reconciles the live
shape from durable intent. PIDs and monitors are never persisted. The
[runtime-pattern and Pod source](../30-sources/agentjido-2026-jido-runtime-patterns-and-pods.md)
is a strong model for separating desired topology from disposable execution
handles.

This is more than an implementation detail. It is the right abstraction for
portable agent deployment: persistent nodes reference identities, artifact
digests, policies, and state; a reconciler recreates engine instances wherever
the runtime can satisfy them.

### Thread, checkpoint, and storage: history versus projection

The [persistence model](../30-sources/agentjido-2026-jido-persistence-and-storage.md)
separates an append-only Thread from a checkpointed state projection. The
checkpoint stores a thread identifier and revision rather than copying the
history. Hibernate flushes history before taking the snapshot; thaw loads both
and checks their relationship.

The general lesson is that agent state, audit history, and conversational
transcript are not the same object. State is a current projection. The journal
is ordered evidence. Model context is a selected projection of one or both.

## What ports and what must be reconstructed

### Direct mapping

| Jido abstraction | Wasm/Extism construction |
| --- | --- |
| Agent definition | Versioned manifest plus one or more content-addressed Wasm artifacts. |
| Agent state | Host-persisted, schema-versioned snapshot with revision. |
| `cmd` | Deterministic guest `reduce` export. |
| Action | Guest handler and schema; effectful operations require grants. |
| Instruction | Versioned invocation envelope with params, context references, deadline, and idempotency key. |
| StateOp | Typed, host-validated patch applied during commit. |
| Directive | Typed capability request placed in a durable outbox. |
| Signal | Versioned CloudEvents-like envelope with causal identifiers. |
| Router | Trusted host route compiler plus optional guest-defined declarative routes. |
| Strategy | Guest reducer, possibly separately packaged, with stable snapshot schema. |
| AgentServer | Host actor cell: mailbox, turn lock, state cache, invocation, commit, and outbox drain. |
| DirectiveExec | Host capability broker and effect handlers. |
| Sensor | Host connector with optional Wasm payload transform. |
| Scheduler | Host timer service that emits signals. |
| InstanceManager | Host activation, idle eviction, restore, and artifact-loading service. |
| Pod | Durable artifact/identity topology plus reconciler. |
| Thread/checkpoint | Append log plus versioned snapshot and revision pointer. |
| Partition | Tenant-scoped identity, policy, storage, keys, and telemetry namespace. |
| Worker pool | Compiled-module cache plus clean execution-slot pool, never shared mutable agent state. |

### BEAM properties that do not come along

Compiling decision logic to Wasm does not reproduce:

- lightweight preemptively scheduled processes;
- per-process mailboxes and selective receive;
- links, monitors, supervisors, and restart strategies;
- distributed process identity;
- runtime code loading and language-native term semantics;
- process garbage collection and failure isolation;
- the scheduler's fairness and reduction accounting.

A Jido-like framework on Wasm must implement or choose alternatives for each.
Extism helps instantiate and call modules; it is not an actor system,
durability layer, event broker, or supervisor.

## Proposed host–guest contract

### Guest exports

A minimal Extism profile could expose:

```text
describe(input: ProtocolVersion) -> AgentManifest
initialize(input: InitRequest) -> TurnResult
reduce(input: TurnRequest) -> TurnResult
migrate(input: MigrationRequest) -> MigrationResult
```

`describe` may be cached and should return schemas, routes, actions, strategy
metadata, required capabilities, state versions, and protocol versions.
`initialize` calculates initial state and startup requests without acquiring
resources. `reduce` handles signals or explicit instructions. `migrate`
transforms durable snapshots under a separately authorized maintenance path.

A single `reduce` entry point is preferable to a large export surface for an
initial profile: it makes the protocol versionable as data and avoids dynamic
linking assumptions across Extism runtimes. Specialized exports can be added
only after profiling shows a need.

### Turn request

```text
TurnRequest {
  protocol_version,
  invocation_id,
  agent { type, version, instance_id, state_revision },
  signal,
  instruction?,
  state,
  strategy_state?,
  runtime_context,
  grants,
  deadline,
  trace_context
}
```

The guest receives a value snapshot, not a handle to authoritative mutable
state. Sensitive runtime context should contain references or attenuated facts,
not raw credentials. The grants list tells the guest which directive kinds and
host calls may succeed, but the host still enforces it independently.

### Turn result

```text
TurnResult {
  protocol_version,
  invocation_id,
  expected_state_revision,
  state_patch,
  directives[],
  strategy_snapshot,
  domain_status,
  diagnostics[]
}
```

Every directive should carry a deterministic or invocation-scoped identifier,
kind, payload schema, requested capability, causal metadata, and optional
completion signal specification. Unknown fields and unknown directive kinds
need explicit compatibility rules; silent fallback is unsafe for authority-
bearing requests.

### Encoding

Extism's common contract is bytes, not WIT types. JSON is the easiest bootstrap
encoding and best for inspection, but it needs canonicalization rules and has
numeric and binary limitations. MessagePack or CBOR can reduce boundary cost
later. Whatever the encoding, the protocol needs:

- an explicit version and schema identifier;
- size, depth, collection, and string limits;
- canonical representations for identifiers, timestamps, errors, and bytes;
- rejection of duplicate or unknown authority-bearing fields;
- stable compatibility and deprecation rules;
- test vectors shared by every guest SDK and host runtime.

The [Extism synthesis](extism-plugin-system-architecture-and-runtimes.md)
explains why this application protocol must be defined above Extism's memory
and calling convention.

## One complete turn

The proposed host flow is:

1. Accept a signal and authenticate its transport identity.
2. Resolve tenant, agent identity, artifact digest, and policy.
3. Validate and canonicalize the signal; preserve correlation and causation.
4. Acquire a per-agent turn lease so only one revision is advanced at a time.
5. Load the snapshot and associated journal revision.
6. Resolve the route and authorize the target action in trusted host policy.
7. Acquire a clean Extism execution instance for the pinned artifact.
8. Invoke `reduce` with deadline, fuel or equivalent budget, memory limit, and
   the minimum host-function set.
9. Treat trap, timeout, invalid encoding, oversize output, or schema failure as
   a failed turn; do not commit state or effects.
10. Validate the expected revision, patch, strategy snapshot, directive types,
    destinations, and capability grants.
11. Atomically commit the next state, journal facts, and directive outbox.
12. Release the turn lease and acknowledge the input according to its delivery
    contract.
13. Drain outbox entries through idempotent effect handlers.
14. Convert result-bearing effects, timer fires, child lifecycle events, and
    sensor events into new signals.

The atomic boundary in step 11 is a proposal beyond Jido's documented
in-memory directive queue. It closes the crash gap between accepting a state
transition and attempting its external effects.

## Effects: directives first, host functions second

There are two ways for guest code to reach the world.

### Asynchronous or durable effect request

The preferred pattern is:

```text
guest returns Request(model.call, ...)
  -> host commits waiting state + outbox request
  -> effect worker calls provider
  -> host emits model.result or model.failed
  -> guest handles the next turn
```

This supports crash recovery, retries, audit, approval, cancellation, and
human-in-the-loop pauses. It maps directly to Jido's result-bearing instruction
and FSM continuation pattern.

### Synchronous host function

A custom Extism host function can return data during the current call. This is
appropriate only when splitting the turn would make the action unusable and
the operation can be bounded, cancelled, and safely retried. Examples may
include a deterministic lookup in a host-owned read snapshot or a tightly
bounded cryptographic service.

Network, filesystem, database, model, and secret operations should not be
granted as ambient WASI access. Each should be a narrow application capability
with tenant, resource, purpose, deadline, and result limits. A synchronous call
also makes transaction and cancellation semantics harder: the external effect
may complete even if the guest later traps or the state commit loses a race.

## State, memory, pooling, and concurrency

Authoritative agent state must not live in Wasm linear memory, Extism
variables, or a long-lived plugin instance. Those stores are useful only as
discardable per-call scratch or caches because:

- their persistence differs by runtime and reset path;
- they are not naturally tied to the durable state revision;
- pooling can expose previous callers' data;
- migration and inspection become engine-dependent;
- a guest trap can leave uncertain transient state.

Compiled artifacts and verified metadata can be shared widely. Mutable
instances should be fresh per turn or provably reset. A stateful instance may
be pinned to one agent as an optimization only if the host snapshot remains
authoritative and differential tests prove that eviction, reset, trap, and
restore do not change semantics.

Each agent processes one committed turn at a time. Parallelism occurs across
agents or in host-managed effect workers. Optimistic state revisions provide a
second line of defense against duplicate workers or lease expiry.

## Composition and packaging

A framework capability manifest should describe:

- package name, semantic version, publisher, and artifact digests;
- protocol and state-schema versions;
- actions and their input/output schemas;
- routes and precedence;
- state namespaces and migration ownership;
- requested host capabilities;
- schedules and sensors;
- trusted lifecycle-hook classes;
- dependencies on other capability packages.

The host composes these manifests into an effective agent definition, checks
route and state-key conflicts, resolves artifacts, and produces a signed lock
record. Composition should happen outside guest memory so the host can inspect
and authorize the result.

Possible artifact granularity is a tradeoff:

| Shape | Advantages | Costs |
| --- | --- | --- |
| One module per agent definition | Simple invocation and shared in-guest state model. | Coarser updates and less reusable actions. |
| One module per capability bundle | Mirrors framework plugins and supports reuse. | Host must compose routes, state, and cross-module calls. |
| One module per action | Fine-grained admission and independent updates. | High instantiation and serialization overhead. |
| Hybrid | Common reducer plus separately admitted high-risk tools. | More packaging rules and test combinations. |

The hybrid is the strongest initial candidate: package an agent's reducer,
routes, and ordinary pure actions together; isolate high-authority or
independently versioned operations behind host services or separately admitted
modules.

## Durable topology and activation

A Wasm Pod analogue should persist:

```text
Topology {
  version,
  nodes { logical_name, agent_type, artifact_digest, state_key, activation },
  links { relation: owns | depends_on, from, to },
  policy_refs
}
```

It must not persist engine stores, Extism plugin handles, threads, sockets, or
worker identifiers. A reconciler loads or starts each node in dependency waves,
reattaches ownership, and recursively reconciles nested topology. Activation
can be eager or lazy. Cycles should be rejected unless a later specification
defines a safe fixed-point model.

The desired topology is authoritative; the live graph is a repairable
projection. This also allows a future distributed scheduler without changing
agent logic, although distribution requires leases, fencing, placement, and
consensus that Jido's current single-node Pod model does not supply.

## Security model

### Trusted versus untrusted phases

Jido's plugin lifecycle suggests useful phases, but a Wasm host must assign
trust deliberately:

1. **Transport authentication and signal canonicalization:** trusted host or
   privileged signed extension.
2. **Route resolution:** trusted declarative compiler; a guest may propose
   routes but cannot bypass policy.
3. **Action authorization:** trusted host, after the action is resolved.
4. **Decision execution:** untrusted or partially trusted Wasm.
5. **Output validation and capability attenuation:** trusted host.
6. **Outbound signing, encryption, and dispatch:** trusted host service.
7. **Caller-view formatting:** may be untrusted because it grants no authority,
   but it must not alter the committed state or audit record.

An untrusted module cannot be allowed to supply the only check that authorizes
its own action or directive.

### Isolation tiers

Logical partitions alone are insufficient. A tenant isolation profile should
bind together:

- registry and storage namespace;
- encryption keys and secret references;
- capability policy and rate limits;
- compiled artifact admission;
- execution-store or process isolation;
- instance-pool membership;
- network policy;
- telemetry and audit access.

For high-risk tenants, separate host processes or nodes may be necessary even
when Wasm supplies memory isolation. The core Wasm sandbox contains guest
memory; it does not prevent a powerful host function from becoming a confused
deputy.

### Output is untrusted

The host must validate guest output just as carefully as input. Directives are
authority requests. State patches can poison later prompts or cross namespace
boundaries. Routes, URLs, resource identifiers, emitted signal types, and
model-facing text all need policy and size checks. The
[WebAssembly foundations synthesis](webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
provides the broader layered containment model.

## Failure, cancellation, and delivery semantics

A useful initial contract is:

- a guest trap, timeout, cancellation, or invalid output commits nothing;
- a committed input advances exactly one state revision;
- committed directives are delivered at least once from the outbox;
- every effect type declares its idempotency and deduplication contract;
- an effect result is a new causally linked signal;
- agent completion is durable state, independent of actor activation;
- infrastructure death causes restore or retry according to lifecycle policy;
- cancellation is a durable request plus optional hard deadline, not only an
  in-memory message;
- timers declare whether missed firings are skipped, coalesced, or replayed.

Exactly-once external effects are generally impossible without cooperation
from the target system. The runtime can instead provide exactly-once state
revision, at-least-once outbox delivery, stable idempotency keys, and explicit
evidence of attempts and outcomes.

## Observability and provenance

Every turn should produce a host-owned record containing:

- tenant and agent identities;
- input signal and causal identifiers;
- artifact and manifest digests;
- protocol, state, and policy versions;
- resolved route and action;
- grants actually supplied;
- resource limits and measured usage;
- prior and committed state revisions;
- directive identifiers and disposition;
- trap, timeout, validation, and effect outcomes;
- trace context and timestamps.

Guest diagnostics can enrich this record but cannot replace it. Model prompts,
secrets, and large payloads require redaction and separate access controls.
The audit journal and the user-facing conversation should remain distinct
projections.

## A staged construction program

### Stage 1: deterministic single-agent kernel

Build one host, one Extism runtime, one `reduce` export, JSON test vectors,
host-owned snapshots, schema validation, and a no-I/O directive interpreter.
Support signals, actions, state patches, direct and FSM strategies, and
terminal status. Verify identical replay from the same state and input.

### Stage 2: durable effects

Add a journal, snapshots, revisions, transactional outbox, idempotent emission,
delayed signals, and result-bearing effect continuations. Fault-inject at every
point between guest return, commit, effect start, effect completion, and result
signal.

### Stage 3: capabilities and framework plugins

Add signed capability manifests, trusted preparation/authorization phases,
host functions for a deliberately small synchronous profile, composition
conflict checks, and separate pure versus privileged extension classes.

### Stage 4: activation and multi-agent topology

Add identity registry, lazy activation, hibernate/thaw, parent relations, Pod-
like topology, reconciliation, cancellation, fan-out/fan-in, and bounded
mailboxes. Keep live handles out of durable state.

### Stage 5: runtime portability

Run the same conformance suite on the Extism reference runtime and an
independent implementation such as Go/Wazero. Compare encoding, limits,
timeouts, cancellation, reset, traps, and host-function behavior. This stage
connects directly to [the Extism adoption inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md).

### Stage 6: AI and high-authority integrations

Expose model calls, retrieval, code execution, and external connectors as
policy-governed effects. Add approvals, quotas, secret leases, provenance, and
prompt-output controls only after the underlying turn and effect model is
stable.

## Tempting translations to reject

- **One Wasm instance equals one BEAM process.** An engine instance lacks the
  mailbox, monitor, scheduler, registry, and restart semantics that make the
  analogy useful.
- **Keep agent state in Extism variables.** This couples durability and
  isolation to instance reuse and reset behavior.
- **Expose full WASI and call it a directive system.** Ambient filesystem and
  network imports bypass typed framework policy and audit.
- **Let every action call synchronous host functions.** This recreates hidden
  effects and makes retries and crash recovery ambiguous.
- **Use a tenant string as the sandbox.** Namespacing is not memory, process,
  secret, or capability isolation.
- **Pool stateful plugin instances across callers.** Both Jido's pool guidance
  and Extism's state model warn that mutable state can survive reuse.
- **Persist live runtime handles.** Topology and identity are durable; engine,
  process, socket, and monitor handles are disposable projections.
- **Treat LLM reasoning as the agent kernel.** It is one replaceable strategy
  and capability consumer, not the architecture's foundation.

## Evidence, inference, and proposal boundary

### Supported by Jido's official sources

- The agent command returns complete new state plus directives.
- State operations and directives have distinct interpreters.
- AgentServer owns live serialization and effect execution.
- Plugins bundle state, actions, routes, and lifecycle hooks.
- Strategies replace execution policy behind a stable snapshot.
- Sensors and schedules convert external events and time into signals.
- Partitions are logical boundaries; separate instances are stronger.
- Pods persist topology but not live process state.
- Threads and checkpoints serve different persistence roles.
- Jido AI is optional and layered above the core.

### Architectural inference

- Jido's command boundary is a suitable Wasm reducer interface.
- Actor, lifecycle, topology, policy, and storage services belong in the host.
- Framework plugins should compose manifests and may reference multiple Wasm
  artifacts.
- Extism state should be treated as disposable cache rather than authoritative
  agent state.

### New proposals

- Atomically commit state, journal records, and a directive outbox.
- Use stable effect identifiers and at-least-once delivery with idempotency.
- Prefer asynchronous effect/result signals over synchronous host functions.
- Define trust classes for plugin hooks and keep authorization host-owned.
- Pin a versioned byte protocol with shared conformance vectors.

## Falsification and decision criteria

The proposed architecture should be reconsidered if experiments show any of
the following:

- reducer serialization dominates realistic turn latency or state size;
- two target Extism runtimes cannot implement equivalent limits, cancellation,
  reset, errors, and host capabilities for the pinned profile;
- common strategies require so many synchronous host calls that the directive
  continuation model becomes unusable;
- snapshot-plus-patch transfer cannot support the required state scale without
  unsafe shared mutable memory;
- the manifest composition model cannot detect route, state, migration, and
  capability conflicts before execution;
- crash injection yields unbounded duplicate effects or state/effect
  divergence despite the outbox and idempotency design;
- instance pooling cannot prove state erasure across tenants at acceptable
  cost;
- a WIT Component Model interface provides materially stronger portability and
  typed async behavior with less application protocol than Extism by the time
  implementation begins.

## Open questions

- Should routing execute entirely in the host, or may a guest return a route
  proposal for dynamic cases?
- Is state transferred as a full snapshot, typed patch base, or capability-
  mediated read model for large agents?
- Which effects, if any, qualify for the synchronous host-function profile?
- How are action and strategy artifacts linked and versioned independently?
- Which hooks can third parties provide, and which require a privileged
  publisher trust root?
- What mailbox bounds, overflow behavior, priority, and fairness are required?
- Which timer and signal delivery guarantees are part of the portable profile?
- When should an actor be pinned to an instance, and how is reset verified?
- Does Extism remain the best bootstrap ABI once Component Model async support
  is broadly implemented?

These are converted into testable work in
[How Should Agent WASM Construct a Jido-Like Framework?](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md).

## Sources

- [Overview and core loop](../30-sources/agentjido-2026-jido-overview-and-core-loop.md)
- [Actions and execution](../30-sources/agentjido-2026-jido-actions.md)
- [Signals and routing](../30-sources/agentjido-2026-jido-signals-and-routing.md)
- [Directives and state operations](../30-sources/agentjido-2026-jido-directives-and-state-operations.md)
- [Runtime and coordination](../30-sources/agentjido-2026-jido-runtime-and-coordination.md)
- [Plugins and strategies](../30-sources/agentjido-2026-jido-plugins-and-strategies.md)
- [Sensors and scheduling](../30-sources/agentjido-2026-jido-sensors-and-scheduling.md)
- [Runtime patterns and Pods](../30-sources/agentjido-2026-jido-runtime-patterns-and-pods.md)
- [Persistence and storage](../30-sources/agentjido-2026-jido-persistence-and-storage.md)
- [Multi-tenancy and worker pools](../30-sources/agentjido-2026-jido-multi-tenancy-and-worker-pools.md)
- [Jido AI runtime](../30-sources/agentjido-2026-jido-ai-runtime.md)
- [Jido 2.3.2 source architecture](../30-sources/agentjido-2026-jido-2-3-2-source-architecture.md)
