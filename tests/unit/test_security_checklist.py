"""Tests for the local security checklist.

Behaviour: a temp build has no third-party script sources and no
secret-shaped strings. The preview source binds to loopback. The
launch checklist records SR-1 and states there is no production host.
Module: ``agentsblog.build``. Existing tests: none.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_SRC = _REPO / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog.build import build_site  # noqa: E402

_THIRD_PARTY_HOSTS = (
    "google-analytics.com",
    "googletagmanager.com",
    "cdn.jsdelivr.net",
)
_SECRET_MARKERS = (
    "AKIA",
    "BEGIN PRIVATE KEY",
    "api_key=",
)
_PREVIEW = _REPO / "src" / "agentsblog" / "preview.py"
_CHECKLIST = _REPO / "docs" / "security" / "launch-checklist.md"


def _html_texts(output: Path) -> list[tuple[str, str]]:
    """Read every built HTML file.

    Args:
        output: Directory written by ``build_site``.

    Returns:
        Pairs of relative path and file text. The scan is O(n) in the
        number of HTML files.
    """
    return [
        (path.relative_to(output).as_posix(), path.read_text(encoding="utf-8"))
        for path in sorted(output.rglob("*.html"))
    ]


def _built_texts(output: Path) -> list[tuple[str, str]]:
    """Read every file written by the build.

    Args:
        output: Directory written by ``build_site``.

    Returns:
        Pairs of relative path and file text. The scan is O(n) in the
        number of built files.
    """
    return [
        (path.relative_to(output).as_posix(), path.read_text(encoding="utf-8"))
        for path in sorted(output.rglob("*"))
        if path.is_file()
    ]


class TestSecurityChecklist(unittest.TestCase):
    """Local build stays free of third-party scripts and secret markers."""

    def _build(self, root: Path) -> Path:
        """Build an empty content directory into a temp output tree.

        Args:
            root: Temporary directory that owns content and output.

        Returns:
            The output directory after ``build_site`` returns.
        """
        content = root / "content"
        output = root / "build"
        content.mkdir()
        build_site(content, output)
        return output

    def test_built_html_has_no_third_party_scripts(self) -> None:
        """No built HTML loads a script URL or a named third-party host."""
        with tempfile.TemporaryDirectory() as tmp:
            pages = _html_texts(self._build(Path(tmp)))
        self.assertGreater(len(pages), 0)
        for name, text in pages:
            self.assertNotIn("<script src=", text, name)
            for host in _THIRD_PARTY_HOSTS:
                self.assertNotIn(host, text, name)

    def test_preview_default_origin_is_loopback(self) -> None:
        """``preview.py`` names ``127.0.0.1`` as the bind host."""
        text = _PREVIEW.read_text(encoding="utf-8")
        self.assertIn("127.0.0.1", text)

    def test_built_files_omit_secret_shaped_strings(self) -> None:
        """Built files do not contain key or credential markers."""
        with tempfile.TemporaryDirectory() as tmp:
            files = _built_texts(self._build(Path(tmp)))
        self.assertGreater(len(files), 0)
        for name, text in files:
            for marker in _SECRET_MARKERS:
                self.assertNotIn(marker, text, name)

    def test_launch_checklist_records_local_scope(self) -> None:
        """The checklist names SR-1 and states there is no production host."""
        text = _CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("SR-1", text)
        self.assertIn("no production host", text)


if __name__ == "__main__":
    unittest.main()
