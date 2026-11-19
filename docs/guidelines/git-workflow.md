# Git workflow

## Branches

| Branch | Role | Environment |
| --- | --- | --- |
| `main` | Production history. Each release is a tag on this branch. | production |
| `develop` | Integration branch for completed tasks. | staging |
| `feature/<id>-<slug>` | Work for a single task. | — |
| `release/*` | Release preparation cut from `develop`. | — |
| `hotfix/*` | A production fix cut from `main`. | — |

`develop` maps to staging. `main` maps to production.

## Merges

- Merge `feature/<id>-<slug>` into `develop` with a squash merge.
- Merge `release/*` into `main`, tag the release on `main`, and back-merge into `develop`.
- Merge `hotfix/*` into `main`, tag the hotfix on `main`, and merge it into `develop`.

## Protection

`main` and `develop` accept changes through pull requests only.

- One approving review is required.
- Checks must be green.
- Force-push is disabled.

## Commits and versions

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Version numbers and release tags follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Pull requests

Each pull request links its task. One task uses one branch and one pull request.

## Agents

Agents open pull requests when changing `main` or `develop`. Direct pushes to `main` and `develop` are outside the workflow.
