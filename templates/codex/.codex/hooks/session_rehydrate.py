#!/usr/bin/env python3
"""Tiny Codex SessionStart hook for compaction recovery.

It intentionally injects instructions, not task contents. Repository truth is
read by the agent after compaction rather than dumped into context by the hook.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    event = json.load(sys.stdin)
    source = event.get("source")
    if source != "compact":
        return 0
    payload = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "Context was compacted. Before editing, rehydrate from the repository's active task-state record, "
                "git status, current diff, relevant project instructions/ADRs, and validation evidence. Reconcile "
                "repository state against remembered state; repository evidence wins. Continue from NEXT_CONCRETE_ACTION."
            ),
        },
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
