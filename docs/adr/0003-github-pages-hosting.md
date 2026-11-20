# ADR 0003: GitHub Pages hosting

## Status

Accepted

This decision covers **staging and production hosting** only. It does not
change the local site builder (ADR 0002), choose a package manager, attach a
custom domain, or pick a newsletter service.

## Date

2026-11-20

## Context

Agents Blog needs shared staging and production URLs so reviewers can accept
milestone work without running a local preview. ADR 0002 left hosting open on
purpose: the local builder is Python standard library, and picking a host was
an approval gate for Venkat.

The git flow already maps long-lived branches to environments: `develop` is
the integration branch; `main` is production history. Staging must be usable
for milestone acceptance, including draft posts 1–3, without those drafts
appearing on the public site. Staging must also stay out of search indexes.
Production must publish only non-draft posts.

A paid host, a new account at a separate vendor, or a custom domain would each
cross additional approval gates. GitHub Pages can serve static output from
this repository through GitHub Actions, using the same remote and credentials
the project already uses for source control. Secrets still stay out of the
repository. Custom domain and DNS remain a separate Venkat approval.

## Decision

Host staging and production on **GitHub Pages**, deployed by **GitHub
Actions**, from the static tree produced by the existing Python standard
library builder (`src/agentsblog/build.py` / ADR 0002).

| Environment | Branch | Build policy | Indexing |
| --- | --- | --- | --- |
| Staging | `develop` | Include drafts so unpublished posts render for review and M3 acceptance | `noindex` (and equivalent robots / meta controls so staging is not indexed) |
| Production | `main` | Exclude drafts | Normal public indexing once the site is live |

Deploy rules:

- A merge (or equivalent protected update) to `develop` deploys staging.
- A merge to `main` deploys production.
- The workflow builds with the same local builder contract as `make build` /
  `.\make.ps1 build`. It does not introduce a second site stack.
- No tokens, passwords, or connection strings are committed. If Actions later
  needs a secret, a person stores it in the GitHub secret store outside the
  repo. This ADR names that store; it does not record values.
- Custom domain and DNS are **not** part of this decision. Default GitHub
  Pages hostnames are enough until Venkat approves DNS changes.

### Remains undecided

These stay open until Venkat approves a later decision. This ADR does not
pick them:

| Topic | Why it stays open |
| --- | --- |
| Custom domain / DNS | Needs separate Venkat approval for DNS changes |
| Package manager | Local and CI builds use the Python standard library only |
| Newsletter service | Needs an approved vendor and account; double opt-in is a later slice |

## Consequences

- Staging and production have a chosen host. ADR 0002's "hosting undecided"
  note is superseded for that topic only; the local builder decision stands.
- Staging can show drafts for acceptance. Production never publishes drafts
  through the build filter.
- Staging must ship with `noindex` (and matching robots / meta behavior) so
  draft URLs are not indexed.
- Production deploys still require Venkat's explicit approval per
  `docs/governance/approval-gates.md`. Choosing GitHub Pages does not by
  itself authorize the first production ship, a custom domain, or DNS.
- Publishing a post remains an approval gate, not a git action alone.
- Newsletter, package manager, and custom domain stay open. Leaving them
  undecided is intentional.

## Rejected alternatives

**Paid static host or separate CDN account.** Would create a new vendor
account and possibly spend before this slice needs it. Rejected while GitHub
Pages covers staging and production from the existing remote.

**Hosted CMS.** Would replace the local markdown → static pipeline and force
an account decision ADR 0002 already deferred. Rejected.

**Deploying drafts to production with robots-only protection.** Drafts must
be absent from the production build, not merely discouraged from indexing.
Rejected.
