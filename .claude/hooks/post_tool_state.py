#!/usr/bin/env python3
"""PostToolUse recorder.

Writes are recorded into workflow-state.json (hash + timestamp) so a resumed run
knows what already exists; MCP calls are appended to mcp-log.jsonl as evidence
that the plan rests on external data rather than model memory.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import state as st  # noqa: E402


def record_write(payload: dict) -> None:
    ti = payload.get("tool_input", {})
    raw = ti.get("file_path", "")
    if not raw:
        return
    p = Path(raw)
    if not p.is_absolute():
        p = Path(payload.get("cwd", ROOT)) / p
    try:
        rel = p.resolve().relative_to(ROOT)
    except ValueError:
        return
    parts = rel.parts
    if len(parts) < 3 or parts[0] != "runs":
        return
    run_id = parts[1]
    if not st.state_path(run_id).is_file():
        return

    s = st.load(run_id)
    s["artifacts"][p.name] = {
        "path": str(rel),
        "sha256": st.sha256_file(p),
        "updated_at": st.now(),
        "written_by": payload.get("agent_type") or "coordinator",
    }
    st.save(s)


def record_mcp(payload: dict) -> None:
    run_id = st.current_run()
    if not run_id:
        return
    entry = {
        "at": st.now(),
        "tool": payload.get("tool_name"),
        "args": payload.get("tool_input", {}),
        "agent": payload.get("agent_type") or "coordinator",
    }
    log = st.RUNS / run_id / "mcp-log.jsonl"
    with log.open("a") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")
    s = st.load(run_id)
    s["mcp_calls"] += 1
    st.save(s)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    tool = payload.get("tool_name", "")
    if tool.startswith("mcp__"):
        record_mcp(payload)
    else:
        record_write(payload)
    sys.exit(0)


if __name__ == "__main__":
    main()
