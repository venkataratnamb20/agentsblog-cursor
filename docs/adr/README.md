# Architecture decision records

Accepted decisions for Agents Blog. Policy and commands stay in
[`AGENTS.md`](../../AGENTS.md). These files record *why* a boundary was chosen.

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-task-runner.md) | Task runner (`Makefile` + `make.ps1`) | Accepted |
| [0002](0002-python-stdlib-site.md) | Python standard library local site builder | Accepted |
| [0003](0003-github-pages-hosting.md) | GitHub Pages hosting (staging / production) | Accepted |

## Still undecided

ADR 0003 decides hosting. These stay open for Venkat:

- Package manager
- Newsletter service
- Custom domain / DNS (gated; not part of ADR 0003)

Do not create accounts or pick a paid host from an ADR alone. Those are
approval gates. Custom domain and DNS still need explicit Venkat approval.
