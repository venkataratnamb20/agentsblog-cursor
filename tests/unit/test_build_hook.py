"""Tests for the conditional local site build hook."""

from __future__ import annotations

import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MAKE_PS1 = _REPO_ROOT / "make.ps1"
_MAKEFILE = _REPO_ROOT / "Makefile"
_AGENTS = _REPO_ROOT / "AGENTS.md"
_ADR = _REPO_ROOT / "docs" / "adr" / "0002-python-stdlib-site.md"
_BUILD_BRANCH = "if ($Target -eq 'build')"
_COMPILEALL = "python -m compileall -q scripts tests"
_COMPILEALL_UNIX = "python3 -m compileall -q scripts tests"
_SITE_BUILD = "python -m agentsblog.build"
_SITE_BUILD_UNIX = "python3 -m agentsblog.build"
_BUILDER = "src/agentsblog/build.py"
_ADR_PATH = "docs/adr/0002-python-stdlib-site.md"
_STDLIB_BUILDER = "local site builder is the Python standard library"
_ADR_REJECTION = (
    "This local slice rejects a Node framework and a hosted CMS."
)


def _powershell_build_branch(source: str) -> str:
    """Return the PowerShell branch that handles the build target.

    Args:
        source: Full text of ``make.ps1``.

    Returns:
        Text from the build conditional up to the next top-level
        statement. Empty when that conditional is absent.
    """
    start = source.find(_BUILD_BRANCH)
    if start < 0:
        return ""
    lines = source[start:].splitlines(keepends=True)
    selected = [lines[0]]
    for line in lines[1:]:
        if line.startswith("if ") or line.startswith("$"):
            break
        selected.append(line)
    return "".join(selected)


def _makefile_build_recipe(makefile: str) -> str:
    """Return the recipe lines under the Makefile build target.

    Args:
        makefile: Full text of ``Makefile``.

    Returns:
        The indented recipe that follows ``build:``. Empty when that
        target is absent.
    """
    lines = makefile.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("build:"):
            start = index + 1
            break
    if start is None:
        return ""
    recipe: list[str] = []
    for line in lines[start:]:
        if line.startswith("\t"):
            recipe.append(line)
            continue
        if line.strip() == "":
            recipe.append(line)
            continue
        break
    return "\n".join(recipe)


class TestBuildHook(unittest.TestCase):
    """Verify build runs the site module only when its file exists."""

    def test_make_ps1_keeps_compileall_and_conditional_builder(self) -> None:
        """The Windows build target compiles, then builds when present.

        ``compileall`` stays in the build branch. ``python -m
        agentsblog.build`` runs only after the branch has checked that
        ``src/agentsblog/build.py`` exists.
        """
        source = _MAKE_PS1.read_text(encoding="utf-8")
        branch = _powershell_build_branch(source)
        self.assertIn(_COMPILEALL, branch)
        self.assertIn("Test-Path", branch)
        self.assertIn(_BUILDER, branch)
        builder_at = branch.find(_SITE_BUILD)
        self.assertGreater(builder_at, branch.find(_COMPILEALL))
        self.assertGreater(builder_at, branch.find(_BUILDER))

    def test_makefile_keeps_compileall_and_conditional_builder(self) -> None:
        """The Makefile build recipe compiles, then builds when present.

        ``python3 -m agentsblog.build`` is gated on
        ``src/agentsblog/build.py`` and stays after ``compileall``.
        """
        makefile = _MAKEFILE.read_text(encoding="utf-8")
        recipe = _makefile_build_recipe(makefile)
        self.assertIn(_COMPILEALL_UNIX, recipe)
        self.assertIn(_BUILDER, recipe)
        builder_at = recipe.find(_SITE_BUILD_UNIX)
        self.assertGreater(builder_at, recipe.find(_COMPILEALL_UNIX))
        self.assertGreater(builder_at, recipe.find(_BUILDER))
        self.assertIn(f"[ -f {_BUILDER} ]", recipe)

    def test_agents_md_names_stdlib_builder_and_adr(self) -> None:
        """AGENTS.md records the stdlib builder and points at ADR 0002."""
        text = _AGENTS.read_text(encoding="utf-8")
        self.assertIn(_STDLIB_BUILDER, text)
        self.assertIn(_ADR_PATH, text)

    def test_adr_rejects_node_framework_and_hosted_cms(self) -> None:
        """ADR 0002 exists and rejects a Node framework and a hosted CMS.

        The rejection is for this local slice. Hosting choices stay
        outside the decision.
        """
        self.assertTrue(_ADR.is_file(), f"{_ADR_PATH} is missing")
        text = _ADR.read_text(encoding="utf-8")
        self.assertIn(_ADR_REJECTION, text)


if __name__ == "__main__":
    unittest.main()
