# TDD evidence: content briefs and first draft wave

Source plan: content briefs draft wave (attached plan; not executed as
instructions). No posts published. No Zotero/Notion accounts. No commit
required for this note.

## User journeys

- As a product strategist, I want a post-1 brief with audience, claim,
  pillar, and slug before prose is written.
- As a research analyst, I want a citeable research pack for that claim.
- As a technical writer, I want a review-ready draft with `draft: true`
  that never appears on the built index.
- As a product strategist, I want a post-2 brief for calendar week 2.
- As a research analyst, I want a local research library layout without
  creating Zotero or Notion accounts.

## Task report

| Task / goal | Owner | RED | GREEN |
| --- | --- | --- | --- |
| post-1 brief | [Post-1 brief TDD](3eeea6db-bc5f-47eb-bd52-67d4f31b134d) | missing brief | `tests.unit.test_brief_post1` OK |
| post-1 research pack | [Post-1 research pack TDD](0bc75f01-5d46-4e4a-88c8-6bac42b6757c) | missing pack | `tests.unit.test_research_pack_post1` OK |
| post-1 draft | [Post-1 draft TDD](b882d91a-2e55-4c01-9a55-367248c6d05b) | missing draft | `tests.unit.test_draft_post1` OK (4) |
| post-2 brief | [Post-2 brief TDD](a9b5dc78-5a4a-4d08-bf4b-18a5725ee94e) | missing brief | `tests.unit.test_brief_post2` OK |
| research library | [Research library TDD](56ffaa0f-4bdf-49b2-97bf-d58f63f23b9c) | missing READMEs | `tests.unit.test_research_library` OK (4) |

Progress catalog: three parent tasks moved to In progress (post-1, post-2,
reference library). Catalog counts **47** in progress, **48** not started
(including M0). Plan goal count was five agents; only three progress
slugs advanced.

## Test specification

| # | What is guaranteed | Test | Result |
| --- | --- | --- | --- |
| 1 | Post-1 brief names contract title, slug, Foundations, audience, claim, not published | `tests/unit/test_brief_post1.py` | PASS |
| 2 | Research pack has ≥3 public sources mapped to agent/workflow/chatbot | `tests/unit/test_research_pack_post1.py` | PASS |
| 3 | Draft has front matter + headings; build omits title from index | `tests/unit/test_draft_post1.py` | PASS |
| 4 | Post-2 brief names anatomy slug, Foundations, ReAct/tools/memory claim | `tests/unit/test_brief_post2.py` | PASS |
| 5 | Local research library docs; Zotero/Notion wait for Venkat | `tests/unit/test_research_library.py` | PASS |
| 6 | Forty-seven in progress, forty-eight not started including M0 | `tests/unit/test_progress.py` | PASS |

## Coverage and known gaps

- `.\make.ps1 coverage` remains a no-op.
- Tech edit and SEO for post-1 not started.
- Post-2 has a brief only (no draft).
- Venkat has not approved closing any of these tasks. None are `Done`.

## Resume

Branch: `feature/local-reader-pages`. Do not commit unless asked. Do not
mark parent tasks Done. Next: tech-edit post-1 against
`docs/editorial/content-qa-checklist.md`, then SEO. Hosting, DNS,
publishing, Zotero/Notion, and social still wait for Venkat.
