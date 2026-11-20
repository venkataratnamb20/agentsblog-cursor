"""Stage 0A harness artifacts: docs, scaffold, and local develop branch."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]

_REQUIRED_PATHS = (
    "docs/guidelines/git-workflow.md",
    "Makefile",
    "make.ps1",
    "docs/guidelines/code-quality.md",
    "src",
    "content",
    "tests",
    "docs",
    "research",
    "scripts",
    "tests/unit/test_scaffold.py",
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/agents-blog.mdc",
)


class TestStage0AArtifacts(unittest.TestCase):
    """Assert Stage 0A documentation and git-flow artifacts exist."""

    def test_required_artifact_paths_exist(self) -> None:
        """Every Stage 0A evidence path is present on disk."""
        missing = [
            relative
            for relative in _REQUIRED_PATHS
            if not (_REPO_ROOT / relative).exists()
        ]
        self.assertEqual(missing, [])

    def test_local_develop_branch_exists(self) -> None:
        """Local ``develop`` is present (``git show-ref refs/heads/develop``)."""
        result = subprocess.run(
            ["git", "show-ref", "refs/heads/develop"],
            cwd=_REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                "local develop branch missing; "
                f"stdout={result.stdout!r} stderr={result.stderr!r}"
            ),
        )
        self.assertIn("refs/heads/develop", result.stdout)


if __name__ == "__main__":
    unittest.main()
