# Approval gates

Some actions need Venkat's approval before they happen. A pull request, a
green check, or a task description is not that approval. Wait for an explicit
yes in the same thread as the request.

Local edits, tests, and drafts inside this repository do not need approval.
The actions below do.

## Actions that need approval

| Action | Examples that must wait |
| --- | --- |
| Spending money | Paid APIs, domains, hosting, ads, SaaS seats, invoices |
| Creating accounts | New users, service accounts, OAuth apps, cloud projects, community accounts |
| Production deploys | Shipping `main` or a release to the live site, including roll-forward |
| DNS changes | Records, nameservers, redirects, and domain verification |
| Publishing posts | Making a draft public on the blog or syndicating the full post |
| Posting on social or communities | Posts, comments, or replies on social networks, forums, or communities |

Ask once per action. A yes for one item does not cover the next item.

## How to ask

Send a short request and stop:

1. **Action.** One sentence on what will run, and where.
2. **Impact.** What changes for readers, cost, or access if this proceeds.
3. **Recovery.** How to undo it, or say that it cannot be undone.
4. **Ask.** End with a clear question: "Approve? (yes / no)".

Do not start the action while waiting. Do not chain a second gated action
into the same request.

## Guardrails

These apply to every session, including work that does not need an approval.

- **Least privilege.** Use the narrowest account, role, and scope that can do
  the task. Do not reuse an admin credential for routine work. Drop access
  when the task is finished.
- **No secrets in prompts or the repo.** Do not put tokens, passwords, keys,
  or connection strings in chat, issues, commits, docs, or `.env` files in
  git. Ask a person to set secrets outside the repository.
- **Log actions.** After an approved action, record who approved it, what ran,
  when it finished, the outcome, and a link to the artifact. Log the fact of
  the action. Do not log secret values.

If an approval is refused or unanswered, leave the work unstarted and note
that in the task hand-off.
