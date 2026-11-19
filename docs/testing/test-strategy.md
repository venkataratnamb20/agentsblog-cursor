# Test strategy

Agents Blog checks behavior with the Python standard library. The local
builder is `src/agentsblog/build.py`. The test runner is:

```text
python -m unittest discover -s tests -v
```

`.\make.ps1 test` (and `make test` on Unix) runs that command when
`tests/` exists. `test-e2e` and `coverage` are still stubs: each prints
a message and exits 0. `test-bdd` is the same kind of stub. This
document does not report a measured coverage percentage. No coverage
tool has been run.

## Unit tests

Unit tests live in `tests/unit/`. They call one module, or they read a
task-runner script, and they use temporary directories for site output.

| Area | Tests | What they check |
| --- | --- | --- |
| Posts | `tests/unit/test_posts.py` | Front matter, slug, body, comma-separated tags, draft default, date-then-slug order, missing title, ignored non-markdown files |
| Render | `tests/unit/test_render.py` | Index lists published posts and omits drafts, post page shows heading and body, title and body are escaped, 404 copy, empty index still has document chrome |
| Search | `tests/unit/test_search.py`, `tests/unit/test_search_page.py` | Empty and whitespace queries return nothing; title, summary, and tags match without case; drafts are excluded; input order is kept; slug is not searched; the search page has a query box; the build writes `search.html` |
| Build | `tests/unit/test_build.py`, `tests/unit/test_build_hook.py` | `build` runs `compileall` on `scripts` and `tests`, a syntax error fails the target, and the task runner still calls the stdlib builder |
| Feed | `tests/unit/test_feed.py` | The feed includes published posts, skips drafts, escapes titles, is linked from the index, and is written as `feed.xml` |
| SEO | `tests/unit/test_seo.py` | `robots.txt` names the sitemap, sitemap locations are absolute, post pages carry canonical, Open Graph, and schema markup, and the build omits drafts |
| Legal | `tests/unit/test_legal.py` | The build writes privacy, cookies, terms, licences, and AI-assistance pages, each marked as not approved for publication |
| Preview | `tests/unit/test_preview.py` | The preview server binds loopback on port 8000, serves the chosen directory, and `dev` / `preview` invoke that module |

The same discovery run also executes unit checks for markdown
rendering, the theme stylesheet, the repository scaffold, agent-skill
copy, developer and reader docs, the manual catalog, CI and CD workflow
text, and progress records. Those modules sit beside the table above.
They do not replace a browser run.

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

## Quality gates

[code-quality.md](../guidelines/code-quality.md) sets the gates. The
ones that apply to this strategy:

| Gate | Rule today |
| --- | --- |
| Tests pass | `.\make.ps1 test` and `python -m unittest discover -s tests -v` exit 0. Every discovered test passes |
| CI coverage | Future threshold: 80% minimum. The gate is never lowered. It is not measured. `coverage` prints a no-op message and exits 0 until a coverage tool exists |
| Core logic | Future threshold: 100% of domain rules and application services, once a coverage tool exists. Generated code and thin adapters sit outside that target and still count toward the 80% CI gate. Core coverage is not measured |

`lint`, `typecheck`, and `coverage` are stubs until a compiler, linter,
or coverage tool is wired to those target names. A stub that exits 0 is
not a coverage result. Cyclomatic complexity (at most 10 per function),
function length (at most 40 lines, excluding blank lines and comments),
and zero lint warnings are the other gates in `code-quality.md`. They
become failing checks when the lint tool exists.

## Gaps

These checks are not in the suite:

- No browser end-to-end tests. `tests/e2e/` has no cases. `test-e2e` is a stub.
- No visual regression. Nothing compares screenshots or rendered pixels.
- No cross-browser run. Nothing launches a second browser engine.
- The coverage target does not measure yet. `coverage` does not collect a figure, so this document states no coverage percentage.

`test-bdd` does not execute the subscribe, read-post, or search
scenarios. Those journeys are specified in `code-quality.md` and checked
by hand in `manual-tests.md`. Subscribe stays blocked until an email
service is approved.

## Code review checklist

Apply this list to a pull request before approving it. The reviewer is
the person named on the task. One review is required. Required checks
must be green. Publishing the site, production deploys, and DNS changes
stay behind Venkat's approval.

- [ ] Tests cover the change. A behavior change has a failing test first, then the smallest code that makes it pass. Docs-only diffs say which claims a person can check.
- [ ] `python -m unittest discover -s tests -v` passes, or `.\make.ps1 test` passes.
- [ ] The diff contains no secrets, credentials, tokens, private keys, or `.env` files.
- [ ] The diff does not deploy to production, change DNS, or publish the site. `release` does not deploy.
- [ ] Drafts are not published. A `draft: true` post stays out of the index, the post pages, the feed, the sitemap, and the search index. Legal pages still say Venkat has not approved them for publication.
