"""Tests for the human manual-test catalog."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MANUAL_DOC = _REPO_ROOT / "docs" / "testing" / "manual-tests.md"
_SECTION_TITLES = (
    "Harness (local)",
    "Developer docs",
    "End-user docs",
    "Not available yet",
)
_REQUIRED_PHRASES = (
    "make.ps1 test",
    "subscribe",
    "not live",
)


class TestManualCatalog(unittest.TestCase):
    """Verify the manual checklist names its sections and checks."""

    def test_section_titles_are_present(self) -> None:
        """Assert the catalog has the four human-facing sections.

        A missing file or a renamed heading fails this test. The
        headings are the contract a person uses to find a case.
        """
        self.assertTrue(_MANUAL_DOC.is_file())
        text = _MANUAL_DOC.read_text(encoding="utf-8")
        missing = [title for title in _SECTION_TITLES if title not in text]
        self.assertEqual(missing, [])

    def test_required_phrases_are_present(self) -> None:
        """Assert the catalog names the harness, subscribe, and site.

        ``make.ps1 test`` is the local harness entry. ``subscribe`` is
        a site journey. ``not live`` records that the site is not
        deployed.
        """
        self.assertTrue(_MANUAL_DOC.is_file())
        text = _MANUAL_DOC.read_text(encoding="utf-8")
        missing = [phrase for phrase in _REQUIRED_PHRASES if phrase not in text]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
