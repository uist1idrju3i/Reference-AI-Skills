"""Positive fixtures and deliberately broken skill inventories."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/check-skills.py"
SPEC = importlib.util.spec_from_file_location("check_skills", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class SkillsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.skill = self.root / ".agents/skills/example"
        self.skill.mkdir(parents=True)
        self.content = "---\nname: example\ndescription: Example skill\n---\n# Example\n"
        self.write_skill(self.content)
        (self.root / ".claude/skills").mkdir(parents=True)
        self.mirror = self.root / ".claude/skills/example"
        self.mirror.symlink_to("../../.agents/skills/example")
        self.config = ('[submodule "vendor/upstream"]\n\tpath = vendor/upstream\n'
                       '\turl = https://github.com/example/upstream.git\n\tshallow = true\n')
        (self.root / ".gitmodules").write_text(self.config, encoding="utf-8")
        self.table = ("## スキル一覧\n\n| スキル | 種類 | 使う場面 |\n|---|---|---|\n"
                      "| [`example`](.agents/skills/example/SKILL.md) | 自作 | 例 |\n")
        self.write_table(self.table)

    def write_skill(self, content):
        (self.skill / "SKILL.md").write_text(content, encoding="utf-8")

    def write_table(self, content):
        (self.root / "README.md").write_text(content, encoding="utf-8")

    def errors(self):
        return CHECK.check(self.root)

    def external(self):
        destination = self.root / "vendor/upstream/skill"
        destination.parent.mkdir(parents=True)
        self.skill.rename(destination)
        self.skill.symlink_to("../../vendor/upstream/skill")
        self.write_table(self.table.replace("自作", "外部"))
        return destination

    def test_valid_local(self):
        self.assertEqual([], self.errors())

    def test_valid_vendor(self):
        self.external()
        self.assertEqual([], self.errors())

    def test_folded_literal_and_quoted_descriptions(self):
        for value in ('>\n  First line\n  second line', '|-\n  Description',
                      '"Description"', "'A ''quoted'' description'", '"Keep # marker"',
                      '"Description" # comment', "'Description' # comment"):
            with self.subTest(value=value):
                self.write_skill(self.content.replace("Example skill", value))
                self.assertEqual([], self.errors())

    def test_missing_extra_copy_and_alias_mirrors(self):
        self.mirror.unlink()
        self.assertTrue(self.errors())
        self.mirror.mkdir()
        self.assertTrue(self.errors())
        self.mirror.rmdir()
        self.mirror.symlink_to("../../.agents/skills/../skills/example")
        self.assertTrue(self.errors())
        self.mirror.unlink()
        self.mirror.symlink_to("../../.agents/skills/example")
        (self.mirror.parent / "extra").symlink_to("../../.agents/skills/example")
        self.assertTrue(self.errors())

    def test_broken_external(self):
        destination = self.external()
        shutil.rmtree(destination)
        self.assertTrue(self.errors())

    def test_escaping_external(self):
        destination = self.external()
        self.skill.unlink()
        self.skill.symlink_to("../../outside")
        destination.rename(self.root / "outside")
        self.assertTrue(self.errors())

    def test_indirect_vendor_escape(self):
        destination = self.external()
        destination.rename(self.root / "outside")
        destination.symlink_to("../../outside")
        self.assertTrue(self.errors())

    def test_absolute_link_is_not_canonical(self):
        destination = self.external()
        self.skill.unlink()
        self.skill.symlink_to(destination)
        self.assertTrue(self.errors())

    def test_file_instead_of_directory(self):
        shutil.rmtree(self.skill)
        self.skill.write_text("not a directory", encoding="utf-8")
        self.assertTrue(self.errors())

    def test_skill_file_cannot_escape(self):
        (self.root / "outside.md").write_text(self.content, encoding="utf-8")
        (self.skill / "SKILL.md").unlink()
        (self.skill / "SKILL.md").symlink_to("../../../outside.md")
        self.assertTrue(self.errors())

    def test_bad_metadata(self):
        for content in ("# No header", "---\nname: example", self.content.replace("name: example", "name: wrong"),
                        self.content.replace("name: example", "name: example\nname: example"),
                        self.content.replace("description: Example skill", "description: good\ndescription: good"),
                        self.content.replace("description: Example skill", "")):
            with self.subTest(content=content):
                self.write_skill(content)
                self.assertTrue(self.errors())

    def test_empty_and_nonstring_descriptions(self):
        for value in ('', '""', "' '", '>', '>\n  ', '# comment', 'null', '~', '[]', '{}', 'true', '"unterminated'):
            with self.subTest(value=value):
                self.write_skill(self.content.replace("Example skill", value))
                self.assertTrue(self.errors())

    def test_kebab_case(self):
        self.skill.rename(self.skill.with_name("Bad_name"))
        self.assertTrue(self.errors())

    def test_empty_and_missing_inventory(self):
        shutil.rmtree(self.skill)
        self.mirror.unlink()
        self.assertTrue(self.errors())
        self.assertTrue(CHECK.check(self.root / "missing"))

    def test_modules_paths_shallow_and_duplicates(self):
        for config in ('', '[DEFAULT]\npath = vendor/upstream\n',
                       self.config.replace('vendor/upstream', 'outside'),
                       self.config.replace('path = vendor/upstream', 'path = vendor/../outside'),
                       self.config.replace('true', 'false'), self.config.replace('\tshallow = true\n', ''),
                       self.config + self.config.replace('"vendor/upstream"', '"duplicate"')):
            with self.subTest(config=config):
                (self.root / ".gitmodules").write_text(config, encoding="utf-8")
                self.assertTrue(self.errors())

    def test_external_must_belong_to_declared_submodule(self):
        self.external()
        (self.root / ".gitmodules").write_text(self.config.replace("vendor/upstream", "vendor/other"), encoding="utf-8")
        self.assertTrue(self.errors())

    def test_table_missing_duplicate_extra_wrong_type_and_link(self):
        row = self.table.splitlines()[-1] + "\n"
        for table in ('', self.table.replace("## スキル一覧", "## Other"),
                      self.table + "\n## スキル一覧\n", self.table + row,
                      self.table + row.replace("example", "extra"),
                      self.table.replace("自作", "外部"), self.table.replace("SKILL.md)", "README.md)"),
                      self.table.replace("[`example`]", "`example`"), self.table.replace(row, ''),
                      self.table.replace("種類", "Type"), self.table.replace("|---|---|---|", "| x | x | x |")):
            with self.subTest(table=table):
                self.write_table(table)
                self.assertTrue(self.errors())

    def test_cli_failure(self):
        self.write_table("")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        self.assertIn("エラー", result.stdout)


if __name__ == "__main__":
    unittest.main()
