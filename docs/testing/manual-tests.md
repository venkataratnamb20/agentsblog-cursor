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
  2. Open `build/index.html`, `build/search.html`, `build/feed.xml`, and `build/privacy.html`.
- Expected result: the command exits 0. It compiles `scripts` and `tests`, then writes the local site. `privacy.html` says Venkat has not approved it for publication.

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

### Site journeys on the local preview

read post and search work on the local preview. subscribe is blocked until an email service is approved.

- [ ] Subscribe. Steps: do not submit an email. There is no email service. Expected result: subscribe is blocked until an email service is approved.
- [ ] Read post. Steps: add a published markdown file under `content/posts/`, run `.\make.ps1 build`, and open `build/posts/<slug>.html`. Expected result: the title and body are shown. Do not publish the post.
- [ ] Search. Steps: run `.\make.ps1 preview` and open `http://127.0.0.1:8000/search.html`. Type a word from a published title. Expected result: that post is listed. A blank query lists nothing.
