"""Unit tests for the post-1 review-ready draft.

These tests fail until ``content/posts/what-is-an-ai-agent.md`` exists
with the shared contract front matter and a body that distinguishes
agents, workflows, and chatbots. The build check confirms drafts stay
off the published index.
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402

_DRAFT_PATH = _REPO_ROOT / "content" / "posts" / "what-is-an-ai-agent.md"
_EXPECTED_TITLE = "What is an AI agent? Agents vs workflows vs chatbots"
_HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse simple ``key: value`` front matter and the body.

    Args:
        text: Full markdown document.

    Returns:
        A field map and the body after the closing fence.

    Raises:
        AssertionError: If the document has no closed front-matter fence.
    """
    if not text.startswith("---"):
        raise AssertionError("draft must start with front-matter fence")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("draft must close the front-matter fence")
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, parts[2]


class TestDraftPost1(unittest.TestCase):
    """Post-1 draft file, front matter, body, and draft omission."""

    def test_draft_file_exists(self) -> None:
        """The review-ready draft lives at the contracted path."""
        self.assertTrue(
            _DRAFT_PATH.is_file(),
            f"expected draft at {_DRAFT_PATH}",
        )

    def test_front_matter_matches_contract(self) -> None:
        """Title, non-empty summary, and draft:true match the contract."""
        text = _DRAFT_PATH.read_text(encoding="utf-8")
        fields, _ = _split_front_matter(text)
        self.assertEqual(fields.get("title"), _EXPECTED_TITLE)
        self.assertTrue(
            fields.get("summary"),
            "summary must be present and non-empty",
        )
        self.assertEqual(fields.get("draft"), "true")

    def test_body_has_headings_and_compares_three_shapes(self) -> None:
        """Body uses headings and discusses agent, workflow, and chatbot."""
        text = _DRAFT_PATH.read_text(encoding="utf-8")
        _, body = _split_front_matter(text)
        headings = _HEADING_RE.findall(body)
        self.assertGreaterEqual(
            len(headings),
            3,
            "body must include at least three markdown headings",
        )
        lowered = body.lower()
        self.assertIn("agent", lowered)
        self.assertIn("workflow", lowered)
        self.assertIn("chatbot", lowered)

    def test_build_omits_draft_from_index(self) -> None:
        """Building a temp site with this draft keeps the title off index."""
        text = _DRAFT_PATH.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            (content / "what-is-an-ai-agent.md").write_text(
                text,
                encoding="utf-8",
            )
            build_site(content, output)
            index = (output / "index.html").read_text(encoding="utf-8")
            self.assertNotIn(
                _EXPECTED_TITLE,
                index,
                "draft title must not appear on the published index",
            )


if __name__ == "__main__":
    unittest.main()
