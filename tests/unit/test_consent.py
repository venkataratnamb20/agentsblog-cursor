"""Tests for the privacy-friendly consent banner.

Behaviour: non-essential storage stays off until the reader chooses.
The banner records that choice in localStorage and never sets a cookie
or calls the network. Module: ``agentsblog.consent`` and
``agentsblog.render``.
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

_FORBIDDEN = (
    "document.cookie",
    "fetch(",
    "XMLHttpRequest",
    "sendBeacon",
    "gtag",
)


class TestConsentMarkup(unittest.TestCase):
    """The banner offers Accept and Reject without a network call."""

    def test_banner_offers_accept_and_reject(self) -> None:
        """Accept and Reject are labelled buttons on the banner."""
        markup = consent_markup()
        self.assertIn('id="cookie-consent"', markup)
        self.assertIn('id="consent-accept"', markup)
        self.assertIn(">Accept<", markup)
        self.assertIn('id="consent-reject"', markup)
        self.assertIn(">Reject<", markup)
        self.assertIn(
            "This preview does not set cookies.",
            markup,
        )

    def test_script_stores_the_choice_in_local_storage_only(self) -> None:
        """The script writes the localStorage key and nothing else."""
        markup = consent_markup()
        script_at = markup.find("<script")
        script_end = markup.find("</script>")
        self.assertGreaterEqual(script_at, 0)
        self.assertGreater(script_end, script_at)
        script = markup[script_at:script_end]
        self.assertIn("localStorage", script)
        self.assertIn("agentsblog-consent", script)
        self.assertIn('"accepted"', script)
        self.assertIn('"rejected"', script)
        self.assertIn("hidden", script)
        for forbidden in _FORBIDDEN:
            self.assertNotIn(forbidden, script)


class TestConsentOnPages(unittest.TestCase):
    """Rendered pages include the banner after the skip link."""

    def test_pages_include_the_banner_after_the_skip_link(self) -> None:
        """Skip link, then the banner, on each reader page."""
        pages = (
            render_index([]),
            render_search(),
            render_about(),
            render_not_found(),
        )
        for page in pages:
            skip = page.find('class="skip-link"')
            banner = page.find('id="cookie-consent"')
            nav = page.find("<nav>")
            self.assertGreaterEqual(skip, 0, page)
            self.assertGreater(banner, skip, page)
            self.assertGreater(nav, skip, page)


if __name__ == "__main__":
    unittest.main()
