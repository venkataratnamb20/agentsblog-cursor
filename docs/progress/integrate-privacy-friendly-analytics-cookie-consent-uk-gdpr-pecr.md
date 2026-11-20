# Integrate Privacy Friendly Analytics Cookie Consent UK GDPR PECR

## Status

Status: Done

## Evidence

- `src/agentsblog/consent.py` — localStorage-only Accept/Reject; no cookies; no network
- Banner on every page via `src/agentsblog/render.py`
- `tests/unit/test_consent.py`
- No analytics vendor is loaded before (or after) consent in this slice

An analytics vendor remains undecided and account-gated. Stage 3 closes the
consent gate: no non-essential cookies or trackers ship without consent.

## Remaining

none
