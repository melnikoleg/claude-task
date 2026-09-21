# Stargazing Night Planner

An agentic Claude Code workflow that plans a stargazing or astrophotography night:
where to go, which night, what to look at, what to pack, what it costs, when to abort.
Output is one standalone HTML guide.

```
/plan-stargazing Plan a stargazing night near Krakow in late October. Two adults,
10x50 binoculars, a car, budget 100 EUR, we want to see Andromeda.
```

Twilight, moon and altitudes come from an `ephem`-backed MCP server; cloud cover from
Open-Meteo; sites, prices and target notes from the web. Nothing is recalled from memory.

## Prerequisites

| Tool | Version | Why |
|---|---|---|
| Claude Code | 2.1+ | agents, skills, hooks |
| Python | 3.10+ | state CLI, hooks, artifact checker |
| uv | recent | runs the astro MCP server with its own dependencies |
| Node.js | 18+ | `npx` runs the Open-Meteo MCP server |

```bash
claude --version && python3 --version && uv --version && node --version
```

## Credentials

None. Both MCP servers are keyless and the workflow reads no private data. No `.env`
to create. `.gitignore` excludes `.claude/settings.local.json` and any `.env*`.

## Setup

```bash
git clone <repo-url> && cd claude-task
python3 scripts/selftest.py
claude
```

`selftest.py` exercises the state CLI, both hooks, the approval gate and the artifact
checker. It ends with `all checks passed`.

On first start, accept the workspace trust prompt and allow the two MCP servers from
`.mcp.json`. Confirm with `claude mcp list`: both `astro` and `open-meteo` must report
connected. The first `astro` start takes a few seconds while `uv` resolves `ephem`.

## Running

```
/plan-stargazing <what you want, where from, when, who is coming, gear, budget>
```

The coordinator asks whatever the request left open, confirms requirements, then runs
the agents. Two decision points:

1. **Confirm requirements** - what it understood, before planning anything.
2. **Approve the plan** - the final HTML cannot be written until you approve. A hook
   enforces that independently of the model.

Everything lands in `runs/<run-id>/`:

```
input.md                  your request and answers
workflow-state.json       stages, artifact hashes, gate results, approval
mcp-log.jsonl             every external data call the plan rests on
artifacts/*.md            one per agent
validation/report-N.md    gate results per cycle
stargazing-guide.html     the final guide
```

The guide is self-contained and works offline.

## Resuming

Nothing is lost if the session dies or a gate blocks the run.

```bash
python3 scripts/state.py list
```

```
/plan-stargazing --resume <run-id>
```

It prints what is done and what remains, then continues at the first unfinished stage.
Completed artifacts are reused. An artifact edited on disk since it was written is
rebuilt, along with everything downstream.

Inspect a run without Claude:

```bash
python3 scripts/state.py resume-plan <run-id>
python3 scripts/state.py show <run-id>
```

## Example runs

`runs/` holds three complete runs: input, artifacts, validation reports, state, MCP
log and guide, so you can read what the workflow did without re-running it.

| Run | Scenario | Demonstrates |
|---|---|---|
| `2026-09-21-warsaw-astrophoto` | Astrophoto weekend near Warsaw, car, 150 EUR | Full agent set, site search, 11 gates passing in one cycle. The astro MCP rejects the requested Milky Way core: it never clears 1 degree from Warsaw in October |
| `2026-09-21-izera-visual` | Fixed site in the Izera Dark-Sky Park, no car, 40 EUR, child in the party | `site-scout` skipped; the observer rejects the first plan and the revision trips two gates (stale budget, targets past the curfew) that a third cycle clears |
| `2026-12-13-berlin-geminids` | Geminids out of Berlin, 25 EUR, cold-weather gap | Interrupted mid-run and resumed from a fresh process: group A reused untouched, group B onward re-ran. Ends NO-GO, the date being beyond the forecast horizon |

Observer answers came from a written scenario rather than live typing, but every
approval passed the same gate: plan shown, decision given, `state.py approve` recording
the hash before any guide existed.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `claude mcp list` shows astro failed | run `uv run --script mcp/astro_server.py` directly; the first run downloads `ephem` |
| `open-meteo` failed | check network, then `npx -y -p open-meteo-mcp-server open-meteo-mcp-server` |
| `open-meteo` fails on certificates | you are behind a TLS-intercepting proxy. Export `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem` before starting Claude Code; `.mcp.json` passes it through. On macOS the intercepting root is usually in the System keychain: `security find-certificate -a -c "<CA name>" -p /Library/Keychains/System.keychain > ca-bundle.pem` |
| Writing the guide is denied | the plan is not approved, or changed after approval |
| An agent cannot write its artifact | missing `## Sources` with a URL, or it contains `TODO` |
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
