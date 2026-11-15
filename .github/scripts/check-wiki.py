#!/usr/bin/env python3
"""Validate a DeepWiki configuration using the Python standard library."""

import argparse
import json
from pathlib import Path
import sys


def fields(value, required, optional, location):
    if not isinstance(value, dict) or not required <= value.keys() or value.keys() - required - optional:
        raise ValueError(f"{location}: 必須キーの不足、未知のキー、またはオブジェクト以外の値があります")


def text(value, location):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location}: 空でない文字列が必要です")


def notes(value, location):
    if not isinstance(value, list):
        raise ValueError(f"{location}: 配列が必要です")
    for index, note in enumerate(value):
        label = f"{location}[{index}]"
        fields(note, {"content"}, {"author"}, label)
        text(note["content"], label + ".content")
        if len(note["content"]) > 10000:
            raise ValueError(f"{label}: contentは10,000文字以下にしてください")
        if "author" in note:
            text(note["author"], label + ".author")
    return len(value)


def validate(config, max_pages=30):
    if not isinstance(max_pages, int) or isinstance(max_pages, bool) or max_pages < 1:
        raise ValueError("ページ上限は1以上の整数にしてください")
    fields(config, {"repo_notes", "pages"}, set(), "config")
    count = notes(config["repo_notes"], "repo_notes")
    pages = config["pages"]
    if not isinstance(pages, list) or not 1 <= len(pages) <= max_pages:
        raise ValueError(f"pages: ページ数は1〜{max_pages}件にしてください")
    parents = {}
    for index, page in enumerate(pages):
        label = f"pages[{index}]"
        fields(page, {"title", "purpose"}, {"parent", "page_notes"}, label)
        title = page["title"]
        text(title, label + ".title")
        text(page["purpose"], label + ".purpose")
        if title != title.strip() or title in parents:
            raise ValueError(f"{label}: titleに前後空白または重複があります")
        parent = page.get("parent")
        if "parent" in page:
            text(parent, label + ".parent")
        parents[title] = parent
        count += notes(page.get("page_notes", []), label + ".page_notes")
    if count > 100:
        raise ValueError("ノートの合計は100件以下にしてください")
    for title in parents:
        seen = set()
        node = title
        while node is not None:
            if node not in parents:
                raise ValueError(f"{title}: 親ページが存在しません: {node}")
            if node in seen:
                raise ValueError(f"{title}: 親ページの参照が循環しています")
            seen.add(node)
            node = parents[node]
    return len(pages), count


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSONのキーが重複しています: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"JSONで許可されない定数です: {value}")


def load_config(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[2] / ".devin/wiki.json")
    parser.add_argument("--max-pages", type=int, default=30)
    args = parser.parse_args()
    try:
        pages, count = validate(load_config(args.path), args.max_pages)
    except (OSError, ValueError, RecursionError) as error:
        print(f"Wiki検査エラー: {error}", file=sys.stderr)
        return 1
    print(f"Wiki検査: OK（{pages}/{args.max_pages}ページ、{count}/100ノート）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
