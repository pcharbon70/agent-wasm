# Agent WASM Research

This repository is a research and exploratory archive for Agent WASM. It is a
place for ideas to develop without losing provenance, relationships, open
questions, or the boundary between research evidence and normative decisions.

Start at the [home map](10-maps/home.md). Repository-wide authoring and
maintenance conventions are defined in [`AGENTS.md`](AGENTS.md).

## Research archive

Folders describe what a document is doing. Links, maps, and tags describe what
it is about. Each directory README is a complete local inventory; maps are
selective conceptual paths.

The [Specification Authority](SPECIFICATION-AUTHORITY.md) defines which
documents are normative and how conflicts are handled. The
[Conformance Vocabulary](CONFORMANCE-VOCABULARY.md) defines requirement force,
failure classes, variability, limits, and implementation-profile obligations.

## Structure

- [`00-inbox/`](00-inbox/README.md) — unprocessed captures
- [`10-maps/`](10-maps/README.md) — curated paths through subjects and questions
- [`20-notes/`](20-notes/README.md) — ideas and synthesis in the authors' words
- [`30-sources/`](30-sources/README.md) — reading notes and bibliographic records
- [`40-inquiries/`](40-inquiries/README.md) — active research workbenches
- [`50-journal/`](50-journal/README.md) — dated observations and experiments
- [`60-specification/`](60-specification/README.md) — versioned normative rules
- [`90-archive/`](90-archive/README.md) — inactive or superseded material
- [`assets/`](assets/README.md) — images, PDFs, datasets, and attachments
- [`templates/`](templates/README.md) — artifact and index starting points

## Frontmatter

Every completed knowledge document begins with YAML frontmatter. The
authoritative contract is [`frontmatter.schema.json`](frontmatter.schema.json).

```yaml
---
title: "A human-readable title"
kind: note
created: "2026-08-07"
maturity: seed
tags: []
aliases: []
---
```

Kinds and controlled lifecycle values are:

- `note`: `maturity: seed | developing | stable`
- `source`
- `inquiry`: `status: open | paused | resolved`
- `map`
- `journal`
- `specification`: `status: draft | candidate | normative` and exact
  `major.minor.patch` `spec_version`

Use lowercase kebab-case tags and YAML lists. Use `[]` for intentionally empty
lists and `null` for unknown nullable values. Git records update history, so do
not add an `updated` field.

## Working rhythm

1. Capture temporary material in `00-inbox/`.
2. Promote useful material with the closest template.
3. Give every durable document a meaningful body link or map entry.
4. Develop topic maps when clusters emerge.
5. Move dormant or superseded work to `90-archive/` without erasing context.
6. Update affected indexes and validate in the same change.

## Validation

Install dependencies once and validate the archive:

```bash
python3 -m pip install -r requirements-validation.txt
python3 validate_archive.py
python3 -m unittest test_validate_archive.py
git diff --check
```

The validator checks frontmatter, placeholders, filenames, local links,
directory inventories, conceptual connections, source identifiers,
specification authority, conformance vocabulary, visible content labels, and
specification-area consistency.

## Repository files

- [`AGENTS.md`](AGENTS.md) — authoring, organization, research, and handoff rules
- [`SPECIFICATION-AUTHORITY.md`](SPECIFICATION-AUTHORITY.md) — normative document authority and conflict policy
- [`CONFORMANCE-VOCABULARY.md`](CONFORMANCE-VOCABULARY.md) — requirement words and behavior classes
- [`frontmatter.schema.json`](frontmatter.schema.json) — metadata schema
- [`requirements-validation.txt`](requirements-validation.txt) — pinned validator dependencies
- [`validate_archive.py`](validate_archive.py) — deterministic archive checks
- [`test_validate_archive.py`](test_validate_archive.py) — focused validator tests
