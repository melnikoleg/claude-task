---
name: plan-stargazing
description: Coordinator for the stargazing night planner. Gathers requirements, plans and runs the subagents, enforces the quality gates and the human approval, persists state for resume, and produces the final HTML guide. Invoke as /plan-stargazing <request> or /plan-stargazing --resume <run-id>.
disable-model-invocation: true
allowed-tools: Agent, AskUserQuestion, Read, Write, Glob, Bash(python3 scripts/state.py:*), Bash(python3 .claude/skills/artifact-validator/check_artifact.py:*), Bash(ls:*), Bash(date:*)
---

# /plan-stargazing

Request: **$ARGUMENTS**

You orchestrate; you never write stargazing content. No sites, targets, weather reads,
prices or guide prose. Catch yourself writing a fact the observer would act on, and
delegate it instead.

Every step is mandatory and ordered. State lives in `runs/<run-id>/workflow-state.json`
and is written only through `scripts/state.py`; a hook denies direct writes.

## 0. Resolve the run

`$ARGUMENTS` starting with `--resume` jumps to **Resume** at the bottom. Otherwise:

1. Derive a run id: `<YYYY-MM-DD>-<short-slug>`, lowercase and hyphens, e.g.
   `2026-10-02-warsaw-astrophoto`.
2. `python3 scripts/state.py init <run-id> --request "<the request, one line>"`
3. Write `runs/<run-id>/input.md` with the verbatim request under `## Request`.

## 1. Requirements

Ask only what the request does not answer. At most two `AskUserQuestion` calls, up to
four questions each, in this priority order:

1. Start point, and whether they already have a site in mind
2. Which nights, and how flexible
3. Visual or astrophotography
4. Party size, ages, experience, transport
5. Gear they own
6. Budget and currency
7. Targets they specifically want
8. Maximum one-way travel time

Offer concrete options, always leave room for a free answer, never guess a budget,
party or gear list.

Append the answers to `runs/<run-id>/input.md` under `## Clarifications` as
question-and-answer pairs. Then:

```
Agent: requirements-formalizer
Prompt: run id <run-id>. Formalize runs/<run-id>/input.md into artifacts/requirements.md.
```

Read the artifact, show a six-line summary (mode, site, nights, party, budget,
thresholds), and ask the observer to confirm or correct. Re-run until they confirm:

```
python3 scripts/state.py plan <run-id> --mode <visual|astrophoto> [--site-fixed] \
  --stages requirements,groupA,groupB,groupC,groupD,validation,plan,approval,html
python3 scripts/state.py stage <run-id> requirements done --agents requirements-formalizer
```

## 2. Build the execution plan

Select agents from the confirmed requirements. These rules are the whole of the dynamic
selection; do not improvise others:

| Condition | Effect |
|---|---|
| `mode: visual` | group B runs `visual-target-planner` |
| `mode: astrophoto` | group B runs `astrophoto-target-planner` |
| site fixed by the observer | `site-scout` skipped, stage marked `skipped` |
| owns everything, zero budget | `gear-planner` runs in checklist-only mode |

Show the observer the resulting plan before running it.

## 3. Run the groups

Agents inside a group are independent: dispatch them **in one message, one Agent call
each**, so they run in parallel. Groups run in order.

| Stage | Agents | Waits on |
|---|---|---|
| groupA | `site-scout` (unless skipped), `night-calculator` | requirements |
| groupB | `sky-forecaster`, the selected target planner | groupA |
| groupC | `gear-planner` | groupB |
| groupD | `budget-aggregator` | groupC |

Per stage:

1. `python3 scripts/state.py stage <run-id> <stage> running --agents <a,b>`
2. Dispatch, giving each agent the run id, the artifact it owns, and on a retry the
   exact validator findings.
3. Mark `done` only after
   `python3 .claude/skills/artifact-validator/check_artifact.py runs/<run-id>/artifacts/*.md`
   passes for the new artifacts. On failure re-run that agent with the findings, up to
   three attempts, then mark the stage `failed` and stop.
4. Skipped agent: `python3 scripts/state.py stage <run-id> groupA skipped --note "site fixed by observer"`.

## 4. Quality gates and targeted retry

Up to three cycles. For cycle `n` from 1:

1. `python3 scripts/state.py stage <run-id> validation running`
2. Run `validator` with the run id and cycle number.
3. Read `runs/<run-id>/validation/report-<n>.md`, record each gate:
   `python3 scripts/state.py gate <run-id> <n> <gate-id> <PASS|FAIL> --affected <artifacts> --finding "<one line>"`
4. PASS: `stage <run-id> validation done`, go to step 5.
5. FAIL: re-run **only the owning agents** from Required Retries with the exact
   findings, then regenerate every downstream artifact:

| Changed artifact | Also regenerate |
|---|---|
| requirements.md | everything |
| sites.md | sky-forecast.md, budget.md |
| night.md | targets.md, sky-forecast.md |
| sky-forecast.md | gear.md, session-plan.md |
| targets.md | gear.md, budget.md, session-plan.md |
| gear.md | budget.md, session-plan.md |
| budget.md | session-plan.md |

   Then run the next cycle.
6. After three failed cycles: write `runs/<run-id>/FAILURE.md` with the unresolved
   gates, their findings and what a human would have to change, run
   `python3 scripts/state.py stage <run-id> validation blocked`, name the gate that
   could not be met, and **stop**. Never build a plan or guide on failed gates.

## 5. Session plan

```
python3 scripts/state.py stage <run-id> plan running
Agent: session-plan-builder   (run id, plus the observer's feedback on a revision)
python3 scripts/state.py stage <run-id> plan done
```

## 6. Human approval

Mandatory, and the hook enforces it independently of anything written here.

1. Show a compact summary of `artifacts/session-plan.md`: verdict, site, night, dark
   window, targets, total cost, biggest risk.
2. `AskUserQuestion`: "Approve this plan and generate the guide?" with **Approve** and
   **Request changes**.
3. Approve: `python3 scripts/state.py approve <run-id>` then
   `python3 scripts/state.py stage <run-id> approval done`. The first stores a hash of
   the exact plan file.
4. Request changes: capture the feedback verbatim, `python3 scripts/state.py reject
   <run-id> --feedback "<verbatim>"`, map it to the owning agents, re-run only those,
   regenerate downstream, re-run `session-plan-builder`, return to step 1. Rejection
   clears the hash, so an unapproved revision cannot be rendered.

Never approve on the observer's behalf. Silence, a passing "looks good", or approval of
an earlier version is not approval of this one.

## 7. Guide

```
python3 scripts/state.py stage <run-id> html running
Agent: html-builder   (run id)
python3 scripts/state.py complete <run-id>
```

A denied write means the plan is unapproved or changed since approval: return to
section 6, never work around the gate.

Finish with the path to `runs/<run-id>/stargazing-guide.html`, the verdict, the primary
night, the total cost and the run id needed to resume.

## Resume

`/plan-stargazing --resume <run-id>`

1. `python3 scripts/state.py resume-plan <run-id>`, and show the observer the output.
2. Re-read `runs/<run-id>/input.md` and the artifacts on disk.
3. Continue at the first stage that is not `done` or `skipped`. Never re-run an agent
   whose artifact is recorded and unchanged: keeping that work is the point.
4. An artifact reported `CHANGED ON DISK` is untrusted: re-run its owning agent and
   everything downstream.
5. If approval is recorded and `session-plan.md` still matches the stored hash, go
   straight to section 7. If it no longer matches, approval is void: return to section 6.
