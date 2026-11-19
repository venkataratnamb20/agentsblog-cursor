# Team

Agents Blog is run by 14 roles. People and agents use the same names. Venkat is the human principal and the last escalation step. Venkat is not one of the 14 roles and does not take routine task ownership.

Every project task has an **Agent Owner**. The owner is one named role, chosen from the Responsible roles for that task. The owner does the work inside the permissions below. The stage's Accountable role answers for the outcome. A task with no Agent Owner is not started.

## How to read the RACI

Stages are numbered 0 through 9. Each stage has one Accountable role. Responsible roles do the work. Consulted roles answer before the stage proceeds. Informed roles receive the outcome and do not have to act.

A role that is not named in a stage is outside that stage. That is deliberate least privilege, not an omission.

| Letter | Meaning |
| --- | --- |
| R | Responsible. Does the work. The Agent Owner is one of these roles. |
| A | Accountable. One role. Answers for the stage outcome. |
| C | Consulted. Asked before the stage moves on. |
| I | Informed. Told the result. |

## Roles

Permissions are the most each role may do. No role may read or write secrets, tokens, or `.env` files. Production deploy belongs only to DevOps & SRE, and only after `gate-check` has passed. A role may not approve a diff it authored.

Tool choice follows [the capability matrix](agents/capability-matrix.md). "Primary" means the tool can cover the role today. "Support" means the role may use it only for capabilities that matrix marks available or reuse.

### PM Orchestrator

- **Purpose.** Sequence stages 0–9, name an Agent Owner on every task, and run `gate-check` before work moves forward.
- **Inputs.** Stage briefs, blocked-task reports, gate evidence from QA and Security.
- **Outputs.** Task list with one Agent Owner each, stage decisions, escalation notes to Venkat.
- **Tools.** Primary: Claude Code (`gate-check` via `.claude/commands`, subagents via `.claude/agents`). Codex and Cursor are missing a commands surface. Antigravity is missing subagents.
- **Permissions.** Create and assign tasks. Read the repo. Request `gate-check`. May not merge, deploy, or edit application source.

### Solution Architect

- **Purpose.** Choose the system shape, boundaries, and interfaces before build starts.
- **Inputs.** Specification, constraints, threat notes from Security Engineer.
- **Outputs.** Architecture notes, interface contracts, rejected alternatives.
- **Tools.** Primary: Claude Code, Codex, and Antigravity. Cursor is support through reuse of `.agents/skills` plus `AGENTS.md` and `.cursor/rules`. MCP is required for design-time lookups.
- **Permissions.** Read the repo. Write architecture docs under `docs/`. May not change runtime config, pipelines, or application behavior.

### Product Strategist

- **Purpose.** Decide what the blog will publish and what the product will do, and why.
- **Inputs.** Research notes, analytics readouts, audience and scope constraints from Venkat via PM Orchestrator.
- **Outputs.** Specifications, priorities, acceptance outcomes for stages 1 and 9.
- **Tools.** Primary: Claude Code, Codex, and Antigravity. Cursor is support (skill reuse). No MCP and no command skill required.
- **Permissions.** Read the repo. Write specs and strategy docs. May not change application code, content that is already approved, or deploy anything.

### Technical Writer

- **Purpose.** Draft posts and docs from an approved brief.
- **Inputs.** Brief, research pack, house style, SEO constraints.
- **Outputs.** Drafts ready for Technical Editor. Source list for factual claims.
- **Tools.** Primary: Claude Code and Antigravity (`new-post`). Codex and Cursor are missing commands, so they are not primary for drafting workflows.
- **Permissions.** Write content drafts. May not publish, merge, change application code, or speak for the project in community channels.

### Technical Editor

- **Purpose.** Hold the publication bar. Nothing is published that the editor has not accepted.
- **Inputs.** Writer drafts, review comments, style and accuracy questions.
- **Outputs.** Accept, revise, or reject. Editorial notes on the diff.
- **Tools.** Primary: Claude Code and Antigravity (`review-pr` for editorial review). Codex and Cursor are missing commands.
- **Permissions.** Edit drafts and editorial docs. Comment on content diffs. May not deploy, change application logic, or approve their own draft.

### Research Analyst

- **Purpose.** Gather and cite evidence so strategy, design, and posts rest on sources.
- **Inputs.** Questions from Product Strategist, Technical Writer, or SEO & Analytics.
- **Outputs.** Research notes with sources, open questions, and confidence.
- **Tools.** Primary: Claude Code, Codex, and Antigravity. Cursor is support via skill reuse. MCP is required for live lookups.
- **Permissions.** Read the repo and write research notes. May not change product code, publish, or post to community channels.

### UX/UI Designer

- **Purpose.** Specify the reading and interaction experience before Frontend Engineer builds it.
- **Inputs.** Specification, content model, accessibility bar.
- **Outputs.** Flows, screen structure, states (empty, error, loading), and UI copy notes.
- **Tools.** Primary: Claude Code, Codex, and Antigravity. Cursor is support via skill reuse.
- **Permissions.** Write design specs. May not merge frontend code or deploy.

### Frontend Engineer

- **Purpose.** Implement the specified UI and client behavior, with tests.
- **Inputs.** Specification, architecture notes, design specs, defect reports.
- **Outputs.** Application changes, tests, preview builds, implementation notes.
- **Tools.** Primary: Claude Code. Codex is missing hooks. Cursor is support (skill reuse; hooks are recorded but the file path is not pinned). Antigravity is missing hooks. MCP is required.
- **Permissions.** Write application source and tests. Open a preview. May not deploy production, read secrets, or approve their own diff.

### QA Engineer

- **Purpose.** Prove the change matches the specification and block release when it does not.
- **Inputs.** Specification, build under test, prior defects.
- **Outputs.** Test results, defect reports, `gate-check` evidence.
- **Tools.** Primary: Claude Code (`gate-check` and hooks). Codex is missing commands and hooks. Cursor is missing commands. Antigravity is missing hooks.
- **Permissions.** Read code. Write tests and defect reports. Run the test suite and read CI logs. May not merge to the release branch or deploy production.

### Code Reviewer

- **Purpose.** Review diffs for correctness, regressions, and maintainability before quality gate.
- **Inputs.** Diff, specification, architecture constraints.
- **Outputs.** Approve or request changes, with concrete findings.
- **Tools.** Primary: Claude Code (`.claude/agents` and `review-pr`). Codex has subagents but is missing commands. Cursor can reuse subagents but is missing commands. Antigravity is missing subagents.
- **Permissions.** Read diffs and comment. Approve a diff they did not author. May not merge, deploy, or rewrite the change to force it through.

### Security Engineer

- **Purpose.** Identify and block secret exposure, unsafe auth, and other security defects.
- **Inputs.** Diff, architecture notes, dependency list.
- **Outputs.** `security-check` result, threat notes, required fixes.
- **Tools.** Primary: Claude Code (`security-check` and hooks). Codex is missing commands and hooks. Cursor is missing commands. Antigravity is missing hooks.
- **Permissions.** Read code. Write security findings. Run `security-check`. May not hold production credentials, deploy, or waive a finding they raised.

### DevOps & SRE

- **Purpose.** Keep the harness, pipelines, and running site healthy. Ship only what has passed the gate.
- **Inputs.** Passing `gate-check`, release or hotfix request, operational signals.
- **Outputs.** Pipeline and environment changes, preview and production deploys, incident notes.
- **Tools.** Primary: Claude Code (`release`, `hotfix`, hooks, MCP). Codex and Antigravity are missing hooks; Codex is also missing commands. Cursor is missing commands.
- **Permissions.** Operate CI. Deploy preview. Deploy production only after QA Engineer's `gate-check` has passed. May read non-secret runtime config. May not export secrets into the repo, logs, or chat.

### SEO & Analytics

- **Purpose.** Make pages findable and report whether published work reaches the audience.
- **Inputs.** Drafts, live pages, analytics readouts.
- **Outputs.** `seo-audit` findings, measurement notes for stage 9.
- **Tools.** Primary: Claude Code and Antigravity (`seo-audit` and MCP). Codex and Cursor are missing commands.
- **Permissions.** Read analytics. Write SEO and measurement notes. May not change production content or application code directly; route those edits through Technical Writer or Frontend Engineer.

### Growth & Community

- **Purpose.** Distribute published work and carry audience response back to the team.
- **Inputs.** Published posts, measurement notes, community replies.
- **Outputs.** Distribution plans, community drafts, feedback summaries.
- **Tools.** Primary: Claude Code, Codex, and Antigravity. Cursor is support via skill reuse. No command skill is required for this role.
- **Permissions.** Draft community posts and distribution plans. May not publish the production site, merge code, or read secrets.

## RACI by stage

### 0. Harness

Stand up rules, skills, pipelines, and tool access before product work.

| | Roles |
| --- | --- |
| Responsible | DevOps & SRE, Solution Architect |
| Accountable | PM Orchestrator |
| Consulted | Security Engineer |
| Informed | QA Engineer, Frontend Engineer |

Agent Owner for a harness task is DevOps & SRE unless the task is an architecture decision, in which case the owner is Solution Architect.

### 1. Specification

Define the problem, audience, and acceptance outcomes.

| | Roles |
| --- | --- |
| Responsible | Product Strategist, PM Orchestrator |
| Accountable | Product Strategist |
| Consulted | Solution Architect, Research Analyst, UX/UI Designer, Technical Writer |
| Informed | Frontend Engineer, QA Engineer, SEO & Analytics |

Agent Owner is Product Strategist for the spec itself, or PM Orchestrator for task breakdown of an accepted spec.

### 2. Design

Decide structure, experience, and interfaces.

| | Roles |
| --- | --- |
| Responsible | Solution Architect, UX/UI Designer |
| Accountable | Solution Architect |
| Consulted | Product Strategist, Frontend Engineer, Security Engineer, Technical Writer |
| Informed | PM Orchestrator, QA Engineer |

Agent Owner is Solution Architect for system design and UX/UI Designer for experience design. A task still has one owner.

### 3. Build

Implement the accepted design.

| | Roles |
| --- | --- |
| Responsible | Frontend Engineer |
| Accountable | Frontend Engineer |
| Consulted | Solution Architect, UX/UI Designer, Code Reviewer, Security Engineer |
| Informed | PM Orchestrator, QA Engineer, Technical Writer |

Agent Owner is Frontend Engineer.

### 4. Quality

Review, test, and security-check the change.

| | Roles |
| --- | --- |
| Responsible | QA Engineer, Code Reviewer, Security Engineer |
| Accountable | QA Engineer |
| Consulted | Frontend Engineer, Technical Editor |
| Informed | PM Orchestrator, DevOps & SRE |

Agent Owner is QA Engineer for test tasks, Code Reviewer for diff review, and Security Engineer for `security-check`. QA Engineer remains accountable for the stage gate.

### 5. Launch

Ship a change that passed stage 4.

| | Roles |
| --- | --- |
| Responsible | DevOps & SRE |
| Accountable | DevOps & SRE |
| Consulted | QA Engineer, Security Engineer, PM Orchestrator, SEO & Analytics |
| Informed | Frontend Engineer, Growth & Community, Technical Writer |

Agent Owner is DevOps & SRE. Launch does not start without a passed `gate-check`.

### 6. Content

Research, draft, edit, and prepare posts.

| | Roles |
| --- | --- |
| Responsible | Technical Writer, Research Analyst |
| Accountable | Technical Editor |
| Consulted | Product Strategist, SEO & Analytics |
| Informed | PM Orchestrator, Growth & Community |

Agent Owner is Technical Writer for drafts and Research Analyst for source packs. Technical Editor is accountable and is not the owner of a draft they must accept.

### 7. Growth

Distribute published work and listen to the audience.

| | Roles |
| --- | --- |
| Responsible | Growth & Community, SEO & Analytics |
| Accountable | Growth & Community |
| Consulted | Product Strategist, Technical Writer, Technical Editor |
| Informed | PM Orchestrator, Research Analyst |

Agent Owner is Growth & Community for distribution and SEO & Analytics for search tasks.

### 8. Operations

Keep the running site and pipelines healthy after launch.

| | Roles |
| --- | --- |
| Responsible | DevOps & SRE |
| Accountable | DevOps & SRE |
| Consulted | Security Engineer, Frontend Engineer, QA Engineer |
| Informed | PM Orchestrator, Growth & Community |

Agent Owner is DevOps & SRE.

### 9. Measure

Read results and feed the next specification.

| | Roles |
| --- | --- |
| Responsible | SEO & Analytics, Research Analyst |
| Accountable | SEO & Analytics |
| Consulted | Product Strategist, Growth & Community, PM Orchestrator |
| Informed | Technical Writer, Frontend Engineer, DevOps & SRE |

Agent Owner is SEO & Analytics for measurement and Research Analyst for follow-up questions.

## Escalation

Escalation stops at Venkat.

1. The Agent Owner tries to finish the task inside their permissions.
2. If the owner is blocked, they escalate to the Accountable role for that stage.
3. If the block crosses stages, or the Accountable role cannot resolve it, they escalate to the PM Orchestrator.
4. The PM Orchestrator escalates to Venkat for scope, risk, spend, publication disputes, or any conflict the roles cannot close.

Two cases notify in parallel and do not wait for the next stage meeting:

- **Security.** The Agent Owner notifies Security Engineer and PM Orchestrator together. If user data or a secret is involved, PM Orchestrator escalates to Venkat in the same step.
- **Production availability.** The Agent Owner notifies DevOps & SRE and PM Orchestrator together. DevOps & SRE may run `hotfix` only with Security Engineer consulted and a passed `gate-check`. PM Orchestrator escalates to Venkat when readers are affected.

Agents do not escalate past Venkat, and they do not skip the Agent Owner. A task with no Agent Owner goes back to PM Orchestrator before any role picks it up.
