"""Staging smoke: posts 1–3 drafts render when drafts are included."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402

_POSTS = _REPO_ROOT / "content" / "posts"
_DRAFTS = (
    "what-is-an-ai-agent.md",
    "anatomy-of-an-agent.md",
    "tool-calling-mcp.md",
)


class TestStagingSmoke(unittest.TestCase):
    """M3 acceptance: draft posts 1–3 render on a staging-shaped build."""

    def test_repo_has_three_opening_drafts(self) -> None:
        """The content tree includes the three opening draft sources."""
        for name in _DRAFTS:
            path = _POSTS / name
            self.assertTrue(path.is_file(), f"missing draft {name}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("draft: true", text)

    def test_staging_build_renders_opening_drafts(self) -> None:
        """A drafts-included build writes pages for posts 1–3."""
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "build"
            build_site(
                _POSTS,
                output,
                site_url="https://venkataratnamb20.github.io/agentsblog-cursor",
                include_drafts=True,
                noindex=True,
            )
            index = (output / "index.html").read_text(encoding="utf-8")
            robots = (output / "robots.txt").read_text(encoding="utf-8")
            for name in _DRAFTS:
                slug = Path(name).stem
                page = (output / "posts" / f"{slug}.html").read_text(
                    encoding="utf-8"
                )
                self.assertTrue(
                    (output / "posts" / f"{slug}.html").is_file(),
                    slug,
                )
                self.assertIn("<h1>", page)
                self.assertIn(
                    'name="robots" content="noindex, nofollow"',
                    page,
                )
            self.assertIn("What is an AI agent?", index)
            self.assertIn("Anatomy of an agent", index)
            self.assertIn("Tool calling and MCP", index)
            self.assertIn("Disallow: /", robots)


if __name__ == "__main__":
    unittest.main()
