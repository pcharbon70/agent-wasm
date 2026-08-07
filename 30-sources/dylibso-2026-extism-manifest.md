---
title: "Extism Manifest and Runtime Constraints"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismmanifest"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/manifest/"
accessed: "2026-08-07"
tags:
  - extism
  - security
  - webassembly
aliases: []
---

# Extism Manifest and Runtime Constraints

## Reference

Dylibso. *The Manifest*. [Extism documentation](https://extism.org/docs/concepts/manifest/),
accessed 7 August 2026. The exported
[JSON Schema](https://raw.githubusercontent.com/extism/extism/main/manifest/schema.json)
was inspected for fields omitted from the prose example.

## Contribution

The manifest declares module sources and identities, configuration, selected
resource limits, and host/network/filesystem constraints used to construct a
plug-in.

## Findings

Modules can come from inline data, a file path, or a URL. Each may carry a name
and optional SHA-256 digest; URL sources may also carry method and headers. A
multi-module manifest identifies the main module by the name `main` or by
placing it last.

Constraint fields include `timeout_ms`, `memory.max_pages`,
`memory.max_http_response_bytes`, `memory.max_var_bytes`, `allowed_hosts`, and
host-to-guest `allowed_paths`. Configuration is an arbitrary string map that
the guest can read. An empty host allowlist denies Extism HTTP while `null`
allows all hosts; filesystem mappings only take effect when WASI is enabled.

## Relevance

The manifest is the natural place to express a portion of an Agent WASM
invocation policy and bind expected module bytes.

## Limits

The manifest is neither a signature nor a provenance record. Its digest checks
integrity only when supplied. It does not model principals, purpose, secrets,
output schemas, per-host-function authority, aggregate I/O, storage lifetime,
or every engine resource. Enforcement also remains runtime-specific.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
