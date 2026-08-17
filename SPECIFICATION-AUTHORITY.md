# Agent WASM Specification Authority

This policy defines how to identify and interpret normative Agent WASM
specifications. It governs documents and conformance evidence; it does not
itself add technical requirements. The companion
[Conformance Vocabulary](CONFORMANCE-VOCABULARY.md) defines requirement words,
behavior classes, variability declarations, and implementation-profile
obligations.

## Authority classes

Only a document under [`60-specification/`](60-specification/README.md) with
both `kind: specification` and `status: normative` is a normative chapter. Its
declarative prose, tables, definitions, judgments, and explicit conformance
obligations bind conforming implementations, except where material is visibly
marked non-normative.

The following are not normative definitions:

- specification chapters whose status is `draft` or `candidate`;
- directory READMEs, maps, notes, source notes, inquiries, and journals;
- visibly marked rationale, proof sketches, evidence, connections, and
  illustrative examples;
- templates, guides, and repository documentation;
- executable references, implementations, tests, generated artifacts, and
  recorded conformance runs.

This document controls classification and conflicts. The conformance policy
controls wording and behavior classification. Both are repository governance.

## Status and applicability

Frontmatter is the status source of truth. Descriptive text cannot promote a
chapter. Promotion changes the chapter to `status: normative` together with
the evidence and indexes required by the repository workflow.

The status lifecycle is:

| Status | Meaning |
| --- | --- |
| `draft` | Active authoring that has not yet been accepted as a review baseline. |
| `candidate` | A reviewed research baseline ready for implementation and conformance work; it remains non-normative and unresolved defects still block conformance claims. |
| `normative` | A binding chapter promoted with its required evidence, cross-references, and conflict resolution complete. |

A chapter applies only within its stated scope and exclusions. A larger
`spec_version` does not automatically replace an older rule. Replacement,
deprecation, and removal require explicit normative text. Two applicable
chapters that disagree without such a relationship expose a specification
defect; the disputed behavior has no conforming interpretation until repaired.

## Normative and non-normative material

Normative chapter content is normative by default. A declarative rule binds
even without an uppercase requirement word.

Use visible rendered labels:

- End a non-normative section heading with `(non-normative)`.
- Introduce an exact grammar, judgment, schema, transition, or defining fenced
  block with `> **Normative definition.**`.
- Introduce a binding example with
  `> **Normative conformance example.**`.
- Introduce a binding conformance criterion with
  `> **Normative conformance criterion.**`.
- Introduce a binding integration-test scenario with
  `> **Normative test scenario.**`.
- Introduce a profiled choice with
  `> **Normative implementation-defined choice.**`.
- Introduce bounded presentation variation with
  `> **Normative unspecified presentation.**`.
- Introduce local explanatory material with one of
  `> **Non-normative example.**`, `> **Non-normative rationale.**`,
  `> **Non-normative note.**`, `> **Non-normative diagram.**`, or
  `> **Non-normative evidence.**`.

A fenced block must immediately follow an applicable label or appear inside a
non-normative section. Non-normative material may explain a rule but cannot
add, narrow, widen, or override one.

Labels are exact. A local non-normative label applies only to the immediately
following Markdown block. Any intervening label ends that pending scope; labels
cannot be stacked to carry a non-normative classification forward.

A bold blockquote beginning with “normative” or “non-normative”, matched
case-insensitively for detection, is an authority-style label and MUST exactly
match one of the labels above. Malformed, differently cased, or invented labels
are prohibited. An ordinary Markdown blockquote that does not have this form is
not a label and remains normative by default in a normative chapter.

## References and traceability

Conflict reports, tests, implementations, and evidence records should identify
the governing rule with a relative document link and heading anchor. A
chapter-only citation is insufficient when several headings could govern.

Stable rule identifiers may be introduced later, but document-and-heading
traceability remains required.

## Conflict resolution

The normative specification is the sole authority when artifacts disagree:

| Disagreement | Required action |
| --- | --- |
| Normative chapter versus implementation | Repair the non-conforming implementation and add regression evidence. |
| Normative chapter versus test | Repair the incorrect or stale test. |
| Normative chapter versus executable reference | Repair the reference; it has no fallback authority. |
| Implementation versus test or reference | Consult the cited normative heading. |
| Two applicable normative chapters | Block the conformance claim until normative text resolves the conflict. |
| Normative silence or ambiguity | Record a specification gap; observed behavior cannot silently fill it. |

While a conflict remains open, report the observed behavior and disagreement,
but do not claim conformance for the disputed rule.

## Repair and promotion workflow

1. Cite the exact normative heading, conflicting artifact, and observable
   disagreement.
2. Locate the defect in normative text or a non-normative artifact.
3. Repair artifacts to agree with unchanged normative text, or approve an
   explicit normative replacement.
4. Update conformance cases, reference paths, implementations, guides,
   indexes, and evidence together.
5. Run archive validation and affected implementation suites before restoring
   a conformance claim.

Passing tests are evidence against specified obligations; they do not promote
a candidate, settle ambiguity, or amend a normative chapter.
