"""Render a small Markdown subset to HTML."""

from __future__ import annotations

import html


def render_markdown(source: str) -> str:
    """Render ATX headings and paragraphs.

    A blank line separates blocks. A block whose only line starts
    with one to six ``#`` characters and a space is a heading. Every
    other block is a paragraph. ``<`` and ``&`` are escaped.

    Args:
        source: Markdown body. May be empty.

    Returns:
        HTML elements with no surrounding document. Empty when
        ``source`` has no non-blank lines.
    """
    return "".join(_render_block(block) for block in _blocks(source))


def _blocks(source: str) -> list[str]:
    """Split Markdown into blocks on blank lines.

    Args:
        source: Markdown body.

    Returns:
        Blocks in source order. Blank lines are separators, not
        blocks.
    """
    blocks: list[str] = []
    current: list[str] = []
    for line in source.splitlines():
        if line.strip():
            current.append(line)
            continue
        _flush(blocks, current)
    _flush(blocks, current)
    return blocks


def _flush(blocks: list[str], current: list[str]) -> None:
    """Move the current lines into ``blocks`` when any exist.

    Args:
        blocks: Completed blocks.
        current: Lines gathered since the last blank line. Cleared
            when a block is stored.
    """
    if not current:
        return
    blocks.append("\n".join(current))
    current.clear()


def _render_block(block: str) -> str:
    """Render one block as a heading or a paragraph.

    Args:
        block: One non-blank block.

    Returns:
        An HTML element.
    """
    heading = _heading(block)
    if heading is None:
        text = " ".join(line.strip() for line in block.splitlines())
        return f"<p>{html.escape(text)}</p>"
    level, text = heading
    return f"<h{level}>{html.escape(text)}</h{level}>"


def _heading(block: str) -> tuple[int, str] | None:
    """Return the level and text of a single-line ATX heading.

    Args:
        block: One block.

    Returns:
        The heading level and text, or None when the block is not
        a heading.
    """
    if "\n" in block:
        return None
    marks, separator, rest = block.partition(" ")
    if separator != " " or not marks or set(marks) != {"#"}:
        return None
    level = len(marks)
    if level > 6 or not rest.strip():
        return None
    return level, rest.strip()
