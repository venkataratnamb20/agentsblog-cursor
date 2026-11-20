"""Render an RSS 2.0 feed of published posts."""

from __future__ import annotations

import html
from collections.abc import Iterable
from datetime import datetime, timezone
from email.utils import format_datetime
from typing import Protocol


class FeedPost(Protocol):
    """Fields the feed reads from a post."""

    title: str
    slug: str
    date: str
    summary: str
    draft: bool


def render_feed(posts: Iterable[FeedPost], site_url: str) -> str:
    """Render published posts as an RSS channel.

    Args:
        posts: Posts in the order they should appear. Drafts are
            omitted.
        site_url: Absolute origin used for item links, without a
            trailing path. Example: ``http://127.0.0.1:8000``.

    Returns:
        An RSS 2.0 document. The channel is present even when no
        post is published.
    """
    origin = site_url.rstrip("/")
    items = "".join(_item(post, origin) for post in posts if not post.draft)
    description = "A technical blog on AI agents."
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<rss version="2.0">'
        "<channel>"
        "<title>Agents Blog</title>"
        f"<link>{html.escape(origin)}/</link>"
        f"<description>{description}</description>"
        f"{items}"
        "</channel>"
        "</rss>"
    )


def _item(post: FeedPost, origin: str) -> str:
    """Render one published post as an RSS item.

    Args:
        post: A post whose draft flag is already false.
        origin: Site origin without a trailing slash.

    Returns:
        One ``item`` element.
    """
    link = f"{origin}/posts/{post.slug}.html"
    published = _pub_date(post.date)
    pub_date = f"<pubDate>{published}</pubDate>" if published else ""
    return (
        "<item>"
        f"<title>{html.escape(post.title)}</title>"
        f"<link>{html.escape(link)}</link>"
        f"<description>{html.escape(post.summary)}</description>"
        f"{pub_date}"
        "</item>"
    )


def _pub_date(value: str) -> str:
    """Format a ``YYYY-MM-DD`` date as an RSS publication date.

    Args:
        value: Date string from front matter.

    Returns:
        An RFC 822 timestamp, or an empty string when ``value`` is
        not that shape.
    """
    try:
        day = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return ""
    return format_datetime(day)
