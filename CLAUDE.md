# Stargazing Night Planner

Turns "I want to see Andromeda sometime in October" into a field-ready plan: where to
stand, which night, what is visible, what to carry, what it costs, when to call it off.

Astronomy punishes guessing. Twilight, moon and altitude come from an MCP server;
cloud cover from a forecast API. No number in a guide is one the model remembered.

## Architecture

Hub and spoke: one coordinator, eleven subagents, each owning one artifact. The
coordinator plans, dispatches, gates and enforces approval. It writes no content.

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

Agents in a group are dispatched in one message and run in parallel. Groups are
sequential: each needs the previous group's artifacts.

## Artifacts

Markdown under `runs/<run-id>/artifacts/`. Structure is fixed by the templates in
`.claude/skills/artifact-validator/templates/`.

| Artifact | Owner | Regenerate downstream if it changes |
|---|---|---|
| `requirements.md` | requirements-formalizer | everything |
| `sites.md` | site-scout | sky-forecast.md, budget.md |
| `night.md` | night-calculator | targets.md, sky-forecast.md |
| `sky-forecast.md` | sky-forecaster | gear.md, session-plan.md |
| `targets.md` | visual- or astrophoto-target-planner | gear.md, budget.md, session-plan.md |
| `gear.md` | gear-planner | budget.md, session-plan.md |
| `budget.md` | budget-aggregator | session-plan.md |
| `session-plan.md` | session-plan-builder | stargazing-guide.html |

Every artifact ends with `## Sources`: at least one http(s) URL plus the MCP calls
behind its numbers. Model knowledge is not a source.

## Dynamic agent selection

The coordinator picks the agent set from confirmed requirements. These are the only
selection rules:

| Condition | Effect |
|---|---|
| `mode: visual` | `visual-target-planner` runs, the astrophoto one does not |
| `mode: astrophoto` | `astrophoto-target-planner` runs, the visual one does not |
| observer named a specific site | `site-scout` skipped, stage marked `skipped` |
| owns everything, no budget | `gear-planner` runs in checklist-only mode |

## Quality gates

`validator` judges and never repairs. Gates G1-G11 live in `.claude/agents/validator.md`:
artifact structure, budget, travel time, usable sky, moon, target altitude, duplicate
targets, gear consistency, sourced recommendations, site legality, mode honoured.

A NO-GO plan passes if the no-go is explicit and a backup night is named. Hiding bad
weather behind an optimistic plan is what the gates exist to catch.

### Retry policy

On failure the coordinator re-runs only the agents in the report's Required Retries,
regenerates their downstream artifacts, revalidates. Three cycles maximum. Then it
writes `runs/<run-id>/FAILURE.md`, marks validation `blocked`, reports the gate and
stops. Dependent work does not proceed on failed gates.

## Human approval

Two independent mechanisms, because an instruction alone is not a gate:

1. The coordinator shows the plan, asks, then runs `python3 scripts/state.py approve
   <run-id>`, storing a SHA-256 of the exact `session-plan.md` shown.
2. A `PreToolUse` hook denies any write to `runs/*/*.html` unless state says `approved`
   and the plan still hashes to that value. Editing after approval voids it.

Rejection clears the hash, records the feedback, sends the run through a targeted revision.

## State and resume

`runs/<run-id>/workflow-state.json` holds status, plan, per-stage status and attempts,
artifact hashes, gate results, approval and the MCP call count. `scripts/state.py` is
its only writer; the PreToolUse hook denies direct writes so state cannot drift.

`/plan-stargazing --resume <run-id>` prints `resume-plan`, continues at the first stage
that is not `done` or `skipped`, and never re-runs an agent whose artifact is recorded
and unchanged. An artifact reported `CHANGED ON DISK` is untrusted: its agent and
everything downstream re-run.

## Skills

- `artifact-validator` - section templates plus `check_artifact.py`, which derives
  required sections from them. Used by every content agent and by the validator.
- `stargazing-html-theme` - fixed section order, placeholder table and the standalone
  dark-sky `template.html`. Used by `html-builder`.

## Hooks

In `.claude/settings.json`, fired for subagent tool calls too.

| Event | Script | Enforces |
|---|---|---|
| PreToolUse on writes | `pre_tool_guard.py` | no final HTML without a matching approval hash; `workflow-state.json` only via `state.py`; no artifact without a `## Sources` URL; no `TODO` placeholders |
| PostToolUse on writes | `post_tool_state.py` | records each artifact's hash, timestamp and authoring agent |
| PostToolUse on MCP calls | `post_tool_state.py` | appends every astro and open-meteo call to `runs/<run-id>/mcp-log.jsonl` |

## MCP servers

`.mcp.json`, both keyless:

- `astro` - custom, `mcp/astro_server.py`, run by `uv`. `dark_window`, `moon_info`,
  `object_visibility`, `list_catalog`, computed with `ephem`.
- `open-meteo` - community `open-meteo-mcp-server`. `geocoding`, `elevation`,
  `weather_forecast` with hourly cloud, wind, temperature and dew point.

Agents also have `WebSearch` and `WebFetch` for sites, prices and target references.

## Rules for extending this

- The coordinator writes no stargazing content. Add a subagent instead.
- One agent, one artifact. Two agents writing one file means the split is wrong.
- A new artifact type needs a template in
  `.claude/skills/artifact-validator/templates/`; the checker picks it up.
- Compute what can be computed. Reach for the astro MCP before prose.
- Run `python3 scripts/selftest.py` after touching hooks, `state.py` or the checker.
