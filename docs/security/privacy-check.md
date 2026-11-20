# Privacy compliance check

This check covers the local preview only. There is no analytics vendor. Built HTML was checked for `google-analytics.com`, `googletagmanager.com`, and `cdn.jsdelivr.net`. The build does not call an analytics host.

The built HTML does not contain `document.cookie=`. There is no non-essential cookie write in the build. A sentence that mentions cookies in consent text is allowed. PECR stays intact until Venkat approves a vendor.

## UK GDPR

The local preview collects no personal data. It creates no accounts and stores no subscriber list. UK GDPR duties for a public site are not in force on this preview because there is no production host and no vendor processing personal data here.

Accounts wait for Venkat. Creating an analytics account, a newsletter account, or any other account is an approval gate.

## PECR

PECR covers cookies and similar tracking on a site offered to people in the United Kingdom. This preview:

- loads no analytics vendor
- writes no non-essential cookie
- does not call a tag manager or a third-party script host

A future analytics vendor needs Venkat's explicit approval before any script or cookie write is added.

## Policies

`privacy.html`, `cookies.html`, `terms.html`, `licences.html`, and `ai-assistance.html` are drafts. They are not approved for publication. Publishing those pages, or treating them as a live privacy notice, waits for Venkat.

## Still open

- No analytics vendor is selected.
- No cookie banner is required on this preview because the build sets no cookie.
- A public privacy notice is not approved for publication.
