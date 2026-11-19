---
name: security-check
description: "Audit a change for secrets and excess privilege. Never print secret values."
---

# Security check

## When to use

Use this skill before merge or release when the change touches auth, dependencies, agent tools, or anything that might contain a secret.

## Steps

1. Inspect the diff for tokens, private keys, `.env` files, and pasted credentials.
2. Confirm each agent token is scoped to that agent and stored outside the repo.
3. Never print secret values. Name the file and the secret's name only.
4. Note that pre-commit and CI secret scanning will be added when CI exists. Until then, this check is manual.

## Done when

Findings are recorded without secret values, and the diff contains zero secrets. This skill must never print secret values.
