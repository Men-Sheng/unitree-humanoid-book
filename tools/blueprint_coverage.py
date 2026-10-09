#!/usr/bin/env python3
"""tools/blueprint_coverage.py — 蓝图覆盖矩阵里那句"可自己复跑"，现在真的能跑。

背景：`verification/blueprint-coverage.md` 逐格记录作者蓝图 BOM 的每个子系统落在哪几章，
并写着"检测方式：对每个条目取判别关键词，`grep -rlEi` 扫 drafts/，命中的章号列在下面（可自己复跑）"。
但**判别词没有写进表里**，读者只能照条目名自己猜——这跟附录 B 曾经"声称由不存在的脚本生成"是同一类问题。

这个脚本把那句话兑现：判别词就取条目括号里那一串（`关节执行器（集成度 / 双编码器 / 齿隙 / 温升）`
→ 四个词），逐个在 `drafts/unit-*/draft.md` 里搜，命中的章号取并集，与表里记的章号清单比。

两种不一致分开报：
  · **某一行在全书里一个判别词都搜不到** → 硬失败（这一格是虚标的，没有落点）；
  · **表里记了某章、那章没搜到词** → 只进清单不判死：自动取词精度有限，
    一章讲六维力时完全可能通篇写"力矩传感器"。判死会让人学会忽略它（与 --claims 同一条理由）。
找不到任何可核对的行时自曝"这道门等于没跑"。
用法：python -X utf8 tools/blueprint_coverage.py [--selftest] [--verbose]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, "verification", "blueprint-coverage.md")
MIN_ROWS = 15


def drafts():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        u = os.path.basename(os.path.dirname(p)).replace("unit-", "")
        out[u] = io.open(p, encoding="utf-8").read()
    return out


STOP = {"对照", "清单", "四条路线", "四档", "功能", "本轮补齐", "覆盖", "不讲", "取舍", "等", "与"}


def keywords(item: str) -> list[str]:
    """判别词 = 条目名括号**外**的部分 + 括号**内**的部分，按 / ／ 、 三种斜杠或顿号切开。
    只用括号内会漏掉 `ROS 2 / DDS / unitree_sdk2 / AimRT（三家中间件对照）` 这种"词在外面、
    说明在括号里"的行；只按半角 / 切会漏掉 `Cosmos／Genie 3／…` 这种全角斜杠。"""
    m = re.search(r"（([^（）]*)）\s*$", item.strip())
    inner = m.group(1) if m else ""
    outer = item.strip()[: m.start()] if m else item.strip()
    parts: list[str] = []
    for src in (outer, inner):          # **分别切**：拼起来再切会造出"结构与机械 丝杠"这种粘连词
        parts += [x.strip() for x in re.split(r"[/／、，,]", src) if x.strip()]
    out = []
    for p in parts:
        p = re.sub(r"^\s*功能[:：]\s*", "", p).strip()
        if len(p) < 2 or p in STOP:
            continue
        out.append(p)
    return out


def hits(kws: list[str], body: dict) -> list[str]:
    got = set()
    pats = [re.compile(re.escape(k), re.I) for k in kws]
    for u, txt in body.items():
        flat = re.sub(r"\s+", "", txt)
        if any(p.search(txt) or re.search(p.pattern.replace("\\ ", ""), flat) for p in pats):
            got.add(u)
    return sorted(got)


def rows(md: str):
    """只读**归属表**（章号那一列是 `26, 39, 43` 这种清单）。

    文档里还有别的表，最典型的是 2026-10-09 追加的「逐格人工判定」一节：它的第一列也是条目名，
    第二列却写成 `00:双目@34 / 03:深度相机@128` 这种"章:词@行号"。上一版把它当归属表读，
    于是"视觉与深度"这种**没有括号的简称**被当判别词去全书搜——搜不到，判成虚标格子。
    门自己造了一条假指控。现在两道保险：带 `@` 的行跳过；条目名不在正文里的简称行也跳过
    （真表的条目名一律带括号里的判别词）。"""
    skip_section = False
    for line in md.split("\n"):
        if line.startswith('#'):
            skip_section = ('人工判定' in line) or ('判别词' in line)
            continue
        if skip_section:
            continue
        if not line.startswith("| ") or line.startswith("|---") or "蓝图条目" in line:
            continue
        if '@' in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        item, chs, status = cells[0], cells[1], cells[2]
        ids = re.findall(r"\b(\d{2})\b", chs)
        if not ids or "不讲" in status:
            continue
        yield item, sorted(set(ids)), status


def check(body=None, table=None, verbose=False):
    """返回 (可核对行数, 额外命中数, 硬失败列表, 软清单列表)。

    硬失败只留一条**判得准的**：某一行在全书里一个判别词都搜不到 ⇒ 这一格是虚标的。
    "表里记了某章但那章没搜到词"只当清单：自动取的判别词精度不够（一章完全可能在讲
    六维力时用的是"力矩传感器"），判死会让人学会忽略它——与 check_xrefs --claims 同一个理由。"""
    body = body or drafts()
    table = table if table is not None else io.open(TABLE, encoding="utf-8").read()
    hard, soft = [], []
    n_rows = notes = 0
    for item, recorded, status in rows(table):
        kws = keywords(item)
        if not kws:
            continue
        n_rows += 1
        got = set(hits(kws, body))
        if not got:
            hard.append(f"{item}：全书搜不到任何一个判别词（{' / '.join(kws[:6])}）——这一格没有落点")
            continue
        missing = [c for c in recorded if c not in got]
        extra = sorted(got - set(recorded))
        notes += len(extra)
        if missing:
            soft.append(f"{item}：表里记了第 {'、'.join(missing)} 章，"
                        f"那几章没搜到判别词（自动取词，可能是同义说法）")
        if extra and verbose:
            print(f"  · {item}：另外还落在 {extra}")
    return n_rows, notes, hard, soft


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    verbose = "--verbose" in sys.argv
    body = drafts()
    n_rows, notes, hard, soft = check(body, verbose=verbose)
    print(f"覆盖矩阵：可核对行 {n_rows} 行（判别词由条目名自动取）；"
          f"额外命中（只报不拦）{notes} 处；章号待复核（清单）{len(soft)} 行")
    if n_rows < MIN_ROWS:
        print(f"✗ 只认出 {n_rows} 行（应 ≥{MIN_ROWS}）：表格式变了或文件没读到，这道门现在等于没跑")
        return 1
    for s in soft:
        print("  · " + s)
    if hard:
        print(f"虚标 {len(hard)} 行：")
        for b in hard:
            print("  ✗ " + b)
        return 1
    print("每一格都能在全书里搜到落点 ✓")
    return 0


def selftest() -> int:
    body = {
        "01": "这一章讲 集成度 与 双编码器 的取舍。",
        "02": "这一章只讲齿隙。",
        "03": "这一章提到 AimRT 与 ROS 2。",
    }
    table = ("| 蓝图条目 | 落在哪些章 | 状态 |\n|---|---|---|\n"
             "| 关节执行器（集成度 / 双编码器 / 齿隙 / 温升） | 01, 02 | 覆盖 |\n"
             "| 关节执行器（集成度 / 双编码器 / 齿隙 / 温升） | 01, 03 | 覆盖 |\n"
             "| 不存在的器件（紫霞神功 / 御剑飞行） | 01 | 覆盖 |\n"
             "| ROS 2 / DDS / AimRT（三家中间件对照） | 03 | 覆盖 |\n")
    n, notes, hard, soft = check(body, table)
    ok1 = n == 4
    ok2 = len(hard) == 1 and "紫霞神功" in hard[0]              # 全书搜不到的那一格才算虚标
    ok3 = any("第 03 章" in s for s in soft)                     # 记了但没搜到 → 只进清单
    ok4 = not any("AimRT" in s for s in hard + soft)   # 命中的格子不进任何清单
    ok9 = "结构与机械 丝杠" not in "".join(keywords("结构与机械（丝杠 / 直线执行器）"))
    kws = keywords("关节执行器（集成度 / 双编码器 / 齿隙）")
    ok5 = all(x in kws for x in ("集成度", "双编码器", "齿隙")) and not any(" " in k and k.startswith("关节执行器") for k in kws)
    ok6 = "ROS 2" in keywords("ROS 2 / DDS / AimRT（三家中间件对照）")   # 词在括号外也要取到
    ok7 = "Genie 3" in keywords("世界模型四条路线（Cosmos／Genie 3／1X）")  # 全角斜杠
    n2, _, h2, _ = check(body, "| 蓝图条目 | 落在哪些章 | 状态 |\n|---|---|---|\n")
    ok8 = n2 == 0 and not h2
    checks = [("四行都可核对", ok1), ("全书搜不到落点的格子判硬失败", ok2),
              ("记了某章但没搜到词只进清单（精度不够不判死）", ok3),
              ("判别词按 / 与 ／ 与 、 三种切", ok5 and ok7),
              ("括号外的名字也当判别词", ok6),
              ("表为空时认出 0 行（由 MIN_ROWS 拦）", ok8),
              ("括号外的名字不会与括号内的词粘连", ok9)]
    bad_n = 0
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
        bad_n += 0 if ok else 1
    print("自检 %d/%d" % (len(checks) - bad_n, len(checks)))
    return 0 if bad_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
