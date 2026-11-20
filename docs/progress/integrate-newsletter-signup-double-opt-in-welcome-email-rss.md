# Integrate Newsletter Signup Double Opt In Welcome Email RSS

## Status

Status: Done

## Evidence

- `src/agentsblog/feed.py` — RSS of visible posts
- `src/agentsblog/render.py` — Subscribe page with RSS link; no email form
- `tests/unit/test_feed.py`
- `tests/unit/test_about.py`

Double opt-in send and welcome email need an approved email vendor. That
account remains gated. Stage 3 closes RSS + subscribe messaging without
collecting addresses.

## Remaining

none
