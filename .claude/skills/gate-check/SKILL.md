---
name: gate-check
description: "Block a merge until tests, review, and the security check have passed."
---

# Gate check

## When to use

Use this skill immediately before a merge, after the change is otherwise ready.

## Steps

1. Confirm the tests for this change pass.
2. Confirm review-pr is complete and the verdict is approve.
3. Confirm security-check is complete and it reported no secrets.
4. Stop the merge if any gate fails, and name the failing gate.

## Done when

Every gate is pass, or the merge is stopped and the failing gate is named.
