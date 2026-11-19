# Agents Blog

Stack-agnostic project scaffold. The application stack is not chosen yet. The directories below are the shared contract for source, content, tests, docs, research, and scripts.

## Layout

| Path | Purpose |
| --- | --- |
| `src/` | Application source. |
| `content/posts/` | Blog posts. |
| `tests/unit/` | Unit tests. |
| `tests/integration/` | Integration tests. |
| `tests/e2e/` | End-to-end tests. |
| `tests/features/` | Feature and acceptance tests. |
| `docs/prd/` | Product requirements. |
| `docs/adr/` | Architecture decision records. |
| `docs/guidelines/` | Engineering guidelines. |
| `docs/runbooks/` | Operational runbooks. |
| `docs/agents/` | Notes for coding agents. |
| `research/sources/` | Research source material. |
| `research/briefs/` | Research briefs. |
| `research/notes/` | Research notes. |
| `scripts/` | Repository scripts. |
| `.github/workflows/` | Automation workflows. |
| `.github/ISSUE_TEMPLATE/` | Issue templates. |
| `.github/pull_request_template.md` | Pull request template. |

Empty directories contain `.gitkeep` so Git keeps them.

## Tasks

Windows:

```powershell
.\make.ps1
```

macOS and Linux:

```sh
make
```

Setup and the test suite must pass. An empty suite is a pass. The scaffold check uses the Python standard library and does not depend on an application framework.

## Scaffold check

From the repository root:

```sh
python -m unittest tests.unit.test_scaffold
```

The test asserts that `src`, `content`, `tests`, `docs`, `research`, and `scripts` exist.

## Further reading

- [Contributing](CONTRIBUTING.md)
- [Git workflow](docs/guidelines/git-workflow.md)
- [Security](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)
