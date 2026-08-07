# Repository instructions

These instructions apply to the entire repository. This is a Markdown research
archive, not a conventional software project. Preserve room for exploratory
thought while keeping provenance, navigation, and document structure reliable.

Follow an explicit user request when it conflicts with this file. Otherwise,
use these conventions for every document and organizational change.

## Archive principles

- Folders describe what a document is doing; maps, links, and tags describe
  what it is about.
- Prefer a small stable top-level structure over speculative subject folders.
- Separate source claims, local synthesis, experimental evidence, normative
  decisions, and unresolved questions.
- Directory READMEs are complete local inventories; maps are selective
  conceptual paths.
- Treat `frontmatter.schema.json` as the authoritative metadata contract.
- Keep related changes atomic: update documents, indexes, links, and maps
  together.

## Canonical structure

```text
00-inbox/         Unprocessed temporary captures
10-maps/          Curated paths through subjects and questions
20-notes/         Ideas and syntheses in the authors' own words
30-sources/       Reading notes and bibliographic records
40-inquiries/     Active questions and research workbenches
50-journal/       Dated observations and research-session evidence
60-specification/ Versioned normative rules and conformance obligations
90-archive/       Inactive or superseded material worth retaining
assets/           Images, PDFs, diagrams, datasets, and attachments
templates/        Starting points for documents and directory indexes
```

Do not add or rename a top-level directory unless the user asks or repeated
work demonstrates that this structure is inadequate. Use tags, links, and
maps to organize subjects first.

## Sources of truth

Use these files for different decisions:

1. `SPECIFICATION-AUTHORITY.md` defines normative authority and conflicts.
2. `CONFORMANCE-VOCABULARY.md` defines requirements and behavior classes.
3. `frontmatter.schema.json` defines valid metadata.
4. `templates/` defines minimum artifact structure.
5. The root `README.md` explains the archive to human readers.
6. Directory READMEs describe and inventory their directories.
7. `10-maps/` provides curated thematic navigation.
8. `validate_archive.py` performs deterministic checks.

If documentation and the filesystem disagree, determine the intended change
and bring them back into sync. Never preserve a stale index merely because it
was previously committed.

## Directory README invariant

Every archive directory, including nested directories, has a `README.md` made
from `templates/directory-readme.md`.

Directory READMEs must:

- use valid frontmatter with `kind: map` (the root README is exempt);
- have a human-readable title and matching H1;
- include `## Purpose`, `## What belongs here`, `## Index`, and
  `## Maintaining this index`;
- list `### Subdirectories` followed by `### Documents`, `### Files`, or
  `### Templates`;
- inventory every direct child except the README itself;
- link relatively and explain each entry's role;
- state an explicit empty condition such as `None yet`;
- link a nested directory through its README.

Whenever content moves or changes, update its old and new indexes, affected
maps, and meaningful body links. Do not index Git data, caches, or editor state.

## Frontmatter contract

Every durable knowledge document and directory README begins with YAML
frontmatter validated by `frontmatter.schema.json`.

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

Additional requirements depend on `kind`:

- `note` requires `maturity: seed | developing | stable`;
- `inquiry` requires `status: open | paused | resolved`;
- `source` may use bibliographic fields defined by the schema;
- `specification` requires `status: draft | candidate | normative` and an
  exact `major.minor.patch` `spec_version`;
- `map` and `journal` use common fields.

Conventions:

- Quote dates in `YYYY-MM-DD` form and use the document's creation date.
- Use lowercase kebab-case tags and YAML lists for tags and aliases.
- Reuse established tags instead of introducing synonyms.
- Use `[]` for an empty list and `null` for an unknown nullable value.
- Put searchable facts in frontmatter and analysis in the body.
- Match the first H1 to the frontmatter title.
- Do not add an `updated` date; Git records revision history.

Exceptions are the root README, governance files, tooling, requirements, and
unfilled templates. A transient inbox capture may be incomplete but needs
valid frontmatter before promotion. Binary assets are documented in an index.

## Document roles and templates

| Artifact | Destination | Template | Result |
| --- | --- | --- | --- |
| Directory index | Any archive directory | `templates/directory-readme.md` | Exhaustive local inventory |
| Conceptual map | `10-maps/` | `templates/map.md` | Selective explained route |
| Note | `20-notes/` | `templates/note.md` | Idea, argument, model, or synthesis |
| Source note | `30-sources/` | `templates/source.md` | Bibliographic and evidence record |
| Inquiry | `40-inquiries/` | `templates/inquiry.md` | Live question and findings |
| Journal entry | `50-journal/` | `templates/journal.md` | Dated reproducible evidence |
| Specification chapter | `60-specification/` | `templates/specification.md` | Versioned normative rule set |

Copy the closest template, replace every placeholder, and adapt headings only
as the material requires. Do not change a template to customize one document.

When a metadata field or kind changes, update the schema first, then templates,
completed documents, guides, validator, and tests before validating everything.

## Filenames and paths

- Use lowercase kebab-case Markdown filenames.
- Name notes and maps for subjects, not dates.
- Name inquiries as concise questions.
- Name journals `YYYY-MM-DD.md`, optionally with a kebab-case suffix.
- Prefer `<author>-<year>-<short-title>.md` for sources and add `et-al` for
  multi-author works.
- Use stable descriptive asset names and relative local links.
- Find and update every incoming link before renaming or moving a file.
- Use aliases for useful former titles, not as a substitute for link repair.

## Producing ordinary documents

Before creating a document:

1. Read the root README, this file, the destination README, relevant template,
   and schema.
2. Search for an existing document that already serves the need.
3. Choose the role based on what the document does rather than its topic.
4. Use the current local date and purposeful existing tags.
5. Add a meaningful body connection or map entry.
6. Update the destination README in the same change.

Prefer clear claims, explicit uncertainty, and explanations of why links
matter. Develop boilerplate sections, remove them, or state what remains
unknown.

## Research and deep dives

Unless the user requests a different artifact shape, a deep dive creates or
updates this connected bundle:

1. one synthesis note;
2. one source note for each substantively used primary work;
3. an inquiry when the central question remains open;
4. a topic map explaining the route through the work;
5. the home map when the topic belongs at the entry point;
6. journal evidence for material local experiments;
7. every affected directory README.

Research method:

- Define the question, scope, terms, and operational standards.
- Search current sources when facts, software, standards, or product behavior
  may have changed.
- Prefer primary papers, official specifications, and project documentation.
- Record exact authorship, title, year, venue, DOI or canonical URL, and access
  date when available; never invent metadata.
- Read enough to support the cited claim; snippets are not detailed evidence.
- Distinguish reported results from inference and proposal.
- Compare approaches and include limits, negative evidence, and uncertainty.
- Paraphrase by default and keep citations near supported claims.
- Record commands, versions, output, and artifacts for local experiments.

Source notes normally include reference, contribution, method, findings,
relevance, limits, and derived work. Synthesis notes should separate evidence,
inference, proposals, tradeoffs, falsification criteria, and open questions.

## Maps, inquiries, and lifecycle

- Maps explain relationships; they are not file dumps.
- Keep the home map selective.
- Inquiries define why a question matters, what evidence can answer it,
  hypotheses, paths, findings, and outcome.
- Promote independently useful conclusions from inquiries or journals.
- Archive dormant or superseded work rather than silently deleting context.
- Do not mark work stable or resolved merely because a writing pass finished.

## Normative specifications

- Follow `SPECIFICATION-AUTHORITY.md` for authority, content labels, citations,
  and conflict resolution.
- Follow `CONFORMANCE-VOCABULARY.md` for the five canonical keywords,
  behavior classes, variability, limits, traps, and profiles.
- Only a `kind: specification`, `status: normative` chapter is normative.
- In normative chapters, rules bind by default; visibly mark rationale,
  evidence, diagrams, and illustrative examples non-normative.
- Classify every fenced block unless it is inside a non-normative section.
- Keep each area's `## Variability register` synchronized with every
  permission, recommendation, permitted presentation, and limit.
- Cite rules by relative document link and heading anchor.
- A compiler, executable reference, test, or guide never supplies behavior
  that normative text leaves silent or ambiguous.

## Assets

- Store an asset only when a durable lawful copy adds value.
- Record provenance, creator, source URL, license, and consumer when available.
- Give any asset subdirectory its own README.
- Never leave an unreferenced asset without an index description.

## Verification and handoff

Before reporting archive work complete:

1. inspect `git status` and preserve unrelated changes;
2. run `python3 validate_archive.py`;
3. run `python3 -m unittest test_validate_archive.py` when tooling changed;
4. verify new external citations against primary sources;
5. run `git diff --check`;
6. review the complete diff for stale paths and unrelated changes.

Do not commit, push, open a pull request, or publish unless the user asks. In
the handoff, summarize artifacts, maps and indexes, validation, and whether the
changes remain uncommitted.
