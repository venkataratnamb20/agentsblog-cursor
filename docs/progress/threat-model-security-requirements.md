# Threat Model Security Requirements

## Status

Status: Done

## Evidence

- `docs/security/threat-model.md` — local-preview threat model: assets, trust boundaries (loopback, static root, same-origin inline scripts), OWASP-aligned XSS / supply-chain / secrets threats, draft exclusion, escaped Markdown bodies, no third-party scripts, auditor least privilege; hosting/TLS/newsletter out of scope; honest gap that CI does not secret-scan.
- `docs/security/requirements.md` — SR-1 through SR-13 with check steps for loopback bind, draft omission, `html.escape` Markdown, no secrets in repo, stdlib-only build, approval gates, policy draft wording, local canonical URL, no remote scripts, localStorage-only consent, no accounts, read-only auditor roles, and preview path confinement; Still open lists no CI secret scan and no prod host.

## Remaining

none
