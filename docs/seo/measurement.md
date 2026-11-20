# Measurement

Agents Blog is written for AI engineers, researchers, and tech leads. This
contract covers the local preview only. The public site is not live.

A **KPI** is an outcome we care about after launch. Those outcomes are not
measured in the field today. A **KPM** is a process measure we can check in
the repository and local preview before a public host exists. Agents do not
invent tracking pixels, measurement IDs, or vendor SDKs for either set.

Related local SEO checks live in `docs/seo/audit.md`. That audit is a
builder fixture check, not a search-engine crawl.

## KPI

Field outcomes. Targets are unchanged from the PRD. None are measured on a
public host today.

| Metric | Target | Today |
| --- | --- | --- |
| Technically verified published posts | 10 | 0 |
| Confirmed newsletter subscribers | 100 | no signup; no email is collected |
| Reading experience | WCAG 2.2 AA | not a finished human audit |

The publishing outcome is 10 technically verified published posts. Today that
count is 0. The audience outcome is 100 confirmed newsletter subscribers.
Today there is no signup, and no email is collected. The reading outcome is a
WCAG 2.2 AA reading experience. Today that is not a finished human audit.

## KPM

These checks use the repository and the local preview at
`http://127.0.0.1:8000`. Run them with the Windows entry point unless you are
on Unix or macOS (`make` with the same target names).

| KPM | How to check | Pass when |
| --- | --- | --- |
| Unit and integration suite | `.\make.ps1 test` | exits 0 |
| Production build | `.\make.ps1 build` | writes `build/` and exits 0 |
| Drafts stay out of discovery | inspect `build/sitemap.xml` and `build/robots.txt` after a fixture build | draft slugs are absent; `Sitemap` is present |
| Local canonical origin | inspect published post HTML | `rel="canonical"` uses `http://127.0.0.1:8000` until a public host exists |
| Measurement contract honesty | this file | names KPIs, KPMs, Venkat gates; stores no credential |

Evidence for the same technical SEO surface is recorded in
`docs/seo/audit.md` and asserted by `tests/unit/test_seo_audit.py`.

## Public metrics that wait

Once a public host exists and Venkat has approved accounts and spending, the
metrics that matter are:

- **Organic sessions and landing pages** for published posts (property name
  only; credentials stay in the secret store outside the repo).
- **Index coverage** for published URLs (submitted sitemap vs indexed).
- **Confirmed subscribers** after double opt-in (newsletter property; no
  address stored in git).
- **Core Web Vitals** on the live origin (field data, not the local byte
  budgets in `docs/testing/performance-budgets.md`).

Until then, agents report KPMs from the table above. They do not create an
analytics property, paste a measurement ID into templates, or claim field
KPI progress from local preview traffic.

## What waits for approval

The measurement contract names **no analytics vendor**. The local rule is
that **no credential**, token, or measurement ID is stored in the repo.
Field analytics, newsletter signup storage, search-engine submission, a
public hostname, accounts, spending, and production deploys wait for
Venkat's explicit approval.

Indexing blockers for the technical editor, when a public host is ready:
missing canonicals, drafts in the sitemap, absent `robots.txt` Sitemap line,
or a non-indexable published URL. Those are reported from `docs/seo/audit.md`
and the builder tests; they are not fixed by adding analytics.
