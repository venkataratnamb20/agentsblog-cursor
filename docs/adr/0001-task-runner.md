# ADR 0001: Task runner

## Status

Accepted

## Date

2026-11-19

## Context

Agents Blog needs one set of task names for setup, local development, checks, tests, and release. The application stack is not chosen yet, and contributors work on macOS, Linux, and Windows.

Windows needs a native PowerShell entrypoint that runs without WSL. A fresh clone should be able to run those tasks with the shell the OS already provides. An extra task-runner install, or a symlink that pretends one file serves every shell, would stop that clone from working.

## Decision

Ship two thin entrypoints that share the same target names:

- macOS and Linux run `make <target>` through `Makefile`.
- Windows runs `.\make.ps1 <target>` through native PowerShell.

Nothing else is installed to run a target. The two files are real, separate scripts. They are not joined by a symlink.

Shared targets:

`setup`, `dev`, `lint`, `format`, `typecheck`, `test`, `test-e2e`, `test-bdd`, `coverage`, `build`, `preview`, `audit`, `sync-agents`, `release`, `clean`.

Until the stack lands, a target that needs a toolchain prints what it will do later and exits 0. `lint`, `typecheck`, and `coverage` follow that rule and say so in their message.

`test` runs the standard-library discovery command when a `tests` directory exists, and exits 0 when it does not:

- Windows: `python -m unittest discover -s tests -v`
- macOS and Linux: `python3 -m unittest discover -s tests -v`

`sync-agents` runs `scripts/sync-agents.ps1` when that file exists. When the file is absent, the target prints a message and exits 0.

An unknown `make.ps1` target prints usage and exits 1. `make` reports an unknown target on its own.

## Consequences

- A clone can run tasks with `make` or Windows PowerShell. There is no runner package to install first.
- `Makefile` and `make.ps1` stay aligned whenever a target is added or its behavior changes.
- Placeholder targets stay visible in the output, and they still exit 0 so local scripts and CI can call them before the stack exists.
- Contributors on Windows do not need WSL to reach the same target names.

## Rejected alternative

**just** and **Task** (go-task) are the rejected alternative.

Both are third-party task runners. Choosing either one would mean every contributor installs an extra binary before `setup`, `test`, or `lint` can run. A single justfile or Taskfile also has no native PowerShell entrypoint. Serving that file to Windows through a symlink is unreliable unless the machine has symlink privileges enabled. `Makefile` plus `make.ps1` keeps one entrypoint per OS, with no extra install and no symlinks.
