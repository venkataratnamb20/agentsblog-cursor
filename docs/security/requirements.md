# Security requirements

A reviewer can check each line against the repository or a local build. These
are security requirements for the **local static preview**. They are not the
full product requirements specification. There are **no user accounts** on this
surface. Consent exists without a third-party analytics vendor.

Cross-check: [threat-model.md](threat-model.md),
[approval-gates.md](../governance/approval-gates.md),
[secrets.md](../governance/secrets.md).

| ID | Requirement | How to check |
| --- | --- | --- |
| SR-1 | The preview listens on `127.0.0.1` only. | `src/agentsblog/preview.py` sets `_LOOPBACK_HOST` / bind address to `127.0.0.1`. It must not bind `0.0.0.0`. |
| SR-2 | A draft post is absent from the built site. | Build a fixture with `draft: true` and confirm it is missing from the index, `posts/`, `search-index.json`, `feed.xml`, and `sitemap.xml`. `build.py` filters drafts before those writers run. |
| SR-3 | Post titles and bodies are escaped; Markdown emits no raw HTML. | A fixture containing `<` renders `&lt;` in titles and bodies. `markdown.py` and `render.py` use `html.escape`; the Markdown subset is headings and paragraphs only. |
| SR-4 | The repository holds no secret values. | The diff has no `.env`, token, password, or private key. Names of secret stores may be documented. Values may not. CI does **not** secret-scan yet; this check is manual review. |
| SR-5 | The local build installs no third-party package. | `build` runs `compileall` and `python -m agentsblog.build` (stdlib only). No `pip install` / package-manager step is required to produce `build/`. |
| SR-6 | Publishing, DNS, production deploy, spending, new accounts, and social posts wait for Venkat. | The change does not perform those actions. `docs/governance/approval-gates.md` still names them. |
| SR-7 | Policy pages say they are not approved for publication. | `privacy.html` and the other policy pages include that sentence after a build. |
| SR-8 | Canonical URLs for the local build use the preview origin until a public host exists. | Generated canonical links use the `site_url` passed to the build, defaulting to `http://127.0.0.1:8000`. |
| SR-9 | Built pages load no third-party analytics or remote script host. | Built HTML has no `google-analytics.com`, `googletagmanager.com`, or `cdn.jsdelivr.net`, and no remote `<script src=...>`. Same-origin **inline** scripts (consent; search `fetch` of `/search-index.json`) are allowed. |
| SR-10 | Consent is local-only: `localStorage` choice, no cookie write, no network call. | `src/agentsblog/consent.py` stores Accept or Reject under `agentsblog-consent`, does not assign `document.cookie`, and does not fetch a vendor. |
| SR-11 | The local preview has no user-account or login surface. | Built pages and `src/` expose no registration, sign-in, or session cookie flow. |
| SR-12 | Reviewer and auditor roles stay read-only for secrets and production writes. | Security Engineer, Code Reviewer, and QA Engineer definitions grant no secret-store access and do not rotate tokens or deploy. |
| SR-13 | The preview serves only files under the chosen static root. | `preview_handler` passes `directory=` to `SimpleHTTPRequestHandler` rooted at the resolved `build/` path. |

## Still open (future surfaces)

These items are **not** required to close the local-preview threat model. They
remain honest gaps until a later stage owns them:

- CI (`.github/workflows/ci.yml`) runs tests and build; it does **not** fail a commit that contains a secret. Pre-commit / CI secret scanning is not implemented yet.
- There is no production host, so TLS, public access control, CDN, and newsletter surfaces are not specified here.
- End-to-end browser tests do not visit these pages yet.
- A public analytics vendor, cookie banner for non-essential cookies, and live privacy notice wait for Venkat.
