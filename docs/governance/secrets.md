# Secrets policy

Agents Blog stores zero secrets in the git repository. That includes worktrees, skills, agent definitions, docs, tests, and any future CI configuration. Do not commit tokens, passwords, private keys, `.env` files, or copies of production configuration.

## Secret store

The secret store lives outside the repository. Use a password manager or the host's secret manager. Agents read only the values their role needs, at runtime, from that store. The repository records secret names and ownership, never the values.

## Scoped tokens

Each agent gets its own token. Scope that token to the minimum access the role needs, and do not reuse one token across agents. Reviewer and auditor agents do not receive write credentials or access to the secret store. A token that is broader than the role is a defect.

## Rotation schedule

Rotate every scoped token on a fixed schedule:

- Routine rotation every 90 days.
- Immediate rotation when a token may have been exposed, when an agent's access changes, or when a person who could use the token leaves.

Record the rotation date and the token name in the secret store. Do not record token values, or even partial values, in the repo.

## Scanning

Pre-commit secret scanning and CI secret scanning will be added when CI exists. Until those checks exist, authors review their own diffs and reject any change that introduces a secret. A scan finding is reported by file and secret name only.

## Account ownership

Venkat creates the registrar, host, and email accounts. Agents do not create those accounts, do not reset their passwords, and do not copy the passwords into the repository or into chat.
