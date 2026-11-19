"""Copy shared agent skills into the Claude skills directory.

Claude on Windows reads real files. This module copies ``.agents/skills``
to ``.claude/skills`` and never creates a symlink or directory junction.
Agent definitions under ``.claude/agents`` are authored in place.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def sync_skills(repo_root: Path) -> list[Path]:
    """Copy ``.agents/skills/<name>`` to ``.claude/skills/<name>``.

    Each destination skill directory is removed and written again, so a
    second run does not nest a skill directory inside itself.

    Args:
        repo_root: Repository root that contains ``.agents`` and
            ``.claude``.

    Returns:
        Destination skill directories that were written, in name order.

    Raises:
        FileNotFoundError: If ``.agents/skills`` does not exist.
    """
    source_root = repo_root / ".agents" / "skills"
    if not source_root.is_dir():
        raise FileNotFoundError(
            f"Shared skills directory not found: {source_root}"
        )
    dest_root = repo_root / ".claude" / "skills"
    dest_root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for skill_dir in sorted(source_root.iterdir()):
        if not skill_dir.is_dir() or skill_dir.is_symlink():
            continue
        if skill_dir.is_junction():
            continue
        destination = dest_root / skill_dir.name
        _remove_existing(destination)
        shutil.copytree(skill_dir, destination, symlinks=False)
        written.append(destination)
    return written


def _remove_existing(path: Path) -> None:
    """Delete ``path`` without following a symlink or junction.

    Args:
        path: File, directory, symlink, or junction to remove. A missing
            path is left unchanged.
    """
    if path.is_symlink() or path.is_junction():
        path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)
        return
    if path.exists():
        path.unlink()


def main(argv: list[str] | None = None) -> int:
    """Copy skills for one repository.

    Args:
        argv: Arguments after the program name. The optional first item
            is the repository root. When omitted, the parent of this
            file's directory is used.

    Returns:
        Process exit code. ``0`` means every skill directory was copied.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if args:
        repo_root = Path(args[0]).resolve()
    else:
        repo_root = Path(__file__).resolve().parents[1]
    for destination in sync_skills(repo_root):
        print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
