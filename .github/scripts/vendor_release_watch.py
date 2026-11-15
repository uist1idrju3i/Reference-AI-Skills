#!/usr/bin/env python3
"""Watch stable tag series; dry-run is the default and writes are opt-in."""

from __future__ import annotations

import argparse
import configparser
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import quote

from vendor_revisions import verify_revisions


class GitHub:
    def request(self, method, path, payload=None):
        command = ["gh", "api", "--method", method, path]
        if payload is not None:
            command += ["--input", "-"]
        result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                                text=True, capture_output=True, timeout=60, check=False)
        if result.returncode:
            raise ValueError(f"GitHub APIが失敗しました: {method} {path}: {result.stderr.strip()}")
        try:
            return json.loads(result.stdout)
        except ValueError as error:
            raise ValueError(f"GitHub APIの応答がJSONではありません: {path}") from error

    def pages(self, path):
        result = []
        separator = "&" if "?" in path else "?"
        for page in range(1, 101):
            items = self.request("GET", f"{path}{separator}per_page=100&page={page}")
            if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
                raise ValueError(f"GitHub APIの一覧形式が不正です: {path}")
            result.extend(items)
            if len(items) < 100:
                return result
        raise ValueError(f"GitHub APIのページ上限に達しました: {path}")


def repository(url):
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:|https://git-manager\.devin\.ai/proxy/github\.com/)"
        r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?", url)
    if not match:
        raise ValueError(f"GitHubの取得元URLではありません: {url}")
    return match[1]


def modules(root):
    config = configparser.ConfigParser(interpolation=None)
    config.read_string((root / ".gitmodules").read_text(encoding="utf-8"))
    if config.defaults() or not config.sections():
        raise ValueError(".gitmodulesにsubmoduleがありません")
    result = []
    seen = set()
    for section in config.sections():
        if not re.fullmatch(r'submodule "[^"\n]+"', section):
            raise ValueError(f".gitmodulesの節が不正です: {section}")
        entry = config[section]
        path = entry.get("path", "")
        parts = PurePosixPath(path).parts
        if (len(parts) < 2 or parts[0] != "vendor" or ".." in parts or "\\" in path
                or str(PurePosixPath(path)) != path or path in seen):
            raise ValueError(f"submoduleのpathが不正または重複しています: {path}")
        seen.add(path)
        if entry.get("shallow", "").lower() != "true":
            raise ValueError(f"{path}: shallow = trueが必要です")
        if "pinned-tag" not in entry:
            if not entry.get("branch", "").strip():
                raise ValueError(f"{path}: pinned-tagまたは追従branchが必要です")
            continue
        if "tag-prefix" not in entry:
            raise ValueError(f"{path}: tag-prefixがありません")
        repo = repository(entry.get("url", ""))
        tag, prefix = entry["pinned-tag"], entry["tag-prefix"]
        if version(tag, prefix) is None:
            raise ValueError(f"{path}: 固定タグが安定版の系列と一致しません: {tag}")
        result.append({"path": path, "repo": repo, "tag": tag, "prefix": prefix})
    return result


def version(tag, prefix):
    if not isinstance(tag, str):
        return None
    match = re.fullmatch(re.escape(prefix) + r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\+[0-9A-Za-z.-]+)?", tag)
    return tuple(map(int, match.groups())) if match else None


def newest(module, releases, tags):
    blocked = set()
    names = set()
    for release in releases:
        if (not isinstance(release.get("tag_name"), str)
                or type(release.get("draft")) is not bool
                or type(release.get("prerelease")) is not bool):
            raise ValueError(f"{module['path']}: releaseの形式が不正です")
        tag = release["tag_name"]
        if release["draft"] or release["prerelease"]:
            blocked.add(tag)
        else:
            names.add(tag)
    tag_names = set()
    for tag in tags:
        if not isinstance(tag.get("name"), str):
            raise ValueError(f"{module['path']}: tagの形式が不正です")
        tag_names.add(tag["name"])
    if module["tag"] not in tag_names:
        raise ValueError(f"{module['path']}: 固定タグが上流に存在しません: {module['tag']}")
    if module["tag"] in blocked:
        raise ValueError(f"{module['path']}: 固定タグがdraftまたはprereleaseです")
    names.update(tag_names)
    stable = [(version(tag, module["prefix"]), tag) for tag in names - blocked]
    stable = [(number, tag) for number, tag in stable if number is not None]
    if not stable:
        raise ValueError(f"{module['path']}: 対象系列の安定版タグがありません")
    return max(stable)[1]


def marker(path):
    return f"<!-- vendor-release-watch:{path} -->"


def issue_body(module, latest):
    base = f"https://github.com/{module['repo']}"
    compare = f"{base}/compare/{quote(module['tag'], safe='')}...{quote(latest, safe='')}"
    return (f"{marker(module['path'])}\n\n"
            f"`{module['path']}`に新しい安定版候補があります。\n\n"
            f"- 固定タグ: `{module['tag']}`\n- 候補タグ: `{latest}`\n"
            f"- 監視する接頭辞: `{module['prefix']}`\n- [変更差分]({compare})\n\n"
            "更新は自動適用しません。変更履歴全体、互換性、新機能・設定の採否、"
            "ライセンスと回帰検査を確認してください。このIssueは自動で閉じません。\n")


def watch(api, entries, target, write=False):
    updates = []
    lines = []
    for module in entries:
        upstream = f"repos/{module['repo']}"
        latest = newest(module, api.pages(upstream + "/releases"), api.pages(upstream + "/tags"))
        newer = version(latest, module["prefix"]) > version(module["tag"], module["prefix"])
        state = "更新候補" if newer else "更新なし"
        lines.append(f"{module['path']}: {module['tag']} → {latest}（{state}）")
        if newer:
            updates.append((module, latest))
    if not entries:
        lines.append("タグ固定のsubmoduleはありません（書き込みなし）")
    if not write:
        return ["dry-run: Issueへの書き込みは行いません", *lines,
                f"更新候補: {len(updates)}件"]
    plans = []
    if updates:
        issues = api.pages(f"repos/{target}/issues?state=all")
        if any(issue.get("body") is not None and not isinstance(issue["body"], str) for issue in issues):
            raise ValueError("通知先Issueの本文形式が不正です")
        for module, latest in updates:
            matches = [issue for issue in issues if "pull_request" not in issue
                       and marker(module["path"]) in (issue.get("body") or "")]
            if len(matches) > 1:
                raise ValueError(f"{module['path']}: 通知Issueが重複しています")
            number = matches[0].get("number") if matches else None
            if matches and (type(number) is not int or number < 1):
                raise ValueError(f"{module['path']}: Issue番号が不正です")
            payload = {"title": f"依存更新: {module['path']} の新しい固定候補",
                       "body": issue_body(module, latest)}
            if number is not None:
                payload["state"] = "open"
            plans.append((number, payload))
    # Finish all upstream reads and issue validation before the first write.
    for number, payload in plans:
        path = f"repos/{target}/issues" + (f"/{number}" if number is not None else "")
        api.request("PATCH" if number is not None else "POST", path, payload)
    return [*lines, f"通知Issueの作成・更新: {len(plans)}件（自動closeなし）"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="照会のみ（既定）")
    modes.add_argument("--write", action="store_true", help="このリポジトリの通知Issueを作成・更新")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        verify_revisions(root)
        origin = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                                check=True, text=True, capture_output=True, timeout=15).stdout.strip()
        lines = watch(GitHub(), modules(root), repository(origin), args.write)
    except (OSError, ValueError, configparser.Error, subprocess.SubprocessError) as error:
        print(f"タグ更新確認エラー: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
