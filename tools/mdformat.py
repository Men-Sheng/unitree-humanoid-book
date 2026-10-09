#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/mdformat.py — 修 Markdown 的"能渲染但各家不一致"问题。

为什么需要：`lint_render.py` 会报 list-no-blank-line / heading-no-blank-line /
fence-no-language 这类 minor。CommonMark 接受它们，Pandoc 与部分 linter 不接受——
而本书要同时出 PDF（Paged.js）、EPUB（pandoc）、站点（VitePress）三个形态，
**同一份源必须三家都渲染成一样**。所以写作时随手写出的紧凑格式，出版前统一过一遍。

用法：
    python tools/mdformat.py            # 修（就地）
    python tools/mdformat.py --check    # 只报告，不改
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
LIST = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
HEAD = re.compile(r"^#{1,6}\s")
TABLE = re.compile(r"^\s*\|")


def needs_blank_before(prev: str, cur: str) -> bool:
    if not prev.strip():
        return False
    if prev.strip() in {"```"} or prev.startswith("```"):
        return False
    if prev.strip().endswith(">"):          # 引用块内的续行
        return False
    if LIST.match(cur):
        # 列表紧跟在普通段落后 → 需要空行；列表项之间不需要
        return not (LIST.match(prev) or prev.strip().startswith(("|", ">"))
                    or re.match(r"^\s+\S", prev))
    if HEAD.match(cur):
        return True
    if TABLE.match(cur):
        return not TABLE.match(prev)
    return False


def fix_text(text: str) -> tuple[str, int]:
    lines = text.split("\n")
    out: list[str] = []
    n_fix = 0
    in_fence = False
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                if stripped == "```":
                    ln = "```text"
                    n_fix += 1
            else:
                in_fence = False
        if not in_fence and needs_blank_before(out[-1] if out else "", ln):
            out.append("")
            n_fix += 1
        out.append(ln)
    return "\n".join(out), n_fix


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--glob", nargs="*", default=["*.md", "bible/*.md", "verification/*.md"])
    a = ap.parse_args()
    changed = 0
    for g in a.glob:
        for p in sorted(ROOT.glob(g)):
            src = p.read_text(encoding="utf-8")
            fixed, n = fix_text(src)
            if n:
                print(f"{'would fix' if a.check else 'fixed':9s} {p.relative_to(ROOT)}  ({n} 处)")
                changed += n
                if not a.check and fixed != src:
                    p.write_text(fixed, encoding="utf-8")
    print(f"total {changed} 处" + ("（--check 未改动文件）" if a.check else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
