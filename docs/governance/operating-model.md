# Operating model

How a task is written down, handed off, and closed. `AGENTS.md` points here
for the definition of done. This file is the checklist. It does not replace
`AGENTS.md` for product scope, commands, or git rules.

## Task template

Copy this into the task before work starts. Fill every section. If a section
does not apply, write "none" and say why.

### Context

Why the task exists, who it is for, and what is out of scope.

### Inputs

Links to the files, decisions, issues, and research the work depends on.
Do not paste secrets.

### Steps

Ordered steps. Each step has one outcome. Call `make` or `make.ps1` targets
by the names in `AGENTS.md` instead of inventing a new entry point.

### Outputs

The artifacts this task will leave behind: files, a branch, a pull request,
or a note. Name the paths.

### Acceptance criteria

Checks a reviewer can observe. Each criterion can be shown with evidence
(a command result, a diff, a preview, or a link).

## Hand-off protocol

When you stop, including at the end of a session, leave all three:

1. **Artifact link.** Path, commit, or pull request. A hand-off without a link
   is incomplete.
2. **Summary.** A few sentences on what changed and what was verified.
3. **Open questions.** Decisions still needed, each with the default you will
   use if nobody answers. Write "none" when there are none.

Do not hand off by retelling the whole log. Point at the artifact and the
open questions.

## Definition of done

A task is done only when every line below is true:

1. **Acceptance criteria met with evidence.** Each criterion from the task
   template is satisfied, and the evidence is linked from the hand-off or the
   pull request.
2. **Reviewed by the named reviewer.** One review, from the person named on
   the task. Author self-review does not count.
3. **Tests pass for code.** For a code change, `test` passes. Also run
   `test-e2e` or `test-bdd` when the change touches those surfaces. A docs-only
   change has no test run to attach; say that in the evidence.
4. **Docs updated.** Readers can follow the new behavior from the docs. If the
   process changed, update this file or `AGENTS.md`, not a private note.
5. **Task progress updated.** Status, owner, and next step are current so the
   next person does not have to ask.

Merge still follows `AGENTS.md`: pull request only, green checks, no
force-push.

## Async stand-up note

Post one note on the task thread for each working day you touch it. Keep it
short enough to scan. Use this shape:

```text
Done: <what finished, with a link to the commit, PR, or file>
Next: <the next concrete step>
Blocked: <what is waiting, and on whom; or "none">
Approvals: <gate waiting on Venkat; or "none">
```

Skip narrative. If nothing moved, say so in `Done` and still name `Next`.
