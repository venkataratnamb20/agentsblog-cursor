# Audit AI Team Harness Capabilities Claude Code Codex Cursor Antigravity

## Status

Status: Done

## Evidence

- `docs/agents/capability-matrix.md` refreshed: seven shared skills present under `.agents/skills` and `.claude/skills`; 14 subagents under `.claude/agents` and `.codex/agents`.
- Tool versions: Cursor `3.30.14` probed; Claude Code CLI absent — `CLAUDE.md` pointer verified; Codex and Antigravity out of scope per `AGENTS.md`.
- Gaps 1, 3 (Claude+Codex), and 6 marked done; remaining gaps left intentional (commands/workflows, Antigravity subagents, hooks, MCP path pins, rules alignment).
- `tests/unit/test_capability_matrix.py` asserts skills present, 14 roles, and version/out-of-scope probe notes — GREEN (`python -m unittest tests.unit.test_capability_matrix -v`).

## Remaining

- None for this audit. Open matrix gaps stay intentional follow-ups (not blockers for closing this task).
