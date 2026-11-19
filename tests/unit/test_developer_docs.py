"""Tests for the developer guide."""

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEVELOPER_DOC = _REPO_ROOT / "docs" / "developers.md"
_REQUIRED_PHRASES = (
    "Prerequisites",
    "Task runner",
    "Test suite",
    "Git workflow",
    "Agent harness",
    "Progress",
    r".\make.ps1 test",
    r".\make.ps1 build",
    "python -m compileall",
)


class TestDeveloperDocs(unittest.TestCase):
    """Verify the developer guide names the harness workflow."""

    def test_developer_doc_contains_required_phrases(self) -> None:
        """Fail when the guide is missing or omits a required phrase.

        The repository root is the parent of ``tests``. Each phrase is
        an exact substring, including the Windows task-runner commands.
        """
        self.assertTrue(
            _DEVELOPER_DOC.is_file(),
            "docs/developers.md is missing",
        )
        text = _DEVELOPER_DOC.read_text(encoding="utf-8")
        missing = [
            phrase for phrase in _REQUIRED_PHRASES if phrase not in text
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
