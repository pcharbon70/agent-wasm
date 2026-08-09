---
title: "Specification"
kind: map
created: "2026-08-07"
tags:
  - archive-navigation
  - directory-index
  - specification
aliases:
  - "Normative definition"
---

# Specification (`60-specification`)

## Purpose

This directory contains versioned candidate and normative rules. Research
notes preserve rationale and evidence; normative chapters determine
conformance within their explicit scope.

The repository-level [Specification Authority](../SPECIFICATION-AUTHORITY.md)
defines document status, visible content labels, references, and conflict
handling. The [Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md) defines
requirement force, behavior classes, variability, limits, and profiles.

## What belongs here

Put separately versioned specification areas and chapters here. A chapter
becomes normative only after its required evidence and cross-references are
present. Tests and implementations never override normative text by
themselves.

## Index

### Subdirectories

- None yet.

### Documents

- [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md) — Phase 1 of Milestone 1; establishes the language-neutral vocabulary, ownership assignments, host--guest interface, and bootstrap profile for the agent system.
- [Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md) — Phase 2 of Milestone 1; defines stable identity types, canonical representations, version fields, error categories, limits, and compatibility diagnostics.
- [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md) — Phase 3 of Milestone 1; defines immutable artifacts, reviewable manifests, schema identifiers, registry lookup, validation order, and cache keys.
- [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md) — Phase 4 of Milestone 1; specifies the complete bytes-in/bytes-out lifecycle for describe, initialize, reduce, and migrate exports, plus canonical JSON encoding rules.
- [Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md) — Phase 5 of Milestone 1; turns the protocol into language-neutral fixtures and guest SDK responsibilities without choosing initial SDK languages.
- [Signal Envelopes Causality Routing And Delivery Vocabulary](10-signals-causality-routing-and-delivery.md) — Phase 1 of Milestone 2; defines the event fabric through which users, effects, timers, sensors, and agents enter deterministic turns.
- [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md) — Phase 2 of Milestone 2; separates reusable operation definitions from concrete invocations and deterministic execution plans.
- [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md) — Phase 3 of Milestone 2; defines safe internal state transitions against host-owned snapshots and optimistic revisions.
- [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md) — Phase 4 of Milestone 2; defines external requests and replaceable decision policies without hiding mutable runtime authority in the guest.
- [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md) — Phase 5 of Milestone 2; assembles signals, actions, state operations, directives, and strategies into one replayable decision kernel.
- [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md) — Phase 1 of Milestone 3; establishes the host boundary that resolves artifacts, creates constrained instances, invokes exports, and treats all guest output as untrusted until validated.
- [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md) — Phase 2 of Milestone 3; provides one-at-a-time committed turns per agent while bounding queued work and making overload behavior explicit.
- [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md) — Phase 3 of Milestone 3; manages logical agent identity and disposable live actors without persisting engine or process handles.
- [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md) — Phase 4 of Milestone 3; converts external events and time into validated signals without granting event sources direct access to agent state.
- [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md) — Phase 5 of Milestone 3; connects admission, mailbox, activation, Extism invocation, validation, lifecycle, and observable results in one single-node runtime.
- [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md) — Phase 1 of Milestone 4; defines durable records and transactional storage boundaries for authoritative state, history, and replay.
- [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md) — Phase 2 of Milestone 4; closes the crash gap between accepting a state transition and making its external requests durable.

## Maintaining this index

Keep lifecycle and versions explicit. Update research maps, inquiries,
evidence, and every affected index with a rule change. Every future
specification area must link both governance policies and maintain a
`## Variability register`.
