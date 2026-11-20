"""Render Agents Blog pages to HTML."""

from __future__ import annotations

import html
from collections.abc import Iterable
from typing import Protocol

from agentsblog.markdown import render_markdown
from agentsblog.seo import LOCAL_SITE_URL, index_metadata, post_metadata
from agentsblog.tags import tag_slug


class IndexPost(Protocol):
    """Fields the index reads from a post."""

    title: str
    slug: str
    draft: bool


_NAV = (
    '<nav><a href="/">Home</a> '
    '<a href="/search.html">Search</a> '
    '<a href="/about.html">About</a> '
    '<a href="/subscribe.html">Subscribe</a> '
    '<a href="/privacy.html">Privacy</a></nav>'
)


_FEED_LINK = (
    '<link rel="alternate" type="application/rss+xml" '
    'href="/feed.xml" title="Agents Blog">'
)


_SKIP_LINK = '<a class="skip-link" href="#main">Skip to content</a>'


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


class ArticlePost(Protocol):
    """Fields a single post page reads from a post."""

    title: str
    body: str


def _document(title: str, main: str, head: str = "") -> str:
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
        f"<title>{title}</title>"
        '<link rel="stylesheet" href="/assets/site.css">'
        f"{_FEED_LINK}"
        f"{head}"
        "</head>"
        "<body>"
        f"{_SKIP_LINK}"
        f"{_NAV}"
        f'<main id="main">{main}</main>'
        '<button id="theme-toggle" type="button" aria-pressed="false">'
        "Toggle theme</button>"
        f"{_THEME_SCRIPT}"
        "</body>"
        "</html>"
    )


def render_search() -> str:
    """Render the page a reader uses to search published posts.

    The page loads ``/search-index.json`` and lists matches in the
    order of that file. A blank query leaves the result list empty.
    Matching is a case-insensitive substring of the title, summary,
    or a tag, the same rule as ``search_posts``.

    Returns:
        The search document as HTML.
    """
    heading = html.escape("Search")
    main = (
        f"<h1>{heading}</h1>"
        '<label for="search-query">Search posts</label>'
        '<input id="search-query" type="search" name="q">'
        '<ul id="search-results"></ul>'
        f"{_SEARCH_SCRIPT}"
    )
    return _document(heading, main)


def render_index(
    posts: Iterable[IndexPost],
    site_url: str = LOCAL_SITE_URL,
) -> str:
    """Render the index of published posts.

    Args:
        posts: Posts that expose title, slug, and draft. Only posts
            whose draft flag is false are listed. Each published title
            links to ``posts/{slug}.html``.
        site_url: Absolute origin used for the canonical URL.

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
    search_link = '<p><a href="search.html">Search</a></p>'
    return _document(
        "Agents Blog",
        search_link + listing,
        head=index_metadata(site_url),
    )


def render_post(post: ArticlePost, site_url: str = LOCAL_SITE_URL) -> str:
    """Render one post as an HTML page.

    Args:
        post: Post whose title becomes the heading and whose body is
            shown as text. ``<`` and ``&`` in both fields are escaped.
        site_url: Absolute origin used for the canonical URL.

    Returns:
        The post document as HTML.
    """
    safe_title = html.escape(post.title)
    content = (
        f"<article><h1>{safe_title}</h1>{_tag_links(post)}"
        f"{render_markdown(post.body)}</article>"
    )
    metadata = post_metadata(
        title=post.title,
        summary=getattr(post, "summary", ""),
        slug=getattr(post, "slug", ""),
        date=getattr(post, "date", ""),
        site_url=site_url,
    )
    return _document(safe_title, content, head=metadata)


_SEARCH_SCRIPT = """\
<script>
(function () {
  var input = document.getElementById("search-query");
  var results = document.getElementById("search-results");
  var posts = [];
  fetch("/search-index.json").then(function (response) {
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
      link.href = "posts/" + post.slug + ".html";
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
        "<p>The public site is not live.</p>"
    )
    return render_page("About", main)


def render_subscribe() -> str:
    """Render the subscribe page without collecting an email.

    Returns:
        HTML that says signup waits on an approved email service.
    """
    sentence = "subscribe is blocked until an email service is approved."
    return render_page("Subscribe", f"<p>{html.escape(sentence)}</p>")


def render_tag_page(label: str, posts: Iterable[IndexPost]) -> str:
    """Render the posts that share one tag.

    Args:
        label: Tag text shown as the heading.
        posts: Published posts in reader order.

    Returns:
        A page of links to those posts.
    """
    items = [
        "<li>"
        f'<a href="/posts/{html.escape(post.slug)}.html">'
        f"{html.escape(post.title)}</a></li>"
        for post in posts
    ]
    return render_page(label, "<ul>" + "".join(items) + "</ul>")


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
            f'<a href="/tags/{slug}.html">{html.escape(str(tag))}</a>'
        )
    if not links:
        return ""
    return "<p>" + " ".join(links) + "</p>"


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
    return _document(message, f"<h1>{message}</h1>")
