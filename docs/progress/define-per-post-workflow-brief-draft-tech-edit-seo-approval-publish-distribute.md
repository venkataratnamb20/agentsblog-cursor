# Define Per Post Workflow Brief Draft Tech Edit SEO Approval Publish Distribute

## Status

Status: In progress

## Evidence

- RED: `python -m unittest tests.unit.test_per_post_workflow -v` — 4 failures (missing `docs/editorial/per-post-workflow.md`).
- GREEN: same command — 4 passed after adding the workflow doc.
- Artifact: [docs/editorial/per-post-workflow.md](../editorial/per-post-workflow.md)
- Tests: [tests/unit/test_per_post_workflow.py](../../tests/unit/test_per_post_workflow.py)
- Stage order with Agent Owners: Brief (Product Strategist) → Draft (Technical Writer) → Tech edit (Technical Editor) → SEO (SEO & Analytics) → Approval (Venkat) → Publish (DevOps & SRE) → Distribute (Growth & Community).
- Publish and Distribute require Venkat's approval; drafts stay unpublished until Publish is approved.
- Hand-off fields: Artifact link, Summary, Open questions (operating-model).

## Remaining

- Venkat has not approved closing this task.
- Exit criteria are not met.
- Named reviewer has not reviewed this change.
- No commit, no publish, no accounts created.
