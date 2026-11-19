"""Tests for the GitHub Actions CI and CD workflows."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CI = _REPO_ROOT / ".github" / "workflows" / "ci.yml"
_CD = _REPO_ROOT / ".github" / "workflows" / "cd.yml"
_README = _REPO_ROOT / "README.md"
_REPO_URL = "https://github.com/venkataratnamb20/agentsblog-cursor"
_DEPLOY_MARKERS = (
    "actions/deploy-pages",
    "actions/upload-pages-artifact",
    "peaceiris/actions-gh-pages",
    "aws-actions/",
)


class TestGitHubActions(unittest.TestCase):
    """CI tests the repo. CD packages the site and does not publish it."""

    def test_readme_names_the_github_repository(self) -> None:
        """The developer entry point records the GitHub remote."""
        text = _README.read_text(encoding="utf-8")
        self.assertIn(_REPO_URL, text)

    def test_ci_runs_tests_and_the_local_build(self) -> None:
        """Pull requests and pushes run unittest and the site builder."""
        self.assertTrue(_CI.is_file(), ".github/workflows/ci.yml is missing")
        text = _CI.read_text(encoding="utf-8")
        self.assertIn("pull_request", text)
        self.assertIn("push", text)
        self.assertIn("actions/checkout@", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("python -m agentsblog.build", text)
        for marker in _DEPLOY_MARKERS:
            self.assertNotIn(marker, text)

    def test_cd_packages_the_build_and_does_not_publish(self) -> None:
        """The CD workflow uploads the build directory and does not deploy."""
        self.assertTrue(_CD.is_file(), ".github/workflows/cd.yml is missing")
        text = _CD.read_text(encoding="utf-8")
        self.assertIn("actions/checkout@", text)
        self.assertIn("python -m agentsblog.build", text)
        self.assertIn("actions/upload-artifact@", text)
        self.assertIn("build/", text)
        self.assertIn("contents: read", text)
        for marker in _DEPLOY_MARKERS:
            self.assertNotIn(marker, text)
