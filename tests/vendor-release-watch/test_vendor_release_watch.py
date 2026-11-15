"""Mock GitHub responses so notification tests never contact a service."""

import importlib.util
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/vendor_release_watch.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("vendor_release_watch", SCRIPT)
WATCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WATCH)
MODULE = {"path": "vendor/example", "repo": "owner/example", "tag": "v1.0.0", "prefix": "v"}


class FakeAPI:
    def __init__(self, releases=None, tags=None, issues=None, fail=None):
        self.releases = releases if releases is not None else []
        self.tags = tags if tags is not None else [{"name": "v1.0.0"}, {"name": "v1.1.0"}]
        self.issues = issues if issues is not None else []
        self.fail = fail
        self.writes = []

    def pages(self, path):
        if self.fail and self.fail in path:
            raise ValueError("API failure")
        if path.endswith("/releases"):
            return self.releases
        if path.endswith("/tags"):
            return self.tags
        if "/issues?" in path:
            return self.issues
        raise AssertionError(path)

    def request(self, method, path, payload):
        self.writes.append((method, path, payload))
        return {"number": 1}


class WatchTest(unittest.TestCase):
    def test_revision_drift_blocks_cli_before_any_api_access(self):
        with patch.object(WATCH, "verify_revisions", side_effect=ValueError("gitlink mismatch")), \
                patch.object(WATCH, "GitHub") as api, \
                patch.object(sys, "argv", [str(SCRIPT), "--write"]), \
                contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(1, WATCH.main())
            api.assert_not_called()
            self.assertIn("gitlink mismatch", errors.getvalue())

    def test_semantic_versions_and_series(self):
        for tag in ("v2.0.0-rc.1", "v1.0", "other@9.0.0", "v01.0.0", "v1.0.0-extra"):
            self.assertIsNone(WATCH.version(tag, "v"))
        self.assertEqual((2, 0, 1), WATCH.version("mcpb-v2.0.1", "mcpb-v"))
        tags = [{"name": name} for name in ("v1.0.0", "v1.9.0", "v1.10.0", "v2.0.0-beta", "ctx7@99.0.0")]
        self.assertEqual("v1.10.0", WATCH.newest(MODULE, [], tags))

    def test_tag_only_repo_and_release_union(self):
        self.assertEqual("v1.1.0", WATCH.newest(MODULE, [], FakeAPI().tags))
        releases = [{"tag_name": "v1.2.0", "draft": False, "prerelease": False}]
        self.assertEqual("v1.2.0", WATCH.newest(MODULE, releases, FakeAPI().tags))

    def test_prerelease_and_draft_flags_override_stable_looking_tags(self):
        releases = [{"tag_name": "v2.0.0", "draft": False, "prerelease": True},
                    {"tag_name": "v3.0.0", "draft": True, "prerelease": False}]
        tags = FakeAPI().tags + [{"name": "v2.0.0"}, {"name": "v3.0.0"}]
        self.assertEqual("v1.1.0", WATCH.newest(MODULE, releases, tags))

    def test_empty_missing_or_malformed_data_fails_closed(self):
        for releases, tags in (([], []), ([], [{"name": "v2.0.0"}]), ([], [{}]),
                               ([{}], FakeAPI().tags),
                               ([{"tag_name": "v1.0.0", "draft": False, "prerelease": True}], FakeAPI().tags)):
            with self.subTest(releases=releases, tags=tags), self.assertRaises(ValueError):
                WATCH.newest(MODULE, releases, tags)

    def test_dry_run_never_writes(self):
        api = FakeAPI()
        result = WATCH.watch(api, [MODULE], "template/repo")
        self.assertIn("更新候補: 1件", result)
        self.assertEqual([], api.writes)

    def test_no_update_no_write(self):
        api = FakeAPI(tags=[{"name": "v1.0.0"}])
        result = WATCH.watch(api, [MODULE], "template/repo", write=True)
        self.assertIn("通知Issueの作成・更新: 0件（自動closeなし）", result)
        self.assertEqual([], api.writes)

    def test_empty_entries(self):
        api = FakeAPI()
        self.assertIn("更新候補: 0件", WATCH.watch(api, [], "template/repo"))
        self.assertEqual([], api.writes)

    def test_create_issue_in_target_only(self):
        api = FakeAPI()
        WATCH.watch(api, [MODULE], "template/repo", write=True)
        method, path, body = api.writes[0]
        self.assertEqual(("POST", "repos/template/repo/issues"), (method, path))
        self.assertIn("依存更新:", body["title"])
        self.assertIn(WATCH.marker(MODULE["path"]), body["body"])
        self.assertIn("/compare/v1.0.0...v1.1.0", body["body"])
        self.assertNotIn("state", body)

    def test_update_and_reopen_existing_issue(self):
        for state in ("open", "closed"):
            api = FakeAPI(issues=[{"number": 9, "state": state, "body": WATCH.marker(MODULE["path"])}])
            WATCH.watch(api, [MODULE], "template/repo", write=True)
            self.assertEqual(("PATCH", "repos/template/repo/issues/9"), api.writes[0][:2])
            self.assertEqual("open", api.writes[0][2]["state"])

    def test_ignore_pull_requests_and_unrelated_issues(self):
        api = FakeAPI(issues=[{"number": 3, "body": "unrelated"},
                             {"number": 4, "body": WATCH.marker(MODULE["path"]), "pull_request": {}}])
        WATCH.watch(api, [MODULE], "template/repo", write=True)
        self.assertEqual("POST", api.writes[0][0])

    def test_duplicate_or_bad_issue_ids_block_writes(self):
        issue = {"number": 9, "body": WATCH.marker(MODULE["path"])}
        for issues in ([issue, issue], [{**issue, "number": "9"}], [{**issue, "body": 42}]):
            api = FakeAPI(issues=issues)
            with self.assertRaises(ValueError):
                WATCH.watch(api, [MODULE], "template/repo", write=True)
            self.assertEqual([], api.writes)

    def test_api_failures_block_all_writes(self):
        for endpoint in ("releases", "tags", "issues"):
            api = FakeAPI(fail=endpoint)
            with self.assertRaises(ValueError):
                WATCH.watch(api, [MODULE], "template/repo", write=True)
            self.assertEqual([], api.writes)
        api = FakeAPI(fail="owner/broken")
        with self.assertRaises(ValueError):
            WATCH.watch(api, [MODULE, {**MODULE, "repo": "owner/broken"}], "template/repo", write=True)
        self.assertEqual([], api.writes)

    def test_url_parsing_and_compare_encoding(self):
        for url in ("https://github.com/owner/repo.git", "git@github.com:owner/repo.git",
                    "https://git-manager.devin.ai/proxy/github.com/owner/repo"):
            self.assertEqual("owner/repo", WATCH.repository(url))
        with self.assertRaises(ValueError):
            WATCH.repository("https://example.com/owner/repo")
        with self.assertRaises(ValueError):
            WATCH.repository("https://evilgithub.com/owner/repo")
        module = {**MODULE, "tag": "@pkg/tool@1.0.0", "prefix": "@pkg/tool@"}
        self.assertIn("%40pkg%2Ftool%401.0.0", WATCH.issue_body(module, "@pkg/tool@1.1.0"))

    def test_submodule_metadata_and_branch_tracking(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / ".gitmodules"
            valid = ('[submodule "vendor/example"]\npath = vendor/example\n'
                     'url = https://github.com/owner/example.git\nshallow = true\n'
                     'pinned-tag = v1.0.0\ntag-prefix = v\n')
            path.write_text(valid, encoding="utf-8")
            self.assertEqual([MODULE], WATCH.modules(root))
            path.write_text(valid.replace('pinned-tag = v1.0.0\ntag-prefix = v', 'branch = main'), encoding="utf-8")
            self.assertEqual([], WATCH.modules(root))
            for value in ('', valid.replace('true', 'false'), valid.replace('tag-prefix = v', ''),
                          valid.replace('v1.0.0', 'v1.1.0-rc.1'), valid.replace('path = vendor/example', 'path = ../escape'),
                          valid.replace('pinned-tag = v1.0.0', ''), valid + valid):
                path.write_text(value, encoding="utf-8")
                with self.subTest(value=value), self.assertRaises((ValueError, WATCH.configparser.Error)):
                    WATCH.modules(root)

    def test_pagination(self):
        api = WATCH.GitHub()
        with patch.object(api, "request", side_effect=[[{"name": "tag"}] * 100, [{"name": "last"}]]) as request:
            self.assertEqual(101, len(api.pages("repos/owner/repo/tags")))
            self.assertTrue(request.call_args.args[1].endswith("page=2"))
        with patch.object(api, "request", return_value={"message": "error"}), self.assertRaises(ValueError):
            api.pages("repos/owner/repo/tags")

    def test_request_error_bad_json_timeout_and_payload(self):
        api = WATCH.GitHub()
        with patch.object(WATCH.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, '', 'API refused')):
            with self.assertRaises(ValueError):
                api.request("GET", "repos/owner/repo/tags")
        with patch.object(WATCH.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, 'not JSON', '')):
            with self.assertRaises(ValueError):
                api.request("GET", "repos/owner/repo/tags")
        with patch.object(WATCH.subprocess, "run", side_effect=subprocess.TimeoutExpired('gh', 60)):
            with self.assertRaises(subprocess.TimeoutExpired):
                api.request("GET", "repos/owner/repo/tags")
        with patch.object(WATCH.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"number":1}', '')) as run:
            self.assertEqual({"number": 1}, api.request("POST", "repos/template/repo/issues", {"title": "更新"}))
            self.assertEqual({"title": "更新"}, json.loads(run.call_args.kwargs["input"]))


if __name__ == "__main__":
    unittest.main()
