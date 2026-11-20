# Accessibility audit (local preview)

Date context: 20 November 2026. This note checks the local HTML preview only. It is not a production review, and it is not a finished human WCAG audit. The public site is not live. Nothing in this check was published or deployed.

The target remains WCAG 2.2 AA. Design rules (focus ring, contrast pair, skip link, heading order, alt text for future media, keyboard paths) live in `docs/design/accessibility.md`. The checks below are the ones a unit test can make without a browser lab.

A human browser and screen-reader audit remains **optional for Stage 3**. Passing these unit checks does not close that audit. Venkat has not accepted a human audit.

## Checks that passed

`tests/unit/test_a11y_audit.py` rendered the current index with `render_index([])`, rendered the search page with `render_search()`, and read `src/agentsblog/build.py` as text for the stylesheet colors. These checks passed:

- The index and the search page use `html lang="en"`.
- Each of those pages has a non-empty document title.
- Each page includes `<main id="main">`.
- A skip link with `href="#main"` appears before `<nav>` on both pages.
- The search page has exactly one `h1`.
- The index has exactly one `h1`, **"Agents Blog"** (including the empty post list). An earlier gap that claimed the empty index had zero headings is closed.
- The search input has a label with `for="search-query"`.
- The theme control is a `button` whose text is `Toggle theme`.
- `#1c1915` on `#f7f4ef` has a calculated contrast of about 15.96:1, which is at least 4.5:1. The test computes relative luminance. Both colors are present in the stylesheet source. Dark theme uses the inverted pair.

## Gaps (implementation / Stage 3)

- Focus rings for links, buttons, and inputs are implemented in
  `src/agentsblog/build.py` (`:focus-visible`).
- No full manual screen-reader pass was run. That pass is optional for Stage 3, not required to close the Stage 2 design spec.
- No browser contrast measurement was run. The 15.96:1 figure is a calculation on the two hex values. It is not a measurement of rendered pixels, focus rings, or the dark theme in a browser.
- Images are not in the fixture, so text alternatives for images were not checked. The alt-text rule for future media is specified in `docs/design/accessibility.md`.
- Focus ring behaviour for ordinary links, the search field, and the theme button is specified in the design doc (WCAG 2.2 AA 2.4.7 Focus Visible; 2.4.11 Focus Not Obscured). The stylesheet today primarily styles `.skip-link` on focus; full ring application in CSS is an implementation follow-up, not a missing design rule.
- Venkat has not accepted a finished human audit.

## What this check does not close

Passing the unit test does not close a WCAG 2.2 AA human audit. A person may still walk the local preview with the keyboard and a screen reader in Stage 3. The public site is not live.
