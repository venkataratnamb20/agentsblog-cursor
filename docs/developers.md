# Developers

Agents Blog is a harness and documentation scaffold. The blog application, hosting, continuous integration, and posts are not built. Hosting and package managers stay undecided. The local site builder is the Python standard library ([ADR 0002](adr/0002-python-stdlib-site.md)). [ADR 0001](adr/0001-task-runner.md) chooses `Makefile` and `make.ps1` as the task runners.

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
| `dev` | Serves the local `build/` directory on 127.0.0.1 port 8000. |
| `lint` | Prints a no-op message. It will enforce zero lint warnings once the stack lands. |
| `format` | Prints that sources will be formatted with Prettier and ruff once the stack is chosen. |
| `typecheck` | Prints a no-op message until the strict type checker exists. |
| `test` | Runs unittest discovery when a `tests` directory exists. |
| `test-e2e` | Prints that end-to-end tests will run once the stack is chosen. |
| `test-bdd` | Prints that Gherkin journeys will run once the stack is chosen. |
| `coverage` | Prints a no-op message. The future core-logic target is 100 percent, and the CI gate is 80 percent. |
| `build` | Compiles `scripts` and `tests`, then runs the local site builder when `src/agentsblog/build.py` exists. |
| `preview` | Serves the local `build/` directory on 127.0.0.1 port 8000. |
| `audit` | Prints that dependencies will be audited once the stack is chosen. |
| `sync-agents` | Copies `.agents/skills` to `.claude/skills` as files. |
| `release` | Prints that a versioned release will be cut once the stack is chosen. It does not deploy. |
| `clean` | Prints that local build artifacts will be removed once the stack is chosen. |

A target that still needs a toolchain prints that future behavior and exits 0. `test`, `build`, `dev`, `preview`, and `sync-agents` do their work today. `dev` and `preview` keep running until you stop them.

Run the tests on Windows:

```powershell
.\make.ps1 test
```

On macOS and Linux the same test target is `make test`.

## Local site

`.\make.ps1 build` compiles `scripts` and `tests` with `python -m compileall`, then runs `python -m agentsblog.build` only when `src/agentsblog/build.py` exists. When that file is absent, the site step is skipped and the target exits with the compileall status. On macOS and Linux, `make build` uses `python3` for the same steps. Hosting and package managers stay undecided. The decision is [ADR 0002](adr/0002-python-stdlib-site.md).

```powershell
.\make.ps1 build
```

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

The GitHub repository is https://github.com/venkataratnamb20/agentsblog-cursor. [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs the test suite and the local site builder on every push and pull request. [`.github/workflows/cd.yml`](../.github/workflows/cd.yml) packages `build/` as an artifact on `main`. Neither workflow publishes the site.

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
