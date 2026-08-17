#!/usr/bin/env python3
"""Focused tests for Agent WASM Research archive validation."""

import json
import unittest

import jsonschema

from validate_archive import (
    ROOT,
    archive_directories,
    github_heading_anchors,
    is_ignored,
    specification_structure_errors,
    specification_vocabulary_errors,
    visible_children,
)


class SpecificationStructureTests(unittest.TestCase):
    def assert_valid(self, body: str) -> None:
        errors, _count = specification_structure_errors("chapter.md", body)
        self.assertEqual([], errors)

    def test_accepts_classified_normative_definition(self) -> None:
        self.assert_valid(
            """# Example

## Rule

> **Normative definition.**

```text
result ::= value
```
"""
        )

    def test_accepts_fence_in_non_normative_section(self) -> None:
        self.assert_valid(
            """# Example

## Rationale (non-normative)

```mermaid
flowchart LR
  A --> B
```
"""
        )

    def test_rejects_unclassified_fence(self) -> None:
        errors, count = specification_structure_errors(
            "chapter.md", "# Example\n\n## Rule\n\n```text\nx\n```\n"
        )
        self.assertEqual(1, count)
        self.assertTrue(any("fenced block" in error for error in errors))

    def test_rejects_content_appended_to_exact_label(self) -> None:
        errors, count = specification_structure_errors(
            "chapter.md",
            "# Example\n\n> **Non-normative note.** extra\n\n```text\nx\n```\n",
        )
        self.assertEqual(1, count)
        self.assertTrue(any("fenced block" in error for error in errors))

    def test_rejects_malformed_authority_label_regardless_of_case(self) -> None:
        errors, _count = specification_structure_errors(
            "chapter.md",
            "# Example\n\n> **non-normative note.**\n\nExplanation.\n",
        )
        self.assertTrue(any("authority label" in error for error in errors))

    def test_rejects_unclosed_authority_style_label(self) -> None:
        errors, _count = specification_structure_errors(
            "chapter.md", "# Example\n\n> **Normative definition.\n\nText.\n"
        )
        self.assertTrue(any("authority label" in error for error in errors))

    def test_rejects_alternate_authority_style_emphasis(self) -> None:
        errors, _count = specification_structure_errors(
            "chapter.md", "# Example\n\n> __Normative definition.__\n\nText.\n"
        )
        self.assertTrue(any("authority label" in error for error in errors))

    def test_accepts_supported_conformance_labels(self) -> None:
        for label in ("Normative conformance criterion", "Normative test scenario"):
            with self.subTest(label=label):
                self.assert_valid(
                    f"# Example\n\n> **{label}.**\n\nImplementations MUST reject it.\n"
                )

    def test_rejects_unmarked_rationale_heading(self) -> None:
        errors, _count = specification_structure_errors(
            "chapter.md", "# Example\n\n## Rationale\n\nExplanation.\n"
        )
        self.assertTrue(any("section heading" in error for error in errors))

    def test_non_normative_scope_ends_at_peer_heading(self) -> None:
        errors, _count = specification_structure_errors(
            "chapter.md",
            """# Example

## Note (non-normative)

```text
explanation
```

## Rules

```text
unclassified
```
""",
        )
        self.assertEqual(1, len(errors))


class SpecificationVocabularyTests(unittest.TestCase):
    def assert_valid(self, body: str) -> None:
        self.assertEqual([], specification_vocabulary_errors("chapter.md", body))

    def test_accepts_canonical_words(self) -> None:
        self.assert_valid(
            "# Example\n\n## Rules\n\nImplementations MUST reject it and MAY explain.\n"
        )

    def test_rejects_requirement_alias(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md", "# Example\n\n## Rules\n\nThis is REQUIRED.\n"
        )
        self.assertTrue(any("requirement alias" in error for error in errors))

    def test_rejects_undefined_behavior(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md", "# Example\n\n## Rules\n\nThis has undefined behavior.\n"
        )
        self.assertTrue(any("undefined behavior" in error for error in errors))

    def test_accepts_visible_implementation_defined_choice(self) -> None:
        self.assert_valid(
            """# Example

## Choices

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little endian or big endian.
The host MUST record the selected byte order in the conformance profile.
The encoded bytes are observations that may differ.
"""
        )

    def test_callout_applies_to_complete_wrapped_paragraph(self) -> None:
        self.assert_valid(
            """# Example

## Choices

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little endian or big endian and
is selected by the conformance profile. The encoded bytes are observations
that may differ.
"""
        )

    def test_callout_accepts_explicit_host_defined_choice(self) -> None:
        self.assert_valid(
            """# Example

## Choices

> **Normative implementation-defined choice.**

The host defines byte order as either little endian or big endian and MUST
record its selection in the conformance profile. The encoded bytes are
observations that may differ.
"""
        )

    def test_callout_rejects_fixed_rule(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

The host applies patches in document order.
""",
        )
        self.assertTrue(any("positively declare" in error for error in errors))
        self.assertTrue(any("conformance profile" in error for error in errors))

    def test_callout_applies_to_complete_table(self) -> None:
        self.assert_valid(
            """# Example

## Choices

> **Normative implementation-defined choice.**

| Choice | Constraint |
| --- | --- |
| Byte order | The implementation-defined selection is either little or big endian, MUST be recorded in the conformance profile, and the encoded bytes are observations that may differ. |
"""
        )

    def test_callout_does_not_extend_past_following_paragraph(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little or big endian and the host MUST
record the selected byte order in the conformance profile. The encoded bytes are
observations that may differ.

Alignment is implementation-defined.
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requires a visible callout", errors[0])

    def test_callout_scope_stops_at_thematic_break(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Non-normative note.**

---
Normative systems SHALL reject this.
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requirement alias", errors[0])

    def test_variability_callout_rejects_thematic_break(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

---
Byte order is implementation-defined as either little endian or big endian,
MUST be recorded in the conformance profile, and encoded bytes are observable
results that may differ.
""",
        )
        self.assertTrue(any("paragraph or table" in error for error in errors))
        self.assertTrue(any("requires a visible callout" in error for error in errors))

    def test_pipe_prefixed_wrapped_prose_remains_one_paragraph(self) -> None:
        self.assert_valid(
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little endian or big endian,
| MUST be recorded in the conformance profile, and encoded bytes are
observable results that may differ.
"""
        )

    def test_reports_one_missing_callout_per_table(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

| Choice | Constraint |
| --- | --- |
| Byte order | The implementation-defined selection is little endian. |
| Alignment | The implementation-defined selection is four bytes. |
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requires a visible callout", errors[0])

    def test_non_normative_callout_applies_to_following_paragraph(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Non-normative note.**

Historical systems use SHALL and implementation-defined behavior.

Normative systems SHALL reject this.
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requirement alias", errors[0])

    def test_accepts_each_exact_non_normative_callout(self) -> None:
        for label in (
            "example",
            "rationale",
            "note",
            "diagram",
            "evidence",
        ):
            with self.subTest(label=label):
                self.assert_valid(
                    f"# Example\n\n> **Non-normative {label}.**\n\n"
                    "Historical systems use SHALL.\n"
                )

    def test_rejects_invented_non_normative_callout(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Non-normative typo.**

Normative systems SHALL reject this.
""",
        )
        self.assertTrue(any("authority label" in error for error in errors))
        self.assertTrue(any("requirement alias" in error for error in errors))

    def test_rejects_unsupported_normative_callout(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative assertion.**

Implementations MUST reject this.
""",
        )
        self.assertTrue(any("authority label" in error for error in errors))

    def test_ordinary_markdown_quote_is_not_an_authority_label(self) -> None:
        self.assert_valid("# Example\n\n> Historical context without a label.\n")
        errors = specification_vocabulary_errors(
            "chapter.md", "# Example\n\n> Historical systems use SHALL.\n"
        )
        self.assertTrue(any("requirement alias" in error for error in errors))

    def test_stacked_label_does_not_leak_non_normative_scope(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Non-normative note.**

> **Normative definition.**

Normative systems SHALL reject this.
""",
        )
        self.assertTrue(any("requirement alias" in error for error in errors))

    def test_variability_callout_rejects_list(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

- Byte order is implementation-defined as either little or big endian and MUST be recorded in the conformance profile.
""",
        )
        self.assertTrue(any("paragraph or table" in error for error in errors))
        self.assertTrue(any("requires a visible callout" in error for error in errors))

    def test_unspecified_variability_callout_rejects_list(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative unspecified presentation.**

- Names use bounded unspecified presentation up to alpha-renaming.
""",
        )
        self.assertTrue(any("paragraph or table" in error for error in errors))
        self.assertTrue(any("requires a visible callout" in error for error in errors))

    def test_variability_callout_rejects_indented_code(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

    Byte order is implementation-defined as either little or big endian and MUST be recorded in the conformance profile.
""",
        )
        self.assertTrue(any("paragraph or table" in error for error in errors))
        self.assertTrue(any("requires a visible callout" in error for error in errors))

    def test_variability_scope_stops_at_list_without_blank_line(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little or big endian, MUST be
recorded in the conformance profile, and encoded bytes are observable results
that may differ.
- Alignment is implementation-defined.
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requires a visible callout", errors[0])

    def test_variability_table_scope_stops_at_list_without_blank_line(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

| Choice | Constraint |
| --- | --- |
| Byte order | Either little or big endian; the implementation-defined selection MUST be recorded in the conformance profile, and encoded bytes are observable results that may differ. |
- Alignment | The alignment is implementation-defined.
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("requires a visible callout", errors[0])

    def test_rejects_negated_implementation_defined_declaration(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

This choice is not implementation-defined and MUST be recorded in the conformance profile.
""",
        )
        self.assertTrue(any("positively declare" in error for error in errors))

    def test_rejects_fixed_host_definition(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

The host defines the algorithm to be SHA-256, MUST record this selection in the
conformance profile, and states that digest bytes are observable results that
may differ.
""",
        )
        self.assertTrue(any("at least two alternatives" in error for error in errors))

    def test_requires_explicit_differing_observations(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little endian or big endian and
MUST be recorded in the conformance profile.
""",
        )
        self.assertTrue(any("observations may differ" in error for error in errors))

    def test_requires_conformance_profile_obligation(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little or big endian.
The encoded bytes are observations that may differ.
""",
        )
        self.assertTrue(any("conformance profile" in error for error in errors))

    def test_rejects_negated_conformance_profile_obligation(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little or big endian and MUST NOT be recorded in the conformance profile.
The encoded bytes are observations that may differ.
""",
        )
        self.assertTrue(any("conformance profile" in error for error in errors))

    def test_rejects_profile_obligation_negated_after_profile_name(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

> **Normative implementation-defined choice.**

Byte order is implementation-defined as either little endian or big endian.
The conformance profile MUST NOT record the selected byte order.
The encoded bytes are observations that may differ.
""",
        )
        self.assertTrue(any("conformance profile" in error for error in errors))

    def test_negated_implementation_defined_mention_needs_no_callout(self) -> None:
        self.assert_valid(
            "# Example\n\nByte order is not an implementation-defined choice.\n"
        )
        self.assert_valid(
            "# Example\n\nThis rule MUST NOT be treated as "
            "implementation-defined behavior.\n"
        )

    def test_profile_recorded_reference_requires_anchor(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md", "# Example\n\nUse the profile-recorded byte order.\n"
        )
        self.assertEqual(1, len(errors))
        self.assertIn("anchored Markdown citation", errors[0])

    def test_profile_selected_reference_accepts_anchor(self) -> None:
        self.assert_valid(
            "# Example\n\nUse the profile-selected byte order from "
            "[Byte order](choices.md#byte-order).\n"
        )

    def test_profile_selected_reference_rejects_anchored_image(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            "# Example\n\nUse the profile-selected byte order "
            "![diagram](choices.md#byte-order).\n",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("anchored Markdown citation", errors[0])

    def test_profile_reference_rejects_link_like_inline_code(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            "# Example\n\nUse the profile-selected byte order; literal "
            "`[not a link](choices.md#byte-order)`.\n",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("anchored Markdown citation", errors[0])

    def test_profile_reference_rejects_unassociated_real_link(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            "# Example\n\nUse the profile-selected byte order; see "
            "[Unrelated](choices.md#unrelated).\n",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("anchored Markdown citation", errors[0])

    def test_each_profile_reference_requires_its_own_link(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            "# Example\n\nUse the profile-selected byte order and the "
            "profile-recorded alignment from [Choices](choices.md#choices).\n",
        )
        self.assertEqual(1, len(errors))
        self.assertIn("anchored Markdown citation", errors[0])

    def test_each_profile_reference_accepts_its_own_link(self) -> None:
        self.assert_valid(
            "# Example\n\nUse the profile-selected byte order from "
            "[Byte order](choices.md#byte-order) and the profile-recorded alignment "
            "from [Alignment](choices.md#alignment).\n"
        )

    def test_profile_reference_accepts_occurrence_inside_link(self) -> None:
        self.assert_valid(
            "# Example\n\nUse the "
            "[profile-selected byte order](choices.md#byte-order).\n"
        )

    def test_each_profile_reference_table_row_requires_anchor(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

| Choice | Use |
| --- | --- |
| Byte order | Use the profile-selected value from [Byte order](choices.md#byte-order). |
| Alignment | Use the profile-recorded value. |
""",
        )
        self.assertEqual(1, len(errors))
        self.assertIn(":6:", errors[0])
        self.assertIn("anchored Markdown citation", errors[0])

    def test_negated_profile_selected_term_is_not_a_reference(self) -> None:
        self.assert_valid(
            "# Example\n\nInternal mechanisms are not profile-selected semantics.\n"
        )

    def test_accepts_bounded_unspecified_presentation(self) -> None:
        self.assert_valid(
            """# Example

## Choices

> **Normative unspecified presentation.**

Names use bounded unspecified presentation up to alpha-renaming.
"""
        )

    def test_rejects_unbounded_unspecified_presentation(self) -> None:
        errors = specification_vocabulary_errors(
            "chapter.md",
            """# Example

## Choices

> **Normative unspecified presentation.**

Names use unspecified presentation.
""",
        )
        self.assertTrue(any("must label bounded" in error for error in errors))

    def test_ignores_non_normative_section_and_fence(self) -> None:
        self.assert_valid(
            """# Example

## Rationale (non-normative)

Historical systems use SHALL and undefined behavior.

> **Non-normative example.**

```text
OPTIONAL undefined behavior
```
"""
        )


class FrontmatterSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads((ROOT / "frontmatter.schema.json").read_text())
        cls.validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )

    def specification(self, version: str) -> dict[str, object]:
        return {
            "title": "Example",
            "kind": "specification",
            "created": "2026-08-07",
            "status": "draft",
            "spec_version": version,
            "tags": [],
            "aliases": [],
        }

    def test_accepts_exact_semantic_version(self) -> None:
        self.assertEqual([], list(self.validator.iter_errors(self.specification("0.1.0"))))

    def test_rejects_non_exact_versions(self) -> None:
        for version in ("0.1", "0.1.0-preview", "01.1.0"):
            with self.subTest(version=version):
                self.assertNotEqual(
                    [], list(self.validator.iter_errors(self.specification(version)))
                )

    def test_rejects_unknown_metadata(self) -> None:
        metadata = self.specification("1.0.0")
        metadata["updated"] = "2026-08-07"
        self.assertNotEqual([], list(self.validator.iter_errors(metadata)))


class HeadingAnchorTests(unittest.TestCase):
    def test_generates_duplicate_github_anchors(self) -> None:
        self.assertEqual(
            {"same-heading", "same-heading-1"},
            github_heading_anchors("# Same heading\n\n## Same heading\n"),
        )


class ArchivePathTests(unittest.TestCase):
    def test_ignores_top_level_application_source(self) -> None:
        self.assertTrue(is_ignored(ROOT / "src" / "lib"))

    def test_does_not_ignore_nested_source_named_src(self) -> None:
        self.assertFalse(is_ignored(ROOT / "20-notes" / "src"))

    def test_root_inventory_includes_application_source(self) -> None:
        self.assertIn(ROOT / "src", visible_children(ROOT))

    def test_archive_traversal_excludes_application_source(self) -> None:
        self.assertNotIn(ROOT / "src", archive_directories())


if __name__ == "__main__":
    unittest.main()
