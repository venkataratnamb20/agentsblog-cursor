# M3 checklist — feature-complete on staging

Gate owner: PM Orchestrator. Approver: Venkat (hosting path approved as
GitHub Pages via Actions in this wave).

## Exit criteria

| Criterion | Evidence |
| --- | --- |
| Nine Stage 3 Build & Integration tasks Done | `docs/progress/README.md` |
| Staging deploy path on `develop` | `.github/workflows/cd.yml` (`deploy-staging`) |
| Hosting ADR accepted | `docs/adr/0003-github-pages-hosting.md` |
| CI green | `python -m unittest discover -s tests -v` |
| Posts 1–3 drafts render on staging-shaped build | `tests/unit/test_staging_smoke.py` |
| Staging is noindex | `AGENTSBLOG_NOINDEX` + `robots.txt` Disallow |

## Staging URL

Default GitHub Pages hostname (no custom domain until DNS approval):

`https://venkataratnamb20.github.io/agentsblog-cursor`

## Still gated after M3

- Custom domain / DNS
- Production deploy from `main` (package-only until Venkat approves ship)
- Newsletter email vendor / double opt-in send
- Analytics vendor
- Publishing posts (`draft: true` until Publish approval)
