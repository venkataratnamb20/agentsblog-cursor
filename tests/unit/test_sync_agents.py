"""Tests for copying shared agent skills into the Claude skills tree."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


def _load_sync_agents() -> ModuleType:
    """Load ``scripts/sync_agents.py`` without making ``scripts`` a package.

    Returns:
        The loaded sync_agents module.

    Raises:
        ImportError: If the module file cannot be loaded.
    """
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "scripts" / "sync_agents.py"
    spec = importlib.util.spec_from_file_location("sync_agents", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load sync_agents from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SyncAgentsTest(unittest.TestCase):
    """Verify skill directories are copied as real files."""

    def test_copies_new_post_skill(self) -> None:
        """A fake repo's new-post skill is copied byte-for-byte.

        The copy is repeated so a second run replaces the destination
        instead of nesting another directory inside it.
        """
        module = _load_sync_agents()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".agents" / "skills" / "new-post" / "SKILL.md"
            source.parent.mkdir(parents=True)
            payload = b"---\nname: new-post\n---\nDraft a post.\n"
            source.write_bytes(payload)

            module.sync_skills(root)
            module.sync_skills(root)

            copied = root / ".claude" / "skills" / "new-post" / "SKILL.md"
            self.assertTrue(copied.is_file())
            self.assertFalse(copied.is_symlink())
            self.assertEqual(copied.read_bytes(), source.read_bytes())
            nested = copied.parent / "new-post" / "SKILL.md"
            self.assertFalse(nested.exists())


if __name__ == "__main__":
    unittest.main()
