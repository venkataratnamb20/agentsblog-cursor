---
title: What is an AI agent? Agents vs workflows vs chatbots
date: 2026-12-01
tags: agents
summary: An agent is a goal-directed loop that chooses tools; a workflow is a fixed graph; a chatbot is turn-based chat without tool autonomy.
draft: true
---

# What is an AI agent? Agents vs workflows vs chatbots

Teams ship “agents” that are really chat UIs, or “chatbots” that secretly run fixed pipelines. The label rarely tells you what the system is allowed to decide. This post treats one distinction carefully: **an agent is a goal-directed loop that chooses tools; a workflow is a fixed graph; a chatbot is turn-based chat without tool autonomy.**

If you design, evaluate, or buy agent systems, that three-way split is enough to ask better questions in reviews and incident postmortems.

## Why the labels blur

Product language collapses three control patterns into one word. Marketing wants “agent.” Engineering inherits a stack that may be a prompt with a session history, a DAG of API calls, or a planner that selects tools at runtime. When those patterns fail differently, a shared name hides the failure mode.

Use the control question, not the brand name: *Who chooses the next action, and when?*

## Agent: a goal-directed loop that chooses tools

An agent keeps a goal (or a goal state) and repeatedly decides what to do next. Between steps it may call tools—search, code execution, ticketing APIs, browsers—then fold the observations back into its state and continue until it stops, asks a human, or hits a budget.

The distinctive property is **tool choice under a goal**. The path is not fully known when the run starts. Branching, retries, and tool selection are part of the runtime policy, not only of the authoring-time graph.

Practical signals you are looking at an agent:

- The system can pick among tools (or tool arguments) based on intermediate results.
- Stopping criteria are about the goal or a budget, not only “end of script.”
- Evaluation cares about trajectory quality: wrong tool, thrashing, or unsafe side effects—not only final string match.

Agents are not magic autonomy. They still need scopes, allowlists, human gates for irreversible actions, and observability for every tool call. The point of the word “agent” here is the control loop, not unbounded trust.

## Workflow: a fixed graph

A workflow is a predetermined graph of steps. Edges and node responsibilities are decided before the run. A step may call an LLM—to classify, extract, or draft—but the *orchestration* does not invent new branches at runtime beyond what the graph already encodes (including explicit conditional edges you authored).

Practical signals you are looking at a workflow:

- The happy path and the main failure paths are enumerable in a diagram or config.
- Adding a new capability usually means editing the graph, not expanding a tool menu the model may invent mid-run.
- Debugging starts at a named node and a known input contract.

Workflows are often the right default. They are easier to test, rate-limit, and certify. Calling every LLM step an “agent” makes reviews harder without buying more capability.

## Chatbot: turn-based chat without tool autonomy

A chatbot is a turn-based conversational interface: user message in, model (or scripted) reply out. It may keep memory across turns. It does not, on its own, choose and execute tools as part of pursuing a goal across a multi-step loop.

Some chatbots sit in front of tools—a “search this doc” button, or a server that always retrieves the same index. That is still not agent autonomy if the system never decides *whether* and *which* tool to call as policy. Retrieval bolted to every turn is a fixed step, closer to a tiny workflow than to an agent.

Practical signals you are looking at a chatbot:

- The unit of progress is the conversational turn, not a goal state machine.
- Side effects, if any, are user-initiated or hard-wired, not selected by a planner.
- Success metrics are reply quality, latency, and safety of text—not tool-trajectory correctness.

## How to choose (and how to argue in a design review)

Pick the weakest control pattern that meets the job:

1. **Chatbot** when the product is conversation, advice, or drafting, and side effects stay with the user or a separate system.
2. **Workflow** when the steps are known, compliance needs a fixed path, or you must bound cost and blast radius tightly.
3. **Agent** when intermediate observation must change which tools run, and you can afford evaluation, budgets, and permission design for that loop.

In a design review, refuse the label and ask for the contract: goal representation, tool set, who selects the next action, stop conditions, and what is logged. If the answer is “the model decides among tools until the goal is met,” you are in agent territory. If the answer is a diagram with named stages, you are in workflow territory. If the answer is “it replies in the thread,” you are in chatbot territory—even if the deck says “agent.”

## What this post is not claiming

This is a working taxonomy for builders, not a settled academic definition. Research papers use “agent” for reinforcement learners, multi-agent debate, and tool-using LLMs with different formalisms. Product teams will keep stretching the word. The useful habit is to map any system back to loop, graph, or turn—and to design tests for the control pattern you actually shipped.
