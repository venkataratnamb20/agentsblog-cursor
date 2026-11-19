"""Tests for the build task-runner target."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MAKE_PS1 = _REPO_ROOT / "make.ps1"
_MAKEFILE = _REPO_ROOT / "Makefile"
_SYNTAX_PROBE = _REPO_ROOT / "scripts" / "_build_syntax_probe.py"
_COMPILEALL = "python -m compileall -q scripts tests"
_COMPILEALL_UNIX = "python3 -m compileall -q scripts tests"
_BUILD_BRANCH = "if ($Target -eq 'build')"
_NOOP_BUILD = (
    "build: will produce a production build once the stack is chosen"
)


def _run_make_build() -> subprocess.CompletedProcess[str]:
    """Run ``make.ps1 build`` and capture both streams.

    Returns:
        The completed PowerShell process.
    """
    return subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-File",
            str(_MAKE_PS1),
            "build",
        ],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _build_branch(source: str) -> str:
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


class TestBuildTarget(unittest.TestCase):
    """Verify build compiles Python and returns the compiler status."""

    def test_windows_build_runs_compileall(self) -> None:
        """``make.ps1 build`` exits 0 and its stdout names compileall.

        The invocation matches the Windows task runner. A no-op
        message that never calls the compiler does not pass.
        """
        if sys.platform != "win32":
            self.skipTest("make.ps1 build is invoked on Windows")
        result = _run_make_build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("compileall", result.stdout)

    def test_windows_build_fails_on_syntax_error(self) -> None:
        """A syntax error in ``scripts`` makes ``make.ps1 build`` fail.

        The probe is removed after the run so a failed assertion does
        not leave a broken module in the tree.
        """
        if sys.platform != "win32":
            self.skipTest("make.ps1 build is invoked on Windows")
        _SYNTAX_PROBE.write_text("def (\n", encoding="utf-8", newline="\n")
        try:
            result = _run_make_build()
            self.assertNotEqual(result.returncode, 0, result.stdout)
        finally:
            _SYNTAX_PROBE.unlink(missing_ok=True)

    def test_build_branch_exits_with_compiler_status(self) -> None:
        """The build branch runs compileall and returns its exit code.

        The old pending entry always exited 0 before compiling. That
        entry is gone, and the branch does not exit 0 on its own.
        """
        source = _MAKE_PS1.read_text(encoding="utf-8")
        self.assertNotIn(_NOOP_BUILD, source)
        branch = _build_branch(source)
        self.assertIn(_COMPILEALL, branch)
        self.assertIn("exit (Get-NativeExitCode)", branch)
        self.assertNotIn("exit 0", branch)

    def test_makefile_build_runs_compileall(self) -> None:
        """The Makefile build recipe compiles scripts and tests."""
        makefile = _MAKEFILE.read_text(encoding="utf-8")
        self.assertIn(_COMPILEALL_UNIX, makefile)
        self.assertNotIn(_NOOP_BUILD, makefile)


if __name__ == "__main__":
    unittest.main()
