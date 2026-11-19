"""Integration checks for the repository contract."""

from __future__ import annotations

import compileall
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


class TestRepoContract(unittest.TestCase):
    """Verify the tree compiles and the scaffold directories exist."""

    def test_sync_agents_and_tests_compile(self) -> None:
        """Assert ``scripts/sync_agents.py`` and ``tests/`` compile.

        ``compileall`` is the standard-library compiler. A false result
        means a syntax error in the sync script or the test tree.
        """
        script = _REPO_ROOT / "scripts" / "sync_agents.py"
        self.assertTrue(script.is_file())
        self.assertTrue(
            compileall.compile_file(str(script), quiet=1),
            msg=f"compileall failed for {script}",
        )
        tests_dir = _REPO_ROOT / "tests"
        self.assertTrue(
            compileall.compile_dir(str(tests_dir), quiet=1),
            msg=f"compileall failed for {tests_dir}",
        )

    def test_required_directories_exist(self) -> None:
        """Assert the contract directories are present on disk.

        The names match the folder map in ``AGENTS.md``. The check is
        path-based and does not import application code.
        """
        missing = [
            name
            for name in _REQUIRED_DIRECTORIES
            if not (_REPO_ROOT / name).is_dir()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
