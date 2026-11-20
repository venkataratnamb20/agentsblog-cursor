"""Tests for draft legal pages.

Behaviour: the build writes privacy, cookies, terms, licences, and
AI-assistance pages, each marked as not approved by Venkat. Privacy
names UK GDPR. Cookies names PECR. Module: ``agentsblog.build``.
Existing tests: none. User instruction: "/tdd-workflow Build and fix.
Check all project goals, pending goals, issues and fix them one by
one."
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

_DRAFT = "Venkat has not approved this page for publication."
_PAGES = (
    "privacy.html",
    "cookies.html",
    "terms.html",
    "licences.html",
    "ai-assistance.html",
)


class TestLegalPages(unittest.TestCase):
    """Policy pages are drafts on the local site."""

    def test_build_writes_draft_policy_pages(self) -> None:
        """Each policy page exists and says it is not approved."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(content, output)
            privacy = (output / "privacy.html").read_text(encoding="utf-8")
            cookies = (output / "cookies.html").read_text(encoding="utf-8")
            for name in _PAGES:
                text = (output / name).read_text(encoding="utf-8")
                self.assertIn(_DRAFT, text, name)
        self.assertIn("UK GDPR", privacy)
        self.assertIn("PECR", cookies)
        self.assertIn('href="/privacy.html"', privacy)


if __name__ == "__main__":
    unittest.main()
