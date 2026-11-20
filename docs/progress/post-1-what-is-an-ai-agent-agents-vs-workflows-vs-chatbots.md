# Post 1 What Is An AI Agent Agents Vs Workflows Vs Chatbots

## Status

Status: In progress

## Evidence

- RED: `python -m unittest tests.unit.test_brief_post1 -v` failed with missing `docs/editorial/briefs/what-is-an-ai-agent.md`.
- GREEN: same command OK after adding the brief (title, slug `what-is-an-ai-agent`, pillar Foundations, audience, claim; not published / not approved for publication).
- Artifacts: `docs/editorial/briefs/what-is-an-ai-agent.md`, `tests/unit/test_brief_post1.py`.
- Brief only. No draft prose. No commit. No publish.
- RED: `python -m unittest tests.unit.test_draft_post1 -v` failed (missing `content/posts/what-is-an-ai-agent.md`).
- GREEN: same command OK after adding the review-ready draft (`draft: true`; title/summary/claim match shared contract; build omits draft from index).
- Artifacts: `content/posts/what-is-an-ai-agent.md`, `tests/unit/test_draft_post1.py`.
- Draft is review-ready only. Status not Done. No commit. No publish.
- RED: `python -m unittest tests.unit.test_research_pack_post1 -v` failed (missing `research/packs/what-is-an-ai-agent.md`).
- GREEN: same command OK after the research pack (slug, ≥3 public sources, claim mapping, open questions).
- Artifact: `research/packs/what-is-an-ai-agent.md`.

## Remaining

- Venkat has not approved closing this task or publishing the post.
- Exit criteria are not met.
- Tech edit, SEO, approval, publish, and distribute stages are still ahead.
