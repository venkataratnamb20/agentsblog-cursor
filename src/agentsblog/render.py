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


_FEED_LINK = (
    '<link rel="alternate" type="application/rss+xml" '
    'href="/feed.xml" title="Agents Blog">'
)


_THEME_SCRIPT = """\
<script>
document.getElementById("theme-toggle").addEventListener("click", function () {
  var root = document.documentElement;
  var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
});
</script>
"""


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
        f"{_FEED_LINK}"
        "</head>"
        "<body>"
        f"<main>{main}</main>"
        '<button id="theme-toggle" type="button">Toggle theme</button>'
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
    search_link = '<p><a href="search.html">Search</a></p>'
    return _document("Agents Blog", search_link + listing)


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


def render_not_found() -> str:
    """Render the page shown when a request has no document.

    Returns:
        HTML that tells the reader the page was not found.
    """
    message = html.escape("Page not found")
    return _document(message, f"<h1>{message}</h1>")
