"""Local preview checks against WCAG 2.2 AA rules a unit test can see.

The checks render the current index and search pages and read the
stylesheet source as text. They do not replace a human audit in a
browser with a screen reader. Module: ``agentsblog.render``.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.render import render_index, render_search  # noqa: E402

_BUILD_SOURCE = (
    Path(__file__).resolve().parents[2] / "src" / "agentsblog" / "build.py"
)
_BODY_TEXT = "#1c1915"
_PAGE_BACKGROUND = "#f7f4ef"
_TEXT_CONTRAST_AA = 4.5


def relative_luminance(hex_color: str) -> float:
    """Return WCAG 2.2 relative luminance for one sRGB color.

    Args:
        hex_color: A ``#rrggbb`` color.

    Returns:
        Luminance from 0 (black) to 1 (white).
    """
    channels = _linear_channels(hex_color)
    red, green, blue = channels
    return (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)


def contrast_ratio(foreground: str, background: str) -> float:
    """Return the WCAG contrast ratio for two ``#rrggbb`` colors.

    Args:
        foreground: Foreground color.
        background: Background color.

    Returns:
        The contrast ratio, from 1 to 21.
    """
    first = relative_luminance(foreground)
    second = relative_luminance(background)
    lighter = max(first, second)
    darker = min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def _linear_channels(hex_color: str) -> tuple[float, float, float]:
    """Convert ``#rrggbb`` to WCAG linear-light channels.

    Args:
        hex_color: A ``#rrggbb`` color.

    Returns:
        Linear red, green, and blue, each from 0 to 1.
    """
    red = int(hex_color[1:3], 16) / 255
    green = int(hex_color[3:5], 16) / 255
    blue = int(hex_color[5:7], 16) / 255
    return (_linearize(red), _linearize(green), _linearize(blue))


def _linearize(channel: float) -> float:
    """Map one sRGB channel to linear light.

    Args:
        channel: Channel value from 0 to 1.

    Returns:
        The linearized channel.
    """
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def _document_title(page: str) -> str:
    """Return the text inside the document title element.

    Args:
        page: An HTML document.

    Returns:
        The title text, or an empty string when it is missing.
    """
    match = re.search(r"<title>(.*?)</title>", page)
    if match is None:
        return ""
    return match.group(1)


def _h1_count(page: str) -> int:
    """Count ``h1`` elements in one HTML document.

    Args:
        page: An HTML document.

    Returns:
        The number of ``h1`` start tags.
    """
    return len(re.findall(r"<h1\b", page, flags=re.IGNORECASE))


class TestLocalPreviewAccessibility(unittest.TestCase):
    """Checks that hold on the current local index and search pages."""

    def test_pages_declare_english_and_a_title(self) -> None:
        """Each audited page sets lang and a non-empty title."""
        for page in (render_index([]), render_search()):
            self.assertIn('<html lang="en">', page)
            self.assertTrue(_document_title(page).strip())

    def test_search_page_has_exactly_one_h1(self) -> None:
        """The search page exposes one h1."""
        self.assertEqual(_h1_count(render_search()), 1)

    def test_index_has_exactly_one_h1(self) -> None:
        """The index exposes one h1 so heading navigation has a target."""
        page = render_index([])
        self.assertEqual(_h1_count(page), 1)
        self.assertIn("<h1>Agents Blog</h1>", page)

    def test_main_landmark_and_skip_link(self) -> None:
        """A skip link to #main appears before the navigation."""
        for page in (render_index([]), render_search()):
            skip = page.find('href="#main"')
            nav = page.find("<nav>")
            self.assertIn('<main id="main">', page)
            self.assertNotEqual(skip, -1)
            self.assertNotEqual(nav, -1)
            self.assertLess(skip, nav)

    def test_search_input_has_a_label(self) -> None:
        """The search field is labelled by for=search-query."""
        page = render_search()
        self.assertIn('<label for="search-query">', page)
        self.assertIn('id="search-query"', page)

    def test_theme_control_is_a_named_button(self) -> None:
        """The theme control is a button named Toggle theme."""
        page = render_index([])
        self.assertRegex(page, r"<button\b[^>]*>Toggle theme</button>")

    def test_body_text_contrast_meets_aa(self) -> None:
        """#1c1915 on #f7f4ef meets the 4.5:1 text contrast floor."""
        stylesheet = _BUILD_SOURCE.read_text(encoding="utf-8")
        self.assertIn(_BODY_TEXT, stylesheet)
        self.assertIn(_PAGE_BACKGROUND, stylesheet)
        ratio = contrast_ratio(_BODY_TEXT, _PAGE_BACKGROUND)
        self.assertGreaterEqual(ratio, _TEXT_CONTRAST_AA)


if __name__ == "__main__":
    unittest.main()
