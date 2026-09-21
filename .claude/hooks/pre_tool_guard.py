#!/usr/bin/env python3
"""PreToolUse guard for Write/Edit.

Three deterministic blocks the model cannot talk its way past:
  approval-gate  - no final HTML before a human approved that exact session plan
  state-guard    - workflow-state.json is written only by scripts/state.py
  artifact-shape - no artifact without a Sources section, no TODO placeholders
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import state as st  # noqa: E402


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        sys.exit(0)

    ti = payload.get("tool_input", {})
    raw = ti.get("file_path", "")
    if not raw:
        sys.exit(0)

    p = Path(raw)
    if not p.is_absolute():
        p = Path(payload.get("cwd", ROOT)) / p
    try:
        rel = p.resolve().relative_to(ROOT)
    except ValueError:
        sys.exit(0)
    parts = rel.parts
    if not parts or parts[0] != "runs" or len(parts) < 2:
        sys.exit(0)
    run_id = parts[1]

    if p.name == "workflow-state.json":
        deny(
            "workflow-state.json is owned by scripts/state.py. Use "
            f"`python3 scripts/state.py stage {run_id} <stage> <status>` (or plan/gate/"
            "approve/reject/complete) instead of writing the file directly."
        )

    if p.suffix == ".html":
        sp = st.state_path(run_id)
        if not sp.is_file():
            deny(f"no workflow state for run {run_id}; the final guide cannot be built outside a tracked run.")
        s = json.loads(sp.read_text())
        approval = s.get("approval", {})
        if approval.get("status") != "approved":
            deny(
                "APPROVAL GATE: the final guide may not be written until the user approves "
                f"the session plan. Current approval status: {approval.get('status')}. Present "
                f"artifacts/session-plan.md to the user, then run `python3 scripts/state.py approve {run_id}`."
            )
        live = st.sha256_file(ROOT / "runs" / run_id / "artifacts" / "session-plan.md")
        if live != approval.get("plan_sha256"):
            deny(
                "APPROVAL GATE: session-plan.md changed after approval, so the approval no "
                "longer covers it. Show the revised plan to the user and re-approve with "
                f"`python3 scripts/state.py approve {run_id}`."
            )
        sys.exit(0)

    if tool == "Write" and len(parts) > 2 and parts[2] == "artifacts" and p.suffix == ".md":
        content = ti.get("content", "")
        placeholder = re.search(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b", content, re.I)
        if placeholder:
            deny(
                f"ARTIFACT SHAPE: {p.name} contains the placeholder {placeholder.group(0)!r}. "
                "Artifacts must be complete; research the value or state the limitation explicitly."
            )
        m = re.search(r"^##+\s*Sources\s*$", content, re.M)
        if not m or not re.search(r"https?://", content[m.end():]):
            deny(
                f"ARTIFACT SHAPE: {p.name} needs a `## Sources` section listing at least one "
                "http(s) URL or MCP tool call that backs its recommendations. Internal model "
                "knowledge is not a source."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
