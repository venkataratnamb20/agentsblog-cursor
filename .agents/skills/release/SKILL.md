---
name: release
description: "Ship a version after the gates pass, with a changelog and a tag, and without secrets."
---

# Release

## When to use

Use this skill when gate-check has passed and a version is ready to ship.

## Steps

1. Confirm gate-check passed on the release commit.
2. Write the changelog from the commits. Do not include secret values.
3. Tag the release commit. Do not put credentials in the tag message.
4. Leave registrar, host, and email accounts to Venkat. Do not create those accounts or read their passwords.

## Done when

The tag exists, the changelog matches the commits, and no secret was written into the release notes.
