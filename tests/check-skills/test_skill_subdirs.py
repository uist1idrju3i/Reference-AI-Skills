import unittest

import test_check_skills


class SkillSubdirectoryTests(unittest.TestCase):
    def test_scripts_and_references_are_accepted(self):
        fixture = test_check_skills.SkillsTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        for directory, name in (("scripts", "probe.py"), ("references", "compatibility.md")):
            child = fixture.skill / directory
            child.mkdir()
            (child / name).write_text("Example\n", encoding="utf-8")
        self.assertEqual([], fixture.errors())
