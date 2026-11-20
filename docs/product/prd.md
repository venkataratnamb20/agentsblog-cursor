# Product requirements

## Problem

People who design, build, evaluate, or lead AI agent systems need careful,
specific writing—one idea treated well—not a news roundup. Agents Blog exists
to serve that need. Today there is no public site: no domain, no hosted pages,
and no way for a reader outside the repository to open a post or subscribe.

A local Python standard-library builder can produce a static preview on
`127.0.0.1`. That is a development aid, not a published blog. Drafts may exist
under `content/posts/` with `draft: true`; they do not appear in the published
index until Venkat approves publishing.

## Audience

| Reader | What they need from a post |
| --- | --- |
| AI engineer | Enough detail to design or debug an agent loop, tools, or eval |
| Researcher | Precise claims and clear limits on what the post does not prove |
| Tech lead | Language that helps review architecture, risk, and trade-offs |

Editorial framing uses five pillars (Foundations, Building, Evaluation, Safety,
Operations) in `docs/product/content-pillars.md`. Pillars guide topic choice;
they do not publish anything by themselves.

## In scope: local preview

A person at the repository can run the site builder (`src/agentsblog/build.py`
via `.\make.ps1 build` / `make build`) and open the output on
`http://127.0.0.1:8000`. That local preview includes:

- an index of **published** posts only (`draft: true` posts are omitted)
- post pages whose bodies render ATX headings and paragraphs (not full Markdown)
- an about page that states the audience and that the public site is not live
- client-side search over title, summary, and tags
- tag pages for tags that appear on published posts
- a 404 page
- an RSS feed at `/feed.xml`
- light and dark theme (including a theme toggle)
- a subscribe page that **does not** collect an email address
- draft policy pages (privacy, cookies, terms, licences, AI assistance)
- robots.txt, sitemap.xml, and canonical / Open Graph metadata
- cookie-consent UI scaffolding in the preview chrome

The default origin is `http://127.0.0.1:8000`. That origin is local preview
only. Hosting and package managers remain undecided
([ADR 0002](../adr/0002-python-stdlib-site.md)).

Also in scope for the repository: Markdown drafts, tests, product and
governance docs, and agent instruction pointers that keep policy in
`AGENTS.md`.

## Out of scope and approval gates

Out of scope until a later decision (and not claimed as shipped):

- a public hostname or production deploy
- a package manager or Node/CMS stack for the site
- a hosted newsletter or email vendor
- measured analytics, subscriber counts, or WCAG audit results
- social or community posting as distribution

Venkat's **explicit** approval is required before any of these
([approval gates](../governance/approval-gates.md)):

- spending money
- creating accounts (including email or analytics vendors)
- production deploys
- DNS changes
- publishing posts (making a draft public or syndicating the full post)
- posting on social networks or communities

`content/posts/` may hold drafts; publishing remains a human gate, not a git
action. The subscribe page must stay non-collecting until an email service is
approved.

## Success metrics

Split what can be checked in the repo today from targets that only apply after
a public launch. A target is not a claim that the number has been reached.

### Measurable now (local repository)

| Metric | Signal | Today |
| --- | --- | --- |
| Local build | `.\make.ps1 build` / `make build` exits 0 and writes `build/` | Builder exists and is the intended check |
| Draft discipline | Published index omits `draft: true` posts | Drafts stay unpublished without approval |

### Not measured until a public launch

| Metric | Target | Today |
| --- | --- | --- |
| Technically verified posts | 10 published | 0 published; public site not live |
| Confirmed newsletter subscribers | 100 (double opt-in) | No signup; subscribe page does not collect email |
| Reading experience | WCAG 2.2 AA | Not audited |

There is no public site, no production hostname, and no subscriber or traffic
measurement in this repository.
