# Stargazing Night Planner

An agentic workflow for Claude Code that plans a stargazing or astrophotography
night: where to go, which night, what to look at, what to pack, what it costs, and
when to call it off. The output is a single standalone HTML guide.

```
/plan-stargazing Plan a stargazing night near Krakow in late October. Two adults,
we have 10x50 binoculars and a car, budget 100 EUR, we want to see Andromeda.
```

Twilight, moon and object altitudes come from an `ephem`-backed MCP server; cloud
cover comes from Open-Meteo; sites, prices and target notes come from the web. The
model is not asked to remember any of it.

## Prerequisites

| Tool | Version | Why |
|---|---|---|
| Claude Code | 2.1 or newer | agents, skills, hooks |
| Python | 3.10 or newer | state CLI, hooks, artifact checker |
| uv | any recent | runs the custom astro MCP server with its own dependencies |
| Node.js | 18 or newer | `npx` runs the Open-Meteo MCP server |

Check them:

```bash
claude --version && python3 --version && uv --version && node --version
```

## Credentials

None. Both MCP servers are keyless, and the workflow reads no private data. There is
no `.env` to create and no secret to store. `.gitignore` excludes
`.claude/settings.local.json` and any `.env*` so local overrides never get committed.

## Setup from a clean checkout

```bash
git clone <repo-url> && cd claude-task
python3 scripts/selftest.py
claude
```

`selftest.py` exercises the state CLI, both hooks, the approval gate and the artifact
checker. It should end with `all checks passed`.

On the first `claude` start, accept the workspace trust prompt and allow the two
project MCP servers from `.mcp.json`. Confirm they connected:

```bash
claude mcp list
```

Both `astro` and `open-meteo` must report connected. The first `astro` start takes a
few seconds while `uv` resolves `ephem`.

## Running a plan

```
/plan-stargazing <what you want, where from, when, who is coming, gear, budget>
```

The coordinator asks for whatever the request left open, confirms the requirements
with you, then runs the agents. Expect two decision points:

1. **Confirm requirements** - it shows what it understood before planning anything.
2. **Approve the plan** - it shows the session plan and asks. The final HTML cannot be
   written until you approve; a hook enforces that independently of the model.

Everything lands in `runs/<run-id>/`:

```
runs/2026-10-02-warsaw-astrophoto/
  input.md                  your request and answers
  workflow-state.json       stages, artifact hashes, gate results, approval
  mcp-log.jsonl             every external data call the plan rests on
  artifacts/*.md            one per agent
  validation/report-N.md    quality gate results per cycle
  stargazing-guide.html     the final guide
```

Open the guide in any browser. It is self-contained and works offline.

## Resuming an interrupted run

Nothing is lost if the session dies, you close the terminal, or a gate blocks the run.

```bash
python3 scripts/state.py list          # what runs exist and where each stands
```

```
/plan-stargazing --resume <run-id>
```

It prints what is done and what remains, then continues at the first unfinished stage.
Completed artifacts are reused, not regenerated. If an artifact was edited on disk
since it was written, that artifact and everything downstream are rebuilt.

Inspect a run without Claude:

```bash
python3 scripts/state.py resume-plan <run-id>
python3 scripts/state.py show <run-id>
```

## Example runs

`runs/` contains three complete runs kept in version control, covering an
astrophotography trip, a fixed-site visual night with a retry, and a bright-moon
request that goes through a rejection and a resume. Each has its input, artifacts,
validation reports, state and final guide.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `claude mcp list` shows astro failed | run `uv run --script mcp/astro_server.py` directly; the first run downloads `ephem` |
| `open-meteo` failed | check network, then `npx -y -p open-meteo-mcp-server open-meteo-mcp-server` |
| Writing the guide is denied | the plan is not approved, or it changed after approval; approve the current version |
| An agent cannot write its artifact | it is missing `## Sources` with a URL, or still contains `TODO` |
| State looks wrong | `python3 scripts/state.py show <run-id>`; never edit the JSON by hand, the hook blocks it |

## Layout

```
CLAUDE.md                     workflow rules and architecture
.mcp.json                     both MCP servers
.claude/skills/               coordinator + 2 reusable skills
.claude/agents/               11 subagents
.claude/hooks/                PreToolUse and PostToolUse guards
.claude/settings.json         hook wiring and permissions
mcp/astro_server.py           custom astronomy MCP server
scripts/state.py              workflow state CLI
scripts/selftest.py           checks hooks, state and gates
runs/                         one directory per run
```
