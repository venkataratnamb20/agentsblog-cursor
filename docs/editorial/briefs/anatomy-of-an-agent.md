# Brief: Anatomy of an agent: LLM, tools, memory, the ReAct loop

Planning artifact only. This brief is **not published** and is **not
approved for publication**. Venkat must approve Publish before any public
release. No draft prose belongs in this file.

## Contract

| Field | Value |
| --- | --- |
| Title | Anatomy of an agent: LLM, tools, memory, the ReAct loop |
| Slug | `anatomy-of-an-agent` |
| Pillar | Foundations |
| Series | Foundations (post 2 of the opening sequence after agents vs workflows) |
| Calendar | Week 2 (8–14 December 2026) in `docs/editorial/calendar-2026-q1.md` |
| Progress | `docs/progress/post-2-anatomy-of-an-agent-llm-tools-memory-the-react-loop.md` |

## Audience

AI engineers, researchers, and tech leads who design, build, evaluate, or
lead work on agent systems. Readers already know what an LLM is; they need
a practical map of the moving parts inside one agent run.

## Promise

After reading, the reader can name the four parts of a typical agent run
and predict how the failure mode changes when one part is missing or weak.

## Claim

An agent run combines a model, tools, short-term memory/state, and a
ReAct-style reason-act loop; missing one piece changes the failure mode.

## Why this post now

Post 1 separates agents from workflows and chatbots. Post 2 opens the
box: what actually loops. Later Building posts (tools/MCP, memory,
LangGraph) go deep on one piece; this Foundations piece keeps the whole
loop in view.

## Outline (headings only — no draft)

1. One agent run, four parts
2. The model: what it decides vs what it cannot see
3. Tools: actions with side effects and contracts
4. Short-term memory / state: what the loop carries forward
5. The ReAct loop: reason → act → observe → repeat
6. Failure modes when a piece is missing or thin
7. What this post does not cover (long-term memory, multi-agent, evals)

## Success signal

A tech lead can sketch the four parts on a whiteboard and give one
concrete failure example for a weak model, missing tools, no state, or
no observe step — without treating ReAct as a product brand.

## Out of scope for this brief wave

- Full draft under `content/`
- Research pack expansion beyond public citeables later
- SEO metadata pass
- Publish or distribute

## Approval

Publication is not approved. Venkat has not approved Publish for this
post. A green PR is not Publish approval.
