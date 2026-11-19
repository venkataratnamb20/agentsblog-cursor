# Threat model

This model covers the local Agents Blog preview. The public host, the analytics vendor, and the newsletter vendor are undecided. They are out of scope until Venkat approves an account and a host.

## Assets

| Asset | Where it lives | Why it matters |
| --- | --- | --- |
| Source and drafts | `content/` and the git history | A draft is not approved for publication. |
| Build output | `build/` | This is what the preview serves. It must omit drafts. |
| Loopback preview | `127.0.0.1` only | It is a local reading surface, not a public site. |
| Policy drafts | `privacy.html` and the other policy pages | They say they are not approved. Treating them as legal advice would be wrong. |

## Trust boundaries

1. **Author workstation.** The person and the agents edit the repository here. This is the trust root.
2. **Loopback HTTP.** `agentsblog.preview` binds `127.0.0.1`. Another machine on the network is outside this boundary.
3. **Future public host.** Not chosen. DNS, production deploy, and new accounts stay behind Venkat's approval.

## Threats

| Threat | What exists today | Requirement |
| --- | --- | --- |
| Script injection from a post body | Post bodies are escaped before they become HTML. Headings and paragraphs are escaped too. | Keep escaping user-controlled text. Do not mark a body as trusted HTML. |
| Draft leakage | The build drops posts whose draft flag is true from the index, post pages, search index, feed, and sitemap. | A draft path must stay absent from `build/`. |
| Preview exposed beyond the machine | The server address is `127.0.0.1`. | Do not bind a public interface for the local preview. |
| Path escape in the preview | The preview uses the standard-library static handler rooted at `build/`. | Serve only files under the chosen directory. |
| A secret committed to git | Policy is zero secrets in the repository, including worktrees. CI packages the build and does not scan for secrets yet. | Reject `.env`, tokens, and private keys in review. Record names, never values. |
| Dependency compromise | The local builder uses the Python standard library. No package is installed to build the site. | Do not add a package manager or a third-party install step in this slice. |
| Unapproved publish or account | Approval gates block publishing, DNS, production deploy, spending, account creation, and social posts. | A pull request is not approval. Wait for Venkat's explicit yes. |

## Out of scope

- A production hostname, CDN, or TLS certificate.
- An analytics account and any non-essential cookie.
- A newsletter vendor and double opt-in storage.
- The four-tool harness smoke test.

## Highest risks

1. A draft is copied into `build/` and then treated as public.
2. A post body is rendered as raw HTML and runs in the reader's browser.
3. The preview is rebound off loopback and becomes reachable on the network.
4. A token or `.env` file is committed. CI does not scan for it yet.
5. Someone treats a policy draft, or a local canonical URL of `http://127.0.0.1:8000`, as the live site.
