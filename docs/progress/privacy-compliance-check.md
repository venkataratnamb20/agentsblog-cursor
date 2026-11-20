# Privacy Compliance Check

## Status

Status: In progress

## Evidence

- `docs/security/privacy-check.md` records UK GDPR and PECR for the local preview, states there is no analytics vendor, and records that policy pages are drafts waiting for Venkat.
- `tests/unit/test_privacy_compliance.py` builds a temp site and checks HTML for analytics hosts and for the substring `document.cookie=`.

## Remaining

- No analytics vendor is approved. Policies are drafts and are not approved for publication. Accounts wait for Venkat.
- Venkat has not approved closing this task.
- Exit criteria are not met.
