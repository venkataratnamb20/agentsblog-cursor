"""Tests for the code-review operating-gate checklist.

The checklist at ``docs/guidelines/code-review.md`` is the gate a named
reviewer applies before approving a pull request. These tests prove the
document exists and states the required rules.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_CHECKLIST = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "guidelines"
    / "code-review.md"
)

_REQUIRED_SUBSTRINGS = (
    "named reviewer",
    "not the author",
    "failing test first",
    "python -m unittest discover -s tests -v",
    "make.ps1 test",
    "secrets",
    "credentials",
    "tokens",
    "private keys",
    ".env",
    "production deploy",
    "DNS",
    "publish",
    "Venkat",
    "draft: true",
    "index",
    "feed",
    "sitemap",
    "search",
    "may not approve their own",
)


class TestCodeReviewChecklist(unittest.TestCase):
    """The code-review checklist exists and states the operating gate."""

    def test_checklist_states_required_operating_rules(self) -> None:
        """Required gate rules are present in the checklist document."""
        self.assertTrue(
            _CHECKLIST.is_file(),
            f"missing code-review checklist: {_CHECKLIST}",
        )
        text = _CHECKLIST.read_text(encoding="utf-8")
        for needle in _REQUIRED_SUBSTRINGS:
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
