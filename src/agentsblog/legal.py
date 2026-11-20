"""Draft legal pages for the local site."""

from __future__ import annotations

import html
from dataclasses import dataclass

_DRAFT = "Venkat has not approved this page for publication."


@dataclass(frozen=True)
class PolicyPage:
    """One draft policy document.

    Attributes:
        filename: File name written at the site root.
        title: Document title.
        main: Escaped HTML placed in the page body.
    """

    filename: str
    title: str
    main: str


def policy_pages() -> tuple[PolicyPage, ...]:
    """Return the draft policy pages in navigation order.

    Returns:
        Privacy, cookies, terms, licences, and AI-assistance drafts.
    """
    return (
        _page(
            "privacy.html",
            "Privacy",
            (
                _DRAFT,
                "This local preview collects no personal data.",
                "The public site is intended to follow UK GDPR.",
                "Non-essential cookies are not set before consent.",
            ),
        ),
        _page(
            "cookies.html",
            "Cookies",
            (
                _DRAFT,
                "This local preview sets no cookies.",
                "A public site would follow PECR before storing any.",
            ),
        ),
        _page(
            "terms.html",
            "Terms",
            (
                _DRAFT,
                "These terms are a draft for the local preview.",
            ),
        ),
        _page(
            "licences.html",
            "Licences",
            (
                _DRAFT,
                "This draft does not grant a licence to the posts.",
            ),
        ),
        _page(
            "ai-assistance.html",
            "AI assistance",
            (
                _DRAFT,
                "Repository drafts may be written with AI assistance.",
            ),
        ),
    )


def _page(filename: str, title: str, paragraphs: tuple[str, ...]) -> PolicyPage:
    """Build one policy page from plain paragraphs.

    Args:
        filename: Output file name.
        title: Document title.
        paragraphs: Plain sentences. Each becomes one paragraph.

    Returns:
        A page whose body HTML is escaped.
    """
    main = "".join(f"<p>{html.escape(text)}</p>" for text in paragraphs)
    return PolicyPage(filename=filename, title=title, main=main)
