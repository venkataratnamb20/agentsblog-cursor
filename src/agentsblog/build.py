"""Build the local static site from markdown posts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from agentsblog.posts import Post, load_posts
from agentsblog.render import (
    render_index,
    render_not_found,
    render_post,
    render_search,
)

_CONTENT = Path("content") / "posts"
_OUTPUT = Path("build")
_STYLESHEET = """\
:root {
  color-scheme: light dark;
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
"""


def build_site(content_dir: Path, output_dir: Path) -> None:
    """Write the static site for one content directory.

    Published posts become the index, post pages, and the search
    index. Drafts stay out of all three. A missing content directory
    produces an empty site: an index, a not-found page, an empty
    search index, and the stylesheet.

    Args:
        content_dir: Directory of markdown posts.
        output_dir: Directory that receives the built site. Existing
            contents are replaced.
    """
    posts = _load_posts(content_dir)
    published = _published(posts)
    _prepare_output(output_dir)
    _write_text(output_dir / "index.html", render_index(posts))
    _write_text(output_dir / "search.html", render_search())
    _write_post_pages(output_dir / "posts", published)
    _write_text(output_dir / "404.html", render_not_found())
    _write_text(output_dir / "search-index.json", _search_index(published))
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


def _write_post_pages(posts_dir: Path, posts: list[Post]) -> None:
    """Write one HTML file for each post.

    Args:
        posts_dir: Directory that receives ``{slug}.html`` files.
        posts: Posts to publish. The caller omits drafts.
    """
    for post in posts:
        page = posts_dir / f"{post.slug}.html"
        _write_text(page, render_post(post))


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
