---
title: "Jido Actions and Execution"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026actions"
container: "Jido and Jido Action Documentation"
edition: "Jido 2.3.2; Jido Action 2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/actions.html"
accessed: "2026-08-07"
tags:
  - agent-tools
  - jido
aliases: []
---

# Jido Actions and Execution

## Reference

AgentJido. *Actions*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/actions.html), with the [Jido Action package overview](https://jido-action.hexdocs.pm/readme.html), accessed 7 August 2026.

## Contribution

The guides define actions as named, described, schema-validated units of work and distinguish action definition, instruction normalization, execution policy, and DAG planning.

## Findings

An action receives validated parameters and context, then returns state updates, optional state operations, and optional directives. Root updates are deep-merged by default; explicit operations support replacement and path-level deletion or assignment.

The companion package separates `Action` metadata and validation from `Instruction` normalization, `Exec` retries/timeouts/cancellation, and `Plan` dependency graphs. Action metadata can be projected into LLM tool schemas.

Jido permits immediate I/O in an action when the result is needed to continue the same decision. Effects whose delivery belongs to the runtime should instead be returned as directives.

## Relevance

A Wasm design needs separate contracts for capability metadata, invocation, execution policy, and orchestration. Treating all four as a single “tool call” would erase useful control points.

## Limits

The documented action return shapes use language-native data. A portable encoding must specify schemas, numeric and error behavior, cancellation, deadlines, and state-patch conflicts independently.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
