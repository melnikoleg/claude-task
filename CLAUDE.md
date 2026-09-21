# Stargazing Night Planner

An agentic workflow that turns "I want to see the Andromeda Galaxy sometime in
October" into a field-ready plan: where to stand, which night, what will be visible,
what to carry, what it costs, and when to call it off.

Astronomy punishes guessing. Twilight times, moon illumination and object altitude are
computed by an MCP server, and cloud cover comes from a forecast API. No number in a
final guide is a number the model remembered.

## Architecture

Hub and spoke. One coordinator, eleven single-purpose subagents, each owning exactly
one artifact. The coordinator plans, dispatches, gates, and enforces approval. It
produces no stargazing content itself.

```
/plan-stargazing
  requirements-formalizer
  groupA  ||  site-scout          night-calculator
  groupB  ||  sky-forecaster      visual|astrophoto-target-planner
  groupC      gear-planner
  groupD      budget-aggregator
  validation  validator            -> targeted retry, max 3 cycles
  plan        session-plan-builder
  approval    human                -> revision loop on reject
  html        html-builder         -> runs/<run-id>/stargazing-guide.html
```

Agents within a group are dispatched in a single message so they run in parallel.
Groups are strictly sequential because each needs the previous group's artifacts.

## Artifacts

All artifacts are Markdown under `runs/<run-id>/artifacts/`. They are read by humans
and by later agents, so structure is fixed by the templates in
`.claude/skills/artifact-validator/templates/`.

| Artifact | Owner | Downstream artifacts to regenerate if it changes |
|---|---|---|
| `requirements.md` | requirements-formalizer | everything |
| `sites.md` | site-scout | sky-forecast.md, budget.md |
| `night.md` | night-calculator | targets.md, sky-forecast.md |
| `sky-forecast.md` | sky-forecaster | gear.md, session-plan.md |
| `targets.md` | visual- or astrophoto-target-planner | gear.md, budget.md, session-plan.md |
| `gear.md` | gear-planner | budget.md, session-plan.md |
| `budget.md` | budget-aggregator | session-plan.md |
| `session-plan.md` | session-plan-builder | stargazing-guide.html |

Every artifact ends with `## Sources`, carrying at least one http(s) URL plus the MCP
calls behind its numbers. Internal model knowledge is not a source.

## Dynamic agent selection

The coordinator picks the agent set from the confirmed requirements. These are the
only selection rules:

| Condition | Effect |
|---|---|
| `mode: visual` | `visual-target-planner` runs; the astrophoto one does not |
| `mode: astrophoto` | `astrophoto-target-planner` runs; the visual one does not |
| observer named a specific observing site | `site-scout` is skipped, stage marked `skipped` |
| observer owns everything and has no budget | `gear-planner` runs in checklist-only mode |

## Quality gates

The `validator` agent judges and never repairs. Gates G1-G11 are defined in
`.claude/agents/validator.md`; in short: artifact structure, budget within limit,
travel within limit, usable sky, moon respected, targets observable, no duplicate
targets, gear consistent with owned gear, every recommendation sourced, site legally
usable, and the confirmed mode honoured.

A NO-GO plan passes, provided the no-go is stated explicitly and a backup night is
named. Hiding bad weather behind an optimistic plan is the failure mode the gates
exist to catch.

### Retry policy

On failure the coordinator re-runs only the agents named in the report's Required
Retries, then regenerates the downstream artifacts from the table above, then
revalidates. Three cycles maximum. After three, the coordinator writes
`runs/<run-id>/FAILURE.md`, marks the validation stage `blocked`, reports which gate
could not be met, and stops. Dependent work does not proceed on failed gates.

## Human approval

Two independent mechanisms, because an instruction alone is not a gate:

1. The coordinator must show the plan and ask, then run
   `python3 scripts/state.py approve <run-id>`, which stores a SHA-256 of the exact
   `session-plan.md` that was shown.
2. A `PreToolUse` hook denies any write to `runs/*/*.html` unless the state says
   `approved` and the plan file still hashes to the stored value. Editing the plan
   after approval voids it.

Rejection clears the hash, records the feedback, and sends the run back through a
targeted revision.

## State and resume

`runs/<run-id>/workflow-state.json` holds the run status, plan, per-stage status and
attempt counts, artifact hashes, gate results, approval status and the MCP call count.
`scripts/state.py` is its only writer; the PreToolUse hook denies direct writes so the
state cannot drift from what actually happened.

`/plan-stargazing --resume <run-id>` prints `resume-plan`, continues at the first
stage that is not `done` or `skipped`, and never re-runs an agent whose artifact is
recorded and unchanged. An artifact reported `CHANGED ON DISK` is untrusted: its agent
and everything downstream re-run.

## Skills

- `artifact-validator` - the artifact contract: section templates plus
  `check_artifact.py`, which derives required sections from the templates. Used by
  every content agent before finishing and by the validator.
- `stargazing-html-theme` - the rendering contract: fixed section order, placeholder
  table and the standalone dark-sky `template.html`. Used by `html-builder`.

## Hooks

Configured in `.claude/settings.json`, fired for subagent tool calls as well.

| Event | Script | What it enforces |
|---|---|---|
| PreToolUse on writes | `.claude/hooks/pre_tool_guard.py` | no final HTML without a matching approval hash; `workflow-state.json` only via `state.py`; no artifact without a `## Sources` URL; no `TODO`/`TBD` placeholders |
| PostToolUse on writes | `.claude/hooks/post_tool_state.py` | records each artifact's hash, timestamp and authoring agent into the state; marks the run complete when the guide is written |
| PostToolUse on MCP calls | `.claude/hooks/post_tool_state.py` | appends every astro and open-meteo call to `runs/<run-id>/mcp-log.jsonl` as evidence the plan rests on external data |

## MCP servers

`.mcp.json`, both keyless:

- `astro` - custom, `mcp/astro_server.py`, run by `uv` with inline dependencies.
  `dark_window`, `moon_info`, `object_visibility`, `list_catalog`. Computed with
  `ephem`, so twilight, moon and altitude are real ephemeris values.
- `open-meteo` - community server `open-meteo-mcp-server`. `geocoding`, `elevation`,
  `weather_forecast` with hourly cloud, wind, temperature and dew point.

Agents also have `WebSearch` and `WebFetch` for sites, prices and target references.

## Rules for anyone extending this

- The coordinator never writes stargazing content. Add a subagent instead.
- One agent, one artifact. If two agents would write the same file, the split is wrong.
- A new artifact type needs a template in
  `.claude/skills/artifact-validator/templates/`; the checker picks it up with no code
  change.
- Numbers that can be computed are computed. Reach for the astro MCP before prose.
- Run `python3 scripts/selftest.py` after touching hooks, `state.py` or the checker.
