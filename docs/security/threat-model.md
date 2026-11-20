# Threat model

This model covers the **local Agents Blog static preview** only. The site is
built with the Python standard library (`src/agentsblog/build.py`), served from
`build/` on loopback (`src/agentsblog/preview.py`), and has **no user
accounts**, no login, and no session store. There is **no third-party analytics
vendor**. Consent on the preview stores a choice in `localStorage` only
(`src/agentsblog/consent.py`); it does not set a cookie and does not call the
network.

The public host, TLS, any analytics account, and any newsletter vendor are
undecided. They stay out of scope until Venkat approves an account and a host
under [approval-gates.md](../governance/approval-gates.md).

This slice aligns with the parts of the [OWASP Top 10](https://owasp.org/www-project-top-ten/)
that apply to a local static site today: **injection / XSS** (escaped author
text), **software supply chain** (stdlib-only build, no third-party packages or
remote scripts), and **secrets mishandling** (zero secrets in the repo; manual
review until CI scans). Account, session, and broken-access-control categories
do not apply yet.

## Assets

| Asset | Where it lives | Why it matters |
| --- | --- | --- |
| Source and drafts | `content/` and the git history | A draft is not approved for publication. |
| Build output | `build/` | This is what the preview serves. It must omit drafts. |
| Loopback preview | `127.0.0.1` only | It is a local reading surface, not a public site. |
| Policy drafts | `privacy.html` and the other policy pages | They say they are not approved. Treating them as legal advice would be wrong. |
| Consent choice | Browser `localStorage` key `agentsblog-consent` | Records Accept or Reject on this machine only. It is not a tracking cookie and must not become one without approval. |
| Guardrail documents | `AGENTS.md`, `docs/governance/secrets.md`, approval gates | They keep secrets out of the repo and block gated actions. Weakening them in a change is a security defect. |

## Trust boundaries

1. **Author workstation.** The person and the agents edit the repository here. This is the trust root. There is no remote reader account to authenticate.
2. **Loopback HTTP.** `agentsblog.preview` binds `127.0.0.1` via `ThreadingHTTPServer`. Another machine on the network is outside this boundary.
3. **Static root.** The preview handler roots `SimpleHTTPRequestHandler` at the chosen `build/` directory. Request paths must resolve inside that directory only.
4. **Browser storage on the same machine.** The consent script may write `localStorage` for that origin. It must not write `document.cookie` or call a third-party host.
5. **Same-origin preview scripts.** Built pages may include **inline** scripts (consent banner; client search that `fetch`es `/search-index.json` on the same origin). They must not load a remote `<script src=...>`.
6. **Future public host.** Not chosen. DNS, production deploy, TLS, CDN, and new accounts stay behind Venkat's approval.

## What is not a threat yet

These are common web threats that **do not apply** to the local static
preview because the surface does not exist:

- Account takeover, password spraying, or session fixation (no accounts or sessions).
- Broken access control on per-user data (no user data store).
- CSRF against authenticated state-changing APIs (no authenticated API).
- TLS misconfiguration or CDN cache poisoning (no public host).

They become in scope when a host, accounts, or a vendor is approved.

## Threats

| Threat | What exists today | Requirement |
| --- | --- | --- |
| Script injection from a post body (XSS) | `render_markdown` and page renderers run author text through `html.escape`. The Markdown subset is ATX headings and paragraphs only; it does not emit raw HTML, links, or scripts. | Keep escaping author-controlled text. Do not mark a body as trusted HTML. |
| Draft leakage | `build.py` drops posts whose draft flag is true before writing the index, post pages, search index, feed, and sitemap. | A draft path must stay absent from `build/`. |
| Preview exposed beyond the machine | `preview.py` sets `_LOOPBACK_HOST = "127.0.0.1"`. | Do not bind `0.0.0.0` or another public interface for the local preview. |
| Path escape in the preview | The handler passes `directory=` to `SimpleHTTPRequestHandler` so files are served only under the chosen root. | Serve only files under the chosen directory. |
| A secret committed to git | Policy is zero secrets in the repository, including worktrees. See [secrets.md](../governance/secrets.md). `.github/workflows/ci.yml` runs tests and a local build with `contents: read`; it does **not** secret-scan. | Reject `.env`, tokens, and private keys in review. Record names, never values. |
| Dependency / supply-chain compromise | The local builder uses the Python standard library. No package manager install step builds the site. Built HTML loads no remote script CDN. | Do not add a package manager, a third-party install step, or a remote `<script src>` in this slice. |
| Unapproved publish or account | Approval gates block publishing, DNS, production deploy, spending, account creation, and social posts. | A pull request is not approval. Wait for Venkat's explicit yes. |
| Third-party analytics or tracking before approval | Built pages load no analytics host and do not set a non-essential cookie. PECR-style storage stays local until a vendor is approved. | Do not add a third-party script, tag manager, or tracking pixel without Venkat's yes. |
| Consent banner used as a tracking hook | The banner stores Accept or Reject in `localStorage` only. It does not set `document.cookie` and does not call the network. | Keep consent local-only. Do not treat Accept as permission to load a vendor that does not exist yet. |
| Auditor privilege creep | Security Engineer, Code Reviewer, and QA Engineer roles are read-only auditors. They do not receive write credentials or secret-store access. | Keep reviewer and auditor tokens out of those roles. Do not paste secret values into chat or the repo. |
| CI package mistaken for a live deploy | GitHub Actions may test and package the local build. Packaging is not publishing. | Treat a CI artifact as a build product only. Production deploy waits for Venkat. |

## Out of scope

- A production hostname, CDN, or TLS certificate.
- An analytics account and any non-essential cookie or third-party storage.
- A newsletter vendor and double opt-in storage.
- User registration, login, or per-reader personal data processing.
- The four-tool harness smoke test (Codex and Antigravity remain out of scope per `AGENTS.md`).

## Highest risks

1. A draft is copied into `build/` and then treated as public.
2. A post body is rendered as raw HTML and runs in the reader's browser.
3. The preview is rebound off loopback and becomes reachable on the network.
4. A token or `.env` file is committed. CI does not scan for it yet.
5. A third-party analytics or consent script is added before Venkat approves a vendor.
6. Someone treats a policy draft, or a local canonical URL of `http://127.0.0.1:8000`, as the live site.
