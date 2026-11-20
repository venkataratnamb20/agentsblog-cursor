"""Tests for markdown headings and paragraphs in a post body.

Behaviour: a post body with an ATX heading and a following
paragraph renders as ``h2`` and ``p``, and raw ``<`` stays escaped.
Module: ``agentsblog.render.render_post``. Existing coverage:
``tests/unit/test_render.py`` checks a single escaped paragraph and
does not cover headings. User instruction: "/tdd-workflow Build and
fix. Check all project goals, pending goals, issues and fix them one
by one."
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.render import render_post  # noqa: E402


def _post(body: str) -> SimpleNamespace:
    """Build a post whose body is the only field under test.

    Args:
        body: Markdown source.

    Returns:
        A post-shaped object.
    """
    return SimpleNamespace(
        title="Loop",
        slug="loop",
        date="2026-12-14",
        summary="A heading and a paragraph.",
        body=body,
        draft=False,
    )


class TestMarkdownBody(unittest.TestCase):
    """Post bodies keep structure instead of one escaped paragraph."""

    def test_heading_and_paragraph_are_separate_elements(self) -> None:
        """An ATX heading is a heading. The next block is a paragraph."""
        page = render_post(_post("## Loop\n\nThe agent calls a tool."))
        self.assertIn("<h2>Loop</h2>", page)
        self.assertIn("<p>The agent calls a tool.</p>", page)

    def test_heading_text_is_escaped(self) -> None:
        """A less-than in a heading is escaped."""
        page = render_post(_post("## A < B\n\nDone."))
        self.assertIn("<h2>A &lt; B</h2>", page)
        self.assertNotIn("<h2>A < B</h2>", page)


if __name__ == "__main__":
    unittest.main()
