"""Tests for the local repo-only research reference library.

The library lives under ``research/``. Notes and source lists stay in
the repository. Zotero and Notion accounts are not created until Venkat
approves. Module: documentation only. Existing tests: none.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_RESEARCH_README = _REPO_ROOT / "research" / "README.md"
_SOURCES_README = _REPO_ROOT / "research" / "sources" / "README.md"

# Phrases the research README must state explicitly.
_REQUIRED_PHRASES = (
    "in-repo",
    "research/packs/",
    "Zotero",
    "Notion",
    "Venkat",
    "approval",
    "not created",
    "secrets",
)

# Markers that must not appear in research library docs.
_SECRET_MARKERS = (
    "AKIA",
    "BEGIN PRIVATE KEY",
    "api_key=",
    "api_key:",
    "password=",
    "token=",
    ".env",
)


class TestResearchLibrary(unittest.TestCase):
    """Local research library docs exist and stay account-free."""

    def test_research_readme_exists(self) -> None:
        """``research/README.md`` must be present."""
        self.assertTrue(
            _RESEARCH_README.is_file(),
            "research/README.md is missing",
        )

    def test_sources_readme_exists(self) -> None:
        """``research/sources/README.md`` must be present."""
        self.assertTrue(
            _SOURCES_README.is_file(),
            "research/sources/README.md is missing",
        )

    def test_research_readme_explains_local_library(self) -> None:
        """README explains in-repo notes, packs path, and approval wait.

        Notes are stored in the repository. Packs live under
        ``research/packs/``. Zotero and Notion accounts are not created
        and wait for Venkat approval. No secret-shaped strings.
        """
        self.assertTrue(
            _RESEARCH_README.is_file(),
            "research/README.md is missing",
        )
        text = _RESEARCH_README.read_text(encoding="utf-8")
        missing = [
            phrase for phrase in _REQUIRED_PHRASES if phrase not in text
        ]
        self.assertEqual(
            missing,
            [],
            f"research/README.md missing required phrases: {missing}",
        )
        lower = text.lower()
        self.assertTrue(
            "note" in lower and ("stor" in lower or "keep" in lower),
            "research/README.md must explain how notes are stored in-repo",
        )
        for marker in _SECRET_MARKERS:
            self.assertNotIn(
                marker,
                text,
                f"research/README.md must not contain secret marker {marker!r}",
            )

    def test_sources_readme_has_no_secrets(self) -> None:
        """``research/sources/README.md`` must not contain secret markers."""
        self.assertTrue(
            _SOURCES_README.is_file(),
            "research/sources/README.md is missing",
        )
        text = _SOURCES_README.read_text(encoding="utf-8")
        for marker in _SECRET_MARKERS:
            self.assertNotIn(
                marker,
                text,
                f"research/sources/README.md must not contain "
                f"secret marker {marker!r}",
            )


if __name__ == "__main__":
    unittest.main()
