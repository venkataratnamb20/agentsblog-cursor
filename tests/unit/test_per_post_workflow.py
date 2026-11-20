"""Tests for the per-post editorial workflow.

The document at ``docs/editorial/per-post-workflow.md`` names the stage
order, one Agent Owner per stage, Venkat approval gates for Publish and
Distribute, and the operating-model hand-off fields. It does not publish
posts or create accounts.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / "docs" / "editorial" / "per-post-workflow.md"
_TEAM = _REPO_ROOT / "docs" / "team.md"

# Ordered stage names the workflow must list exactly once each, in order.
_STAGES = (
    "Brief",
    "Draft",
    "Tech edit",
    "SEO",
    "Approval",
    "Publish",
    "Distribute",
)

# Agent Owner for each stage. Approval is Venkat (human principal).
_STAGE_OWNERS = {
    "Brief": "Product Strategist",
    "Draft": "Technical Writer",
    "Tech edit": "Technical Editor",
    "SEO": "SEO & Analytics",
    "Approval": "Venkat",
    "Publish": "DevOps & SRE",
    "Distribute": "Growth & Community",
}

_HAND_OFF_FIELDS = (
    "Artifact link",
    "Summary",
    "Open questions",
)


def _stage_heading_positions(text: str) -> list[tuple[str, int]]:
    """Return ``(stage, index)`` for each required stage heading.

    Args:
        text: Full workflow markdown.

    Returns:
        Positions of stage headings found via ``### <stage>``.
    """
    found: list[tuple[str, int]] = []
    for stage in _STAGES:
        match = re.search(
            rf"^###\s+{re.escape(stage)}\s*$",
            text,
            flags=re.MULTILINE,
        )
        if match is not None:
            found.append((stage, match.start()))
    return found


class TestPerPostWorkflow(unittest.TestCase):
    """Per-post workflow names stages, owners, gates, and hand-off."""

    def test_workflow_lists_stages_in_order(self) -> None:
        """Stages appear as ``###`` headings in the required order."""
        self.assertTrue(
            _WORKFLOW.is_file(),
            f"missing per-post workflow: {_WORKFLOW}",
        )
        text = _WORKFLOW.read_text(encoding="utf-8")
        found = _stage_heading_positions(text)
        self.assertEqual(
            [stage for stage, _ in found],
            list(_STAGES),
            "workflow must name Brief → Draft → Tech edit → SEO → "
            "Approval → Publish → Distribute as ### headings in order",
        )
        positions = [pos for _, pos in found]
        self.assertEqual(positions, sorted(positions))

    def test_each_stage_names_agent_owner_from_team(self) -> None:
        """Each stage names an Agent Owner that exists in ``docs/team.md``."""
        self.assertTrue(_WORKFLOW.is_file(), f"missing: {_WORKFLOW}")
        self.assertTrue(_TEAM.is_file(), f"missing team roster: {_TEAM}")
        text = _WORKFLOW.read_text(encoding="utf-8")
        team_text = _TEAM.read_text(encoding="utf-8")
        for stage, owner in _STAGE_OWNERS.items():
            if owner != "Venkat":
                self.assertIn(
                    owner,
                    team_text,
                    f"owner {owner!r} for {stage} must appear in docs/team.md",
                )
            # Owner must appear near the stage heading (same section).
            pattern = (
                rf"###\s+{re.escape(stage)}\s*\n"
                rf"(?:.*\n){{0,12}}?"
                rf".*Agent Owner.*{re.escape(owner)}"
            )
            self.assertRegex(
                text,
                pattern,
                f"stage {stage!r} must name Agent Owner {owner!r}",
            )

    def test_publish_and_distribute_require_venkat_approval(self) -> None:
        """Publish and Distribute stay gated; drafts stay unpublished."""
        self.assertTrue(_WORKFLOW.is_file(), f"missing: {_WORKFLOW}")
        text = _WORKFLOW.read_text(encoding="utf-8")
        for stage in ("Publish", "Distribute"):
            self.assertRegex(
                text,
                rf"###\s+{stage}\s*\n(?:.*\n){{0,20}}?.*Venkat",
                f"{stage} must require Venkat's approval",
            )
        self.assertIn("Venkat", text)
        self.assertRegex(
            text,
            r"(?i)drafts?\s+stay\s+unpublished|unpublished\s+until|"
            r"remain\s+unpublished\s+until",
            "workflow must state drafts stay unpublished until Venkat "
            "approves Publish",
        )
        self.assertIn("approval", text.lower())

    def test_hand_off_uses_operating_model_fields(self) -> None:
        """Hand-off requires artifact link, summary, and open questions."""
        self.assertTrue(_WORKFLOW.is_file(), f"missing: {_WORKFLOW}")
        text = _WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"(?i)hand[- ]off",
            "workflow must describe the hand-off protocol",
        )
        for field in _HAND_OFF_FIELDS:
            self.assertIn(
                field,
                text,
                f"hand-off must name {field!r} from the operating model",
            )
        self.assertIn("operating-model", text)


if __name__ == "__main__":
    unittest.main()
