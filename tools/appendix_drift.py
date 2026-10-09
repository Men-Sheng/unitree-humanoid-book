#!/usr/bin/env python3
"""tools/appendix_drift.py — 附录里承诺的数字，必须与工具现在跑出来的一致。

为什么要有它（2026-10-08 第三轮审阅）：附录 B 自称"由 tools/gen_appendix_b.py 生成"，
**而仓库里当时根本没有那个脚本**；B.2 只誊了 10 条（脚本现在打 19 条），B.4 写"概念 150 个"
而 check_kg 现在报 158，B.5 又写 146，附录 E 的 URL 清单标题写 100 条而实际粘了 117 行。
工程师读者只要照附录的承诺跑一次，就会发现清单做不到它承诺的事——这比讲错一个数更伤信任。

做法：不假装"生成"，而是**当场跑一遍再比对**。附录里凡是承诺了可数的东西（自检条数、
概念数、用例合计、图数），这里都取实际值比一次；不一致就失败并打印两边。附录也不许再声称
由不存在的脚本生成。--selftest 造两个假现场（数字过期、脚本不存在），证明门会响。
用法：python -X utf8 tools/appendix_drift.py [--selftest]
"""
from __future__ import annotations

import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-X", "utf8"]
APPENDIX_UNITS = ["unit-42", "unit-43", "unit-44", "unit-45"]
MIN_CLAIMS = 3        # 门至少要到附录里找到 3 处计数承诺，否则它就是空跑的

# 附录里"承诺了某个可数东西"的写法。**顺序即优先级**：先匹配更具体的说法，
# 匹配过的区间不再被泛化模式重复计数——否则 B.4 那句"未被任何章引入的概念 0 个"
# 会被当成"概念 0 个"，门就会报一条假漂移（2026-10-08 实测）。
CLAIMS = [
    (r"未被任何章引入的概念\s*(\d+)\s*个", "未引入概念"),
    (r"概念\s*(\d+)\s*个", "概念总数"),
    (r"(\d+)\s*个概念", "概念总数"),          # B.5 表里那格是反着写的："158 个概念"
    (r"含 \*\*(\d+) 条\*\*已知答案用例", "foc自检"),
    (r"另含 \*\*(\d+) 条\*\*", "ar自检"),
    (r"这 (\d+) 条用例已经抓到", "用例合计"),
    (r"URL 清单（(\d+) 条", "E3清单"),          # 附录 E.3 的标题条数
    (r"另有 \*\*(\d+) 条\*\*", "E3排除"),       # E.3 里"按规则不进清单"的条数
    (r"(\d+)\s*幅", "图数"),
]


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", timeout=600)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:                                   # 工具炸了也要让附录失配可见
        return f"__ERR__ {type(e).__name__} {e}"


def actual_values() -> dict[str, int]:
    kg = run(PY + ["tools/check_kg.py"])
    foc = run(PY + ["code/tools/foc_check.py"])
    ar = run(PY + ["code/tools/arithmetic_check.py"])
    out: dict[str, int] = {}
    m = re.search(r"概念\s*(\d+)\s*个", kg)
    if m:
        out["概念总数"] = int(m.group(1))
    m = re.search(r"未被任何章引入的概念\s*(\d+)\s*个", kg)
    if m:
        out["未引入概念"] = int(m.group(1))
    out["foc自检"] = len(re.findall(r"^\s*(?:ok|PASS)\s", foc, re.M))
    out["foc推算行"] = len(re.findall(r"^\[\d\d ", foc, re.M))
    m = re.search(r"selfcheck:\s*(\d+)/(\d+)", ar)
    if m:
        out["ar自检"] = int(m.group(1))
    out["用例合计"] = out.get("foc自检", 0) + out.get("ar自检", 0)
    kept = {k: v for k, v in out.items() if v}
    # E.3 的条数直接问生成器要实际集合（0 也要留着，否则"另有 0 条"没人核）
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gen_appendix_e
        urls, _, skipped = gen_appendix_e.collect()
        kept["E3清单"] = len(urls)
        kept["E3排除"] = len(skipped)
    except Exception as e:
        print("（这一轮没能从 gen_appendix_e 取到实际集合：%s）" % e)
    return kept


def claims_in_appendix(root: str = ROOT) -> list[tuple[str, int, str]]:
    """附录 B/C/D/E 里"承诺了某个计数"的行：返回 (承诺名, 附录写的数, 出处)。"""
    out: list[tuple[str, int, str]] = []
    for unit in APPENDIX_UNITS:
        p = os.path.join(root, "drafts", unit, "draft.md")
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        for ln, line in enumerate(s.split("\n"), 1):
            used: list[tuple[int, int]] = []
            for pat, name in CLAIMS:
                for m in re.finditer(pat, line):
                    if any(a <= m.start() < b for a, b in used):
                        continue
                    used.append(m.span())
                    out.append((name, int(m.group(1)), f"{unit}:{ln}"))
    return out


def missing_generators(root: str = ROOT) -> list[str]:
    """附录声称"由 tools/gen_*.py 生成"的那些脚本，必须真的存在。"""
    bad = []
    for unit in APPENDIX_UNITS:
        p = os.path.join(root, "drafts", unit, "draft.md")
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        for script in sorted(set(re.findall(r"tools/(gen_[a-z_]+\.py)", s))):
            if not os.path.exists(os.path.join(root, "tools", script)):
                bad.append(f"{unit} 声称由 tools/{script} 生成，但仓库里没有这个脚本")
    return bad


def check() -> int:
    act = actual_values()
    claims = claims_in_appendix()
    bad = []
    for name, want, where in claims:
        if name not in act:
            continue                       # 本门没有实际值的（如图数），由别的门管
        if act[name] != want:
            bad.append(f"{where} 说 {name} {want}，实际跑出来是 {act[name]}")
    bad += missing_generators()
    if len(claims) < MIN_CLAIMS:
        bad.append(f"门只找到 {len(claims)} 处计数承诺（应 ≥{MIN_CLAIMS}）："
                   f"附录写法变了或文件没读到，这道门现在等于没跑")
    print(f"实际值：{act}")
    print(f"附录里的计数承诺：{len(claims)} 处 → {[(w, n, v) for n, v, w in claims]}")
    if bad:
        print(f"漂移 {len(bad)} 处：")
        for b in bad:
            print("  ✗ " + b)
        return 1
    print("附录的计数承诺与工具实际输出一致，且没有声称不存在的生成脚本 ✓")
    return 0


def selftest() -> int:
    """假现场：数字过期 + 声称不存在的脚本 + 附录被改空，三种都要被抓到。"""
    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix="drift_")
    try:
        os.makedirs(os.path.join(d, "drafts", "unit-42"), exist_ok=True)
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        io.open(os.path.join(d, "drafts", "unit-42", "draft.md"), "w", encoding="utf-8").write(
            "概念 158 个，未被任何章引入的概念 4 个\n"
            "含 **19 条**已知答案用例；另含 **3 条**。\n"
            "这 22 条用例已经抓到过四次算错\n"
            "B.5 表那格反着写：146 个概念\n"
            "由 tools/gen_appendix_b.py 生成。\n")
        act = {"概念总数": 157, "未引入概念": 0, "foc自检": 19, "ar自检": 3, "用例合计": 22}
        claims = claims_in_appendix(d)
        drift = [f"{n}={v}!={act.get(n)}" for n, v, w in claims if act.get(n) is not None
                 and act[n] != v]
        ok1 = "概念总数=158!=157" in drift
        ok2 = "未引入概念=4!=0" in drift                      # 具体的那条不能被泛化模式抢走
        ok3 = not any(n == "概念总数" and v == 4 for n, v, w in claims)   # 也不能报出假漂移
        ok4 = bool(missing_generators(d))
        ok7 = "概念总数=146!=157" in drift        # 反着写的那一格也要看得见
        empty = claims_in_appendix(os.path.join(d, "nowhere"))
        ok5 = len(empty) < MIN_CLAIMS                        # 没输入时门必须自曝空跑
        # 全都对得上时应当放行，否则门会把正确的稿子也判死
        io.open(os.path.join(d, "drafts", "unit-42", "draft.md"), "w", encoding="utf-8").write(
            "概念 157 个，未被任何章引入的概念 0 个\n"
            "含 **19 条**已知答案用例；另含 **3 条**。\n"
            "这 22 条用例已经抓到过四次算错\n"
            "B.5 表那格反着写：157 个概念\n"
            "由 tools/gen_appendix_b.py 生成。\n")
        io.open(os.path.join(d, "tools", "gen_appendix_b.py"), "w", encoding="utf-8").write("# x\n")
        good = [f"{n}={v}" for n, v, w in claims_in_appendix(d)
                if act.get(n) is not None and act[n] != v] + missing_generators(d)
        ok6 = len(good) == 0 and len(claims_in_appendix(d)) >= MIN_CLAIMS
        checks = [
            ("概念数写 158、实际 157 被抓到", ok1),
            ("未引入概念写 4、实际 0 被抓到", ok2),
            ("『未被任何章引入的概念 0 个』不会被误读成『概念 0 个』", ok3),
            ("声称由不存在的脚本生成被抓到", ok4),
            ("反着写的『146 个概念』也被看见", ok7),
            ("附录为空时门自曝『没看见输入』", ok5),
            ("数字都对得上且脚本存在时放行（正向对照）", ok6),
        ]
        bad = 0
        for label, ok in checks:
            print(("PASS " if ok else "FAIL ") + label)
            bad += 0 if ok else 1
        print("自检 %d/%d" % (len(checks) - bad, len(checks)))
        return 0 if bad == 0 else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else check())
