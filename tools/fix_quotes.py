#!/usr/bin/env python3
"""tools/fix_quotes.py — 把中文段落里的 ASCII 直引号成对换成中文弯引号 “ ”。

为什么要有它（2026-10-09 目视成品 PDF 第 20 页）：全书大部分引号是 “ ”，但 28 个文件里还有
986 个 ASCII `"` 混在中文句子中（例如 这张表只说了"谁限制谁"）。交给出版社的稿子，
引号体例必须一处一样——这属于"能直接印"的一部分，不是洁癖。

四条安全规则（宁可不改，不可改错）：
1. 代码块（``` 围栏）内**一个字符都不动**：脚本输出与命令里的引号是要照着敲的。
2. 行内代码（`...`）内的引号不动。
3. 只处理**含中文**的段落；纯英文的官方原文引语保持 ASCII 引号（那是逐字引文，不动它的标点）。
4. 段落里引号个数是奇数 → 跳过并打印，绝不猜哪一半。

改完自证：把结果里的 “ ” 全部还原成 " 必须与原文逐字相同（只允许引号形状变化），
并且每个文件 “ 与 ” 数量相等。不满足就回滚。
用法：python -X utf8 tools/fix_quotes.py [--dry]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
OPEN = "“”"[0]      # 左弯引号
CLOSE = "“”"[1]     # 右弯引号


def code_spans(line: str) -> list[tuple[int, int]]:
    spans, start = [], None
    for m in re.finditer(r"`", line):
        if start is None:
            start = m.start()
        else:
            spans.append((start, m.start()))
            start = None
    if start is not None:
        spans.append((start, len(line)))
    return spans


def link_dest_spans(line: str) -> list[tuple[int, int]]:
    """markdown 链接/图片的目的地：`]` 后面那对圆括号。
    pandoc 会写 `![alt](f03.png "图 03-1 …")`——里面的 ASCII 引号是**语法**，不是排版引号。
    2026-10-09 第一版把它换成弯引号，pandoc 立刻解析不出图片，交稿 docx 变成 0 图 0.6 MB，
    是 rebuild_all 里的"内嵌图 != 引用数"这道门把它拦下来的。"""
    return [(m.start(1) - 1, m.end(1) + 1) for m in re.finditer(r"\]\(([^()]*)\)", line)]


def link_dest_spans_depth(line: str) -> list[tuple[int, int]]:
    """按括号深度扫 `](` … `)`：图注里带公式就有圆括号（`…/(z̈+g) 的三种工况`），
    上面那种 `[^()]*` 的写法会漏掉这两条，标题的语法引号就被换成弯引号，
    pandoc 于是少嵌 3 张图（2026-10-09 实测：31/34）。**用这个。**"""
    spans = []
    for m in re.finditer(r"\]\(", line):
        depth, i = 1, m.end()
        while i < len(line) and depth:
            if line[i] == "(":
                depth += 1
            elif line[i] == ")":
                depth -= 1
            i += 1
        spans.append((m.start(), i))
    return spans


def protected(line: str) -> list[tuple[int, int]]:
    return code_spans(line) + link_dest_spans_depth(line)


def in_spans(i: int, spans) -> bool:
    return any(a <= i <= b for a, b in spans)


def fence_mask(lines):
    mask, f = [], False
    for l in lines:
        if l.startswith("```"):
            f = not f
            mask.append(True)
        else:
            mask.append(f)
    return mask


def paragraph_groups(lines, fence):
    """段落 = 分组单位；标题行单独成组（标题里也有引号，2026-10-09 首版把标题整类跳过了，
    留下 7 处 `## 一条被删掉的除法：两个"超过"…` 这种残留）。"""
    out, cur = [], []
    for i, l in enumerate(lines):
        if fence[i]:
            if cur:
                out.append(cur)
                cur = []
            continue
        if not l.strip():
            if cur:
                out.append(cur)
                cur = []
            continue
        if l.startswith("#"):
            if cur:
                out.append(cur)
                cur = []
            out.append([i])
            continue
        cur.append(i)
    if cur:
        out.append(cur)
    return out


def convert(txt: str) -> tuple[str, int, list]:
    ls = txt.split("\n")
    fence = fence_mask(ls)
    arr = list(ls)
    skipped = []
    n = 0
    for g in paragraph_groups(ls, fence):
        pos = []
        for i in g:
            sp = protected(arr[i])
            for j, ch in enumerate(arr[i]):
                if ch == '"' and not in_spans(j, sp):
                    pos.append((i, j))
        if not pos:
            continue
        body = "".join(arr[i] for i in g)
        if len(pos) % 2:
            skipped.append((g[0] + 1, len(pos), body[:48]))
            continue
        if not CJK.search(body):
            continue
        for k, (i, j) in enumerate(pos):
            arr[i] = arr[i][:j] + ("“" if k % 2 == 0 else "”") + arr[i][j + 1:]
        n += len(pos)
    return "\n".join(arr), n, skipped



def _fix_fence_block(block: str, state: list) -> str:
    """围栏内：把包着**纯 ASCII**（可跨行）的那一对弯引号退回直引号。
    英文官方原话常常一行放不下（第 37、44 章那两条就是跨行的），所以按整块匹配而不是按行。"""
    def sub(m):
        inner = m.group(1)
        if CJK.search(inner):
            return m.group(0)          # 围栏里夹的中文说明保持弯引号
        state[0] += 1
        return '"' + inner + '"'
    return re.sub(r"“((?:(?!”)[\s\S])*?)”", sub, block)


CJK_PAIR = re.compile(r'"([^"\n]*[\u4e00-\u9fff][^"\n]*)"')


def fence_cjk_pairs(block: str, state: list) -> str:
    """围栏内那半边的漏网规则：`_fix_fence_block` 说"围栏里夹的中文说明保持弯引号"，
    可 `convert()` 整段跳过围栏，于是**中文说明在围栏里从来没被换过**。2026-10-09 实测 34 行。
    只动内侧含中文的一对；内侧是纯 ASCII 的（官方原话、命令行、字段名）继续留直引号，
    因为那是要复制去跑的。"""
    def sub(m):
        state[0] += 1
        return '\u201c' + m.group(1) + '\u201d'
    return CJK_PAIR.sub(sub, block)


def fences_cjk_apply(txt: str) -> tuple:
    ls = txt.split(chr(10))
    out, fence, blocks, cnt = [], False, [], [0]
    for l in ls:
        if l.startswith("```"):
            if fence:
                out.append(fence_cjk_pairs(chr(10).join(blocks), cnt))
                blocks = []
            fence = not fence
            out.append(l)
            continue
        (blocks if fence else out).append(l)
    if blocks:
        out.append(fence_cjk_pairs(chr(10).join(blocks), cnt))
    return chr(10).join(out), cnt[0]


def fence_cjk_residue(root=ROOT) -> int:
    n = 0
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        n += len(CJK_PAIR.findall(fence_block_text(f)))
    return n


def fence_block_text(path: str) -> str:
    ls = io.open(path, encoding="utf-8").read().split(chr(10))
    fence, keep = False, []
    for l in ls:
        if l.startswith("```"):
            fence = not fence
            continue
        if fence:
            keep.append(l)
    return chr(10).join(keep)


def fences_to_ascii(txt: str) -> tuple[str, int]:
    """``` 围栏之内是**字面量**（`imu_type = "pelvis"`、官方英文原话、命令行），
    那里出现弯引号会让读者复制下来跑不通，也分不清是原文还是中文措辞。
    2026-10-09 独立审稿发现 8 行围栏内是弯引号；回查改动前的备份，那是历史遗留，
    不是本轮归一化改坏的——规则以前没写下来。"""
    ls = txt.split(chr(10))
    out, fence, blocks, n = [], False, [], 0
    cnt = [0]
    for l in ls:
        if l.startswith("```"):
            if fence:
                out.append(_fix_fence_block(chr(10).join(blocks), cnt))
                blocks = []
            fence = not fence
            out.append(l)
            continue
        if fence:
            blocks.append(l)
        else:
            out.append(l)
    if blocks:
        out.append(_fix_fence_block(chr(10).join(blocks), cnt))
    return chr(10).join(out), cnt[0]


def fence_residue(root=ROOT) -> int:
    n = 0
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        n += fences_to_ascii(io.open(f, encoding="utf-8").read())[1]
    return n

def residue(root=ROOT) -> list[tuple[str, int, str]]:
    """中文段落/标题里残留的 ASCII 直引号（代码块与行内代码不算）。"""
    out = []
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        ls = io.open(f, encoding="utf-8").read().split("\n")
        fence = False
        for i, l in enumerate(ls, 1):
            if l.startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            sp = protected(l)
            if any(ch == '"' and not in_spans(j, sp) for j, ch in enumerate(l)) and CJK.search(l):
                out.append((os.path.basename(os.path.dirname(f)), i, l.strip()[:70]))
    return out


def _count_groups(text):
    ls = text.split(chr(10))
    fence = fence_mask(ls)
    n = 0
    for g in paragraph_groups(ls, fence):
        depth = 0
        for i in g:
            if fence[i]:
                continue
            sp = protected(ls[i])
            for j, ch in enumerate(ls[i]):
                if in_spans(j, sp):
                    continue
                if ch == OPEN:
                    depth += 1
                elif ch == CLOSE:
                    depth -= 1
        if depth != 0:
            n += 1
    return n


def cross_paragraph(root=ROOT):
    """弯引号必须**在同一个段落组里成对**。跨段闭合意味着：某个引号开了没在本段关，
    是归一化按顺序赋号时配错对的唯一硬症状。
    不检"单行配平"——散文折行与表格行本来就跨行成对（第 27、28 章那 4 处就是），
    按行检会天天假报警。围栏与行内代码跳过。"""
    bad = []
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        s = io.open(f, encoding="utf-8").read()
        ls = s.split(chr(10))
        fence = fence_mask(ls)
        for g in paragraph_groups(ls, fence):
            depth = 0
            for i in g:
                if fence[i]:
                    continue
                sp = protected(ls[i])
                for j, ch in enumerate(ls[i]):
                    if in_spans(j, sp):
                        continue
                    if ch == OPEN:
                        depth += 1
                    elif ch == CLOSE:
                        depth -= 1
                    if depth < 0:
                        break
                if depth < 0:
                    break
            if depth != 0:
                bad.append((os.path.basename(os.path.dirname(f)), g[0] + 1, depth,
                            ls[g[0]].strip()[:56]))
    return bad


def apply_glob(pattern: str) -> int:
    """对**构建产物**（如 submission/src-docx/*.md）就地归一化：docx 走 pandoc，
    不经过 build.mjs 的渲染层，所以交稿包要在打包后单独过一遍同一条体例。"""
    total = 0
    for f in sorted(glob.glob(pattern)):
        old = io.open(f, encoding="utf-8").read()
        new, n, _ = convert(old)
        if not n:
            continue
        assert new.replace("“", '"').replace("”", '"') == old.replace("“", '"').replace("”", '"'), f
        assert new.count("“") == new.count("”"), f
        io.open(f, "w", encoding="utf-8", newline="\n").write(new)
        total += n
    print("构建产物引号归一：%s → %d 个字符" % (pattern, total))
    return total


def selftest() -> int:
    src = ('# 章题\n\n'
           '这是一句"混用"的中文，还有 `code "x"` 与 ![图 03-1](f.png "图 03-1 标题")。\n\n'
           '![图 17-1](f17.png "图 17-1 p_x = x − z·ẍ/(z+g) 的三种工况") 这条目的地里有圆括号。\n\n'
           'English verbatim: "not to be touched".\n\n'
           '```\n脚本输出 "不要动"\n```\n\n'
           '这条段落里只有一个"落单的引号。\n')
    out, n, skipped = convert(src)
    checks = [
        ("中文段落里的成对直引号被换成弯引号", "“混用”" in out),
        ("markdown 图片标题的语法引号必须保留（否则 pandoc 丢图）", '(f.png "图 03-1 标题")' in out),
        ("标题目的地里带圆括号的也要保住（图 17-1 与 23-1 就是这两条）",
         '(f17.png "图 17-1 p_x = x − z·ẍ/(z+g) 的三种工况")' in out),
        ("行内代码内的引号不动", '`code "x"`' in out),
        ("代码块内的引号不动", '脚本输出 "不要动"' in out),
        ("纯英文段保持 ASCII 引号（逐字引文不动标点）", '"not to be touched"' in out),
        ("落单引号的段落被跳过而不是乱配", bool(skipped) and skipped[0][1] == 1),
        ("还原后与原文逐字相同", out.replace("“", '"').replace("”", '"') == src.replace("“", '"').replace("”", '"')),
    ]
    bad = 0
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
        bad += 0 if ok else 1
    print("自检 %d/%d" % (len(checks) - bad, len(checks)))
    return 0 if bad == 0 else 1


def main() -> int:
    if "--fences-cjk-apply" in sys.argv:
        tot = 0
        for f in sorted(glob.glob(os.path.join(ROOT, "drafts", "*", "draft.md"))):
            old = io.open(f, encoding="utf-8").read()
            new, n = fences_cjk_apply(old)
            if not n:
                continue
            assert new.replace('“', '"').replace('”', '"') == old.replace('“', '"').replace('”', '"'), f
            assert new.count("\u201c") == new.count("\u201d"), f
            io.open(f, "w", encoding="utf-8", newline="\n").write(new)
            tot += n
            print("  围栏内中文引号归一 %d 个：%s" % (n, f.split(os.sep)[-2]))
        print("围栏内含中文的 ASCII 引号：共替换 %d 个字符" % tot)
        return 0
    argv = sys.argv
    if "--selftest" in argv:
        return selftest()
    for i, a in enumerate(argv):
        if a == "--apply" and i + 1 < len(argv):
            apply_glob(argv[i + 1])
            return 0
    if "--fences-apply" in sys.argv:
        tot = 0
        for f in sorted(glob.glob(os.path.join(ROOT, "drafts", "*", "draft.md"))):
            old = io.open(f, encoding="utf-8").read()
            new, n = fences_to_ascii(old)
            if n:
                # 只允许"引号形状"变化：把三种引号统一成一个记号后必须逐字相同
                norm = lambda x: x.replace("“", "Q").replace("”", "Q").replace('"', "Q")
                assert norm(new) == norm(old), f
                io.open(f, "w", encoding="utf-8", newline=chr(10)).write(new)
                tot += n
                print("  %-9s 围栏内退回 ASCII 引号 %d 个" % (os.path.basename(os.path.dirname(f)), n))
        print("围栏内引号：共退回 %d 个" % tot)
        return 0
    if "--fences-check" in sys.argv:
        n = fence_residue()
        print("围栏内残留弯引号 %d 个（字面量与英文原话应当是 ASCII）" % n)
        return 1 if n else 0
    if "--test-cross-paragraph" in sys.argv:
        good_txt = '甲段\u201c你好\u201d收尾。\n\n乙段没有引号。\n'
        bad_txt = '甲段\u201c开了没关\n\n乙段\u201d在别处关上。\n'
        wrap_txt = '同一句\u201c从这里\n一直折到下一行\u201d不跨段。\n'
        ok1 = _count_groups(good_txt) == 0
        ok2 = _count_groups(bad_txt) == 2      # 开口段与闭合段各记一次，所以是 2 不是 1
        print(('PASS ' if ok1 else 'FAIL ') + '同段成对不误报')
        print(('PASS ' if ok2 else 'FAIL ') + '跨段闭合被抓到')
        ok3 = _count_groups(wrap_txt) == 0     # 同段跨行（散文折行 / 表格长句）不算泄漏
        print(('PASS ' if ok3 else 'FAIL ') + '同段跨行不误报')
        return 0 if (ok1 and ok2 and ok3) else 1
    if "--check" in sys.argv:
        r = residue()
        bal = []
        for f in sorted(glob.glob(os.path.join(ROOT, "drafts", "*", "draft.md"))):
            s = io.open(f, encoding="utf-8").read()
            if s.count("“") != s.count("”"):
                bal.append(os.path.basename(os.path.dirname(f)))
        xp = cross_paragraph()
        print("引号体例：中文里残留 ASCII 直引号 %d 处；弯引号不配平的文件 %d 个；跨段未闭合 %d 处"
              % (len(r), len(bal), len(xp)))
        for u, ln, d, txt in xp[:6]:
            print("    跨段：", u, "行", ln, "净差", d, txt)
        for u, ln, txt in r[:8]:
            print("   ", u, ln, txt)
        for u in bal[:8]:
            print("    不配平：", u)
        return 1 if (r or bal or xp) else 0
    dry = "--dry" in sys.argv
    total = 0
    all_skipped = []
    for f in sorted(glob.glob(os.path.join(ROOT, "drafts", "*", "draft.md"))):
        old = io.open(f, encoding="utf-8").read()
        new, n, skipped = convert(old)
        all_skipped += [(os.path.basename(os.path.dirname(f)), s) for s in skipped]
        if not n:
            continue
        # 自证 1：还原引号形状后必须与原文逐字相同
        assert new.replace("“", '"').replace("”", '"') == old.replace("“", '"').replace("”", '"'), \
            f"{f}: 除引号形状外出现了别的改动，中止"
        # 自证 2：左右必须配平
        assert new.count("“") == new.count("”"), f"{f}: 弯引号不配平，中止"
        total += n
        if not dry:
            io.open(f, "w", encoding="utf-8", newline="\n").write(new)
        print("  %-9s 换 %3d 个引号字符" % (os.path.basename(os.path.dirname(f)), n))
    print(("dry-run：" if dry else "") + "共 %d 个引号字符被成对替换" % total)
    if all_skipped:
        print("奇数引号、跳过不猜的段落 %d 处：" % len(all_skipped))
        for u, s in all_skipped[:10]:
            print("   ", u, "行", s[0], "有", s[1], "个｜", s[2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
