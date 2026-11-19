# Manual tests

Checklist for a person at the repository root on Windows. Check an item only after its expected result holds. Do not publish the site, spend money, or create accounts while running these steps.

Commands below use `.\make.ps1`. The stack is not chosen yet, so some targets only print a message and exit 0.

## Harness (local)

### `.\make.ps1 test` exits 0

- [ ] Steps:
  1. Open a shell at the repository root.
  2. Run `.\make.ps1 test`.
- Expected result: the process exits 0. The target runs `python -m unittest discover -s tests -v` when `tests/` exists.

### `.\make.ps1 build` exits 0

- [ ] Steps:
  1. From the repository root, run `.\make.ps1 build`.
  2. Leave `make.ps1` unchanged. On this branch `build` is still a no-op: it prints that a production build waits until the stack is chosen, and it does not compile Python.
  3. Compile the Python that exists today: `python -m compileall -q scripts tests`.
- Expected result: compileall exits 0.

### `python -m unittest discover -s tests -v` exits 0

- [ ] Steps:
  1. From the repository root, run `python -m unittest discover -s tests -v`.
- Expected result: the process exits 0 and every discovered test passes.

### `.\make.ps1 sync-agents` copies skills without a symlink

- [ ] Steps:
  1. From the repository root, run `.\make.ps1 sync-agents`.
  2. Open `.claude/skills` and confirm each skill directory was copied from `.agents/skills`.
  3. Confirm each copied skill is a real directory. It must not be a symlink or a directory junction.
- Expected result: the command exits 0, the skill files are copies, and no symlink was created.

## Developer docs

### `AGENTS.md`, `docs/developers.md`, and `docs/users.md`

- [ ] Steps:
  1. Open `AGENTS.md`, `docs/developers.md`, and `docs/users.md` from the repository root.
  2. Check claims you can verify on this machine: the folder map (`src`, `content`, `tests`, `docs`, `research`, `scripts`), `.\make.ps1` target names, and the statement that the stack is not chosen yet.
  3. Do not require a deployed blog. Publishing is an approval gate, and drafts stay in the repository.
- Expected result: the files open and match the claims you can check locally. The site is not live.

## End-user docs

### Reader-facing claims

- [ ] Steps:
  1. Open `docs/users.md`.
  2. Compare reader-facing claims with what exists locally: posts under `content/posts/`, and no running site.
  3. Do not try to subscribe, open a published page, or search a deployed blog.
- Expected result: `docs/users.md` opens and matches the claims you can check locally. The site is not live.

## Not available yet

### Four-tool smoke test is not run

- [ ] Steps:
  1. Read `docs/agents/capability-matrix.md`. The version table records Claude Code, Codex, Cursor, and Antigravity as not probed.
  2. Do not launch those tools for this checklist.
- Expected result: the four-tool smoke test (Claude Code, Codex, Cursor, Antigravity) is listed as not run.

### Site journeys are blocked

subscribe, read post, and search are blocked until the site exists.

- [ ] Subscribe. Steps: do not submit an email. There is no site to accept it. Expected result: subscribe is blocked until the site exists.
- [ ] Read post. Steps: do not open a published URL. `content/posts/` has no live page. Expected result: read post is blocked until the site exists.
- [ ] Search. Steps: do not query a site search box. Expected result: search is blocked until the site exists.
