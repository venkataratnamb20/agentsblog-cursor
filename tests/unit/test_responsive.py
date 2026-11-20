"""Tests for a narrow-screen viewport and column.

Behaviour: every page declares a device-width viewport, and the
stylesheet source in ``build.py`` tightens the column below 40rem.
Module: ``agentsblog.render`` and the stylesheet string in
``agentsblog.build``.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.consent import consent_markup  # noqa: E402
from agentsblog.render import (  # noqa: E402
    render_about,
    render_index,
    render_not_found,
    render_search,
)

_VIEWPORT = (
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
)
_BUILD_PY = _SRC / "agentsblog" / "build.py"


class TestResponsivePages(unittest.TestCase):
    """Pages expose a viewport and keep the skip link first."""

    def test_pages_declare_a_device_width_viewport(self) -> None:
        """The index, search, about, and 404 pages set the viewport."""
        pages = (
            render_index([]),
            render_search(),
            render_about(),
            render_not_found(),
        )
        for page in pages:
            self.assertIn(_VIEWPORT, page)
            self.assertIn('id="cookie-consent"', page)
            skip = page.find('class="skip-link"')
            banner = page.find('id="cookie-consent"')
            self.assertGreaterEqual(skip, 0)
            self.assertLess(skip, banner)

    def test_index_pairs_the_viewport_with_the_banner(self) -> None:
        """The index carries the viewport meta and the consent banner."""
        page = render_index([])
        self.assertIn("cookie-consent", page)
        self.assertIn(_VIEWPORT, page)
        self.assertLess(
            page.find('class="skip-link"'),
            page.find('id="cookie-consent"'),
        )
        markup = consent_markup()
        self.assertIn('id="consent-accept"', markup)
        self.assertIn('id="consent-reject"', markup)


class TestNarrowStylesheet(unittest.TestCase):
    """The stylesheet source names the narrow-screen query."""

    def test_stylesheet_source_has_a_narrow_media_query(self) -> None:
        """``build.py`` contains the 40rem max-width query."""
        source = _BUILD_PY.read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 40rem)", source)
        self.assertIn("#1c1915", source)
        self.assertIn("#f7f4ef", source)
        self.assertIn("prefers-color-scheme", source)


if __name__ == "__main__":
    unittest.main()
