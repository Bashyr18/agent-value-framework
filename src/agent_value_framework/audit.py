from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "target", ".next", ".turbo"}


@dataclass
class RepoAudit:
    root: str
    is_git_repo: bool
    dirty_entries: int | None
    instruction_files: list[str]
    codex_files: list[str]
    skill_files: list[str]
    ci_files: list[str]
    automation_files: list[str]
    package_scripts: dict[str, str]
    detected_stacks: list[str]
    collisions: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    def to_markdown(self) -> str:
        lines = ["# AVF repository audit", "", f"Root: `{self.root}`", ""]
        lines += [f"- Git repository: **{self.is_git_repo}**"]
        lines += [f"- Dirty/untracked entries: **{self.dirty_entries if self.dirty_entries is not None else 'unknown'}**"]
        lines += [f"- Detected stacks: {', '.join(self.detected_stacks) or 'unknown'}", ""]
        sections = [
            ("Instruction files", self.instruction_files),
            ("Codex files", self.codex_files),
            ("Skills", self.skill_files),
            ("CI", self.ci_files),
            ("Automation", self.automation_files),
            ("Potential collisions", self.collisions),
        ]
        for title, values in sections:
            lines += [f"## {title}"]
            lines += [f"- `{v}`" for v in values] if values else ["- None detected"]
            lines.append("")
        lines += ["## Package scripts"]
        if self.package_scripts:
            lines += [f"- `{k}` → `{v}`" for k, v in sorted(self.package_scripts.items())]
        else:
            lines += ["- None detected"]
        return "\n".join(lines) + "\n"


def _walk(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(current)
        for name in files:
            yield base / name


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _git_status_count(root: Path) -> tuple[bool, int | None]:
    try:
        p = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return True, len([line for line in p.stdout.splitlines() if line.strip()])
    except Exception:
        return False, None


def _package_scripts(root: Path) -> dict[str, str]:
    package = root / "package.json"
    if not package.exists():
        return {}
    try:
        data = json.loads(package.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.get("scripts", {}).items()}
    except Exception:
        return {}


def audit_repository(path: str | Path) -> RepoAudit:
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(root)
    files = list(_walk(root))
    rels = {_rel(p, root): p for p in files}

    instruction = sorted(
        r for r in rels if Path(r).name in {"AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "CONTEXT.md"}
    )
    codex = sorted(r for r in rels if r.startswith(".codex/") or r == ".codex/config.toml")
    skills = sorted(r for r in rels if Path(r).name == "SKILL.md")
    ci = sorted(r for r in rels if r.startswith(".github/workflows/") or r in {".gitlab-ci.yml", "Jenkinsfile"})
    automation = sorted(
        r
        for r in rels
        if r.startswith("scripts/")
        or Path(r).name in {"Makefile", "Taskfile.yml", "justfile", "package.json", "pyproject.toml", "Cargo.toml", "go.mod"}
    )

    stacks: list[str] = []
    if "package.json" in rels:
        stacks.append("node")
    if "pyproject.toml" in rels or "requirements.txt" in rels:
        stacks.append("python")
    if "Cargo.toml" in rels:
        stacks.append("rust")
    if "go.mod" in rels:
        stacks.append("go")
    if any(r.endswith(".csproj") or r.endswith(".sln") for r in rels):
        stacks.append("dotnet")

    collisions: list[str] = []
    for candidate in ["AGENTS.md", ".codex/config.toml", "docs/agents/agent-value-workflow.md", ".agents/skills/value/SKILL.md"]:
        if candidate in rels or (root / candidate).exists():
            collisions.append(candidate)
    if (root / "bin").exists():
        collisions.append("bin/ exists; AVF should reuse the project's existing automation convention")
    if (root / ".scratch").exists():
        collisions.append(".scratch/ exists; reuse it for task state instead of creating a competing tracker")

    is_git, dirty = _git_status_count(root)
    return RepoAudit(
        root=str(root),
        is_git_repo=is_git,
        dirty_entries=dirty,
        instruction_files=instruction,
        codex_files=codex,
        skill_files=skills,
        ci_files=ci,
        automation_files=automation,
        package_scripts=_package_scripts(root),
        detected_stacks=stacks,
        collisions=collisions,
    )
