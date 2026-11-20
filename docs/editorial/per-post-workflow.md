# Per-post workflow

Stage order for every Agents Blog post. Do not skip a stage. Do not
publish or distribute without Venkat's approval. Drafts stay unpublished
until Venkat approves Publish.

Roles come from [docs/team.md](../team.md). Hand-offs follow
[docs/governance/operating-model.md](../governance/operating-model.md).
Publishing and social posting are approval gates in
[docs/governance/approval-gates.md](../governance/approval-gates.md).

## Stages

### Brief

- **Agent Owner:** Product Strategist
- **Outcome:** An approved brief naming audience, claim, pillar, and
  target slug. No draft prose yet.

### Draft

- **Agent Owner:** Technical Writer
- **Outcome:** A review-ready draft in the repository from the approved
  brief (see the `new-post` skill). The draft stays unpublished.

### Tech edit

- **Agent Owner:** Technical Editor
- **Outcome:** Accept, revise, or reject against
  [content-qa-checklist.md](content-qa-checklist.md). Nothing moves to
  SEO until the editor accepts the draft.

### SEO

- **Agent Owner:** SEO & Analytics
- **Outcome:** `seo-audit` findings applied or recorded. Metadata and
  discoverability notes ready for Approval. The draft remains unpublished.

### Approval

- **Agent Owner:** Venkat
- **Outcome:** Explicit yes or no for making the post public and for any
  related social or community post. A pull request or green check is not
  this approval. Ask once per gated action using the approval-gates form.

### Publish

- **Agent Owner:** DevOps & SRE
- **Outcome:** The accepted post is made public on the blog only after
  Venkat's approval for Publish. Until that yes, drafts stay unpublished.

### Distribute

- **Agent Owner:** Growth & Community
- **Outcome:** Distribution and community posts only after Venkat's
  approval for posting on social networks or communities. Publish
  approval does not cover Distribute; ask again for social posting.

## Hand-off

At the end of each stage, leave all three fields from the operating-model
hand-off protocol:

1. **Artifact link.** Path, commit, or pull request for the stage output.
2. **Summary.** What changed and what was verified.
3. **Open questions.** Decisions still needed, each with a default; or
   "none".

A hand-off without an artifact link is incomplete. Do not retell the
session log.
