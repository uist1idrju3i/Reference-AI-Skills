"""Mock remote refs and gitlinks, including annotated tags and drift."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/vendor_revisions.py"
SPEC = importlib.util.spec_from_file_location("vendor_revisions_tests", SCRIPT)
REVISIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVISIONS)
SHA = "a" * 40
OTHER = "b" * 40
URL = "https://github.com/owner/example.git"
REF = "refs/tags/v1.0.0"


class RevisionTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = ('[submodule "vendor/example"]\npath = vendor/example\n'
                       f'url = {URL}\nshallow = true\npinned-tag = v1.0.0\n')
        (self.root / ".gitmodules").write_text(self.config, encoding="utf-8")

    def test_lightweight_and_annotated_tags(self):
        for output in (f"{SHA}\t{REF}\n", f"{OTHER}\t{REF}\n{SHA}\t{REF}^{{}}\n",
                       f"{SHA}\t{REF}^{{}}\n{OTHER}\t{REF}\n"):
            with patch.object(REVISIONS, "run_git", side_effect=["", output]) as run:
                self.assertEqual(SHA, REVISIONS.tag_commit(self.root, URL, "v1.0.0"))
                self.assertEqual((self.root, "ls-remote", "--exit-code", "--", URL, REF, REF + "^{}"), run.call_args.args)

    def test_empty_wrong_duplicate_or_malformed_refs(self):
        for output in ("", "bad JSON", f"{SHA}\trefs/heads/main\n", f"{SHA}\t{REF}^{{}}\n",
                       f"{SHA}\t{REF}\n{SHA}\t{REF}\n", f"short\t{REF}\n",
                       f"{SHA}\t{REF}\n{OTHER}\trefs/tags/unexpected\n"):
            with self.subTest(output=output), patch.object(REVISIONS, "run_git", side_effect=["", output]), self.assertRaises(ValueError):
                REVISIONS.tag_commit(self.root, URL, "v1.0.0")

    def test_gitlink_requires_exact_committed_path_and_mode(self):
        with patch.object(REVISIONS, "run_git", return_value=f"160000 commit {SHA}\tvendor/example\0"):
            self.assertEqual(SHA, REVISIONS.gitlink_commit(self.root, "vendor/example"))
        for output in ("", f"040000 tree {SHA}\tvendor/example\0",
                       f"160000 commit {SHA}\tvendor/other\0", f"160000 commit {SHA}\tvendor/example\n"):
            with patch.object(REVISIONS, "run_git", return_value=output), self.assertRaises(ValueError):
                REVISIONS.gitlink_commit(self.root, "vendor/example")

    def test_matching_gitlink_and_drift(self):
        with patch.object(REVISIONS, "gitlink_commit", return_value=SHA), patch.object(REVISIONS, "tag_commit", return_value=SHA):
            REVISIONS.verify_revisions(self.root)
        with patch.object(REVISIONS, "gitlink_commit", return_value=OTHER), patch.object(REVISIONS, "tag_commit", return_value=SHA), self.assertRaisesRegex(ValueError, "一致しません"):
            REVISIONS.verify_revisions(self.root)

    def test_branch_tracking_does_not_query_a_tag(self):
        (self.root / ".gitmodules").write_text(self.config.replace("pinned-tag = v1.0.0", "branch = main"), encoding="utf-8")
        with patch.object(REVISIONS, "run_git") as run:
            REVISIONS.verify_revisions(self.root)
            run.assert_not_called()

    def test_missing_config_or_metadata_is_rejected(self):
        with self.assertRaises(ValueError):
            REVISIONS.verify_revisions(self.root / "missing")
        for config in ("", "[DEFAULT]\npath = vendor/example\n", self.config + self.config,
                       self.config.replace("pinned-tag = v1.0.0", "pinned-tag ="),
                       self.config.replace("pinned-tag = v1.0.0", ""),
                       self.config.replace("path = vendor/example", "path = vendor/../escape"),
                       self.config.replace(URL, "ext::execute-a-command")):
            (self.root / ".gitmodules").write_text(config, encoding="utf-8")
            with self.subTest(config=config), self.assertRaises(ValueError):
                REVISIONS.verify_revisions(self.root)

    def test_network_errors_timeout_and_missing_git_fail_closed(self):
        for outcome in (subprocess.CompletedProcess([], 128, "", "connection refused"),
                        subprocess.TimeoutExpired("git", 60), FileNotFoundError("git missing")):
            kwargs = {"side_effect": outcome} if isinstance(outcome, Exception) else {"return_value": outcome}
            with patch.object(REVISIONS.subprocess, "run", **kwargs), self.assertRaises(ValueError):
                REVISIONS.tag_commit(self.root, URL, "v1.0.0")


if __name__ == "__main__":
    unittest.main()
