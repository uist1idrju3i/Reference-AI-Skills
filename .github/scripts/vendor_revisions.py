"""Fail closed when a committed gitlink differs from its upstream pinned tag."""

import configparser
from pathlib import PurePosixPath
import re
import subprocess


def run_git(root, *arguments):
    try:
        result = subprocess.run(["git", *arguments], cwd=root, text=True,
                                capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        raise ValueError(f"固定版を照合できません: git {arguments[0]}: {error}") from error
    if result.returncode:
        raise ValueError(f"固定版を照合できません: git {arguments[0]}: {result.stderr.strip()}")
    return result.stdout


def tag_commit(root, url, tag):
    ref = f"refs/tags/{tag}"
    run_git(root, "check-ref-format", ref)
    output = run_git(root, "ls-remote", "--exit-code", "--", url, ref, ref + "^{}")
    found = {}
    for line in output.splitlines():
        match = re.fullmatch(r"([0-9a-f]{40})\t(" + re.escape(ref) + r"(?:\^\{\})?)", line)
        if not match or match[2] in found:
            raise ValueError(f"上流タグの応答が不正または重複しています: {tag}")
        found[match[2]] = match[1]
    if ref not in found:
        raise ValueError(f"上流に固定タグがありません: {tag}")
    return found.get(ref + "^{}", found[ref])


def gitlink_commit(root, path):
    output = run_git(root, "ls-tree", "-z", "HEAD", "--", path)
    match = re.fullmatch(r"160000 commit ([0-9a-f]{40})\t" + re.escape(path) + "\0", output)
    if not match:
        raise ValueError(f"HEADに一意なsubmoduleのgitlinkがありません: {path}")
    return match[1]


def verify_revisions(root):
    config = configparser.ConfigParser(interpolation=None)
    try:
        config.read_string((root / ".gitmodules").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, configparser.Error) as error:
        raise ValueError(f"固定版の設定を読み取れません: {error}") from error
    if config.defaults() or not config.sections():
        raise ValueError("固定版のsubmodule設定がありません")
    seen = set()
    for section in config.sections():
        if not re.fullmatch(r'submodule "[^"\n]+"', section):
            raise ValueError(f"submoduleの節が不正です: {section}")
        entry = config[section]
        path = entry.get("path", "")
        parts = PurePosixPath(path).parts
        if (len(parts) < 2 or parts[0] != "vendor" or ".." in parts or "\\" in path
                or str(PurePosixPath(path)) != path or path in seen):
            raise ValueError(f"submoduleのpathが不正または重複しています: {path}")
        seen.add(path)
        if "pinned-tag" not in entry:
            if not entry.get("branch", "").strip():
                raise ValueError(f"{path}: pinned-tagまたは追従branchが必要です")
            continue
        url, tag = entry.get("url", ""), entry["pinned-tag"]
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", url):
            raise ValueError(f"{path}: 固定タグの取得元はGitHubのHTTPS URLにしてください")
        if not tag:
            raise ValueError(f"{path}: pinned-tagが空です")
        actual = gitlink_commit(root, path)
        expected = tag_commit(root, url, tag)
        if actual != expected:
            raise ValueError(f"{path}: gitlink {actual} と固定タグ {tag} のcommit {expected} が一致しません")
