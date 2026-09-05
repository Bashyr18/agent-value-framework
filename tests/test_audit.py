import json
from pathlib import Path

from agent_value_framework.audit import audit_repository


def test_audit_detects_common_files(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("hello", encoding="utf-8")
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "pytest"}}), encoding="utf-8")
    (tmp_path / ".agents/skills/demo").mkdir(parents=True)
    (tmp_path / ".agents/skills/demo/SKILL.md").write_text("---\nname: demo\ndescription: demo\n---", encoding="utf-8")
    report = audit_repository(tmp_path)
    assert "AGENTS.md" in report.instruction_files
    assert ".agents/skills/demo/SKILL.md" in report.skill_files
    assert report.package_scripts["test"] == "pytest"
