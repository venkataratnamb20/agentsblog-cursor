# Topic backlog

Scored candidate posts for Agents Blog. This file is a planning artifact.
Topics in this backlog are **not approved for publication**. They are
candidates only. Drafting and publishing still require Venkat's explicit
approval.

Audience: AI engineers, researchers, and tech leads who design, build,
evaluate, or lead agent systems.

## Scoring

| Dimension | Scale | Meaning |
| --- | --- | --- |
| Reader value | 1–5 | How useful the post is to the named audience (5 = must-read for most readers) |
| Effort | 1–5 | Cost to research, draft, and edit to blog quality (5 = heavy research or long series piece) |

**Priority rule:** `priority = reader value / effort`

Higher priority is better for the next draft pick. Prefer lower effort when
two topics share the same priority. Scores are product judgment, not
measurements.

## Backlog

| Topic | Pillar | Reader value | Effort | Priority | Notes |
| --- | --- | --- | --- | --- | --- |
| What is an AI agent? Agents vs workflows vs chatbots | Foundations | 5 | 2 | 2.5 | Progress: post-1; opens the Foundations series |
| Anatomy of an agent: LLM, tools, memory, the ReAct loop | Foundations | 5 | 3 | 1.67 | Progress: post-2 |
| Tool calling and MCP explained | Building | 5 | 3 | 1.67 | Progress: post-3 |
| Guardrails, safety, and human-in-the-loop for agents | Safety | 5 | 3 | 1.67 | Progress: post-9 |
| Agent memory: short-term, long-term, retrieval | Building | 4 | 3 | 1.33 | Progress: post-4; Memory series |
| Observability: debugging agents in production (tracing) | Operations | 4 | 3 | 1.33 | Progress: idea-observability-… |
| Cost and latency optimisation for production agents | Operations | 4 | 3 | 1.33 | Progress: idea-cost-latency-… |
| Agentic RAG vs classic RAG | Building | 4 | 3 | 1.33 | Progress: idea-agentic-rag-… |
| Evaluating agents: benchmarks, evals, LLM-as-judge | Evaluation | 5 | 4 | 1.25 | Progress: post-8; Judging agents series |
| Building stateful agents with LangGraph | Building | 4 | 4 | 1.0 | Progress: post-5 |
| Multi-agent patterns: supervisor, swarm, hierarchical | Building | 4 | 4 | 1.0 | Progress: post-6 |
| Computer-use and browser agents: how they work and fail | Building | 4 | 4 | 1.0 | Progress: idea-computer-use-… |
| Deep agents: planning, sub-agents, file systems | Building | 4 | 5 | 0.8 | Progress: post-7 |
| Agent-to-agent protocols (A2A) and interoperability | Building | 3 | 4 | 0.75 | Progress: idea-agent-to-agent-… |

## How to use

1. Sort by Priority descending (already ordered above).
2. Map the pick to its content pillar in `docs/product/content-pillars.md`.
3. Hand an approved brief to the PM orchestrator before any draft is written.
4. Do not publish from this list without Venkat's approval.

## Out of scope here

- Full post drafts
- Publish dates or calendar slots
- Research roundups and deploy/smoke posts (parked until the core pillars have drafts)
