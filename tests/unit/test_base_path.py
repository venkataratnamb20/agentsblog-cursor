"""Tests for project-Pages base path prefixing."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from agentsblog import render  # noqa: E402
from agentsblog.build import build_site  # noqa: E402


class TestBasePath(unittest.TestCase):
    """Root-absolute links honour AGENTSBLOG_BASE_PATH."""

    def tearDown(self) -> None:
        """Reset the renderer base path after each test."""
        render.set_base_path("")

    def test_document_prefixes_stylesheet_and_nav(self) -> None:
        """A non-empty base path prefixes chrome URLs."""
        render.set_base_path("/agentsblog-cursor")
        page = render.render_index([])
        self.assertIn('href="/agentsblog-cursor/assets/site.css"', page)
        self.assertIn('href="/agentsblog-cursor/"', page)
        self.assertIn('href="/agentsblog-cursor/search.html"', page)

    def test_build_writes_prefixed_assets(self) -> None:
        """build_site accepts base_path and writes prefixed pages."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            output = root / "build"
            content.mkdir()
            build_site(
                content,
                output,
                site_url="https://example.github.io/agentsblog-cursor",
                base_path="/agentsblog-cursor",
            )
            index = (output / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/agentsblog-cursor/assets/site.css"', index)
        self.assertIn('href="/agentsblog-cursor/about.html"', index)


if __name__ == "__main__":
    unittest.main()
