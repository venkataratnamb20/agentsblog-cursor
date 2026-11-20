"""Tests for the Post 2 editorial brief (anatomy of an agent).

The brief at ``docs/editorial/briefs/anatomy-of-an-agent.md`` is a planning
artifact only. It must name audience, claim, pillar, slug, and title from
the shared post-2 contract. It is not a published post and is not approved
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
    / "anatomy-of-an-agent.md"
)

_TITLE = "Anatomy of an agent: LLM, tools, memory, the ReAct loop"
_SLUG = "anatomy-of-an-agent"
_PILLAR = "Foundations"
_AUDIENCE_PHRASE = "AI engineers, researchers, and tech leads"
_CLAIM = (
    "An agent run combines a model, tools, short-term memory/state, "
    "and a ReAct-style reason-act loop; missing one piece changes "
    "the failure mode."
)


class TestBriefPost2(unittest.TestCase):
    """Post 2 brief exists with contract fields and no publish approval."""

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
            re.search(r"(?is)\b(LLM|model)\b", text)
            and re.search(r"(?is)\btools?\b", text)
            and re.search(r"(?is)\bmemory\b", text)
            and re.search(r"(?is)\bReAct\b", text)
        )
        self.assertTrue(
            claim_ok,
            "brief must state the contract claim or a clear paraphrase "
            "covering LLM/model, tools, memory, and ReAct",
        )

        _flags = re.IGNORECASE | re.DOTALL
        self.assertRegex(
            text,
            re.compile(
                r"(not|no).{0,40}(published|publication|publish)",
                _flags,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(not|no).{0,60}(approved|approval).{0,40}"
                r"(publish|publication)|"
                r"(publish|publication).{0,60}"
                r"(not|no).{0,40}(approved|approval)|"
                r"venkat.{0,80}(has not|must|before).{0,40}"
                r"(approv|publish)",
                _flags,
            ),
        )


if __name__ == "__main__":
    unittest.main()
