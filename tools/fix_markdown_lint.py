#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_markdown_lint.py — 消掉 manuscript_gate 的 MG-5 minor 里那两类真会影响排版的项。

只动两类，且都是机械安全的：
  1. list-no-blank-line：`- [ ]` / `- ` / `1. ` 紧跟在上一段文字后面。
     CommonMark 要求列表前有空行，否则整段会被当普通段落——
     在 Paged.js 里表现为"可核对清单"不再缩进、复选框消失。这是**排版风险**，不是洁癖。
  2. fence-no-language：裸 ``` 开栏。本书的 ``` 块是公式与时序图，不是代码，
     统一标 `text`，让 marked 输出 <code class="language-text">，
     样式表里按等宽正文处理。

不动的东西：正文文字、表格、引用块、图注、标记 [厂]/[算]/[未]。
用法：python -X utf8 tools/fix_markdown_lint.py [--dry]
"""
import io
import os
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = ("* ", "- ", "+ ", "[ ] ", "- [ ] ", "- [x] ")


def is_list(line):
    s = line.lstrip()
    if s.startswith(LIST):
        return True
    i = 0
    while i < len(s) and s[i].isdigit():
        i += 1
    return i > 0 and s[i:i + 2] in (". ", ") ")


def fix(text):
    lines = text.split(chr(10))
    out = []
    n_blank = n_lang = 0
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                if stripped == "```":
                    indent = line[:len(line) - len(line.lstrip())]
                    line = indent + "```text"
                    n_lang += 1
            else:
                in_fence = False
        if (not in_fence and is_list(line) and out):
            prev = out[-1]
            if prev.strip() and not is_list(prev) and not prev.lstrip().startswith(
                    ("#", ">", "|", "```", "!", "- ", "* ")):
                out.append("")
                n_blank += 1
        out.append(line)
    return chr(10).join(out), n_blank, n_lang


def main():
    dry = "--dry" in sys.argv
    args = sys.argv[1:]
    ex = set()
    if "--exclude" in args:
        i = args.index("--exclude") + 1
        while i < len(args) and not args[i].startswith("--"):
            ex.add(int(args[i].replace("unit-", "")))
            i += 1
    tb = tl = 0
    touched = []
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        u = os.path.basename(os.path.dirname(p))
        if int(u.replace("unit-", "")) in ex:
            continue
        raw = io.open(p, encoding="utf-8").read()
        new, nb, nl = fix(raw)
        if new != raw:
            if not dry:
                io.open(p, "w", encoding="utf-8").write(new)
            touched.append(u)
        tb += nb
        tl += nl
    print("补列表前空行 %d 处、给代码块补 text 标签 %d 处（dry=%s，跳过 %s，实改 %d 章）"
          % (tb, tl, dry, sorted(ex) or "无", len(touched)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
