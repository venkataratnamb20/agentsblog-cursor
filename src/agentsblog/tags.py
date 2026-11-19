"""Group published posts by tag."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol


class TaggedPost(Protocol):
    """Fields used to group a post under its tags."""

    title: str
    slug: str
    tags: Sequence[str]
    draft: bool


def tag_slug(name: str) -> str:
    """Return a URL slug for a tag name.

    Args:
        name: Tag text from front matter.

    Returns:
        Lowercase letters, digits, and hyphens. Empty when the name
        has no letters or digits.
    """
    characters = [char if char.isalnum() else "-" for char in name.casefold()]
    parts = [part for part in "".join(characters).split("-") if part]
    return "-".join(parts)


def tag_groups(
    posts: Iterable[TaggedPost],
) -> list[tuple[str, str, list[TaggedPost]]]:
    """Group published posts by tag slug.

    Args:
        posts: Posts in reader order. Drafts are ignored.

    Returns:
        ``(slug, first label, posts)`` in the order tags first appear.
        A tag with an empty slug is dropped.
    """
    labels: dict[str, str] = {}
    buckets: dict[str, list[TaggedPost]] = {}
    order: list[str] = []
    for post in posts:
        _collect_post(post, labels, buckets, order)
    return [(slug, labels[slug], buckets[slug]) for slug in order]


def _collect_post(
    post: TaggedPost,
    labels: dict[str, str],
    buckets: dict[str, list[TaggedPost]],
    order: list[str],
) -> None:
    """Add one published post to each of its tag buckets.

    Args:
        post: Candidate post.
        labels: First-seen label for each slug.
        buckets: Posts for each slug.
        order: Slug order of first appearance.
    """
    if post.draft:
        return
    for tag in post.tags:
        slug = tag_slug(tag)
        if not slug:
            continue
        if slug not in buckets:
            labels[slug] = tag
            buckets[slug] = []
            order.append(slug)
        buckets[slug].append(post)
