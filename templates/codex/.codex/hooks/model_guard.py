#!/usr/bin/env python3
"""Example runtime model guard for Codex hooks.

Set AVF_EXPECTED_MODEL in the hook command environment or adapt this script to
role-specific expected models. The active model slug comes from Codex hook input.
"""
from __future__ import annotations

import json
import os
import sys


def main() -> int:
    event = json.load(sys.stdin)
    actual = event.get("model", "")
    expected = os.environ.get("AVF_EXPECTED_MODEL", "").strip()
    if not expected or actual == expected:
        return 0
    message = f"AVF ROUTING_MISMATCH: expected model '{expected}', active model is '{actual}'. Reconcile routing before relying on this role."
    print(json.dumps({"continue": True, "systemMessage": message}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
