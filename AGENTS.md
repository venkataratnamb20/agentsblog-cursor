# AGENTS.md

This file is the single source of truth for **Agents Blog**. Agent instruction
files, Cursor rules, and Claude project notes point here. They do not copy
these rules into a second place.

If a tool-specific file disagrees with this one, this file wins. Fix the
pointer. Do not fork the policy.

## Purpose

Agents Blog is a technical blog on AI agents. The readers are AI engineers,
researchers, and tech leads: people who design, build, evaluate, or lead work
on agent systems.

Posts should be accurate, specific, and useful in practice. Prefer one idea
treated carefully over a news roundup. Drafts stay in the repo until a person
publishes them. Publishing is an approval gate, not a git action.

## Stack

The stack is not chosen yet. Do not pick a framework, language runtime, host,
or package manager in code or in docs while this is still true.

Architecture decisions will be recorded as ADRs in stage 1, under `docs/adr/`.
Until an ADR is accepted, treat the stack as unknown. The command names below
are stable. Their implementations arrive with the stack.

## Folder map

| Path | Role |
| --- | --- |
| `src/` | Application source, once a stack exists |
| `content/` | Posts, drafts, and media |
| `tests/unit/` | Unit tests |
| `tests/integration/` | Integration tests |
| `tests/e2e/` | End-to-end tests |
| `tests/features/` | BDD feature files |
| `docs/` | Guidelines, governance, and ADRs |
| `research/` | Notes and source material that are not posts |
| `scripts/` | Repository automation |
| `.agents/` | Shared agent instructions |
| `.claude/` | Claude project configuration |
| `.codex/` | Codex project configuration |
| `.cursor/` | Cursor rules and project configuration |
| `.github/` | CI workflows and pull request templates |

Create a directory when the first real file needs it. Do not add empty
placeholder trees. Tool directories (`.agents`, `.claude`, `.codex`, `.cursor`)
hold pointers and tool config. Policy stays in this file.

## Commands

Use `make <target>` on Unix and macOS. Use `make.ps1 <target>` on Windows.
Both entry points expose the same target names. Prefer a target over a one-off
script when the target already names the job.

| Target | What it does |
| --- | --- |
| `setup` | Install local dependencies |
| `dev` | Run the local development server |
| `lint` | Lint the repository |
| `format` | Format the repository |
| `typecheck` | Run static type checks |
| `test` | Run unit and integration tests |
| `test-e2e` | Run end-to-end tests |
| `test-bdd` | Run BDD scenarios from `tests/features/` |
| `coverage` | Run tests and report coverage |
| `build` | Produce a production build |
| `preview` | Serve the production build locally |
| `audit` | Audit dependencies and common security issues |
| `sync-agents` | Check that agent instruction files still point at this document |
| `release` | Prepare a release artifact. This does not deploy |
| `clean` | Remove local build and cache output |

Until stage 1, a target may be a stub. Call the target name anyway so docs,
scripts, and automation stay aligned. `release` never deploys to production.

## Git flow

Long-lived branches:

- `main` is production history and is protected.
- `develop` is the integration branch for the next release.

Short-lived branches:

- `feature/*` is normal work, branched from `develop`.
- `release/*` is stabilization before production.
- `hotfix/*` is an urgent fix, branched from `main`.

Integration rules:

- Land changes only through a pull request. Do not commit directly to `main` or `develop`.
- One review is required. The reviewer is the person named on the task.
- Required checks must be green before merge.
- Do not force-push `main`, `develop`, or any other shared branch.
- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

## Coding standards

Make the smallest change that meets the task. Match the surrounding style.
Name identifiers for the domain. Keep each function focused on one job. When a
test runner exists, add or update a test for the behavior you change.

The full guide is [docs/guidelines/code-quality.md](docs/guidelines/code-quality.md).
Follow that guide for naming, structure, comments, and review expectations.
Do not copy the guide into this file or into tool rules.

## Definition of done

A task is done when:

- the acceptance criteria are met and the evidence is linked
- the named reviewer has reviewed the change
- tests pass for any code change
- docs affected by the change are updated
- the task progress record is updated

The checklist, task template, and hand-off format are in
[docs/governance/operating-model.md](docs/governance/operating-model.md).
Use that document. Do not keep a second definition of done elsewhere.

## Approval gates

Stop and get Venkat's explicit approval before any of these:

- spending money
- creating accounts
- production deploys
- DNS changes
- publishing posts
- posting on social networks or communities

How to ask, and the guardrails that always apply, are in
[docs/governance/approval-gates.md](docs/governance/approval-gates.md).

## Do not touch

Do not read, write, commit, or paste any of the following:

- secrets, credentials, tokens, and private keys
- `.env`, `.env.*`, and any other file that holds secrets
- plan files, including implementation plans and stage plans

Do not create secrets or `.env` files. If a task needs a secret, stop and ask
a person to provide it outside the repository. Record that an action happened.
Never record the secret itself.
