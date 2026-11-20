# Build 12 Week Editorial Calendar With Owners Per Stage Dec 2026 Feb 2027

## Status

Status: In progress

## Evidence

- RED: `python -m unittest tests.unit.test_editorial_calendar -v` failed with
  `AssertionError: False is not true : missing editorial calendar:
  .../docs/editorial/calendar-2026-q1.md` (file absent before draft).
- GREEN: same command after writing the calendar — `Ran 1 test in 0.012s` /
  `OK`.
- Calendar plan: `docs/editorial/calendar-2026-q1.md` — Weeks 1–12 covering
  December 2026, January 2027, February 2027; each slot names Brief (Product
  Strategist), Draft (Technical Writer), Tech edit (Technical Editor), SEO
  (SEO & Analytics); publish gate states Venkat approval and that nothing in
  the calendar is published.
- Unit test: `tests/unit/test_editorial_calendar.py`.

## Remaining

- Venkat has not approved closing this task.
- Exit criteria are not met.
- Human review of owner assignments and week dates before any content work
  starts. Publishing posts is out of scope for this task.
