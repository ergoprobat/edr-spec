"""Validate EDR examples against the JSON Schema and the body rules.

YAML dates become ISO strings before validation. Draft 0.1 and draft 0.2
schemas are checked against the draft 2020-12 metaschema. The 0.1 corpus
must pass both drafts. Premises fixtures must pass 0.2 and fail 0.1.
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
SCHEMA_V01 = ROOT / "schema" / "edr-v0.1.schema.json"
SCHEMA_V02 = ROOT / "schema" / "edr-v0.2.schema.json"
EXAMPLES = ROOT / "examples"
INVALID = ROOT / "conformance" / "invalid"
V02_EXAMPLES = EXAMPLES / "v0.2"
V02_INVALID = INVALID / "v0.2"
V02_EXAMPLE_NAMES = frozenset({"premise-equals.md", "premise-semver.md"})
V02_INVALID_NAMES = frozenset(
    {
        "two-comparisons.md",
        "no-comparison.md",
        "every-zero.md",
        "every-366.md",
        "twenty-one-premises.md",
        "statement-empty.md",
        "statement-too-long.md",
        "probe-script.md",
        "duplicate-premise-id.md",
        "equals-too-large.md",
        "semver-build.md",
    }
)

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
    # A line that is exactly "---" closes the frontmatter. A later "---" line
    # in the body, including a horizontal rule, stays in the body.
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: frontmatter must start with ---")
    try:
        close = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: frontmatter is missing the closing ---") from exc
    raw = "\n".join(lines[1:close])
    body = "\n".join(lines[close + 1 :])
    if text.endswith("\n"):
        body += "\n"
    loaded = yaml.safe_load(raw)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return coerce(loaded), body


def visible_lines(lines: list[str]) -> list[str]:
    visible: list[str] = []
    fenced = False
    for line in lines:
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        visible.append(line)
    return visible


def check_body(body: str, path: Path) -> list[str]:
    lines = visible_lines(body.splitlines())
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
        found = [index for index, line in enumerate(lines) if line == heading]
        if len(found) > 1:
            errors.append(f"{path}: duplicate heading {heading}")
            continue
        if not found:
            errors.append(f"{path}: missing heading {heading}")
            positions.append(-1)
            continue
        positions.append(found[0])
    if errors:
        return errors
    if positions != sorted(positions) or positions[0] < h1_at[0]:
        errors.append(f"{path}: headings are out of order")
        return errors
    bounds = positions + [len(lines)]
    for heading, start, stop in zip(REQUIRED_HEADINGS, positions, bounds[1:]):
        chunk = lines[start + 1 : stop]
        if not any(is_prose(line) for line in chunk):
            errors.append(f"{path}: {heading} has no paragraph or list")
    return errors


def is_prose(line: str) -> bool:
    trimmed = line.strip()
    if not trimmed or trimmed.startswith("#") or trimmed == "---":
        return False
    return True


def schema_reason(error: object) -> str:
    path = list(getattr(error, "absolute_path", []))
    keyword = getattr(error, "validator", "")
    if keyword == "additionalProperties":
        return "additional-properties"
    if path[:1] == ["status"]:
        return "status"
    if path[:1] == ["owner"]:
        return "owner"
    if path[:1] == ["valid_to"]:
        return "valid_to"
    if path[:1] == ["scope"]:
        return "scope"
    if len(path) >= 3 and path[0] == "sources" and path[2] == "url":
        return "source-url"
    if path[:1] == ["checks"] and keyword == "minItems":
        return "checks-empty"
    if path[:1] == ["checks"] and keyword == "contains":
        if getattr(error, "instance", None) == []:
            return "checks-empty"
        return "checks-deterministic"
    if path[:1] == ["premises"]:
        return "premises"
    return ""


def reason_code(path: Path, error: str) -> str:
    message = error_message(path, error)
    if message == "frontmatter must start with ---":
        return "frontmatter-start"
    if message == "frontmatter is missing the closing ---":
        return "frontmatter-close"
    if message == "frontmatter must be a mapping":
        return "frontmatter-mapping"
    if message == "expected exactly one level-1 heading":
        return "one-h1"
    if message == "headings are out of order":
        return "heading-order"
    if message.startswith("duplicate heading "):
        return "duplicate-heading"
    if message.startswith("missing heading "):
        return "missing-heading"
    if message.endswith("has no paragraph or list"):
        return "section-empty"
    return ""


def error_message(path: Path, error: str) -> str:
    prefix = f"{path}: "
    if error.startswith(prefix):
        return error[len(prefix) :]
    return error


def equals_too_large(document: object) -> bool:
    if not isinstance(document, dict):
        return False
    premises = document.get("premises")
    if not isinstance(premises, list):
        return False
    for item in premises:
        if not isinstance(item, dict):
            continue
        probe = item.get("probe")
        if not isinstance(probe, dict) or "equals" not in probe:
            continue
        encoded = json.dumps(
            probe["equals"], ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        if len(encoded) > 1024:
            return True
    return False


def duplicate_premise_id(document: object) -> bool:
    if not isinstance(document, dict):
        return False
    premises = document.get("premises")
    if not isinstance(premises, list):
        return False
    seen: set[str] = set()
    for item in premises:
        if not isinstance(item, dict):
            continue
        premise_id = item.get("id")
        if not isinstance(premise_id, str):
            continue
        if premise_id in seen:
            return True
        seen.add(premise_id)
    return False


def document_errors(path: Path, validator: Draft202012Validator) -> list[str]:
    try:
        document, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    for error in validator.iter_errors(document):
        code = schema_reason(error)
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{path}: {code}: {location}: {error.message}")
    if duplicate_premise_id(document):
        errors.append(f"{path}: premise-id: premises: duplicate premise id")
    if equals_too_large(document):
        errors.append(f"{path}: premises: premises: equals exceeds 1024 bytes")
    errors.extend(check_body(body, path))
    return errors


def reason_codes(path: Path, errors: list[str]) -> list[str]:
    codes: list[str] = []
    for error in errors:
        code = reason_code(path, error)
        if code == "" and ": " in error:
            # Schema errors store the code between the path and the location.
            parts = error.split(": ", 2)
            if len(parts) == 3 and parts[1]:
                code = parts[1]
        if code:
            codes.append(code)
    return codes


def load_validator(schema_path: Path) -> tuple[Draft202012Validator | None, list[str]]:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"{schema_path}: {exc.msg}"]
    if not isinstance(schema, dict):
        return None, [f"{schema_path}: schema must be a JSON object"]
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return None, [f"{schema_path}: {exc.message}"]
    return Draft202012Validator(schema), []


def check_valid(validator: Draft202012Validator, paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        errors.extend(document_errors(path, validator))
    return errors


def check_invalid(validator: Draft202012Validator, directory: Path) -> list[str]:
    errors: list[str] = []
    invalid_paths = sorted(directory.glob("*.md"))
    if not invalid_paths:
        return [f"{directory}: expected negative fixtures"]
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
        codes = reason_codes(path, found)
        if set(codes) != {expected}:
            errors.append(f"{path}: reasons {codes} != {expected!r}")
    return errors


def named_markdown(directory: Path, expected: frozenset[str]) -> tuple[list[Path], list[str]]:
    found = {path.name for path in directory.glob("*.md")}
    if found != expected:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        return [], [f"{directory}: names missing {missing} extra {extra}"]
    return sorted(directory.glob("*.md")), []


def main() -> int:
    errors: list[str] = []
    validator_v01, load_errors = load_validator(SCHEMA_V01)
    errors.extend(load_errors)
    validator_v02, load_errors = load_validator(SCHEMA_V02)
    errors.extend(load_errors)
    if validator_v01 is None or validator_v02 is None:
        for message in errors:
            fail(message)
        return 1

    examples = sorted(EXAMPLES.glob("*.md"))
    if len(examples) != 21:
        errors.append(f"{EXAMPLES}: expected 21 examples, found {len(examples)}")
    else:
        errors.extend(check_valid(validator_v01, examples))
        errors.extend(check_valid(validator_v02, examples))

    shared_invalid = sorted(INVALID.glob("*.md"))
    if not shared_invalid:
        errors.append(f"{INVALID}: expected negative fixtures")
    else:
        errors.extend(check_invalid(validator_v01, INVALID))
        errors.extend(check_invalid(validator_v02, INVALID))

    v02_examples, name_errors = named_markdown(V02_EXAMPLES, V02_EXAMPLE_NAMES)
    errors.extend(name_errors)
    if v02_examples:
        errors.extend(check_valid(validator_v02, v02_examples))
        for path in v02_examples:
            found = document_errors(path, validator_v01)
            codes = reason_codes(path, found)
            if set(codes) != {"additional-properties"}:
                errors.append(
                    f"{path}: draft 0.1 reasons {codes} != 'additional-properties'"
                )

    v02_invalid, name_errors = named_markdown(V02_INVALID, V02_INVALID_NAMES)
    errors.extend(name_errors)
    if v02_invalid:
        errors.extend(check_invalid(validator_v02, V02_INVALID))

    if errors:
        for message in errors:
            fail(message)
        return 1
    print(
        f"validated {len(examples)} examples and {len(shared_invalid)} invalid fixtures "
        f"against {SCHEMA_V01.name} and {SCHEMA_V02.name}; "
        f"validated {len(v02_examples)} v0.2 examples and {len(v02_invalid)} v0.2 invalid fixtures"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
