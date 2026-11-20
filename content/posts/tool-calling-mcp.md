---
title: Tool calling and MCP: Model Context Protocol explained
date: 2026-12-15
tags: tools, mcp
summary: How tool calling shapes an agent loop, and what MCP changes about tool surfaces.
draft: true
series: Foundations
series_total: 3
series_part: 3
---

# Tool calling and MCP: Model Context Protocol explained

Tool calling is how an agent leaves the chat transcript and touches systems. MCP (Model Context Protocol) is one way to describe and expose those tools with a shared contract.

## Tool calling in the loop

The model chooses a tool and arguments. The runtime executes the call, returns an observation, and the loop continues.

## What MCP adds

A protocol for listing tools, calling them, and returning results without inventing a one-off adapter for every host.

## What this draft is not

This file is a staging draft for review. It is not approved for publication.
