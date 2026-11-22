import csv
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       ".agents/skills/mruby-idiomatic/scripts"))
import probe_mrubyc as probe


def result(code=0, stdout="", stderr="", timed_out=False):
    return dict(exit_code=code, stdout=stdout, stderr=stderr, timed_out=timed_out)


class ClassificationTests(unittest.TestCase):
    def test_exact_pass(self):
        self.assertEqual(probe.classify("x", result(), result(stdout="PASS x\n")), ("PASS", 0, "PASS x"))

    def test_empty_output_is_not_pass(self):
        self.assertEqual(probe.classify("x", result(), result()), ("FAIL", 0, "missing PASS marker"))

    def test_extra_output_is_not_pass(self):
        self.assertEqual(probe.classify("x", result(), result(stdout="PASS x\nnoise\n"))[0], "FAIL")
        self.assertEqual(probe.classify("x", result(), result(stdout="PASS x\n", stderr="warning"))[0], "FAIL")

    def test_wrong_id_is_not_pass(self):
        self.assertEqual(probe.classify("x", result(), result(stdout="PASS y\n"))[0], "FAIL")

    def test_fail_assertion_even_with_nonzero_exit(self):
        self.assertEqual(probe.classify("x", result(), result(2, "FAIL x nil case\nexception\n")), ("FAIL", 2, "FAIL x nil case"))

    def test_compile_error(self):
        self.assertEqual(probe.classify("x", result(1, stderr="syntax error\nmore")), ("COMPILE_ERROR", 1, "syntax error"))

    def test_runtime_error(self):
        self.assertEqual(probe.classify("x", result(), result(2, "NoMethodError\n")), ("RUNTIME_ERROR", 2, "NoMethodError"))

    def test_marker_before_crash_is_not_pass(self):
        self.assertEqual(probe.classify("x", result(), result(-11, "PASS x\n"))[0], "RUNTIME_ERROR")

    def test_compile_timeout(self):
        self.assertEqual(probe.classify("x", result(None, timed_out=True)), ("TIMEOUT", None, "compile timeout"))

    def test_runtime_timeout(self):
        self.assertEqual(probe.classify("x", result(), result(None, timed_out=True)), ("TIMEOUT", None, "runtime timeout"))


class EvidenceTests(unittest.TestCase):
    def test_recorded_probe_inventory_and_document_links(self):
        skill = Path(probe.__file__).resolve().parent.parent
        probes = {path.stem for path in (skill / "scripts/probes").glob("*.rb")}
        expected = probe.read_expected(skill / "scripts/expected.csv", probes)
        alternatives = {name for name in probes if name.startswith("alt-")}
        self.assertTrue(alternatives)
        self.assertTrue(all(expected[name] == "PASS" for name in alternatives))
        for path in (skill / "SKILL.md", skill / "references/compatibility.md",
                     skill / "references/principles.md"):
            content = path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in link:
                    self.assertTrue((path.parent / link.split("#")[0]).exists(), link)
        table = (skill / "references/compatibility.md").read_text(encoding="utf-8")
        for name in probes - alternatives:
            self.assertIn("../scripts/probes/" + name + ".rb", table)

    def test_actual_timeout_retains_partial_output(self):
        output = probe.execute([sys.executable, "-c", "import time; print('partial', flush=True); time.sleep(10)"], 0.1)
        self.assertTrue(output["timed_out"])
        self.assertEqual(output["stdout"], "partial\n")
        self.assertIsNone(output["exit_code"])

    def test_actual_exit_code_and_streams(self):
        output = probe.execute([sys.executable, "-c", "import sys; print('out'); print('err',file=sys.stderr); sys.exit(3)"], 5)
        self.assertEqual(output["exit_code"], 3)
        self.assertEqual(output["stdout"], "out\n")
        self.assertEqual(output["stderr"], "err\n")

    def test_expected_and_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.csv"
            rows = [dict(id="x", status="PASS", exit_code=0, diagnostic="PASS x")]
            probe.write_csv(path, rows)
            self.assertEqual(probe.read_expected(path, ["x"]), {"x": "PASS"})
            with path.open(newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream))[0]["diagnostic"], "PASS x")
            with self.assertRaises(ValueError):
                probe.read_expected(path, ["y"])

    def test_bad_expected_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.csv"
            for text in ("id,status\nx,MAYBE\n", "id,status\nx,PASS\nx,FAIL\n", "wrong,columns\n"):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    probe.read_expected(path, ["x"])

    def test_positive_repeat(self):
        self.assertEqual(probe.positive_int("5"), 5)
        for value in ("0", "-1"):
            with self.assertRaises(probe.argparse.ArgumentTypeError):
                probe.positive_int(value)

    def test_repeats_and_expected_comparison(self):
        row = dict(id="x", status="PASS", exit_code=0, diagnostic="PASS x")
        other = dict(row, status="FAIL", diagnostic="FAIL x wrong")
        self.assertEqual(probe.compare_results([[row]] * 5, None), ([], []))
        self.assertEqual(probe.compare_results([[row], [other]], {"x": "PASS"}), (["x"], []))
        self.assertEqual(probe.compare_results([[row]], {"x": "FAIL"}), ([], ["x"]))


if __name__ == "__main__":
    unittest.main()
