"""Tests for HTML page rendering."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
_RENDER_PY = _SRC / "agentsblog" / "render.py"


def _post(**overrides: Any) -> SimpleNamespace:
    """Build a post-shaped object for render tests.

    Args:
        **overrides: Attributes that replace the published-post defaults.

    Returns:
        A simple object with the post fields the renderer reads.
    """
    fields: dict[str, Any] = {
        "title": "Ship the agent",
        "slug": "ship-the-agent",
        "date": "2026-01-15",
        "tags": ["agents"],
        "summary": "How a small agent ships a page.",
        "body": "The agent writes the page and stops.",
        "draft": False,
    }
    fields.update(overrides)
    return SimpleNamespace(**fields)


def _load_render() -> Any:
    """Import ``agentsblog.render`` after the module file exists.

    ``src`` is added to ``sys.path`` only when ``render.py`` is present.
    Until then the import fails, which is the red step.

    Returns:
        The render module.

    Raises:
        ImportError: If ``agentsblog.render`` cannot be imported.
    """
    if _RENDER_PY.is_file():
        src_path = str(_SRC)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
    import agentsblog.render as render

    return render


class RenderPagesTest(unittest.TestCase):
    """HTML for the index, a post, and the not-found page."""

    def _assert_document_chrome(self, page: str) -> None:
        """Assert shared document chrome on one page.

        Args:
            page: Rendered HTML document.
        """
        self.assertIn('lang="en"', page)
        self.assertIn('href="/assets/site.css"', page)
        self.assertIn('<button id="theme-toggle"', page)

    def test_index_lists_published_posts_and_omits_drafts(self) -> None:
        """Published titles link to their pages and draft titles are absent."""
        render = _load_render()
        published = _post()
        second = _post(
            title="Evaluate the loop",
            slug="evaluate-the-loop",
            draft=False,
        )
        draft = _post(
            title="Secret draft",
            slug="secret-draft",
            draft=True,
        )
        page = render.render_index([published, draft, second])
        self.assertIn("Ship the agent", page)
        self.assertIn('href="posts/ship-the-agent.html"', page)
        self.assertIn("Evaluate the loop", page)
        self.assertIn('href="posts/evaluate-the-loop.html"', page)
        self.assertNotIn("Secret draft", page)
        self.assertNotIn("secret-draft", page)
        self._assert_document_chrome(page)

    def test_post_page_shows_heading_and_body(self) -> None:
        """A post page contains an h1 of the title and the body text."""
        render = _load_render()
        page = render.render_post(
            _post(title="Ship the agent", body="The agent writes the page."),
        )
        self.assertIn("<h1>Ship the agent</h1>", page)
        self.assertIn("The agent writes the page.", page)
        self._assert_document_chrome(page)

    def test_post_page_escapes_title_and_body(self) -> None:
        """Less-than and ampersand in a title and body are escaped."""
        render = _load_render()
        page = render.render_post(_post(title="A < B & C", body="x < y & z"))
        self.assertIn("<h1>A &lt; B &amp; C</h1>", page)
        self.assertIn("x &lt; y &amp; z", page)
        self.assertNotIn("A < B", page)
        self.assertNotIn("x < y", page)
        self._assert_document_chrome(page)

    def test_not_found_page_states_that_the_page_is_missing(self) -> None:
        """The not-found page tells the reader the page was not found."""
        render = _load_render()
        page = render.render_not_found()
        self.assertIn("Page not found", page)
        self._assert_document_chrome(page)

    def test_empty_index_still_has_document_chrome(self) -> None:
        """An index with no published posts is still a full HTML page."""
        render = _load_render()
        page = render.render_index([])
        self._assert_document_chrome(page)
