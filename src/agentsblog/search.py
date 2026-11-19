"""Search published posts by title, summary, and tags."""

from collections.abc import Iterable, Sequence
from typing import Protocol


class _SearchablePost(Protocol):
    """Post fields that search is allowed to read.

    The blog post type stays outside this module. Any object with these
    attributes can be searched.
    """

    title: str
    summary: str
    tags: Sequence[str]
    draft: bool


def search_posts(
    posts: Iterable[_SearchablePost],
    query: str,
) -> list[_SearchablePost]:
    """Return published posts that match a query.

    Matching is a case-insensitive substring check of the title, the
    summary, and every tag. Draft posts are omitted. Results follow the
    order of ``posts``.

    Args:
        posts: Posts in the order a reader should see matches.
        query: Text to find. An empty or whitespace-only query matches
            nothing. Surrounding whitespace is ignored.

    Returns:
        Matching published posts, in input order. The list is empty when
        the query is blank or nothing matches.
    """
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return []

    # One pass keeps input order. Each post checks a fixed set of fields.
    return [
        post
        for post in posts
        if not post.draft and _matches(post, normalized_query)
    ]


def _matches(post: _SearchablePost, normalized_query: str) -> bool:
    """Return whether the query occurs in the post's searchable text.

    Args:
        post: Post whose title, summary, and tags are checked.
        normalized_query: Query already stripped and casefolded.

    Returns:
        True when the query is a substring of the title, summary, or a tag.
    """
    searchable_text = (post.title, post.summary, *post.tags)
    return any(normalized_query in text.casefold() for text in searchable_text)
