"""Tests for loading markdown posts with front matter."""

from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(_SRC))

from agentsblog.posts import Post, load_posts


def _write(directory: Path, name: str, content: str) -> None:
    """Write one fixture file into a post directory.

    Args:
        directory: Directory that receives the file.
        name: File name, including the suffix.
        content: Full file text.
    """
    (directory / name).write_text(content, encoding="utf-8")


def _post(
    title: str | None,
    date: str,
    *,
    tags: str = "agents",
    summary: str = "Short text",
    body: str = "Body paragraph.",
    draft: bool | None = False,
) -> str:
    """Build a markdown post with front matter.

    Args:
        title: Title value. None omits the field.
        date: Publication date.
        tags: Comma-separated tags.
        summary: Short description.
        body: Text after the closing fence.
        draft: Draft flag. None omits the field.

    Returns:
        Markdown file contents.
    """
    lines = ["---"]
    if title is not None:
        lines.append(f"title: {title}")
    lines.append(f"date: {date}")
    lines.append(f"tags: {tags}")
    lines.append(f"summary: {summary}")
    if draft is not None:
        lines.append(f"draft: {str(draft).lower()}")
    lines.append("---")
    lines.append(body)
    return "\n".join(lines) + "\n"


class TestLoadPosts(unittest.TestCase):
    """Load markdown posts from a directory."""

    def setUp(self) -> None:
        """Create a temporary directory for post files."""
        self._temp = tempfile.TemporaryDirectory()
        self.directory = Path(self._temp.name)

    def tearDown(self) -> None:
        """Remove the temporary post directory."""
        self._temp.cleanup()

    def test_post_is_a_frozen_dataclass(self) -> None:
        """Post fields cannot change after construction."""
        post = Post(
            title="Hello",
            slug="hello",
            date="2026-12-14",
            tags=("agents", "basics"),
            summary="Short text",
            body="Body paragraph.",
            draft=False,
        )
        with self.assertRaises(FrozenInstanceError):
            post.title = "Changed"

    def test_loads_front_matter_slug_and_body(self) -> None:
        """A published file exposes front matter, stem slug, and body."""
        content = """\
---
title: Hello
date: 2026-12-14
tags: agents, basics
summary: Short text
draft: false
---
Body paragraph.
"""
        _write(self.directory, "hello-world.md", content)
        post = load_posts(self.directory)[0]
        self.assertEqual(
            post,
            Post(
                title="Hello",
                slug="hello-world",
                date="2026-12-14",
                tags=("agents", "basics"),
                summary="Short text",
                body="Body paragraph.",
                draft=False,
            ),
        )

    def test_draft_defaults_to_false_when_omitted(self) -> None:
        """An omitted draft field means the post is published."""
        _write(
            self.directory,
            "published.md",
            _post("Published", "2026-04-01", draft=None),
        )
        post = load_posts(self.directory)[0]
        self.assertFalse(post.draft)

    def test_tags_are_split_on_commas_and_stripped(self) -> None:
        """Tags are a tuple of stripped names."""
        _write(
            self.directory,
            "tagged.md",
            _post("Tagged", "2026-03-01", tags=" agents , basics "),
        )
        post = load_posts(self.directory)[0]
        self.assertEqual(post.tags, ("agents", "basics"))

    def test_body_is_text_after_closing_fence(self) -> None:
        """The body keeps paragraphs after the closing fence."""
        body = "Body paragraph.\n\nSecond paragraph."
        _write(
            self.directory,
            "longer.md",
            _post("Longer", "2026-05-01", body=body),
        )
        post = load_posts(self.directory)[0]
        self.assertEqual(post.body, body)

    def test_returns_drafts_and_published_sorted_by_date_then_slug(
        self,
    ) -> None:
        """Drafts stay in the list and order is date, then slug."""
        _write(self.directory, "zeta.md", _post("Zeta", "2026-01-01", draft=True))
        _write(
            self.directory,
            "alpha.md",
            _post("Alpha", "2026-01-01", draft=False),
        )
        _write(
            self.directory,
            "later.md",
            _post("Later", "2026-06-01", draft=False),
        )
        posts = load_posts(self.directory)
        self.assertEqual(
            [(post.slug, post.draft) for post in posts],
            [("alpha", False), ("zeta", True), ("later", False)],
        )

    def test_missing_title_raises_value_error(self) -> None:
        """A markdown file without a title is rejected."""
        _write(self.directory, "untitled.md", _post(None, "2026-01-01"))
        with self.assertRaises(ValueError):
            load_posts(self.directory)

    def test_non_markdown_files_are_ignored(self) -> None:
        """Only markdown files become posts."""
        _write(self.directory, "hello.md", _post("Hello", "2026-12-14"))
        _write(self.directory, "notes.txt", "not a post")
        _write(self.directory, "picture.png", "bytes")
        posts = load_posts(self.directory)
        self.assertEqual([post.slug for post in posts], ["hello"])


if __name__ == "__main__":
    unittest.main()
