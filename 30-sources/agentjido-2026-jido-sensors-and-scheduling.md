---
title: "Jido Sensors and Scheduling"
kind: source
created: "2026-08-07"
authors:
  - "AgentJido"
published: "2026"
citation_key: "agentjido2026sensorsscheduling"
container: "Jido v2.3.2 Documentation"
edition: "2.3.2"
isbn: null
doi: null
url: "https://jido.hexdocs.pm/sensors.html"
accessed: "2026-08-07"
tags:
  - jido
  - runtime
aliases: []
---

# Jido Sensors and Scheduling

## Reference

AgentJido. *Sensors* and *Scheduling*. [Jido v2.3.2 documentation](https://jido.hexdocs.pm/sensors.html), including the [scheduling guide](https://jido.hexdocs.pm/scheduling.html), accessed 7 August 2026.

## Contribution

The guides define how external event sources and clocks enter the signal model without becoming part of agent decision state.

## Findings

A sensor module transforms events into signals while a sensor runtime owns connections, subscriptions, timers, monitoring, and cleanup. Agent-owned sensors are tagged, monitored, and stopped with their owner. Sensors do not provide built-in backpressure.

Jido has declarative recurring schedules, one-time delayed messages, and dynamic cron directives. All ultimately re-enter normal signal routing. One-time timers are in-memory; selected dynamic cron registrations can survive hibernate/thaw, but missed ticks are not replayed.

## Relevance

Long-lived sockets, webhooks, clocks, and broker consumers belong in the host. Optional Wasm transforms can normalize payloads, but cannot safely own durable external subscriptions through ephemeral linear memory.

## Limits

The timer model is intentionally not exactly-once. A Wasm agent runtime must specify backpressure, clock behavior, missed-run policy, and durable timer delivery rather than inheriting them accidentally.

## Derived work

- [Jido architecture synthesis](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Construction inquiry](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
