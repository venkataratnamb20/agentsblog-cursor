# Fortnightly Project Status Updates

## Status

Status: In progress

## Evidence

- `docs/progress/fortnightly-project-status-updates.md` (file) exists.

Update date: 2026-11-19.

### Goals against the repository

The public product site was not built. Hosting, DNS, accounts, spending, publishing, and social posts still wait on Venkat. The local preview can be built and opened on 127.0.0.1:8000.

| Goal | In the repository | Still open |
| --- | --- | --- |
| M0 harness | Guidelines, roster, approval gates, task runner, and Cursor and Claude pointers exist. | The four-tool smoke test has not been run. M0 is not closed. |
| Local site | The Python standard library builder writes the index, post pages, search, a 404 page, an RSS feed, robots.txt, a sitemap, draft policy pages, and a theme toggle. | There is no public host. |
| Content | Posts load from Markdown front matter. Bodies render headings and paragraphs. | `content/posts/` is empty. Publishing a post is an approval gate. MDX is not supported. |
| Newsletter | `feed.xml` lists published posts and skips drafts. | Double opt-in needs an email service. Creating that account is an approval gate. |
| SEO | Canonical URLs, Open Graph, schema.org, robots.txt, and a sitemap are generated. | The default origin is the local preview, because no production domain is chosen. |
| Quality | Unit and integration tests cover the builder. | End-to-end tests, visual regression, and a coverage tool are not in place. |
| Launch, M3 through M9 | Not started. | Staging, DNS, launch, hypercare, and subscriber goals need a host and Venkat's approval. |

## Remaining

- Venkat has not approved closing this task.
- Exit criteria are not met.
- The next update is due on 2026-12-03.
- Production deploy, DNS, account creation, publishing, and social posts stay behind the approval gates.
