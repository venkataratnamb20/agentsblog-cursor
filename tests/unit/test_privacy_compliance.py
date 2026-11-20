"""Tests for the local privacy compliance check.

Behaviour: built HTML does not call an analytics host and does not
assign ``document.cookie``. Consent prose may mention cookies. The
privacy check names UK GDPR, PECR, no analytics vendor, and Venkat.
Module: ``agentsblog.build``. Existing tests: none.
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

_ANALYTICS_HOSTS = (
    "google-analytics.com",
    "googletagmanager.com",
    "cdn.jsdelivr.net",
)
_PRIVACY_DOC = _REPO / "docs" / "security" / "privacy-check.md"
_REQUIRED_PHRASES = (
    "UK GDPR",
    "PECR",
    "no analytics vendor",
    "Venkat",
)


def _html_texts(output: Path) -> list[tuple[str, str]]:
    """Read every built HTML file.

    Args:
        output: Directory written by ``build_site``.

    Returns:
        Pairs of relative path and file text. The scan is O(n) in the
        number of HTML files.
    """
    return [
        (path.relative_to(output).as_posix(), path.read_text(encoding="utf-8"))
        for path in sorted(output.rglob("*.html"))
    ]


class TestPrivacyCompliance(unittest.TestCase):
    """Built pages do not call an analytics host or write a cookie."""

    def test_built_html_has_no_analytics_or_cookie_write(self) -> None:
        """HTML omits analytics hosts and ``document.cookie=``."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(content, output)
            pages = _html_texts(output)
        self.assertGreater(len(pages), 0)
        for name, text in pages:
            self.assertNotIn("document.cookie=", text, name)
            for host in _ANALYTICS_HOSTS:
                self.assertNotIn(host, text, name)

    def test_privacy_check_names_uk_rules_and_venkat(self) -> None:
        """The privacy note names UK GDPR, PECR, no vendor, and Venkat."""
        text = _PRIVACY_DOC.read_text(encoding="utf-8")
        for phrase in _REQUIRED_PHRASES:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
