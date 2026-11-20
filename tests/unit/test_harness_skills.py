"""Harness inventory: shared skills, Claude commands, and Claude agents."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_SKILLS = (
    "new-post",
    "review-pr",
    "security-check",
    "seo-audit",
    "gate-check",
    "release",
    "hotfix",
)


class TestHarnessSkills(unittest.TestCase):
    """Assert the seven shared skills and their Claude entry points exist."""

    def test_seven_skills_in_agents_skills(self) -> None:
        """``.agents/skills`` holds exactly the seven shared skill dirs."""
        skills_root = REPO_ROOT / ".agents" / "skills"
        self.assertTrue(skills_root.is_dir())
        found = sorted(
            path.name for path in skills_root.iterdir() if path.is_dir()
        )
        self.assertEqual(found, sorted(EXPECTED_SKILLS))
        for name in EXPECTED_SKILLS:
            skill_file = skills_root / name / "SKILL.md"
            self.assertTrue(skill_file.is_file(), skill_file)

    def test_seven_command_files_in_claude_commands(self) -> None:
        """``.claude/commands`` has one markdown entry point per skill."""
        commands_root = REPO_ROOT / ".claude" / "commands"
        self.assertTrue(commands_root.is_dir())
        found = sorted(
            path.stem
            for path in commands_root.iterdir()
            if path.is_file() and path.suffix == ".md"
        )
        self.assertEqual(found, sorted(EXPECTED_SKILLS))
        for name in EXPECTED_SKILLS:
            command_file = commands_root / f"{name}.md"
            self.assertTrue(command_file.is_file(), command_file)
            text = command_file.read_text(encoding="utf-8")
            self.assertIn(name, text)

    def test_fourteen_agent_files_in_claude_agents(self) -> None:
        """``.claude/agents`` holds fourteen role agent markdown files."""
        agents_root = REPO_ROOT / ".claude" / "agents"
        self.assertTrue(agents_root.is_dir())
        found = sorted(
            path.name
            for path in agents_root.iterdir()
            if path.is_file() and path.suffix == ".md"
        )
        self.assertEqual(len(found), 14)
        for name in found:
            self.assertTrue((agents_root / name).is_file())


if __name__ == "__main__":
    unittest.main()
