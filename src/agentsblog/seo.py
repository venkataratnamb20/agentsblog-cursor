"""Render robots, sitemap, and on-page SEO metadata."""

from __future__ import annotations

import html
import json
from collections.abc import Iterable

LOCAL_SITE_URL = "http://127.0.0.1:8000"
_DESCRIPTION = "A technical blog on AI agents."


def render_robots(site_url: str) -> str:
    """Render a robots file that allows the site.

    Args:
        site_url: Absolute origin, with or without a trailing slash.

    Returns:
        ``robots.txt`` contents, including the sitemap URL.
    """
    origin = site_url.rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n"


def render_sitemap(locations: Iterable[str]) -> str:
    """Render a sitemap for absolute page URLs.

    Args:
        locations: Absolute URLs in the order they should be listed.

    Returns:
        An XML sitemap.
    """
    urls = "".join(
        f"<url><loc>{html.escape(location)}</loc></url>" for location in locations
    )
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}"
        "</urlset>"
    )


def index_metadata(site_url: str) -> str:
    """Render canonical and Open Graph tags for the index.

    Args:
        site_url: Absolute origin.

    Returns:
        HTML elements for the document head. The text is escaped.
    """
    canonical = f"{site_url.rstrip('/')}/"
    return _metadata(
        canonical=canonical,
        title="Agents Blog",
        description=_DESCRIPTION,
        kind="website",
        schema_type="Blog",
        date="",
    )


def post_metadata(
    title: str,
    summary: str,
    slug: str,
    date: str,
    site_url: str,
) -> str:
    """Render canonical, Open Graph, and BlogPosting metadata.

    Args:
        title: Post title.
        summary: Short description. May be empty.
        slug: Post filename stem.
        date: Publication date, usually ``YYYY-MM-DD``.
        site_url: Absolute origin.

    Returns:
        HTML elements for the document head. The text is escaped.
    """
    canonical = f"{site_url.rstrip('/')}/posts/{slug}.html"
    return _metadata(
        canonical=canonical,
        title=title,
        description=summary,
        kind="article",
        schema_type="BlogPosting",
        date=date,
    )


def _metadata(
    canonical: str,
    title: str,
    description: str,
    kind: str,
    schema_type: str,
    date: str,
) -> str:
    """Render the shared head elements for one page.

    Args:
        canonical: Absolute page URL.
        title: Page title.
        description: Meta description.
        kind: Open Graph type, such as ``website`` or ``article``.
        schema_type: schema.org type name.
        date: Publication date. Empty omits ``datePublished``.

    Returns:
        Escaped HTML for the document head.
    """
    safe_title = html.escape(title, quote=True)
    safe_description = html.escape(description, quote=True)
    safe_url = html.escape(canonical, quote=True)
    schema = _schema(schema_type, title, description, canonical, date)
    return (
        f'<link rel="canonical" href="{safe_url}">'
        f'<meta name="description" content="{safe_description}">'
        f'<meta property="og:title" content="{safe_title}">'
        f'<meta property="og:type" content="{html.escape(kind, quote=True)}">'
        f'<meta property="og:url" content="{safe_url}">'
        f'<script type="application/ld+json">{schema}</script>'
    )


def _schema(
    schema_type: str,
    title: str,
    description: str,
    canonical: str,
    date: str,
) -> str:
    """Serialize schema.org JSON for embedding in HTML.

    Args:
        schema_type: schema.org type name.
        title: Headline.
        description: Description.
        canonical: Absolute page URL.
        date: Publication date. Empty omits the field.

    Returns:
        A JSON object. ``<`` is escaped so it cannot close the script.
    """
    payload: dict[str, str] = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "headline": title,
        "description": description,
        "url": canonical,
    }
    if date:
        payload["datePublished"] = date
    return json.dumps(payload).replace("<", r"\u003c")
