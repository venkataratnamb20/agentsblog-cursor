# Editorial Content Qa Checklist Applies To Every Post

## Status

Status: In progress

## Evidence

- RED: `python -m unittest tests.unit.test_editorial_qa -v` failed with 2 failures while `docs/editorial/content-qa-checklist.md` was missing (`FileNotFound` / `is_file` assert).
- GREEN: after adding the checklist, `python -m unittest tests.unit.test_editorial_qa -v` passed (2 tests).
- `docs/editorial/content-qa-checklist.md` covers claim accuracy and sources cited, one-idea structure with clear headings, voice for AI engineers / researchers / tech leads, no secrets or credentials, SEO title / description / slug, `draft: true` until Venkat approves publish, and code samples correct or marked unverified.
- `tests/unit/test_editorial_qa.py` asserts the checklist file exists and contains those required gates (case-insensitive).

## Remaining

- Venkat has not approved closing this task.
- Exit criteria are not met; status stays In progress (not Done).
- Hand-off to seo-audit of the checklist wording is still open if required by the per-post workflow owner.
- No post has been run through this checklist yet.
