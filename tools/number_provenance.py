#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""number_provenance.py — "不能讲错"的数字溯源门。

作者的原则是「你可以不讲，但是你不能讲错」。文字层面的错很难机检，
但**带单位的数**是可以逐一对账的：每一个出现在书稿里的数，要么能在
一手资料/脚本/研究笔记里找到，要么就是有人现编的。

做法：
  1. 建"已知数集合"：research/*.md、bible/*.md、code/tools/*.py、
     code/tools/calculations.yaml、outline/*.yaml、tools/*.py、assets/fig/*.svg。
     草稿本身不进集合（否则等于让被检查者给自己开证明）。
  2. 从每章 draft.md 抽出带单位或带小数的数（跳过纯小整数、年份、章节号、
     markdown 表格里的序号、代码块里的行号）。
  3. 报告"集合里找不到"的数，连同上下文 60 字，供人工判定：
     要么它是由集合里两个数一步算出来的（合法，但正文要写出算式），
     要么它必须删掉或降级为 [未]。

用法：
  python -X utf8 tools/number_provenance.py                 # 全书
  python -X utf8 tools/number_provenance.py unit-27 unit-37 # 只看指定章
  python -X utf8 tools/number_provenance.py --summary       # 只看计数

退出码：0 = 没有可疑数；1 = 有，需要人看。这个门**故意**会误报，
漏报才是致命的。
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORPUS_GLOBS = [
    "research/*.md", "../research/*.md", "bible/*.md", "code/tools/*.py", "code/tools/*.yaml",
    "code/tools/*.txt",              # foc_check / arithmetic_check 的运行输出（[算] 数的真出处）
    "outline/*.yaml", "tools/*.py", "assets/fig/*.svg", "verification/*.md",
    "manifesto.md", "print/style.css",
]

NUM = re.compile(r"\d+(?:[,，]\d{3})*(?:\.\d+)?")
# 只在这些语境里认为"这是个有含义的量"：带单位、带小数、或紧跟 % / 倍 / 万
MEANINGFUL = re.compile(
    r"(\d+(?:[,，]\d{3})*(?:\.\d+)?)\s*"
    r"(?:%|％|倍|万|千|毫米|厘米|米|千克|公斤|克|瓦|毫瓦|千瓦|焦|焦耳|安培|毫安|安|"
    r"伏特|毫伏|伏|特斯拉|毫特|匝|赫兹|千赫|兆赫|牛[·]?米|毫牛|牛|摄氏度|度|"
    r"毫秒|微秒|纳秒|秒|分钟|小时|天|次|台|档|级|元|美元|位|比特|字节|"
    r"Wh|kWh|Ah|mAh|Hz|kHz|MHz|GHz|mm|cm|kg|ms|\u00b5s|ns|rpm|bps|Mbps|GB|TB|"
    r"TFLOPS|GFLOPS|TOPS|N\[?·\u00b7\]?m|V|A|W|J|\u2103|Ω|FS)")
HEADING = re.compile(r"^\s*(#{1,6}|\|)")
CODE_FENCE = re.compile("^```.*$", re.M)


def norm(s):
    s = s.replace(",", "").replace("，", "")
    try:
        v = float(s)
    except ValueError:
        return None
    return round(v, 6)


def build_corpus():
    known = set()
    files = []
    for g in CORPUS_GLOBS:
        files += glob.glob(os.path.join(ROOT, *g.split("/")))
    for p in files:
        try:
            t = io.open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in NUM.finditer(t):
            v = norm(m.group(0))
            if v is not None:
                known.add(v)
    return known, len(files)


def digits_of(v):
    """把 1.32 与 132 视为不同；但 0.64 与 64 在"同一量纲写成了百分比"时常见，
    所以同时收录去掉小数点的形态，降低误报。"""
    out = {v}
    s = ("%.6f" % v).rstrip("0").rstrip(".")
    if "." in s:
        out.add(float(s.replace(".", "")))
    out.add(v * 100)
    out.add(v / 100)
    return out


def arithmetic_ok(line, v):
    """同行自带可核算式 ⇒ 放行。

    本书的纪律是"推算链的算式必须印在正文里"，所以 `23 × 369 = 8,487` 这类行
    不该被当可疑数报出来。做法：取最后一个 `=` 左边的表达式，把 × ÷ ， 全角
    等换成可求值形式，只允许数字与 + - * / ( ) . ，求值后与 v 比 1% 容差。
    求不了值或值不吻合，仍然报——宁误报不漏报。
    """
    if "=" not in line:
        return False
    # 一行里可能有两条算式（"A × 0.40 = x；A × 0.60 = y"），逐个 = 都试，
    # 且只取该 '=' 前面、上一条分句之后那一截
    bounds = [m.start() for m in re.finditer("[=；;。]", line)]
    for i, pos in enumerate(bounds):
        if line[pos] != "=":
            continue
        start = max([b for b in bounds[:i] if line[b] != "="] or [-1]) + 1
        if _one_expr(line[start:pos], v):
            return True
    return False


def _one_expr(left, v):
    expr = (left.replace("×", "*").replace("÷", "/").replace("，", "")
                .replace(",", "").replace("（", "(").replace("）", ")")
                .replace("−", "-"))
    expr = re.sub(r"[A-Za-z][A-Za-z0-9·/\-]*", "", expr)   # IM6014 / N·m / rad/s 整块去掉
    # 去掉中文与字母单位，只留数字与运算符
    expr = re.sub(r"[^0-9().+\-*/ ]", "", expr).strip()
    if not expr or not re.fullmatch(r"[0-9().+\-*/ ]+", expr):
        return False
    if not re.search(r"[+\-*/]", expr):
        return False                      # 单边一个数不算算式
    try:
        r = eval(expr, {"__builtins__": {}}, {})   # 上面已限制字符集，只有数字与运算符
    except Exception:
        return False
    if not isinstance(r, (int, float)) or r == 0:
        return False
    # 允许量纲换算（bit vs Mbps、g vs kg 这类同行单位差 10 的幂）
    for scale in (1.0, 1e3, 1e-3, 1e6, 1e-6, 100.0, 0.01):
        if abs(r * scale - v) / max(abs(float(v)), 1e-9) < 0.01:
            return True
    return False


def selftest():
    """这个门自己必须先证明它会抓错的算式。"""
    cases = [
        ("23 × 369 = 8,487 美元", 8487.0, True),
        ("15 台 × 6000 Hz × 17 B × 8 = 12.24 Mbps", 12.24, True),
        ("365 × 24 × 3600 = 31,536,000 秒", 31536000.0, True),
        ("23 × 369 = 9,000 美元", 9000.0, False),      # 算错了必须仍然报
        ("IM6014：31.7 N·m × 54.2 rad/s = 1718 W ÷ 0.535 kg = 3.21 kW/kg", 1718.0, True),
        ("41,574 × 0.40 = 16,630 元；41,574 × 0.60 = 24,944 元", 24944.0, True),
        ("41,574 × 0.60 = 25,944 元", 25944.0, False),  # 分句里算错也要报
        ("这台机器重 1234 千克", 1234.0, False),        # 没有算式，必须报
        ("扭矩 42.5 N·m 很大", 42.5, False),
    ]
    bad = 0
    for line, v, want in cases:
        got = arithmetic_ok(line, v)
        if got != want:
            bad += 1
        print("  %-46s 期望放行=%-5s 实得=%-5s %s"
              % (line[:44], want, got, "" if got == want else "  ← 判错"))
    print("number_provenance 自检：%d/%d 通过" % (len(cases) - bad, len(cases)))
    return 0 if bad == 0 else 1


def scan(path, known, self_values):
    raw = io.open(path, encoding="utf-8").read()
    body = CODE_FENCE.sub("", raw)
    lines = body.split(chr(10))
    unit = os.path.basename(os.path.dirname(path))
    findings = []
    for i, line in enumerate(lines):
        if not line.strip() or HEADING.match(line):
            continue
        for m in MEANINGFUL.finditer(line):
            v = norm(m.group(1))
            if v is None:
                continue
            if v <= 12 and float(v).is_integer():
                continue          # 小整数几乎总是序号/列举
            if 1900 <= v <= 2100:
                continue          # 年份
            cands = digits_of(v)
            if cands & known:
                continue
            if cands & self_values.get(unit, set()):
                continue          # 同一章里已经交代过出处的数（表格行或带标记行）
            if arithmetic_ok(line, v):
                continue          # 同行自带可核算式，算式印在正文里
            ctx = line.strip()
            findings.append((unit, i + 1, m.group(0), ctx[:88]))
    return findings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        return selftest()
    summary = "--summary" in sys.argv
    known, nfiles = build_corpus()
    # 二遍：只承认"章内已经交代过出处的位置"里的数当白名单——
    # 即表格行、以及"证据等级 / 可核对清单 / 锚点 / [算] / [厂] / [拆]"这些行。
    # 若把整份草稿都当白名单，等于允许一个数在正文里互相引用，门就形同虚设。
    PROV_LINE = re.compile(r"^\s*\||证据等级|可核对清单|锚点|\[算\]|\[厂\]|\[拆\]|\[查\]")
    self_values = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        u = os.path.basename(os.path.dirname(p))
        vals = set()
        for line in io.open(p, encoding="utf-8", errors="replace").read().split(chr(10)):
            if not PROV_LINE.search(line):
                continue
            for m in NUM.finditer(line):
                v = norm(m.group(0))
                if v is not None:
                    vals.add(v)
        self_values[u] = vals
    files = sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md")))
    if args:
        files = [f for f in files
                 if os.path.basename(os.path.dirname(f)) in
                 ["unit-" + a.replace("unit-", "") for a in args]]
    all_find = []
    for p in files:
        all_find += scan(p, known, self_values)
    print("已知数集合：%d 个文件" % nfiles)
    print("可疑数：%d 处 / 覆盖 %d 章" % (
        len(all_find), len(set(f[0] for f in all_find))))
    if summary:
        for u in sorted(set(f[0] for f in all_find)):
            print("  %-9s %d" % (u, len([f for f in all_find if f[0] == u])))
        return 0
    for u, ln, num, ctx in all_find:
        print("%-9s:%-4d %-10s  %s" % (u, ln, num, ctx))
    return 1 if all_find else 0


if __name__ == "__main__":
    sys.exit(main())
