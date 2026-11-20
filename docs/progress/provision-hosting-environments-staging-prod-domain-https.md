# Provision Hosting Environments Staging Prod Domain HTTPS

## Status

Status: Done

## Evidence

- Hosting ADR: `docs/adr/0003-github-pages-hosting.md` (GitHub Pages via Actions)
- Staging path: `develop` → Pages (`deploy-staging` in `.github/workflows/cd.yml`)
- Production path: `main` packages build; live ship still needs Venkat deploy approval
- Default HTTPS hostname: `https://venkataratnamb20.github.io/agentsblog-cursor`
- Environments documented in `docs/architecture/system.md`

Custom domain and DNS remain gated and are not part of this close.

## Remaining

none
