"""Tests for staging build flags: drafts, site URL, and noindex.

Behaviour: ``include_drafts`` writes draft post pages and lists them;
``noindex`` blocks crawlers; ``site_url`` drives canonicals. Local
defaults still exclude drafts and allow indexing.
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
from agentsblog.seo import render_robots  # noqa: E402


def _write(directory: Path, name: str, lines: list[str]) -> None:
    """Write one markdown post into a temporary content directory.

    Args:
        directory: Content directory.
        name: File name.
        lines: Full file lines, including front matter.
    """
    (directory / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestStagingBuild(unittest.TestCase):
    """Staging flags for GitHub Pages review builds."""

    def test_include_drafts_writes_draft_post_pages(self) -> None:
        """A staging build includes draft posts in pages and the index."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            _write(
                content,
                "secret.md",
                [
                    "---",
                    "title: Secret draft",
                    "date: 2026-12-15",
                    "tags: agents",
                    "summary: Hidden on production",
                    "draft: true",
                    "---",
                    "Do not publish yet.",
                ],
            )
            build_site(
                content,
                output,
                site_url="https://example.github.io/agentsblog",
                include_drafts=True,
                noindex=True,
            )
            index = (output / "index.html").read_text(encoding="utf-8")
            post = (output / "posts" / "secret.html").read_text(encoding="utf-8")
            robots = (output / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Secret draft", index)
        self.assertIn("Hidden on production", index)
        self.assertIn("Secret draft", post)
        self.assertIn('name="robots" content="noindex, nofollow"', post)
        self.assertIn("Disallow: /", robots)
        self.assertNotIn("Allow: /", robots)

    def test_default_build_still_omits_drafts(self) -> None:
        """The local default build keeps drafts out of public artifacts."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            _write(
                content,
                "secret.md",
                [
                    "---",
                    "title: Secret draft",
                    "date: 2026-12-15",
                    "summary: Hidden",
                    "draft: true",
                    "---",
                    "Do not publish.",
                ],
            )
            build_site(content, output)
            index = (output / "index.html").read_text(encoding="utf-8")
            robots = (output / "robots.txt").read_text(encoding="utf-8")
        self.assertNotIn("Secret draft", index)
        self.assertFalse((output / "posts" / "secret.html").exists())
        self.assertIn("Allow: /", robots)

    def test_robots_noindex_helper_disallows_all(self) -> None:
        """``render_robots`` can emit a disallow-all staging policy."""
        text = render_robots("https://example.github.io/x", noindex=True)
        self.assertIn("Disallow: /", text)
        self.assertNotIn("Allow: /", text)


if __name__ == "__main__":
    unittest.main()
