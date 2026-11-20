"""Tests for the about page, the subscribe page, and tag pages.

Behaviour: the build writes about.html and subscribe.html, and one
page per published tag. Subscribe has no email form. Module:
``agentsblog.build``. Existing tests cover search, feed, and policy
pages, not these pages. User instruction: "Go ahead and complete the
next goals. Deploy multiple agents with similar and relevant skills
with gitworktree."
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

_SUBSCRIBE = "Subscribe is blocked until an email service is approved"


def _write(directory: Path, name: str, lines: list[str]) -> None:
    """Write one markdown post into a temporary content directory.

    Args:
        directory: Content directory.
        name: File name.
        lines: Full file lines, including front matter.
    """
    (directory / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestAboutAndSubscribe(unittest.TestCase):
    """About and subscribe pages on the local preview."""

    def test_build_writes_about_and_subscribe(self) -> None:
        """About names the audience. Subscribe does not collect email."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(content, output)
            about = (output / "about.html").read_text(encoding="utf-8")
            subscribe = (output / "subscribe.html").read_text(encoding="utf-8")
            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("technical blog on AI agents", about)
        self.assertIn("engineers, researchers, and tech leads", about)
        self.assertIn("The public site is not live.", about)
        self.assertIn(_SUBSCRIBE, subscribe)
        self.assertNotIn("<form", subscribe)
        self.assertNotIn('type="email"', subscribe)
        self.assertIn("/about.html", sitemap)
        self.assertIn("/subscribe.html", sitemap)


class TestTagPages(unittest.TestCase):
    """One page per tag on published posts."""

    def test_tag_page_lists_published_posts_and_skips_drafts(self) -> None:
        """A published tag is a page. A draft-only tag is not."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            _write(
                content,
                "loop.md",
                [
                    "---",
                    "title: The loop",
                    "date: 2026-12-14",
                    "tags: AI Agents, Long Term",
                    "summary: A loop",
                    "draft: false",
                    "---",
                    "The agent loops.",
                ],
            )
            _write(
                content,
                "secret.md",
                [
                    "---",
                    "title: Secret draft",
                    "date: 2026-12-15",
                    "tags: Hidden Topic",
                    "summary: Hidden",
                    "draft: true",
                    "---",
                    "Do not publish.",
                ],
            )
            build_site(content, output)
            agents = (output / "tags" / "ai-agents.html").read_text(encoding="utf-8")
            memory = (output / "tags" / "long-term.html").read_text(encoding="utf-8")
            post = (output / "posts" / "loop.html").read_text(encoding="utf-8")
            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("The loop", agents)
        self.assertIn("posts/loop.html", agents)
        self.assertNotIn("Secret draft", agents)
        self.assertIn("The loop", memory)
        self.assertFalse((output / "tags" / "hidden-topic.html").exists())
        self.assertIn('href="/tags/ai-agents.html"', post)
        self.assertIn("/tags/long-term.html", sitemap)


if __name__ == "__main__":
    unittest.main()
