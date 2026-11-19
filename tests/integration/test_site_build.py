"""Integration tests for the local static site build."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402


class TestSiteBuild(unittest.TestCase):
    """A content directory becomes browsable HTML."""

    def test_build_publishes_posts_and_skips_drafts(self) -> None:
        """Published posts are written; drafts stay out of the site.

        The index, the post page, the search index, and the not-found
        page are the files a reader can open after ``build``.
        """
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
                        "tags: agents",
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
                        "tags: agents",
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

            index = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("What is an agent?", index)
            self.assertNotIn("Secret draft", index)
            post = (output / "posts" / "what-is-an-agent.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("An agent uses tools.", post)
            self.assertFalse((output / "posts" / "secret-draft.html").exists())
            missing = (output / "404.html").read_text(encoding="utf-8")
            self.assertIn("Page not found", missing)
            catalog = json.loads(
                (output / "search-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                [item["title"] for item in catalog],
                ["What is an agent?"],
            )
            self.assertTrue((output / "assets" / "site.css").is_file())
