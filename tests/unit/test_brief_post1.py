"""Tests for the Post 1 editorial brief (agents vs workflows vs chatbots).

The brief at ``docs/editorial/briefs/what-is-an-ai-agent.md`` is a planning
artifact only. It must name audience, claim, pillar, slug, and title from
the shared post-1 contract. It is not a published post and is not approved
for publication.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

_BRIEF = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "editorial"
    / "briefs"
    / "what-is-an-ai-agent.md"
)

_TITLE = "What is an AI agent? Agents vs workflows vs chatbots"
_SLUG = "what-is-an-ai-agent"
_PILLAR = "Foundations"
_AUDIENCE_PHRASE = "AI engineers, researchers, and tech leads"
_CLAIM = (
    "An agent is a goal-directed loop that chooses tools; "
    "a workflow is a fixed graph; "
    "a chatbot is turn-based chat without tool autonomy"
)


class TestBriefPost1(unittest.TestCase):
    """Post 1 brief exists with contract fields and no publish approval."""

    def test_brief_exists_with_contract_fields_and_is_unpublished(self) -> None:
        """Assert path, title, slug, pillar, audience, claim, not published."""
        self.assertTrue(
            _BRIEF.is_file(),
            f"missing editorial brief: {_BRIEF}",
        )
        text = _BRIEF.read_text(encoding="utf-8")

        self.assertIn(_TITLE, text)
        self.assertIn(_SLUG, text)
        self.assertIn(_PILLAR, text)
        self.assertIn(_AUDIENCE_PHRASE, text)

        claim_ok = _CLAIM in text or (
            re.search(r"(?is)\bagent\b", text)
            and re.search(r"(?is)\bworkflow\b", text)
            and re.search(r"(?is)\bchatbot\b", text)
            and re.search(r"(?is)goal[- ]directed|loop|tools?", text)
        )
        self.assertTrue(
            claim_ok,
            "brief must state the contract claim or a clear paraphrase "
            "covering agent, workflow, and chatbot",
        )

        self.assertRegex(
            text,
            re.compile(
                r"(?is)(not|no).{0,40}(published|publication|publish)"
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(?is)"
                r"(not|no).{0,60}(approved|approval).{0,40}"
                r"(publish|publication)|"
                r"(publish|publication).{0,60}"
                r"(not|no).{0,40}(approved|approval)|"
                r"venkat.{0,80}(has not|must|before).{0,40}"
                r"(approv|publish)"
            ),
        )


if __name__ == "__main__":
    unittest.main()
