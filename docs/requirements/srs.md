# Software requirements

Requirements for the local Agents Blog preview. Each ID is checkable. A public host, newsletter vendor, and analytics vendor are out of scope until Venkat approves them. Security-specific checks also live in `docs/security/requirements.md`.

## Functional

| ID | Requirement | How to check |
| --- | --- | --- |
| FR-1 | Markdown posts with front matter load from `content/posts/`. | A fixture with `title` builds a page. |
| FR-2 | Draft posts are omitted from the built site. | `draft: true` is absent from the index, post pages, search index, feed, and sitemap. |
| FR-3 | Readers can search published titles, summaries, and tags. | `search.html` lists a match and ignores a blank query. |
| FR-4 | An RSS feed lists published posts only. | `feed.xml` includes a published title and skips a draft. |
| FR-5 | The build writes robots.txt, a sitemap, and page metadata. | Files exist; drafts are absent from the sitemap. |
| FR-6 | Pages switch between light and dark themes. | The theme button sets `data-theme` and `aria-pressed`. |
| FR-7 | About names the audience. Subscribe collects no email. | `about.html` and `subscribe.html` exist; subscribe has no form. |
| FR-8 | Each published tag has a page of post links. | `tags/{slug}.html` lists published posts only. |
| FR-9 | Policy pages exist as drafts. | Privacy and related pages say Venkat has not approved publication. |
| FR-10 | The preview binds loopback. | The server listens on `127.0.0.1`. |
| FR-11 | A skip link reaches main content. | The first focusable control is the skip link to `#main`. |

## Non-functional

| ID | Requirement | How to check |
| --- | --- | --- |
| NFR-1 | The local build uses the Python standard library only. | `build` runs `compileall` and `python -m agentsblog.build`. |
| NFR-2 | Post text is escaped. | A `<` in a title or body becomes `&lt;`. |
| NFR-3 | The repository holds no secret values. | Diffs exclude `.env`, tokens, and private keys. |
| NFR-4 | The accessibility target is WCAG 2.2 AA. | Named in `docs/design/accessibility.md`. The site is not audited yet. |
| NFR-5 | Keyboard users can move through the local pages. | Tab reaches skip link, nav, search, and the theme button. |

## Out of scope

- Production hostname, DNS, and TLS
- Double opt-in newsletter storage
- Privacy-friendly analytics and cookie consent UI
- Publishing a post
