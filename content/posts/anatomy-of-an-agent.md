---
title: Anatomy of an agent: LLM, tools, memory, the ReAct loop
date: 2026-12-08
tags: agents
summary: Name the four parts of a typical agent run and how failure modes shift when one part is weak.
draft: true
series: Foundations
series_part: 2
series_total: 3
---

# Anatomy of an agent: LLM, tools, memory, the ReAct loop

An agent run is not a single prompt. It is a loop that keeps a goal, calls tools, and folds observations back into state until it stops. This draft maps four parts: the LLM, tools, memory, and the ReAct-style control loop.

## LLM

The model proposes the next step. It does not move the world by itself.

## Tools

Tools are the side effects. Search, code execution, tickets, and browsers change what the run can observe and do.

## Memory

Short-term context and longer stores decide what the model can see on the next step.

## The loop

Observe, reason, act, repeat. Stopping rules and budgets matter as much as the prompt.

This draft is not approved for publication.
