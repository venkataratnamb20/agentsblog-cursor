"""Pending reader journeys recorded in the manual catalog."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MANUAL_DOC = _REPO_ROOT / "docs" / "testing" / "manual-tests.md"
_LOCAL_SENTENCE = "read post and search work on the local preview"
_SUBSCRIBE_SENTENCE = (
    "subscribe is blocked until an email service is approved"
)


class TestJourneysPending(unittest.TestCase):
    """Verify site journeys stay blocked in the manual catalog."""

    def test_local_read_and_search_work_and_subscribe_is_blocked(self) -> None:
        """Assert local read and search work, and subscribe stays blocked.

        The manual catalog is read from disk. This test does not skip.
        Subscribe stays blocked because no email service is approved.
        """
        self.assertTrue(_MANUAL_DOC.is_file())
        text = _MANUAL_DOC.read_text(encoding="utf-8").lower()
        self.assertIn(_LOCAL_SENTENCE, text)
        self.assertIn(_SUBSCRIBE_SENTENCE, text)
        self.assertNotIn(
            "subscribe, read post, and search are blocked until the site exists",
            text,
        )


if __name__ == "__main__":
    unittest.main()
