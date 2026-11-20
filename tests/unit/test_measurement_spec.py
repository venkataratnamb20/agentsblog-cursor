"""Tests for the local SEO and analytics measurement contract.

The spec at ``docs/seo/measurement.md`` names KPIs and KPMs that can
be checked in the repo. It must not choose a vendor or store credentials.
"""

from __future__ import annotations

import unittest
from pathlib import Path

_SPEC = Path(__file__).resolve().parents[2] / "docs" / "seo" / "measurement.md"

_REQUIRED_SUBSTRINGS = (
    "KPI",
    "KPM",
    "published posts",
    "WCAG 2.2 AA",
    "127.0.0.1",
    "Venkat",
    "no analytics vendor",
    "no credential",
)


class TestMeasurementSpec(unittest.TestCase):
    """The measurement spec exists and states the local contract."""

    def test_spec_names_local_kpis_kpms_and_approval_gate(self) -> None:
        """Required phrases and the KPI table are present in the spec."""
        self.assertTrue(
            _SPEC.is_file(),
            f"missing measurement spec: {_SPEC}",
        )
        text = _SPEC.read_text(encoding="utf-8")
        for needle in _REQUIRED_SUBSTRINGS:
            self.assertIn(needle, text)
        header = [
            line
            for line in text.splitlines()
            if line.strip().startswith("|")
            and "Metric" in line
            and "Target" in line
            and "Today" in line
        ]
        self.assertTrue(
            header,
            "local KPI table must include columns Metric, Target, and Today",
        )


if __name__ == "__main__":
    unittest.main()
