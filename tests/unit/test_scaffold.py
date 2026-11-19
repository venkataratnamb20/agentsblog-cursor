"""Tests for the stack-agnostic repository scaffold."""

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REQUIRED_DIRECTORIES = (
    "src",
    "content",
    "tests",
    "docs",
    "research",
    "scripts",
)


class TestScaffoldLayout(unittest.TestCase):
    """Verify required top-level directories exist."""

    def test_required_top_level_directories_exist(self) -> None:
        """Assert the scaffold directories are present on disk.

        The check is path-based so it stays valid before a framework
        is chosen. The repository root is the parent of ``tests``.
        """
        missing = [
            name
            for name in _REQUIRED_DIRECTORIES
            if not (_REPO_ROOT / name).is_dir()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
