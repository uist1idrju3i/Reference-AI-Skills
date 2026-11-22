import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".agents/skills/mrubyc-c-binding"
SCRIPT = SKILL / "scripts/run.py"
SPEC = importlib.util.spec_from_file_location("c_binding_runner", SCRIPT)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
EXPECTED = RUNNER.read_expected(SKILL / "scripts/expected.json")


def execution(code=0, stdout="", stderr="", timed_out=False):
    return dict(exit_code=code, stdout=stdout, stderr=stderr, timed_out=timed_out)


def good_run(lines=None):
    return dict(compile=execution(), run=execution(stdout="\n".join(EXPECTED if lines is None else lines) + "\n"))


class ResultTests(unittest.TestCase):
    def test_five_passes(self):
        rows, identical, passed = RUNNER.evaluate([good_run()] * 5, EXPECTED)
        self.assertEqual(rows, [("PASS", 0, "PASS binding-contract")] * 5)
        self.assertTrue(identical and passed)

    def test_line_order_independent(self):
        rows, identical, passed = RUNNER.evaluate([good_run(), good_run(EXPECTED[::-1])], EXPECTED)
        self.assertTrue(identical and passed)

    def test_empty_runs(self):
        with self.assertRaises(ValueError):
            RUNNER.evaluate([], EXPECTED)

    def test_missing_extra_duplicate_and_marker_only_fail(self):
        for lines in ([], EXPECTED[1:], EXPECTED + [EXPECTED[0]],
                      EXPECTED + ["noise"], ["PASS ALL binding-contract"]):
            with self.subTest(lines=lines):
                self.assertEqual(RUNNER.classify_run(good_run(lines), EXPECTED)[0], "FAIL")

    def test_stderr_fails(self):
        run = good_run()
        run["run"]["stderr"] = "Exception"
        self.assertEqual(RUNNER.classify_run(run, EXPECTED)[0], "FAIL")

    def test_keyword_guard_evidence_is_required(self):
        checks = ["PASS keyword guard " + suffix for suffix in (
            "missing rescued", "missing no side effects",
            "unknown rescued", "unknown no side effects",
            "wrong type rescued", "wrong type no side effects",
            "normal", "normal one side effect")]
        for line in checks:
            with self.subTest(line=line):
                self.assertIn(line, EXPECTED)
                incomplete = [item for item in EXPECTED if item != line]
                self.assertEqual(RUNNER.classify_run(good_run(incomplete), EXPECTED)[0], "FAIL")

    def test_public_value_type_evidence_is_required(self):
        names = ("nil", "false", "true", "Integer", "Float", "Symbol", "Class", "Module",
                 "Object", "Proc", "Array", "String", "Range", "Hash", "Exception")
        for name in names:
            line = "PASS typed " + name + " contract"
            with self.subTest(name=name):
                self.assertIn(line, EXPECTED)
                incomplete = [item for item in EXPECTED if item != line]
                self.assertEqual(RUNNER.classify_run(good_run(incomplete), EXPECTED)[0], "FAIL")

    def test_crash_even_with_all_pass_markers_fails(self):
        run = good_run()
        run["run"]["exit_code"] = -11
        self.assertEqual(RUNNER.classify_run(run, EXPECTED)[0], "RUNTIME_ERROR")

    def test_runtime_timeout(self):
        run = good_run()
        run["run"].update(timed_out=True, exit_code=None)
        self.assertEqual(RUNNER.classify_run(run, EXPECTED)[0], "TIMEOUT")

    def test_compile_failure_and_timeout(self):
        for result, status in ((execution(1, stderr="syntax"), "COMPILE_ERROR"),
                               (execution(None, timed_out=True), "TIMEOUT")):
            self.assertEqual(RUNNER.classify_run(dict(compile=result), EXPECTED)[0], status)

    def test_missing_runtime_rejected(self):
        with self.assertRaises(ValueError):
            RUNNER.classify_run(dict(compile=execution()), EXPECTED)

    def test_consistent_failure_and_unstable_are_not_success(self):
        failed = good_run([])
        _, identical, passed = RUNNER.evaluate([failed] * 5, EXPECTED)
        self.assertTrue(identical)
        self.assertFalse(passed)
        _, identical, passed = RUNNER.evaluate([good_run(), failed], EXPECTED)
        self.assertFalse(identical or passed)

    def test_invalid_expected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.json"
            for value in ([], {}, ["PASS a"], ["PASS ALL binding-contract"] * 2,
                          [1], ["FAIL a"], ["PASS a\n", "PASS ALL binding-contract"]):
                with self.subTest(value=value):
                    path.write_text(json.dumps(value))
                    with self.assertRaises(ValueError):
                        RUNNER.read_expected(path)
            path.write_text("not json")
            with self.assertRaises(ValueError):
                RUNNER.read_expected(path)

    def test_cli_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "already-there"
            output.mkdir()
            sentinel = output / "keep"
            sentinel.write_text("original")
            result = subprocess.run([sys.executable, str(SCRIPT), "--mrubyc", directory + "/source",
                                     "--mrbc", directory + "/mrbc", "--out", str(output)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("output already exists", result.stderr)
            self.assertEqual(sentinel.read_text(), "original")

    def test_expected_fixture_and_docs_stay_in_sync(self):
        fixture = (SKILL / "scripts/contract.rb").read_text()
        binding = "\n".join(path.read_text() for path in (SKILL / "scripts").glob("*.c"))
        for line in EXPECTED:
            if line == "PASS ALL binding-contract":
                self.assertIn(line, fixture)
            else:
                self.assertTrue(line in binding or '"' + line[5:] + '"' in fixture, line)
        docs = "\n".join(path.read_text() for path in SKILL.rglob("*.md"))
        self.assertNotIn("/home/", docs)
        self.assertNotIn("load_bytecode", docs)
        self.assertNotIn("NULL検査順", docs)
        for path in (SKILL / "SKILL.md", SKILL / "references/api.md", SKILL / "references/patterns.md"):
            self.assertTrue(path.is_file())
