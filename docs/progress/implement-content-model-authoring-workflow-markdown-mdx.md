# Implement Content Model Authoring Workflow Markdown MDX

## Status

Status: Done

## Evidence

- `src/agentsblog/posts.py` — front matter, series fields, title required, image alt validation
- `src/agentsblog/markdown.py` — headings and paragraphs subset
- `tests/unit/test_content_validation.py`
- `tests/unit/test_posts.py`

MDX is out of scope for the Python stdlib builder (ADR 0002). Markdown +
front matter is the authoring workflow for Stage 3.

## Remaining

none
