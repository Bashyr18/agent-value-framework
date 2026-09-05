from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .audit import audit_repository


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _command_version(command: str, args: list[str]) -> str | None:
    if not shutil.which(command):
        return None
    try:
        p = subprocess.run([command, *args], capture_output=True, text=True, timeout=10)
        text = (p.stdout or p.stderr).strip().splitlines()
        return text[0] if text else "installed"
    except Exception:
        return "installed (version unavailable)"


def doctor(path: str | Path) -> list[Check]:
    root = Path(path).resolve()
    audit = audit_repository(root)
    checks: list[Check] = []
    checks.append(Check("git", "ok" if audit.is_git_repo else "warn", "repository detected" if audit.is_git_repo else "not a git repository"))
    if audit.dirty_entries:
        checks.append(Check("worktree", "warn", f"{audit.dirty_entries} changed/untracked entries; never assume they are disposable"))
    else:
        checks.append(Check("worktree", "ok", "clean or status unavailable"))
    codex_version = _command_version("codex", ["--version"])
    checks.append(Check("codex", "ok" if codex_version else "info", codex_version or "not installed on PATH"))
    checks.append(Check("project-config", "ok" if (root / ".codex/config.toml").exists() else "info", "present" if (root / ".codex/config.toml").exists() else "no repository Codex config"))
    checks.append(Check("agents", "ok" if (root / "AGENTS.md").exists() else "info", "AGENTS.md present" if (root / "AGENTS.md").exists() else "no AGENTS.md"))
    checks.append(Check("avf-skill", "ok" if (root / ".agents/skills/avf-task/SKILL.md").exists() else "info", "installed" if (root / ".agents/skills/avf-task/SKILL.md").exists() else "not installed"))
    return checks
