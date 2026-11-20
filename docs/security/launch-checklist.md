# Launch security checklist

This maps SR-1 through SR-8 from [requirements.md](requirements.md) onto the local preview. There is no production host. TLS is not configured. A CDN is not configured. This is not a completed launch review.

The checks below were run against a temporary build from `agentsblog.build.build_site` and against the repository text. They do not replace Venkat's approval for a public host.

| ID | Local check | What this run saw |
| --- | --- | --- |
| SR-1 | `src/agentsblog/preview.py` sets the bind host to `127.0.0.1`. | The preview source contains `127.0.0.1`. |
| SR-2 | A draft post is absent from the index, `posts/`, `search-index.json`, `feed.xml`, and `sitemap.xml`. | The checklist build used an empty content directory. Draft exclusion stays with the post build tests. |
| SR-3 | A fixture containing `<` renders `&lt;` and does not leave the raw character in the text. | Escaping stays with the render tests. This run did not add an escape fixture. |
| SR-4 | The diff has no `.env`, token, password, or private key. Secret-store names may be documented. Values may not. | Built files were scanned for `AKIA`, `BEGIN PRIVATE KEY`, and `api_key=`. No `.env` file was created. |
| SR-5 | `build` runs `compileall` and `python -m agentsblog.build`. The local build installs no third-party package. | This run called `build_site` from the standard-library builder. It did not install a package. |
| SR-6 | Publishing, DNS, production deploy, spending, new accounts, and social posts wait for Venkat. | This run did none of those. [approval-gates.md](../governance/approval-gates.md) still names them. |
| SR-7 | `privacy.html` and the other policy pages include the sentence that they are not approved for publication. | The builder writes those draft pages. Publication still waits for Venkat. |
| SR-8 | Generated canonical links use the `site_url` passed to the build, defaulting to `http://127.0.0.1:8000`. | The builder default remains the loopback preview origin. |

## Third-party scripts

Built HTML was checked for `<script src=` and for `google-analytics.com`, `googletagmanager.com`, and `cdn.jsdelivr.net`. A CDN is not configured for this preview.

## Still open

- There is no production host, so TLS and public access control are not configured.
- CI does not yet fail a commit that contains a secret.
- This is not a completed launch review. Venkat has not approved a public host, a certificate, or a CDN.
