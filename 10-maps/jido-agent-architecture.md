---
title: "Jido Agent Architecture"
kind: map
created: "2026-08-07"
tags:
  - agent-tools
  - extism
  - jido
  - runtime
  - webassembly
aliases:
  - "Jido to Wasm map"
---

# Jido Agent Architecture

## Scope

This map treats Jido as a language-independent agent architecture: immutable
decision state, structured operations, event routing, effect interpretation,
live actor lifecycle, capability composition, durable topology, persistence,
and optional AI. It then connects those responsibilities to a Wasm/Extism
host–guest design.

## Start here

- [Jido Agent Architecture and a Wasm/Extism Construction](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
  — the integrated architectural model, direct component mapping, proposed turn
  protocol, host flow, security boundary, durability model, and staged build.
- [How Should Agent WASM Construct a Jido-Like Framework?](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
  — converts the proposal into conformance, isolation, crash, performance,
  composition, topology, and WIT-comparison experiments.

## Trails

### Decision kernel

- [Overview and core loop](../30-sources/agentjido-2026-jido-overview-and-core-loop.md)
  — immutable agent plus runtime-owned effects.
- [Actions and execution](../30-sources/agentjido-2026-jido-actions.md) — separates
  operation metadata, normalized invocation, execution policy, and DAG plans.
- [Directives and state operations](../30-sources/agentjido-2026-jido-directives-and-state-operations.md)
  — the internal-patch versus external-effect algebra.
- [Plugins and strategies](../30-sources/agentjido-2026-jido-plugins-and-strategies.md)
  — capability bundles and replaceable transition policies.

### Messaging and live runtime

- [Signals and routing](../30-sources/agentjido-2026-jido-signals-and-routing.md)
  — CloudEvents-derived envelope, causal metadata, precedence, dispatch, and
  reliability features.
- [Runtime and coordination](../30-sources/agentjido-2026-jido-runtime-and-coordination.md)
  — serialized actor turns, logical hierarchy, completion, cancellation, and
  fan-out/fan-in.
- [Sensors and scheduling](../30-sources/agentjido-2026-jido-sensors-and-scheduling.md)
  — external event and clock adapters that re-enter normal signal routing.

### Durability, topology, and isolation

- [Runtime patterns and Pods](../30-sources/agentjido-2026-jido-runtime-patterns-and-pods.md)
  — live versus durable lifecycle and topology reconciliation.
- [Persistence and storage](../30-sources/agentjido-2026-jido-persistence-and-storage.md)
  — append-only history, versioned projection, hibernate, and thaw.
- [Multi-tenancy and worker pools](../30-sources/agentjido-2026-jido-multi-tenancy-and-worker-pools.md)
  — logical versus hard isolation and mutable reuse hazards.

### Optional AI and implementation evidence

- [Jido AI runtime](../30-sources/agentjido-2026-jido-ai-runtime.md) — model
  routing and reasoning are a layer above the core agent contract.
- [Jido 2.3.2 source architecture](../30-sources/agentjido-2026-jido-2-3-2-source-architecture.md)
  — confirms the documented seams as behaviors, protocols, normalized specs,
  and storage APIs.

### Wasm and Extism context

- [Extism Plugin-System Architecture and Runtimes](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
  — the bytes ABI, host functions, state, manifests, engines, and limitations
  beneath the proposed guest boundary.
- [WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
  — standards, runtimes, research evidence, and the layered security model.

## Primary evidence

The Jido source notes above cover official v2.3.2 guides, the current companion
Action, Signal, and AI packages, and the tagged Jido source tree. They support
claims about Jido. The proposed outbox, Extism protocol, host/guest allocation,
trust tiers, and build stages are new analysis in the synthesis and remain
subject to the inquiry.

## Open questions

- Can a versioned byte protocol remain equivalent across independent Extism
  runtime families?
- Which action effects must remain synchronous, if any?
- Can full state stay outside guest memory at realistic sizes and latency?
- How should framework capability manifests compose multiple Wasm artifacts?
- What are the precise crash and delivery contracts for state plus effects?
- When do WIT types and component-native async outweigh Extism's simpler and
  broader bootstrap toolchains?

These remain tracked in the
[construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md).
