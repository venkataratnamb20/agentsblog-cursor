"""Tests for the theme toggle.

Behaviour: the theme button sets ``data-theme`` to dark and light, and
the built stylesheet paints a dark background. Module:
``agentsblog.render`` and the stylesheet from ``agentsblog.build``.
Existing tests: ``tests/unit/test_render.py`` checks the button id
only. There is no ``test_theme.py``. User instruction: "/tdd-workflow
Build and fix. Check all project goals, pending goals, issues and fix
them one by one."
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
from agentsblog.render import render_index  # noqa: E402


class TestThemeToggle(unittest.TestCase):
    """The theme button switches the document between light and dark."""

    def test_page_script_sets_dark_and_light(self) -> None:
        """The shared page script writes both theme names.

        The button is useless until the script sets ``data-theme`` to
        ``dark`` and back to ``light``.
        """
        page = render_index([])
        self.assertIn('setAttribute("data-theme"', page)
        self.assertIn('"dark"', page)
        self.assertIn('"light"', page)

    def test_stylesheet_paints_a_dark_background(self) -> None:
        """Dark theme uses a dark page background."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(content, output)
            css = (output / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertIn('[data-theme="dark"]', css)
        self.assertIn("#1c1915", css)


if __name__ == "__main__":
    unittest.main()
