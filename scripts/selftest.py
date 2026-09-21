#!/usr/bin/env python3
"""End-to-end check of the deterministic parts: state CLI, both hooks, validator.

Run from the repo root: python3 scripts/selftest.py
Uses a throwaway run id and removes it afterwards.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN = "selftest-run"
RUN_DIR = ROOT / "runs" / RUN
PRE = ROOT / ".claude/hooks/pre_tool_guard.py"
POST = ROOT / ".claude/hooks/post_tool_state.py"
STATE = ROOT / "scripts/state.py"
CHECK = ROOT / ".claude/skills/artifact-validator/check_artifact.py"

# A structurally valid artifact, used for the positive cases.
GOOD_SITES = """# Dark-Sky Sites - selftest

## Candidate Sites
### 1. Example Ridge
| Field | Value |
|---|---|
| Coordinates | lat 52.10, lon 20.40 |
| Estimated drive | 55 minutes |
| Access and legality | public forest car park, open all night, no fee |

The ridge faces south over farmland with a clear horizon and no nearby town glow,
which makes it the most usable of the three candidates for a short winter session.

## Recommended Site
Example Ridge, because it is the darkest option inside the travel limit and the car
park is open through the night. The runner-up is the lakeside pull-in to the east.

## Risks
Forest tracks turn muddy after rain, and the gate is occasionally closed in storms.

## Sources
- https://www.lightpollutionmap.info/
"""

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else ' -- ' + detail}")
    if not ok:
        failures.append(name)


def hook(script: Path, payload: dict) -> str:
    r = subprocess.run(
        [sys.executable, str(script)], input=json.dumps(payload), capture_output=True, text=True, cwd=ROOT
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


def denied(out: str) -> bool:
    if not out.strip():
        return False
    return json.loads(out)["hookSpecificOutput"].get("permissionDecision") == "deny"


def write_payload(path: str, content: str = "", tool: str = "Write") -> dict:
    return {
        "tool_name": tool,
        "cwd": str(ROOT),
        "hook_event_name": "PreToolUse",
        "tool_input": {"file_path": str(ROOT / path), "content": content},
    }


def sh(*args: str) -> str:
    r = subprocess.run([sys.executable, str(STATE), *args], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr
    return r.stdout


def main() -> None:
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)

    print("state CLI")
    sh("init", RUN, "--request", "selftest")
    sh("plan", RUN, "--mode", "visual", "--stages", "requirements,groupA,validation,plan,html")
    sh("stage", RUN, "requirements", "done")
    s = json.loads((RUN_DIR / "workflow-state.json").read_text())
    check("init + plan + stage persist", s["stages"]["requirements"]["status"] == "done")
    check("resume-plan names next stage", "resume at    : groupA" in sh("resume-plan", RUN))

    print("PreToolUse guard")
    check("blocks direct state writes", denied(hook(PRE, write_payload(f"runs/{RUN}/workflow-state.json", "{}"))))
    check("blocks artifact with no Sources", denied(hook(PRE, write_payload(f"runs/{RUN}/artifacts/sites.md", "# Sites\nbody"))))
    check("blocks artifact with TODO", denied(hook(PRE, write_payload(f"runs/{RUN}/artifacts/sites.md", "# Sites\nTODO\n## Sources\n- https://a.example"))))
    good = GOOD_SITES
    check("allows well-formed artifact", not denied(hook(PRE, write_payload(f"runs/{RUN}/artifacts/sites.md", good))))
    check("ignores files outside runs/", not denied(hook(PRE, write_payload("README.md", "TODO"))))
    check("blocks HTML before approval", denied(hook(PRE, write_payload(f"runs/{RUN}/stargazing-guide.html", "<html>"))))

    print("PostToolUse recorder")
    (RUN_DIR / "artifacts").mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "artifacts" / "sites.md").write_text(good)
    hook(POST, {"tool_name": "Write", "cwd": str(ROOT), "agent_type": "site-scout",
                "tool_input": {"file_path": str(RUN_DIR / "artifacts/sites.md")}, "tool_response": {}})
    s = json.loads((RUN_DIR / "workflow-state.json").read_text())
    check("records artifact hash and author", s["artifacts"].get("sites.md", {}).get("written_by") == "site-scout")

    hook(POST, {"tool_name": "mcp__astro__moon_info", "cwd": str(ROOT), "agent_type": "night-calculator",
                "tool_input": {"lat": 52.2, "lon": 21.0, "date": "2026-10-10"}, "tool_response": {}})
    log = (RUN_DIR / "mcp-log.jsonl").read_text().strip().splitlines()
    check("logs MCP calls as evidence", len(log) == 1 and json.loads(log[0])["tool"] == "mcp__astro__moon_info")

    print("approval gate")
    plan = RUN_DIR / "artifacts" / "session-plan.md"
    plan.write_text("# Session plan\nv1\n\n## Sources\n- https://a.example\n")
    sh("approve", RUN)
    check("allows HTML once approved", not denied(hook(PRE, write_payload(f"runs/{RUN}/stargazing-guide.html", "<html>"))))
    plan.write_text("# Session plan\nv2 edited after approval\n\n## Sources\n- https://a.example\n")
    check("re-blocks HTML when plan changed after approval",
          denied(hook(PRE, write_payload(f"runs/{RUN}/stargazing-guide.html", "<html>"))))
    sh("reject", RUN, "--feedback", "too expensive")
    s = json.loads((RUN_DIR / "workflow-state.json").read_text())
    check("reject clears approval and stores feedback",
          s["approval"]["status"] == "rejected" and s["approval"]["feedback"][0]["text"] == "too expensive")

    print("artifact-validator skill")
    r = subprocess.run([sys.executable, str(CHECK), str(RUN_DIR / "artifacts/sites.md")],
                       capture_output=True, text=True, cwd=ROOT)
    check("checker passes a valid artifact", r.returncode == 0, r.stdout + r.stderr)
    bad = RUN_DIR / "artifacts" / "budget.md"
    bad.write_text("# Budget\nno sections here\n")
    r = subprocess.run([sys.executable, str(CHECK), str(bad)], capture_output=True, text=True, cwd=ROOT)
    check("checker fails an artifact missing required sections", r.returncode != 0)

    shutil.rmtree(RUN_DIR)
    print()
    if failures:
        print(f"{len(failures)} FAILED: {', '.join(failures)}")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
