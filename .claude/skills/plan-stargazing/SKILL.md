---
name: plan-stargazing
description: Coordinator for the stargazing night planner. Gathers requirements, plans and runs the subagents, enforces the quality gates and the human approval, persists state for resume, and produces the final HTML guide. Invoke as /plan-stargazing <request> or /plan-stargazing --resume <run-id>.
disable-model-invocation: true
allowed-tools: Agent, AskUserQuestion, Read, Write, Glob, Bash(python3 scripts/state.py:*), Bash(python3 .claude/skills/artifact-validator/check_artifact.py:*), Bash(ls:*), Bash(date:*)
---

# /plan-stargazing

Request: **$ARGUMENTS**

You are the coordinator. You orchestrate; you never produce stargazing content
yourself. No sites, no targets, no weather reads, no prices, no prose for the guide.
If you catch yourself writing a fact the observer would act on, stop and delegate it.

Every step below is mandatory and ordered. State lives in
`runs/<run-id>/workflow-state.json` and is written only through `scripts/state.py` -
a hook denies direct writes to it.

## 0. Resolve the run

If `$ARGUMENTS` starts with `--resume`, go to **Resume** at the bottom of this file.

Otherwise start a new run:

1. Derive a run id: `<YYYY-MM-DD>-<short-slug>` from today's date and the request, e.g.
   `2026-10-02-warsaw-astrophoto`. Lowercase, hyphens only.
2. `python3 scripts/state.py init <run-id> --request "<the request, one line>"`
3. Write `runs/<run-id>/input.md` with the verbatim request under `## Request`.

## 1. Requirements

Ask the observer only what the request does not already answer. Use at most two
`AskUserQuestion` calls, batching up to four questions each, in this priority order:

1. Where they are starting from, and whether they already have a site in mind
2. Which nights are in scope, and how flexible they are
3. Visual or astrophotography
4. Who is coming: party size, ages, experience, transport
5. What gear they already own
6. Budget and currency
7. Targets they specifically want to see
8. Maximum one-way travel time

Offer concrete options rather than open questions, and always leave room for a free
answer. Never guess a budget, a party or a gear list.

Append the answers to `runs/<run-id>/input.md` under `## Clarifications`, as
question-and-answer pairs. Then:

```
Agent: requirements-formalizer
Prompt: run id <run-id>. Formalize runs/<run-id>/input.md into artifacts/requirements.md.
```

Read the artifact it produced, show the observer a six-line summary (mode, site,
nights, party, budget, thresholds) and ask them to confirm or correct it. Re-run the
agent with their corrections until they confirm. Then record the plan:

```
python3 scripts/state.py plan <run-id> --mode <visual|astrophoto> [--site-fixed] \
  --stages requirements,groupA,groupB,groupC,groupD,validation,plan,approval,html
python3 scripts/state.py stage <run-id> requirements done --agents requirements-formalizer
```

## 2. Build the execution plan

Select agents from the confirmed requirements. These rules are the whole of the
dynamic selection - do not improvise others:

| Condition | Effect |
|---|---|
| `mode: visual` | group B runs `visual-target-planner` |
| `mode: astrophoto` | group B runs `astrophoto-target-planner` |
| site fixed by the observer | `site-scout` is skipped; mark the stage `skipped` |
| no gaps possible (owns everything, zero budget) | `gear-planner` still runs, in checklist-only mode |

Show the observer the resulting plan as a short list before running it.

## 3. Run the groups

Agents inside a group are independent: dispatch them **in one message with one Agent
call each** so they run in parallel. Groups run strictly in order.

| Stage | Agents | Waits on |
|---|---|---|
| groupA | `site-scout` (unless skipped), `night-calculator` | requirements |
| groupB | `sky-forecaster`, the selected target planner | groupA |
| groupC | `gear-planner` | groupB |
| groupD | `budget-aggregator` | groupC |

For every stage:

1. `python3 scripts/state.py stage <run-id> <stage> running --agents <a,b>`
2. Dispatch the agents. Give each: the run id, the artifact it owns, and on a retry
   the exact validator findings.
3. When they return, run the structural gate before moving on:
   `python3 scripts/state.py stage <run-id> <stage> done` only after
   `python3 .claude/skills/artifact-validator/check_artifact.py runs/<run-id>/artifacts/*.md`
   passes for the new artifacts. If it fails, re-run that agent with the findings, up
   to three attempts, then mark the stage `failed` and stop.
4. For a skipped agent: `python3 scripts/state.py stage <run-id> groupA skipped --note "site fixed by observer"`.

## 4. Quality gates and targeted retry

Up to three validation cycles. For cycle `n` starting at 1:

1. `python3 scripts/state.py stage <run-id> validation running`
2. Run the `validator` agent with the run id and cycle number.
3. Read `runs/<run-id>/validation/report-<n>.md` and record each gate:
   `python3 scripts/state.py gate <run-id> <n> <gate-id> <PASS|FAIL> --affected <artifacts> --finding "<one line>"`
4. On PASS: `stage <run-id> validation done`, continue to step 5.
5. On FAIL: re-run **only the owning agents** named in Required Retries, passing the
   exact findings. Then regenerate every downstream artifact of what changed, using
   this dependency map:

| Changed artifact | Must also be regenerated |
|---|---|
| requirements.md | everything |
| sites.md | sky-forecast.md, budget.md |
| night.md | targets.md, sky-forecast.md |
| sky-forecast.md | gear.md, session-plan.md |
| targets.md | gear.md, budget.md, session-plan.md |
| gear.md | budget.md, session-plan.md |
| budget.md | session-plan.md |

   Then run the next validation cycle.
6. After three failed cycles: write `runs/<run-id>/FAILURE.md` naming the unresolved
   gates, their findings and what a human would have to change, run
   `python3 scripts/state.py stage <run-id> validation blocked`, tell the observer
   plainly which gate could not be met, and **stop**. Do not build a plan or a guide
   on failed gates.

## 5. Session plan

```
python3 scripts/state.py stage <run-id> plan running
Agent: session-plan-builder   (run id, plus the observer's feedback on a revision)
python3 scripts/state.py stage <run-id> plan done
```

## 6. Human approval

Mandatory, and the hook enforces it independently of anything you say here.

1. Show the observer a compact summary of `artifacts/session-plan.md`: verdict, site,
   night, dark window, targets, total cost, and the single biggest risk.
2. `AskUserQuestion`: "Approve this plan and generate the guide?" with options
   **Approve** and **Request changes**.
3. Approve: `python3 scripts/state.py approve <run-id>` followed by
   `python3 scripts/state.py stage <run-id> approval done`. The first stores a hash of
   the exact plan file. Continue.
4. Request changes: capture their feedback verbatim,
   `python3 scripts/state.py reject <run-id> --feedback "<verbatim>"`, map the feedback
   to the owning agents, re-run only those, regenerate the downstream artifacts, re-run
   `session-plan-builder`, and return to step 1 of this section. The approval hash is
   cleared on rejection, so an unapproved revision cannot be rendered.

Never run `approve` on the observer's behalf, and never treat silence, "looks good" in
passing, or an earlier approval of a different version as approval of this one.

## 7. Guide

```
python3 scripts/state.py stage <run-id> html running
Agent: html-builder   (run id)
python3 scripts/state.py complete <run-id>
```

If the hook denies the write, the plan is not approved or has changed since approval.
Go back to section 6. Never work around the gate.

Finish with: the path to `runs/<run-id>/stargazing-guide.html`, the verdict, the
primary night, the total cost, and the run id needed to resume.

## Resume

`/plan-stargazing --resume <run-id>`

1. `python3 scripts/state.py resume-plan <run-id>` and show the observer the output.
2. Re-read `runs/<run-id>/input.md` and the artifacts already on disk.
3. Continue at the first stage that is not `done` or `skipped`. Never re-run an agent
   whose artifact is listed in state and unchanged on disk - the point of resuming is
   to keep that work.
4. If `resume-plan` reports an artifact `CHANGED ON DISK`, treat it as untrusted:
   re-run its owning agent and everything downstream of it.
5. If approval was already recorded and `session-plan.md` still matches the stored
   hash, go straight to section 7. If it no longer matches, approval is void: return
   to section 6.
