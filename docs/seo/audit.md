# SEO audit

This audit reads pages from the local builder. It is a check of `agentsblog.build.build_site` on a temporary directory, not a crawl of a public host. There is no public hostname. The origin is the local preview at `http://127.0.0.1:8000`, which is what the builder uses when `site_url` is omitted.

The fixture was one published post (`canonical-urls`, with title, summary, tags, and `draft: false`) and one draft (`hidden-draft`). The site was not submitted to a search engine. This note stores no analytics IDs.

## Checks

These checks passed against that local preview:

- `robots.txt` contains `Sitemap`, and the draft slug is absent.
- `sitemap.xml` contains the published slug and does not contain the draft slug.
- The published post HTML contains `rel="canonical"`, `property="og:title"` (Open Graph), and exactly one `h1`.
- The canonical URL uses `http://127.0.0.1:8000` when `site_url` is omitted.

Evidence for the same checks is `tests/unit/test_seo_audit.py`, run with `python -m unittest tests.unit.test_seo_audit -v`.

## Out of scope

Search-engine submission, a public hostname, accounts, and analytics IDs wait for a later approval. This audit does not choose keywords for a public site.
