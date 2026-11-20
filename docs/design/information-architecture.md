# Information architecture

There is no public host. Paths below are for the local preview at
`http://127.0.0.1:8000` (`build/` from `agentsblog.build`). Draft posts are
absent from every reader surface and from `sitemap.xml`.

## Sitemap

Paths match files the local builder writes under `build/`.

| Path | Page |
| --- | --- |
| `/` (`index.html`) | Index of published posts |
| `/search.html` | Search |
| `/about.html` | About the blog and its readers |
| `/subscribe.html` | Subscribe, with no email form |
| `/posts/{slug}.html` | One published post |
| `/tags/{slug}.html` | Posts that share a published tag |
| `/feed.xml` | RSS |
| `/privacy.html` | Privacy draft |
| `/cookies.html` | Cookies draft |
| `/terms.html` | Terms draft |
| `/licences.html` | Licences draft |
| `/ai-assistance.html` | AI assistance draft |
| `/404.html` | Missing page (written for preview; omitted from `sitemap.xml`) |

Supporting files (not reader pages): `/robots.txt`, `/sitemap.xml`,
`/search-index.json`, `/assets/site.css`.

## Navigation

**Global nav** (every page): Home, Search, About, Subscribe, Privacy.

**Footer legal links:** Cookies, Terms, Licences, and AI assistance. Privacy
stays in the global nav as the primary policy entry; the other draft policies
are secondary legal links, not global nav items.

Tag links sit on the post page, not in the global nav.

## Taxonomy

| Kind | URL rule |
| --- | --- |
| Tag | `/tags/{slug}.html` for each distinct published tag. Slug is lowercase; non-alphanumeric runs become hyphens; empty slugs are dropped. Drafts do not create tag pages. |
| Pillar | Editorial only: Foundations, Building, Evaluation, Safety, Operations. No `/pillars/...` URLs. |
| Series | Ordered reading list inside a pillar (`docs/product/content-pillars.md`). No dedicated series URLs. |

A tag is a label on a published post. A series is an ordered list of posts
inside a pillar. Pillars guide topic choice; they are not routes.

## Home browse

The index may list the five pillar names as browse headings or filters above
the post list so readers can scan the body of work by topic. Pillar labels on
Home do not add `/pillars/...` URLs.
