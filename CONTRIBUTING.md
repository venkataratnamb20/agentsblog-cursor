# Contributing

## One task, one branch, one pull request

Each task uses one branch and one pull request. Name the branch `feature/<id>-<slug>` and link the task in the pull request. The branch model, review rules, and release flow are in [docs/guidelines/git-workflow.md](docs/guidelines/git-workflow.md).

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
type(scope): summary
```

The scope is optional. Use types such as `feat`, `fix`, `docs`, `test`, `refactor`, and `chore`. Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Before a pull request

On Windows, run `.\make.ps1`. On macOS and Linux, run `make`. Setup and the test suite must pass. An empty suite is a pass.

Keep secrets out of the branch. See [SECURITY.md](SECURITY.md).
