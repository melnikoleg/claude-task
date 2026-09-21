#!/usr/bin/env python3
"""Structural + citation check for workflow artifacts.

The required section list for each artifact type is read from the template beside
this file, so templates/ is the single source of truth: change a template and the
check follows. Usage:

    python3 .claude/skills/artifact-validator/check_artifact.py <file> [<file> ...]
    python3 .claude/skills/artifact-validator/check_artifact.py runs/<id>/artifacts/*.md

Exit code 0 = all files pass, 1 = at least one finding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent / "templates"
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b|<run-id>", re.I)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.M)
H1 = re.compile(r"^#\s+\S", re.M)
URL = re.compile(r"https?://\S+")
# A placeholder row the agent forgot to replace: | <something> | <something> |
UNFILLED_ROW = re.compile(r"^\|.*<[a-z][^>\n]*>.*$", re.M | re.I)


def required_sections(kind: str) -> list[str] | None:
    tpl = TEMPLATES / f"{kind}.md"
    if not tpl.is_file():
        return None
    return HEADING.findall(tpl.read_text())


def check(path: Path) -> list[str]:
    kind = path.stem
    findings: list[str] = []
    text = path.read_text()

    wanted = required_sections(kind)
    if wanted is None:
        known = ", ".join(sorted(x.stem for x in TEMPLATES.glob("*.md")))
        return [f"unknown artifact type {kind!r}; templates exist for: {known}"]

    if not H1.search(text):
        findings.append("missing a top-level `# ` title")

    present = {h.strip().lower() for h in HEADING.findall(text)}
    for section in wanted:
        if section.strip().lower() not in present:
            findings.append(f"missing required section `## {section}`")

    if m := PLACEHOLDER.search(text):
        findings.append(f"placeholder {m.group(0)!r} left in the artifact")

    row = UNFILLED_ROW.search(text)
    if row:
        findings.append(f"unfilled template row: {row.group(0).strip()[:70]}")

    m = re.search(r"^##\s+Sources\s*$", text, re.M)
    if m and not URL.search(text[m.end():]):
        findings.append("`## Sources` lists no http(s) URL - every artifact must cite external evidence")

    return findings


def main() -> None:
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        sys.exit("usage: check_artifact.py <artifact.md> [...]")
    failed = False
    for p in paths:
        if not p.is_file():
            print(f"FAIL {p}: file does not exist")
            failed = True
            continue
        findings = check(p)
        if findings:
            failed = True
            print(f"FAIL {p}")
            for f in findings:
                print(f"     - {f}")
        else:
            print(f"PASS {p}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
