---
name: stargazing-html-theme
description: Rendering rules and the standalone dark-sky HTML template for the final stargazing guide. Use when converting an approved session plan into runs/<run-id>/stargazing-guide.html, or when restyling that page.
allowed-tools: Read, Write
---

# Stargazing guide HTML theme

Renders `artifacts/session-plan.md` as one self-contained page. Same plan in, same
page out - section order and ids are fixed so two runs are comparable.

## Rules

1. Start from `.claude/skills/stargazing-html-theme/template.html`. Do not restructure
   it: keep every `<section>`, its `id`, and the order Summary, Site, Night and Sky,
   Timeline, Targets, Gear Checklist, Budget, Go / No-Go, Safety, Sources.
2. Replace each `{{PLACEHOLDER}}` with rendered HTML. A section with nothing to say
   gets one honest sentence, never an empty block and never a removed section.
3. Single file. All CSS stays inline in `<head>`. No external scripts, fonts, images
   or network requests - the page has to work offline in a field with no signal.
4. Content comes only from the approved `session-plan.md`. Rendering is a format
   change, not an edit: no new numbers, no new recommendations, no dropped warnings.
5. Every link in the plan survives into the page as a real `<a href>`.

## Placeholders

| Placeholder | Fill with |
|---|---|
| `{{TITLE}}` | `Stargazing - <site short name>, <night date>` |
| `{{SUBTITLE}}` | observer, mode, drive time, dark window in local time |
| `{{VERDICT}}` | `GO - <primary night>` or `NO-GO - use backup <date>` |
| `{{VERDICT_CLASS}}` | `go` or `nogo` |
| `{{SUMMARY}}` | the plan's Summary paragraph |
| `{{KEY_STATS}}` | 4 to 6 `<div class="stat"><div class="k">Label</div><div class="v">Value</div></div>` tiles: dark window, moon illumination, mean cloud, drive time, total cost, target count |
| `{{SITE}}` … `{{SAFETY}}` | that section of the plan as HTML |
| `{{SOURCES}}` | `<ul>` of links grouped by artifact |
| `{{FOOTER_NOTE}}` | run id, generation date, and that the forecast needs rechecking on the day |

## Markup conventions

- Tables in the plan become `<table>` with a `<thead>`; never a `<pre>` block.
- The gear checklist uses `<ul class="check">` so every line has a tick box.
- Abort rules and hazards go in `<div class="warn">`.
- Prose blocks that are not tables or lists are wrapped in `<div class="card">`.
- Escape `&`, `<`, `>` inside content.

## Before you finish

Re-read the written file and confirm: no `{{` remains, every section present, the
verdict class matches the verdict text, and every source is a clickable link.
