# Software requirements

Requirements for the local Agents Blog preview produced by
`src/agentsblog/`. Each ID is checkable against a local build or the
repository. A public host, newsletter vendor, and analytics vendor are
out of scope until Venkat approves them.

This specification matches the local builder described in
`docs/architecture/system.md` and the product slice in
`docs/product/prd.md`. Security-specific checks also live in
`docs/security/requirements.md`. Transfer-size limits live in
`docs/testing/performance-budgets.md`.

## Functional

| ID | Requirement | How to check |
| --- | --- | --- |
| FR-1 | Markdown posts with front matter load from `content/posts/`. A missing or empty directory still builds chrome. | A fixture with `title` builds `posts/{slug}.html`. A missing content directory still writes `index.html`, `404.html`, `search-index.json`, and `assets/site.css`. |
| FR-2 | Draft posts are omitted from every published surface. | `draft: true` is absent from the index, `posts/`, `search-index.json`, `search.html` results, `feed.xml`, `sitemap.xml`, and tag pages. |
| FR-3 | Readers can search published titles, summaries, and tags. | `search.html` loads `search-index.json`, lists a match for a query, and ignores a blank query. Drafts are not in the index. |
| FR-4 | An RSS feed lists published posts only. | `feed.xml` includes a published title and skips a draft. |
| FR-5 | The build writes robots.txt, a sitemap, and discovery metadata. | `robots.txt` and `sitemap.xml` exist. Drafts are absent from the sitemap. Index and post pages include canonical and Open Graph tags that use the build `site_url` (default `http://127.0.0.1:8000`). |
| FR-6 | Pages switch between light and dark themes. | The theme button sets `data-theme` and `aria-pressed`. |
| FR-7 | About names the audience. Subscribe collects no email. | `about.html` and `subscribe.html` exist; subscribe has no form and no email field. |
| FR-8 | Each published tag has a page of post links. | `tags/{slug}.html` lists published posts only. |
| FR-9 | Policy pages exist as drafts. | After a build, `privacy.html`, `cookies.html`, `terms.html`, `licences.html`, and `ai-assistance.html` state that Venkat has not approved publication. |
| FR-10 | The preview binds loopback. | The server listens on `127.0.0.1` (default origin `http://127.0.0.1:8000`). |
| FR-11 | A skip link reaches main content. | The first focusable control is the skip link to `#main`. |
| FR-12 | A consent banner precedes non-essential storage, and pages fit a narrow screen. | The banner offers Accept and Reject, stores the choice in `localStorage` under `agentsblog-consent`, and does not set a cookie or call the network. Each page includes a device-width viewport. The stylesheet narrows body margin at `40rem`. |
| FR-13 | A not-found page is part of the built site. | `404.html` exists after a build, including when `content/posts/` is empty. |
| FR-14 | A published post page keeps body structure and required title. | `posts/{slug}.html` shows the title. A body with a heading and a paragraph renders as HTML heading and paragraph elements. A missing or blank front-matter `title` fails the load. |

## Non-functional

| ID | Requirement | How to check |
| --- | --- | --- |
| NFR-1 | The local build uses the Python standard library only. | `build` runs `compileall` and `python -m agentsblog.build` (or `python3` on Unix). No package install is required to build the site. |
| NFR-2 | Post text is escaped. | A `<` in a title or body becomes `&lt;` in the HTML text. |
| NFR-3 | The repository holds no secret values. | Diffs and committed files exclude `.env`, tokens, passwords, connection strings, and private keys. Secret store *names* may appear in docs; values must not. Secrets live outside the repo. |
| NFR-4 | The accessibility target is WCAG 2.2 AA. | Named in `docs/design/accessibility.md`. The site is not audited yet; a human browser audit has not been accepted. |
| NFR-5 | Keyboard users can move through the local pages. | Tab reaches skip link, nav, search, and the theme button on Home, Search, a post, About, Subscribe, and 404. |
| NFR-6 | Built pages stay inside the local performance budgets. | After a build with one published post and one draft, `index.html` is at most 20000 bytes, `assets/site.css` is at most 8000 bytes, built HTML has no `<script src=`, and pages do not reference `fonts.googleapis.com` or a `cdn.` host. Limits and method: `docs/testing/performance-budgets.md`. These are on-disk byte and request-host budgets, not lab or field Core Web Vitals. |

## Out of scope

- Production hostname, DNS, and TLS
- Staging or production deploy
- Double opt-in newsletter storage or any email collection
- Third-party analytics or RUM vendor
- Publishing a post (approval gate, not a build flag alone)
- Package managers and hosted CMS choices

## Related documents

- `docs/product/prd.md` — problem, audience, local features, success metrics
- `docs/architecture/system.md` — pipeline, modules, content model, environments
- `docs/testing/performance-budgets.md` — NFR-6 limits
- `docs/design/accessibility.md` — WCAG 2.2 AA target
- `docs/security/requirements.md` — security checks for the local preview
- `docs/governance/approval-gates.md` — actions that wait on Venkat
