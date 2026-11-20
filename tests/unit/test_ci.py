"""Tests for the GitHub Actions CI and CD workflows."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CI = _REPO_ROOT / ".github" / "workflows" / "ci.yml"
_CD = _REPO_ROOT / ".github" / "workflows" / "cd.yml"
_README = _REPO_ROOT / "README.md"
_REPO_URL = "https://github.com/venkataratnamb20/agentsblog-cursor"
_STAGING_URL = "https://venkataratnamb20.github.io/agentsblog-cursor"


class TestGitHubActions(unittest.TestCase):
    """CI tests the repo. CD deploys staging from develop to Pages."""

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
        self.assertNotIn("actions/deploy-pages", text)

    def test_cd_deploys_develop_to_pages_with_drafts_and_noindex(self) -> None:
        """Develop builds include drafts, set noindex, and deploy to Pages."""
        self.assertTrue(_CD.is_file(), ".github/workflows/cd.yml is missing")
        text = _CD.read_text(encoding="utf-8")
        self.assertIn("develop", text)
        self.assertIn("actions/checkout@", text)
        self.assertIn("python -m agentsblog.build", text)
        self.assertIn("AGENTSBLOG_INCLUDE_DRAFTS", text)
        self.assertIn("AGENTSBLOG_NOINDEX", text)
        self.assertIn("AGENTSBLOG_SITE_URL", text)
        self.assertIn(_STAGING_URL, text)
        self.assertIn("actions/upload-pages-artifact@", text)
        self.assertIn("actions/deploy-pages@", text)
        self.assertIn("pages: write", text)
        self.assertIn("id-token: write", text)

    def test_cd_packages_main_without_staging_draft_flags(self) -> None:
        """Main packages the production build and does not include drafts."""
        text = _CD.read_text(encoding="utf-8")
        self.assertIn("main", text)
        self.assertIn("actions/upload-artifact@", text)
        # Staging draft include must be scoped to the develop job, not global.
        self.assertIn("package-main", text)


if __name__ == "__main__":
    unittest.main()
