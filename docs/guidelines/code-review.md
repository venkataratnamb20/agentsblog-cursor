# Code review checklist

This is the operating gate for every pull request. The named reviewer
applies it before approving. The named reviewer is not the author. The
author may not approve their own diff.

Apply every item. Request changes when any item fails.

## Checklist

- [ ] Behavior changes follow TDD: a failing test first, then the
  smallest change that makes it pass. Docs-only diffs name which claims
  a person can check.
- [ ] `python -m unittest discover -s tests -v` passes, or
  `.\make.ps1 test` passes.
- [ ] The diff contains no secrets, credentials, tokens, private keys,
  or `.env` files.
- [ ] The diff does not include a production deploy, a DNS change, or a
  publish action without Venkat approval. `release` does not deploy.
- [ ] Drafts stay unpublished. A `draft: true` post stays out of the
  index, the feed, the sitemap, and search.
