---
name: hotfix
description: "Ship the smallest production fix from the released commit, with tests and a security check."
---

# Hotfix

## When to use

Use this skill when production is broken and the fix must ship ahead of unreleased work.

## Steps

1. Branch from the released commit, not from unreleased work.
2. Change only what is required to fix the incident.
3. Run the relevant tests, security-check, and an expedited review-pr.
4. Never print secret values while debugging. Refer to secrets by name only.

## Done when

The fix is merged, a patch tag exists or the release tag is updated, and main contains the same fix.
