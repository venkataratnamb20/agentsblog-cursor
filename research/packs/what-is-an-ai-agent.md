# Research pack: What is an AI agent?

**Slug:** `what-is-an-ai-agent`

**Post title:** What is an AI agent? Agents vs workflows vs chatbots

**Status of these notes:** Research notes only. This file is **not a published post** and is not a draft post for `content/`.

**Pack date:** 2026-11-20

**Overall confidence:** Medium-high for the agent-vs-workflow distinction (multiple independent lab/docs sources agree). Medium for the chatbot boundary (industry use of “chatbot” is looser; few sources define it as a crisp technical term opposite “agent”).

## Claim under study

An **agent** is a goal-directed loop that chooses tools; a **workflow** is a fixed graph; a **chatbot** is turn-based chat without tool autonomy.

## Sources

### 1. ReAct: Synergizing Reasoning and Acting in Language Models

- **Title:** ReAct: Synergizing Reasoning and Acting in Language Models
- **Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **URL:** https://arxiv.org/abs/2210.03629
- **Bibliographic cite:** Yao et al., arXiv:2210.03629 (2022); ICLR 2023 camera-ready as arXiv:2210.03629v3
- **Accessed:** 2026-11-20
- **Confidence:** High (canonical public preprint; project page https://react-lm.github.io/)
- **Supports:** Interleaved reasoning traces and **actions** against an environment or API (e.g. Wikipedia), forming a goal-directed decide–act–observe loop rather than a single chat reply.

### 2. Building effective agents (Anthropic)

- **Title:** Building effective agents
- **Authors / org:** Anthropic (Erik S., Barry Zhang acknowledged)
- **URL:** https://www.anthropic.com/engineering/building-effective-agents
- **Alternate listing:** https://www.anthropic.com/research/building-effective-agents (same article family in public indexes)
- **Date on page:** 2024-12-19
- **Accessed:** 2026-11-20
- **Confidence:** High (primary lab engineering post; live fetch succeeded on the engineering URL)
- **Supports:** Explicit split: **workflows** = LLMs and tools on **predefined code paths**; **agents** = LLMs that **dynamically** direct process and tool use; agents described as “LLMs using tools based on environmental feedback in a **loop**.”

### 3. Workflows and agents (LangGraph docs)

- **Title:** Workflows and agents
- **Org:** LangChain / LangGraph documentation
- **URL:** https://docs.langchain.com/oss/python/langgraph/workflows-agents
- **Related:** Graph API overview — https://docs.langchain.com/oss/python/langgraph/graph-api (workflows as graphs of state, nodes, and edges)
- **Accessed:** 2026-11-20
- **Confidence:** High for “workflow as predetermined / graph-shaped control flow” in current LangGraph docs; medium as a vendor doc (framework-specific vocabulary).
- **Supports:** Workflows have **predetermined code paths** and ordered node/edge graphs; agents are dynamic, define their own processes and tool usage, and are shown as LLM ↔ tool **feedback loops**.

### 4. Function calling (OpenAI platform docs)

- **Title:** Function calling
- **Org:** OpenAI
- **URL:** https://platform.openai.com/docs/guides/function-calling
- **Related cookbook (turn-based chat primitives):** https://developers.openai.com/cookbook/examples/how_to_call_functions_with_chat_models
- **Accessed:** 2026-11-20
- **Confidence:** High for the documented tool-call **multi-step conversation** pattern; medium for labeling the no-tools path as “chatbot” (OpenAI does not use that word as a formal type).
- **Supports:** Plain chat completions are **turn-based** model ↔ user messages. Tool/function calling is a separate application-managed loop (model may emit `tool_calls`; the app executes tools and continues). Without that autonomy loop, the system stays conversational chat.

## Claim mapping

| Claim part | Working definition for this pack | Primary sources | How the source maps |
| --- | --- | --- | --- |
| **Agent** | Goal-directed **loop** that **chooses** tools (and may update plans from observations) | ReAct (#1); Anthropic (#2); LangGraph agents section (#3) | ReAct: interleaved reason + act + observe toward a task. Anthropic: LLM dynamically directs tool usage in a loop. LangGraph: agent as continuous LLM–tool feedback loop. |
| **Workflow** | **Fixed** / predetermined **graph** or code path (nodes and edges decided ahead of time) | Anthropic (#2); LangGraph workflows + Graph API (#3) | Anthropic: orchestrated through predefined code paths (prompt chaining, routing, etc.). LangGraph: predetermined paths; Graph API models workflows as state/nodes/edges. |
| **Chatbot** | **Turn-based chat** without tool **autonomy** (no app-driven tool loop deciding next actions) | OpenAI function calling / chat cookbook (#4); contrast with Anthropic agent loop (#2) | OpenAI: message turns are the default; tools require an explicit multi-step app loop. Absent that loop, behavior is conversational chat. Anthropic treats plain LLM chat / single-call patterns as simpler than agentic systems. |

### Mapping caveats

- Anthropic groups both workflows and agents under “agentic systems”; the post’s **architectural** distinction still matches this pack’s agent vs workflow claim.
- “Chatbot” is a product term. Prefer contrasting **turn-based chat UI / Completions without a tool loop** vs **tool-autonomous loops**, rather than implying every branded chatbot cannot call tools.
- Hybrid products (support bots with tools) sit between chatbot UX and agent loops; call that out in the eventual draft.

## Open questions

1. Should the post treat “agentic workflow” (Anthropic’s umbrella) as a third term, or stick to the three-way agent / workflow / chatbot split for readers?
2. Where do RAG-only assistants land—workflow, chatbot with retrieval, or neither?
3. How strictly should “fixed graph” allow conditional edges (LangGraph) without collapsing into “agent”?
4. Is there a standards-body or RFC-style definition of “AI agent,” or only lab/blog/vendor usage?
5. Which single diagram best teaches the three-way split without overselling autonomy?

## Notes for Technical Writer / Editor

- Lead with Anthropic’s workflow vs agent sentence pair; use ReAct for the academic “loop that acts” picture; use LangGraph for the “fixed graph” metaphor; use OpenAI docs for chat turns vs tool loops.
- Do not invent DOIs; prefer the arXiv id and live URLs above.
- Keep draft claims scoped to architecture, not marketing labels.
- These notes are research notes only — **not a published post**.
