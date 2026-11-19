"""Pending reader journeys recorded in the manual catalog."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MANUAL_DOC = _REPO_ROOT / "docs" / "testing" / "manual-tests.md"
_BLOCKED_SENTENCE = (
    "subscribe, read post, and search are blocked until the site exists"
)


class TestJourneysPending(unittest.TestCase):
    """Verify site journeys stay blocked in the manual catalog."""

    def test_subscribe_read_post_and_search_are_blocked(self) -> None:
        """Assert subscribe, read post, and search are blocked.

        The manual catalog is read from disk. This test does not skip.
        A missing catalog or a journey that is not marked blocked fails.
        """
        self.assertTrue(_MANUAL_DOC.is_file())
        text = _MANUAL_DOC.read_text(encoding="utf-8").lower()
        self.assertIn(_BLOCKED_SENTENCE, text)
        for journey in ("subscribe", "read post", "search"):
            self.assertIn(journey, text)
            self.assertIn("blocked", text)


if __name__ == "__main__":
    unittest.main()
