"""Tests for the editorial content QA checklist.

The checklist at ``docs/editorial/content-qa-checklist.md`` is the
gate every post must pass before it is offered for Venkat publish
approval. These tests assert the file exists and names the required
checks. They do not publish a post.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_CHECKLIST = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "editorial"
    / "content-qa-checklist.md"
)

_REQUIRED_SUBSTRINGS = (
    "accuracy",
    "sources cited",
    "one idea",
    "headings",
    "AI engineers",
    "researchers",
    "tech leads",
    "secrets",
    "credentials",
    "title",
    "description",
    "slug",
    "draft: true",
    "Venkat",
    "code samples",
    "unverified",
)


class TestEditorialContentQaChecklist(unittest.TestCase):
    """The editorial QA checklist exists and covers every required gate."""

    def test_checklist_exists(self) -> None:
        """``docs/editorial/content-qa-checklist.md`` is present."""
        self.assertTrue(
            _CHECKLIST.is_file(),
            f"missing editorial QA checklist: {_CHECKLIST}",
        )

    def test_checklist_covers_required_gates(self) -> None:
        """Required accuracy, structure, voice, SEO, and publish phrases."""
        self.assertTrue(
            _CHECKLIST.is_file(),
            f"missing editorial QA checklist: {_CHECKLIST}",
        )
        text = _CHECKLIST.read_text(encoding="utf-8").casefold()
        for needle in _REQUIRED_SUBSTRINGS:
            self.assertIn(needle.casefold(), text)


if __name__ == "__main__":
    unittest.main()
