"""Tests for case-insensitive search over published posts."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

# The package lives under src/. The required unittest command runs from
# the repository root and does not set PYTHONPATH.
_SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from agentsblog.search import search_posts


def _post(
    title: str,
    slug: str,
    tags: tuple[str, ...],
    summary: str,
    draft: bool,
) -> SimpleNamespace:
    """Build a post stand-in with the fields search reads.

    Args:
        title: Post title.
        slug: URL slug. Search must ignore this field.
        tags: Tag names stored as a tuple.
        summary: Short post summary.
        draft: True when the post is unpublished.

    Returns:
        A ``SimpleNamespace`` with those attributes.
    """
    return SimpleNamespace(
        title=title,
        slug=slug,
        tags=tags,
        summary=summary,
        draft=draft,
    )


class TestSearchPosts(unittest.TestCase):
    """Search returns published posts that match the query, in input order."""

    def test_empty_query_returns_no_posts(self) -> None:
        """A blank query matches nothing, even when posts would otherwise match."""
        post = _post(
            title="Worktrees",
            slug="worktrees",
            tags=("git",),
            summary="How a worktree isolates a task.",
            draft=False,
        )

        self.assertEqual(search_posts([post], ""), [])

    def test_whitespace_query_returns_no_posts(self) -> None:
        """A query of only spaces, tabs, or newlines matches nothing."""
        post = _post(
            title="Worktrees",
            slug="worktrees",
            tags=("git",),
            summary="How a worktree isolates a task.",
            draft=False,
        )

        self.assertEqual(search_posts([post], " \t\n "), [])

    def test_match_is_case_insensitive_on_title(self) -> None:
        """Title matching ignores case and surrounding whitespace in the query."""
        post = _post(
            title="Tool Use",
            slug="other-slug",
            tags=(),
            summary="Unrelated summary.",
            draft=False,
        )

        found = search_posts([post], "  tOOL uSE  ")

        self.assertEqual(found, [post])

    def test_match_is_case_insensitive_on_summary(self) -> None:
        """Summary matching ignores case."""
        post = _post(
            title="Planning",
            slug="planning",
            tags=(),
            summary="How agents plan a task.",
            draft=False,
        )

        found = search_posts([post], "AGENTS PLAN")

        self.assertEqual(found, [post])

    def test_match_is_case_insensitive_on_any_tag(self) -> None:
        """Any tag can match, independent of case."""
        post = _post(
            title="Notes",
            slug="notes",
            tags=("eval", "Tracing"),
            summary="Field notes.",
            draft=False,
        )

        found = search_posts([post], "tracing")

        self.assertEqual(found, [post])

    def test_draft_posts_are_excluded(self) -> None:
        """A draft stays out of the results even when its text matches."""
        draft = _post(
            title="Worktrees",
            slug="draft-worktrees",
            tags=("git",),
            summary="Unpublished notes.",
            draft=True,
        )
        published = _post(
            title="Other topic",
            slug="other-topic",
            tags=(),
            summary="Nothing about the query.",
            draft=False,
        )

        self.assertEqual(search_posts([draft, published], "worktrees"), [])

    def test_results_keep_input_order(self) -> None:
        """Matches keep their relative order and each post appears once."""
        first = _post(
            title="Worktrees",
            slug="worktrees",
            tags=("git", "worktree"),
            summary="Isolating a task.",
            draft=False,
        )
        skipped = _post(
            title="Lint",
            slug="lint",
            tags=("quality",),
            summary="Static checks.",
            draft=False,
        )
        draft = _post(
            title="Worktrees later",
            slug="worktrees-later",
            tags=("worktree",),
            summary="Not ready.",
            draft=True,
        )
        second = _post(
            title="Branches",
            slug="branches",
            tags=("git",),
            summary="Using worktrees safely.",
            draft=False,
        )

        found = search_posts([first, skipped, draft, second], "worktree")

        self.assertEqual(found, [first, second])
        self.assertIs(found[0], first)
        self.assertIs(found[1], second)

    def test_query_with_no_matches_returns_empty_list(self) -> None:
        """A query that hits no published post returns an empty list."""
        post = _post(
            title="Worktrees",
            slug="absent-term",
            tags=("git",),
            summary="How a worktree isolates a task.",
            draft=False,
        )

        self.assertEqual(search_posts([post], "missing"), [])
        self.assertEqual(search_posts([], "worktree"), [])

    def test_slug_is_not_searched(self) -> None:
        """A slug that contains the query does not make the post a match."""
        post = _post(
            title="Notes",
            slug="worktree-notes",
            tags=("git",),
            summary="Unrelated summary.",
            draft=False,
        )

        self.assertEqual(search_posts([post], "worktree"), [])


if __name__ == "__main__":
    unittest.main()
