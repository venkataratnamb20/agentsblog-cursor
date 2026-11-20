# Fortnightly Project Status Updates

## Status

Status: In progress

## Evidence

- `docs/progress/fortnightly-project-status-updates.md` (file) exists.

Update date: 2026-11-20.

### Goals against the repository

The public product site was not built. Hosting, DNS, accounts, spending, publishing, and social posts still wait on Venkat. The local preview can be built and opened on 127.0.0.1:8000.

| Goal | In the repository | Still open |
| --- | --- | --- |
| M0 harness | Stages 0A and 0B closed: smoke evidence, skills/commands, roster, gates, secrets, DoD. | Codex and Antigravity remain out of scope per AGENTS.md. |
| M1 specifications | Closed: PRD, pillars, ADRs, architecture, SRS, threat model, security requirements, test strategy, SEO measurement. | Hosting and vendors stay undecided; publish waits for Venkat. |
| Local site | The Python standard library builder writes the index, post pages, search, a 404 page, an RSS feed, robots.txt, a sitemap, draft policy pages, and a theme toggle. | There is no public host. |
| Content | Posts load from Markdown front matter. Bodies render headings and paragraphs. | Publishing a post is an approval gate. MDX is not supported. |
| Newsletter | `feed.xml` lists published posts and skips drafts. | Double opt-in needs an email service. Creating that account is an approval gate. |
| SEO | Canonical URLs, Open Graph, schema.org, robots.txt, and a sitemap are generated. Local KPI/KPM checks are specified. | The default origin is the local preview, because no production domain is chosen. |
| Quality | Unit and integration tests cover the builder. Test strategy records honest gaps. | End-to-end tests, visual regression, and a coverage tool are not in place. |
| Design (M2) | Closed: IA, wireframes, brand, a11y specs, and free Canva hi-fi comps. | Stage 3 build and hosting still wait; human a11y audit optional later. |
| Launch, M3 through M9 | Not started. | Staging, DNS, launch, hypercare, and subscriber goals need a host and Venkat's approval. |

## Remaining

- Venkat has not approved closing this task.
- Exit criteria are not met.
- The next update is due on 2026-12-03.
- Production deploy, DNS, account creation, publishing, and social posts stay behind the approval gates.
