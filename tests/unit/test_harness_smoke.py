"""Tests for the four-tool harness smoke evidence record.

Behaviour: ``docs/agents/harness-smoke.md`` must document Cursor and Claude
checks that passed, and record Codex and Antigravity as out of scope per
``AGENTS.md``. Module: documentation only. Existing tests: none.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SMOKE_DOC = _REPO_ROOT / "docs" / "agents" / "harness-smoke.md"
_REQUIRED_SKILLS = (
    "new-post",
    "review-pr",
    "security-check",
    "seo-audit",
    "gate-check",
    "release",
    "hotfix",
)


class TestHarnessSmoke(unittest.TestCase):
    """Verify harness-smoke.md records the stage 0A smoke evidence."""

    def test_smoke_doc_exists(self) -> None:
        """Fail when the smoke evidence file is missing."""
        self.assertTrue(
            _SMOKE_DOC.is_file(),
            "docs/agents/harness-smoke.md is missing",
        )

    def test_cursor_checks_are_documented(self) -> None:
        """Cursor section names AGENTS.md, unittest, skills, and 14 roles."""
        text = _SMOKE_DOC.read_text(encoding="utf-8")
        self.assertIn("Cursor", text)
        self.assertIn("AGENTS.md", text)
        self.assertIn("python -m unittest discover -s tests -q", text)
        for skill in _REQUIRED_SKILLS:
            self.assertIn(skill, text)
        self.assertIn(".agents/skills", text)
        self.assertIn("14", text)
        self.assertIn(".claude/agents", text)

    def test_claude_checks_are_documented(self) -> None:
        """Claude section records CLAUDE.md pointer and seven skills."""
        text = _SMOKE_DOC.read_text(encoding="utf-8")
        self.assertIn("Claude", text)
        self.assertTrue(
            "@AGENTS.md" in text or "points at AGENTS.md" in text,
            "CLAUDE.md import or AGENTS.md pointer missing from smoke doc",
        )
        self.assertIn(".claude/skills", text)
        for skill in _REQUIRED_SKILLS:
            self.assertIn(skill, text)

    def test_codex_and_antigravity_are_out_of_scope(self) -> None:
        """Codex and Antigravity are OUT OF SCOPE with AGENTS.md Stack wording."""
        text = _SMOKE_DOC.read_text(encoding="utf-8")
        self.assertIn("Codex", text)
        self.assertIn("Antigravity", text)
        self.assertIn("OUT OF SCOPE", text)
        self.assertIn(
            "Codex and Antigravity are out of scope for this build",
            text,
        )
        self.assertIn("AGENTS.md", text)
        self.assertIn("Stack", text)

    def test_in_scope_tools_pass(self) -> None:
        """Smoke result is PASS for Cursor and Claude."""
        text = _SMOKE_DOC.read_text(encoding="utf-8")
        self.assertIn("PASS", text)
        self.assertRegex(
            text,
            r"(?i)(cursor|claude).{0,80}PASS|PASS.{0,80}(cursor|claude)",
        )


if __name__ == "__main__":
    unittest.main()
