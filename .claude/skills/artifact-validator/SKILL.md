---
name: artifact-validator
description: Shared artifact contract for the stargazing workflow - the section templates every artifact must follow and the structural/citation checker that enforces them. Use before writing any artifact under runs/<run-id>/artifacts/ and whenever validating artifacts against quality gates.
allowed-tools: Read, Bash(python3 .claude/skills/artifact-validator/check_artifact.py:*), Glob
---

# Artifact validator

Every artifact in this workflow is a Markdown file that humans read and later agents
reuse. Same input, same structure, every run. This skill owns that contract.

## Before you write an artifact

1. Read the template for your artifact: `.claude/skills/artifact-validator/templates/<name>.md`
   where `<name>` is your artifact's filename without `.md`.
2. Keep every `## ` heading, in the template's order. Add subsections freely; never
   drop or rename a required one.
3. Replace every `<placeholder>` with a real value. If a value cannot be found, write
   the limitation as a sentence. Never leave `TODO`, `TBD` or an `<angle-bracket>` stub.
4. End with `## Sources`. At least one http(s) URL. MCP-derived numbers are cited as
   the tool call plus its arguments, e.g.
   `astro MCP dark_window(lat=52.23, lon=21.01, date=2026-10-10)` - and any narrative
   claim still needs a URL.

## After you write an artifact

Run the checker on it and fix anything it reports before you finish your turn:

```bash
python3 .claude/skills/artifact-validator/check_artifact.py runs/<run-id>/artifacts/<name>.md
```

Exit code 0 means the artifact is structurally acceptable. The PreToolUse hook blocks
the most common failures at write time, but the checker is stricter: it also enforces
the section list, unfilled table rows and body length.

## What the checker enforces

| Check | Rule |
|---|---|
| Title | file starts with a `# ` heading |
| Sections | every `## ` heading present in the matching template exists |
| Placeholders | no `TODO`, `TBD`, `FIXME`, `XXX`, `<run-id>` |
| Table rows | no row still containing an `<angle-bracket>` stub |
| Citations | `## Sources` contains at least one http(s) URL |
| Substance | body is at least 40 words |

Structural validity is not correctness. The domain gates in `CLAUDE.md` (budget,
cloud cover, moon, altitude, drive time) are the validator agent's job.

## Adding an artifact type

Add `templates/<name>.md` with the required `## ` headings. The checker reads the
template directory at runtime, so nothing else needs to change.
