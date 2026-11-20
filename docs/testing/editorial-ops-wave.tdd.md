# TDD evidence: editorial ops wave

Source plan: none. Journeys came from the next local not-started progress
tasks after `docs/testing/local-measurement-consent-audits.tdd.md`. No
posts published, no accounts, no deploy, no commit required for this note.

## User journeys

- As a named PR reviewer, I want a single code-review checklist that forbids
  secrets, deploys, DNS changes, and publishing without Venkat.
- As an editor, I want a per-post stage order with one Agent Owner per stage.
- As a technical editor, I want a content QA checklist before publish approval.
- As a product strategist, I want topics scored by reader value and effort.
- As a PM, I want a 12-week calendar (Dec 2026–Feb 2027) with stage owners.

## Task report

| Task | Owner | RED | GREEN |
| --- | --- | --- | --- |
| `code-review-every-pr-reviewed-against-the-checklist` | [Code-review checklist TDD](61278c58-61e1-4f1f-b61f-a686ba741f7c) | missing `docs/guidelines/code-review.md` | `tests.unit.test_code_review_checklist` OK |
| `define-per-post-workflow-brief-draft-tech-edit-seo-approval-publish-distribute` | [Per-post workflow TDD](5c3b3733-b3b4-4060-9169-6e1d5c28a022) | 4 failures, missing workflow doc | 4 OK |
| `editorial-content-qa-checklist-applies-to-every-post` | [Editorial QA checklist TDD](806462b8-47b0-4e8f-b087-e4b432e660ca) | 2 failures, missing checklist | 2 OK |
| `create-topic-backlog-score-ideas-reader-value-x-effort` | [Topic backlog scoring TDD](3a642287-dd66-4d6c-bacf-b49ef8028c9c) | missing `docs/product/topic-backlog.md` | `tests.unit.test_topic_backlog` OK |
| `build-12-week-editorial-calendar-with-owners-per-stage-dec-2026-feb-2027` | [Editorial calendar TDD](9962a1fb-b991-46ea-9a96-80cd6b942ad5) | missing `docs/editorial/calendar-2026-q1.md` | `tests.unit.test_editorial_calendar` OK |

Scoring rule chosen: `priority = reader value / effort` (higher is better).
Calendar weeks 11–12 point at the backlog Operations topics.

## Test specification

| # | What is guaranteed | Test | Type | Result |
| --- | --- | --- | --- | --- |
| 1 | Code-review gate names TDD, green tests, no secrets, no deploy/DNS/publish, drafts stay draft, author cannot self-approve | `tests/unit/test_code_review_checklist.py` | unit | PASS |
| 2 | Stages Brief→…→Distribute with team owners; Publish/Distribute need Venkat; hand-off fields present | `tests/unit/test_per_post_workflow.py` | unit | PASS |
| 3 | Editorial QA covers accuracy, structure, voice, secrets, SEO, draft gate, code samples | `tests/unit/test_editorial_qa.py` | unit | PASS |
| 4 | Backlog defines scoring, ≥8 topics, all five pillars, not approved for publication | `tests/unit/test_topic_backlog.py` | unit | PASS |
| 5 | Calendar covers Dec 2026–Feb 2027, weeks 1–12, stage owners, nothing published | `tests/unit/test_editorial_calendar.py` | unit | PASS |
| 6 | Forty-four tasks in progress, fifty-one not started including M0 | `tests/unit/test_progress.py` | unit | PASS |

## Coverage and known gaps

- `.\make.ps1 coverage` remains a no-op. No coverage percentage.
- No real PR has been reviewed against the code-review checklist yet.
- No post has been run through the editorial QA checklist.
- Venkat has not approved closing any of these tasks. None are `Done`.

## Resume

Branch: `feature/local-reader-pages`. Working tree may be uncommitted. Do not
commit unless asked. Do not mark parent tasks Done.

Next local work that still waits for Venkat for hosting/accounts: draft
briefs from the top of `docs/product/topic-backlog.md` (post-1 first), or
apply the code-review checklist to a real PR. Hosting, DNS, publishing, and
new accounts still wait for Venkat.
