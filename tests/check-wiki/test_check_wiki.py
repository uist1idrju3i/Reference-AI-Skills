"""DeepWiki schema, boundary, and graph negative controls."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/check-wiki.py"
SPEC = importlib.util.spec_from_file_location("check_wiki", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class WikiTest(unittest.TestCase):
    def setUp(self):
        self.config = {"repo_notes": [{"content": "根拠を確認する"}], "pages": [
            {"title": "概要", "purpose": "目的を説明する", "page_notes": [{"content": "Read sources", "author": "editor"}]},
            {"title": "検査", "purpose": "手順を説明する", "parent": "概要"}]}

    def test_valid(self):
        self.assertEqual((2, 2), CHECK.validate(self.config))

    def test_minimal_with_empty_notes(self):
        self.assertEqual((1, 0), CHECK.validate({"repo_notes": [], "pages": [{"title": "A", "purpose": "B"}]}))

    def test_page_boundaries_and_override(self):
        for count, maximum in [(1, 30), (30, 30), (31, 31)]:
            self.config["pages"] = [{"title": str(i), "purpose": "purpose"} for i in range(count)]
            self.assertEqual(count, CHECK.validate(self.config, maximum)[0])
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)
        self.config["pages"] = []
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)

    def test_total_notes_boundary(self):
        self.config["repo_notes"] = [{"content": "a"}] * 99
        self.assertEqual(100, CHECK.validate(self.config)[1])
        self.config["pages"][1]["page_notes"] = [{"content": "b"}]
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)

    def test_note_character_boundary(self):
        self.config["repo_notes"][0]["content"] = "文" * 10000
        CHECK.validate(self.config)
        self.config["repo_notes"][0]["content"] += "字"
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)

    def test_required_and_unknown_keys_at_every_level(self):
        for path, required in [((), "pages"), ((), "repo_notes"), (("pages", 0), "title"),
                               (("pages", 0), "purpose"), (("repo_notes", 0), "content")]:
            for unknown in (False, True):
                config = copy.deepcopy(self.config)
                node = config
                for key in path:
                    node = node[key]
                if unknown:
                    node["unknown"] = "unexpected"
                else:
                    del node[required]
                with self.subTest(path=path, unknown=unknown), self.assertRaises(ValueError):
                    CHECK.validate(config)

    def test_invalid_types_and_empty_text(self):
        for path in [("repo_notes",), ("pages",), ("repo_notes", 0), ("repo_notes", 0, "content"),
                     ("pages", 0), ("pages", 0, "title"), ("pages", 0, "purpose"),
                     ("pages", 0, "page_notes"), ("pages", 0, "page_notes", 0, "author"),
                     ("pages", 1, "parent")]:
            for value in (None, 42, "", " ", {}):
                config = copy.deepcopy(self.config)
                node = config
                for key in path[:-1]:
                    node = node[key]
                node[path[-1]] = value
                with self.subTest(path=path, value=value), self.assertRaises(ValueError):
                    CHECK.validate(config)

    def test_duplicate_title_and_parent_graph(self):
        for parent in ("missing", "検査"):
            self.config["pages"][1]["parent"] = parent
            with self.assertRaises(ValueError):
                CHECK.validate(self.config)
        self.config["pages"][1]["parent"] = "概要"
        self.config["pages"][0]["parent"] = "検査"
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)
        del self.config["pages"][0]["parent"]
        self.config["pages"][1]["title"] = "概要"
        with self.assertRaises(ValueError):
            CHECK.validate(self.config)

    def test_invalid_limit(self):
        for limit in (0, -1, True, "30"):
            with self.assertRaises(ValueError):
                CHECK.validate(self.config, limit)

    def test_json_errors_and_cli_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "wiki.json"
            for value in ('{', '{"repo_notes":[],"repo_notes":[],"pages":[]}', '{"pages":NaN}', '{"pages":Infinity}'):
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    CHECK.load_config(path)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("Wiki検査エラー", result.stderr)

    def test_cli_success_and_configurable_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "wiki.json"
            path.write_text(json.dumps(self.config), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-pages", "1"], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
