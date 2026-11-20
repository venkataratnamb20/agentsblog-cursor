"""Build the local static site from markdown posts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

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

#theme-toggle {
  margin-top: 2rem;
}

.skip-link {
  left: 0.5rem;
  position: absolute;
  top: -3rem;
}

.skip-link:focus {
  top: 0.5rem;
}
"""


def build_site(
    content_dir: Path,
    output_dir: Path,
    site_url: str = _DEFAULT_SITE_URL,
) -> None:
    """Write the static site for one content directory.

    Published posts become the index, post pages, and the search
    index. Drafts stay out of all three. A missing content directory
    produces an empty site: an index, a not-found page, an empty
    search index, and the stylesheet.

    Args:
        content_dir: Directory of markdown posts.
        output_dir: Directory that receives the built site. Existing
            contents are replaced.
        site_url: Absolute origin used for feeds, canonical URLs, and
            the sitemap. Defaults to the local preview origin.
    """
    posts = _load_posts(content_dir)
    published = _published(posts)
    _prepare_output(output_dir)
    _write_text(output_dir / "index.html", render_index(posts, site_url))
    _write_text(output_dir / "search.html", render_search())
    _write_post_pages(output_dir / "posts", published, site_url)
    _write_text(output_dir / "404.html", render_not_found())
    _write_reader_pages(output_dir, published)
    _write_policies(output_dir)
    _write_text(output_dir / "search-index.json", _search_index(published))
    _write_text(output_dir / "feed.xml", render_feed(published, site_url))
    _write_discovery(output_dir, published, site_url)
    _write_text(output_dir / "assets" / "site.css", _STYLESHEET)


def main() -> int:
    """Build ``content/posts`` into ``build`` at the repository root.

    A missing or empty post directory still writes the empty index,
    the not-found page, an empty search index, and the stylesheet.

    Returns:
        Zero after the site has been written.
    """
    repo_root = Path(__file__).resolve().parents[2]
    build_site(repo_root / _CONTENT, repo_root / _OUTPUT)
    return 0


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


def _published(posts: list[Post]) -> list[Post]:
    """Drop drafts and keep the loaded order.

    Args:
        posts: Loaded posts, including drafts.

    Returns:
        Posts whose draft flag is false.
    """
    return [post for post in posts if not post.draft]


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
) -> None:
    """Write one HTML file for each post.

    Args:
        posts_dir: Directory that receives ``{slug}.html`` files.
        posts: Posts to publish. The caller omits drafts.
        site_url: Absolute origin used for canonical URLs.
    """
    for post in posts:
        page = posts_dir / f"{post.slug}.html"
        _write_text(page, render_post(post, site_url))


def _write_discovery(
    output_dir: Path,
    posts: list[Post],
    site_url: str,
) -> None:
    """Write robots.txt and sitemap.xml for published pages.

    Args:
        output_dir: Build destination.
        posts: Published posts. The caller omits drafts.
        site_url: Absolute origin.
    """
    origin = site_url.rstrip("/")
    locations = [f"{origin}{path}" for path in _public_paths(posts)]
    _write_text(output_dir / "robots.txt", render_robots(origin))
    _write_text(output_dir / "sitemap.xml", render_sitemap(locations))


def _public_paths(posts: list[Post]) -> list[str]:
    """Return site paths that belong in the sitemap.

    Args:
        posts: Published posts. The caller omits drafts.

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
        posts: Published posts. The caller omits drafts.
    """
    _write_text(output_dir / "about.html", render_about())
    _write_text(output_dir / "subscribe.html", render_subscribe())
    for slug, label, tagged in tag_groups(posts):
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
        posts: Published posts. The caller omits drafts.

    Returns:
        A JSON array. Each object includes the post title.
    """
    records = [_search_record(post) for post in posts]
    return json.dumps(records)


def _search_record(post: Post) -> dict[str, object]:
    """Return the search-index fields for one post.

    Args:
        post: A published post.

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
