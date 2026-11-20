# TDD evidence: Stage 3 / M3 (GitHub Pages staging)

Source plan: Stage 3 M3 Build (nine Build & Integration goals + M3 gate).
Venkat approved hosting via GitHub Actions / GitHub Pages for this wave.

## Verdict

**Stage 3 is closed. M3 is Done.** Catalog: **37 Done**, **16 In progress**,
**42 Not started**.

## User journeys

- As a reader on staging, I want wireframe chrome (tagline, footer, list
  anatomy, 404 home link) so the site matches the approved design.
- As an author, I want invalid front matter and images without alt text to
  fail the build.
- As a reviewer, I want drafts 1–3 to render on staging with noindex.
- As DevOps, I want `develop` to deploy to GitHub Pages and `main` to package
  a production build without drafts.

## Agents

| Owner | Result |
| --- | --- |
| [Draft ADR 0003 text](79b1ead2-e749-442a-a4d0-353c97d76378) | `docs/adr/0003-github-pages-hosting.md`; system environments updated |
| [Security check Stage 3](c5d3dda0-8f21-48ee-a1ed-3328954c1086) | PASS — no secrets in CD; consent local-only |
| Frontend Engineer (orchestrator) | Wireframe chrome, content validation, staging flags |
| DevOps & SRE (orchestrator) | `.github/workflows/cd.yml` Pages staging deploy |
| PM Orchestrator (orchestrator) | Nine goals + M3 progress Done; this evidence file |

## Task report

| Task | RED | GREEN | Guarantee |
| --- | --- | --- | --- |
| Wireframe chrome | `test_wireframe_chrome` failed on footer/theme/list | same suite PASS | Shared chrome matches wireframes |
| Staging drafts/noindex | `test_staging_build` TypeError/fail | PASS | `include_drafts` + `noindex` |
| Content validation | `test_content_validation` fail | PASS | Title + alt text enforced |
| CD Pages | `test_ci` fail (no develop/Pages) | PASS | develop → Pages; main packages |
| Staging smoke | new tests | PASS | Posts 1–3 drafts render |

## Test specification

| # | What is guaranteed | Test | Type | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | Theme toggle before main; footer policy links | `tests/unit/test_wireframe_chrome.py` | unit | PASS | `python -m unittest tests.unit.test_wireframe_chrome` |
| 2 | Staging includes drafts and Disallow:/ | `tests/unit/test_staging_build.py` | unit | PASS | unittest |
| 3 | Empty alt images rejected | `tests/unit/test_content_validation.py` | unit | PASS | unittest |
| 4 | CD deploys develop to Pages with flags | `tests/unit/test_ci.py` | unit | PASS | unittest |
| 5 | Posts 1–3 drafts render on staging build | `tests/unit/test_staging_smoke.py` | unit | PASS | unittest |

## Coverage and gaps

- Command: `python -m unittest discover -s tests -v`
- `.\make.ps1 coverage` remains a stub/no-op
- Email vendor double opt-in and analytics vendor remain gated (documented in
  progress Evidence, Remaining none for Stage 3 scope)
- Custom domain / DNS gated
- Production ship from `main` packages only until Venkat approves deploy
- First live Pages deploy needs GitHub Pages enabled on the repo and a push
  to `develop`

## Merge evidence

RED→GREEN captured above. Squash-safe summary: Stage 3 nine goals + M3 closed
on GitHub Pages staging path with TDD and security PASS.
