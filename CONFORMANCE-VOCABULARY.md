# Agent WASM Conformance Vocabulary

This policy defines how normative Agent WASM chapters express requirements,
classify failure and permitted variation, and support conformance claims. It is
repository governance rather than a technical revision.

Read it with [Specification Authority](SPECIFICATION-AUTHORITY.md), which says
which material is normative and how conflicts are resolved.

## Canonical requirement words

Normative text has exactly five uppercase requirement words:

| Word | Meaning |
| --- | --- |
| `MUST` | Absolute conformance requirement. |
| `MUST NOT` | Absolute prohibition. |
| `SHOULD` | Recommended quality or technique; deviation needs a published justification. |
| `SHOULD NOT` | Discouraged quality or technique; use needs a published justification. |
| `MAY` | Permitted form, option, metadata, or technique. |

Only uppercase forms carry these meanings. Uppercase aliases such as `SHALL`,
`REQUIRED`, `RECOMMENDED`, and `OPTIONAL` are prohibited. Plain declarative
rules remain binding.

`SHOULD` and `SHOULD NOT` cannot make safety, acceptance, runtime values,
evaluation order, effects, artifact meaning, or other observable semantics
optional. `MAY` does not by itself create implementation-defined behavior.

## Behavior classes

| Class | Meaning |
| --- | --- |
| **Required** | Specified behavior is mandatory. |
| **Invalid** | The affected input or action fails without publishing successful output. |
| **Implementation-defined** | The specification bounds observable choices and each implementation publishes its selection. |
| **Unspecified presentation** | Bounded presentation or internal strategy may vary without changing semantics or stable identity. |
| **Implementation limit** | Otherwise valid input is refused with a distinct limit diagnostic. |
| **Explicit runtime failure or trap** | A named runtime condition has specified abrupt behavior. |

### Invalid input and actions

Malformed input cannot be decoded or violates required structure. Ill-formed
input decodes but violates a formation, scope, typing, policy, or other static
rule. Both are invalid. Failure must not publish new or partially replaced
final output.

### Implementation-defined choices

An implementation-defined choice is permitted only where a normative chapter:

1. uses the visible implementation-defined callout;
2. enumerates the complete set or bounded domain of choices;
3. states which observations may differ; and
4. requires the selected choice in the conformance profile.

The governed paragraph or table positively identifies the choice as
implementation-defined, or states that the host or implementation defines the
choice, and states how the conformance profile records or publishes the
selection. A negated mention of “implementation-defined” and a fixed rule are
not declarations.

The governed block enumerates at least two alternatives with `either ... or`,
`one of`, `whether`, a parenthesized alternative list, multiple table rows, or
an explicitly bounded or finite set, range, or domain. Naming an algorithm,
format, mechanism, policy, or other single value does not establish a choice.
The block also uses `observations that may differ` or states that an
`observable` result `may` or `can` `differ`, `vary`, or `change`, followed by
the affected observations. These explicit forms keep declaration checks
deterministic.

A statement that the selection must not be recorded, documented, published,
selected, specified, declared, included, or contained in the conformance
profile is invalid whether the negation precedes or follows “conformance
profile”. It cannot satisfy the profile obligation.

Specification silence and existing implementation behavior create no choice.

### Unspecified presentation

The governing paragraph defines a finite set or equivalence relation bounding
the variation. It cannot affect acceptance, safety, values, effects,
evaluation order, stable diagnostic family, governance, or artifact identity.

### Implementation limits

Exceeding a limit is not ordinary invalidity: the input would otherwise
conform. Report a diagnostic reserved for limit exhaustion and disclose
relevant limits in the implementation profile.

### Explicit runtime failures and traps

A failure or trap is specified behavior. Its rule identifies the triggering
condition, preceding effects, and terminated runtime scope. It never licenses
arbitrary behavior.

## No undefined behavior

Agent WASM has no undefined behavior. Omission is a specification defect and
supplies no conforming interpretation. Invalid input must fail as specified;
every in-scope runtime fault must have explicit behavior.

## Visible variability declarations

Use these rendered callouts in normative chapters:

- `> **Normative implementation-defined choice.**`
- `> **Normative unspecified presentation.**`

The label applies to exactly one immediately following paragraph or table. A
list, fenced block, or mixed sequence of Markdown blocks is not a governing
block. A thematic break ends any pending or active local scope. A table exists
for this purpose only when its header is immediately followed by a valid
Markdown delimiter row; a wrapped prose line containing a pipe remains part of
its paragraph. An unspecified-presentation paragraph contains the words
“bounded unspecified presentation” and states its bound. Each
specification-area README summarizes all `MAY`, `SHOULD`, presentation, and
limit clauses in a `## Variability register`.

A dependent rule or conformance test refers to an already declared choice as
the `profile-selected` or `profile-recorded` value and cites the governing
heading with an anchored Markdown link. Such a reference does not repeat the
variability callout and cannot widen the declared domain or alter its
observations. Each occurrence is either inside its own rendered anchored link
or is followed by that link in the same sentence or table row before another
profile reference or a semicolon; one link cannot satisfy multiple
occurrences. Link-like text inside inline code is not a citation.

## Conformance profiles

Every claimed implementation release publishes a versioned profile recording
its implementation and format versions, target, supported specification
versions, extensions, implementation-defined choices, `MAY` dispositions,
recommendation deviations, limits, and bounded unspecified presentation.

Profiles describe implementations; they never amend normative authority,
excuse a violated requirement, or turn an extension into standard behavior.
