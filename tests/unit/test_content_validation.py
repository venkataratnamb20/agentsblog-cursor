"""Tests for content-model validation on load.

Behaviour: missing titles fail; markdown images without alt text
fail; series front matter is loaded when present.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.posts import load_posts  # noqa: E402


def _write(directory: Path, name: str, text: str) -> None:
    """Write one markdown file.

    Args:
        directory: Content directory.
        name: File name.
        text: Full file contents.
    """
    (directory / name).write_text(text, encoding="utf-8")


class TestContentValidation(unittest.TestCase):
    """Front matter and alt-text rules for the content model."""

    def test_missing_title_raises(self) -> None:
        """A markdown file without a title is rejected."""
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp)
            _write(
                content,
                "no-title.md",
                "---\ndate: 2026-01-01\ndraft: false\n---\nBody.\n",
            )
            with self.assertRaises(ValueError):
                load_posts(content)

    def test_image_without_alt_raises(self) -> None:
        """An image markdown token with an empty alt text is rejected."""
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp)
            _write(
                content,
                "bad-alt.md",
                (
                    "---\n"
                    "title: Bad alt\n"
                    "date: 2026-01-01\n"
                    "draft: false\n"
                    "---\n"
                    "See ![](diagram.png).\n"
                ),
            )
            with self.assertRaises(ValueError) as raised:
                load_posts(content)
        self.assertIn("alt", str(raised.exception).lower())

    def test_series_fields_load(self) -> None:
        """Optional series metadata is available on the post object."""
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp)
            _write(
                content,
                "part-two.md",
                (
                    "---\n"
                    "title: Part two\n"
                    "date: 2026-01-02\n"
                    "series: Anatomy\n"
                    "series_part: 2\n"
                    "series_total: 3\n"
                    "draft: false\n"
                    "---\n"
                    "Second part.\n"
                ),
            )
            posts = load_posts(content)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].series, "Anatomy")
        self.assertEqual(posts[0].series_part, 2)
        self.assertEqual(posts[0].series_total, 3)


if __name__ == "__main__":
    unittest.main()
