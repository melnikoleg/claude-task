#!/usr/bin/env python3
"""Workflow state for the stargazing planner.

Single writer for runs/<run-id>/workflow-state.json. The PreToolUse hook denies
any direct Write/Edit of that file, so every state change goes through here and
stays machine-checkable - that is what makes resume and the approval gate
deterministic rather than a thing the model remembers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"

STAGE_STATUSES = ("pending", "running", "done", "failed", "blocked", "skipped")

NEW_STAGE = {"status": "pending", "attempts": 0, "agents": [], "started_at": None, "finished_at": None}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state_path(run_id: str) -> Path:
    return RUNS / run_id / "workflow-state.json"


def load(run_id: str) -> dict:
    p = state_path(run_id)
    if not p.is_file():
        sys.exit(f"no such run: {run_id} (expected {p})")
    return json.loads(p.read_text())


def save(state: dict) -> None:
    p = state_path(state["run_id"])
    p.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now()
    fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".tmp")
    with os.fdopen(fd, "w") as fh:
        json.dump(state, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, p)


def current_run() -> str | None:
    """Newest run still marked running - used by hooks to locate the live run."""
    candidates = []
    for sp in RUNS.glob("*/workflow-state.json"):
        try:
            s = json.loads(sp.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if s.get("status") == "running":
            candidates.append((s.get("updated_at", ""), s["run_id"]))
    return max(candidates)[1] if candidates else None


def cmd_init(a) -> None:
    p = state_path(a.run_id)
    if p.is_file():
        sys.exit(f"run {a.run_id} already exists; use --resume or pick another id")
    (RUNS / a.run_id / "artifacts").mkdir(parents=True, exist_ok=True)
    (RUNS / a.run_id / "validation").mkdir(parents=True, exist_ok=True)
    save(
        {
            "run_id": a.run_id,
            "status": "running",
            "created_at": now(),
            "updated_at": now(),
            "request": a.request,
            "plan": {"mode": None, "site_fixed": None, "stages": []},
            "stages": {},
            "artifacts": {},
            "gates": [],
            "validation_cycles": 0,
            "approval": {"status": "pending", "plan_sha256": None, "feedback": [], "decided_at": None},
            "mcp_calls": 0,
        }
    )
    print(f"initialised run {a.run_id}")


def cmd_plan(a) -> None:
    s = load(a.run_id)
    stages = [x.strip() for x in a.stages.split(",") if x.strip()]
    s["plan"] = {"mode": a.mode, "site_fixed": a.site_fixed, "stages": stages}
    for name in stages:
        s["stages"].setdefault(name, dict(NEW_STAGE))
    save(s)
    print(f"plan stored: {' -> '.join(stages)}")


def cmd_stage(a) -> None:
    s = load(a.run_id)
    if a.status not in STAGE_STATUSES:
        sys.exit(f"status must be one of {', '.join(STAGE_STATUSES)}")
    st = s["stages"].setdefault(a.name, dict(NEW_STAGE))
    st["status"] = a.status
    if a.agents:
        st["agents"] = [x.strip() for x in a.agents.split(",") if x.strip()]
    if a.status == "running":
        st["attempts"] += 1
        st["started_at"] = now()
    if a.status in ("done", "failed", "blocked", "skipped"):
        st["finished_at"] = now()
    if a.note:
        st["note"] = a.note
    if a.status in ("failed", "blocked"):
        s["status"] = "blocked"
    save(s)
    print(f"{a.name}: {a.status}")


def cmd_gate(a) -> None:
    s = load(a.run_id)
    s["gates"].append(
        {
            "cycle": a.cycle,
            "gate": a.gate,
            "result": a.result.upper(),
            "affected": [x.strip() for x in (a.affected or "").split(",") if x.strip()],
            "finding": a.finding or "",
            "at": now(),
        }
    )
    s["validation_cycles"] = max(s["validation_cycles"], a.cycle)
    save(s)
    print(f"cycle {a.cycle} {a.gate}: {a.result.upper()}")


def cmd_approve(a) -> None:
    s = load(a.run_id)
    plan = RUNS / a.run_id / "artifacts" / "session-plan.md"
    digest = sha256_file(plan)
    if digest is None:
        sys.exit("cannot approve: artifacts/session-plan.md does not exist")
    s["approval"] = {
        "status": "approved",
        "plan_sha256": digest,
        "feedback": s["approval"]["feedback"],
        "decided_at": now(),
    }
    save(s)
    print(f"approved session-plan.md ({digest[:12]}...) - html-builder is now unblocked")


def cmd_reject(a) -> None:
    s = load(a.run_id)
    s["approval"]["status"] = "rejected"
    s["approval"]["plan_sha256"] = None
    s["approval"]["decided_at"] = now()
    s["approval"]["feedback"].append({"at": now(), "text": a.feedback})
    save(s)
    print("rejected; feedback recorded - revise, rebuild the plan, ask again")


def cmd_complete(a) -> None:
    s = load(a.run_id)
    s["status"] = "complete"
    save(s)
    print(f"run {a.run_id} complete")


def cmd_show(a) -> None:
    print(json.dumps(load(a.run_id), indent=2))


def cmd_list(a) -> None:
    for sp in sorted(RUNS.glob("*/workflow-state.json")):
        s = json.loads(sp.read_text())
        print(f"{s['run_id']:40} {s['status']:9} approval={s['approval']['status']}")


def cmd_resume_plan(a) -> None:
    """What a resumed run must still do, and what it must not redo."""
    s = load(a.run_id)
    stages = s["plan"]["stages"] or list(s["stages"])
    print(f"run          : {s['run_id']}  (status {s['status']})")
    print(f"request      : {s['request']}")
    print(f"mode         : {s['plan']['mode']}   site_fixed: {s['plan']['site_fixed']}")
    print(f"approval     : {s['approval']['status']}")
    print(f"validation   : {s['validation_cycles']} cycle(s) run")
    print("\nstages:")
    todo = []
    for name in stages:
        st = s["stages"].get(name, {"status": "pending", "attempts": 0})
        mark = {"done": "x", "skipped": "-", "failed": "!", "blocked": "!"}.get(st["status"], " ")
        print(f"  [{mark}] {name:24} {st['status']:9} attempts={st['attempts']}")
        if st["status"] not in ("done", "skipped"):
            todo.append(name)
    print("\nartifacts on disk (do NOT regenerate these):")
    for name, meta in sorted(s["artifacts"].items()):
        live = sha256_file(ROOT / meta["path"])
        flag = "ok" if live == meta["sha256"] else "CHANGED ON DISK"
        print(f"  {name:24} {flag}")
    if not s["artifacts"]:
        print("  (none)")
    print(f"\nresume at    : {todo[0] if todo else 'nothing pending'}")
    print(f"remaining    : {', '.join(todo) if todo else '-'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("run_id"); p.add_argument("--request", required=True); p.set_defaults(fn=cmd_init)
    p = sub.add_parser("plan"); p.add_argument("run_id"); p.add_argument("--stages", required=True)
    p.add_argument("--mode", required=True); p.add_argument("--site-fixed", dest="site_fixed", action="store_true"); p.set_defaults(fn=cmd_plan)
    p = sub.add_parser("stage"); p.add_argument("run_id"); p.add_argument("name"); p.add_argument("status")
    p.add_argument("--agents"); p.add_argument("--note"); p.set_defaults(fn=cmd_stage)
    p = sub.add_parser("gate"); p.add_argument("run_id"); p.add_argument("cycle", type=int); p.add_argument("gate")
    p.add_argument("result"); p.add_argument("--affected"); p.add_argument("--finding"); p.set_defaults(fn=cmd_gate)
    p = sub.add_parser("approve"); p.add_argument("run_id"); p.set_defaults(fn=cmd_approve)
    p = sub.add_parser("reject"); p.add_argument("run_id"); p.add_argument("--feedback", required=True); p.set_defaults(fn=cmd_reject)
    p = sub.add_parser("complete"); p.add_argument("run_id"); p.set_defaults(fn=cmd_complete)
    p = sub.add_parser("show"); p.add_argument("run_id"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("list"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("resume-plan"); p.add_argument("run_id"); p.set_defaults(fn=cmd_resume_plan)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
