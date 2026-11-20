"""Tests for skip link and theme button accessibility.

Behaviour: every page has a skip link before nav, main has id
``main``, and the theme script sets ``aria-pressed``. Module:
``agentsblog.render``. Existing tests only check the theme button
id. User instruction: finish the a11y worktree after the agent
stopped with no progress.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.render import render_index  # noqa: E402


class TestAccessibilityChrome(unittest.TestCase):
    """Shared document chrome meets the skip-link and theme checks."""

    def test_skip_link_comes_before_nav_and_targets_main(self) -> None:
        """The first focusable control skips to main content."""
        page = render_index([])
        skip = page.find('href="#main"')
        nav = page.find("<nav>")
        main = page.find('<main id="main">')
        self.assertNotEqual(skip, -1)
        self.assertNotEqual(nav, -1)
        self.assertNotEqual(main, -1)
        self.assertLess(skip, nav)
        self.assertIn("Skip to content", page)

    def test_theme_script_sets_aria_pressed(self) -> None:
        """The theme script writes aria-pressed for the current theme."""
        page = render_index([])
        self.assertIn('setAttribute("aria-pressed"', page)
        self.assertIn('"true"', page)
        self.assertIn('"false"', page)


if __name__ == "__main__":
    unittest.main()
