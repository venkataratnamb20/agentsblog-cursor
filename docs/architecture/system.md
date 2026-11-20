# System architecture

Local preview only. Staging and production hosts are undecided and wait on Venkat's approval. The builder choice is recorded in [ADR 0002](../adr/0002-python-stdlib-site.md).

## Pipeline

```text
content/posts/*.md  -->  agentsblog.build  -->  build/
                              |
                         preview on 127.0.0.1:8000
```

`.\make.ps1 build` compiles `scripts` and `tests`, then runs `python -m agentsblog.build`. Drafts never enter `build/`.

## Modules

| Module | Role |
| --- | --- |
| `posts` | Load markdown and front matter |
| `markdown` | Headings and paragraphs to HTML |
| `render` | Shared document chrome and pages |
| `search` | In-memory match of title, summary, tags |
| `feed` | RSS 2.0 |
| `seo` | robots, sitemap, canonical, Open Graph |
| `legal` | Draft policy pages |
| `tags` | Group published posts by tag slug |
| `preview` | Loopback static server |
| `build` | Orchestrate the write to `build/` |

## Content model

A post is a markdown file with YAML-like `key: value` front matter between `---` fences. Required field: `title`. Optional: `date`, `tags`, `summary`, `draft`. The slug is the filename stem. `draft: true` keeps the post out of every public file.

## Environments

| Environment | Status |
| --- | --- |
| Local preview | Exists. Origin defaults to `http://127.0.0.1:8000`. |
| Staging | Not provisioned. Needs a host decision and approval. |
| Production | Not provisioned. DNS and deploy are approval gates. |

No secret values live in the repository. Account credentials for a future host stay outside git.
