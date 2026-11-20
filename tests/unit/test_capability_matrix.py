"""Tests for the AI team harness capability matrix.

Behaviour: ``docs/agents/capability-matrix.md`` records the seven shared
skills as present, names fourteen roles, and documents tool version
probes (Cursor/Claude live or smoke note; Codex/Antigravity out of
scope). Existing tests: none for this document.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MATRIX = _REPO_ROOT / "docs" / "agents" / "capability-matrix.md"

_SHARED_SKILLS = (
    "new-post",
    "review-pr",
    "security-check",
    "seo-audit",
    "gate-check",
    "release",
    "hotfix",
)

_ROLES = (
    "PM Orchestrator",
    "Solution Architect",
    "Product Strategist",
    "Technical Writer",
    "Technical Editor",
    "Research Analyst",
    "UX/UI Designer",
    "Frontend Engineer",
    "QA Engineer",
    "Code Reviewer",
    "Security Engineer",
    "DevOps & SRE",
    "SEO & Analytics",
    "Growth & Community",
)


class TestCapabilityMatrix(unittest.TestCase):
    """Assert the capability matrix reflects the current harness."""

    def setUp(self) -> None:
        """Load the matrix text once per test."""
        self.assertTrue(_MATRIX.is_file(), f"missing {_MATRIX}")
        self.text = _MATRIX.read_text(encoding="utf-8")

    def test_seven_shared_skills_recorded_as_present(self) -> None:
        """Each shared skill is named and marked present, not planned-only."""
        lowered = self.text.lower()
        for skill in _SHARED_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(skill, lowered)
        # Skills exist on disk; the matrix must not claim none exist.
        self.assertNotIn(
            "none of them exist in this worktree",
            lowered,
            "matrix still claims shared skills are absent",
        )
        self.assertRegex(
            self.text,
            r"(?is)((present|exist|written|available).{0,80}(seven|7).{0,40}skill"
            r"|(seven|7).{0,40}skill.{0,80}(present|exist|written|available)"
            r"|shared skills.{0,40}(present|exist|written))",
            msg="matrix must state the seven shared skills are present",
        )

    def test_fourteen_roles_listed(self) -> None:
        """All fourteen team roles appear in the matrix."""
        for role in _ROLES:
            with self.subTest(role=role):
                self.assertIn(role, self.text)
        self.assertRegex(
            self.text,
            r"(?i)14\s+(roles|subagents)|fourteen\s+(roles|subagents)",
            msg="matrix must record that 14 roles/subagents exist",
        )

    def test_version_probe_recorded(self) -> None:
        """Cursor/Claude probe results (or smoke note) and out of scope tools."""
        lowered = self.text.lower()
        cursor_ok = "cursor" in lowered and (
            "3." in self.text
            or "probed in smoke" in lowered
            or "unavailable" in lowered
        )
        claude_ok = "claude" in lowered and (
            "not probed — claude.md pointer verified" in lowered
            or "claude.md pointer verified" in lowered
            or "probed in smoke" in lowered
        )
        codex_oos = "codex" in lowered and (
            "out of scope" in lowered or "probed in smoke" in lowered
        )
        antigravity_oos = "antigravity" in lowered and (
            "out of scope" in lowered or "probed in smoke" in lowered
        )
        self.assertTrue(cursor_ok, "Cursor version probe missing from matrix")
        self.assertTrue(
            claude_ok,
            "Claude version probe or CLAUDE.md pointer note missing",
        )
        self.assertTrue(
            codex_oos,
            "Codex must be marked out of scope or probed in smoke",
        )
        self.assertTrue(
            antigravity_oos,
            "Antigravity must be marked out of scope or probed in smoke",
        )


if __name__ == "__main__":
    unittest.main()
