# Wireframes

Stage 2 low-fi text wireframes for the local preview. Paths match
`docs/design/information-architecture.md`. Accessibility chrome (skip link,
focus, heading order) follows `docs/design/accessibility.md`. Brand tokens
follow `docs/design/brand-identity.md`.

## Shared layout

- Single reading column, measure about `40rem`, centered on the page.
- Light theme: page `#f7f4ef`, text `#1c1915`. Dark theme inverts the pair.
- Type: Georgia (Times New Roman fallback). No purple, terracotta, or second
  accent palette.
- No cards: lists are plain stacked items (title, date, dek). Borders or
  background fills that turn a list item into a card are out of scope.
- Theme control sits after primary nav (and before `<main>` content in focus
  order per the a11y spec). Label: **Toggle theme**.

Every screen below starts with the same chrome:

```text
[Skip to content -> #main]
[Home] [Search] [About] [Subscribe] [Privacy]
[Toggle theme]
---------------------------------------------
<main id="main">  ...page body...  </main>
---------------------------------------------
Footer: Cookies | Terms | Licences | AI assistance
```

## Home (`/` / `index.html`)

First viewport hierarchy: brand `h1`, then tagline, then optional pillar
browse labels (editorial filters, not routes), then the post list.

```text
[Skip to content] [nav…] [Toggle theme]

H1  Agents Blog
    Clear writing for people who build AI agents.

    Pillars (optional browse labels — not links / not URLs):
    Foundations · Building · Evaluation · Safety · Operations

    Posts
    ---------------------------------------------------------
    Post title                          -> /posts/{slug}.html
    2026-03-01
    One-line dek (summary).
    ---------------------------------------------------------
    Another post title                  -> /posts/{slug}.html
    2026-02-14
    One-line dek (summary).
    ---------------------------------------------------------

    (Empty index: keep H1 + tagline; show empty-state copy.
     Draft titles never appear.)
```

List item anatomy (Home and Tag): **title** (link) + **published date** +
**one-line dek**. No card chrome.

## Post (`/posts/{slug}.html`)

```text
[Skip to content] [nav…] [Toggle theme]

H1  Post title
    Published: 2026-03-01
    Tags: tag-a -> /tags/{slug}.html · tag-b -> /tags/{slug}.html

    --- series chrome (only when the post is in a series) ---
    Part n of m · Series name (label only — no series URL)
    [← Previous: earlier post title]   [Next: later post title →]
    (Prev/Next are links to sibling post pages; series has no /series/… path.)
    -----------------------------------------------------------

    H2  Section heading
    paragraph…

    H2  Another section
    paragraph…  (author `<` shows as text, not markup)

    --- series chrome may repeat after the body if useful ---
    Part n of m
    [← Previous]  [Next →]
```

Series is an ordered reading list inside a pillar. Show **Part n of m** and/or
**Prev / Next** when metadata exists. Do not invent `/series/...` or
`/pillars/...` routes.

## Tag (`/tags/{slug}.html`)

```text
[Skip to content] [nav…] [Toggle theme]

H1  Tag name

    Posts with this tag
    ---------------------------------------------------------
    Post title                          -> /posts/{slug}.html
    2026-03-01
    One-line dek (summary).
    ---------------------------------------------------------
    Another post title                  -> /posts/{slug}.html
    2026-02-14
    One-line dek (summary).
    ---------------------------------------------------------
```

Same list anatomy as Home. No cards. Drafts do not appear and do not create
tag pages.

## About (`/about.html`)

```text
[Skip to content] [nav…] [Toggle theme]

H1  About

    Agents Blog is a technical blog on AI agents for engineers,
    researchers, and tech leads.

    Clear writing for people who build AI agents.

    The public site is not live. This page is for the local preview.
```

## Subscribe (`/subscribe.html`)

Messaging only. No email field, no form, no submit control.

```text
[Skip to content] [nav…] [Toggle theme]

H1  Subscribe

    Subscribe is blocked until an email service is approved.

    There is no signup form on this page in Stage 2.
    Check back after Venkat approves an email provider.
```

## 404 (`/404.html`)

```text
[Skip to content] [nav…] [Toggle theme]

H1  Page not found

    That URL is not in the local preview.

    [← Back to Home]  -> /
```

Written for preview; omitted from `sitemap.xml` per IA.

## High-fidelity Canva comps

Free Canva designs (no paid assets). Same links live in
`docs/design/brand-identity.md`.

| Asset | Screens / purpose | Design URL |
| --- | --- | --- |
| Wordmark / logo | Brand lockup for comps | https://canva.link/oxyabeh6l5e8ob5 (`DAHbfcx1QuE`) |
| Cover template | Post social cover (`1200×630`) | https://canva.link/g38m5q8jonztu6a (`DAHbfb7CfD4`) |
| UI kit (hi-fi) | Home, Post, Tag, About, Subscribe, 404 | https://canva.link/hqxpaycdvp8mt9y (`DAHbfYnneE0`) |

Design note: an earlier kit (`DAHbfbK4dXg`) drifted on tagline, nav, and
subscribe copy. The link above is the iterated free kit aimed at the Stage 2
brief. ASCII wireframes in this file remain the implementation source of truth
for Stage 3.
