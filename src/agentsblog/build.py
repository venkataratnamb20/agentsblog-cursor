"""Build the local static site from markdown posts."""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from agentsblog.feed import render_feed
from agentsblog.legal import policy_pages
from agentsblog.posts import Post, load_posts
from agentsblog.render import (
    render_about,
    render_index,
    render_not_found,
    render_page,
    render_post,
    render_search,
    render_subscribe,
    render_tag_page,
)
from agentsblog.seo import render_robots, render_sitemap
from agentsblog.tags import tag_groups

_CONTENT = Path("content") / "posts"
_OUTPUT = Path("build")
_DEFAULT_SITE_URL = "http://127.0.0.1:8000"
_STYLESHEET = """\
:root {
  color-scheme: light dark;
  background: #f7f4ef;
  color: #1c1915;
}

:root[data-theme="dark"] {
  color-scheme: dark;
  background: #1c1915;
  color: #f7f4ef;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    background: #1c1915;
    color: #f7f4ef;
  }
}

body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.5;
  margin: 2rem auto;
  max-width: 40rem;
}

a:focus-visible,
button:focus-visible,
input:focus-visible {
  outline: 2px solid #1c1915;
  outline-offset: 2px;
}

:root[data-theme="dark"] a:focus-visible,
:root[data-theme="dark"] button:focus-visible,
:root[data-theme="dark"] input:focus-visible {
  outline-color: #f7f4ef;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) a:focus-visible,
  :root:not([data-theme="light"]) button:focus-visible,
  :root:not([data-theme="light"]) input:focus-visible {
    outline-color: #f7f4ef;
  }
}

#theme-toggle {
  margin: 1rem 0;
}

.skip-link {
  left: 0.5rem;
  position: absolute;
  top: -3rem;
}

.skip-link:focus {
  background: #f7f4ef;
  color: #1c1915;
  outline: 2px solid #1c1915;
  outline-offset: 2px;
  top: 0.5rem;
}

#cookie-consent {
  background: #f7f4ef;
  border: 1px solid #1c1915;
  color: #1c1915;
  margin-bottom: 1rem;
  padding: 1rem;
}

:root[data-theme="dark"] #cookie-consent {
  background: #1c1915;
  border-color: #f7f4ef;
  color: #f7f4ef;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) #cookie-consent {
    background: #1c1915;
    border-color: #f7f4ef;
    color: #f7f4ef;
  }
}

footer {
  margin-top: 2rem;
}

@media (max-width: 40rem) {
  body {
    margin: 1rem auto;
    max-width: calc(100% - 2rem);
  }
}
"""


def build_site(
    content_dir: Path,
    output_dir: Path,
    site_url: str = _DEFAULT_SITE_URL,
    include_drafts: bool = False,
    noindex: bool = False,
) -> None:
    """Write the static site for one content directory.

    Published posts become the index, post pages, and the search
    index. Drafts stay out unless ``include_drafts`` is True. A
    missing content directory produces an empty site.

    Args:
        content_dir: Directory of markdown posts.
        output_dir: Directory that receives the built site. Existing
            contents are replaced.
        site_url: Absolute origin used for feeds, canonical URLs, and
            the sitemap. Defaults to the local preview origin.
        include_drafts: When True, draft posts are written and listed.
        noindex: When True, robots and meta tags discourage indexing.
    """
    posts = _load_posts(content_dir)
    visible = _visible(posts, include_drafts=include_drafts)
    _prepare_output(output_dir)
    _write_text(
        output_dir / "index.html",
        render_index(
            _index_posts(visible, include_drafts=include_drafts),
            site_url,
            noindex=noindex,
        ),
    )
    _write_text(output_dir / "search.html", render_search())
    _write_post_pages(output_dir / "posts", visible, site_url, noindex=noindex)
    _write_text(output_dir / "404.html", render_not_found())
    _write_reader_pages(output_dir, visible)
    _write_policies(output_dir)
    catalog = [replace(post, draft=False) for post in visible]
    _write_text(output_dir / "search-index.json", _search_index(visible))
    _write_text(output_dir / "feed.xml", render_feed(catalog, site_url))
    _write_discovery(output_dir, catalog, site_url, noindex=noindex)
    _write_text(output_dir / "assets" / "site.css", _STYLESHEET)


def main() -> int:
    """Build ``content/posts`` into ``build`` at the repository root.

    Environment variables:

    - ``AGENTSBLOG_SITE_URL``: Absolute origin for canonicals and feeds.
    - ``AGENTSBLOG_INCLUDE_DRAFTS``: ``1`` / ``true`` includes drafts.
    - ``AGENTSBLOG_NOINDEX``: ``1`` / ``true`` sets staging noindex.

    Returns:
        Zero after the site has been written.
    """
    repo_root = Path(__file__).resolve().parents[2]
    site_url = os.environ.get("AGENTSBLOG_SITE_URL", _DEFAULT_SITE_URL)
    include_drafts = _env_flag("AGENTSBLOG_INCLUDE_DRAFTS")
    noindex = _env_flag("AGENTSBLOG_NOINDEX")
    build_site(
        repo_root / _CONTENT,
        repo_root / _OUTPUT,
        site_url=site_url,
        include_drafts=include_drafts,
        noindex=noindex,
    )
    return 0


def _env_flag(name: str) -> bool:
    """Read a truthy environment flag.

    Args:
        name: Environment variable name.

    Returns:
        True when the value is ``1`` or ``true`` (case-insensitive).
    """
    value = os.environ.get(name, "").strip().lower()
    return value in {"1", "true", "yes"}


def _load_posts(content_dir: Path) -> list[Post]:
    """Load posts, treating a missing directory as empty.

    Args:
        content_dir: Directory of markdown posts.

    Returns:
        Posts from the directory, or an empty list when it is absent.
    """
    if not content_dir.is_dir():
        return []
    return load_posts(content_dir)


def _visible(posts: list[Post], include_drafts: bool) -> list[Post]:
    """Return the posts that belong in the built site.

    Args:
        posts: Loaded posts, including drafts.
        include_drafts: When True, keep drafts.

    Returns:
        Posts in loaded order after the draft filter.
    """
    if include_drafts:
        return list(posts)
    return [post for post in posts if not post.draft]


def _index_posts(
    posts: list[Post],
    include_drafts: bool,
) -> list[SimpleNamespace]:
    """Return index rows that render even when drafts are included.

    Args:
        posts: Visible posts for this build.
        include_drafts: When True, clear the draft flag so the index
            lists staging drafts.

    Returns:
        Namespace objects the index renderer can list.
    """
    rows: list[SimpleNamespace] = []
    for post in posts:
        rows.append(
            SimpleNamespace(
                title=post.title,
                slug=post.slug,
                date=post.date,
                summary=post.summary,
                draft=False if include_drafts else post.draft,
            )
        )
    return rows


def _prepare_output(output_dir: Path) -> None:
    """Replace ``output_dir`` with an empty directory.

    Args:
        output_dir: Build destination.
    """
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)


def _write_post_pages(
    posts_dir: Path,
    posts: list[Post],
    site_url: str,
    noindex: bool = False,
) -> None:
    """Write one HTML file for each post.

    Args:
        posts_dir: Directory that receives ``{slug}.html`` files.
        posts: Posts to publish.
        site_url: Absolute origin used for canonical URLs.
        noindex: When True, ask crawlers not to index post pages.
    """
    for post in posts:
        page = posts_dir / f"{post.slug}.html"
        document = render_post(
            _with_series_nav(post, posts),
            site_url,
            noindex=noindex,
        )
        _write_text(page, document)


def _with_series_nav(post: Post, posts: list[Post]) -> SimpleNamespace:
    """Attach prev/next series links for one post.

    Args:
        post: Post being rendered.
        posts: All visible posts in the build.

    Returns:
        A namespace with post fields plus optional series navigation.
    """
    payload = {
        "title": post.title,
        "slug": post.slug,
        "date": post.date,
        "tags": post.tags,
        "summary": post.summary,
        "body": post.body,
        "draft": post.draft,
        "series": post.series,
        "series_part": post.series_part,
        "series_total": post.series_total,
        "series_prev_slug": "",
        "series_prev_title": "",
        "series_next_slug": "",
        "series_next_title": "",
    }
    if not post.series:
        return SimpleNamespace(**payload)
    siblings = sorted(
        [item for item in posts if item.series == post.series],
        key=lambda item: (item.series_part, item.slug),
    )
    for index, sibling in enumerate(siblings):
        if sibling.slug != post.slug:
            continue
        if index > 0:
            previous = siblings[index - 1]
            payload["series_prev_slug"] = previous.slug
            payload["series_prev_title"] = previous.title
        if index + 1 < len(siblings):
            following = siblings[index + 1]
            payload["series_next_slug"] = following.slug
            payload["series_next_title"] = following.title
        break
    return SimpleNamespace(**payload)


def _write_discovery(
    output_dir: Path,
    posts: list[Post],
    site_url: str,
    noindex: bool = False,
) -> None:
    """Write robots.txt and sitemap.xml for visible pages.

    Args:
        output_dir: Build destination.
        posts: Visible posts for this build.
        site_url: Absolute origin.
        noindex: When True, emit a disallow-all robots file.
    """
    origin = site_url.rstrip("/")
    locations = [f"{origin}{path}" for path in _public_paths(posts)]
    _write_text(
        output_dir / "robots.txt",
        render_robots(origin, noindex=noindex),
    )
    _write_text(output_dir / "sitemap.xml", render_sitemap(locations))


def _public_paths(posts: list[Post]) -> list[str]:
    """Return site paths that belong in the sitemap.

    Args:
        posts: Visible posts for this build.

    Returns:
        Root-relative paths. The not-found page is omitted.
    """
    paths = ["/", "/search.html", "/about.html", "/subscribe.html", "/feed.xml"]
    paths.extend(f"/{page.filename}" for page in policy_pages())
    paths.extend(f"/tags/{slug}.html" for slug, _label, _posts in tag_groups(posts))
    paths.extend(f"/posts/{post.slug}.html" for post in posts)
    return paths


def _write_reader_pages(output_dir: Path, posts: list[Post]) -> None:
    """Write the about page, the subscribe page, and tag pages.

    Args:
        output_dir: Build destination.
        posts: Visible posts for this build.
    """
    _write_text(output_dir / "about.html", render_about())
    _write_text(output_dir / "subscribe.html", render_subscribe())
    # Visible posts already passed the draft filter; clear the flag so
    # tag_groups includes staging drafts that belong in this build.
    catalog = [replace(post, draft=False) for post in posts]
    for slug, label, tagged in tag_groups(catalog):
        document = render_tag_page(label, tagged)
        _write_text(output_dir / "tags" / f"{slug}.html", document)


def _write_policies(output_dir: Path) -> None:
    """Write the draft policy pages.

    Args:
        output_dir: Build destination.
    """
    for page in policy_pages():
        document = render_page(page.title, page.main)
        _write_text(output_dir / page.filename, document)


def _search_index(posts: list[Post]) -> str:
    """Serialize posts as a JSON list of search records.

    Args:
        posts: Visible posts for this build.

    Returns:
        A JSON array. Each object includes the post title.
    """
    records = [_search_record(post) for post in posts]
    return json.dumps(records)


def _search_record(post: Post) -> dict[str, object]:
    """Return the search-index fields for one post.

    Args:
        post: A visible post.

    Returns:
        Title plus the fields a reader search can show.
    """
    return {
        "title": post.title,
        "slug": post.slug,
        "date": post.date,
        "tags": list(post.tags),
        "summary": post.summary,
    }


def _write_text(path: Path, text: str) -> None:
    """Write UTF-8 text, creating parent directories.

    Args:
        path: Destination file.
        text: File contents.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
