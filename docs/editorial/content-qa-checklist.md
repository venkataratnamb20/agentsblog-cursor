# Content QA checklist

Use this checklist on every Agents Blog post before offering it for Venkat
publish approval. A green pull request is not publish approval. Leave
`draft: true` until Venkat says yes.

Audience: AI engineers, researchers, and tech leads.

## Accuracy

- [ ] Claim accuracy: every non-obvious claim is true and tied to evidence.
- [ ] Sources cited are public, named, and match what the draft asserts.
- [ ] Outdated or contested claims are labeled as such, or removed.

## Structure

- [ ] The post treats one idea carefully, not a news roundup.
- [ ] Structure uses clear headings a skim reader can follow.
- [ ] The opening states the problem and who it is for.

## Voice

- [ ] Voice fits AI engineers, researchers, and tech leads: specific,
  practical, and free of hype.
- [ ] Jargon earns its place; undefined buzzwords are cut or defined once.

## Secrets

- [ ] The draft has no secrets, credentials, tokens, private keys, or `.env`
  values.
- [ ] Examples use placeholders, never real credentials.

## SEO basics

- [ ] Front matter includes a title.
- [ ] Front matter includes a description (summary).
- [ ] The post has a stable slug suitable for `/posts/{slug}.html`.

## Draft vs publish

- [ ] Front matter keeps `draft: true` until Venkat approves publish.
- [ ] The draft is not offered for syndication, social posting, or a live
  deploy until that approval is recorded.

## Code samples

- [ ] All code samples are correct for the stated stack and version, or are
  marked unverified.
- [ ] Unverified snippets are not presented as copy-paste production advice.

## Sign-off

Editor: ________  Date: ________

Only after every box above is checked may the post be offered for Venkat
publish approval.
