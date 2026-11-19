# Content pillars

This is a taxonomy for future posts. It does not publish any post.

## Pillars

| Pillar | What a reader gets |
| --- | --- |
| Foundations | What an agent is, and how it differs from a workflow or a chatbot |
| Building | Tools, memory, state, and the loop that calls them |
| Evaluation | Benchmarks, evals, and how to judge an agent run |
| Safety | Guardrails and human approval before an action |
| Operations | Cost, latency, tracing, and failure in production |

## Tags

Tags name a technique inside a pillar. A post may carry more than one. Proposed starter tags:

- agents
- tools
- memory
- evals
- guardrails
- multi-agent

The local builder turns a published tag into a page at `/tags/{slug}.html`. The slug is lowercase, spaces become hyphens, and other characters are dropped. Drafts do not create a tag page.

## Series

A series is an ordered set of posts inside one pillar. Proposed series, with no posts written yet:

| Series | Pillar | Order |
| --- | --- | --- |
| Agent basics | Foundations | What an agent is, then the loop, then tools |
| Memory | Building | Short-term context, then retrieval |
| Judging agents | Evaluation | Benchmarks, then an eval harness |

Publishing any post in a series still requires Venkat's approval.
