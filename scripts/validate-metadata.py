#!/usr/bin/env python3
"""Validate the public metadata in this repo. No network, no build step.

This repo is metadata only, so nothing here is exercised by a test suite or a
deploy. Every file is read by somebody else's parser - the MCP Registry, a
skill installer, an agent - and a file that does not parse fails silently, in
their runtime, where we never see it.

That is not hypothetical. The SKILL.md frontmatter shipped for weeks as invalid
YAML: the description was an unquoted plain scalar containing "Read-only: ", and
a colon-space terminates a plain scalar. PyYAML, ruamel (YAML 1.2) and js-yaml
all rejected it. It went unnoticed because the one parser we control reads the
frontmatter with a regex, which is lenient, so our own discovery endpoint kept
serving a description that stricter loaders could not read at all.

Run:  python3 scripts/validate-metadata.py
Exit: 0 all good, 1 something is malformed.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "just-domain" / "SKILL.md"

failures: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
    if not ok:
        failures.append(f"{label}{': ' + detail if detail else ''}")


print("JSON")
for rel in ("server.json", ".mcp.json"):
    path = ROOT / rel
    try:
        json.loads(path.read_text(encoding="utf-8"))
        check(True, rel)
    except Exception as exc:  # noqa: BLE001 - report, never raise
        check(False, rel, str(exc))

print("SKILL.md frontmatter")
text = SKILL.read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
check(bool(match), "delimited by --- fences")

if match:
    block = match.group(1)

    # The whole point of this script. A frontmatter that only a lenient parser
    # can read is a frontmatter that strict installers drop on the floor.
    data = None
    try:
        data = yaml.safe_load(block)
        check(True, "parses as YAML (strict)")
    except Exception as exc:  # noqa: BLE001
        check(False, "parses as YAML (strict)", str(exc).splitlines()[0])

    if isinstance(data, dict):
        check("name" in data, "has a name")
        check("description" in data, "has a description")
        check(
            data.get("name") == "just-domain",
            "name matches the package directory",
            f"got {data.get('name')!r}",
        )
        desc = data.get("description")
        check(
            isinstance(desc, str) and desc.strip() != "",
            "description is a non-empty string",
        )
    elif data is not None:
        check(False, "frontmatter is a mapping", f"got {type(data).__name__}")

    # Guardrail, not a style rule. An unquoted value containing ": " is exactly
    # the bug above, and it reads as valid to the naked eye.
    raw = re.search(r"^description:[ \t]*(.+)$", block, re.MULTILINE)
    if raw:
        value = raw.group(1).strip()
        unquoted = not (value.startswith('"') or value.startswith("'"))
        check(
            not (unquoted and re.search(r"\S: ", value)),
            "description with a colon-space is quoted",
            "unquoted plain scalar contains ': ' - wrap the value in quotes",
        )

print()
if failures:
    print(f"{len(failures)} problem(s):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("all metadata valid")
