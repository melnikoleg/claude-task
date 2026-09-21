---
name: artifact-validator
description: Shared artifact contract for the stargazing workflow - the section templates every artifact must follow and the structural/citation checker that enforces them. Use before writing any artifact under runs/<run-id>/artifacts/ and whenever validating artifacts against quality gates.
allowed-tools: Read, Bash(python3 .claude/skills/artifact-validator/check_artifact.py:*), Glob
---

# Artifact validator

Every artifact is Markdown that humans read and later agents reuse. Same input, same
structure, every run. This skill owns that contract.

## Before you write

1. Read `.claude/skills/artifact-validator/templates/<name>.md`, where `<name>` is your
   artifact's filename without `.md`.
2. Keep every `## ` heading, in the template's order. Add subsections freely; never drop
   or rename a required one.
3. Replace every `<placeholder>` with a real value. Cannot find one? Write the
   limitation as a sentence. Never leave `TODO`, `TBD` or an `<angle-bracket>` stub.
4. End with `## Sources`, at least one http(s) URL. Cite MCP numbers as the call plus
   its arguments, e.g. `astro MCP dark_window(lat=52.23, lon=21.01, date=2026-10-10)`.
   Narrative claims still need a URL.

## After you write

```bash
python3 .claude/skills/artifact-validator/check_artifact.py runs/<run-id>/artifacts/<name>.md
```

Fix everything it reports before finishing your turn. Exit code 0 means structurally
acceptable. The PreToolUse hook blocks the common failures at write time; the checker is
stricter and also enforces the section list and unfilled table rows.

## What the checker enforces

| Check | Rule |
|---|---|
| Title | file starts with a `# ` heading |
| Sections | every `## ` heading from the matching template exists |
| Placeholders | no `TODO`, `TBD`, `FIXME`, `XXX`, `<run-id>` |
| Table rows | no row still holding an `<angle-bracket>` stub |
| Citations | `## Sources` holds at least one http(s) URL |

Structural validity is not correctness. The domain gates in `CLAUDE.md` (budget, cloud,
moon, altitude, drive time) are the validator agent's job.

## Adding an artifact type

Add `templates/<name>.md` with the required `## ` headings. The checker reads the
template directory at runtime; nothing else changes.
