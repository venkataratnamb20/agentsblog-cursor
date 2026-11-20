"""Tests for the post-1 research pack (agents vs workflows vs chatbots).

The pack at ``research/packs/what-is-an-ai-agent.md`` gathers citeable public
sources for the Foundations post. It is research notes only: not a draft and
not a published post.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_PACK = _REPO / "research" / "packs" / "what-is-an-ai-agent.md"
_SLUG = "what-is-an-ai-agent"

# Claim terms the pack must map sources onto.
_CLAIM_TERMS = ("agent", "workflow", "chatbot")

# A source block needs a title and either an http(s) URL or a bibliographic cite.
_URL_RE = re.compile(r"https?://[^\s\)\]>]+", re.IGNORECASE)
_BIB_HINTS = (
    "arxiv:",
    "doi:",
    "isbn",
    "proceedings",
    "journal",
    "conference",
    "iclr",
    "neurips",
    "acl",
)


def _source_blocks(text: str) -> list[str]:
    """Split the Sources section into per-source blocks.

    Args:
        text: Full markdown pack.

    Returns:
        Non-empty blocks under a Sources heading.
    """
    match = re.search(
        r"^##\s+Sources\b.*?(?=^##\s|\Z)",
        text,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    body = match.group(0)
    # Prefer numbered or heading-style source entries; fall back to list items.
    parts = re.split(r"(?=^###\s+|^####\s+|^\d+\.\s+|^-\s+\*\*)", body, flags=re.MULTILINE)
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    if blocks:
        return blocks
    return [line.strip() for line in body.splitlines() if line.strip().startswith("-")]


def _looks_like_source(block: str) -> bool:
    """Return True if a block has a title cue and a URL or bibliographic cite."""
    has_title = bool(
        re.search(r"\*\*[^*]+\*\*|Title\s*:", block, flags=re.IGNORECASE)
    ) or bool(re.match(r"^(###|####|\d+\.)\s+\S+", block))
    has_url = bool(_URL_RE.search(block))
    has_bib = any(hint in block.lower() for hint in _BIB_HINTS)
    return has_title and (has_url or has_bib)


class TestResearchPackPost1(unittest.TestCase):
    """Post-1 research pack exists, cites sources, and maps the claim."""

    def test_pack_exists_and_names_slug(self) -> None:
        """Pack file exists and states the post slug."""
        self.assertTrue(_PACK.is_file(), f"missing research pack: {_PACK}")
        text = _PACK.read_text(encoding="utf-8")
        self.assertIn(_SLUG, text)

    def test_pack_lists_at_least_three_public_sources(self) -> None:
        """Sources section lists at least three titled public citations."""
        self.assertTrue(_PACK.is_file(), f"missing research pack: {_PACK}")
        text = _PACK.read_text(encoding="utf-8")
        sources = [b for b in _source_blocks(text) if _looks_like_source(b)]
        self.assertGreaterEqual(
            len(sources),
            3,
            "need at least 3 public sources with titles and URLs or bibliographic cites",
        )

    def test_pack_maps_sources_to_agent_workflow_chatbot_claim(self) -> None:
        """Claim mapping covers agent, workflow, and chatbot with source links."""
        self.assertTrue(_PACK.is_file(), f"missing research pack: {_PACK}")
        text = _PACK.read_text(encoding="utf-8")
        lower = text.lower()
        for term in _CLAIM_TERMS:
            self.assertIn(term, lower, f"pack must discuss {term}")
        # A dedicated mapping section (or equivalent) ties sources to the claim.
        self.assertRegex(
            text,
            r"(?im)^##\s+(Claim\s+mapping|Source\s+to\s+claim|Mapping)\b",
            "pack must include a claim-mapping section",
        )
        mapping = re.search(
            r"(?im)^##\s+(Claim\s+mapping|Source\s+to\s+claim|Mapping)\b.*?(?=^##\s|\Z)",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(mapping)
        mapping_text = mapping.group(0).lower()
        for term in _CLAIM_TERMS:
            self.assertIn(term, mapping_text, f"claim mapping must cover {term}")

    def test_pack_states_open_questions_confidence_and_not_published(self) -> None:
        """Open questions, confidence, and non-publication disclaimer are present."""
        self.assertTrue(_PACK.is_file(), f"missing research pack: {_PACK}")
        text = _PACK.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?im)^##\s+Open\s+questions\b")
        self.assertRegex(text, r"(?im)\bconfidence\b")
        self.assertRegex(
            text,
            r"(?is)not\s+a\s+published\s+post|research\s+notes\s+only|not\s+a\s+draft\s+post",
            "pack must state these notes are not a published post",
        )


if __name__ == "__main__":
    unittest.main()
