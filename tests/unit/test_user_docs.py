"""Tests for the reader-facing users guide."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_USERS_DOC = _REPO_ROOT / "docs" / "users.md"

# Phrases a reader must be able to find without knowing the build.
_REQUIRED_PHRASES = (
    "What you can do today",
    "Reading posts",
    "Newsletter",
    "Privacy",
    "Accessibility",
    "The public site is not live yet.",
    "no domain",
    "no posts",
    "no signup form",
    "AI agents",
    "tags",
    "series",
    "search",
    "RSS",
    "dark mode",
    "double opt-in",
    "WCAG 2.2 AA",
    "open a post",
    "follow tags",
    "subscribe",
    "confirm",
    "unsubscribe",
    "one click",
    "non-essential cookies",
    "consent",
    "UK GDPR",
    "PECR",
    "Policies are not published yet.",
    "keyboard",
    "contrast",
    "alt text",
    "not audited yet",
    "Venkat",
)


class TestUserDocs(unittest.TestCase):
    """Verify the reader guide states what exists and what is planned."""

    def test_users_guide_covers_reader_topics(self) -> None:
        """The guide names today's limits and the planned reader pages.

        The check is a plain text search so the page can stay written
        for readers. The repository root is the parent of ``tests``.
        """
        self.assertTrue(_USERS_DOC.is_file(), f"missing {_USERS_DOC}")
        text = _USERS_DOC.read_text(encoding="utf-8")
        missing = [
            phrase for phrase in _REQUIRED_PHRASES if phrase not in text
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
