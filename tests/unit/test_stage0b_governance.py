"""Tests for stage 0B governance documents.

Behaviour: the four stage 0B policy files exist under ``docs/`` and
state roles/RACI, approval gates, secrets outside the repo, and a
definition of done. Module: documentation only. Existing tests: none.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

_TEAM = _REPO / "docs" / "team.md"
_APPROVAL = _REPO / "docs" / "governance" / "approval-gates.md"
_SECRETS = _REPO / "docs" / "governance" / "secrets.md"
_OPERATING = _REPO / "docs" / "governance" / "operating-model.md"

_GOVERNANCE_DOCS = (_TEAM, _APPROVAL, _SECRETS, _OPERATING)


class TestStage0BGovernance(unittest.TestCase):
    """Stage 0B governance docs exist and carry the required phrases."""

    def test_governance_docs_exist(self) -> None:
        """Each of the four stage 0B governance files is on disk."""
        for path in _GOVERNANCE_DOCS:
            with self.subTest(path=path.as_posix()):
                self.assertTrue(path.is_file(), f"missing {path}")

    def test_team_doc_names_roles_or_raci(self) -> None:
        """Team roster states roles or a RACI."""
        text = _TEAM.read_text(encoding="utf-8")
        has_raci = "RACI" in text or "raci" in text
        has_roles = "Roles" in text or "roles" in text
        self.assertTrue(
            has_raci or has_roles,
            "docs/team.md must mention RACI or roles",
        )

    def test_approval_gates_doc_mentions_approval(self) -> None:
        """Approval-gates policy mentions approval."""
        text = _APPROVAL.read_text(encoding="utf-8")
        self.assertIn("approval", text.lower())

    def test_secrets_doc_keeps_secrets_out_of_repo(self) -> None:
        """Secrets policy keeps secrets out of the repository."""
        text = _SECRETS.read_text(encoding="utf-8").lower()
        self.assertIn("secret", text)
        self.assertTrue(
            "repository" in text or "repo" in text,
            "docs/governance/secrets.md must refer to the repo",
        )
        keeps_out = (
            "zero secrets" in text
            or "not commit" in text
            or "never" in text
            or "outside the repository" in text
            or "outside the repo" in text
        )
        self.assertTrue(
            keeps_out,
            "docs/governance/secrets.md must say secrets stay out of the repo",
        )

    def test_operating_model_defines_done(self) -> None:
        """Operating model states a definition of done."""
        text = _OPERATING.read_text(encoding="utf-8").lower()
        self.assertIn("definition of done", text)


if __name__ == "__main__":
    unittest.main()
