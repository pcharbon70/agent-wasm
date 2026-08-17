---
id: agent_wasm.decision.specification_authority
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Specification Authority

## Context

The repository has 39 technical specification areas and two governance
specifications. Implementations need one rule for authority, conflicts, and
silence across that complete normative corpus.

## Decision

The implementation follows
[Specification Authority](../../../SPECIFICATION-AUTHORITY.md). Frontmatter is
the status source of truth, normative chapters are binding within scope, and
tests or implementation behavior never override them. Conflicting normative
rules and normative silence block conformance until the source text is
repaired.

<!-- covers: agent_wasm.package.source_authority -->

## Consequences

Every SpecLed subject links its governing source area. Implementation choices
must be explicitly permitted by the source and published in the conformance
profile. No ADR may silently settle a conflict between normative chapters.
