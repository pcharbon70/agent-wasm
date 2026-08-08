---
title: "WebAssembly Testing, Verification, and Agent Runtime Assurance"
kind: note
created: "2026-08-07"
maturity: developing
tags:
  - agent-tools
  - extism
  - fuzzing
  - jido
  - runtime
  - testing
  - verification
  - webassembly
aliases:
  - "Wasm testing deep dive"
  - "Agent WASM assurance design"
---

# WebAssembly Testing, Verification, and Agent Runtime Assurance

## Executive conclusion

WebAssembly has a mature collection of testing techniques, but no single
“WebAssembly testing framework” proves that an agent runtime is correct. The
official Core suite tests the abstract machine. The WASI suite tests selected
host interfaces. WABT and Binaryen provide construction, interpretation,
fuzzing, and reduction tools. `wasm-smith`, `wasm-mutate`, and `wasm-shrink`
support structured exploration. Wasmtime demonstrates continuous fuzzing and
differential oracles. XTP exercises compiled Extism plug-ins and mock host
imports. Browser projects add `wasm-bindgen-test` and Web Platform Tests for a
different embedding profile.

Those tools are necessary but stop below the central risks in the proposed
Jido-like system. They do not establish that the host serializes turns,
validates state patches, commits state and an effect outbox atomically, resumes
after a crash, prevents tenant residue, reconciles topology, or produces the
same protocol behavior on independent Extism engines. That evidence requires a
host-level model and a layered assurance corpus built around the
[Jido/Extism architecture](jido-agent-architecture-and-wasm-extism-construction.md).

The recommended research direction is therefore an assurance stack, not a
single harness:

1. upstream Core and WASI conformance for each engine and pinned feature set;
2. compiler, PDK, ABI, schema, and plug-in contract tests for each guest build;
3. differential reducer tests across Extism/Wasmtime and Extism/Wazero;
4. state-machine and property tests for the host actor cell;
5. deterministic fault injection around commit, dispatch, acknowledgement, and
   recovery boundaries;
6. adversarial isolation and resource-governance tests;
7. record/replay, reduction, and permanent regression fixtures for failures;
8. a smaller formal model for the invariants that example tests cannot cover.

This document is a non-normative research and assurance design. It does not
specify conformance obligations and no executable harness was created in this
pass.

## Scope and method

The review asks:

- What is actually available for testing Wasm specifications, engines,
  compilers, guest libraries, host interfaces, browsers, and Extism plug-ins?
- What do fuzzing, differential testing, record/replay, reduction, empirical
  bug studies, and formal verification contribute?
- Which oracles are valid, and where can multiple implementations agree on the
  same error?
- How should those methods be arranged around a host-owned Jido-like agent
  runtime?

Sources prioritize official specifications and project documentation,
peer-reviewed primary research, and two first-party engineering/incident
articles. Tool and standards status was checked on 7 August 2026. No runtime,
compiler, plug-in, benchmark, or fault-injection experiment was run.

“Host” retains the meaning established by the earlier research: it is the
ordinary application that loads the Extism runtime, supplies capabilities,
owns authoritative agent state, schedules turns, validates results, commits
effects, and decides policy. Wasmtime or Wazero is an engine inside that host;
the guest plug-in is not the host.

## The assurance problem is layered

The easiest testing mistake is asking evidence from one layer to support a
claim at another. A useful decomposition is:

| Layer | Claim under test | Representative evidence | What it cannot establish |
| --- | --- | --- | --- |
| Specification | An engine implements the pinned Core semantics | Official `.wast` suite, SpecTec interpreter, negative validation cases | WASI, Extism, application state, security policy |
| Host interfaces | Selected WASI calls match a preview contract | WASI testsuite and runtime adapters | Least authority or correct application policy |
| Compiler/toolchain | Source becomes the intended Wasm program | Source-language tests, optimizer tests, artifact golden vectors | Engine correctness or host durability |
| Extism ABI | Bytes, memory handles, errors, variables, and imports behave as profiled | XTP, native Host SDK integration tests, malformed payloads | Mailbox ordering, database atomicity, crash recovery |
| Reducer protocol | A turn maps prior state and signal to a valid deterministic result | Golden vectors, schemas, properties, cross-runtime comparison | Correct execution of external effects |
| Host state machine | Revisions, commits, outbox, retries, and topology obey invariants | Model-based sequences and deterministic fault injection | Compiler or CPU backend correctness |
| Isolation/governance | One invocation cannot exceed or contaminate its authority and budget | Adversarial guests, tenant cross-products, limits, cancellation | Semantic quality of an agent decision |
| Operations | Supported builds remain reproducible and regressions stay closed | CI matrices, artifact provenance, replay corpus, telemetry | Proof of untested states |

Passing the official [Core test suite](../30-sources/webassembly-community-group-2026-core-testsuite.md)
is meaningful evidence only for the first row. The same discipline applies
upward: a crash-safe outbox test says nothing about a compiler backend's bounds
checks.

## Available frameworks and tools

### Standards conformance

The [Core suite](../30-sources/webassembly-community-group-2026-core-testsuite.md)
is the portable semantic baseline. Its S-expression scripts contain modules,
actions, and assertions for successful results, traps, malformed encodings,
invalid typing, unlinkable modules, and instantiation failures. A runtime can
consume the scripts directly or use
[WABT](../30-sources/webassembly-project-2026-wabt-testing-toolchain.md) to
translate them into JSON and binary fixtures.

The [WASI testsuite](../30-sources/webassembly-wasi-subgroup-2026-wasi-testsuite.md)
adds an adapter-driven layer for selected WASI previews. Its explicit
skip/expected-failure records are particularly important: lack of support
stays visible rather than being silently converted into success. Agent WASM
should only run the suites belonging to its declared guest profile. A reducer
with no WASI imports should not inherit a broad command-world test matrix or
the authority it implies.

The existing [SpecTec source note](../30-sources/youn-et-al-2024-spectec.md)
documents a complementary approach: generate specification prose and an
interpreter from a shared semantic language. The earlier
[mechanized specification](../30-sources/watt-2018-mechanising-and-verifying-webassembly.md)
also used differential fuzzing against a verified executable semantics. These
are stronger semantic anchors than implementation consensus, though each still
depends on model scope and correspondence with the released specification.

### Toolchain testing and diagnostics

[WABT](../30-sources/webassembly-project-2026-wabt-testing-toolchain.md) is the
workbench for text/binary conversion, validation, interpretation, disassembly,
and spec-script adaptation. It is especially useful after a failure has been
reduced: a reviewer can inspect the WAT, validate the binary under an explicit
feature set, and run the same spec assertion independently.

[Binaryen](../30-sources/webassembly-project-2026-binaryen-testing.md) targets a
different surface: Wasm construction and optimization. Its random module/pass
driver and `wasm-reduce` address defects introduced after source compilation.
The [compiler bug study](../30-sources/romano-et-al-2021-webassembly-compiler-bugs.md)
shows why this is a first-class tier. Two engines may faithfully execute the
same incorrectly compiled reducer and therefore agree on the wrong result.

The [wasm-tools trio](../30-sources/bytecode-alliance-2026-wasm-tools-testing-toolchain.md)
provides reusable primitives:

- `wasm-smith` deterministically generates valid, feature-configured modules;
- `wasm-mutate` diversifies real seeds and can request semantics-preserving
  transformations; and
- `wasm-shrink` minimizes any case for which an external predicate remains
  true.

The peer-reviewed
[Wasm-Mutate evaluation](../30-sources/cabrera-arteaga-et-al-2024-wasm-mutate.md)
supports diversification as a way to explore different engine paths while
retaining program-level behavior. For agent artifacts, “same semantics” needs
additional qualification: signatures, hashes, custom metadata, execution cost,
and import traces may change even when functional output does not.

### Runtime regression and fuzzing frameworks

[Wasmtime's documentation](../30-sources/bytecode-alliance-2026-wasmtime-testing-and-fuzzing.md)
provides the clearest production example. It combines the unmodified upstream
suite, engine-specific WAST regressions, WASI integration tests, structured
generators, reusable oracles, libFuzzer, OSS-Fuzz, and reduction. Differential
oracles compare execution modes or engines, but only after accounting for NaN
behavior, stack limits, memory-growth constraints, and host-specific APIs.

[Waltzz](../30-sources/zhang-et-al-2025-waltzz.md) demonstrates the value of
stack-invariant transformations that stay valid long enough to reach deep
engine paths. [LWDIFF](../30-sources/zhou-et-al-2025-lwdiff.md) and the accepted
[WASCII](../30-sources/fu-et-al-2026-wascii.md) explore LLM-assisted derivation
of spec-aware tests. Their defensible pattern is not “the model verifies the
runtime.” The model proposes structured cases; deterministic execution and
maintainer confirmation supply the evidence.

The empirical
[runtime-bug taxonomy](../30-sources/zhang-et-al-2023-webassembly-runtime-bugs.md)
is a reminder to direct some campaigns toward historically productive failure
classes. Pure coverage maximization can miss a narrow semantic boundary; pure
random generation can spend most of its budget rediscovering equivalent
failures.

### Extism plug-in testing

[XTP](../30-sources/dylibso-2026-extism-plugin-testing.md) occupies the correct
middle layer. It loads the compiled plug-in in a real WebAssembly runtime,
allows a Wasm test module to call exports and assert output/state/timing, and
can compose a Wasm mock host for imported functions. The harness language and
PDK language do not need to match.

That architecture is well suited to:

- positive and negative `reduce` vectors;
- bytes-in/bytes-out encoding and error-channel behavior;
- repeated calls that expose unintended persistent variables or memory;
- imported capability contracts with deterministic mock responses;
- per-PDK compatibility fixtures; and
- plugin-local performance smoke tests.

It is not a substitute for launching the native Agent WASM host. A Wasm mock
key-value function cannot prove transaction isolation in the real store; a mock
model call cannot prove idempotency after a successful external request and a
host crash; and plug-in state assertions cannot prove tenant erasure in a
native instance pool. Those belong to the host and system tiers.

### Browser-specific frameworks

For a browser host profile,
[`wasm-bindgen-test`](../30-sources/rustwasm-2026-wasm-bindgen-test.md) executes
compiled Rust/Wasm tests in Node.js or browsers, while
[Web Platform Tests](../30-sources/web-platform-tests-2026-webassembly-suite.md)
exercise shared WebAssembly Web API behavior across browser engines. They are
valuable evidence for browser embeddings but should not be mixed with the
native Extism profile. Different host APIs, process models, clocks, workers,
and capability boundaries make the two matrices related but non-equivalent.

## What the research literature adds

### Defect taxonomies are inputs to generators

The compiler and runtime bug studies analyze 1,316 and 311 issue records,
respectively, with smaller manually classified subsets. They establish that
Wasm failures distribute across source lowering, glue, optimization, decoding,
validation, execution, platform backends, APIs, and resource management. The
practical implication is not a timeless percentage for each category. It is a
seed taxonomy for directed tests and a warning to preserve the entire build and
execution chain with a failure.

### Differential testing needs a semantic contract

Differential testing is powerful because independent implementations rarely
fail identically by accident. It is not an oracle by majority vote. All engines
can share a misunderstanding, different feature profiles can reject different
inputs legitimately, and nondeterminism can look like disagreement.

For Core Wasm, a case can be adjudicated against the specification or a
verified/reference interpreter. For the proposed agent protocol, the corpus
needs an explicit equivalence relation. Two `TurnResult` values should be
considered equivalent only after:

- canonical decoding and schema validation;
- normalization of permitted presentation differences;
- comparison of state-patch meaning, directive order, identifiers, errors, and
  strategy continuation;
- exclusion or controlled injection of time, randomness, and external results;
  and
- confirmation that both runs started from identical artifact, state revision,
  signal, and policy inputs.

[WarpDiff](../30-sources/jiang-et-al-2023-warpdiff.md) extends the method to
performance outliers, but timing ratios are triage evidence rather than
semantic conformance. Agent WASM should record cold/warm state, compiler tier,
cache state, hardware, load, and input size before interpreting a ratio.

### Realistic inputs require replay and reduction

[Wasm-R3](../30-sources/baek-et-al-2024-wasm-r3.md) records host interactions
from real applications and emits reduced standalone replay modules. The idea is
directly transferable to agent turns: record explicit nondeterministic inputs
and imported results, then replay the guest portion across engines without
requiring the live model, database, or network.

[RR-Reduce](../30-sources/baek-et-al-2025-rr-reduce.md) shows that an execution
trace can make large Wasm failures dramatically easier to minimize. An Agent
WASM reducer should operate on two coupled objects:

1. the guest artifact; and
2. the smallest signal/state/effect/crash history that preserves the violated
   invariant.

Reduction is part of assurance, not mere convenience. Small fixtures are easier
to adjudicate, keep permanently, port across engines, and map back to a protocol
clause.

### Fuzzing, proofs, and implementation drift are complementary risks

[Fitzgerald's engineering account](../30-sources/fitzgerald-2022-security-and-correctness-in-wasmtime.md)
contrasts statistical fuzzing evidence with proofs over an explicit model. The
April 2026
[Wasmtime advisory review](../30-sources/wasmtime-project-2026-security-advisory-lessons.md)
makes the limits concrete: invalid Component Model strings lacked a fuzz
oracle, aarch64 lacked continuous compiler fuzzing, and a formal lowering model
had fallen behind production rules.

The lesson is broader than Wasmtime. Every assurance claim needs scope metadata:
which inputs, which target architecture, which feature set, which engine and
compiler revisions, which model commit, and which CI cadence. “Formally
verified” without model-to-code synchronization and “continuously fuzzed”
without target coverage are incomplete statements.

## Proposed assurance architecture for the Jido-like Extism runtime

The following architecture refines the earlier host-owned actor-cell proposal.
It is descriptive and intentionally non-normative.

### Tier 0: evidence manifest

Every result should bind:

- source revision, guest compiler, PDK, optimizer, and artifact digest;
- Extism SDK/kernel and underlying engine revision;
- target OS, architecture, and enabled Core/WASI features;
- host protocol/schema version and storage implementation;
- fixture seed or trace identity;
- policy, limits, clock/randomness mode, and instance lifecycle mode; and
- oracle version and disposition: pass, expected failure, skip, divergence,
  quarantined, or confirmed defect.

This prevents a green aggregate from hiding an untested runtime, architecture,
or feature. It also gives a replay enough context to be meaningful.

### Tier 1: upstream engine and interface gates

Run the official Core suite against each engine profile. Run only the selected
WASI suites for guests that import those interfaces. Retain upstream revision
and feature exclusions. Consume engine security advisories and upstream fuzzing
regressions rather than attempting to recreate full compiler assurance in the
application repository.

The initial independent pair remains:

- reference Extism over Wasmtime; and
- Extism Go over Wazero.

JavaScript or Chicory can become a third profile later, but adding engines
before the equivalence oracle is stable multiplies ambiguity rather than
confidence.

### Tier 2: artifact and Extism contract corpus

For every guest language/PDK pair, compile a small common set of reducers and
run the identical vectors through XTP and native Host SDK integration tests.
The corpus should cover:

- empty, minimum, typical, maximum, malformed, and unknown-field inputs;
- UTF-8 boundaries, embedded zero bytes, numeric limits, and oversized output;
- normal return, declared domain error, Extism error, Wasm trap, timeout, and
  cancellation;
- missing/wrong imports, denied WASI, and manifest resource constraints;
- repeated calls with variables and linear memory dirtied between calls; and
- mock host results that succeed, fail, delay, return malformed bytes, or
  exceed limits.

XTP establishes the portable plug-in contract. Native SDK tests establish that
the actual host binding exposes the same behavior and policies.

### Tier 3: reducer semantics and cross-runtime equivalence

The portable decision kernel is modeled as a pure transition over explicit
inputs:

`(manifest, prior state revision, signal, effect result, policy context) ->
(state patch, directives, strategy snapshot, facts, error)`.

Golden examples are necessary for protocol readability. Property-based
sequences provide wider coverage. Useful properties include:

- identical explicit inputs produce canonically equivalent results;
- a successful patch applied to the stated base revision yields the expected
  next state and cannot touch undeclared paths;
- a stale base revision never commits;
- rejected output leaves state and outbox unchanged;
- directive identifiers are stable under replay of the same committed turn;
- retrying an uncommitted turn cannot observe prior guest residue; and
- no guest-provided identity, route, or capability bypasses host policy.

Execute each vector on both Extism families. A divergence becomes an artifact
with both raw outputs, normalized outputs, engine configurations, and a reduced
reproducer. Do not automatically choose the majority result.

### Tier 4: host model and state-machine testing

The host actor cell contains the highest-value logic and should be modeled
independently of Wasm. Generate command sequences over:

- receive signal;
- load snapshot and expected revision;
- invoke reducer;
- validate or reject result;
- atomically commit state, facts, and outbox entries;
- lease and dispatch an effect;
- record external success or failure;
- acknowledge, retry, or return a result signal;
- hibernate, activate, and reconcile topology; and
- cancel or terminate an agent.

After every step, check invariants against a simple reference model. The key
invariants are:

- a committed state revision has exactly the committed journal facts and
  directive set for that turn;
- no directive is dispatched unless its originating state transition committed;
- every committed directive is either pending, leased, completed, or in a
  defined terminal failure state;
- retries reuse a stable idempotency key;
- a result signal is causally tied to one directive attempt/result policy;
- one agent's state, variables, memory, mailbox, or results never become input
  to another agent without an explicit route; and
- durable topology contains logical identities and dependencies, never live
  engine handles or process identifiers.

### Tier 5: deterministic fault injection

Fault injection should enumerate named boundaries rather than kill processes at
arbitrary times and hope for coverage. For each effectful turn, inject failure:

1. before reducer invocation;
2. during invocation and cancellation;
3. after result production but before validation;
4. after validation but before transaction start;
5. during or immediately after atomic state/outbox commit;
6. after leasing an outbox entry but before external dispatch;
7. after the external system succeeds but before local acknowledgement;
8. after acknowledgement but before the result signal is enqueued; and
9. during activation or topology reconciliation.

The oracle is not “exactly once,” which cannot generally be promised across an
uncoordinated external boundary. The defensible target is no lost committed
effects, no effect from an uncommitted turn, bounded retries, stable
idempotency, and explicit duplicate-risk classification.

### Tier 6: isolation, capabilities, and resource governance

Adversarial guests should attempt to:

- fill memory, grow output, loop, recurse, and produce decompression-like
  expansion at the protocol boundary;
- retain secrets in linear memory or Extism variables across calls;
- call absent, wrong-namespace, or over-broad imports;
- escape allowed filesystem roots or network-origin policies;
- exploit malformed host results and error strings;
- race cancellation with host callbacks and instance reuse; and
- recover data across the cross-product of tenant, agent, artifact, trap,
  timeout, reset, and pool mode.

Fresh instances are the reference behavior. Pooling is acceptable only when
its observable result matches fresh instances under this adversarial matrix.
Sharing compiled immutable code is not the same as sharing mutable instances.

### Tier 7: performance and operational confidence

Correctness gates precede performance comparisons. Measure cold compilation,
warm instantiation, call latency, serialization, schema validation, transaction
commit, and effect dispatch separately across representative state sizes. Use
ratio-based cross-runtime alerts as WarpDiff-style triage, not as conformance.

Long-running campaigns should include:

- structured guest fuzzing seeded by real reducer artifacts;
- protocol fuzzing seeded by real, redacted turn traces;
- optimizer and PDK upgrade comparisons;
- supported architecture jobs, not only the easiest CI architecture;
- replay of every confirmed historical defect; and
- periodic proof/model synchronization checks.

## Oracle design

An oracle decides whether a test found a problem. Tool selection is secondary
to choosing a defensible oracle.

| Oracle | Strong use | Main false-positive or false-negative risk |
| --- | --- | --- |
| Normative semantic oracle | Core validation and execution | Spec/model bug or profile mismatch |
| Golden vector | Stable protocol examples and regressions | Hand-authored expectation is wrong or narrow |
| Cross-runtime differential | Independent engine/Extism behavior | Legitimate variability or shared defect |
| Metamorphic relation | Equivalent transforms or input relations | Relation omits resource/trace effects |
| Reference state machine | Host sequences and recovery | Model repeats implementation assumptions |
| Invariant/property | Large generated state space | Important invariant was never stated |
| Crash/trap oracle | Memory safety and availability failures | Expected traps mistaken for defects |
| Performance ratio | Outlier triage | Noise, tiering, caching, hardware mismatch |
| Security policy oracle | Capability denials and provenance | Policy fixture differs from production identity/context |

Agent-level semantic quality—whether a model chose a useful plan—is a separate
evaluation problem. The runtime assurance suite should test deterministic
protocol and safety properties around model calls, not claim to prove the
quality of probabilistic model output.

## Corpus shape and traceability

The future executable corpus should distinguish:

- upstream vectors mirrored by immutable revision;
- project-owned positive and negative protocol vectors;
- generated seeds with deterministic generator configuration;
- redacted record/replay fixtures;
- minimized confirmed regressions; and
- known variability or expected failures with owner and expiry condition.

Each project-owned vector should trace to a protocol clause, threat, invariant,
or historical defect. Each clause should trace back to at least one positive
case and, when it constrains invalid behavior, one negative case. WASCII's Check
Tree is a useful research model for this relation, but the traceability graph
should remain inspectable without an LLM.

## Evidence, inference, and proposals

### Supported by current sources

- Core and WASI have reusable official test suites with different scopes.
- Production runtimes combine conformance tests, regressions, fuzzing,
  differential oracles, and reduction.
- Structured generation and stack-aware mutation have found confirmed runtime
  vulnerabilities.
- Compiler and runtime bugs occupy distinct surfaces.
- Record/replay can make realistic host-dependent Wasm workloads portable, and
  execution-aware reduction can substantially shrink failures.
- XTP executes compiled Extism plug-ins and supports Wasm mock hosts.
- Recent Wasmtime incidents exposed invalid-input, architecture-coverage, and
  formal-model-drift gaps despite a mature assurance program.

### Inference from the combined evidence

- Two independent Extism families are more informative than two Host SDK
  languages that both call the same native runtime.
- The highest-risk Agent WASM defects are likely to occur at composition seams:
  compiled guest to Extism ABI, normalized result to host commit, committed
  directive to external effect, and reused instance to another principal.
- A replayable explicit-effect protocol makes cross-runtime testing materially
  easier than synchronous effectful host calls because nondeterminism can be
  isolated as data.
- Fresh-instance behavior is the simplest isolation oracle against which
  pooling can be compared.

### Proposed, not yet demonstrated

- Canonical JSON is sufficient for the initial cross-language turn corpus.
- Extism/Wasmtime and Extism/Wazero can produce equivalent turn behavior under
  one pinned profile.
- A host reference model can cover the outbox and topology invariants without
  reproducing implementation defects.
- State transfer and validation costs remain acceptable at representative
  agent state sizes.
- A small formal model of revisions and effects can remain synchronized with
  the eventual implementation.

## Tradeoffs

- More engines increase independence but multiply feature negotiation,
  legitimate variability, CI cost, and triage load.
- Mock hosts improve determinism but can conceal native SDK, storage, network,
  and concurrency defects.
- Record/replay improves portability but explores recorded paths and creates
  secret-redaction obligations.
- Fresh instances simplify isolation but may cost latency; pooling improves
  throughput but expands the state-erasure proof burden.
- Golden fixtures are readable but narrow; fuzzing is broad but demands strong
  oracles and disciplined reduction.
- Formal models cover unbounded modeled states but can omit production behavior
  or drift; tests exercise real code but only selected executions.
- Strict canonical results simplify differential testing but can freeze
  presentation details that should remain variable.

## Falsification criteria

The provisional assurance design should be reconsidered if any of the
following persists after reduction and configuration alignment:

- independent Extism families cannot agree on the pinned ABI and turn corpus;
- a valid turn cannot be replayed without hidden ambient state or synchronous
  effect access;
- crash injection produces lost committed effects or effects from uncommitted
  turns;
- stable idempotency cannot bound duplicate external actions;
- pooled instances reveal prior tenant, agent, artifact, or failed-call state;
- resource limits or cancellation cannot stop adversarial guests within the
  stated bound;
- generated failures cannot be reduced to reproducible fixtures;
- the host model and implementation repeatedly diverge because the proposed
  state/effect boundary is incomplete; or
- protocol validation and state transfer exceed the workload budget even after
  measuring and optimizing the actual bottleneck.

## Open questions

- What exact Core, WASI, Extism, PDK, and JSON profiles define the first matrix?
- Which result differences are allowed presentation variability, and which are
  semantic divergence?
- Can XTP run unchanged across the two chosen Extism families, or does native
  SDK integration become the portable boundary?
- How should a replay redact secrets while preserving byte-accurate behavior?
- Which host invariants merit formalization first: revision monotonicity,
  state/outbox atomicity, or effect idempotency?
- What is the supported architecture matrix, and how is a skipped architecture
  made visible in release evidence?
- How much mutable instance reuse is worth the increased isolation burden?
- When Component Model interfaces mature, which Extism byte-contract tests can
  become interface-level component tests without weakening runtime diversity?

These questions are carried by
[How Should Agent WASM Assure a Jido-Like Extism Runtime?](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md).

## Connections

- [Jido Agent Architecture and a Wasm/Extism Construction](jido-agent-architecture-and-wasm-extism-construction.md)
  — supplies the actor cell, reducer/effect split, state, outbox, topology, and
  isolation claims this design proposes to test.
- [Extism Plugin-System Architecture and Runtimes](extism-plugin-system-architecture-and-runtimes.md)
  — defines the ABI, state, manifest, capabilities, and independent execution
  families under comparison.
- [WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
  — supplies the standards and runtime layers beneath this testing program.
- [Testing and verification map](../10-maps/webassembly-testing-and-verification.md)
  — provides a shorter route through tools, methods, and open assurance work.

## Sources

The source notes linked throughout preserve the evidence in this synthesis.
The central trail begins with the
[Core suite](../30-sources/webassembly-community-group-2026-core-testsuite.md),
[Wasmtime testing and fuzzing](../30-sources/bytecode-alliance-2026-wasmtime-testing-and-fuzzing.md),
[XTP](../30-sources/dylibso-2026-extism-plugin-testing.md), the
[runtime-bug study](../30-sources/zhang-et-al-2023-webassembly-runtime-bugs.md),
[Wasm-R3](../30-sources/baek-et-al-2024-wasm-r3.md), and the
[2026 Wasmtime lessons](../30-sources/wasmtime-project-2026-security-advisory-lessons.md).
