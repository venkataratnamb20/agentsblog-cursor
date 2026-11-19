# TDD evidence: local site

## Journeys

- A reader sees published titles on the index. Draft titles are absent.
- A reader opens a published post and sees the body.
- The search index lists published titles only.
- A missing page says "Page not found".
- `dev` and `preview` serve the `build/` directory on 127.0.0.1.

Subscribe stays blocked. There is no newsletter form.

## Checkpoints

| Stage | Commit | Evidence |
| --- | --- | --- |
| RED builder | `43a947e` | `ModuleNotFoundError: No module named 'agentsblog.build'` |
| GREEN builder | `61ef1f1` | `tests.integration.test_site_build` passed |
| RED preview | `10144e6` | `ModuleNotFoundError: No module named 'agentsblog.preview'` |
| GREEN preview | `67d18de` | `tests.unit.test_preview` — 12 tests OK |
| Merged | `362f272` | `python -m unittest discover -s tests -v` — 61 tests OK |

`python -m agentsblog.build` wrote `build/index.html`, `build/404.html`, `build/search-index.json`, and `build/assets/site.css`. `content/posts` has no posts, so the index list is empty.

## Gaps

- `coverage` was not run. `coverage.py` is not installed, and this slice does not add a dependency.
- Playwright was not used. There is no browser runner in the repository.
- The four-tool smoke test was not run. This build uses Cursor and the Claude pointer in `CLAUDE.md`.
