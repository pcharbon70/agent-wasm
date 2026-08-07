---
title: "Jido 2.3.2 Source Architecture"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026sourcearchitecture"
container: "agentjido/jido"
edition: "2.3.2"
isbn: null
doi: null
url: "https://github.com/agentjido/jido/tree/v2.3.2"
accessed: "2026-08-07"
tags:
  - jido
  - plugin-system
  - runtime
aliases: []
---

# Jido 2.3.2 Source Architecture

## Reference

AgentJido. *jido*, tag `v2.3.2`. [GitHub source tree](https://github.com/agentjido/jido/tree/v2.3.2), accessed 7 August 2026.

## Method

The tagged repository was cloned at commit `eff8f5d23544024b2190ab7cb2c906e540d82077`; package dependencies, module layout, behavior callbacks, normalized plugin specification, directive protocol, and storage behavior were inspected locally.

## Findings

The package depends on `jido_action ~> 2.3` and `jido_signal ~> 2.2`. Its source modules separately implement agent value semantics, AgentServer lifecycle, strategies, plugin manifests, directives and executors, sensors, scheduler, storage, thread, instance management, worker pools, Pods, memory, identity, and observability.

`Jido.Agent.Strategy` is a behavior with command, initialization, tick, snapshot, and routing hooks. `Jido.AgentServer.DirectiveExec` is a protocol for effect handlers. `Jido.Plugin.Spec` normalizes actions, namespaced state, configuration, patterns, and routes. `Jido.Storage` exposes separate checkpoint and thread operations.

## Relevance

The source confirms that the higher-level decomposition is reflected in enforceable interfaces. A Wasm reconstruction can preserve those seams even though its runtime substrate is not OTP.

## Limits

This was source inspection, not an execution or fault-injection experiment. The checkout was temporary and produced no durable local artifact that warrants a journal entry.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Jido architecture map](../10-maps/jido-agent-architecture.md)
