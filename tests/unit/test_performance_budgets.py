"""Byte and request budgets for the local static preview.

Behaviour: ``index.html`` and ``assets/site.css`` stay within transfer
budgets, and built HTML does not load a remote script or a CDN font
stylesheet. Module: ``agentsblog.build``. Field Core Web Vitals are
not collected. Existing tests do not check these budgets.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SRC = _REPO / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402

_INDEX_BUDGET = 20000
_CSS_BUDGET = 8000
_BUDGET_DOC = _REPO / "docs" / "testing" / "performance-budgets.md"
_DOC_PHRASES = (
    "LCP",
    "INP",
    "CLS",
    "20000",
    "8000",
    "field data is not collected",
)

_PUBLISHED = """\
---
title: What is an agent?
date: 2026-12-14
summary: A short definition
draft: false
---
An agent uses tools.
"""

_DRAFT = """\
---
title: Secret draft
date: 2026-12-15
summary: Hidden
draft: true
---
Do not publish.
"""


def _html_files(output: Path) -> list[Path]:
    """Return built HTML files under one output directory.

    Args:
        output: Directory written by ``build_site``.

    Returns:
        HTML paths in sorted order. An empty list means the build
        wrote no HTML.
    """
    return sorted(output.rglob("*.html"))


class TestPerformanceBudgets(unittest.TestCase):
    """The local preview stays small and does not call remote hosts."""

    def setUp(self) -> None:
        """Build one published post and one draft into a temp site."""
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        content = root / "content"
        self.output = root / "build"
        content.mkdir()
        (content / "what-is-an-agent.md").write_text(
            _PUBLISHED,
            encoding="utf-8",
        )
        (content / "secret-draft.md").write_text(
            _DRAFT,
            encoding="utf-8",
        )
        build_site(content, self.output)

    def tearDown(self) -> None:
        """Remove the temporary site."""
        self._tmp.cleanup()

    def test_index_and_stylesheet_stay_within_byte_budgets(self) -> None:
        """``index.html`` and ``site.css`` exist and fit the budgets.

        The limits leave room for a small consent banner and extra CSS.
        """
        index = self.output / "index.html"
        css = self.output / "assets" / "site.css"
        self.assertTrue(index.is_file())
        self.assertTrue(css.is_file())
        self.assertLessEqual(index.stat().st_size, _INDEX_BUDGET)
        self.assertLessEqual(css.stat().st_size, _CSS_BUDGET)

    def test_built_html_loads_no_remote_script_or_font_cdn(self) -> None:
        """Built pages do not reference an external script or font CDN."""
        pages = _html_files(self.output)
        self.assertGreater(len(pages), 0)
        for page in pages:
            text = page.read_text(encoding="utf-8")
            self.assertNotIn("<script src=", text, page.name)
            self.assertNotIn("fonts.googleapis.com", text, page.name)
            self.assertNotIn("cdn.", text, page.name)

    def test_budget_doc_names_vitals_and_byte_limits(self) -> None:
        """The budget note names the vitals that are not measured."""
        self.assertTrue(_BUDGET_DOC.is_file())
        text = _BUDGET_DOC.read_text(encoding="utf-8")
        for phrase in _DOC_PHRASES:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
