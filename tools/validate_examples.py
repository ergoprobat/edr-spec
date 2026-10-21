"""Validate EDR v0.1 examples against the JSON Schema and the body rules.

YAML dates become ISO strings before validation. The schema file is also
checked against the draft 2020-12 metaschema.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "edr-v0.1.schema.json"
EXAMPLES = ROOT / "examples"
INVALID = ROOT / "conformance" / "invalid"

REQUIRED_HEADINGS = (
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Verification",
)


def fail(message: str) -> None:
    print(message, file=sys.stderr)


def coerce(value: object) -> object:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: coerce(item) for key, item in value.items()}
    if isinstance(value, list):
        return [coerce(item) for item in value]
    return value


def split_frontmatter(text: str, path: Path) -> tuple[object, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: frontmatter must start with ---")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: frontmatter is missing the closing ---")
    raw = text[4:end]
    body = text[end + 5 :]
    loaded = yaml.safe_load(raw)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return coerce(loaded), body


def check_body(body: str, path: Path) -> list[str]:
    lines = body.splitlines()
    errors: list[str] = []
    h1_at = [
        index
        for index, line in enumerate(lines)
        if line.startswith("# ") and not line.startswith("## ")
    ]
    if len(h1_at) != 1:
        errors.append(f"{path}: expected exactly one level-1 heading")
        return errors
    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in lines:
            errors.append(f"{path}: missing heading {heading}")
            positions.append(-1)
        else:
            positions.append(lines.index(heading))
    if errors:
        return errors
    if positions != sorted(positions) or positions[0] < h1_at[0]:
        errors.append(f"{path}: headings are out of order")
        return errors
    bounds = positions + [len(lines)]
    for heading, start, stop in zip(REQUIRED_HEADINGS, positions, bounds[1:]):
        chunk = lines[start + 1 : stop]
        if not any(line.strip() and not line.startswith("#") for line in chunk):
            errors.append(f"{path}: {heading} has no paragraph or list")
    return errors


def document_errors(path: Path, validator: Draft202012Validator) -> list[str]:
    try:
        document, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    for error in validator.iter_errors(document):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{path}: {location}: {error.message}")
    errors.extend(check_body(body, path))
    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        fail(f"{SCHEMA_PATH}: schema must be a JSON object")
        return 1
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail(f"{SCHEMA_PATH}: {exc.message}")
        return 1

    validator = Draft202012Validator(schema)
    paths = sorted(EXAMPLES.glob("*.md"))
    if len(paths) != 20:
        fail(f"{EXAMPLES}: expected 20 examples, found {len(paths)}")
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(document_errors(path, validator))

    invalid_paths = sorted(INVALID.glob("*.md"))
    if not invalid_paths:
        errors.append(f"{INVALID}: expected negative fixtures")
    for path in invalid_paths:
        expect_path = path.with_suffix(".expect")
        if not expect_path.is_file():
            errors.append(f"{path}: missing {expect_path.name}")
            continue
        expected = expect_path.read_text(encoding="utf-8").strip()
        if not expected or "\n" in expected:
            errors.append(f"{expect_path}: expected one line")
            continue
        found = document_errors(path, validator)
        if not found:
            errors.append(f"{path}: expected a failure containing {expected!r}")
            continue
        combined = "\n".join(found)
        if expected not in combined:
            errors.append(f"{path}: failure did not contain {expected!r}: {combined}")

    if errors:
        for message in errors:
            fail(message)
        return 1
    print(
        f"validated {len(paths)} examples and {len(invalid_paths)} invalid fixtures "
        f"against {SCHEMA_PATH.name}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
