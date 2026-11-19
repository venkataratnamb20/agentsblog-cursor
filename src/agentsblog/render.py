"""Render Agents Blog pages to HTML."""

from __future__ import annotations

import html
from collections.abc import Iterable
from typing import Protocol


class IndexPost(Protocol):
    """Fields the index reads from a post."""

    title: str
    slug: str
    draft: bool


class ArticlePost(Protocol):
    """Fields a single post page reads from a post."""

    title: str
    body: str


def _document(title: str, main: str) -> str:
    """Wrap a page title and main content in the shared document.

    Args:
        title: Document title. Callers pass already escaped text.
        main: Inner HTML placed in the document body.

    Returns:
        A complete HTML document.
    """
    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        f"<title>{title}</title>"
        '<link rel="stylesheet" href="/assets/site.css">'
        "</head>"
        "<body>"
        f"<main>{main}</main>"
        '<button id="theme-toggle" type="button">Toggle theme</button>'
        "</body>"
        "</html>"
    )


def render_index(posts: Iterable[IndexPost]) -> str:
    """Render the index of published posts.

    Args:
        posts: Posts that expose title, slug, and draft. Only posts
            whose draft flag is false are listed. Each published title
            links to ``posts/{slug}.html``.

    Returns:
        The index document as HTML.
    """
    items: list[str] = []
    for post in posts:
        if post.draft:
            continue
        safe_title = html.escape(post.title)
        safe_slug = html.escape(post.slug)
        items.append(
            f'<li><a href="posts/{safe_slug}.html">{safe_title}</a></li>'
        )
    listing = "<ul>" + "".join(items) + "</ul>"
    return _document("Agents Blog", listing)


def render_post(post: ArticlePost) -> str:
    """Render one post as an HTML page.

    Args:
        post: Post whose title becomes the heading and whose body is
            shown as text. ``<`` and ``&`` in both fields are escaped.

    Returns:
        The post document as HTML.
    """
    safe_title = html.escape(post.title)
    safe_body = html.escape(post.body)
    content = f"<article><h1>{safe_title}</h1><p>{safe_body}</p></article>"
    return _document(safe_title, content)


def render_not_found() -> str:
    """Render the page shown when a request has no document.

    Returns:
        HTML that tells the reader the page was not found.
    """
    message = html.escape("Page not found")
    return _document(message, f"<h1>{message}</h1>")
