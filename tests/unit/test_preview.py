"""Tests for the local static-site preview server."""

from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from inspect import signature
from pathlib import Path
from typing import Iterator
from unittest import mock

# The package lives under src/. Unittest discovery does not set PYTHONPATH.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC_ROOT = _REPO_ROOT / "src"
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from agentsblog.preview import (  # noqa: E402
    create_preview_server,
    main,
    preview_handler,
    resolve_preview_directory,
    serve_preview,
)

_MAKE_PS1 = _REPO_ROOT / "make.ps1"
_MAKEFILE = _REPO_ROOT / "Makefile"
_PREVIEW_BRANCH = "if ($Target -eq 'dev' -or $Target -eq 'preview')"
_PREVIEW_COMMAND = "python -m agentsblog.preview"
_PREVIEW_COMMAND_UNIX = "PYTHONPATH=src python3 -m agentsblog.preview"
_LOOPBACK_HOST = "127.0.0.1"
_DEFAULT_PORT = 8000


class _RequestStub:
    """Socket stand-in so a handler can be built without binding a port."""

    def makefile(self, mode: str, buffering: int = -1) -> io.BytesIO:
        """Return an empty binary stream for the handler.

        Args:
            mode: File mode requested by the handler.
            buffering: Buffer size requested by the handler.

        Returns:
            An empty in-memory binary stream.
        """
        del mode, buffering
        return io.BytesIO()


def _powershell_branch(source: str, marker: str) -> str:
    """Return one top-level PowerShell conditional.

    Args:
        source: Full text of ``make.ps1``.
        marker: First line of the conditional, without a newline.

    Returns:
        The conditional through the line before the next top-level
        statement. Empty when ``marker`` is absent.
    """
    start = source.find(marker)
    if start < 0:
        return ""
    lines = source[start:].splitlines(keepends=True)
    selected = [lines[0]]
    for line in lines[1:]:
        if line.startswith("if ") or line.startswith("$"):
            break
        selected.append(line)
    return "".join(selected)


def _makefile_recipe(makefile: str, target: str) -> str:
    """Return the recipe lines under one Makefile target.

    Args:
        makefile: Full text of ``Makefile``.
        target: Target name, without a colon.

    Returns:
        The indented recipe that follows ``target:``. Empty when that
        target is absent.
    """
    lines = makefile.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith(f"{target}:"):
            start = index + 1
            break
    if start is None:
        return ""
    recipe: list[str] = []
    for line in lines[start:]:
        if line.startswith("\t") or line.strip() == "":
            recipe.append(line)
            continue
        break
    return "\n".join(recipe)


@contextmanager
def _working_directory(directory: Path) -> Iterator[Path]:
    """Change the working directory for the duration of a test.

    Args:
        directory: Directory to use as the working directory.

    Yields:
        The same directory, after it has become the working directory.
    """
    previous = Path.cwd()
    os.chdir(directory)
    try:
        yield directory
    finally:
        os.chdir(previous)


class TestPreviewDirectory(unittest.TestCase):
    """Preview paths resolve from the working directory."""

    def test_default_directory_is_build_under_the_working_directory(
        self,
    ) -> None:
        """The default directory is ``build`` beside the working directory."""
        with tempfile.TemporaryDirectory() as raw_directory:
            root = Path(raw_directory)
            with _working_directory(root):
                self.assertEqual(
                    resolve_preview_directory(),
                    root / "build",
                )

    def test_relative_directory_uses_the_working_directory(self) -> None:
        """A relative directory is joined to the working directory."""
        with tempfile.TemporaryDirectory() as raw_directory:
            root = Path(raw_directory)
            with _working_directory(root):
                self.assertEqual(
                    resolve_preview_directory("public"),
                    root / "public",
                )


class TestPreviewHandler(unittest.TestCase):
    """The handler class serves the directory it was given."""

    def test_handler_maps_to_the_chosen_directory(self) -> None:
        """A handler instance maps a URL into the chosen directory.

        The handler is constructed with a socket stand-in, so this test
        does not bind a port.
        """
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            handler = preview_handler(directory)(
                _RequestStub(),
                (_LOOPBACK_HOST, 0),
                None,
            )
            self.assertIsInstance(handler, SimpleHTTPRequestHandler)
            self.assertEqual(Path(handler.directory), directory)
            mapped = Path(handler.translate_path("/index.html"))
            self.assertEqual(mapped, directory / "index.html")

    def test_handlers_keep_separate_directories(self) -> None:
        """Each handler class keeps the directory from its own call."""
        with tempfile.TemporaryDirectory() as first_raw:
            with tempfile.TemporaryDirectory() as second_raw:
                first = Path(first_raw)
                second = Path(second_raw)
                first_type = preview_handler(first)
                second_type = preview_handler(second)
                first_handler = first_type(
                    _RequestStub(),
                    (_LOOPBACK_HOST, 0),
                    None,
                )
                second_handler = second_type(
                    _RequestStub(),
                    (_LOOPBACK_HOST, 0),
                    None,
                )
                self.assertEqual(Path(first_handler.directory), first)
                self.assertEqual(Path(second_handler.directory), second)


class TestPreviewServer(unittest.TestCase):
    """The server binds the loopback interface and then closes."""

    def test_default_port_is_8000(self) -> None:
        """The port argument defaults to 8000 and does not bind it."""
        parameters = signature(create_preview_server).parameters
        self.assertEqual(parameters["port"].default, _DEFAULT_PORT)
        self.assertIsNone(parameters["directory"].default)

    def test_server_binds_loopback_and_uses_the_handler_directory(
        self,
    ) -> None:
        """Port 0 binds 127.0.0.1, and the handler still serves the directory.

        The listening socket is closed in a ``finally`` block. The test
        does not call ``serve_forever``.
        """
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            server = create_preview_server(directory=directory, port=0)
            try:
                host, bound_port = server.server_address[:2]
                self.assertIsInstance(server, ThreadingHTTPServer)
                self.assertEqual(host, _LOOPBACK_HOST)
                self.assertIsInstance(bound_port, int)
                self.assertGreater(bound_port, 0)
                self.assertNotEqual(bound_port, _DEFAULT_PORT)
                handler = server.RequestHandlerClass(
                    _RequestStub(),
                    (_LOOPBACK_HOST, 0),
                    server,
                )
                self.assertEqual(Path(handler.directory), directory)
            finally:
                server.server_close()


class TestPreviewEntryPoint(unittest.TestCase):
    """Running the module serves the preview and then closes it."""

    def test_serve_preview_serves_and_closes(self) -> None:
        """``serve_preview`` starts the server and closes it afterward."""
        server = mock.Mock()
        with mock.patch(
            "agentsblog.preview.create_preview_server",
            return_value=server,
        ) as factory:
            serve_preview(directory="site", port=9000)
        factory.assert_called_once_with(directory="site", port=9000)
        server.serve_forever.assert_called_once_with()
        server.server_close.assert_called_once_with()

    def test_main_starts_the_default_preview(self) -> None:
        """``main`` serves the preview with default directory and port."""
        with mock.patch("agentsblog.preview.serve_preview") as serve:
            main()
        serve.assert_called_once_with()

    def test_module_runs_main_when_executed(self) -> None:
        """``python -m agentsblog.preview`` calls ``main`` and does not import-serve."""
        source = (_SRC_ROOT / "agentsblog" / "preview.py").read_text(
            encoding="utf-8",
        )
        tail = [line.strip() for line in source.strip().splitlines()[-2:]]
        self.assertEqual(tail, ['if __name__ == "__main__":', "main()"])


class TestPreviewTaskRunner(unittest.TestCase):
    """``dev`` and ``preview`` start the preview module and unknown targets fail."""

    def test_make_ps1_dev_and_preview_run_the_preview_module(self) -> None:
        """Windows ``dev`` and ``preview`` run the preview module.

        ``PYTHONPATH`` includes ``src``, matching the site build hook.
        The old stub messages are gone.
        """
        source = _MAKE_PS1.read_text(encoding="utf-8")
        branch = _powershell_branch(source, _PREVIEW_BRANCH)
        self.assertIn("$Target -eq 'dev'", branch)
        self.assertIn("$Target -eq 'preview'", branch)
        self.assertIn("PYTHONPATH", branch)
        self.assertIn(_PREVIEW_COMMAND, branch)
        self.assertIn("exit (Get-NativeExitCode)", branch)
        self.assertNotIn("agentsblog.build", branch)
        self.assertNotIn("once the stack is chosen", branch)

    def test_makefile_dev_and_preview_run_the_preview_module(self) -> None:
        """Unix ``dev`` and ``preview`` run the preview module.

        Both recipes set ``PYTHONPATH=src`` and call ``python3``.
        """
        makefile = _MAKEFILE.read_text(encoding="utf-8")
        for target in ("dev", "preview"):
            recipe = _makefile_recipe(makefile, target)
            self.assertIn(_PREVIEW_COMMAND_UNIX, recipe)
            self.assertNotIn("once the stack is chosen", recipe)

    def test_unknown_target_exits_with_status_1(self) -> None:
        """An unknown task-runner target still exits 1."""
        if sys.platform != "win32":
            self.skipTest("make.ps1 is invoked on Windows")
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-File",
                str(_MAKE_PS1),
                "not-a-real-target",
            ],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Unknown target: not-a-real-target", result.stderr)


if __name__ == "__main__":
    unittest.main()
