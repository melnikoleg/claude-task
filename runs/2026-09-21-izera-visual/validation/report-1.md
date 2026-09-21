# Validation Report - cycle 1

## Verdict
PASS — all eleven gates pass; the sky-forecast is a data-honest, explicitly-stated NO-GO with a named backup night, which is an accepted pass condition, not a failure.

## Gates
| Gate | Result | Affected artifact | Owning agent | Finding |
|---|---|---|---|---|
| G1 | PASS | all 6 artifacts | all | `check_artifact.py` reports PASS on budget.md, gear.md, night.md, requirements.md, sky-forecast.md, targets.md — no structural findings. |
| G2 | PASS | budget.md | budget-aggregator | Total 31.87 EUR against the 40 EUR limit from requirements.md; 8.13 EUR headroom. |
| G3 | PASS | requirements.md / budget.md | site-scout (N/A, site fixed) / budget-aggregator | Site was fixed by the observer, so G3 applies to the recorded site. Bus travel Szklarska Poręba to Świeradów-Zdrój is 35-45 minutes, against the 60-minute limit from requirements.md. |
| G4 | PASS | sky-forecast.md | sky-forecaster | Mean cloud is unresolvable (Open-Meteo horizon caps at 2026-10-06; target nights are 2026-11-05/06/07, 45-47 days out - no number exists, so the 40% threshold cannot even be tested). The plan is explicitly marked "Plan status: NO-GO (provisional, weather unresolved)" with backup night 2026-11-06 named alongside primary 2026-11-07 - satisfies the stated no-go-plus-backup pass condition. |
| G5 | PASS | night.md / targets.md | night-calculator / visual-target-planner | Primary night 2026-11-07: moon illumination 2.0%, moon up 0% of the dark window. Backup night 2026-11-06: 5.7% illumination, moon up 0%. Both under the 40% illumination threshold from requirements.md, and the moon is not up during either window for the deep-sky targets (M42, M45, M31, Double Cluster). |
| G6 | PASS | targets.md | visual-target-planner | All five kept targets clear 20 deg for over an hour in the dark window: Jupiter 3.33 h, M42 6 h, M45 10.33 h, Double Cluster 11 h, M31 11 h (both candidate nights, per `object_visibility`). |
| G7 | PASS | targets.md | visual-target-planner | Five distinct objects listed (Jupiter, M42, M45, Double Cluster, M31); no repeats or aliases of the same object. |
| G8 | PASS | gear.md | gear-planner | No purchase repeats owned gear (binoculars, warm clothes kept as owned; only new item is a red-light headlamp). Telescope was priced (~45 EUR purchase, unreachable rental) and explicitly rejected with reasoning rather than silently omitted; visual mode's essential gear (binoculars) is present and confirmed sufficient for every listed target. |
| G9 | PASS | targets.md, gear.md, budget.md | visual-target-planner, gear-planner, budget-aggregator | Every target, the priced headlamp, the rejected telescope options, the bus fare, and the site-fee claim each cite a source URL or MCP call (e.g. decathlon.pl for the headlamp, astropolis.pl/bresser.com for telescope pricing, swieradowzdroj.pl for the bus schedule and park access). |
| G10 | PASS | requirements.md / budget.md | site-scout (N/A, site fixed) / budget-aggregator | Site fixed by observer, so G10 applies to the recorded site. Access is on foot/local bus (no parking concern - no car), and legality is addressed: the park is a protected nature area with free, unrestricted, 24/7 access and no permit required (sourced from swieradow.pl and swieradowzdroj.pl). |
| G11 | PASS | requirements.md, targets.md | requirements-formalizer, visual-target-planner | requirements.md confirms `mode: visual`; targets.md is written by the visual-target-planner (binocular/small-telescope guidance, no camera/exposure content), and no astrophoto artifact exists in this run. |

## Required Retries
None. All gates pass.

## Sources
- Checker: `python3 .claude/skills/artifact-validator/check_artifact.py runs/2026-09-21-izera-visual/artifacts/*.md` - PASS on all 6 artifacts.
- Thresholds used, all from `runs/2026-09-21-izera-visual/artifacts/requirements.md`: budget limit 40 EUR; max travel one way 60 minutes; max cloud cover in dark window 40% (default); max moon illumination 40% (default).
- Artifacts read in full: `requirements.md`, `night.md`, `sky-forecast.md`, `targets.md`, `gear.md`, `budget.md` under `runs/2026-09-21-izera-visual/artifacts/`.
- No `sites.md` or `session-plan.md` exists yet in this run (site-scout stage skipped because the observer fixed the site; session-plan.md not yet built) - the site-scout-owned gate rows (G3, G10) were evaluated against the site recorded in requirements.md per the workflow's "site fixed by observer" fallback rule.
