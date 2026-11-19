# Product requirements

## Problem

Engineers who build AI agents need one place to read a careful argument, not a news roundup. Agents Blog does not have a public site yet. Readers cannot open a domain, subscribe, or read a published post.

## Audience

The readers are AI engineers, researchers, and tech leads. They design, build, evaluate, or lead work on agent systems.

## What the local preview does

A person at the repository can build a static site with the Python standard library and open it on `127.0.0.1`. That preview includes:

- an index of published posts, with drafts omitted
- a post page whose body keeps headings and paragraphs
- search over title, summary, and tags
- a 404 page
- an RSS feed
- a light and dark theme
- draft policy pages for privacy, cookies, terms, licences, and AI assistance
- robots.txt, a sitemap, and canonical and Open Graph metadata

The default origin is `http://127.0.0.1:8000`. That is the local preview, not a public host.

## What waits on approval

Venkat's explicit approval is required before any of these:

- spending money
- creating accounts, including an email or analytics vendor
- a production deploy
- DNS changes
- publishing posts
- posting on social networks or communities

`content/posts/` has no published posts. The subscribe page must not collect an email address until an email service is approved.

## Scope

In scope for the repository: the local builder, drafts, tests, and the documents that describe the product.

Out of scope until a later decision: a package manager, a hosted CMS, a production hostname, and a newsletter vendor.

## Success metrics

These are targets for after a public launch. None of them are measured today.

| Metric | Target | Today |
| --- | --- | --- |
| Technically verified posts | 10 published | 0 published |
| Confirmed newsletter subscribers | 100 | No signup |
| Reading experience | WCAG 2.2 AA | Not audited |
| Local build | `.\make.ps1 build` exits 0 | The builder writes `build/` |

A metric is not a claim that the number has been reached.
