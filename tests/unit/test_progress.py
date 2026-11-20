"""Tests for the parent-task progress record.

The repository root is the parent of ``tests`` (``parents[2]`` of this
file). Progress files are the record of work, not a claim that the
product site exists.

Behaviour under test: DONE / IN_PROGRESS / NOT_STARTED inventory for
every parent task under ``docs/progress/``, including closed stages
0A/0B, M0, and M1. This module is the existing coverage file for that
inventory. User instruction: close Stage 1 specification tasks and
sync the catalog; no new unit test files.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRESS_DIR = REPO_ROOT / "docs" / "progress"

# Slugs are the parent-task names: lowercase, spaces as hyphens,
# punctuation dropped. DONE closed stage 0A/0B (and M0) with evidence.
DONE: dict[str, tuple[str, ...]] = {
    "git-branching-model-pr-workflow-main-develop-feature-release-hotfix": (
        "docs/guidelines/git-workflow.md",
    ),
    "code-maintainability-guidelines-clean-code-solid-tdd-bdd-data-structures-algorithms": (
        "docs/guidelines/code-quality.md",
    ),
    "create-missing-skills-commands-workflows-subagents-for-every-agent-role": (
        ".agents/skills",
        ".claude/agents",
        ".claude/commands",
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
    "verify-harness-end-to-end-in-all-four-tools-smoke-test": (
        "docs/agents/harness-smoke.md",
    ),
    "m0-agent-harness-team-governance-ready": (
        "docs/governance/m0-checklist.md",
        "docs/agents/harness-smoke.md",
    ),
    "write-prd-problem-audience-features-scope-success-metrics": (
        "docs/product/prd.md",
    ),
    "define-content-pillars-topic-taxonomy-pillars-tags-series": (
        "docs/product/content-pillars.md",
    ),
    "select-tech-stack-hosting-services-adrs": (
        "docs/adr/0002-python-stdlib-site.md",
    ),
    "define-test-strategy-quality-gates-code-review-standards": (
        "docs/testing/test-strategy.md",
    ),
    "design-system-architecture-content-model-environments": (
        "docs/architecture/system.md",
    ),
    "threat-model-security-requirements": (
        "docs/security/threat-model.md",
        "docs/security/requirements.md",
    ),
    "write-requirements-spec-functional-non-functional-srs": (
        "docs/requirements/srs.md",
    ),
    "define-seo-analytics-kpi-kpm-tracking-spec": (
        "docs/seo/measurement.md",
    ),
    "m1-specifications-approved-prd-requirements-architecture-security-test-plans": (
        "docs/product/prd.md",
        "docs/requirements/srs.md",
        "docs/architecture/system.md",
        "docs/security/threat-model.md",
        "docs/security/requirements.md",
        "docs/testing/test-strategy.md",
    ),
    "information-architecture-sitemap-navigation-taxonomy": (
        "docs/design/information-architecture.md",
    ),
    "wireframes-high-fidelity-ui-home-post-pillar-about-subscribe-404": (
        "docs/design/wireframes.md",
    ),
    "design-system-accessibility-spec-wcag-22-aa": (
        "docs/design/accessibility.md",
    ),
    "brand-identity-name-tagline-logo-colours-typography-cover-template": (
        "docs/design/brand-identity.md",
    ),
    "m2-design-approved": (
        "docs/design/wireframes.md",
        "docs/design/brand-identity.md",
    ),
    "implement-content-model-authoring-workflow-markdown-mdx": (
        "src/agentsblog/posts.py",
        "src/agentsblog/markdown.py",
    ),
    "build-site-templates-components-responsive-dark-mode": (
        "src/agentsblog/build.py",
        "src/agentsblog/render.py",
    ),
    "integrate-privacy-friendly-analytics-cookie-consent-uk-gdpr-pecr": (
        "src/agentsblog/consent.py",
    ),
    "set-up-cicd-pipeline-with-preview-deploys-rollback": (
        ".github/workflows/ci.yml",
        ".github/workflows/cd.yml",
    ),
    "provision-hosting-environments-staging-prod-domain-https": (
        "docs/adr/0003-github-pages-hosting.md",
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
    "m3-feature-complete-on-staging": (
        "docs/governance/m3-checklist.md",
        "docs/adr/0003-github-pages-hosting.md",
    ),
}

IN_PROGRESS: dict[str, tuple[str, ...]] = {
    "automated-test-suite-unit-integration-e2e-visual-regression": (
        "tests/unit",
        "tests/integration",
    ),
    "fortnightly-project-status-updates": (
        "docs/progress/fortnightly-project-status-updates.md",
    ),
    "cross-browser-responsive-testing": (
        "tests/unit/test_responsive.py",
    ),
    "accessibility-audit-wcag-22-aa": (
        "docs/design/accessibility-audit.md",
    ),
    "performance-testing-budgets-core-web-vitals": (
        "docs/testing/performance-budgets.md",
    ),
    "security-vulnerability-checklist": (
        "docs/security/launch-checklist.md",
    ),
    "privacy-compliance-check": (
        "docs/security/privacy-check.md",
    ),
    "seo-audit": (
        "docs/seo/audit.md",
    ),
    "code-review-every-pr-reviewed-against-the-checklist": (
        "docs/guidelines/code-review.md",
    ),
    "define-per-post-workflow-brief-draft-tech-edit-seo-approval-publish-distribute": (
        "docs/editorial/per-post-workflow.md",
    ),
    "editorial-content-qa-checklist-applies-to-every-post": (
        "docs/editorial/content-qa-checklist.md",
    ),
    "create-topic-backlog-score-ideas-reader-value-x-effort": (
        "docs/product/topic-backlog.md",
    ),
    "build-12-week-editorial-calendar-with-owners-per-stage-dec-2026-feb-2027": (
        "docs/editorial/calendar-2026-q1.md",
    ),
    "post-1-what-is-an-ai-agent-agents-vs-workflows-vs-chatbots": (
        "docs/editorial/briefs/what-is-an-ai-agent.md",
        "content/posts/what-is-an-ai-agent.md",
        "research/packs/what-is-an-ai-agent.md",
    ),
    "post-2-anatomy-of-an-agent-llm-tools-memory-the-react-loop": (
        "docs/editorial/briefs/anatomy-of-an-agent.md",
    ),
    "set-up-reference-library-for-papers-notes-zotero-notion": (
        "research/README.md",
    ),
}

NOT_STARTED: tuple[str, ...] = (
    "production-readiness-review-go-no-go",
    "m4-quality-gates-passed-go-for-launch",
    "caching-cdn-configuration",
    "backups-disaster-recovery",
    "production-deployment-dns-cutover",
    "post-deploy-smoke-tests-search-engine-submission",
    "m5-production-launch-blog-live-with-first-3-posts",
    "launch-communications-linkedin-x-first-newsletter",
    "monitoring-uptime-alerting-slos",
    "runbooks-deploy-rollback-incident-response",
    "idea-cost-latency-optimisation-for-production-agents",
    "build-research-pipeline-arxiv-alerts-lab-blogs-github-trending-conference-papers",
    "post-10-research-roundup-1-notable-agent-papers-of-the-quarter",
    "m7-10-technically-verified-posts-published",
    "post-7-deep-agents-planning-sub-agents-file-systems-for-long-tasks",
    "post-9-guardrails-safety-human-in-the-loop-for-agents",
    "idea-computer-use-browser-agents-how-they-work-and-where-they-fail",
    "idea-agentic-rag-vs-classic-rag",
    "post-4-agent-memory-short-term-long-term-retrieval",
    "post-8-evaluating-agents-benchmarks-evals-llm-as-judge",
    "post-3-tool-calling-mcp-model-context-protocol-explained",
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
    """Return every parent-task slug: done, then in-progress, then not started.

    Returns:
        The stable slug for each parent task, including M0.
    """
    return tuple(DONE) + tuple(IN_PROGRESS) + NOT_STARTED


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
        """Count done, partial, and not-started tasks through M3.

        94 other parent tasks plus M0 is 95 task files, plus the index.
        """
        slugs = _task_slugs()
        self.assertEqual(len(DONE), 37)
        self.assertEqual(len(IN_PROGRESS), 16)
        self.assertEqual(len(NOT_STARTED), 42)
        self.assertEqual(len(slugs), 95)
        self.assertEqual(len(set(slugs)), 95)
        self.assertIn("m0-agent-harness-team-governance-ready", DONE)
        self.assertIn(
            "m1-specifications-approved-prd-requirements-architecture-security-test-plans",
            DONE,
        )
        self.assertIn("m2-design-approved", DONE)
        self.assertIn("m3-feature-complete-on-staging", DONE)

    def test_readme_exists_and_names_the_three_statuses(self) -> None:
        """The index exists and names Not started, In progress, and Done.

        The opening states that stages through M3 are closed.
        """
        readme = PROGRESS_DIR / "README.md"
        self.assertTrue(readme.is_file())
        text = readme.read_text(encoding="utf-8")
        self.assertIn("Not started", text)
        self.assertIn("In progress", text)
        self.assertIn("Done", text)
        self.assertIn("Stage 3 build", text)
        self.assertIn("0A and 0B", text)
        self.assertIn("M3", text)
        for slug in DONE:
            matched = [line for line in text.splitlines() if slug in line]
            self.assertEqual(len(matched), 1, slug)
            self.assertIn("Done", matched[0])
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

    def test_done_tasks_are_done(self) -> None:
        """Closed stage 0A/0B tasks use the exact Done status line."""
        for slug in DONE:
            lines = [
                line.strip()
                for line in _read(slug).splitlines()
                if line.strip().startswith("Status:")
            ]
            self.assertEqual(lines, ["Status: Done"], slug)

    def test_only_done_inventory_may_say_done(self) -> None:
        """Tasks outside DONE must not claim Status: Done."""
        for slug in tuple(IN_PROGRESS) + NOT_STARTED:
            self.assertNotIn("Status: Done", _read(slug), slug)

    def test_done_evidence_cites_paths_that_exist(self) -> None:
        """Done evidence names repo paths that are on disk."""
        for slug, paths in DONE.items():
            evidence = _section(_read(slug), "Evidence")
            self.assertNotEqual(evidence, "none", slug)
            for relative in paths:
                self.assertTrue(
                    (REPO_ROOT / relative).exists(),
                    relative,
                )
                self.assertIn(relative, evidence, slug)

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
