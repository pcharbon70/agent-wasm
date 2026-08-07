#!/usr/bin/env python3
"""Focused tests for Agent WASM Research archive validation."""

import json
import unittest

import jsonschema

from validate_archive import (
    ROOT,
    github_heading_anchors,
    specification_structure_errors,
    specification_vocabulary_errors,
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
"""
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


if __name__ == "__main__":
    unittest.main()
