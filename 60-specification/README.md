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

## Maintaining this index

Keep lifecycle and versions explicit. Update research maps, inquiries,
evidence, and every affected index with a rule change. Every future
specification area must link both governance policies and maintain a
`## Variability register`.
