"""Serve a directory of static files on the local loopback interface."""

from __future__ import annotations

import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

_LOOPBACK_HOST = "127.0.0.1"
_DEFAULT_PORT = 8000
_DEFAULT_DIRECTORY_NAME = "build"


def resolve_preview_directory(
    directory: str | os.PathLike[str] | None = None,
) -> Path:
    """Return the directory a preview server should serve.

    Args:
        directory: Directory to serve. ``None`` selects ``build`` under
            the current working directory. A relative path is joined to
            that working directory.

    Returns:
        The preview directory. The directory does not need to exist yet.
    """
    if directory is None:
        directory = _DEFAULT_DIRECTORY_NAME
    return Path.cwd() / Path(directory)


def preview_handler(
    directory: str | os.PathLike[str] | None = None,
) -> type[SimpleHTTPRequestHandler]:
    """Return a handler class that serves one static directory.

    Args:
        directory: Directory to serve. ``None`` selects ``build`` under
            the current working directory.

    Returns:
        A handler class. Each instance maps request paths into that
        directory.
    """
    # Captured per call so a later handler cannot retarget this class.
    static_root = os.fspath(resolve_preview_directory(directory))

    class StaticPreviewHandler(SimpleHTTPRequestHandler):
        """Serve files from the directory captured for this class."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=static_root, **kwargs)

    return StaticPreviewHandler


def create_preview_server(
    directory: str | os.PathLike[str] | None = None,
    port: int = _DEFAULT_PORT,
) -> ThreadingHTTPServer:
    """Return a loopback server bound to a static preview directory.

    The socket is bound and listening. The caller starts and closes it.

    Args:
        directory: Directory to serve. ``None`` selects ``build`` under
            the current working directory.
        port: TCP port on ``127.0.0.1``. ``0`` asks the OS for a free port.

    Returns:
        A threaded HTTP server bound to the loopback interface.
    """
    handler = preview_handler(directory)
    address = (_LOOPBACK_HOST, port)
    return ThreadingHTTPServer(address, handler)


def serve_preview(
    directory: str | os.PathLike[str] | None = None,
    port: int = _DEFAULT_PORT,
) -> None:
    """Serve a preview directory until the server stops, then close it.

    Args:
        directory: Directory to serve. ``None`` selects ``build`` under
            the current working directory.
        port: TCP port on ``127.0.0.1``.
    """
    server = create_preview_server(directory=directory, port=port)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main() -> None:
    """Start the preview server with the default directory and port."""
    serve_preview()


if __name__ == "__main__":
    main()
