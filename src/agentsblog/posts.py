"""Load markdown posts and their front matter."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_FENCE = "---"
_TRUE = "true"
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


@dataclass(frozen=True)
class Post:
    """One markdown blog post.

    Attributes:
        title: Post title from front matter.
        slug: Filename stem of the source file.
        date: Publication date, usually ``YYYY-MM-DD``.
        tags: Tag names in file order.
        summary: Short description from front matter.
        body: Markdown after the closing front-matter fence.
        draft: Whether the post is unpublished.
        series: Optional series label. Empty when the post stands alone.
        series_part: One-based part number inside the series, or zero.
        series_total: Total parts in the series, or zero.
    """

    title: str
    slug: str
    date: str
    tags: tuple[str, ...]
    summary: str
    body: str
    draft: bool
    series: str = ""
    series_part: int = 0
    series_total: int = 0


def load_posts(directory: Path) -> list[Post]:
    """Load markdown posts from a directory.

    Drafts and published posts are both returned. Files that are not
    markdown are ignored.

    Args:
        directory: Folder that contains ``.md`` post files.

    Returns:
        Posts sorted by date, then slug.

    Raises:
        ValueError: If a markdown file omits ``title`` or includes an
            image without alt text.
    """
    posts = [
        _load_post(path)
        for path in directory.iterdir()
        if _is_markdown(path)
    ]
    return sorted(posts, key=_sort_key)


def _is_markdown(path: Path) -> bool:
    """Return whether ``path`` is a markdown file.

    Args:
        path: Candidate path inside the post directory.

    Returns:
        True when the path is a file whose suffix is ``.md``.
    """
    return path.is_file() and path.suffix.lower() == ".md"


def _sort_key(post: Post) -> tuple[str, str]:
    """Return the date-then-slug ordering key.

    Args:
        post: Loaded post.

    Returns:
        Date and slug, compared in that order.
    """
    return (post.date, post.slug)


def _load_post(path: Path) -> Post:
    """Parse one markdown file into a post.

    Args:
        path: Markdown file with front matter.

    Returns:
        The parsed post. The slug is the filename stem.

    Raises:
        ValueError: If ``title`` is missing or an image lacks alt text.
    """
    text = path.read_text(encoding="utf-8")
    front_matter, body = _split_document(text)
    fields = _parse_fields(front_matter)
    _require_image_alt(body)
    return Post(
        title=_require_title(fields),
        slug=path.stem,
        date=fields.get("date", "").strip(),
        tags=_parse_tags(fields.get("tags", "")),
        summary=fields.get("summary", "").strip(),
        body=body.strip(),
        draft=_parse_draft(fields.get("draft")),
        series=fields.get("series", "").strip(),
        series_part=_parse_int(fields.get("series_part")),
        series_total=_parse_int(fields.get("series_total")),
    )


def _split_document(text: str) -> tuple[str, str]:
    """Split a document into front matter and body.

    Args:
        text: Full file contents.

    Returns:
        The front-matter block and the text after the closing fence.
        A file without a closed fence yields an empty front matter.
    """
    if not text.startswith(_FENCE):
        return "", text
    parts = text.split(_FENCE, 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def _parse_fields(front_matter: str) -> dict[str, str]:
    """Parse ``key: value`` lines from front matter.

    Args:
        front_matter: Text between the opening and closing fences.

    Returns:
        Field names mapped to stripped values.
    """
    fields: dict[str, str] = {}
    for line in front_matter.splitlines():
        key, separator, value = line.partition(":")
        if separator != ":":
            continue
        fields[key.strip()] = value.strip()
    return fields


def _require_title(fields: dict[str, str]) -> str:
    """Return the title or reject a post that has none.

    Args:
        fields: Parsed front-matter fields.

    Returns:
        The stripped title.

    Raises:
        ValueError: If ``title`` is missing or blank.
    """
    title = fields.get("title", "").strip()
    if not title:
        raise ValueError("post is missing a title")
    return title


def _require_image_alt(body: str) -> None:
    """Reject markdown images that omit alt text.

    Args:
        body: Markdown after the front-matter fence.

    Raises:
        ValueError: If an image token has an empty alt string.
    """
    for match in _IMAGE.finditer(body):
        if match.group(1).strip():
            continue
        raise ValueError("markdown image is missing alt text")


def _parse_tags(raw_tags: str) -> tuple[str, ...]:
    """Split a comma-separated tag list.

    Args:
        raw_tags: Front-matter ``tags`` value.

    Returns:
        Stripped tag names. Empty segments are dropped.
    """
    if not raw_tags:
        return ()
    return tuple(tag.strip() for tag in raw_tags.split(",") if tag.strip())


def _parse_draft(raw_draft: str | None) -> bool:
    """Read the draft flag.

    Args:
        raw_draft: Front-matter ``draft`` value, or None when omitted.

    Returns:
        True when the value is ``true``. Omitted and ``false`` are
        published posts.
    """
    if raw_draft is None:
        return False
    return raw_draft.strip().lower() == _TRUE


def _parse_int(raw_value: str | None) -> int:
    """Parse an optional positive integer field.

    Args:
        raw_value: Front-matter value, or None when omitted.

    Returns:
        The integer, or zero when the field is absent or blank.
    """
    if raw_value is None or not raw_value.strip():
        return 0
    return int(raw_value.strip())
