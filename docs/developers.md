# Developers

Agents Blog is a harness and documentation scaffold. The blog application, hosting, continuous integration, and posts are not built. The stack is not chosen. [ADR 0001](adr/0001-task-runner.md) only chooses `Makefile` and `make.ps1` as the task runners.

## Prerequisites

- Python 3. The current tests use the standard library. No extra packages are required.
- Windows: PowerShell, for `.\make.ps1 <target>`.
- macOS and Linux: `make`, for `make <target>`.

From the repository root, compile the Python sources with the standard library:

```sh
python -m compileall
```

`python -m compileall` bytecode-compiles `.py` files under the current directory and reports syntax errors. It does not install packages, and it does not build the blog.

## Task runner

Windows:

```powershell
.\make.ps1 <target>
```

macOS and Linux:

```sh
make <target>
```

Both entry points share these targets: `setup`, `dev`, `lint`, `format`, `typecheck`, `test`, `test-e2e`, `test-bdd`, `coverage`, `build`, `preview`, `audit`, `sync-agents`, `release`, `clean`.

| Target | What it does today |
| --- | --- |
| `setup` | Prints that dependencies will be installed once the stack is chosen. |
| `dev` | Prints that the local development server will start once the stack is chosen. |
| `lint` | Prints a no-op message. It will enforce zero lint warnings once the stack lands. |
| `format` | Prints that sources will be formatted with Prettier and ruff once the stack is chosen. |
| `typecheck` | Prints a no-op message until the strict type checker exists. |
| `test` | Runs unittest discovery when a `tests` directory exists. |
| `test-e2e` | Prints that end-to-end tests will run once the stack is chosen. |
| `test-bdd` | Prints that Gherkin journeys will run once the stack is chosen. |
| `coverage` | Prints a no-op message. The future core-logic target is 100 percent, and the CI gate is 80 percent. |
| `build` | Prints that a production build will be produced once the stack is chosen. |
| `preview` | Prints that the production build will be served once the stack is chosen. |
| `audit` | Prints that dependencies will be audited once the stack is chosen. |
| `sync-agents` | Copies `.agents/skills` to `.claude/skills` as files. |
| `release` | Prints that a versioned release will be cut once the stack is chosen. It does not deploy. |
| `clean` | Prints that local build artifacts will be removed once the stack is chosen. |

A target that still needs a toolchain prints that future behavior and exits 0. `test` and `sync-agents` do their work today.

Run the tests on Windows:

```powershell
.\make.ps1 test
```

Ask for a production build on Windows. Until the stack exists, this prints the future build step and exits 0:

```powershell
.\make.ps1 build
```

On macOS and Linux the same names are `make test` and `make build`.

## Test suite

From the repository root:

```sh
python -m unittest discover -s tests -v
```

`.\make.ps1 test` runs that command. `make test` runs `python3 -m unittest discover -s tests -v`.

Automated tests cover the scaffold and skill sync. `tests/unit/test_developer_docs.py` checks this guide. Manual tests live in [docs/testing/manual-tests.md](testing/manual-tests.md). That file is being added on another branch.

## Git workflow

`main` is protected production history. `develop` is the integration branch for the next release. Day-to-day work uses `feature/*`, branched from `develop`. `release/*` stabilizes a release. `hotfix/*` is an urgent fix branched from `main`.

Land changes through a pull request. One review is required, and required checks must be green. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/). Force-push is disabled on `main`, `develop`, and other shared branches.

The branch model, merge rules, and review rules are in [docs/guidelines/git-workflow.md](guidelines/git-workflow.md).

Coding standards are in [docs/guidelines/code-quality.md](guidelines/code-quality.md).

## Agent harness

Agents follow [AGENTS.md](../AGENTS.md).

Sync skills on Windows:

```powershell
.\make.ps1 sync-agents
```

`.\make.ps1 sync-agents` copies `.agents/skills` to `.claude/skills` with files, not symlinks. On macOS and Linux, `make sync-agents` runs the same copy.

## Progress

Task status is recorded in [docs/progress/README.md](progress/README.md).
