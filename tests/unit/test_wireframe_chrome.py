"""Tests for Stage 3 wireframe chrome on shared and home pages.

Behaviour: shared footer and theme order match wireframes; home shows
tagline, pillars, and list anatomy; 404 links home; posts show
published date and series chrome when metadata exists.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.render import (  # noqa: E402
    render_about,
    render_index,
    render_not_found,
    render_post,
    render_tag_page,
)


def _post(**overrides: Any) -> SimpleNamespace:
    """Build a post-shaped object for chrome tests.

    Args:
        **overrides: Fields that replace the published defaults.

    Returns:
        An object with the fields the renderer reads.
    """
    fields: dict[str, Any] = {
        "title": "Ship the agent",
        "slug": "ship-the-agent",
        "date": "2026-01-15",
        "tags": ["agents"],
        "summary": "How a small agent ships a page.",
        "body": "The agent writes the page and stops.",
        "draft": False,
        "series": "",
        "series_part": 0,
        "series_total": 0,
    }
    fields.update(overrides)
    return SimpleNamespace(**fields)


class TestWireframeChrome(unittest.TestCase):
    """Shared chrome and reader surfaces match Stage 3 wireframes."""

    def test_theme_toggle_comes_before_main(self) -> None:
        """Focus order places the theme control after nav and before main."""
        page = render_index([])
        nav = page.find("<nav>")
        toggle = page.find('id="theme-toggle"')
        main = page.find('<main id="main">')
        self.assertNotEqual(nav, -1)
        self.assertNotEqual(toggle, -1)
        self.assertNotEqual(main, -1)
        self.assertLess(nav, toggle)
        self.assertLess(toggle, main)

    def test_footer_lists_policy_links(self) -> None:
        """Footer links Cookies, Terms, Licences, and AI assistance."""
        page = render_index([])
        footer_start = page.find("<footer>")
        self.assertNotEqual(footer_start, -1)
        footer = page[footer_start:]
        self.assertIn('href="/cookies.html"', footer)
        self.assertIn("Cookies", footer)
        self.assertIn('href="/terms.html"', footer)
        self.assertIn("Terms", footer)
        self.assertIn('href="/licences.html"', footer)
        self.assertIn("Licences", footer)
        self.assertIn('href="/ai-assistance.html"', footer)
        self.assertIn("AI assistance", footer)

    def test_index_shows_tagline_pillars_and_list_anatomy(self) -> None:
        """Home brand, tagline, pillars, and post list match the wireframe."""
        page = render_index([_post()])
        self.assertIn("<h1>Agents Blog</h1>", page)
        self.assertIn(
            "Clear writing for people who build AI agents.",
            page,
        )
        self.assertIn("Foundations", page)
        self.assertIn("Building", page)
        self.assertIn("Evaluation", page)
        self.assertIn("Safety", page)
        self.assertIn("Operations", page)
        self.assertIn("Ship the agent", page)
        self.assertIn("2026-01-15", page)
        self.assertIn("How a small agent ships a page.", page)
        self.assertNotIn(">Search</a></p>", page)

    def test_not_found_links_back_to_home(self) -> None:
        """The 404 page offers a link back to the home page."""
        page = render_not_found()
        self.assertIn("Page not found", page)
        self.assertIn('href="/"', page)
        self.assertIn("Back to Home", page)

    def test_about_includes_tagline(self) -> None:
        """About repeats the brand tagline under the audience sentence."""
        page = render_about()
        self.assertIn(
            "Clear writing for people who build AI agents.",
            page,
        )

    def test_post_shows_published_date_and_tagged_links(self) -> None:
        """A post page labels the published date and tags."""
        page = render_post(_post())
        self.assertIn("Published: 2026-01-15", page)
        self.assertIn("Tags:", page)
        self.assertIn('href="/tags/agents.html"', page)

    def test_post_series_chrome_when_metadata_present(self) -> None:
        """Series posts show part n of m and prev/next sibling links."""
        page = render_post(
            _post(
                series="Anatomy",
                series_part=2,
                series_total=3,
                series_prev_slug="part-one",
                series_prev_title="Part one",
                series_next_slug="part-three",
                series_next_title="Part three",
            )
        )
        self.assertIn("Part 2 of 3", page)
        self.assertIn("Anatomy", page)
        self.assertIn('href="/posts/part-one.html"', page)
        self.assertIn("Previous: Part one", page)
        self.assertIn('href="/posts/part-three.html"', page)
        self.assertIn("Next: Part three", page)

    def test_tag_page_uses_list_anatomy(self) -> None:
        """Tag pages list title, date, and dek for each post."""
        page = render_tag_page("agents", [_post()])
        self.assertIn("Ship the agent", page)
        self.assertIn("2026-01-15", page)
        self.assertIn("How a small agent ships a page.", page)


if __name__ == "__main__":
    unittest.main()
