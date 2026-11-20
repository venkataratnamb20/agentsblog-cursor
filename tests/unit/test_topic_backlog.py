"""Tests for the scored topic backlog product artifact.

The backlog at ``docs/product/topic-backlog.md`` scores draft ideas by
reader value and effort so the editorial calendar can pick the next
post without guessing. It does not approve or publish any post.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

_BACKLOG = Path(__file__).resolve().parents[2] / "docs" / "product" / "topic-backlog.md"

_PILLARS = (
    "Foundations",
    "Building",
    "Evaluation",
    "Safety",
    "Operations",
)

# Priority = reader_value / effort (higher is better for next-draft pick).
_PRIORITY_RULE = "priority = reader value / effort"


def _table_rows(text: str) -> list[dict[str, str]]:
    """Parse markdown pipe tables into lower-cased header maps.

    Args:
        text: Full markdown document.

    Returns:
        One dict per data row. Keys are stripped, lower-cased headers.
    """
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= {"-", ":"} and c for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(header, cells, strict=True)))
    return rows


def _topic_rows(text: str) -> list[dict[str, str]]:
    """Return backlog rows that include pillar and score columns.

    Args:
        text: Full markdown document.

    Returns:
        Rows that look like scored topics.
    """
    required = {"topic", "pillar", "reader value", "effort", "priority"}
    return [
        row
        for row in _table_rows(text)
        if required.issubset(row.keys())
    ]


class TestTopicBacklog(unittest.TestCase):
    """Topic backlog exists, scores ideas, and covers every pillar."""

    def test_backlog_defines_scoring_and_lists_scored_topics(self) -> None:
        """Scoring rule, five pillars, eight topics, and no publish approval."""
        self.assertTrue(
            _BACKLOG.is_file(),
            f"missing topic backlog: {_BACKLOG}",
        )
        text = _BACKLOG.read_text(encoding="utf-8")

        self.assertIn("reader value", text.lower())
        self.assertIn("1–5", text.replace("1-5", "1–5"))
        self.assertIn("effort", text.lower())
        self.assertRegex(
            text,
            re.compile(r"priority\s*=\s*reader value\s*/\s*effort", re.I),
            f"backlog must document {_PRIORITY_RULE}",
        )
        self.assertIn("not approved for publication", text.lower())

        topics = _topic_rows(text)
        self.assertGreaterEqual(
            len(topics),
            8,
            "backlog must list at least 8 scored topics",
        )

        pillars_seen = {row["pillar"] for row in topics}
        for pillar in _PILLARS:
            self.assertIn(
                pillar,
                pillars_seen,
                f"backlog must include a topic for pillar {pillar}",
            )

        for row in topics:
            value = int(row["reader value"])
            effort = int(row["effort"])
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 5)
            self.assertGreaterEqual(effort, 1)
            self.assertLessEqual(effort, 5)
            expected = value / effort
            actual = float(row["priority"])
            self.assertAlmostEqual(
                actual,
                expected,
                places=2,
                msg=(
                    f"{row['topic']}: priority must be "
                    f"reader value / effort ({value}/{effort}={expected})"
                ),
            )


if __name__ == "__main__":
    unittest.main()
