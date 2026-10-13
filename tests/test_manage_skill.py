import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("manage_skill", REPO_ROOT / "scripts/manage_skill.py")
manage_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manage_skill)


class SkillPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="technews-test-")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.output = self.work / "skill"

    def export(self, overwrite=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return manage_skill.export_skill(REPO_ROOT, self.output, overwrite=overwrite)

    def test_repo_entries_are_current(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(manage_skill.sync_entries(REPO_ROOT, check=True), 0)

    def test_export_is_self_contained_and_repeatable(self):
        self.assertEqual(self.export(), 0)
        self.assertEqual(self.export(), 0)
        skill = self.output / "SKILL.md"
        self.assertEqual(skill.read_bytes(), (REPO_ROOT / "docs/skills/technews.md").read_bytes())
        for filename in ("sources.md", "output-format.md"):
            self.assertTrue((self.output / "references" / filename).is_file())
        self.assertNotIn("../../../docs/skills", skill.read_text(encoding="utf-8"))

    def test_conflict_does_not_partially_install(self):
        references = self.output / "references"
        references.mkdir(parents=True)
        existing = references / "sources.md"
        existing.write_text("user notes", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.export()
        self.assertEqual(existing.read_text(encoding="utf-8"), "user notes")
        self.assertFalse((self.output / "SKILL.md").exists())
        self.assertFalse((references / "output-format.md").exists())

    def test_overwrite_preserves_unrelated_files(self):
        self.output.mkdir()
        (self.output / "SKILL.md").write_text("old version", encoding="utf-8")
        unrelated = self.output / "personal-notes.md"
        unrelated.write_text("keep this", encoding="utf-8")
        self.assertEqual(self.export(overwrite=True), 0)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep this")

    def test_symlinked_reference_directory_is_rejected(self):
        external = self.work / "external"
        external.mkdir()
        self.output.mkdir()
        (self.output / "references").symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.export(overwrite=True)
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.output / "SKILL.md").exists())

    def test_export_cannot_replace_repo_entries(self):
        for entry in manage_skill.ENTRY_ROOTS:
            output = REPO_ROOT / entry / "skills/technews"
            with self.assertRaises(ValueError):
                manage_skill.export_skill(REPO_ROOT, output, overwrite=True)

    def test_sync_check_detects_drift_without_writing(self):
        root = self.work / "repo"
        for relative in (
            "docs/skills/technews.md",
            "docs/skills/references/sources.md",
            "docs/skills/references/output-format.md",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((REPO_ROOT / relative).read_bytes())
        with contextlib.redirect_stdout(io.StringIO()):
            manage_skill.sync_entries(root)
        entry = root / ".cursor/skills/technews/SKILL.md"
        entry.write_text("out of sync", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(manage_skill.sync_entries(root, check=True), 1)
        self.assertEqual(entry.read_text(encoding="utf-8"), "out of sync")


if __name__ == "__main__":
    unittest.main()
