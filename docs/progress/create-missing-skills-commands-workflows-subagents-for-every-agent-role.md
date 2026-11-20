# Create Missing Skills Commands Workflows Subagents For Every Agent Role

## Status

Status: Done

## Evidence

- `.agents/skills` holds the seven shared skills: `new-post`, `review-pr`, `security-check`, `seo-audit`, `gate-check`, `release`, `hotfix`.
- `.claude/commands` holds thin slash-command entry points for those seven skills.
- `.agents/workflows` holds thin Antigravity workflow wrappers for the same seven.
- `.claude/agents` holds fourteen role agent files.
- `tests/unit/test_harness_skills.py` asserts the seven skills, seven commands, and fourteen agents.
- `.\make.ps1 sync-agents` copies `.agents/skills` into `.claude/skills`.

## Remaining

none
