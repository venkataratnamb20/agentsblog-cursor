"""Tests for the parent-task progress record.

The repository root is the parent of ``tests`` (``parents[2]`` of this
file). Progress files are the record of work, not a claim that the
product site exists.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRESS_DIR = REPO_ROOT / "docs" / "progress"

# Slugs are the parent-task names: lowercase, spaces as hyphens,
# punctuation dropped. These tasks have a document or script on disk.
# Venkat has not approved them, and their exit criteria are not met.
IN_PROGRESS: dict[str, tuple[str, ...]] = {
    "git-branching-model-pr-workflow-main-develop-feature-release-hotfix": (
        "docs/guidelines/git-workflow.md",
    ),
    "code-maintainability-guidelines-clean-code-solid-tdd-bdd-data-structures-algorithms": (
        "docs/guidelines/code-quality.md",
    ),
    "create-missing-skills-commands-workflows-subagents-for-every-agent-role": (
        ".agents/skills",
        ".claude/agents",
    ),
    "cross-platform-task-runner-makefile-with-windows-support": (
        "Makefile",
        "make.ps1",
    ),
    "audit-ai-team-harness-capabilities-claude-code-codex-cursor-antigravity": (
        "docs/agents/capability-matrix.md",
    ),
    "write-project-guidelines-agentsmd-single-source-of-truth-claudemd-tool-adapters": (
        "AGENTS.md",
        "CLAUDE.md",
        ".cursor/rules/agents-blog.mdc",
    ),
    "project-scaffold-folder-structure-docs-research-tests-tooling": (
        "src",
        "content",
        "tests",
        "docs",
        "research",
        "scripts",
        "tests/unit/test_scaffold.py",
    ),
    "define-agent-team-roster-roles-raci": ("docs/team.md",),
    "define-human-in-the-loop-approval-gates-agent-guardrails": (
        "docs/governance/approval-gates.md",
    ),
    "set-up-secrets-access-management-for-agents": (
        "docs/governance/secrets.md",
    ),
    "define-agent-operating-model-task-template-handoffs-definition-of-done": (
        "docs/governance/operating-model.md",
    ),
    "set-up-cicd-pipeline-with-preview-deploys-rollback": (
        ".github/workflows/ci.yml",
        ".github/workflows/cd.yml",
    ),
    "select-tech-stack-hosting-services-adrs": (
        "docs/adr/0002-python-stdlib-site.md",
    ),
    "automated-test-suite-unit-integration-e2e-visual-regression": (
        "tests/unit",
        "tests/integration",
    ),
    "implement-content-model-authoring-workflow-markdown-mdx": (
        "src/agentsblog/posts.py",
        "src/agentsblog/markdown.py",
    ),
    "build-site-templates-components-responsive-dark-mode": (
        "src/agentsblog/build.py",
        "src/agentsblog/render.py",
    ),
    "integrate-newsletter-signup-double-opt-in-welcome-email-rss": (
        "src/agentsblog/feed.py",
    ),
    "site-search-404-error-pages": (
        "src/agentsblog/search.py",
        "src/agentsblog/render.py",
    ),
    "implement-technical-seo-metadata-open-graph-schemaorg-sitemap-robots-canonicals": (
        "src/agentsblog/seo.py",
    ),
    "legal-policy-pages-privacy-cookies-terms-licences-ai-assistance-disclosure": (
        "src/agentsblog/legal.py",
    ),
    "fortnightly-project-status-updates": (
        "docs/progress/fortnightly-project-status-updates.md",
    ),
    "define-test-strategy-quality-gates-code-review-standards": (
        "docs/testing/test-strategy.md",
    ),
}

NOT_STARTED: tuple[str, ...] = (
    "verify-harness-end-to-end-in-all-four-tools-smoke-test",
    "m0-agent-harness-team-governance-ready",
    "write-prd-problem-audience-features-scope-success-metrics",
    "define-content-pillars-topic-taxonomy-pillars-tags-series",
    "design-system-architecture-content-model-environments",
    "threat-model-security-requirements",
    "write-requirements-spec-functional-non-functional-srs",
    "m1-specifications-approved-prd-requirements-architecture-security-test-plans",
    "define-seo-analytics-kpi-kpm-tracking-spec",
    "information-architecture-sitemap-navigation-taxonomy",
    "wireframes-high-fidelity-ui-home-post-pillar-about-subscribe-404",
    "brand-identity-name-tagline-logo-colours-typography-cover-template",
    "design-system-accessibility-spec-wcag-22-aa",
    "m2-design-approved",
    "integrate-privacy-friendly-analytics-cookie-consent-uk-gdpr-pecr",
    "m3-feature-complete-on-staging",
    "provision-hosting-environments-staging-prod-domain-https",
    "production-readiness-review-go-no-go",
    "m4-quality-gates-passed-go-for-launch",
    "cross-browser-responsive-testing",
    "seo-audit",
    "security-vulnerability-checklist",
    "privacy-compliance-check",
    "accessibility-audit-wcag-22-aa",
    "code-review-every-pr-reviewed-against-the-checklist",
    "caching-cdn-configuration",
    "performance-testing-budgets-core-web-vitals",
    "backups-disaster-recovery",
    "production-deployment-dns-cutover",
    "post-deploy-smoke-tests-search-engine-submission",
    "m5-production-launch-blog-live-with-first-3-posts",
    "launch-communications-linkedin-x-first-newsletter",
    "monitoring-uptime-alerting-slos",
    "runbooks-deploy-rollback-incident-response",
    "idea-cost-latency-optimisation-for-production-agents",
    "set-up-reference-library-for-papers-notes-zotero-notion",
    "build-research-pipeline-arxiv-alerts-lab-blogs-github-trending-conference-papers",
    "post-2-anatomy-of-an-agent-llm-tools-memory-the-react-loop",
    "post-1-what-is-an-ai-agent-agents-vs-workflows-vs-chatbots",
    "define-per-post-workflow-brief-draft-tech-edit-seo-approval-publish-distribute",
    "post-10-research-roundup-1-notable-agent-papers-of-the-quarter",
    "create-topic-backlog-score-ideas-reader-value-x-effort",
    "m7-10-technically-verified-posts-published",
    "post-7-deep-agents-planning-sub-agents-file-systems-for-long-tasks",
    "post-9-guardrails-safety-human-in-the-loop-for-agents",
    "build-12-week-editorial-calendar-with-owners-per-stage-dec-2026-feb-2027",
    "idea-computer-use-browser-agents-how-they-work-and-where-they-fail",
    "idea-agentic-rag-vs-classic-rag",
    "post-4-agent-memory-short-term-long-term-retrieval",
    "post-8-evaluating-agents-benchmarks-evals-llm-as-judge",
    "post-3-tool-calling-mcp-model-context-protocol-explained",
    "editorial-content-qa-checklist-applies-to-every-post",
    "idea-observability-debugging-agents-in-production-tracing-langsmith",
    "idea-agent-to-agent-protocols-a2a-interoperability",
    "post-5-building-stateful-agents-with-langgraph",
    "post-6-multi-agent-patterns-supervisor-swarm-hierarchical",
    "repurpose-each-post-for-linkedin-x-thread-carousel",
    "newsletter-welcome-sequence-weekly-digest",
    "share-posts-in-communities-hn-reddit-langchain-forum-drafted-by-agent-posted-by-venkat",
    "m8-100-confirmed-newsletter-subscribers",
    "set-up-social-profiles-link-in-bio-linkedin-x",
    "subscriber-growth-experiments-ctas-lead-magnet-a-b-tests",
    "backlink-guest-post-outreach-plan",
    "hypercare-daily-monitoring-fixes-for-2-weeks-after-launch",
    "quarterly-security-review-access-audit",
    "m6-hypercare-complete-stable-in-production",
    "dependency-security-patching-cadence",
    "incident-response-postmortem-process",
    "monthly-maintenance-checklist",
    "monthly-kpi-kpm-review-backlog-re-prioritisation",
    "m9-q1-review-kpis-reader-feedback-roadmap-refresh",
    "kpi-kpm-dashboard-asana-dashboard-analytics",
    "agent-performance-retrospective-quality-rework-cycle-time",
)


def _task_slugs() -> tuple[str, ...]:
    """Return every parent-task slug, in-progress tasks first.

    Returns:
        The stable slug for each parent task, including M0.
    """
    return tuple(IN_PROGRESS) + NOT_STARTED


def _heading_names(text: str) -> list[str]:
    """Return ATX heading text with the hash marks removed.

    Args:
        text: Markdown source.

    Returns:
        Heading labels in document order.
    """
    names: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        names.append(stripped.lstrip("#").strip())
    return names


def _section(text: str, heading: str) -> str:
    """Return the body under one heading, stopping at the next heading.

    Args:
        text: Markdown source.
        heading: Heading label to collect, without hash marks.

    Returns:
        The stripped section body. Empty when the heading is absent.
    """
    collecting = False
    body: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            name = stripped.lstrip("#").strip()
            if collecting:
                break
            collecting = name == heading
            continue
        if collecting:
            body.append(line)
    return "\n".join(body).strip()


def _read(slug: str) -> str:
    """Read one task file as UTF-8 text.

    Args:
        slug: Parent-task slug, also the file stem.

    Returns:
        The file contents.
    """
    return (PROGRESS_DIR / f"{slug}.md").read_text(encoding="utf-8")


class TestProgressRecord(unittest.TestCase):
    """Verify the honest status of every parent task."""

    def test_parent_task_inventory_includes_m0(self) -> None:
        """Count 22 partial tasks and 73 not-started tasks, including M0.

        94 other parent tasks plus M0 is 95 task files, plus the index.
        """
        slugs = _task_slugs()
        self.assertEqual(len(IN_PROGRESS), 22)
        self.assertEqual(len(NOT_STARTED), 73)
        self.assertEqual(len(slugs), 95)
        self.assertEqual(len(set(slugs)), 95)
        self.assertIn("m0-agent-harness-team-governance-ready", NOT_STARTED)

    def test_readme_exists_and_names_the_three_statuses(self) -> None:
        """The index exists and names Not started, In progress, and Done.

        The opening states that the product site was not built and that
        only the stage 0A and 0B harness documents were started.
        """
        readme = PROGRESS_DIR / "README.md"
        self.assertTrue(readme.is_file())
        text = readme.read_text(encoding="utf-8")
        self.assertIn("Not started", text)
        self.assertIn("In progress", text)
        self.assertIn("Done", text)
        self.assertIn("The product site was not built", text)
        self.assertIn("stages 0A and 0B", text)
        for slug, _paths in IN_PROGRESS.items():
            matched = [line for line in text.splitlines() if slug in line]
            self.assertEqual(len(matched), 1, slug)
            self.assertIn("In progress", matched[0])
        for slug in NOT_STARTED:
            matched = [line for line in text.splitlines() if slug in line]
            self.assertEqual(len(matched), 1, slug)
            self.assertIn("Not started", matched[0])

    def test_one_markdown_file_per_parent_task(self) -> None:
        """Each parent task has one markdown file besides the index."""
        expected = {f"{slug}.md" for slug in _task_slugs()}
        expected.add("README.md")
        found = {path.name for path in PROGRESS_DIR.glob("*.md")}
        self.assertEqual(found, expected)
        self.assertEqual(len(found), 96)

    def test_every_task_file_has_status_evidence_and_remaining(self) -> None:
        """Task files use Status, Evidence, and Remaining headings."""
        for slug in _task_slugs():
            headings = _heading_names(_read(slug))
            self.assertIn("Status", headings, slug)
            self.assertIn("Evidence", headings, slug)
            self.assertIn("Remaining", headings, slug)

    def test_partial_tasks_are_in_progress(self) -> None:
        """Partial tasks use the exact in-progress status line."""
        for slug in IN_PROGRESS:
            lines = [
                line.strip()
                for line in _read(slug).splitlines()
                if line.strip().startswith("Status:")
            ]
            self.assertEqual(lines, ["Status: In progress"], slug)

    def test_not_started_tasks_are_not_started(self) -> None:
        """Tasks that have not begun use the exact not-started line."""
        for slug in NOT_STARTED:
            lines = [
                line.strip()
                for line in _read(slug).splitlines()
                if line.strip().startswith("Status:")
            ]
            self.assertEqual(lines, ["Status: Not started"], slug)

    def test_no_task_file_says_done(self) -> None:
        """No parent task is marked Done."""
        for slug in _task_slugs():
            self.assertNotIn("Status: Done", _read(slug), slug)

    def test_partial_evidence_cites_paths_that_exist(self) -> None:
        """In-progress evidence names repo paths that are on disk."""
        for slug, paths in IN_PROGRESS.items():
            evidence = _section(_read(slug), "Evidence")
            self.assertNotEqual(evidence, "none", slug)
            for relative in paths:
                self.assertTrue(
                    (REPO_ROOT / relative).exists(),
                    relative,
                )
                self.assertIn(relative, evidence, slug)
            remaining = _section(_read(slug), "Remaining")
            self.assertIn("Venkat has not approved", remaining, slug)
            self.assertIn("Exit criteria are not met", remaining, slug)

    def test_not_started_evidence_is_none(self) -> None:
        """Tasks that have not begun do not cite invented evidence."""
        for slug in NOT_STARTED:
            self.assertEqual(_section(_read(slug), "Evidence"), "none", slug)
            self.assertTrue(_section(_read(slug), "Remaining"), slug)


if __name__ == "__main__":
    unittest.main()
