"""Tests for the RSS feed.

Behaviour: published posts appear in an RSS 2.0 feed and drafts do
not. Module: ``agentsblog.feed.render_feed`` and
``agentsblog.build.build_site``. Existing tests: none.
``tests/unit/test_user_docs.py`` only requires the word RSS in the
reader guide. User instruction: "/tdd-workflow Build and fix. Check
all project goals, pending goals, issues and fix them one by one."
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402
from agentsblog.feed import render_feed  # noqa: E402
from agentsblog.render import render_index  # noqa: E402

_SITE = "http://127.0.0.1:8000"


def _post(**overrides: object) -> SimpleNamespace:
    """Build a post-shaped object for feed tests.

    Args:
        **overrides: Fields that replace the published defaults.

    Returns:
        An object with the fields the feed reads.
    """
    fields: dict[str, object] = {
        "title": "What is an agent?",
        "slug": "what-is-an-agent",
        "date": "2026-12-14",
        "summary": "A short definition",
        "draft": False,
    }
    fields.update(overrides)
    return SimpleNamespace(**fields)


class TestFeed(unittest.TestCase):
    """The feed lists published posts and skips drafts."""

    def test_feed_includes_published_posts_and_skips_drafts(self) -> None:
        """A published title and link are present. A draft title is not."""
        feed = render_feed(
            [
                _post(),
                _post(title="Secret draft", slug="secret-draft", draft=True),
            ],
            _SITE,
        )
        self.assertIn("<rss", feed)
        self.assertIn("What is an agent?", feed)
        self.assertIn(f"{_SITE}/posts/what-is-an-agent.html", feed)
        self.assertNotIn("Secret draft", feed)

    def test_empty_feed_has_a_channel_and_no_items(self) -> None:
        """An empty post list is still a valid channel."""
        feed = render_feed([], _SITE)
        self.assertIn("<channel>", feed)
        self.assertNotIn("<item>", feed)

    def test_feed_escapes_title_text(self) -> None:
        """A less-than in a title is escaped in the XML."""
        feed = render_feed([_post(title="A < B")], _SITE)
        self.assertIn("A &lt; B", feed)
        self.assertNotIn("A < B", feed)

    def test_index_links_the_feed(self) -> None:
        """Pages advertise the feed to feed readers."""
        page = render_index([])
        self.assertIn('type="application/rss+xml"', page)
        self.assertIn('href="/feed.xml"', page)

    def test_build_writes_feed_xml(self) -> None:
        """``build_site`` writes ``feed.xml`` for published posts only."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            (content / "what-is-an-agent.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: What is an agent?",
                        "date: 2026-12-14",
                        "summary: A short definition",
                        "draft: false",
                        "---",
                        "An agent uses tools.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (content / "secret-draft.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Secret draft",
                        "date: 2026-12-15",
                        "summary: Hidden",
                        "draft: true",
                        "---",
                        "Do not publish.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            build_site(content, output)
            feed = (output / "feed.xml").read_text(encoding="utf-8")
        self.assertIn("What is an agent?", feed)
        self.assertNotIn("Secret draft", feed)


if __name__ == "__main__":
    unittest.main()
