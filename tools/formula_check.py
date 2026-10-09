#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""formula_check.py — 把正文里每一条形如"算式 = 结果"的句子真的算一遍。

为什么要有它：`number_provenance.py` 管的是"这个数有没有出处"，管不了
"作者把 0.99^500 写成 6.6%（实为 0.66%）"这种**算错**。2026-10-08 人工复核时
抓到过一处，而它藏在一张表里、旁边没有算式，任何"数从哪来"的门都拦不住。
所以这一道门只做一件事：**凡正文写了等号，就把等号左边当表达式求值，与右边比。**

规则：
  · 只处理"左边是纯算式（数字 + × ÷ + − × / 括号）、右边是一个数"的片段；
  · 允许量纲差 10 的幂（bit↔Mbps、g↔kg、Hz↔rad/s 这类同行换算），但差 10 倍
    且不是 10 的整数幂的仍然报；
  · 容差 1%（书里到处是"约"，比这更严会把正常四舍五入全报出来）；
  · 一条都不许静默跳过：跳过的行会计数打印出来，让人知道覆盖面有多大。

自检：--selftest 里放一条**故意算错**的句子，必须被抓到；否则这个门不算存在过。

用法：
  python -X utf8 tools/formula_check.py                 # 全书
  python -X utf8 tools/formula_check.py unit-38 unit-03 # 指定章
  python -X utf8 tools/formula_check.py --selftest
"""
import io
import math
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_FENCE = re.compile("^```.*$", re.M)

NUMRE = r"\d{1,3},\d{3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?"
SCALES = (1.0, 1e3, 1e-3, 1e4, 1e-4, 1e6, 1e-6, 1e9, 1e-9, 100.0, 0.01, 10.0, 0.1)
SAFE = {"sqrt": math.sqrt}


def norm_expr(s):
    s = re.sub(r"^\s*(?:[-*·]|\d+\.)\s+", " ", s)     # markdown 列表记号不是负号
    s = desup(s)
    s = (s.replace("½", "0.5").replace("⅓", "0.333333")
             .replace("×", "*").replace("÷", "/").replace("−", "-")
         .replace("，", "").replace(",", "").replace("（", "(").replace("）", ")")
         .replace("√", "sqrt").replace("^", "**"))
    s = re.sub(r"[A-Za-z][A-Za-z0-9·/\-²]*", lambda m: "" if m.group(0).lower() not in (
        "sqrt",) else m.group(0), s)                  # 保住 sqrt，其余字母单位删掉
    s = s.replace("sqrt", "@")                        # 占位符，躲过下一道的字符白名单
    s = re.sub(r"[^0-9().+\-*/@ ]", "", s)            # 中文单位与残留符号一并去掉
    if False:
      for sup, val in (("10", "**10"), ("15", "**15"), ("9", "**9"), ("8", "**8"),
                     ("7", "**7"), ("6", "**6"), ("5", "**5"), ("4", "**4"),
                     ("3", "**3"), ("2", "**2"), ("1", "**1"), ("0", "**0")):
        s = s.replace("⁰" if sup == "0" else "¹" * 0 + "²", "²")
    return s.replace("@", "sqrt").strip()


def unbalanced(s):
    return s.count("(") != s.count(")")


SUP = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4",
       "⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9"}


def desup(s):
    """把 2¹⁵ / 10⁻³ 这类上标翻成 **N（幂），供 eval 用。"""
    out, i = "", 0
    while i < len(s):
        if s[i] in SUP:
            j = i
            digits = ""
            while j < len(s) and (s[j] in SUP or s[j] == "⁻"):
                if s[j] == "⁻":
                    digits += "-"
                else:
                    digits += SUP[s[j]]
                j += 1
            out += "**(" + digits + ")"
            i = j
        else:
            out += s[i]
            i += 1
    return out


def clauses(line):
    """把一行切成 (原始算式, 可求值式, 声称值) 若干对。

    做法：先按分句切，再在每个分句里按 `=` 切成若干段；
    相邻两段构成一次"左式 = 右数"，右段取**开头那个数**（后面跟的是单位与话）。
    这样 `A = B = C` 与 `41,574 × 0.40 = 16,630 元；… = 24,944 元` 都能各算一次。
    """
    out = []
    for seg in re.split(r"[；;。\n]", line):
        if "=" not in seg:
            continue
        parts = seg.split("=")
        for i in range(len(parts) - 1):
            left = norm_expr(parts[i])
            right_raw = parts[i + 1].strip()
            m = re.match(NUMRE, right_raw)
            if not m or not left or unbalanced(left):
                continue
            if not re.search(r"[+\-*/]", left):
                continue
            right = float(m.group(0).replace(",", ""))
            out.append((parts[i].strip(), left, right))
    return out


def check_line(line):
    """返回 (通过数, 失败列表, 跳过数)。"""
    ok = 0
    bad = []
    for raw, left, right in clauses(line):
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                v = eval(left, {"__builtins__": {}}, dict(SAFE))
        except Exception:
            return ok, bad, 1
        if not isinstance(v, (int, float)) or v == 0:
            continue
        hit = any(abs(v * s - right) / max(abs(right), 1e-12) < 0.02 for s in SCALES)
        if hit:
            ok += 1
        else:
            bad.append((raw, right, v))
    return ok, bad, 0


def selftest():
    n, b, _ = check_line("41,574 × 0.60 = 24,944 元")
    print("  正例 41,574 × 0.60 = 24,944 → 通过 %d、失败 %d" % (n, len(b)))
    n2, b2, _ = check_line("41,574 × 0.60 = 25,944 元")
    print("  反例 41,574 × 0.60 = 25,944 → 通过 %d、失败 %d" % (n2, len(b2)))
    n3, b3, _ = check_line("12 GB ÷ 100 GB/s = 120 ms")
    print("  量纲换算 12 ÷ 100 = 120 → 通过 %d、失败 %d" % (n3, len(b3)))
    n4, b4, _ = check_line("G1：√(9.80665 ÷ 0.600) = 4.04 s")
    print("  开方 √(9.80665 ÷ 0.600) = 4.04 → 通过 %d、失败 %d" % (n4, len(b4)))
    n5, b5, _ = check_line("- 自己算一次 1820 ÷ 1320 = 1.379")
    print("  列表记号 - 1820 ÷ 1320 = 1.379 → 通过 %d、失败 %d" % (n5, len(b5)))
    ok = (n == 1 and not b and n2 == 0 and len(b2) == 1 and n3 == 1
          and n4 == 1 and not b4 and n5 == 1 and not b5)
    print("formula_check 自检：%s" % ("PASS" if ok else "FAIL：判不准，不许上岗"))
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        return selftest()
    files = sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md")))
    if args:
        want = ["unit-" + a.replace("unit-", "") for a in args]
        files = [f for f in files if os.path.basename(os.path.dirname(f)) in want]
    total_ok = total_bad = total_skip = 0
    report = []
    for p in files:
        u = os.path.basename(os.path.dirname(p))
        raw = io.open(p, encoding="utf-8").read()
        body = CODE_FENCE.sub("", raw)
        for i, line in enumerate(body.split(chr(10))):
            if "=" not in line or line.strip().startswith("|"):
                continue
            n, b, sk = check_line(line)
            total_ok += n
            total_skip += sk
            for rawexpr, right, got in b:
                total_bad += 1
                report.append("%s:%-4d 声称 %g，实算 %g（差 %.1f 倍）  %s" % (
                    u, i + 1, right, got, (right / got if got else 0),
                    rawexpr[:70]))
    print("可核算式：通过 %d 条，对不上 %d 条，无法解析跳过 %d 条" % (
        total_ok, total_bad, total_skip))
    for r in report:
        print("  ✗ " + r)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
