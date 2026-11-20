# System architecture

Agents Blog is a local static site. Markdown under `content/` is compiled into
HTML under `build/` by the Python standard library package at
`src/agentsblog/`. There is no package manager for the builder, and no hosting
choice in this document. Staging and production remain open decisions behind
approval gates (see ADR 0002).

This note describes the local system only. It does not name a host, a DNS
provider, or a secret store value.

## Boundaries

| Boundary | What it holds | What it does not hold |
| --- | --- | --- |
| Repository source | `content/`, `src/agentsblog/`, tests, docs | Tokens, passwords, connection strings, `.env` files |
| Build output | `build/` static files | Draft posts, unpublished policy claims treated as live |
| Local preview | Loopback HTTP on `127.0.0.1:8000` | Public traffic, TLS termination, multi-tenant auth |
| Outside the repo | Any future secret store a person configures | Secrets written into git, chat, or this doc |

Secrets, if a later environment needs them, live outside the repository. This
design names that constraint and does not invent a store. Agent roles that
touch this tree stay least-privilege: writers and editors change content and
docs; builders change `src/agentsblog/`; no role may create `.env` files or
paste credentials into architecture notes.

## Content to build pipeline

```text
content/posts/*.md
        |
        v
  agentsblog.posts   load markdown + front matter (all posts)
        |
        v
  agentsblog.build   drop drafts from public artifacts; write static tree
        |
        v
     build/          index, posts, search, feed, SEO, policies, CSS
        |
        v
  agentsblog.preview serve build/ on 127.0.0.1:8000
```

1. **Load.** `posts.load_posts` reads each `.md` file under `content/posts/`.
   Non-markdown files are ignored. Drafts and published posts are both
   returned. A missing directory yields an empty site.
2. **Filter.** `build_site` keeps published posts for post pages, tag pages,
   search index, feed, and sitemap. A post with `draft: true` is absent from
   those surfaces. The index renderer also skips drafts when listing.
3. **Render.** Published posts and fixed reader pages become HTML. Markdown
   bodies keep headings and paragraphs through `markdown`. Titles and body
   text are escaped on the way to HTML.
4. **Write.** `build_site` replaces `build/` and writes the public tree,
   including `assets/site.css`, `search-index.json`, `feed.xml`, `robots.txt`,
   and `sitemap.xml`. Canonical, feed, and sitemap origins default to the
   local preview URL until hosting is decided.
5. **Preview.** `preview` serves `build/` with the standard-library HTTP
   server bound to loopback. Default origin:
   `http://127.0.0.1:8000`.

Task runners call the same pipeline: `make build` / `.\make.ps1 build` runs
`compileall` on `scripts` and `tests`, then `python -m agentsblog.build` when
`src/agentsblog/build.py` exists. `dev` and `preview` invoke the preview
module against `build/`.

## Modules under `src/agentsblog/`

Package layout matches these modules (plus `__init__.py`):

| Module | Role |
| --- | --- |
| `__init__` | Marks the `agentsblog` package |
| `build` | Orchestrates load → filter → write into `build/` (`build_site`, `main`) |
| `posts` | Parses markdown posts and line-oriented front matter into `Post` (`load_posts`) |
| `markdown` | Renders a small Markdown subset to HTML |
| `render` | Builds HTML for index, post, search, about, subscribe, 404, tags |
| `consent` | Renders the local consent banner. The choice stays in localStorage |
| `search` | Matches published posts by title, summary, and tags |
| `tags` | Groups published posts by tag for tag pages |
| `feed` | Writes an RSS 2.0 feed of published posts |
| `seo` | Writes robots, sitemap, and on-page discovery metadata |
| `legal` | Generates draft policy pages (privacy, cookies, terms, licences, AI assistance) |
| `preview` | Serves a static directory on `127.0.0.1` (`serve_preview`, `main`) |

Modules stay free of host credentials and of network calls beyond the local
preview server. No module reads environment secrets.

## Content model

Posts live as one markdown file per post under `content/posts/`. Front matter
is a fenced block of `key: value` lines (not a full YAML parser).

### Document shape

```text
---
title: Required title
date: YYYY-MM-DD
tags: tag-a, tag-b
summary: Short description for search and feeds
draft: true
---

Body markdown after the closing fence.
```

| Field | Rules |
| --- | --- |
| `title` | Required. Missing or blank title fails the load. |
| `slug` | Derived from the filename stem, not from front matter. |
| `date` | Optional string, usually `YYYY-MM-DD`. Sort is date, then slug. |
| `tags` | Optional comma-separated list. Empty segments are dropped. |
| `summary` | Optional short description used by search and feeds. |
| `draft` | `true` (case-insensitive) means unpublished. Omitted or `false` means published for the local build. |
| body | Markdown after the closing `---` fence. |

### Drafts

- A draft stays in `content/` and in git until a person publishes it.
- Publishing a post is an approval gate, not a git action and not a build flag flip alone for a public site.
- The local build must never copy a draft into `build/` reader surfaces.
- Policy pages from `legal` are themselves drafts: they state they are not approved for publication.

`content/posts/` may be empty. An empty or missing directory still produces a
valid empty site (chrome, 404, empty search index, stylesheet).

## Environments

| Environment | Status | Purpose |
| --- | --- | --- |
| Local preview | Active | Build `content/` → `build/`, serve on loopback for authors and reviewers |
| Staging | Active path (GitHub Pages from `develop`) | Shared review URL via GitHub Actions; builds include drafts; must stay `noindex` / not indexed |
| Production | Active path (GitHub Pages from `main`) | Public site via GitHub Actions; builds exclude drafts; custom domain and DNS still wait on Venkat approval |

Local preview defaults:

- Origin: `http://127.0.0.1:8000`
- Bind host: `127.0.0.1` only
- Output directory: `build/`

Hosting is GitHub Pages via Actions ([ADR 0003](../adr/0003-github-pages-hosting.md)).
Default Pages hostnames are enough until Venkat approves a custom domain and
DNS. Treat loopback canonical URLs as local-only metadata.

## Explicit non-goals

- Attaching a custom domain or changing DNS without Venkat's approval
- Recording secret values or creating `.env` files in the repository
- Collecting email addresses before an email service is approved
- Choosing a package manager or newsletter vendor

## Related documents

- [ADR 0002: Python standard library site](../adr/0002-python-stdlib-site.md)
- [ADR 0003: GitHub Pages hosting](../adr/0003-github-pages-hosting.md)
- [Product requirements](../product/prd.md)
- [Approval gates](../governance/approval-gates.md)
- [Information architecture](../design/information-architecture.md)
