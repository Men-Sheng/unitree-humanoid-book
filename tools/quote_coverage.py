#!/usr/bin/env python3
"""tools/quote_coverage.py — 附录 A 里那句"每章一条语录，实际做到多少"必须与 quotes.yaml 一致。

为什么要有它（2026-10-09）：作者承诺"每一章插一条带出处的王兴兴语录"，实际是 41 个正文章里 32 章有、
9 章查不到原话而留空。这个达成度本轮才第一次**写进书里**（附录 A）。写进去的那一刻起，它就变成
一句可以被反驳的事实：以后新增/删除一条语录、或把某章的"记者转述"升级成逐字，这句话就会过期。
所以它得有机检，不能靠人记着改。

核对四件事：
① 正文章数（按 draft 首行是不是 `# 附录` 划分正文与附录）；
② 有语录的章数 = quotes.yaml 的键数（且键必须落在正文章里，不许挂到附录上）；
③ 留空章清单 = 正文减去有语录的章，必须与附录 A 里逐个列出的章号**完全相同**；
④ 非逐字条数与其章号清单：`kind` 里带"整理稿/转述/书面化/非逐字"的，必须与附录 A 写的那串一致。

--selftest 造三处假现场（少算一章、多算一条、留空清单写错），证明门会响；
并在附录 A 找不到任何承诺时自曝"这道门等于没跑"。
用法：python -X utf8 tools/quote_coverage.py [--selftest]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NONVERBATIM = ("整理稿", "转述", "书面化", "非逐字", "大意")
MIN_CLAIMS = 4


def split_units(root=ROOT):
    body, appendix = [], []
    for p in sorted(glob.glob(os.path.join(root, "drafts", "unit-*", "draft.md"))):
        u = os.path.basename(os.path.dirname(p)).replace("unit-", "")
        first = io.open(p, encoding="utf-8").readline()
        (appendix if first.startswith("# 附录") else body).append(u)
    return body, appendix


def quotes_map(root=ROOT):
    q = yaml.safe_load(io.open(os.path.join(root, "bible", "quotes.yaml"), encoding="utf-8"))["quotes"]
    return {str(k).zfill(2): (v or {}) for k, v in q.items()}


def actual(root=ROOT):
    body, appendix = split_units(root)
    qm = quotes_map(root)
    stray = sorted(k for k in qm if k not in body)
    have = sorted(k for k in qm if k in body)
    blank = [u for u in body if u not in qm]
    nv = sorted(k for k, v in qm.items() if any(t in str(v.get("kind", "")) for t in NONVERBATIM))
    return {"正文章数": len(body), "有语录章数": len(have), "留空章": blank,
            "非逐字章": nv, "挂到附录的键": stray, "附录单元": appendix}


def claims_in_appendix_a(root=ROOT):
    """附录 A 的达成度段落里的承诺：返回 [(名字, 值, 行号)]。"""
    p = os.path.join(root, "drafts", "unit-41", "draft.md")
    if not os.path.exists(p):
        return []
    out = []
    for ln, line in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
        if "正文章里" not in line and "留空" not in line and "非逐字" not in line and "条**（第" not in line:
            continue
        for m in re.finditer(r"(\d+)\s*个正文章", line):
            out.append(("正文章数", int(m.group(1)), ln))
        for m in re.finditer(r"(\d+)\s*\*{0,2}\s*章\s*\*{0,2}\s*有", line):
            out.append(("有语录章数", int(m.group(1)), ln))
        for m in re.finditer(r"(\d+)\s*\*{0,2}\s*章留空", line):
            out.append(("留空章数", int(m.group(1)), ln))
        m = re.search(r"第\s*([\d、,，\s]+?)\s*章（", line)
        if m:
            ids = re.findall(r"\d{2}", m.group(1))
            out.append(("留空清单", sorted(ids), ln))
        m = re.search(r"(\d+)\s*条\*\*（第\s*([\d、,，\s]+?)\s*章）", line)
        if m:
            ids = re.findall(r"\d{2}", m.group(2))
            out.append(("非逐字章数", int(m.group(1)), ln))
            out.append(("非逐字清单", sorted(ids), ln))
    return out


def check(root=ROOT) -> int:
    act = actual(root)
    claims = claims_in_appendix_a(root)
    bad = []
    for name, want, ln in claims:
        if name == "留空章数":
            if want != len(act["留空章"]):
                bad.append(f"附录 A:{ln} 说 {want} 章留空，实际是 {len(act['留空章'])} 章（{act['留空章']}）")
        elif name in act:
            if act[name] != want:
                bad.append(f"附录 A:{ln} 说 {name} {want}，实际是 {act[name]}")
        elif name == "留空清单":
            if want != act["留空章"]:
                bad.append(f"附录 A:{ln} 列的留空章号与实际不符\n      写的：{want}\n      实际：{act['留空章']}")
        elif name == "非逐字清单":
            if want != act["非逐字章"]:
                bad.append(f"附录 A:{ln} 列的非逐字章号与 quotes.yaml 的 kind 不符\n"
                           f"      写的：{want}\n      实际：{act['非逐字章']}")
        elif name == "非逐字章数":
            if want != len(act["非逐字章"]):
                bad.append(f"附录 A:{ln} 说 {want} 条非逐字，实际 {len(act['非逐字章'])} 条")
    if act["挂到附录的键"]:
        bad.append(f"quotes.yaml 有键落在附录单元上：{act['挂到附录的键']}（附录不该塞语录）")
    if len(claims) < MIN_CLAIMS:
        bad.append(f"门只找到 {len(claims)} 处承诺（应 ≥{MIN_CLAIMS}）：附录 A 那段达成度被改写或删掉了，"
                   f"这道门现在等于没跑")
    print(f"实际：正文章 {act['正文章数']}，有语录 {act['有语录章数']}，"
          f"留空 {len(act['留空章'])} 章 {act['留空章']}，非逐字 {len(act['非逐字章'])} 条 {act['非逐字章']}")
    print(f"附录 A 的承诺：{len(claims)} 处")
    if bad:
        print(f"不一致 {len(bad)} 处：")
        for b in bad:
            print("  ✗ " + b)
        return 1
    print("附录 A 的语录达成度声明与 quotes.yaml 一致 ✓")
    return 0


def selftest() -> int:
    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix="qc_")
    try:
        body = ["00", "01", "02", "03"]
        for u in body:
            os.makedirs(os.path.join(d, "drafts", f"unit-{u}"), exist_ok=True)
            io.open(os.path.join(d, "drafts", f"unit-{u}", "draft.md"), "w", encoding="utf-8").write(
                f"# 第 {u} 章 标题\n")
        os.makedirs(os.path.join(d, "drafts", "unit-41"), exist_ok=True)
        io.open(os.path.join(d, "drafts", "unit-41", "draft.md"), "w", encoding="utf-8").write(
            "# 附录 A：口径\n\n**这条规则的实际达成度**：41 个正文章里 **32 章**有逐字可回读的语录，"
            "**9 章留空**——第 05、07 章（扭矩与换向）。\n"
            "其中 **5 条**（第 17、19 章）是演讲整理稿、书面化微调或记者转述。\n")
        os.makedirs(os.path.join(d, "bible"), exist_ok=True)
        io.open(os.path.join(d, "bible", "quotes.yaml"), "w", encoding="utf-8").write(
            "quotes:\n  '00':\n    text: 甲\n    kind: 直接引语\n"
            "  '01':\n    text: 乙\n    kind: 演讲整理稿（非逐字）\n"
            "  '41':\n    text: 丙\n    kind: 直接引语\n")
        act = actual(d)
        claims = claims_in_appendix_a(d)
        ok1 = act["正文章数"] == 4 and act["有语录章数"] == 2      # 只数正文，键 '41' 不算
        ok2 = act["留空章"] == ["02", "03"] and act["非逐字章"] == ["01"]
        ok3 = ("正文章数", 41, 3) in [(n, v, l) for n, v, l in claims]        # 门看见了"41 个正文章"
        ok4 = ("留空清单", ["05", "07"], 3) in claims
        ok5 = ("非逐字清单", ["17", "19"], 4) in claims
        # 三处假现场必须被抓
        drifts = []
        if ("正文章数", 41) in [(n, v) for n, v, _ in claims] and act["正文章数"] != 41:
            drifts.append("正文章数")
        if act["留空章"] != ["05", "07"]:
            drifts.append("留空清单")
        if act["非逐字章"] != ["17", "19"]:
            drifts.append("非逐字清单")
        ok6 = len(drifts) == 3
        ok7 = bool(act["挂到附录的键"])                            # '41' 这个键要被点出来
        empty = claims_in_appendix_a(os.path.join(d, "nowhere"))
        ok8 = len(empty) == 0                                      # 没输入时由 MIN_CLAIMS 拦
        checks = [
            ("正文/附录分开数（附录上的语录键不算达成）", ok1 and ok7),
            ("留空章与非逐字章由 quotes.yaml 算出", ok2),
            (f"附录 A 的承诺被读到（{len(claims)} 处）", len(claims) >= MIN_CLAIMS),
            ("写的『41 个正文章』被当成承诺取出来", ok3),
            ("写的留空章号清单被取出来", ok4),
            ("写的非逐字章号清单被取出来", ok5),
            ("三处过期（章数/留空清单/非逐字清单）全部会被判不一致", ok6),
            ("附录 A 缺失时承诺数为 0，由 MIN_CLAIMS 自曝空跑", ok8),
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
