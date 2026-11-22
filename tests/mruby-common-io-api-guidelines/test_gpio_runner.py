import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / ".agents/skills/mruby-common-io-api-guidelines/scripts/gpio-example/run.py"
SPEC = importlib.util.spec_from_file_location("gpio_example_runner", SCRIPT)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def execution(code=0, stdout="", timed_out=False):
    return dict(exit_code=code, stdout=stdout, stderr="", timed_out=timed_out)


class ResultTests(unittest.TestCase):
    def test_repeated_pass(self):
        result = dict(compile=execution(), run=execution(stdout="PASS gpio-contract\n"))
        rows, identical, passed = RUNNER.evaluate([result] * 5)
        self.assertEqual(len(rows), 5)
        self.assertTrue(identical and passed)

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            RUNNER.evaluate([])

    def test_consistent_crash_is_not_success(self):
        result = dict(compile=execution(), run=execution(-11))
        rows, identical, passed = RUNNER.evaluate([result] * 5)
        self.assertEqual(rows[0][0], "RUNTIME_ERROR")
        self.assertTrue(identical)
        self.assertFalse(passed)

    def test_unstable_and_compile_timeout(self):
        ok = dict(compile=execution(), run=execution(stdout="PASS gpio-contract\n"))
        timeout = dict(compile=execution(None, timed_out=True))
        rows, identical, passed = RUNNER.evaluate([ok, timeout])
        self.assertEqual(rows[1][0], "TIMEOUT")
        self.assertFalse(identical or passed)
