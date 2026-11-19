# Capability matrix

Role-by-tool map for Agents Blog. It records where Claude Code, Codex, Cursor, and Antigravity load rules, skills, subagents, commands or workflows, MCP, and hooks, and whether each surface is **available**, **missing**, or **reuse**.

This document is a planning record. It does not install tools, author skills, or change agent config.

## Status words

| Status | Meaning |
| --- | --- |
| available | The tool has its own documented place to read this capability. A role can depend on it. |
| reuse | The tool has no exclusive copy. It reads a directory that belongs to another tool or to the shared `.agents` tree. Author the artifact once in that shared place. |
| missing | No path was recorded for this capability. A role that needs it cannot rely on this tool until the skills and subagents task adds a path or an explicit reuse decision. |

A cell is **missing** when any capability that role needs is missing on that tool. A cell is **reuse** when every needed capability is available or reuse, and at least one is reuse. A cell is **available** when every needed capability is available on that tool.

## Tool versions

Tool versions were **not probed** in this worktree. Do not treat the paths below as proof that a binary is installed or that a given version honors them. A later smoke test must fill the version column on the same machine that will run the agents.

| Tool | Version | Probed in this worktree |
| --- | --- | --- |
| Claude Code | not probed | No. Fill in the later smoke test. |
| Codex | not probed | No. Fill in the later smoke test. |
| Cursor | not probed | No. Fill in the later smoke test. |
| Antigravity | not probed | No. Fill in the later smoke test. |

## Where each tool reads config

Facts recorded for this matrix. Paths not in this list are not assumed.

| Capability | Claude Code | Codex | Cursor | Antigravity |
| --- | --- | --- | --- | --- |
| Rules | available: `CLAUDE.md` | available: `AGENTS.md` | available: `AGENTS.md` and `.cursor/rules` | available: `AGENTS.md` or `GEMINI.md`, plus `.agents/rules` |
| Skills | available: `.claude/skills` | available: `.agents/skills` | available: `.cursor/skills`. reuse: `.agents/skills` | available: `.agents/skills` |
| Subagents | available: `.claude/agents` | available: `.codex/agents/*.toml` | available: `.cursor/agents`. reuse: `.claude/agents` and `.codex/agents` | missing |
| Commands / workflows | available: `.claude/commands` | missing | missing | available: `.agents/workflows` |
| MCP | available: `.mcp.json` | available: MCP. The only Codex config file named here is `.codex/config.toml`; the MCP server file itself was not pinned | available: MCP. Config file path was not pinned | available: MCP. Config file path was not pinned |
| Hooks | available: `.claude/settings.json` | missing | available: hooks. Config file path was not pinned | missing |

Notes that follow from those facts:

- Codex, Cursor, and Antigravity can share one `AGENTS.md`. Antigravity may use `GEMINI.md` instead. Claude Code does not read `AGENTS.md`; its rules file is `CLAUDE.md`.
- `.agents/skills` is the native skills directory for Codex and Antigravity. Cursor can reuse that same directory or use `.cursor/skills`.
- Cursor is the only tool recorded as reading another tool's subagents (`.claude/agents` and `.codex/agents`) as well as its own (`.cursor/agents`).
- Codex project config lives in `.codex/config.toml`. Subagents there are TOML files under `.codex/agents/`.
- Claude Code is the only tool with a recorded path for every capability in this matrix, including hooks (`.claude/settings.json`) and MCP (`.mcp.json`).

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

Shared skills named in that table are planned, not written. See [Shared skills to plan](#shared-skills-to-plan).

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

Claude Code stays **available** on every row because `CLAUDE.md`, `.claude/skills`, `.claude/agents`, `.claude/commands`, `.claude/settings.json`, and `.mcp.json` cover the full set. Skills that must also run in Codex or Antigravity still need a copy or a deliberate reuse link under `.agents/skills`. Claude Code does not read `.agents/skills`.

## Shared skills to plan

Author these seven skills once, then expose them through each tool that has a commands or workflows surface. Until they exist, every command-dependent cell above stays blocked even on a tool whose directory layout is available.

| Skill | Purpose | Primary roles | Claude Code command | Antigravity workflow | Codex | Cursor |
| --- | --- | --- | --- | --- | --- | --- |
| `new-post` | Draft a post from a brief, sources, and the house style | Technical Writer, Technical Editor consulted | `.claude/commands` | `.agents/workflows` | missing | missing |
| `review-pr` | Review a diff for correctness, regressions, and editorial or code standards | Code Reviewer, Technical Editor | `.claude/commands` | `.agents/workflows` | missing | missing |
| `security-check` | Review a change for secrets, auth, and unsafe defaults | Security Engineer | `.claude/commands` | `.agents/workflows` | missing | missing |
| `seo-audit` | Check titles, headings, links, and indexability of a post or page | SEO & Analytics | `.claude/commands` | `.agents/workflows` | missing | missing |
| `gate-check` | Decide whether a change may proceed to the next stage | PM Orchestrator, QA Engineer | `.claude/commands` | `.agents/workflows` | missing | missing |
| `release` | Ship a change that has passed gate-check | DevOps & SRE | `.claude/commands` | `.agents/workflows` | missing | missing |
| `hotfix` | Ship a narrow production fix with the same checks, shortened path | DevOps & SRE, Frontend Engineer consulted, Security Engineer consulted | `.claude/commands` | `.agents/workflows` | missing | missing |

Skill bodies should live in both `.claude/skills` (Claude Code) and `.agents/skills` (Codex, Antigravity, and Cursor reuse). Do not fork the procedure per tool. Commands and workflows should be thin entry points that call the shared skill.

## Gaps the skills and subagents task must close

1. **Write the seven shared skills** (`new-post`, `review-pr`, `security-check`, `seo-audit`, `gate-check`, `release`, `hotfix`) in `.claude/skills` and `.agents/skills`. None of them exist in this worktree.
2. **Add command and workflow entry points** for those skills. Claude Code can use `.claude/commands`. Antigravity can use `.agents/workflows`. Codex has no commands directory on record. Cursor has no commands or workflows directory on record. The task must add those surfaces or record a reuse rule that points Codex and Cursor at an existing command tree.
3. **Define subagents for the 14 roles.** Claude Code reads `.claude/agents`. Codex reads `.codex/agents/*.toml`. Cursor reads `.cursor/agents` and can reuse the Claude Code and Codex agent directories. Antigravity has no subagent directory. The task must add an Antigravity subagent location or an explicit decision that Antigravity reuses `.claude/agents` or `.codex/agents`.
4. **Record hooks for Codex and Antigravity.** Both are missing. Roles that need hooks (Frontend Engineer, QA Engineer, Security Engineer, DevOps & SRE) cannot use those tools for hook-gated checks until a path exists. Pin the Cursor hooks file path in the same pass; this matrix only knows the capability name.
5. **Pin MCP config paths** for Codex, Cursor, and Antigravity. Only Claude Code names a file (`.mcp.json`). Codex names `.codex/config.toml` as project config and "MCP" as a capability, without a server-file path.
6. **Fill tool versions** with a smoke test. This worktree did not probe Claude Code, Codex, Cursor, or Antigravity. The version table above must be updated from that run before anyone treats a path as live.
7. **Keep rules aligned across files.** Claude Code reads `CLAUDE.md` only. Codex and Cursor read `AGENTS.md`. Antigravity reads `AGENTS.md` or `GEMINI.md`, plus `.agents/rules`. A rule that applies to every tool has to be written in each file that tool actually reads, or the smoke test must prove one file is included by the others.

## Out of scope for this record

- Installing CLIs or MCP servers.
- Choosing model names or temperature settings.
- Granting credentials. No role and no tool entry in this matrix receives a secret.
