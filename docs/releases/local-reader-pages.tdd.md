# TDD evidence: local reader pages

## Source plan

Journeys were derived during this TDD run from `docs/users.md`, `docs/guidelines/code-quality.md`, and `docs/progress/fortnightly-project-status-updates.md`. No plan file was executed.

## User journeys

- As a reader, I want to search published posts on the local preview, so that a blank query shows nothing and a matching title is listed.
- As a reader, I want to switch the page between light and dark.
- As a reader, I want an RSS feed of published posts, with drafts omitted.
- As a reader, I want canonical, Open Graph, and schema.org metadata, plus robots.txt and a sitemap that skips drafts.
- As a reader, I want policy pages that say they are drafts and are not approved for publication.
- As a reader, I want a post body to keep headings and paragraphs, with raw HTML escaped.

## Test specification

| # | What is guaranteed | Test file | Test type | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | The build writes a search page that ignores a blank query | `tests/unit/test_search_page.py` | unit | PASS | `python -m unittest tests.unit.test_search_page` |
| 2 | The theme button sets dark and light, and the stylesheet paints a dark background | `tests/unit/test_theme.py` | unit | PASS | `python -m unittest tests.unit.test_theme` |
| 3 | RSS includes published posts, skips drafts, and escapes titles | `tests/unit/test_feed.py` | unit | PASS | `python -m unittest tests.unit.test_feed` |
| 4 | Robots, sitemap, canonical, Open Graph, and BlogPosting are written, and drafts stay out of the sitemap | `tests/unit/test_seo.py` | unit | PASS | `python -m unittest tests.unit.test_seo` |
| 5 | Headings and paragraphs render, and `<` in a heading is escaped | `tests/unit/test_markdown.py` | unit | PASS | `python -m unittest tests.unit.test_markdown` |
| 6 | Draft policy pages name UK GDPR and PECR and say Venkat has not approved publication | `tests/unit/test_legal.py` | unit | PASS | `python -m unittest tests.unit.test_legal` |

## Coverage and known gaps

The project `coverage` target does not run a coverage tool yet. These tests were run with `python -m unittest`. Intentional gaps: no public host, no email service, no published posts, no end-to-end browser suite, and no visual regression. Subscribe stays blocked until an email service is approved.

## Merge evidence

RED commits add the failing tests. GREEN commits add the smallest implementation that makes those tests pass. Checkpoint commits are on `feature/local-reader-pages`.
