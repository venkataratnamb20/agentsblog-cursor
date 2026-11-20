# ADR 0002: Python standard library site

## Status

Accepted

This decision covers the **local site builder only**. It does not choose a
host, a package manager, or a newsletter service.

## Date

2026-11-19

## Context

This slice needs a local site builder the task runner can call without choosing
hosting or a package manager. The builder file is `src/agentsblog/build.py`.
Until that file exists, `build` still compiles the Python that is already in
the repository.

A Node framework would bring a JavaScript runtime and a package manager. A
hosted CMS would choose a host and an account. A newsletter vendor would choose
an email service and an account. None of those belong in this local slice.
Creating accounts and picking a paid host are approval gates for Venkat.

## Decision

The local site builder is the Python standard library. No package is installed
to build the local site.

`build` always runs `compileall` on `scripts` and `tests`. Only when
`src/agentsblog/build.py` exists does it then run the builder:

- Windows: `python -m agentsblog.build`
- macOS and Linux: `python3 -m agentsblog.build`

When the builder file is absent, `build` skips that step and exits with the
`compileall` status.

Cursor setup is in `.cursor` and follows `AGENTS.md`. Claude loads `AGENTS.md`
through `CLAUDE.md`. Codex and Antigravity are out of scope for this build.

### Remains undecided

These stay open until Venkat approves a later decision. This ADR does not
pick them:

| Topic | Why it stays open |
| --- | --- |
| Hosting (staging / production) | Needs an approved host and account; not a local-builder concern |
| Package manager | Local build uses the Python standard library only |
| Newsletter service | Needs an approved vendor and account; double opt-in is a later slice |

## Consequences

- `.\make.ps1 build` and `make build` compile `scripts` and `tests` even when
  the site module is missing.
- A syntax error in `scripts` or `tests` still fails the build.
- Adding `src/agentsblog/build.py` turns the same target into a site build
  without a new task name.
- Hosting, DNS, package managers, and newsletter remain open decisions. Leaving
  them undecided is an intentional consequence of this ADR, not unfinished work
  on the local builder.
- Production deploys, DNS changes, and newsletter accounts still require
  Venkat's explicit approval per `docs/governance/approval-gates.md`.

## Rejected alternatives

This local slice rejects a Node framework and a hosted CMS.

**Node framework.** A Node framework would decide a JavaScript runtime and a
package manager before this slice has a site module. Rejected for this local
slice.

**Hosted CMS.** A hosted CMS would decide hosting and an account before the
local builder exists. Rejected for this local slice.
