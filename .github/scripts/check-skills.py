#!/usr/bin/env python3
"""Validate canonical skills, vendor boundaries, mirrors, and the README table."""

from __future__ import annotations

import argparse
import configparser
import json
import os
from pathlib import Path, PurePosixPath
import re

from vendor_revisions import verify_revisions


NAME = r"[a-z0-9]+(?:-[a-z0-9]+)*"
YAML_NUMBER = re.compile(
    r"[-+]?(?:0b[01]+|0o[0-7]+|0x[0-9a-f]+|(?:\d[\d_]*(?:\.[\d_]*)?|\.[\d_]+)(?:e[-+]?\d+)?"
    r"|\.(?:inf|nan)|\d[\d_]*(?::[0-5]?\d)+(?:\.[\d_]*)?)", re.IGNORECASE)


def scalar(value: str, continuation: list[str]) -> str:
    value = value.strip()
    if value.startswith("#"):
        return ""
    if value.startswith('"'):
        result, end = json.JSONDecoder().raw_decode(value)
        suffix = value[end:].strip()
        if not isinstance(result, str) or (suffix and not suffix.startswith("#")):
            raise ValueError("文字列ではありません")
        return result.strip()
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(?:\s+#.*)?", value)
        if not match:
            raise ValueError("引用符が閉じていません")
        return match[1].replace("''", "'").strip()
    value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
    if re.fullmatch(r"[>|][+-]?", value):
        return " ".join(line.strip() for line in continuation).strip()
    if (value.lower() in ("null", "~", "true", "false", "yes", "no", "on", "off")
            or YAML_NUMBER.fullmatch(value) or value.startswith(("[", "{"))):
        raise ValueError("文字列ではありません")
    return value


def metadata(content: str, name: str) -> list[str]:
    lines = content.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return [f"{name}: SKILL.mdにfrontmatterがありません"]
    header = lines[1:lines.index("---", 1)]
    fields: dict[str, list[str]] = {"name": [], "description": []}
    try:
        for i, line in enumerate(header):
            match = re.fullmatch(r"(name|description):\s*(.*)", line)
            if not match:
                continue
            following = []
            for rest in header[i + 1:]:
                if rest and not rest[0].isspace():
                    break
                following.append(rest)
            fields[match[1]].append(scalar(match[2], following))
    except (ValueError, TypeError) as error:
        return [f"{name}: frontmatterの文字列が不正です: {error}"]
    errors = []
    if fields["name"] != [name]:
        errors.append(f"{name}: frontmatterのnameはディレクトリ名と一致する1件が必要です")
    if len(fields["description"]) != 1 or not fields["description"][0]:
        errors.append(f"{name}: descriptionは空でない文字列が1件必要です")
    return errors


def submodules(root: Path) -> tuple[list[str], list[str]]:
    errors = []
    paths = []
    config = configparser.ConfigParser(interpolation=None)
    try:
        config.read_string((root / ".gitmodules").read_text(encoding="utf-8"))
        if config.defaults() or not config.sections():
            raise ValueError("submoduleの定義がありません")
        for section in config.sections():
            if not re.fullmatch(r'submodule "[^"\n]+"', section):
                errors.append(f".gitmodules: 不正な節です: {section}")
            entry = config[section]
            path = entry.get("path", "")
            parts = PurePosixPath(path).parts
            if (len(parts) < 2 or parts[0] != "vendor" or ".." in parts
                    or str(PurePosixPath(path)) != path or "\\" in path):
                errors.append(f".gitmodules: submoduleはvendor/配下に置いてください: {path}")
            else:
                paths.append(path)
            if entry.get("shallow", "").lower() != "true":
                errors.append(f".gitmodules: {path}: shallow = trueが必要です")
        if len(paths) != len(set(paths)):
            errors.append(".gitmodules: submoduleのpathが重複しています")
    except (OSError, UnicodeError, configparser.Error, ValueError) as error:
        errors.append(f".gitmodulesを読み取れません: {error}")
    return errors, paths


def inventory_table(text: str, kinds: dict[str, str]) -> list[str]:
    errors = []
    lines = text.splitlines()
    headings = [i for i, line in enumerate(lines) if line.strip() == "## スキル一覧"]
    if len(headings) != 1:
        return ["README.md: 「## スキル一覧」は1節だけ必要です"]
    section = []
    for line in lines[headings[0] + 1:]:
        if re.match(r"^#{1,2}\s", line):
            break
        section.append(line)
    rows = [line for line in section if line.lstrip().startswith("|")]
    if len(rows) < 2:
        return ["README.md: スキル一覧の表がありません"]
    cells = lambda line: [cell.strip() for cell in line.strip().strip("|").split("|")]
    header = cells(rows[0])
    if not header or header[0] != "スキル" or header.count("種類") != 1:
        return ["README.md: 表の先頭列はスキル、種類列は1列だけ必要です"]
    if len(cells(rows[1])) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in cells(rows[1])):
        errors.append("README.md: 表の区切り行が不正です")
    found = []
    for row in rows[2:]:
        values = cells(row)
        if len(values) != len(header):
            errors.append("README.md: スキル表の列数が一致しません")
            continue
        match = re.fullmatch(rf"\[`({NAME})`\]\(\.agents/skills/\1/SKILL\.md\)", values[0])
        if not match:
            errors.append(f"README.md: スキルリンクの形式が不正です: {values[0]}")
            continue
        name = match[1]
        found.append(name)
        if values[header.index("種類")] != kinds.get(name):
            errors.append(f"README.md: {name}: 種類は実体に応じた自作／外部を指定してください")
    if sorted(found) != sorted(kinds):
        errors.append("README.md: 正本スキルを過不足・重複なく1回ずつ列挙してください")
    return errors


def check(root: Path) -> list[str]:
    errors, modules = submodules(root)
    try:
        verify_revisions(root)
    except ValueError as error:
        errors.append(f"vendor固定版: {error}")
    agents, claude = root / ".agents/skills", root / ".claude/skills"
    if (not agents.is_dir() or agents.is_symlink()
            or not claude.is_dir() or claude.is_symlink()):
        return errors + [".agents/skillsと.claude/skillsには実ディレクトリが必要です"]
    canonical = {entry.name: entry for entry in agents.iterdir()}
    mirrors = {entry.name: entry for entry in claude.iterdir()}
    if not canonical:
        errors.append("正本のスキル一覧が空です")
    if canonical.keys() != mirrors.keys():
        errors.append(".claude/skillsの一覧が.agents/skillsと一致しません")
    kinds = {}
    vendor = root / "vendor"
    for name, skill in sorted(canonical.items()):
        kinds[name] = "外部" if skill.is_symlink() else "自作"
        if not re.fullmatch(NAME, name):
            errors.append(f"{name}: スキル名は小文字のkebab-caseにしてください")
        mirror = mirrors.get(name)
        expected = f"../../.agents/skills/{name}"
        if mirror is None or not mirror.is_symlink() or os.readlink(mirror) != expected:
            errors.append(f"{name}: ミラーは{expected}へのsymlinkにしてください")
        try:
            resolved = skill.resolve(strict=True)
            if skill.is_symlink():
                target = os.readlink(skill)
                if (vendor.is_symlink() or not target.startswith("../../vendor/")
                        or not resolved.is_relative_to(vendor.resolve())
                        or not any(resolved.is_relative_to(root / path) for path in modules)):
                    errors.append(f"{name}: 外部スキルのリンクはvendor/のsubmodule内に限定してください")
                    continue
            if not resolved.is_dir():
                errors.append(f"{name}: スキルはディレクトリでなければなりません")
                continue
            document = resolved / "SKILL.md"
            boundary = vendor.resolve() if skill.is_symlink() else resolved
            if not document.resolve(strict=True).is_relative_to(boundary):
                errors.append(f"{name}: SKILL.mdが許可範囲の外へリンクされています")
                continue
            errors.extend(metadata(document.read_text(encoding="utf-8"), name))
            if mirror is not None and mirror.is_symlink() and not (mirror / "SKILL.md").is_file():
                errors.append(f"{name}: ミラーのSKILL.mdを読み取れません")
        except (OSError, RuntimeError, ValueError, UnicodeError) as error:
            errors.append(f"{name}: SKILL.mdまたはリンクを読み取れません: {error}")
    try:
        errors.extend(inventory_table((root / "README.md").read_text(encoding="utf-8"), kinds))
    except (OSError, UnicodeError) as error:
        errors.append(f"README.mdを読み取れません: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    errors = check(args.root.resolve())
    for error in errors:
        print(f"エラー: {error}")
    print(f"スキル検査: {len(errors)}件のエラー")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
