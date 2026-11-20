# Harness smoke test

Stage 0A end-to-end smoke of the Agents Blog agent harness. No accounts,
deploys, publishes, or spend. Evidence recorded from this worktree on
2026-11-20.

## Result

| Tool | Scope | Verdict |
| --- | --- | --- |
| Cursor | In scope | PASS |
| Claude | In scope | PASS |
| Codex | Out of scope | OUT OF SCOPE |
| Antigravity | Out of scope | OUT OF SCOPE |

Smoke result: **PASS** for in-scope tools (Cursor and Claude).

## Cursor

Checks run in this repository (Cursor session on the Agents Blog worktree).

| Check | Evidence |
| --- | --- |
| `AGENTS.md` present | `Test-Path AGENTS.md` → `True` |
| Unit test runner can run | `python -m unittest discover -s tests -q` executed (137 tests discovered and ran; two unrelated failures in `test_capability_matrix`, outside this smoke task) |
| Seven skills under `.agents/skills` | Directories: `gate-check`, `hotfix`, `new-post`, `release`, `review-pr`, `security-check`, `seo-audit` |
| 14 role files under `.claude/agents` | Count: 14 — `code-reviewer.md`, `devops-sre.md`, `frontend-engineer.md`, `growth-community.md`, `pm-orchestrator.md`, `product-strategist.md`, `qa-engineer.md`, `research-analyst.md`, `security-engineer.md`, `seo-analytics.md`, `solution-architect.md`, `technical-editor.md`, `technical-writer.md`, `ux-ui-designer.md` |

Cursor verdict: PASS.

## Claude

Claude loads the project contract through `CLAUDE.md`.

| Check | Evidence |
| --- | --- |
| `CLAUDE.md` points at `AGENTS.md` | First line is `@AGENTS.md` (Claude import of the project contract) |
| Seven skills under `.claude/skills` | Directories: `gate-check`, `hotfix`, `new-post`, `release`, `review-pr`, `security-check`, `seo-audit` |

Claude verdict: PASS.

## Codex and Antigravity

**OUT OF SCOPE** for this build.

Citation — `AGENTS.md` Stack section:

> Codex and Antigravity are out of scope for this build.

Recording OUT OF SCOPE here is not a fail. No Codex or Antigravity smoke
was required.

## Commands used (brief)

```text
Test-Path AGENTS.md
# True

Get-Content CLAUDE.md -TotalCount 1
# @AGENTS.md

(Get-ChildItem .agents\skills -Directory).Name
# gate-check, hotfix, new-post, release, review-pr, security-check, seo-audit

(Get-ChildItem .claude\skills -Directory).Name
# gate-check, hotfix, new-post, release, review-pr, security-check, seo-audit

(Get-ChildItem .claude\agents -File -Filter *.md).Count
# 14

python -m unittest discover -s tests -q
# Ran 137 tests in ~29s (suite had 2 pre-existing capability-matrix failures)
```
