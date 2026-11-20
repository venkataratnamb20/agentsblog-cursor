# Capability matrix

Role-by-tool map for Agents Blog. It records where Claude Code, Codex, Cursor, and Antigravity load rules, skills, subagents, commands or workflows, MCP, and hooks, and whether each surface is **available**, **missing**, or **reuse**.

This document records the harness layout. It does not install tools or grant credentials.

## Status words

| Status | Meaning |
| --- | --- |
| available | The tool has its own documented place to read this capability. A role can depend on it. |
| reuse | The tool has no exclusive copy. It reads a directory that belongs to another tool or to the shared `.agents` tree. Author the artifact once in that shared place. |
| missing | No path was recorded for this capability. A role that needs it cannot rely on this tool until the skills and subagents task adds a path or an explicit reuse decision. |

A cell is **missing** when any capability that role needs is missing on that tool. A cell is **reuse** when every needed capability is available or reuse, and at least one is reuse. A cell is **available** when every needed capability is available on that tool.

## Tool versions

Probed in this worktree on 2026-11-20. Codex and Antigravity are **out of scope** for this build per `AGENTS.md`; their version cells are not filled here.

| Tool | Version | Probed in this worktree |
| --- | --- | --- |
| Claude Code | not probed — CLAUDE.md pointer verified | CLI binary not present. `CLAUDE.md` imports `AGENTS.md`. |
| Codex | out of scope (per AGENTS.md) | Not probed. Codex is out of scope for this build. |
| Cursor | 3.30.14 (5f54c8173e5552412beb40702adac16275677fa0, x64) | Yes. `cursor --version`. |
| Antigravity | out of scope (per AGENTS.md) | Not probed. Antigravity is out of scope for this build. |

## Where each tool reads config

Facts recorded for this matrix. Paths not in this list are not assumed.

| Capability | Claude Code | Codex | Cursor | Antigravity |
| --- | --- | --- | --- | --- |
| Rules | available: `CLAUDE.md` | available: `AGENTS.md` | available: `AGENTS.md` and `.cursor/rules` | available: `AGENTS.md` or `GEMINI.md`, plus `.agents/rules` |
| Skills | available: `.claude/skills` | available: `.agents/skills` | available: `.cursor/skills`. reuse: `.agents/skills` | available: `.agents/skills` |
| Subagents | available: `.claude/agents` (14 roles) | available: `.codex/agents/*.toml` (14 roles) | available: `.cursor/agents`. reuse: `.claude/agents` and `.codex/agents` | missing |
| Commands / workflows | available: `.claude/commands` | missing | missing | available: `.agents/workflows` |
| MCP | available: `.mcp.json` | available: MCP. The only Codex config file named here is `.codex/config.toml`; the MCP server file itself was not pinned | available: MCP. Config file path was not pinned | available: MCP. Config file path was not pinned |
| Hooks | available: `.claude/settings.json` | missing | available: hooks. Config file path was not pinned | missing |

Notes that follow from those facts:

- Codex, Cursor, and Antigravity can share one `AGENTS.md`. Antigravity may use `GEMINI.md` instead. Claude Code does not read `AGENTS.md`; its rules file is `CLAUDE.md`.
- `.agents/skills` is the native skills directory for Codex and Antigravity. Cursor can reuse that same directory or use `.cursor/skills`.
- Cursor is the only tool recorded as reading another tool's subagents (`.claude/agents` and `.codex/agents`) as well as its own (`.cursor/agents`).
- Codex project config lives in `.codex/config.toml`. Subagents there are TOML files under `.codex/agents/`.
- Claude Code is the only tool with a recorded path for every capability in this matrix, including hooks (`.claude/settings.json`) and MCP (`.mcp.json`).
- Fourteen subagents exist: 14 markdown files under `.claude/agents` and 14 TOML files under `.codex/agents`.

## What each role needs

A role needs a capability only when its job cannot be done without it. Tools the role does not need are out of scope for that row.

| Role | Rules | Skills | Subagents | Commands / workflows | MCP | Hooks |
| --- | --- | --- | --- | --- | --- | --- |
| PM Orchestrator | yes | yes | yes | yes (`gate-check`) | yes | no |
| Solution Architect | yes | yes | no | no | yes | no |
| Product Strategist | yes | yes | no | no | no | no |
| Technical Writer | yes | yes | no | yes (`new-post`) | no | no |
| Technical Editor | yes | yes | no | yes (`review-pr`) | no | no |
| Research Analyst | yes | yes | no | no | yes | no |
| UX/UI Designer | yes | yes | no | no | no | no |
| Frontend Engineer | yes | yes | no | no | yes | yes |
| QA Engineer | yes | yes | no | yes (`gate-check`) | no | yes |
| Code Reviewer | yes | yes | yes | yes (`review-pr`) | no | no |
| Security Engineer | yes | yes | no | yes (`security-check`) | no | yes |
| DevOps & SRE | yes | yes | no | yes (`release`, `hotfix`) | yes | yes |
| SEO & Analytics | yes | yes | no | yes (`seo-audit`) | yes | no |
| Growth & Community | yes | yes | no | no | no | no |

Shared skills named in that table are **present** (written under `.agents/skills` and synced to `.claude/skills`). See [Shared skills (present)](#shared-skills-present).

## Role x tool

| Role | Claude Code | Codex | Cursor | Antigravity |
| --- | --- | --- | --- | --- |
| PM Orchestrator | available | missing | missing | missing |
| Solution Architect | available | available | reuse | available |
| Product Strategist | available | available | reuse | available |
| Technical Writer | available | missing | missing | available |
| Technical Editor | available | missing | missing | available |
| Research Analyst | available | available | reuse | available |
| UX/UI Designer | available | available | reuse | available |
| Frontend Engineer | available | missing | reuse | missing |
| QA Engineer | available | missing | missing | missing |
| Code Reviewer | available | missing | missing | missing |
| Security Engineer | available | missing | missing | missing |
| DevOps & SRE | available | missing | missing | missing |
| SEO & Analytics | available | missing | missing | available |
| Growth & Community | available | available | reuse | available |

Why a cell is missing or reuse:

| Role | Codex | Cursor | Antigravity |
| --- | --- | --- | --- |
| PM Orchestrator | missing commands | missing commands | missing subagents |
| Solution Architect | available | reuse skills (`.agents/skills`) | available |
| Product Strategist | available | reuse skills (`.agents/skills`) | available |
| Technical Writer | missing commands | missing commands | available (`.agents/workflows`) |
| Technical Editor | missing commands | missing commands | available (`.agents/workflows`) |
| Research Analyst | available | reuse skills (`.agents/skills`) | available |
| UX/UI Designer | available | reuse skills (`.agents/skills`) | available |
| Frontend Engineer | missing hooks | reuse skills (`.agents/skills`); hooks path not pinned but hooks are recorded | missing hooks |
| QA Engineer | missing commands and hooks | missing commands | missing hooks |
| Code Reviewer | missing commands | missing commands. Subagents can reuse `.claude/agents` and `.codex/agents` | missing subagents |
| Security Engineer | missing commands and hooks | missing commands | missing hooks |
| DevOps & SRE | missing commands and hooks | missing commands | missing hooks |
| SEO & Analytics | missing commands | missing commands | available (`.agents/workflows`) |
| Growth & Community | available | reuse skills (`.agents/skills`) | available |

Cursor cells marked **reuse** assume the role's skills are authored in `.agents/skills` and Cursor is configured to read that tree. If a skill is authored only in `.cursor/skills`, that role's Cursor cell becomes **available** and Codex and Antigravity cannot see it. Prefer `.agents/skills` for skills more than one tool must run.

Claude Code stays **available** on every row because `CLAUDE.md`, `.claude/skills`, `.claude/agents`, `.claude/commands`, `.claude/settings.json`, and `.mcp.json` cover the full set. Skills that must also run in Codex or Antigravity live under `.agents/skills` (with a Claude copy under `.claude/skills`). Claude Code does not read `.agents/skills` directly.

## Shared skills (present)

The seven shared skills are **present** on disk under `.agents/skills/{name}/SKILL.md` and `.claude/skills/{name}/SKILL.md`. Expose them through each tool that has a commands or workflows surface. Command-dependent cells stay blocked on tools that still lack a commands or workflows directory.

| Skill | Purpose | Primary roles | Claude Code command | Antigravity workflow | Codex | Cursor |
| --- | --- | --- | --- | --- | --- | --- |
| `new-post` | Draft a post from a brief, sources, and the house style | Technical Writer, Technical Editor consulted | `.claude/commands` | `.agents/workflows` | missing | missing |
| `review-pr` | Review a diff for correctness, regressions, and editorial or code standards | Code Reviewer, Technical Editor | `.claude/commands` | `.agents/workflows` | missing | missing |
| `security-check` | Review a change for secrets, auth, and unsafe defaults | Security Engineer | `.claude/commands` | `.agents/workflows` | missing | missing |
| `seo-audit` | Check titles, headings, links, and indexability of a post or page | SEO & Analytics | `.claude/commands` | `.agents/workflows` | missing | missing |
| `gate-check` | Decide whether a change may proceed to the next stage | PM Orchestrator, QA Engineer | `.claude/commands` | `.agents/workflows` | missing | missing |
| `release` | Ship a change that has passed gate-check | DevOps & SRE | `.claude/commands` | `.agents/workflows` | missing | missing |
| `hotfix` | Ship a narrow production fix with the same checks, shortened path | DevOps & SRE, Frontend Engineer consulted, Security Engineer consulted | `.claude/commands` | `.agents/workflows` | missing | missing |

Skill bodies live in both `.claude/skills` (Claude Code) and `.agents/skills` (Codex, Antigravity, and Cursor reuse). Do not fork the procedure per tool. Commands and workflows should be thin entry points that call the shared skill.

## Gaps

Closed gaps are marked **done**. Remaining items are intentional open work (including Codex/Antigravity surfaces that stay out of scope for this build).

1. **done — Write the seven shared skills** (`new-post`, `review-pr`, `security-check`, `seo-audit`, `gate-check`, `release`, `hotfix`) in `.claude/skills` and `.agents/skills`. All seven `SKILL.md` files exist in both trees.
2. **Add command and workflow entry points** for those skills. Claude Code can use `.claude/commands`. Antigravity can use `.agents/workflows`. Codex has no commands directory on record. Cursor has no commands or workflows directory on record. The task must add those surfaces or record a reuse rule that points Codex and Cursor at an existing command tree.
3. **done (Claude Code + Codex) — Define subagents for the 14 roles.** Fourteen markdown agents exist under `.claude/agents`. Fourteen TOML agents exist under `.codex/agents`. Cursor can reuse those directories. **Open (intentional):** Antigravity has no subagent directory; out of scope for this build per `AGENTS.md` unless a later decision records reuse of `.claude/agents` or `.codex/agents`.
4. **Record hooks for Codex and Antigravity.** Both are missing. Roles that need hooks (Frontend Engineer, QA Engineer, Security Engineer, DevOps & SRE) cannot use those tools for hook-gated checks until a path exists. Pin the Cursor hooks file path in the same pass; this matrix only knows the capability name. Codex/Antigravity remain out of scope for this build.
5. **Pin MCP config paths** for Codex, Cursor, and Antigravity. Only Claude Code names a file (`.mcp.json`). Codex names `.codex/config.toml` as project config and "MCP" as a capability, without a server-file path.
6. **done — Fill tool versions.** Cursor probed (`3.30.14`). Claude Code CLI absent; `CLAUDE.md` pointer verified. Codex and Antigravity recorded as out of scope per `AGENTS.md`.
7. **Keep rules aligned across files.** Claude Code reads `CLAUDE.md` only. Codex and Cursor read `AGENTS.md`. Antigravity reads `AGENTS.md` or `GEMINI.md`, plus `.agents/rules`. A rule that applies to every tool has to be written in each file that tool actually reads, or a smoke test must prove one file is included by the others.

## Out of scope for this record

- Installing CLIs or MCP servers.
- Choosing model names or temperature settings.
- Granting credentials. No role and no tool entry in this matrix receives a secret.
- Codex and Antigravity runtime setup for this build (per `AGENTS.md`).
