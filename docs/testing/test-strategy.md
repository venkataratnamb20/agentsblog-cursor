# Test strategy

Agents Blog checks behavior with the Python standard library. The local
builder is `src/agentsblog/build.py`. The test runner is:

```text
python -m unittest discover -s tests -v
```

`.\make.ps1 test` (and `make test` on Unix) runs that command when
`tests/` exists. The same discovery run covers `tests/unit/`,
`tests/integration/`, and any unittest modules under `tests/features/`
(today that is a pending-journey catalog check only).

## make.ps1 targets

| Target | Behavior today |
| --- | --- |
| `test` | Runs `python -m unittest discover -s tests -v` when `tests/` exists; otherwise prints that there is nothing to run and exits 0 |
| `test-e2e` | Stub. Prints that end-to-end tests will run once the stack is chosen, then exits 0. No Playwright (or other browser) cases exist |
| `test-bdd` | Stub. Prints that Gherkin journeys (subscribe, read post, search) will run once the stack is chosen, then exits 0 |
| `coverage` | No-op. Prints the future core-logic 100% / CI 80% intent, then exits 0. No coverage tool is wired; this document states no measured percentage |
| `lint`, `typecheck` | Stubs that print a no-op message and exit 0 until a toolchain lands |

Unix `make` exposes the same target names with the same stub messages.

## Unit tests

Unit tests live in `tests/unit/`. They call one module, or they read a
task-runner script or governance doc, and they use temporary directories
for site output when the builder is under test.

| Area | Tests | What they check |
| --- | --- | --- |
| Posts | `tests/unit/test_posts.py` | Front matter, slug, body, comma-separated tags, draft default, date-then-slug order, missing title, ignored non-markdown files |
| Markdown | `tests/unit/test_markdown.py` | Local markdown rendering used by the builder |
| Render | `tests/unit/test_render.py` | Index lists published posts and omits drafts, post page shows heading and body, title and body are escaped, 404 copy, empty index still has document chrome |
| Theme | `tests/unit/test_theme.py` | Theme stylesheet and theme-toggle chrome on rendered pages |
| Search | `tests/unit/test_search.py`, `tests/unit/test_search_page.py` | Empty and whitespace queries return nothing; title, summary, and tags match without case; drafts are excluded; input order is kept; slug is not searched; the search page has a query box; the build writes `search.html` |
| About / tags | `tests/unit/test_about.py` | About and subscribe pages, per-tag pages; subscribe stays blocked until an email service is approved |
| Build | `tests/unit/test_build.py`, `tests/unit/test_build_hook.py` | `build` runs `compileall` on `scripts` and `tests`, a syntax error fails the target, and the task runner still calls the stdlib builder |
| Feed | `tests/unit/test_feed.py` | The feed includes published posts, skips drafts, escapes titles, is linked from the index, and is written as `feed.xml` |
| SEO | `tests/unit/test_seo.py` | `robots.txt` names the sitemap, sitemap locations are absolute, post pages carry canonical, Open Graph, and schema markup, and the build omits drafts |
| Legal | `tests/unit/test_legal.py` | The build writes privacy, cookies, terms, licences, and AI-assistance pages, each marked as not approved for publication |
| Preview | `tests/unit/test_preview.py` | The preview server binds loopback on port 8000, serves the chosen directory, and `dev` / `preview` invoke that module |
| Consent | `tests/unit/test_consent.py` | The banner offers Accept and Reject, stores only a localStorage choice, and does not set a cookie or call the network |
| Responsive | `tests/unit/test_responsive.py` | Pages include a device-width viewport, and the stylesheet has a max-width 40rem rule |
| Accessibility chrome | `tests/unit/test_a11y.py` | Skip link before nav, `main` id, and theme `aria-pressed` |
| Measurement | `tests/unit/test_measurement_spec.py` | The KPI and KPM spec names local checks and forbids an analytics credential |
| Accessibility audit | `tests/unit/test_a11y_audit.py` | Language, headings, skip link, search label, theme button name, and text contrast on the local preview |
| Performance budgets | `tests/unit/test_performance_budgets.py` | Index HTML and CSS stay within byte budgets and load no remote script or font |
| Security checklist | `tests/unit/test_security_checklist.py` | The local build has no third-party script host and no secret-shaped strings |
| Privacy check | `tests/unit/test_privacy_compliance.py` | Built pages do not assign `document.cookie` or call an analytics host |
| SEO audit | `tests/unit/test_seo_audit.py` | Canonical URLs, Open Graph, robots.txt, the sitemap, and draft exclusion on the local preview |
| Code review gate | `tests/unit/test_code_review_checklist.py` | `docs/guidelines/code-review.md` exists and states the operating-gate rules |

The same discovery run also executes unit checks for the repository
scaffold, agent-skill copy, CI and CD workflow text, developer and
reader docs, the manual catalog, progress records, harness and stage
0A/0B artifacts, and editorial or research docs that already have
modules under `tests/unit/`. Those checks prove documents and scripts
on disk. They do not replace a browser run.

## Integration tests

Integration tests live in `tests/integration/`.

The site build (`tests/integration/test_site_build.py`) writes a
temporary content directory through `build_site` and reads the output.
A published post appears on the index, as `posts/<slug>.html`, and in
`search-index.json`. A draft is absent from the index, has no post
page, and is absent from the search index. The build also writes
`404.html` and `assets/site.css`.

`tests/integration/test_repo_contract.py` checks that
`scripts/sync_agents.py` and `tests/` compile, and that `src`,
`content`, `tests`, `docs`, `research`, and `scripts` exist.

## Manual checks

A person runs the checklist in
[manual-tests.md](manual-tests.md) at the repository root on Windows.
Check an item only after its expected result holds. Do not publish the
site, spend money, or create accounts while running the steps.

| Group | What the person checks |
| --- | --- |
| Harness | `.\make.ps1 test` exits 0, `.\make.ps1 build` writes `build/index.html`, `build/search.html`, `build/feed.xml`, and `build/privacy.html` (privacy says it is not approved), `python -m unittest discover -s tests -v` passes, and `.\make.ps1 sync-agents` copies skills as real directories |
| Developer docs | `AGENTS.md`, `docs/developers.md`, and `docs/users.md` match claims that can be checked on this machine. The site is not live |
| End-user docs | `docs/users.md` matches local posts under `content/posts/` and the fact that no site is running |
| Not available yet | The four-tool smoke test (Claude Code, Codex, Cursor, Antigravity) is listed as not run and is not launched |
| Local preview journeys | Subscribe is blocked until an email service is approved. Read post: a published markdown file under `content/posts/` shows its title and body in `build/posts/<slug>.html` after `.\make.ps1 build`, and the post is not published. Search: `.\make.ps1 preview` at `http://127.0.0.1:8000/search.html` lists a post for a word in a published title, and a blank query lists nothing |

`tests/features/test_journeys_pending.py` asserts that the manual
catalog still records local read/search as working and subscribe as
blocked. It is not a Gherkin runner and not a browser test.

## Quality gates

[code-quality.md](../guidelines/code-quality.md) sets the gates. The
ones that apply to this strategy:

| Gate | Rule today |
| --- | --- |
| Tests pass | `.\make.ps1 test` and `python -m unittest discover -s tests -v` exit 0. Every discovered test passes |
| CI coverage | Future threshold: 80% minimum. The gate is never lowered. It is not measured. `.\make.ps1 coverage` (and `make coverage`) prints a no-op message and exits 0 until a coverage tool exists |
| Core logic | Future threshold: 100% of domain rules and application services, once a coverage tool exists. Generated code and thin adapters sit outside that target and still count toward the 80% CI gate. Core coverage is not measured |

A stub that exits 0 is not a coverage result. Cyclomatic complexity (at
most 10 per function), function length (at most 40 lines, excluding
blank lines and comments), and zero lint warnings are the other gates
in `code-quality.md`. They become failing checks when the lint tool
exists.

## Gaps

These checks are not in the suite:

- No Playwright (or other) browser end-to-end tests. `tests/e2e/` holds
  only package scaffolding (`.gitkeep` / `__init__.py`). `test-e2e` is a
  stub that exits 0 without launching a browser.
- No visual regression. Nothing compares screenshots or rendered pixels.
- No cross-browser run. Nothing launches a second browser engine.
- The coverage target does not measure yet. `coverage` does not collect a
  figure, so this document states no coverage percentage.
- `test-bdd` does not execute the subscribe, read-post, or search
  Gherkin scenarios from `code-quality.md`. Those journeys are checked by
  hand in `manual-tests.md`. Subscribe stays blocked until an email
  service is approved.

## Code review checklist

The operating gate is
[docs/guidelines/code-review.md](../guidelines/code-review.md). Apply
that document to a pull request before approving it. The reviewer is the
person named on the task and is not the author. One review is required.
Required checks must be green. Publishing the site, production deploys,
and DNS changes stay behind Venkat's approval.

Summary of the gate (full wording lives in `code-review.md`):

- [ ] Tests cover the change. A behavior change has a failing test first, then the smallest code that makes it pass. Docs-only diffs say which claims a person can check.
- [ ] `python -m unittest discover -s tests -v` passes, or `.\make.ps1 test` passes.
- [ ] The diff contains no secrets, credentials, tokens, private keys, or `.env` files.
- [ ] The diff does not deploy to production, change DNS, or publish the site without Venkat approval. `release` does not deploy.
- [ ] Drafts are not published. A `draft: true` post stays out of the index, the feed, the sitemap, and search.
