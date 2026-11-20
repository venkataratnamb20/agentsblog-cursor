# Content pillars

Taxonomy for Agents Blog posts. Planning only — nothing here is published.
Audience matches `docs/product/topic-backlog.md`: AI engineers, researchers,
and tech leads who design, build, evaluate, or lead agent systems.

Pillar names on backlog rows and calendar slots must match this file.

## Pillars

| Pillar | Promise | Typical backlog / calendar fit |
| --- | --- | --- |
| Foundations | What an agent is, how it differs from a workflow or chatbot, and the core loop | Opening posts; anatomy; optional research roundups |
| Building | Tools, memory, state, multi-agent patterns, and the loop that calls them | Tool calling / MCP; memory; LangGraph; multi-agent; deep agents; RAG; computer-use; protocols |
| Evaluation | Benchmarks, evals, and how to judge an agent run | Evaluating agents; LLM-as-judge |
| Safety | Guardrails and human approval before an action | Guardrails; human-in-the-loop |
| Operations | Cost, latency, tracing, and failure in production | Observability / tracing; cost and latency |

Reject any topic that would require publishing secrets or private customer
data. Those never get a pillar assignment.

## Tags

Tags name a technique or concern inside a pillar. A post may carry more than
one. Starter set, aligned to the scored backlog:

| Tag | Primary pillar | Use when the post centres on |
| --- | --- | --- |
| agents | Foundations | Definitions, anatomy, agent vs workflow vs chatbot |
| tools | Building | Tool calling, tool design, tool failure modes |
| mcp | Building | Model Context Protocol and MCP-shaped tool surfaces |
| memory | Building | Short-term context, long-term store, retrieval |
| state | Building | Graphs, checkpoints, durable agent state |
| multi-agent | Building | Supervisor, swarm, hierarchical, and related patterns |
| rag | Building | Retrieval-augmented generation in an agent loop |
| planning | Building | Plans, sub-agents, long-horizon / deep agents |
| computer-use | Building | Browser and computer-use agents |
| protocols | Building | Agent-to-agent and interoperability protocols |
| evals | Evaluation | Benchmarks, harnesses, LLM-as-judge |
| guardrails | Safety | Policy, allowlists, human-in-the-loop gates |
| observability | Operations | Tracing, debugging production runs |
| cost | Operations | Token spend, latency, production optimisation |

The local builder turns a published tag into a page at `/tags/{slug}.html`.
The slug is lowercase, spaces become hyphens, and other characters are
dropped. Drafts do not create a tag page.

## Series

A series is an ordered set of posts that usually stay inside one pillar.
Proposed series (no posts written or published yet):

| Series | Pillar | Order (candidate topics) |
| --- | --- | --- |
| Agent basics | Foundations | What an agent is → anatomy of the loop |
| Memory | Building | Short-term context → long-term / retrieval |
| Judging agents | Evaluation | Benchmarks and evals → harness / LLM-as-judge depth |
| Running in production | Operations | Observability / tracing → cost and latency |

Tool calling / MCP, LangGraph, multi-agent, and deep-agent posts sit under
**Building** as standalone picks unless a later brief opens a dedicated
series. Research roundups stay under **Foundations** as orientation, not as
a numbered series.

Publishing any post in a series still requires Venkat's approval.

## How to use

1. Pick a topic from `docs/product/topic-backlog.md` (priority order).
2. Confirm its pillar and tags against this file.
3. If it belongs in a series, place it in the series order above.
4. Hand an approved brief to the PM orchestrator before drafting.
5. Calendar slots in `docs/editorial/calendar-2026-q1.md` reuse these
   pillar names; do not invent a sixth pillar for a one-off topic.
