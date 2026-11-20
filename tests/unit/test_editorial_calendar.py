"""Tests for the Dec 2026–Feb 2027 editorial calendar plan.

The calendar at ``docs/editorial/calendar-2026-q1.md`` is a planning
document only. It must name stage owners and must not publish posts.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

_CALENDAR = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "editorial"
    / "calendar-2026-q1.md"
)

_MONTHS = (
    "December 2026",
    "January 2027",
    "February 2027",
)

_STAGE_OWNERS = (
    ("Brief", "Product Strategist"),
    ("Draft", "Technical Writer"),
    ("Tech edit", "Technical Editor"),
    ("SEO", "SEO & Analytics"),
)


class TestEditorialCalendar(unittest.TestCase):
    """The 12-week calendar exists with owners and a publish gate."""

    def test_calendar_covers_window_weeks_owners_and_publish_gate(self) -> None:
        """Assert months, 12 weeks, stage owners, and no-publish gate."""
        self.assertTrue(
            _CALENDAR.is_file(),
            f"missing editorial calendar: {_CALENDAR}",
        )
        text = _CALENDAR.read_text(encoding="utf-8")

        for month in _MONTHS:
            self.assertIn(
                month,
                text,
                f"calendar must cover {month}",
            )

        week_labels = re.findall(
            r"(?im)^(?:#+\s*)?week\s*([1-9]|1[0-2])\b",
            text,
        )
        unique_weeks = {int(label) for label in week_labels}
        self.assertEqual(
            unique_weeks,
            set(range(1, 13)),
            "calendar must clearly label weeks 1–12",
        )

        for stage, role in _STAGE_OWNERS:
            self.assertRegex(
                text,
                re.compile(
                    rf"(?is){re.escape(stage)}.{{0,80}}{re.escape(role)}",
                ),
                f"each slot must name {role} for {stage}",
            )
            # Require the stage owner pair on enough rows for 12 weeks.
            pair_hits = len(
                re.findall(
                    rf"(?is){re.escape(stage)}.{{0,80}}{re.escape(role)}",
                    text,
                )
            )
            self.assertGreaterEqual(
                pair_hits,
                12,
                f"need {stage} → {role} on all 12 weekly slots "
                f"(found {pair_hits})",
            )

        self.assertIn("Venkat", text)
        self.assertRegex(
            text,
            re.compile(r"(?is)publish.{0,120}venkat.{0,80}approval"),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(?is)(nothing|no\s+post|none).{0,80}(published|publish)"
            ),
        )


if __name__ == "__main__":
    unittest.main()
