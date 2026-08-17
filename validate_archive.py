#!/usr/bin/env python3
"""Validate the Agent WASM Research archive's structural invariants."""

from __future__ import annotations

import copy
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import jsonschema
    import yaml
except ModuleNotFoundError as error:
    print(
        f"Missing validation dependency: {error.name}. "
        "Run `python3 -m pip install -r requirements-validation.txt`.",
        file=sys.stderr,
    )
    raise SystemExit(2) from error


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "frontmatter.schema.json"
SPECIFICATION_ROOT = ROOT / "60-specification"
SPECIFICATION_AUTHORITY_PATH = ROOT / "SPECIFICATION-AUTHORITY.md"
CONFORMANCE_VOCABULARY_PATH = ROOT / "CONFORMANCE-VOCABULARY.md"
ARCHIVE_DIRECTORIES = {
    "00-inbox",
    "10-maps",
    "20-notes",
    "30-sources",
    "40-inquiries",
    "50-journal",
    "60-specification",
    "90-archive",
    "assets",
    "templates",
}
NON_ARCHIVE_ROOTS = {"src"}
IGNORED_NAMES = {
    ".DS_Store",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
REQUIRED_README_HEADINGS = {
    "Purpose",
    "What belongs here",
    "Index",
    "Maintaining this index",
}
KNOWLEDGE_FILENAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
JOURNAL_FILENAME = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?\.md$"
)
PLACEHOLDER = re.compile(
    r"\{(?:title|question|YYYY-MM-DD|author|directory title|directory-name|"
    r"MAJOR\.MINOR\.PATCH)\}"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_CITATION = re.compile(r"(?<![!\\])\[[^\]\n]+\]\(([^)\n]+)\)")
FENCE_START = re.compile(r"^(`{3,}|~{3,})")
SPECIFICATION_CONTENT_LABEL = re.compile(
    r"^> \*\*(?:Normative definition|Normative conformance example|"
    r"Non-normative (?:example|rationale|note|diagram|evidence))\.\*\*$"
)
IMPLEMENTATION_DEFINED_CALLOUT = "> **Normative implementation-defined choice.**"
UNSPECIFIED_PRESENTATION_CALLOUT = "> **Normative unspecified presentation.**"
NORMATIVE_CALLOUTS = {
    "> **Normative definition.**",
    "> **Normative conformance example.**",
    "> **Normative conformance criterion.**",
    "> **Normative test scenario.**",
    IMPLEMENTATION_DEFINED_CALLOUT,
    UNSPECIFIED_PRESENTATION_CALLOUT,
}
NON_NORMATIVE_CALLOUTS = {
    "> **Non-normative example.**",
    "> **Non-normative rationale.**",
    "> **Non-normative note.**",
    "> **Non-normative diagram.**",
    "> **Non-normative evidence.**",
}
AUTHORITY_CALLOUTS = NORMATIVE_CALLOUTS | NON_NORMATIVE_CALLOUTS
AUTHORITY_STYLE_BLOCKQUOTE = re.compile(
    r"^>\s*(?:\*{2,3}|_{2,3})\s*"
    r"(?:normative|non[^A-Za-z0-9]*normative)\b",
    re.IGNORECASE,
)
UPPERCASE_REQUIREMENT_ALIAS = re.compile(
    r"\b(?:REQUIRED|SHALL(?: NOT)?|RECOMMENDED|NOT RECOMMENDED|OPTIONAL)\b"
)
UNDEFINED_BEHAVIOR = re.compile(r"\bundefined behavior\b", re.IGNORECASE)
IMPLEMENTATION_DEFINED_TERM = re.compile(
    r"\bimplementation[- ]defined\b", re.IGNORECASE
)
IMPLEMENTATION_DEFINED_DECLARATION = re.compile(
    r"\b(?:implementation[- ]defined|(?:the )?(?:host|implementation) defines)\b",
    re.IGNORECASE,
)
NEGATED_IMPLEMENTATION_DEFINED = re.compile(
    r"(?:\b(?:(?:(?:is|are|was|were|be|being)\s+(?:explicitly\s+)?)?"
    r"(?:not|never|no longer)|(?:MUST|SHOULD|MAY)\s+NOT|cannot|no)\s+"
    r"(?:(?:be\s+)?(?:(?:treated|classified|regarded|considered|described)\s+"
    r"as\s+)?)?(?:an?\s+)?implementation[- ]defined\b|"
    r"\b(?:does|do)\s+not\s+(?:constitute|create)\s+(?:an?\s+)?"
    r"implementation[- ]defined\b)",
    re.IGNORECASE,
)
NEGATED_HOST_DEFINITION = re.compile(
    r"\b(?:no\s+(?:host|implementation)|(?:the\s+)?(?:host|implementation)\s+"
    r"(?:does\s+not|never))\s+defines\b",
    re.IGNORECASE,
)
IMPLEMENTATION_DEFINED_ALTERNATIVES = re.compile(
    r"(?:\beither\b.{0,160}\bor\b|\bone of\b|\bwhether\b|"
    r"\bbetween\b.{0,160}\band\b|\b(?:bounded|finite)\s+"
    r"(?:set|range|domain)\b|\b(?:set|range|domain)\s+(?:of|from)\b|"
    r"\([^()\n]*(?:,|\bor\b)[^()\n]*\))",
    re.IGNORECASE,
)
DIFFERING_OBSERVATIONS = re.compile(
    r"(?:\bobservations?\s+(?:that\s+)?(?:may|can)\s+"
    r"(?:differ|vary|change)\b|\b(?:observable|observed)\b.{0,160}"
    r"\b(?:may|can)\s+(?:differ|vary|change)\b|\b(?:may|can)\s+"
    r"(?:differ|vary|change)\b.{0,160}\b(?:observable|observations?)\b)",
    re.IGNORECASE,
)
PROFILE_ACTION = (
    r"(?:record(?:ed|ing|s)?|document(?:ed|ing|s)?|publish(?:ed|ing|es)?|"
    r"select(?:ed|ing|s)?|specif(?:ied|ies|ying)|declar(?:ed|es|ing)|"
    r"include(?:d|s|ing)?|contain(?:ed|s|ing)?)"
)
CONFORMANCE_PROFILE_OBLIGATION = re.compile(
    rf"(?:\b{PROFILE_ACTION}\b.{{0,160}}\bconformance profile\b|"
    rf"\bconformance profile\b.{{0,160}}\b{PROFILE_ACTION}\b)",
    re.IGNORECASE,
)
PROFILE_NEGATION = (
    r"(?:(?:MUST|SHOULD|MAY)\s+NOT|(?:does|do|is|are|was|were|need)\s+not|"
    r"not|never)"
)
NEGATED_CONFORMANCE_PROFILE_OBLIGATION = re.compile(
    rf"(?:\b{PROFILE_NEGATION}\s+(?:(?:be|required\s+to)\s+)?"
    rf"{PROFILE_ACTION}\b.{{0,160}}\bconformance profile\b|"
    rf"\bconformance profile\b.{{0,160}}\b{PROFILE_NEGATION}\s+"
    rf"(?:(?:be|required\s+to)\s+)?{PROFILE_ACTION}\b)",
    re.IGNORECASE,
)
PROFILE_RECORDED_REFERENCE = re.compile(
    r"\bprofile-(?:selected|recorded)\b", re.IGNORECASE
)
NEGATED_PROFILE_RECORDED_REFERENCE = re.compile(
    r"\b(?:not|never|no longer)\s+profile-(?:selected|recorded)\b", re.IGNORECASE
)
UNSPECIFIED_TERM = re.compile(r"\bunspecified\b", re.IGNORECASE)
BOUNDED_UNSPECIFIED = re.compile(
    r"\bbounded unspecified presentation\b", re.IGNORECASE
)
NON_NORMATIVE_HEADING_SUFFIX = " (non-normative)"
NON_NORMATIVE_HEADING_ROLE = re.compile(
    r"(?:\brationale\b|^connections$|^proof(?: outline| status)?$|"
    r"^evidence(?: route| status)?$)",
    re.IGNORECASE,
)
LIST_ITEM_START = re.compile(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+")
PARAGRAPH_INTERRUPTING_LIST = re.compile(r"^\s{0,3}(?:[-+*]|1[.)])\s+")
TABLE_DELIMITER_CELL = re.compile(r"^:?-{3,}:?$")
THEMATIC_BREAK = re.compile(
    r"^\s{0,3}(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$"
)


class StringDateLoader(yaml.SafeLoader):
    """A safe YAML loader that preserves ISO dates as strings."""


StringDateLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)
for initial, resolvers in list(StringDateLoader.yaml_implicit_resolvers.items()):
    StringDateLoader.yaml_implicit_resolvers[initial] = [
        (tag, expression)
        for tag, expression in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]


def relative(path: Path) -> str:
    """Return a stable repository-relative display path."""

    try:
        value = path.resolve().relative_to(ROOT)
    except ValueError:
        return str(path)
    return "." if value == Path(".") else value.as_posix()


def is_ignored(path: Path) -> bool:
    """Return whether a path is excluded from archive traversal."""

    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return (
        bool(parts and parts[0] in NON_ARCHIVE_ROOTS)
        or any(part in IGNORED_NAMES or part.startswith(".") for part in parts)
    )


def visible_children(directory: Path) -> list[Path]:
    """Return direct children that the directory README must inventory."""

    is_root = directory.resolve() == ROOT
    return sorted(
        (
            child
            for child in directory.iterdir()
            if child.name != "README.md"
            and (
                not is_ignored(child)
                or (is_root and child.name in NON_ARCHIVE_ROOTS)
            )
        ),
        key=lambda child: child.name,
    )


def archive_directories() -> list[Path]:
    """Return the root and every non-generated archive directory."""

    return [
        ROOT,
        *sorted(
            (
                path
                for path in ROOT.rglob("*")
                if path.is_dir() and not is_ignored(path)
            ),
            key=lambda path: path.as_posix(),
        ),
    ]


def completed_markdown_files() -> list[Path]:
    """Return completed knowledge documents and directory READMEs."""

    files: list[Path] = []
    for top_name in sorted(ARCHIVE_DIRECTORIES):
        top = ROOT / top_name
        if not top.is_dir():
            continue
        for path in sorted(top.rglob("*.md")):
            if is_ignored(path):
                continue
            if top_name == "templates" and path.name != "README.md":
                continue
            if top_name == "00-inbox" and path.name != "README.md":
                continue
            files.append(path)
    return files


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    """Parse one completed Markdown file into metadata and body."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing YAML frontmatter delimiter")
    metadata = yaml.load(text[4:end], Loader=StringDateLoader)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return metadata, text[end + 5 :]


def link_destination(raw: str) -> str:
    """Remove optional Markdown angle brackets and link titles."""

    value = raw.strip()
    if value.startswith("<"):
        close = value.find(">")
        return value[1:close] if close >= 0 else value[1:]
    return value.split(maxsplit=1)[0]


def authority_callout_error(stripped: str) -> str | None:
    """Return an error for a malformed or unsupported authority-style quote."""

    if (
        AUTHORITY_STYLE_BLOCKQUOTE.match(stripped)
        and stripped not in AUTHORITY_CALLOUTS
    ):
        return "malformed or unsupported specification authority label"
    return None


def strip_inline_code(text: str) -> str:
    """Blank inline code spans while preserving offsets and line breaks."""

    characters = list(text)
    index = 0
    while index < len(text):
        if text[index] != "`" or (index > 0 and text[index - 1] == "\\"):
            index += 1
            continue
        marker_end = index
        while marker_end < len(text) and text[marker_end] == "`":
            marker_end += 1
        marker = text[index:marker_end]
        close = text.find(marker, marker_end)
        if close < 0:
            index = marker_end
            continue
        for position in range(index, close + len(marker)):
            if characters[position] != "\n":
                characters[position] = " "
        index = close + len(marker)
    return "".join(characters)


def without_matches(pattern: re.Pattern[str], text: str) -> str:
    """Blank regex matches while preserving offsets and line breaks."""

    characters = list(text)
    for match in pattern.finditer(text):
        for position in range(match.start(), match.end()):
            if characters[position] != "\n":
                characters[position] = " "
    return "".join(characters)


def is_table_delimiter(line: str) -> bool:
    """Return whether a line is a valid GFM-style table delimiter row."""

    stripped = line.strip()
    if "|" not in stripped:
        return False
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = [cell.strip() for cell in stripped.split("|")]
    return bool(cells) and all(TABLE_DELIMITER_CELL.fullmatch(cell) for cell in cells)


def is_table_row(line: str) -> bool:
    """Return whether a line can continue a recognized Markdown table."""

    return re.search(r"(?<!\\)\|", line) is not None


def local_link_target(source: Path, raw: str) -> tuple[Path, str] | None:
    """Resolve a Markdown destination, returning None for external links."""

    destination = link_destination(raw)
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc:
        return None
    decoded_path = unquote(parsed.path)
    target = source if not decoded_path else source.parent / decoded_path
    return target.resolve(), unquote(parsed.fragment)


def github_heading_anchors(markdown: str) -> set[str]:
    """Approximate GitHub heading IDs, including duplicate suffixes."""

    anchors: set[str] = set()
    occurrences: defaultdict[str, int] = defaultdict(int)
    for line in markdown.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = re.sub(r"<[^>]+>", "", match.group(1))
        heading = re.sub(r"[`*_~]", "", heading).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", slug)
        suffix = occurrences[slug]
        occurrences[slug] += 1
        anchors.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return anchors


def specification_structure_errors(
    display_path: str, body: str, line_offset: int = 0
) -> tuple[list[str], int]:
    """Validate visible authority labels in one specification chapter."""

    errors: list[str] = []
    active_non_normative_level: int | None = None
    previous_nonempty = ""
    fence_marker = ""
    fenced_blocks = 0

    for body_line, line in enumerate(body.splitlines(), start=1):
        line_number = body_line + line_offset
        stripped = line.strip()
        if fence_marker:
            if stripped.startswith(fence_marker):
                fence_marker = ""
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if active_non_normative_level is not None and level <= active_non_normative_level:
                active_non_normative_level = None
            is_non_normative = text.casefold().endswith(
                NON_NORMATIVE_HEADING_SUFFIX
            )
            role = (
                text[: -len(NON_NORMATIVE_HEADING_SUFFIX)]
                if is_non_normative
                else text
            )
            if NON_NORMATIVE_HEADING_ROLE.search(role) and not is_non_normative:
                errors.append(
                    f"{display_path}:{line_number}: non-normative section heading "
                    "must end with '(non-normative)'"
                )
            if is_non_normative:
                active_non_normative_level = level
            previous_nonempty = stripped
            continue

        authority_error = authority_callout_error(stripped)
        if authority_error is not None:
            errors.append(f"{display_path}:{line_number}: {authority_error}")

        fence = FENCE_START.match(stripped)
        if fence:
            fenced_blocks += 1
            if (
                active_non_normative_level is None
                and SPECIFICATION_CONTENT_LABEL.fullmatch(previous_nonempty) is None
            ):
                errors.append(
                    f"{display_path}:{line_number}: specification fenced block must "
                    "follow a visible authority callout or appear in a "
                    "non-normative section"
                )
            fence_marker = fence.group(1)
            continue

        if stripped:
            previous_nonempty = stripped

    return errors, fenced_blocks


def specification_vocabulary_errors(
    display_path: str, body: str, line_offset: int = 0
) -> list[str]:
    """Check normative prose for canonical requirement and variability terms."""

    errors: list[str] = []
    active_non_normative_level: int | None = None
    fence_marker = ""
    fence_is_non_normative = False
    pending_variability: tuple[str, int] | None = None
    pending_non_normative = False
    block_lines: list[tuple[int, str]] = []
    block_kind = ""
    block_variability = ""
    block_is_non_normative = False
    previous_nonempty = ""

    def line_block_kind(line: str) -> str:
        if LIST_ITEM_START.match(line):
            return "list"
        if line.startswith("    ") or line.startswith("\t"):
            return "other"
        return "paragraph"

    def uncited_profile_reference_lines() -> list[int]:
        raw_text = "\n".join(line for _line_number, line in block_lines)
        text = strip_inline_code(raw_text)
        text = without_matches(NEGATED_PROFILE_RECORDED_REFERENCE, text)
        if block_kind == "table":
            units: list[tuple[int, int]] = []
            start = 0
            for line in text.splitlines(keepends=True):
                units.append((start, start + len(line)))
                start += len(line)
            if start < len(text) or not units:
                units.append((start, len(text)))
        else:
            units = []
            start = 0
            for boundary in re.finditer(r"(?<=[.!?])(?:[ \t]+|\n+)", text):
                units.append((start, boundary.start()))
                start = boundary.end()
            units.append((start, len(text)))

        missing: list[int] = []
        for unit_start, unit_end in units:
            unit = text[unit_start:unit_end]
            references = list(PROFILE_RECORDED_REFERENCE.finditer(unit))
            citations = [
                match
                for match in MARKDOWN_CITATION.finditer(unit)
                if urlsplit(link_destination(match.group(1))).fragment
            ]
            used_citations: set[int] = set()
            for reference_index, reference in enumerate(references):
                next_reference = (
                    references[reference_index + 1].start()
                    if reference_index + 1 < len(references)
                    else len(unit)
                )
                citation_index = next(
                    (
                        index
                        for index, citation in enumerate(citations)
                        if index not in used_citations
                        and citation.start() <= reference.start() < citation.end()
                    ),
                    None,
                )
                if citation_index is None:
                    citation_index = next(
                        (
                            index
                            for index, citation in enumerate(citations)
                            if index not in used_citations
                            and reference.end() <= citation.start() < next_reference
                            and ";" not in unit[reference.end() : citation.start()]
                        ),
                        None,
                    )
                if citation_index is not None:
                    used_citations.add(citation_index)
                    continue
                position = unit_start + reference.start()
                line_index = raw_text.count("\n", 0, position)
                missing.append(block_lines[min(line_index, len(block_lines) - 1)][0])
        return missing

    def finish_block() -> None:
        nonlocal block_lines, block_kind, block_variability, block_is_non_normative
        if not block_lines:
            return

        if not block_is_non_normative:
            text = " ".join(line for _line_number, line in block_lines)
            for line_number, line in block_lines:
                if UPPERCASE_REQUIREMENT_ALIAS.search(line):
                    errors.append(
                        f"{display_path}:{line_number}: prohibited uppercase "
                        "requirement alias"
                    )
                if UNDEFINED_BEHAVIOR.search(line):
                    errors.append(
                        f"{display_path}:{line_number}: normative text must not "
                        "define undefined behavior"
                    )

            if block_variability == "implementation-defined":
                positive_text = without_matches(NEGATED_IMPLEMENTATION_DEFINED, text)
                positive_text = without_matches(NEGATED_HOST_DEFINITION, positive_text)
                choice_text = without_matches(
                    CONFORMANCE_PROFILE_OBLIGATION, positive_text
                )
                enumerated_table = block_kind == "table" and len(block_lines) >= 4
                if not IMPLEMENTATION_DEFINED_DECLARATION.search(choice_text):
                    errors.append(
                        f"{display_path}:{block_lines[0][0]}: "
                        "implementation-defined callout must positively declare "
                        "an implementation-defined choice"
                    )
                if not (
                    IMPLEMENTATION_DEFINED_ALTERNATIVES.search(choice_text)
                    or enumerated_table
                ):
                    errors.append(
                        f"{display_path}:{block_lines[0][0]}: "
                        "implementation-defined choice must enumerate at least two "
                        "alternatives or an explicitly bounded domain"
                    )
                if not DIFFERING_OBSERVATIONS.search(choice_text):
                    errors.append(
                        f"{display_path}:{block_lines[0][0]}: "
                        "implementation-defined choice must state which observations "
                        "may differ"
                    )
                if (
                    NEGATED_CONFORMANCE_PROFILE_OBLIGATION.search(text)
                    or not CONFORMANCE_PROFILE_OBLIGATION.search(text)
                ):
                    errors.append(
                        f"{display_path}:{block_lines[0][0]}: "
                        "implementation-defined choice must require its selection "
                        "in the conformance profile"
                    )
            elif block_variability == "unspecified-presentation":
                if not BOUNDED_UNSPECIFIED.search(text):
                    errors.append(
                        f"{display_path}:{block_lines[0][0]}: "
                        "unspecified-presentation callout must label bounded "
                        "unspecified presentation"
                    )
            else:
                implementation_defined_line = next(
                    (
                        line_number
                        for line_number, line in block_lines
                        if IMPLEMENTATION_DEFINED_TERM.search(
                            without_matches(NEGATED_IMPLEMENTATION_DEFINED, line)
                        )
                    ),
                    None,
                )
                if implementation_defined_line is not None:
                    errors.append(
                        f"{display_path}:{implementation_defined_line}: "
                        "implementation-defined choice requires a visible callout"
                    )
                unspecified_line = next(
                    (
                        line_number
                        for line_number, line in block_lines
                        if UNSPECIFIED_TERM.search(line)
                    ),
                    None,
                )
                if unspecified_line is not None:
                    errors.append(
                        f"{display_path}:{unspecified_line}: unspecified presentation "
                        "requires a visible callout"
                    )

            for profile_reference_line in uncited_profile_reference_lines():
                errors.append(
                    f"{display_path}:{profile_reference_line}: profile-selected or "
                    "profile-recorded reference requires an anchored Markdown citation"
                )

        block_lines = []
        block_kind = ""
        block_variability = ""
        block_is_non_normative = False

    def start_or_extend_block(
        line_number: int, line: str, kind_override: str | None = None
    ) -> None:
        nonlocal pending_variability, pending_non_normative
        nonlocal block_kind, block_variability, block_is_non_normative
        kind = kind_override or line_block_kind(line)

        if block_lines:
            if (
                block_kind == "paragraph"
                and is_table_delimiter(line)
                and len(block_lines) == 1
                and is_table_row(block_lines[0][1])
            ):
                block_kind = "table"
            elif block_kind == "paragraph" and PARAGRAPH_INTERRUPTING_LIST.match(line):
                finish_block()
            elif block_kind == "paragraph" and kind == "quote":
                finish_block()
            elif block_kind == "table" and (
                kind in {"list", "other"} or not is_table_row(line)
            ):
                finish_block()
            elif block_kind == "quote" and kind != "quote":
                finish_block()

        if not block_lines:
            block_kind = kind
            if pending_variability is not None:
                if block_kind in {"paragraph", "table"}:
                    block_variability = pending_variability[0]
                    pending_variability = None
                else:
                    reject_pending_variability(
                        "must govern an immediately following paragraph or table"
                    )
            block_is_non_normative = pending_non_normative
            pending_non_normative = False
        block_lines.append((line_number, line))

    def reject_pending_variability(reason: str | None = None) -> None:
        nonlocal pending_variability
        if pending_variability is None:
            return
        kind, callout_line = pending_variability
        if reason is not None:
            errors.append(f"{display_path}:{callout_line}: variability callout {reason}")
            pending_variability = None
            return
        if kind == "implementation-defined":
            errors.append(
                f"{display_path}:{callout_line}: implementation-defined callout "
                "must label an implementation-defined choice"
            )
        else:
            errors.append(
                f"{display_path}:{callout_line}: unspecified-presentation callout "
                "must label bounded unspecified presentation"
            )
        pending_variability = None

    for body_line, line in enumerate(body.splitlines(), start=1):
        line_number = body_line + line_offset
        stripped = line.strip()
        if fence_marker:
            if stripped.startswith(fence_marker):
                finish_block()
                fence_marker = ""
                fence_is_non_normative = False
            elif not fence_is_non_normative:
                if stripped:
                    start_or_extend_block(line_number, line)
                else:
                    finish_block()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            finish_block()
            reject_pending_variability()
            pending_non_normative = False
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if active_non_normative_level is not None and level <= active_non_normative_level:
                active_non_normative_level = None
            if text.casefold().endswith(NON_NORMATIVE_HEADING_SUFFIX):
                active_non_normative_level = level
            previous_nonempty = stripped
            continue

        fence = FENCE_START.match(stripped)
        if fence:
            finish_block()
            reject_pending_variability(
                "must govern an immediately following paragraph or table"
            )
            fence_marker = fence.group(1)
            fence_is_non_normative = (
                active_non_normative_level is not None
                or pending_non_normative
                or previous_nonempty in NON_NORMATIVE_CALLOUTS
            )
            pending_non_normative = False
            continue

        if active_non_normative_level is not None:
            if stripped:
                previous_nonempty = stripped
            continue

        if THEMATIC_BREAK.fullmatch(line):
            finish_block()
            reject_pending_variability(
                "must govern an immediately following paragraph or table"
            )
            pending_non_normative = False
            previous_nonempty = stripped
            continue

        if stripped == IMPLEMENTATION_DEFINED_CALLOUT:
            finish_block()
            reject_pending_variability()
            pending_non_normative = False
            pending_variability = ("implementation-defined", line_number)
            previous_nonempty = stripped
            continue
        if stripped == UNSPECIFIED_PRESENTATION_CALLOUT:
            finish_block()
            reject_pending_variability()
            pending_non_normative = False
            pending_variability = ("unspecified-presentation", line_number)
            previous_nonempty = stripped
            continue
        if stripped in NORMATIVE_CALLOUTS:
            finish_block()
            reject_pending_variability()
            pending_non_normative = False
            previous_nonempty = stripped
            continue
        if stripped in NON_NORMATIVE_CALLOUTS:
            finish_block()
            reject_pending_variability()
            pending_non_normative = True
            previous_nonempty = stripped
            continue
        authority_error = authority_callout_error(stripped)
        if authority_error is not None:
            finish_block()
            reject_pending_variability()
            pending_non_normative = False
            errors.append(f"{display_path}:{line_number}: {authority_error}")
            previous_nonempty = stripped
            continue
        if not stripped:
            finish_block()
            continue
        if stripped.startswith(">"):
            quote_line = re.sub(r"^\s{0,3}>\s?", "", line)
            if not quote_line.strip():
                finish_block()
                reject_pending_variability(
                    "must govern an immediately following paragraph or table"
                )
                pending_non_normative = False
            else:
                start_or_extend_block(line_number, quote_line, "quote")
            previous_nonempty = stripped
            continue

        start_or_extend_block(line_number, line)
        previous_nonempty = stripped

    finish_block()
    reject_pending_variability()
    return errors


def policy_link_errors(
    display_path: str, targets: set[Path], required: Path, label: str
) -> list[str]:
    """Require a specification index to expose a repository policy."""

    if required.resolve() in targets:
        return []
    return [f"{display_path}: missing link to {label}"]


def validate() -> tuple[list[str], dict[str, int]]:
    """Run all checks and return errors plus summary counts."""

    errors: list[str] = []
    counts: defaultdict[str, int] = defaultdict(int)
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError) as error:
        return [f"{relative(SCHEMA_PATH)}: invalid JSON Schema: {error}"], counts

    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    records: dict[Path, tuple[dict[str, object], str]] = {}

    for name in sorted(ARCHIVE_DIRECTORIES):
        if not (ROOT / name).is_dir():
            errors.append(f"{name}/: missing canonical archive directory")

    for path in completed_markdown_files():
        counts["completed_documents"] += 1
        try:
            metadata, body = parse_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{relative(path)}: {error}")
            continue
        records[path.resolve()] = (metadata, body)
        for schema_error in sorted(
            validator.iter_errors(metadata), key=lambda item: list(item.absolute_path)
        ):
            location = ".".join(str(part) for part in schema_error.absolute_path)
            errors.append(
                f"{relative(path)}: frontmatter {location or '<root>'}: "
                f"{schema_error.message}"
            )

        h1 = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
        title = str(metadata.get("title", ""))
        if h1 is None:
            errors.append(f"{relative(path)}: missing H1")
        elif path.name == "README.md":
            if not h1.group(1).replace("`", "").startswith(title):
                errors.append(
                    f"{relative(path)}: H1 {h1.group(1)!r} does not match title {title!r}"
                )
        elif h1.group(1) != title:
            errors.append(
                f"{relative(path)}: H1 {h1.group(1)!r} does not match title {title!r}"
            )

        if path.name == "README.md":
            continue
        kind = metadata.get("kind")
        filename_pattern = JOURNAL_FILENAME if kind == "journal" else KNOWLEDGE_FILENAME
        if not filename_pattern.fullmatch(path.name):
            errors.append(
                f"{relative(path)}: filename does not follow the convention for {kind}"
            )
        destinations = {
            "map": "10-maps",
            "note": "20-notes",
            "source": "30-sources",
            "inquiry": "40-inquiries",
            "journal": "50-journal",
            "specification": "60-specification",
        }
        top_name = path.relative_to(ROOT).parts[0]
        expected = destinations.get(str(kind))
        if top_name not in {"90-archive", "assets"} and expected and top_name != expected:
            errors.append(f"{relative(path)}: kind {kind!r} belongs in {expected}/")
        if kind == "specification":
            counts["specification_documents"] += 1
            raw = path.read_text(encoding="utf-8")
            line_offset = raw[: raw.find("\n---\n", 4) + 5].count("\n")
            structure, fences = specification_structure_errors(
                relative(path), body, line_offset
            )
            errors.extend(structure)
            counts["specification_fenced_blocks"] += fences
            if metadata.get("status") == "normative":
                errors.extend(
                    specification_vocabulary_errors(relative(path), body, line_offset)
                )

    for path in sorted(ROOT.rglob("*.md")):
        if is_ignored(path) or path.parent == ROOT / "templates" or path == ROOT / "AGENTS.md":
            continue
        if path.parent == ROOT / "00-inbox" and path.name != "README.md":
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if PLACEHOLDER.search(line):
                errors.append(
                    f"{relative(path)}:{line_number}: unresolved template placeholder"
                )

    links_by_source: defaultdict[Path, set[Path]] = defaultdict(set)
    incoming_from_conceptual: defaultdict[Path, set[Path]] = defaultdict(set)
    for path in sorted(ROOT.rglob("*.md")):
        if is_ignored(path):
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for raw in MARKDOWN_LINK.findall(line):
                resolved = local_link_target(path, raw)
                if resolved is None:
                    continue
                target, fragment = resolved
                counts["local_links"] += 1
                if link_destination(raw).startswith("/"):
                    errors.append(
                        f"{relative(path)}:{line_number}: local link must be relative: {raw}"
                    )
                    continue
                if not target.exists():
                    errors.append(
                        f"{relative(path)}:{line_number}: missing local link target: {raw}"
                    )
                    continue
                links_by_source[path.resolve()].add(target)
                if target.suffix.lower() == ".md" and fragment:
                    anchors = github_heading_anchors(target.read_text(encoding="utf-8"))
                    if fragment not in anchors:
                        errors.append(
                            f"{relative(path)}:{line_number}: missing heading fragment "
                            f"#{fragment} in {relative(target)}"
                        )
                source_record = records.get(path.resolve())
                source_is_conceptual = path == ROOT / "README.md" or (
                    source_record is not None
                    and path.name != "README.md"
                    and source_record[0].get("kind") == "map"
                )
                if source_is_conceptual:
                    incoming_from_conceptual[target].add(path.resolve())

    for directory in archive_directories():
        counts["directories"] += 1
        readme = directory / "README.md"
        if not readme.is_file():
            errors.append(f"{relative(directory)}: missing README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        headings = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
        if directory != ROOT:
            for missing in sorted(REQUIRED_README_HEADINGS - headings):
                errors.append(f"{relative(readme)}: missing section ## {missing}")
            if not re.search(r"^###\s+Subdirectories\s*$", text, re.MULTILINE):
                errors.append(f"{relative(readme)}: missing ### Subdirectories")
            if not re.search(
                r"^###\s+(?:Documents|Files|Templates)\s*$", text, re.MULTILINE
            ):
                errors.append(
                    f"{relative(readme)}: missing ### Documents, ### Files, or ### Templates"
                )
        indexed = links_by_source.get(readme.resolve(), set())
        for child in visible_children(directory):
            expected = (child / "README.md").resolve() if child.is_dir() else child.resolve()
            if expected not in indexed:
                errors.append(
                    f"{relative(readme)}: unindexed direct child {child.name!r}"
                )

    specification_indexes = [SPECIFICATION_ROOT / "README.md"]
    specification_indexes.extend(
        child / "README.md"
        for child in sorted(SPECIFICATION_ROOT.iterdir())
        if child.is_dir() and not is_ignored(child)
    )
    for policy, label in (
        (SPECIFICATION_AUTHORITY_PATH, "SPECIFICATION-AUTHORITY.md"),
        (CONFORMANCE_VOCABULARY_PATH, "CONFORMANCE-VOCABULARY.md"),
    ):
        if not policy.is_file():
            errors.append(f"{label}: missing governance policy")
            continue
        for readme in specification_indexes:
            if readme.is_file():
                errors.extend(
                    policy_link_errors(
                        relative(readme),
                        links_by_source.get(readme.resolve(), set()),
                        policy,
                        label,
                    )
                )

    for area in sorted(
        child
        for child in SPECIFICATION_ROOT.iterdir()
        if child.is_dir() and not is_ignored(child)
    ):
        readme = area / "README.md"
        if readme.is_file() and not re.search(
            r"^## Variability register\s*$",
            readme.read_text(encoding="utf-8"),
            re.MULTILINE,
        ):
            errors.append(f"{relative(readme)}: missing section ## Variability register")
        chapters = [
            records[path.resolve()]
            for path in sorted(area.glob("*.md"))
            if path.name != "README.md" and path.resolve() in records
        ]
        if not chapters:
            errors.append(f"{relative(area)}: specification area has no chapters")
            continue
        if len({metadata.get("spec_version") for metadata, _ in chapters}) != 1:
            errors.append(
                f"{relative(area)}: specification chapters must share one spec_version"
            )
        if len({metadata.get("status") for metadata, _ in chapters}) != 1:
            errors.append(
                f"{relative(area)}: specification chapters must share one status"
            )
        if not any(
            re.search(r"^## Status and authority\s*$", body, re.MULTILINE)
            for _, body in chapters
        ):
            errors.append(
                f"{relative(area)}: specification area lacks a chapter with "
                "## Status and authority"
            )

    completed_paths = set(records)
    for path, (_metadata, _body) in sorted(records.items(), key=lambda item: relative(item[0])):
        if path.name == "README.md":
            continue
        outgoing = {
            target
            for target in links_by_source.get(path, set())
            if target == ROOT / "README.md" or target in completed_paths
        }
        if not outgoing and not incoming_from_conceptual.get(path):
            errors.append(f"{relative(path)}: no conceptual body link or incoming map link")

    identifiers: dict[str, defaultdict[str, list[Path]]] = {
        key: defaultdict(list) for key in ("citation_key", "doi", "url")
    }
    for path, (metadata, _body) in records.items():
        if metadata.get("kind") != "source":
            continue
        counts["source_documents"] += 1
        for key, values in identifiers.items():
            value = metadata.get(key)
            if value:
                values[str(value).casefold()].append(path)
    for key, values in identifiers.items():
        for value, paths in sorted(values.items()):
            if len(paths) > 1:
                joined = ", ".join(relative(path) for path in sorted(paths))
                errors.append(f"duplicate {key} {value!r}: {joined}")

    return sorted(set(errors)), counts


def main() -> int:
    errors, counts = validate()
    if errors:
        print(f"Archive validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Archive validation passed: "
        f"{counts['completed_documents']} completed documents, "
        f"{counts['directories']} directories, "
        f"{counts['local_links']} local links, and "
        f"{counts['source_documents']} source notes checked; "
        f"{counts['specification_documents']} specification chapters and "
        f"{counts['specification_fenced_blocks']} classified fenced blocks checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
