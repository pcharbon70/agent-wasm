---
title: "How Should Agent WASM Assure a Jido-Like Extism Runtime?"
kind: inquiry
created: "2026-08-07"
status: open
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
  - "Agent WASM assurance inquiry"
---

# How Should Agent WASM Assure a Jido-Like Extism Runtime?

## Why this matters

The proposed architecture puts deterministic decisions in portable Extism
reducers and keeps authoritative state, effects, policy, scheduling, durability,
and topology in the host. This creates a useful separation of authority, but it
also creates seams where independently correct pieces can compose incorrectly.

The [testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
shows that established WebAssembly suites mostly test below these seams. This
inquiry defines what evidence would be sufficient before the
[Jido-like construction](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
is treated as an implementation-ready architecture.

## Operational question

Can a versioned Agent WASM profile produce reproducible evidence that:

- the same artifact and explicit turn inputs produce canonically equivalent
  results on Extism/Wasmtime and Extism/Wazero;
- the host alone authorizes and commits validated state and effects;
- failures at every commit/dispatch/acknowledgement boundary cause neither lost
  committed effects nor effects from uncommitted turns;
- retries use stable identities and bound unavoidable duplication;
- no guest or host-runtime residue crosses agent or tenant boundaries;
- resource limits, deadlines, and cancellation remain effective for adversarial
  guests and host calls;
- topology restoration depends only on durable logical data; and
- every supported engine, compiler, PDK, architecture, and profile claim is
  tied to inspectable evidence rather than an aggregate green status?

A candidate answer needs a written profile, equivalence relation, threat and
fault model, evidence manifest, reference host state model, and traceability
from each invariant to positive, negative, fault, or generated cases. This
inquiry plans those artifacts; it does not create the executable suite.

## Working hypotheses

1. Core and selected WASI conformance can remain upstream gates; the project
   does not need to fork their semantic suites.
2. XTP can supply most compiled plug-in contract fixtures, but native SDK tests
   are required for real host functions, limits, cancellation, and pooling.
3. A canonical JSON bootstrap profile can make reducer results comparable
   across guest languages and independent Extism families.
4. An explicit directive/result protocol permits deterministic replay of model,
   network, storage, and timer interactions without granting ambient authority.
5. A small reference state machine can detect revision, outbox, retry, and
   recovery defects without duplicating the production implementation.
6. Fresh instances define the isolation reference; pooled/reset instances must
   be observationally equivalent across an adversarial tenant cross-product.
7. Stable directive and attempt identities can prevent lost work and bound
   duplicates, but cannot manufacture general exactly-once external effects.
8. Formalizing state/outbox atomicity and revision monotonicity will add value
   only if model-to-code correspondence is checked continuously.

## Paths to explore

### Freeze the first profile on paper

Record Core features, WASI imports, Extism ABI/kernel behavior, PDK/compiler
versions, JSON/schema rules, error categories, resource limits, instance
lifecycle, and supported architectures. Give every exclusion an explicit
reason and reconsideration condition.

### Define result equivalence

Specify canonical decoding, ordered and unordered collections, number and text
rules, identifier generation, timestamps, errors, directive order, unknown
fields, and allowed presentation variability. Construct examples where raw
bytes differ but semantics agree and where similar-looking results must fail.

### Build the traceability model

Map protocol clauses, threats, host invariants, historical defects, and
supported profiles to test-case classes. Keep upstream, hand-authored,
generated, replayed, and minimized-regression provenance distinct.

### Model the host actor cell

Describe a minimal transition system for receive, invoke, validate, commit,
lease, dispatch, acknowledge, retry, result ingress, hibernate, activate,
reconcile, cancel, and terminate. State the invariants without reference to a
particular database or programming language.

### Enumerate fault boundaries

Create a table for failure before/during/after reducer execution, result
validation, atomic commit, outbox lease, external success, acknowledgement,
result-signal enqueue, activation, and reconciliation. For each boundary,
record expected durable state and permitted duplicate behavior.

### Define the isolation cross-product

Cross tenant, agent, artifact, engine, PDK, fresh/reset/pooled lifecycle, clean
return, trap, timeout, cancellation, memory pressure, and variable use. Define
what observations would constitute residue or authority leakage.

### Design replay and reduction records

Identify nondeterministic inputs, import calls, directive results, scheduler
choices, and crash positions needed to replay a turn. Define secret redaction
that preserves required byte structure. Specify how module and event-history
reduction preserve the same violated invariant.

### Separate correctness and performance evidence

Define cold compile, warm instantiate, guest call, serialization, schema
validation, transaction, and effect-dispatch measures. Treat cross-runtime
ratios as triage. Establish workload budgets only after representative state
and strategy shapes exist.

### Decide formal scope

Compare a state/outbox transition model, a revision/optimistic-concurrency
model, and an idempotent-effect model. Select the smallest one whose property
cannot be convincingly covered by finite sequences alone, and define how its
assumptions remain linked to implementation revisions.

## Findings

### Evidence already available

- The official Core and WASI suites provide reusable but bounded conformance
  layers.
- WABT, Binaryen, and wasm-tools provide complementary construction,
  interpretation, mutation, fuzzing, and reduction capabilities.
- Production and research systems have found confirmed engine defects through
  structured generation, stack-preserving mutation, differential execution,
  and specification-assisted case generation.
- Compiler defects can survive correct execution on multiple runtimes, so a
  cross-runtime matrix does not replace post-compilation guest semantics tests.
- XTP exercises real compiled Extism plug-ins and Wasm mock hosts, but not the
  native application's transaction and lifecycle semantics.
- Record/replay and execution-aware reduction address realistic host-dependent
  workloads and oversized failure reports.
- The 2026 Wasmtime advisories demonstrate that invalid-input oracles,
  architecture coverage, and model synchronization can remain missing even in
  a mature project.

### Not yet established

- The exact portable subset shared by the two intended Extism families.
- A reviewed cross-language `TurnResult` equivalence relation.
- Whether XTP behaves consistently over both runtime families.
- A database-independent but implementation-relevant host reference model.
- Crash semantics and duplicate bounds for each directive family.
- Observable erasure guarantees for reset and pooled instances.
- A replay format that is both useful and safe for agent data.
- Performance budgets for representative state sizes and strategy shapes.
- The formal property with the best value-to-maintenance ratio.

## Outcome

Open. Current evidence supports a layered program and rejects “passes the Wasm
spec suite” as an adequate agent-runtime assurance claim. The next decision
artifact should freeze the initial profile and result-equivalence rules before
any executable test framework is selected or implemented.
