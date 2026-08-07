---
title: "Extism Plugin-System Architecture and Runtimes"
kind: note
created: "2026-08-07"
maturity: developing
tags:
  - agent-tools
  - extism
  - plugin-system
  - runtime
  - security
  - webassembly
aliases:
  - "Extism deep dive"
---

# Extism Plugin-System Architecture and Runtimes

## Executive conclusion

Extism is best understood as a portable **core-WebAssembly plug-in protocol
plus a family of host implementations**. It is not a new Wasm engine and it is
not simply a wrapper around Wasmtime.

The portable center is deliberately small:

- plug-in exports use no core-Wasm parameters and return no result or one
  `i32` status;
- application input and output travel as byte buffers through an
  offset-and-length convention;
- built-in imports live under `extism:host/env` and application host functions
  default to `extism:host/user`; and
- an internal Wasm kernel, `extism-runtime.wasm`, implements the resettable
  allocator and input, output, and error bookkeeping.

Everything around that center is host policy and implementation: module
loading, hashing, linking, configuration, mutable variables, HTTP, WASI,
filesystem mappings, logging, timeouts, cancellation, memory limits, custom
host functions, compilation caches, pools, and native packaging.

That split lets one plug-in run on four materially different stacks:

1. the Rust reference runtime on Wasmtime, used directly or through
   `libextism` by many language SDKs;
2. the pure-Go SDK on Wazero;
3. the JavaScript SDK on the WebAssembly engine already inside a browser,
   Node.js, Deno, Bun, or a worker platform; and
4. the experimental pure-Java SDK on Chicory, alongside the separate,
   established Java SDK that binds `libextism`.

The important qualification is that protocol portability is not full
behavioral parity. Engine features, WASI coverage, timeout mechanics, memory
accounting, filesystem support, HTTP scheduling, thread availability, and
failure modes differ. Extism is therefore a strong candidate for a pragmatic
Agent WASM plug-in layer, but adoption should be conditioned on a pinned
profile and differential conformance tests rather than the SDK API alone.

## Scope and method

This review asks:

1. What exactly constitutes an Extism plug-in and host?
2. How are modules loaded, linked, called, and given capabilities?
3. Which components are shared across runtimes and which are reimplemented?
4. How do the Wasmtime, Wazero, JavaScript, native-Java, and Chicory paths
   differ?
5. What would Extism provide—and leave unresolved—for Agent WASM?

The evidence is the current official documentation, Extism Improvement
Proposals, and implementation repositories inspected on 7 August 2026. The
reference runtime release inspected is 1.21.0. No local performance or
cross-runtime conformance experiment was performed in this pass. Where prose
documentation and source appear to disagree, the discrepancy is recorded as
an open test rather than silently resolved.

## The architectural stack

```text
Host application
  └─ Host SDK API
      ├─ manifest and module resolver
      ├─ policy: WASI, paths, hosts, limits, timeout, config
      ├─ Extism built-ins: vars, HTTP, logs, host functions
      └─ engine adapter
          ├─ Wasmtime  ← Rust and libextism-backed SDKs
          ├─ Wazero    ← Go SDK
          ├─ JS engine ← browser, Node, Deno, Bun, workers
          └─ Chicory   ← pure-Java SDK
              ├─ extism-runtime.wasm (portable kernel)
              └─ user module(s)
                  └─ guest code + language PDK
```

The [system concepts](../30-sources/dylibso-2026-extism-plugin-system.md)
separate the ordinary application—the **host**—from the Wasm module that
implements an extension—the **plug-in**. A **Host SDK** embeds and controls the
plug-in. A **PDK** supplies guest-language bindings, macros, serialization, and
build guidance.

This creates two language choices that are easy to conflate:

- the **host language** selects an SDK and, indirectly, an engine family; and
- the **guest language** selects a PDK/compiler and determines module size,
  runtime initialization, WASI imports, and required Wasm features.

A Python host and Rust host can both execute the same Rust-authored plug-in
through the reference runtime. A Go host can execute that artifact with Wazero
instead. A Java host can choose native `libextism`/Wasmtime or experimental
pure-Java Chicory. “Written in Java” therefore says nothing conclusive about
which Wasm engine runs the code.

## The portable plug-in contract

### Export shape

The [calling-convention proposal](../30-sources/extism-project-2026-plugin-calling-convention.md)
and current reference implementation converge on a simple export shape:

```text
plugin_export() -> i32
```

The runtime also accepts an export with no result. Application values are not
core-Wasm arguments. A zero `i32` normally signals success; a non-zero result,
an Extism error buffer, a Wasm trap, a WASI exit, cancellation, or an engine
error supplies different failure channels that each SDK translates into its
own host-language result or exception.

PDKs make this look richer. A Rust function such as
`fn greet(name: String) -> FnResult<String>` is transformed by a macro into the
no-argument export, input decoding, output encoding, and status/error
protocol. Go, C, Zig, AssemblyScript, .NET, Haskell, and JavaScript PDKs hide
different amounts of the same underlying work. The current
[PDK guide](../30-sources/dylibso-2026-extism-plugin-quickstart.md) documents
Rust, JavaScript/TypeScript, Go, C#, F#, C, Haskell, Zig, and AssemblyScript.

### Import namespaces

The [namespace proposal](../30-sources/extism-project-2026-host-function-namespaces.md)
assigns two defaults:

| Namespace | Provider | Purpose |
| --- | --- | --- |
| `extism:host/env` | Extism host/runtime | memory, input/output, errors, config, vars, HTTP, logging |
| `extism:host/user` | embedding application | application-defined capabilities such as database or model access |
| `wasi_snapshot_preview1` | optional WASI implementation | Preview 1 system interfaces required by some guest toolchains |

These are core-Wasm import module names. The colon-separated spelling is
friendly to the Component Model naming direction, but it does not turn the
imports into WIT interfaces. Extism payloads remain byte-oriented and their
schema remains an agreement between host and plug-in.

### The kernel

The key portability device is the
[runtime kernel](../30-sources/extism-project-2026-runtime-kernel.md), compiled
once as `extism-runtime.wasm`. The host instantiates it as the
`extism:host/env` module and links user modules against its exported functions.

The kernel owns a linear memory separate from the host and user module, with:

- a resettable allocator;
- metadata for input, output, and error offsets and lengths;
- allocation length lookup, load/store helpers, and explicit free;
- a zero offset used as null or allocation failure; and
- a reset operation that clears current allocations and call metadata.

The current allocator is a bump allocator that can reuse explicitly freed
blocks and grows in 64 KiB Wasm pages. It centralizes pointer bookkeeping that
would otherwise have to be implemented separately for Wasmtime, Wazero,
JavaScript, and Chicory.

It is intentionally not the entire runtime. Configuration lookup, variables,
HTTP, logs, custom functions, WASI, deadlines, cancellation, and engine limits
are implemented by each host adapter. Shared kernel bytes reduce memory-ABI
drift; they cannot eliminate semantic drift in those host services.

## Compile, load, instantiate, and call

### 1. Build the guest artifact

Guest source plus a PDK is compiled to a core Wasm module. The resulting
module:

- exports one or more Extism-shaped functions;
- imports the Extism functions its code or PDK uses;
- may import user host functions;
- may import WASI Preview 1 if the source-language runtime needs it; and
- may retain its own language-runtime state and linear memory.

WASI is not required by Extism itself. A small Rust, C, Zig, or AssemblyScript
plug-in can target a freestanding core module. The current JavaScript and Go
guest guides require WASI, and larger language runtimes may add initialization
exports such as `_initialize`, `_start`, constructors, or language-specific
hooks.

### 2. Resolve the manifest

The [manifest](../30-sources/dylibso-2026-extism-manifest.md) accepts:

- raw Wasm/WAT or inline module bytes;
- files, if that host build/runtime supports filesystem registration;
- URLs, if that host supports remote registration;
- optional module names and SHA-256 hashes; and
- multiple modules, with `main` or the last item selected as the entry module.

The runtime verifies a supplied digest after loading bytes. This protects
against unintended byte changes; it does not identify an author, validate a
signature, describe dependencies, or prove review status. URL headers in a
manifest can contain credentials, so manifest storage and logging are security
concerns in their own right.

### 3. Compile and link

The host compiles the shared kernel and supplied modules in its chosen engine.
It links:

1. kernel exports and the host implementations of Extism built-ins;
2. optional WASI imports;
3. application-provided host functions; and
4. named user modules and their inter-module dependencies.

Instantiation fails when required imports cannot be satisfied or signatures
do not match. A compiled plug-in or engine cache can amortize validation and
compilation across multiple instances. Each instance should still receive
separate mutable state unless the host intentionally shares external state.

### 4. Invoke an export

The logical call path, grounded in the
[memory model](../30-sources/dylibso-2026-extism-memory.md), is:

1. The Host SDK receives a function name, input bytes, and optionally a
   per-call host context.
2. Extism resets **kernel call memory** from the prior invocation and clears
   the prior output/error markers.
3. The host allocates a kernel block, copies input bytes into it, and calls the
   kernel's `input_set` with its handle and length.
4. The runtime starts its deadline/cancellation mechanism and calls the
   no-argument user export.
5. The PDK queries the input offset and length and decodes or copies the bytes
   into guest-language values.
6. Guest code computes and may invoke built-in or user host functions.
   Complex host-function values are normally 64-bit handles to kernel blocks.
7. The PDK encodes the result, allocates a kernel block, stores the bytes, and
   calls `output_set`; errors use the parallel error channel.
8. The export returns a status or traps. The runtime stops the deadline,
   inspects the status, error, and trap channels, and reads output metadata.
9. The Host SDK exposes or copies the output bytes and translates failures.
10. The output remains valid only for the documented plug-in-memory lifetime;
    the next call resets kernel allocations.

This path explains both the portability and cost model. It avoids agreement on
host object layouts, but introduces encoding/decoding, allocator calls, and at
least host-to-kernel and kernel-to-host copies. A guest runtime may copy again
between kernel and guest linear memory.

## Three different kinds of state

An Extism plug-in is not necessarily stateless. At least three lifetimes must
be distinguished:

| State | Typical lifetime | Reset behavior |
| --- | --- | --- |
| Kernel call blocks and input/output/error metadata | one call | reset before the next ordinary call |
| Extism variables | plug-in instance | host-side map; bounded by `max_var_bytes` where implemented |
| User-module globals, tables, and linear memory | Wasm instance | generally survive calls; replaced when the implementation reinstantiates |

Extism variables are mutable byte values addressed by string keys. They are
convenient instance-local state, not durable storage and not automatically
shared across instances. External persistence requires a host function backed
by a database, object store, or other host service.

The meaning of an explicit `reset` deserves testing. Ordinary calls reset
kernel allocations without erasing variables or all user-module memory. The
JavaScript README says variables persist until `plugin.reset()`, while current
source appears to preserve the variable map during reset. That inconsistency
is tracked in the open inquiry. Callers needing a clean security boundary
should create a fresh instance until the required reset semantics are proven
per runtime.

## Manifest, capabilities, and policy

The manifest is a useful deployment blueprint, but only part of a complete
capability policy.

| Field | What it governs | Important qualification |
| --- | --- | --- |
| `wasm` | module location, name, optional digest | URL/file loading is a host capability distinct from guest egress |
| `config` | host-supplied string values readable by the guest | can expose secrets; guest cannot change runtime policy through it |
| `allowed_hosts` | destinations for Extism's non-WASI HTTP import | empty denies; `null` permits all; does not govern arbitrary custom network functions |
| `allowed_paths` | host-to-guest filesystem preopens | only effective with WASI; path and read-only support differ by runtime |
| `timeout_ms` | call wall-clock deadline | interruption machinery and edge cases differ by engine |
| `max_pages` | Wasm/Extism memory ceiling | accounting scope and enforcement mechanism require parity tests |
| `max_http_response_bytes` | Extism HTTP response body | does not bound every custom or WASI network path |
| `max_var_bytes` | aggregate Extism-variable bytes | source already exposes parity gaps, including a Chicory FIXME |

The [configuration documentation](../30-sources/dylibso-2026-extism-manifest.md)
also exposes a build-time distinction in the reference runtime:

- `register-http` lets the **host loader** fetch module bytes;
- `register-filesystem` lets the **host loader** read module files; and
- `http` installs the **guest-callable** non-WASI HTTP function.

Treating these as one “network enabled” switch would obscure two different
attack surfaces.

### Custom host functions are the real application authority

[Host functions](../30-sources/dylibso-2026-extism-host-functions.md) can grant
precisely scoped operations, but Extism does not infer scope from a function
name. `read_record` could enforce tenant, key, and field constraints—or expose
an entire database. Agent WASM would still need to bind every call to an
artifact, principal, purpose, invocation, budget, and audit context.

Host functions also cross trust and concurrency boundaries. They must:

- validate every handle, length, encoding, and semantic field;
- treat guest-provided data as untrusted even after Wasm containment succeeds;
- limit output size and execution time;
- avoid holding stale kernel-memory views across calls;
- define reentrancy and cancellation behavior;
- keep opaque user data alive for the plug-in lifetime; and
- synchronize shared user data when pools or threads can call concurrently.

## Runtime families

### Reference Rust runtime: Wasmtime

The [reference runtime](../30-sources/extism-project-2026-reference-runtime.md)
is a Rust crate; release 1.21.0 embeds Wasmtime 41. It uses Wasmtime's linker, store,
Cranelift compilation, caching, pooling support, resource limiter, fuel, epoch
interruption, WASI Preview 1 support, and trap/error machinery.

Manifest timeouts and cancellation drive epoch interruption. Optional fuel
supports deterministic guest-instruction budgets, but host-function time still
needs host-side governance. The reference stack implements Extism HTTP,
variables, hashing, path preopens, compiled plug-ins, instance pools, coredumps,
and memory dumps around Wasmtime.

Rust applications can use this runtime directly. `libextism` exposes the same
implementation through the documented
[C API](../30-sources/dylibso-2026-extism-runtime-apis.md). Many official Host
SDKs—including the established Java route—are language bindings over that
native library. They are different API surfaces, not different Wasm engines.

Operational consequences include a native shared-library dependency, a
Wasmtime-sized distribution, target-specific releases, C-ABI object lifetimes,
and FFI error and callback translation. Conversely, this path concentrates
feature completeness and fixes in one implementation.

### Go runtime: Wazero

The [Go SDK](../30-sources/extism-project-2026-go-sdk.md) reimplements the host
stack on [Wazero](../30-sources/wazero-project-2026-runtime.md). It is pure Go
and does not need CGO or `libextism`. It embeds
the same kernel, constructs Extism and user host modules, supports WASI Preview
1, maps manifest page limits into Wazero configuration, and uses contexts for
timeout and cancellation.

Wazero normally selects its compiler on supported architectures and can be
configured to use its portable interpreter. Compilation caches let multiple
instances share compiled modules, while each instance keeps its own variables
and guest state. This is attractive for static Go deployments and broad Go
cross-compilation.

It is also the most valuable independent conformance target for a server-side
Agent WASM profile. Differences in WASI, cancellation by module closure,
engine proposals, memory ceilings, exit codes, and HTTP implementation should
be observed rather than assumed away.

### JavaScript runtime: the environment's engine

The [JavaScript SDK](../30-sources/extism-project-2026-js-sdk.md) uses the
standard `WebAssembly` API supplied by its environment instead of FFI. In
Chrome this ultimately means V8; Firefox uses SpiderMonkey; WebKit uses its own
engine; Node normally uses V8; Deno, Bun, Cloudflare Workers, and other hosts
add their own execution and capability policies.

The SDK supplies TypeScript/JavaScript orchestration, the Extism kernel,
manifest resolution, host functions, call context, variables, HTTP adapters,
and environment-specific WASI and worker polyfills. The same npm API therefore
runs over multiple independent browser/server engines.

The cost of that reach is visible variability:

- Deno's adapter currently reports no WASI support and Bun's is partial;
- timeouts require worker execution;
- allowed-host HTTP requires a worker unless JS Promise Integration is
  available;
- browser workers require cross-origin isolation, shared buffers, and atomics;
- read-only directory mappings are rejected by the current SDK path; and
- worker termination and async host functions do not have the same mechanics
  as Wasmtime epochs or Wazero context cancellation.

This family is indispensable for in-browser plug-ins but should have its own
conformance profile rather than inheriting server assumptions.

### Java routes: native reference runtime or Chicory

The established [Java SDK](../30-sources/extism-project-2026-java-sdk.md)
requires the native Extism shared library. Its Java classes and host callbacks
ultimately use the Rust/Wasmtime reference runtime.

The separate [Chicory SDK](../30-sources/extism-project-2026-chicory-sdk.md) is
a pure-Java implementation over the JVM-native Chicory runtime. It embeds the
kernel, links multiple modules and host functions, can install Chicory's WASI
Preview 1 implementation, and offers HTTP adapters and selectable machine
factories, including AOT-oriented code paths.

Chicory is appealing for Android, managed deployment, and environments where
native libraries are undesirable. The project currently labels itself
experimental, however, and its source exposes unfinished parity work such as
variable-limit enforcement. It should be treated as an exploratory portability
target rather than a production-equivalent Java replacement without evidence.

## Runtime comparison

| Host path | Wasm engine | Native dependency | Primary strengths | Material caveats |
| --- | --- | --- | --- | --- |
| Rust SDK | Wasmtime | Rust/native binary | fullest Extism feature set, fuel, epochs, pools | platform binaries and Wasmtime footprint |
| C and FFI-backed SDKs | Wasmtime through `libextism` | shared library | shared mature implementation across host languages | FFI packaging/lifetimes; not independent conformance |
| Go SDK | Wazero compiler or interpreter | none beyond Go binary | pure Go, cross-compilation, contexts, cache | independently reimplemented semantics and WASI |
| JS SDK | host JS engine | none beyond JS environment | browsers, Node, Deno, Bun, workers | environment-dependent WASI, workers, HTTP, limits |
| Java SDK | Wasmtime through `libextism` | shared library | established Java API and reference behavior | not JVM-native; native target constraints |
| Chicory SDK | Chicory | pure JVM | Android/JVM-native deployment, selectable machine | explicitly experimental and incomplete parity |

The official host-language list is therefore not the right unit for runtime
evaluation. The right unit is the engine adapter plus SDK version, engine
version/configuration, WASI implementation, host-service implementations, and
deployment environment.

## Extism, WASI, and the Component Model

Extism solves a narrower problem than the Component Model:

| Concern | Extism | Component Model/WIT |
| --- | --- | --- |
| Basic value boundary | byte buffer plus status | typed records, variants, results, resources, streams, futures |
| Interface description | application convention; PDK types/macros | WIT worlds and interfaces |
| Runtime target | core Wasm engines with Extism protocol | component-aware runtime or lowering/adapters |
| Host capabilities | Extism built-ins, WASI Preview 1, custom imports | imported typed interfaces, often WASI 0.2/0.3 |
| Maturity tradeoff | pragmatic stable protocol with multiple SDKs | richer evolving standards stack |

Extism can run without WASI and adds controlled HTTP, variables, logging, and
host calls through its own ABI. When enabled, its current stacks primarily
provide WASI Preview 1 for guest language runtimes and filesystem preopens.
That is distinct from the component-native WASI 0.3 direction described in the
[WASM foundations synthesis](webassembly-foundations-ecosystem-and-agent-runtime-implications.md).

The approaches are not automatically exclusive. An Agent WASM system could:

1. adopt Extism as its initial pragmatic core-module protocol;
2. define a strict payload schema and capability envelope above it;
3. expose Component Model adapters later; or
4. use Extism only as an implementation reference while standardizing directly
   on WIT.

The tradeoff is between Extism's broad present-day host/guest reach and the
Component Model's richer, standard typed interface. Building an elaborate
private schema, streaming, resource, and async layer over Extism may eventually
recreate the problem WIT and the Canonical ABI are designed to solve.

## Security interpretation for Agent WASM

Extism inherits core Wasm's validated isolation and makes least-authority
embedding convenient. It does not collapse the security layers identified in
the foundational research.

What it materially provides:

- a narrow import/export boundary;
- explicit application capability injection;
- optional absence of WASI;
- host allowlists and path mappings for built-in facilities;
- memory, HTTP response, variable, and wall-time controls;
- cancellation hooks;
- module digest verification when configured; and
- per-instance state with compilation/instance separation.

What Agent WASM still needs:

- artifact signing, provenance, dependency inventory, and revocation;
- principal- and purpose-bound authorization for every host function;
- schemas, size limits, and untrusted-output validation;
- quotas for aggregate CPU, host-function time, I/O, storage, and downstream
  effects;
- secret redaction and manifest/config handling;
- pool hygiene and cross-principal state tests;
- audit events with artifact, policy, runtime, and invocation identity;
- network controls beyond Extism HTTP, including custom functions and WASI;
- a defined outer process/VM boundary for threats outside Wasm's model; and
- differential conformance across at least two independent engine families.

In particular, `allowed_hosts` does not constrain a custom `fetch_anything`
host function, a digest is not a signature, a timeout does not necessarily
cancel work already delegated by a host function, and a valid Wasm result is
still untrusted data when it enters model context or a downstream tool.

## Provisional assessment

Extism is strongest as a **minimal portable plug-in substrate**, not a complete
agent sandbox or final typed agent interface. Its kernel and bytes ABI offer a
real interoperability advantage over inventing pointer conventions separately
for each engine. Its PDKs and Host SDKs also reduce the cost of proving an
initial end-to-end system in several languages.

For Agent WASM, the most informative next step is a constrained prototype on
the reference Wasmtime runtime and Go/Wazero, with JavaScript as a separate web
profile. The prototype should forbid WASI initially, expose only purpose-built
host functions, require hashed in-memory artifacts, enforce small payload and
state limits, and use fresh instances across principals. It should then test
the exact same adversarial corpus across runtimes.

Adoption should be rejected or narrowed if:

- identical artifacts cannot produce sufficiently equivalent success, error,
  timeout, cancellation, memory, and state behavior;
- required agent interfaces demand extensive private type, streaming, or async
  machinery better expressed in WIT;
- capability policy cannot be bound cleanly outside the manifest;
- cold/warm boundary costs miss the workload envelope; or
- a required deployment relies on an experimental or incomplete runtime path.

These are evaluation criteria, not findings. They remain tracked in
[Should Agent WASM Adopt Extism?](../40-inquiries/should-agent-wasm-adopt-extism.md).

## Sources

- [Extism plug-in system concepts](../30-sources/dylibso-2026-extism-plugin-system.md)
- [Extism memory and message passing](../30-sources/dylibso-2026-extism-memory.md)
- [Extism manifest and runtime constraints](../30-sources/dylibso-2026-extism-manifest.md)
- [Extism host functions](../30-sources/dylibso-2026-extism-host-functions.md)
- [Extism runtime C API](../30-sources/dylibso-2026-extism-runtime-apis.md)
- [Extism plug-in language and PDK guide](../30-sources/dylibso-2026-extism-plugin-quickstart.md)
- [Extism calling convention](../30-sources/extism-project-2026-plugin-calling-convention.md)
- [Extism host-function namespaces](../30-sources/extism-project-2026-host-function-namespaces.md)
- [Extism runtime kernel](../30-sources/extism-project-2026-runtime-kernel.md)
- [Extism reference runtime](../30-sources/extism-project-2026-reference-runtime.md)
- [Extism Go SDK](../30-sources/extism-project-2026-go-sdk.md)
- [Extism JavaScript SDK](../30-sources/extism-project-2026-js-sdk.md)
- [Extism Java SDK](../30-sources/extism-project-2026-java-sdk.md)
- [Extism Chicory SDK](../30-sources/extism-project-2026-chicory-sdk.md)
- [Wazero runtime](../30-sources/wazero-project-2026-runtime.md)
