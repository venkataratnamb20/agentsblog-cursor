# Accessibility Audit WCAG 2.2 AA

## Status

Status: In progress

## Evidence

- `docs/design/accessibility-audit.md` records the local preview checks that passed and the gaps that remain.
- `tests/unit/test_a11y_audit.py` passes against the current index, search page, and stylesheet colors.

## Remaining

- A human audit in a browser was not run. There was no manual screen-reader pass and no browser contrast measurement. The empty index has no `h1`, images are not in the fixture, and the focus style for ordinary links is not fully specified.
- Venkat has not approved closing this task.
- Exit criteria are not met.
