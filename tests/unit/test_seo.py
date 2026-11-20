"""Tests for technical SEO files and page metadata.

Behaviour: the build writes robots.txt and sitemap.xml, and post
pages carry a canonical URL, Open Graph title, description, and
schema.org BlogPosting. Drafts stay out of the sitemap. Module:
``agentsblog.seo`` plus ``agentsblog.render`` and
``agentsblog.build``. Existing tests: none for SEO. User instruction:
"/tdd-workflow Build and fix. Check all project goals, pending goals,
issues and fix them one by one."
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
from agentsblog.render import render_index, render_post  # noqa: E402
from agentsblog.seo import render_robots, render_sitemap  # noqa: E402

_SITE = "http://127.0.0.1:8000"


def _post(**overrides: object) -> SimpleNamespace:
    """Build a post-shaped object for SEO tests.

    Args:
        **overrides: Fields that replace the published defaults.

    Returns:
        An object with the fields the renderer and sitemap read.
    """
    fields: dict[str, object] = {
        "title": "What is an agent?",
        "slug": "what-is-an-agent",
        "date": "2026-12-14",
        "summary": "A short definition",
        "body": "An agent uses tools.",
        "draft": False,
    }
    fields.update(overrides)
    return SimpleNamespace(**fields)


class TestSeo(unittest.TestCase):
    """Robots, sitemap, and on-page metadata."""

    def test_robots_allows_the_site_and_names_the_sitemap(self) -> None:
        """Crawlers may read the site and can find the sitemap."""
        text = render_robots(_SITE)
        self.assertIn("User-agent: *", text)
        self.assertIn("Allow: /", text)
        self.assertIn(f"Sitemap: {_SITE}/sitemap.xml", text)

    def test_sitemap_lists_absolute_locations(self) -> None:
        """Each location is an absolute URL in a urlset."""
        xml = render_sitemap([f"{_SITE}/", f"{_SITE}/search.html"])
        self.assertIn("<urlset", xml)
        self.assertIn(f"<loc>{_SITE}/</loc>", xml)
        self.assertIn(f"<loc>{_SITE}/search.html</loc>", xml)

    def test_post_page_has_canonical_open_graph_and_schema(self) -> None:
        """A post page names its URL, title, description, and type."""
        page = render_post(
            _post(title="A < B", summary="Tools & memory"),
            _SITE,
        )
        self.assertIn('rel="canonical"', page)
        self.assertIn(f"{_SITE}/posts/what-is-an-agent.html", page)
        self.assertIn('property="og:title"', page)
        self.assertIn("A &lt; B", page)
        self.assertNotIn("A < B", page)
        self.assertIn("Tools &amp; memory", page)
        self.assertIn('type="application/ld+json"', page)
        self.assertIn("BlogPosting", page)

    def test_index_has_a_canonical_url(self) -> None:
        """The index canonical points at the site origin."""
        page = render_index([], _SITE)
        self.assertIn('rel="canonical"', page)
        self.assertIn(f"{_SITE}/", page)

    def test_build_writes_robots_and_sitemap_without_drafts(self) -> None:
        """Draft slugs are absent from sitemap.xml."""
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
            build_site(content, output, _SITE)
            robots = (output / "robots.txt").read_text(encoding="utf-8")
            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(f"Sitemap: {_SITE}/sitemap.xml", robots)
        self.assertIn(f"{_SITE}/posts/what-is-an-agent.html", sitemap)
        self.assertNotIn("secret-draft", sitemap)


if __name__ == "__main__":
    unittest.main()
