# TDD evidence: local measurement, consent, and audits

Source plan: none. Journeys were written for this run from the next not-started progress tasks that can be checked on the local preview. No analytics vendor, account, deploy, or post was created.

Checkpoint commits were not split. Six owners edited one working tree at the same time, and the RED and GREEN edits are already mixed. This note is the RED/GREEN record.

## User journeys

- As an SEO lead, I want a KPI and KPM spec that names local checks and what waits for Venkat, so agents do not invent tracking or store credentials.
- As a UK reader, I want a consent choice before any non-essential storage, so the preview follows PECR without a third-party analytics account.
- As a reader on a phone, I want a viewport and a layout that fits a narrow screen.
- As a keyboard reader, I want the local HTML checked against WCAG 2.2 AA rules a unit test can see.
- As a tech lead, I want byte and request budgets on the built pages.
- As a security reviewer, I want the local build checked for third-party scripts and secret-shaped strings.
- As a privacy reviewer, I want proof the built pages do not call an analytics host.
- As an editor, I want an SEO audit of generated pages, including draft exclusion.

## Task report

| Task | Owner | RED | GREEN |
| --- | --- | --- | --- |
| `define-seo-analytics-kpi-kpm-tracking-spec` | [SEO measurement spec](1e55f741-a7bc-4ca8-940a-7e20e1174d9a) | `python -m unittest tests.unit.test_measurement_spec -v` failed: measurement spec missing | same command, 1 test OK |
| `integrate-privacy-friendly-analytics-cookie-consent-uk-gdpr-pecr` | [Consent and viewport](21ed92c8-50b4-4179-a417-b773e5f047fc) | `tests.unit.test_consent` and `tests.unit.test_responsive` errored: `No module named 'agentsblog.consent'` | 6 tests OK. Later copy and storage-guard edits stayed green |
| `cross-browser-responsive-testing` | same frontend owner | included in the consent RED run | viewport and `@media (max-width: 40rem)` tests OK. No Chrome, Firefox, or Safari matrix was run |
| `accessibility-audit-wcag-22-aa` | [Local accessibility audit](dfbf15c3-6930-4d78-921d-6c6b1e390d94) | `test_each_page_has_exactly_one_h1` failed: empty index had `0 != 1` | 6 tests OK after the empty-index assertion was recorded as a gap. A later test, `test_index_has_exactly_one_h1`, is OK after the index gained `<h1>Agents Blog</h1>` |
| `performance-testing-budgets-core-web-vitals` | [Performance budget checks](46a2c174-efb3-4323-bb06-06bc7119b0dd) | `test_budget_doc_names_vitals_and_byte_limits` failed because `docs/testing/performance-budgets.md` was absent. Byte and remote-script checks passed | 3 tests OK |
| `security-vulnerability-checklist` | [Security and privacy checks](9fde95a7-5393-4b6c-824d-48c04430b7c8) | `FileNotFoundError` for `docs/security/launch-checklist.md` | checklist tests OK |
| `privacy-compliance-check` | same security owner | `FileNotFoundError` for `docs/security/privacy-check.md` | privacy tests OK |
| `seo-audit` | [Local SEO audit](e34e4763-2d92-49f3-9120-514c8954e5fd) | `test_audit_record_names_the_local_preview_checks` failed: `docs/seo/audit.md` missing | 2 tests OK |

The progress catalog was RED after those files said `In progress` while `tests/unit/test_progress.py` still required `Not started` (`define-seo-analytics-kpi-kpm-tracking-spec`). After the catalog moved those eight tasks, `python -m unittest discover -s tests -v` reported `Ran 111 tests` and `OK`.

`.\make.ps1 coverage` prints `coverage: no-op until the stack lands` and exits 0. No coverage percentage was measured. The project gate remains 80 percent once a coverage tool exists.

## Test specification

| # | What is guaranteed | Test | Type | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | The measurement spec names KPIs, KPMs, the local origin, and no analytics credential | `tests/unit/test_measurement_spec.py` | unit | PASS | `python -m unittest tests.unit.test_measurement_spec -v` |
| 2 | Accept and Reject record only `agentsblog-consent` in localStorage | `tests/unit/test_consent.py` | unit | PASS | same module |
| 3 | The script does not assign `document.cookie` or call fetch, XHR, sendBeacon, or gtag | `tests/unit/test_consent.py` | unit | PASS | same module |
| 4 | The skip link comes before the banner on the index, search, about, and 404 pages | `tests/unit/test_consent.py` | unit | PASS | same module |
| 5 | Pages declare `width=device-width, initial-scale=1` | `tests/unit/test_responsive.py` | unit | PASS | `python -m unittest tests.unit.test_responsive -v` |
| 6 | The stylesheet has a max-width 40rem rule | `tests/unit/test_responsive.py` | unit | PASS | same module |
| 7 | Index and search declare English, a title, main, a skip link, and a named theme button | `tests/unit/test_a11y_audit.py` | unit | PASS | `python -m unittest tests.unit.test_a11y_audit -v` |
| 8 | The empty index and the search page each have one h1 | `tests/unit/test_a11y_audit.py` | unit | PASS | same module |
| 9 | `#1c1915` on `#f7f4ef` is at least 4.5:1 | `tests/unit/test_a11y_audit.py` | unit | PASS | calculated, not a browser pixel measurement |
| 10 | `index.html` is at most 20000 bytes and `site.css` at most 8000 | `tests/unit/test_performance_budgets.py` | unit | PASS | temp `build_site` |
| 11 | Built HTML has no `<script src=` and no font CDN | `tests/unit/test_performance_budgets.py` | unit | PASS | same module |
| 12 | Built files omit third-party script hosts and secret-shaped markers | `tests/unit/test_security_checklist.py` | unit | PASS | temp `build_site` |
| 13 | Built HTML does not assign `document.cookie` or call an analytics host | `tests/unit/test_privacy_compliance.py` | unit | PASS | temp `build_site` |
| 14 | robots, sitemap, canonical, Open Graph, one h1, and draft exclusion hold when `site_url` is omitted | `tests/unit/test_seo_audit.py` | unit | PASS | temp `build_site` |
| 15 | Thirty-nine tasks are in progress and fifty-six, including M0, are not started | `tests/unit/test_progress.py` | unit | PASS | full discovery |

## Browser check

`python -m agentsblog.preview` served `http://127.0.0.1:8000/`.

- Home showed Skip to content, then Accept and Reject, then the heading Agents Blog.
- Reject stored `agentsblog-consent=rejected`, set `hidden` on the banner, and left `document.cookie` empty.
- The viewport meta was `width=device-width, initial-scale=1`.
- Search exposed a search box named "Search posts" and one heading. The query `agent` added no result rows. `content/posts/` has no published posts.
- `/404.html` is the project not-found page. A path with no file still returns the Python handler's own 404. That handler was not changed in this batch.
- Subscribe has no email field. The theme button moves to pressed.

## Coverage and known gaps

- Coverage is not measured. `.\make.ps1 coverage` is still a no-op.
- No human screen-reader pass, no browser contrast measurement, and no Chrome/Firefox/Safari matrix.
- LCP, INP, and CLS were not measured. The budgets are byte and request limits.
- No production host, TLS, CDN, analytics vendor, or search-engine submission.
- Focus styles for ordinary links are still incomplete. The skip link focus style now has a light background.
- Venkat has not approved closing any of these tasks. None are `Done`.

## Resume after compact

Branch: `feature/local-reader-pages`. The working tree is uncommitted. Do not commit unless asked. Do not mark any parent task `Done`.

The local preview process was stopped on purpose after the browser check. `.\make.ps1 preview` starts it again.

Eight tasks moved to **In progress** (39 in progress, 56 not started, including M0). Catalog: `docs/progress/README.md` and `tests/unit/test_progress.py`. Full suite: `python -m unittest discover -s tests -v` → 111 tests, OK. `.\make.ps1 coverage` is still a no-op.

Do not redo consent, the measurement spec, the local audits, or the progress-catalog move. A missing URL still returns Python's handler 404; `/404.html` is the project page. No analytics vendor, account, deploy, or published post.

Next not-started work that can stay local, in progress-index order: `code-review-every-pr-reviewed-against-the-checklist`, then editorial docs (`define-per-post-workflow-brief-draft-tech-edit-seo-approval-publish-distribute`, `editorial-content-qa-checklist-applies-to-every-post`, `create-topic-backlog-score-ideas-reader-value-x-effort`). Hosting, DNS, publishing, social posts, and new accounts still wait for Venkat.
