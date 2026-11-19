# Security requirements

A reviewer can check each line against the repository or a local build. These are security requirements for the local preview. They are not the full product requirements specification.

| ID | Requirement | How to check |
| --- | --- | --- |
| SR-1 | The preview listens on `127.0.0.1`. | `src/agentsblog/preview.py` sets the bind host to `127.0.0.1`. |
| SR-2 | A draft post is absent from the built site. | Build a fixture with `draft: true` and confirm it is missing from the index, `posts/`, `search-index.json`, `feed.xml`, and `sitemap.xml`. |
| SR-3 | Post titles and bodies are escaped. | A fixture containing `<` renders `&lt;` and does not contain the raw character in the text. |
| SR-4 | The repository holds no secret values. | The diff has no `.env`, token, password, or private key. Names of secret stores may be documented. Values may not. |
| SR-5 | The local build installs no third-party package. | `build` runs `compileall` and `python -m agentsblog.build`. |
| SR-6 | Publishing, DNS, production deploy, spending, new accounts, and social posts wait for Venkat. | The change does not perform those actions. `docs/governance/approval-gates.md` still names them. |
| SR-7 | Policy pages say they are not approved for publication. | `privacy.html` and the other policy pages include that sentence after a build. |
| SR-8 | Canonical URLs for the local build use the preview origin until a public host exists. | Generated canonical links use the `site_url` passed to the build, defaulting to `http://127.0.0.1:8000`. |

## Still open

- CI does not yet fail a commit that contains a secret.
- There is no production host, so TLS and public access control are not specified here.
- End-to-end browser tests do not visit these pages yet.
