"""Tests for the reader-facing search page.

The page under test is ``agentsblog.render.render_search`` and the
file ``agentsblog.build.build_site`` writes. Existing coverage is
``tests/unit/test_render.py`` (index, post, 404),
``tests/unit/test_search.py`` (in-memory matching), and
``tests/integration/test_site_build.py`` (``search-index.json``).
None of those assert a search page. The user asked to build and fix
pending goals with the TDD workflow, including search.
"""

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
from agentsblog.render import render_index, render_search  # noqa: E402


class TestSearchPage(unittest.TestCase):
    """A reader can open a search page on the built site."""

    def test_search_page_has_a_query_box_and_empty_query_rule(self) -> None:
        """The page names its query field and ignores a blank query.

        A blank query must not list every post. The page reads the
        built search index, which already omits drafts.
        """
        page = render_search()
        self.assertIn('id="search-query"', page)
        self.assertIn('id="search-results"', page)
        self.assertIn("/search-index.json", page)
        self.assertIn("if (!query)", page)
        self.assertIn('lang="en"', page)

    def test_index_links_to_the_search_page(self) -> None:
        """The index offers a way to open search."""
        page = render_index([])
        self.assertIn('href="search.html"', page)

    def test_build_writes_the_search_page(self) -> None:
        """``build_site`` writes ``search.html`` beside the index."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(content, output)
            page = (output / "search.html").read_text(encoding="utf-8")
            self.assertIn('id="search-query"', page)


if __name__ == "__main__":
    unittest.main()
