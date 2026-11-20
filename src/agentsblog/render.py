"""Render Agents Blog pages to HTML."""

from __future__ import annotations

import html
from collections.abc import Iterable
from typing import Protocol

from agentsblog.consent import consent_markup
from agentsblog.markdown import render_markdown
from agentsblog.seo import LOCAL_SITE_URL, index_metadata, post_metadata
from agentsblog.tags import tag_slug

_TAGLINE = "Clear writing for people who build AI agents."
_PILLARS = ("Foundations", "Building", "Evaluation", "Safety", "Operations")
_BASE_PATH = ""

_THEME_TOGGLE = (
    '<button id="theme-toggle" type="button" aria-pressed="false">'
    "Toggle theme</button>"
)

_SKIP_LINK = '<a class="skip-link" href="#main">Skip to content</a>'

_VIEWPORT = (
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
)

_THEME_SCRIPT = """\
<script>
(function () {
  var button = document.getElementById("theme-toggle");
  function pressed(theme) {
    button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }
  pressed(document.documentElement.getAttribute("data-theme"));
  button.addEventListener("click", function () {
    var root = document.documentElement;
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    pressed(next);
  });
})();
</script>
"""


class IndexPost(Protocol):
    """Fields the index reads from a post."""

    title: str
    slug: str
    draft: bool
    date: str
    summary: str


class ArticlePost(Protocol):
    """Fields a single post page reads from a post."""

    title: str
    body: str


def set_base_path(path: str) -> None:
    """Set the site base path for root-absolute links.

    Args:
        path: Prefix such as ``/agentsblog-cursor``, or empty for local.
    """
    global _BASE_PATH
    cleaned = path.strip()
    if cleaned.endswith("/"):
        cleaned = cleaned[:-1]
    _BASE_PATH = cleaned


def _href(path: str) -> str:
    """Prefix a root-absolute path with the configured base path.

    Args:
        path: A site path beginning with ``/``.

    Returns:
        The path with ``_BASE_PATH`` prepended when configured.
    """
    if not path.startswith("/"):
        return path
    return f"{_BASE_PATH}{path}"


def _nav() -> str:
    """Return the primary navigation with the current base path."""
    return (
        f'<nav><a href="{_href("/")}">Home</a> '
        f'<a href="{_href("/search.html")}">Search</a> '
        f'<a href="{_href("/about.html")}">About</a> '
        f'<a href="{_href("/subscribe.html")}">Subscribe</a> '
        f'<a href="{_href("/privacy.html")}">Privacy</a></nav>'
    )


def _footer() -> str:
    """Return the policy footer with the current base path."""
    return (
        "<footer>"
        f'<a href="{_href("/cookies.html")}">Cookies</a> | '
        f'<a href="{_href("/terms.html")}">Terms</a> | '
        f'<a href="{_href("/licences.html")}">Licences</a> | '
        f'<a href="{_href("/ai-assistance.html")}">AI assistance</a>'
        "</footer>"
    )


def _feed_link() -> str:
    """Return the RSS alternate link with the current base path."""
    return (
        '<link rel="alternate" type="application/rss+xml" '
        f'href="{_href("/feed.xml")}" title="Agents Blog">'
    )


def _document(
    title: str,
    main: str,
    head: str = "",
) -> str:
    """Wrap a page title and main content in the shared document.

    Args:
        title: Document title. Callers pass already escaped text.
        main: Inner HTML placed in the document body.
        head: Extra escaped elements for the document head.

    Returns:
        A complete HTML document.
    """
    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        f"{_VIEWPORT}"
        f"<title>{title}</title>"
        f'<link rel="stylesheet" href="{_href("/assets/site.css")}">'
        f"{_feed_link()}"
        f"{head}"
        "</head>"
        "<body>"
        f"{_SKIP_LINK}"
        f"{consent_markup()}"
        f"{_nav()}"
        f"{_THEME_TOGGLE}"
        f'<main id="main">{main}</main>'
        f"{_footer()}"
        f"{_THEME_SCRIPT}"
        "</body>"
        "</html>"
    )


def render_search() -> str:
    """Render the page a reader uses to search published posts.

    The page loads the search index and lists matches in the order of
    that file. A blank query leaves the result list empty.

    Returns:
        The search document as HTML.
    """
    heading = html.escape("Search")
    index_url = _href("/search-index.json")
    post_prefix = _href("/posts/")
    script = _SEARCH_SCRIPT.replace("__INDEX_URL__", index_url).replace(
        "__POST_PREFIX__",
        post_prefix,
    )
    main = (
        f"<h1>{heading}</h1>"
        '<label for="search-query">Search posts</label>'
        '<input id="search-query" type="search" name="q">'
        '<ul id="search-results"></ul>'
        f"{script}"
    )
    return _document(heading, main)


def render_index(
    posts: Iterable[IndexPost],
    site_url: str = LOCAL_SITE_URL,
    noindex: bool = False,
) -> str:
    """Render the index of published posts.

    Args:
        posts: Posts that expose title, slug, date, summary, and draft.
        site_url: Absolute origin used for the canonical URL.
        noindex: When True, ask crawlers not to index the page.

    Returns:
        The index document as HTML.
    """
    items: list[str] = []
    for post in posts:
        if post.draft:
            continue
        items.append(_list_item(post, absolute=False))
    listing = "<ul>" + "".join(items) + "</ul>"
    pillars = " · ".join(html.escape(name) for name in _PILLARS)
    main = (
        "<h1>Agents Blog</h1>"
        f"<p>{html.escape(_TAGLINE)}</p>"
        f"<p>{pillars}</p>"
        "<h2>Posts</h2>"
        f"{listing}"
    )
    return _document(
        "Agents Blog",
        main,
        head=index_metadata(site_url, noindex=noindex),
    )


def render_post(
    post: ArticlePost,
    site_url: str = LOCAL_SITE_URL,
    noindex: bool = False,
) -> str:
    """Render one post as an HTML page.

    Args:
        post: Post whose title becomes the heading and whose body is
            shown as text.
        site_url: Absolute origin used for the canonical URL.
        noindex: When True, ask crawlers not to index the page.

    Returns:
        The post document as HTML.
    """
    safe_title = html.escape(post.title)
    date = html.escape(str(getattr(post, "date", "") or ""))
    published = f"<p>Published: {date}</p>" if date else ""
    content = (
        f"<article><h1>{safe_title}</h1>{published}"
        f"{_tag_links(post)}{_series_chrome(post)}"
        f"{render_markdown(post.body)}</article>"
    )
    metadata = post_metadata(
        title=post.title,
        summary=getattr(post, "summary", ""),
        slug=getattr(post, "slug", ""),
        date=getattr(post, "date", ""),
        site_url=site_url,
        noindex=noindex,
    )
    return _document(safe_title, content, head=metadata)


_SEARCH_SCRIPT = """\
<script>
(function () {
  var input = document.getElementById("search-query");
  var results = document.getElementById("search-results");
  var posts = [];
  fetch("__INDEX_URL__").then(function (response) {
    return response.json();
  }).then(function (records) {
    posts = records;
  });
  input.addEventListener("input", function () {
    var query = input.value.trim().toLowerCase();
    results.replaceChildren();
    if (!query) {
      return;
    }
    posts.forEach(function (post) {
      if (!matches(post, query)) {
        return;
      }
      var item = document.createElement("li");
      var link = document.createElement("a");
      link.href = "__POST_PREFIX__" + post.slug + ".html";
      link.textContent = post.title;
      item.appendChild(link);
      results.appendChild(item);
    });
  });

  function matches(post, query) {
    var fields = [post.title || "", post.summary || ""].concat(post.tags || []);
    return fields.some(function (field) {
      return String(field).toLowerCase().indexOf(query) !== -1;
    });
  }
})();
</script>
"""


def render_about() -> str:
    """Render the about page.

    Returns:
        HTML that names the audience and says the public site is not live.
    """
    main = (
        "<p>Agents Blog is a technical blog on AI agents for "
        "engineers, researchers, and tech leads.</p>"
        f"<p>{html.escape(_TAGLINE)}</p>"
        "<p>The public site is not live. This page is for the local "
        "preview.</p>"
    )
    return render_page("About", main)


def render_subscribe() -> str:
    """Render the subscribe page without collecting an email.

    Returns:
        HTML that says signup waits on an approved email service.
    """
    feed = _href("/feed.xml")
    main = (
        "<p>Subscribe is blocked until an email service is approved.</p>"
        "<p>There is no signup form on this page. Check back after "
        "Venkat approves an email provider.</p>"
        f'<p>RSS: <a href="{feed}">{html.escape(feed)}</a></p>'
    )
    return render_page("Subscribe", main)


def render_tag_page(label: str, posts: Iterable[IndexPost]) -> str:
    """Render the posts that share one tag.

    Args:
        label: Tag text shown as the heading.
        posts: Published posts in reader order.

    Returns:
        A page of links to those posts.
    """
    items = [_list_item(post, absolute=True) for post in posts]
    main = f"<p>Posts with this tag</p><ul>{''.join(items)}</ul>"
    return render_page(label, main)


def _list_item(post: IndexPost, absolute: bool) -> str:
    """Render one post list entry with title, date, and dek.

    Args:
        post: Post fields for the list row.
        absolute: When True, post hrefs are root-absolute under base.

    Returns:
        An ``<li>`` element.
    """
    safe_title = html.escape(post.title)
    safe_slug = html.escape(post.slug)
    href = (
        _href(f"/posts/{safe_slug}.html")
        if absolute
        else f"posts/{safe_slug}.html"
    )
    date = html.escape(str(getattr(post, "date", "") or ""))
    summary = html.escape(str(getattr(post, "summary", "") or ""))
    date_line = f"<p>{date}</p>" if date else ""
    dek = f"<p>{summary}</p>" if summary else ""
    return f'<li><a href="{href}">{safe_title}</a>{date_line}{dek}</li>'


def _tag_links(post: ArticlePost) -> str:
    """Render links from a post to its tag pages.

    Args:
        post: Post that may expose ``tags``.

    Returns:
        A paragraph of links, or an empty string when there are none.
    """
    links: list[str] = []
    for tag in getattr(post, "tags", ()):
        slug = tag_slug(str(tag))
        if not slug:
            continue
        links.append(
            f'<a href="{_href(f"/tags/{slug}.html")}">'
            f"{html.escape(str(tag))}</a>"
        )
    if not links:
        return ""
    return "<p>Tags: " + " · ".join(links) + "</p>"


def _series_chrome(post: ArticlePost) -> str:
    """Render series navigation when series metadata is present.

    Args:
        post: Post that may expose series fields.

    Returns:
        Series chrome HTML, or an empty string.
    """
    series = str(getattr(post, "series", "") or "").strip()
    part = int(getattr(post, "series_part", 0) or 0)
    total = int(getattr(post, "series_total", 0) or 0)
    if not series or part <= 0 or total <= 0:
        return ""
    lines = [
        f"<p>Part {part} of {total} · {html.escape(series)}</p>",
    ]
    prev_slug = str(getattr(post, "series_prev_slug", "") or "")
    prev_title = str(getattr(post, "series_prev_title", "") or "")
    next_slug = str(getattr(post, "series_next_slug", "") or "")
    next_title = str(getattr(post, "series_next_title", "") or "")
    nav: list[str] = []
    if prev_slug and prev_title:
        nav.append(
            f'<a href="{_href(f"/posts/{html.escape(prev_slug)}.html")}">'
            f"Previous: {html.escape(prev_title)}</a>"
        )
    if next_slug and next_title:
        nav.append(
            f'<a href="{_href(f"/posts/{html.escape(next_slug)}.html")}">'
            f"Next: {html.escape(next_title)}</a>"
        )
    if nav:
        lines.append("<p>" + " ".join(nav) + "</p>")
    return "".join(lines)


def render_page(title: str, main: str) -> str:
    """Render a standalone page with the shared document chrome.

    Args:
        title: Visible title. This function escapes it.
        main: Inner HTML. The caller escapes any untrusted text.

    Returns:
        A complete HTML document.
    """
    return _document(html.escape(title), f"<h1>{html.escape(title)}</h1>{main}")


def render_not_found() -> str:
    """Render the page shown when a request has no document.

    Returns:
        HTML that tells the reader the page was not found.
    """
    message = html.escape("Page not found")
    main = (
        f"<h1>{message}</h1>"
        "<p>That URL is not in the local preview.</p>"
        f'<p><a href="{_href("/")}">Back to Home</a></p>'
    )
    return _document(message, main)
