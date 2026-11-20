# Set Up CI/CD Pipeline With Preview Deploys Rollback

## Status

Status: Done

## Evidence

- `.github/workflows/ci.yml` — unittest + local build on push/PR
- `.github/workflows/cd.yml` — `develop` → GitHub Pages staging (drafts + noindex); `main` → production package artifact
- `docs/adr/0003-github-pages-hosting.md`
- `tests/unit/test_ci.py`
- Rollback: redeploy a prior successful `develop` commit / Pages deployment

## Remaining

none
