"""SEO audit of the local static build.

The audit reads a temporary site from ``agentsblog.build.build_site``.
It checks robots.txt, sitemap.xml, canonical URLs, Open Graph, one
heading, and draft exclusion. It also requires the written audit
record. The site is not submitted to a search engine.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402

_REPO = Path(__file__).resolve().parents[2]
_AUDIT = _REPO / "docs" / "seo" / "audit.md"
_LOCAL_ORIGIN = "http://127.0.0.1:8000"
_PUBLISHED_SLUG = "canonical-urls"
_DRAFT_SLUG = "hidden-draft"
_AUDIT_PHRASES = (
    "local preview",
    "canonical",
    "Open Graph",
    "draft",
    "not submitted",
)


def _front_matter(
    title: str,
    summary: str,
    tags: str,
    draft: bool,
) -> str:
    """Return markdown a real post parser accepts.

    Args:
        title: Required front-matter title.
        summary: Short description.
        tags: Comma-separated tag names.
        draft: Whether the post stays unpublished.

    Returns:
        A fenced markdown document with a plain paragraph body.
    """
    flag = "true" if draft else "false"
    return "\n".join(
        [
            "---",
            f"title: {title}",
            "date: 2026-12-14",
            f"summary: {summary}",
            f"tags: {tags}",
            f"draft: {flag}",
            "---",
            "A published page belongs in the local preview.",
            "",
        ]
    )


class TestSeoAudit(unittest.TestCase):
    """Local preview metadata, discovery files, and the audit record."""

    def test_local_preview_sets_canonical_and_excludes_the_draft(self) -> None:
        """Omitted site_url uses the local origin and hides the draft."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            (content / f"{_PUBLISHED_SLUG}.md").write_text(
                _front_matter(
                    title="Canonical URLs on the local preview",
                    summary="How the preview sets a canonical URL",
                    tags="canonical, preview",
                    draft=False,
                ),
                encoding="utf-8",
            )
            (content / f"{_DRAFT_SLUG}.md").write_text(
                _front_matter(
                    title="Hidden draft note",
                    summary="This draft stays out of discovery files",
                    tags="draft",
                    draft=True,
                ),
                encoding="utf-8",
            )
            build_site(content, output)
            robots = (output / "robots.txt").read_text(encoding="utf-8")
            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
            page = (output / "posts" / f"{_PUBLISHED_SLUG}.html").read_text(
                encoding="utf-8",
            )
        self.assertIn("Sitemap", robots)
        self.assertNotIn(_DRAFT_SLUG, robots)
        self.assertIn(_PUBLISHED_SLUG, sitemap)
        self.assertNotIn(_DRAFT_SLUG, sitemap)
        self.assertIn('rel="canonical"', page)
        self.assertIn('property="og:title"', page)
        self.assertEqual(page.count("<h1"), 1)
        self.assertIn(
            f'rel="canonical" href="{_LOCAL_ORIGIN}/posts/{_PUBLISHED_SLUG}.html"',
            page,
        )

    def test_audit_record_names_the_local_preview_checks(self) -> None:
        """The audit note exists and states it was not submitted."""
        self.assertTrue(_AUDIT.is_file(), "docs/seo/audit.md is missing")
        text = _AUDIT.read_text(encoding="utf-8")
        for phrase in _AUDIT_PHRASES:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
