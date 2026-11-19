---
name: review-pr
description: "Review a pull request for scope, tests, and accidental secrets before it merges."
---

# Review pull request

## When to use

Use this skill when a pull request is ready for review and before it merges.

## Steps

1. Read the diff and the stated intent of the change.
2. Check that the change stays in scope and that tests cover the behavior.
3. Reject the diff if it adds a secret, a token, or a credential file.
4. Comment on defects with file references. Do not quote secret values. Record approve or request changes.

## Done when

The review is submitted, the verdict is explicit, and the review text contains no secret values.
