#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_terms.py — 校验"先现象后命名"与每章术语预算（voice-profile §3 / §3.1）。

① 未定义先用：某概念的中文名出现在它 introduced_in 之前的稿子里 → 违规。
   （科普书最隐蔽的掉车点：作者以为"这词大家懂"。）
② 每章新术语 ≤3：本章稿中出现的、introduced_in 指向本章的概念数超预算 → 违规。
③ 行话黑名单：出现时同段无"——"或"（…）"式即时解释 → 违规。

已知局限（别把它当成全知）：概念名只取 ≥3 字的片段做匹配，两字词（摩擦、总线、骨架）
是日常用语，拿来判定会大量误报；这类词靠 §3.1 的人工自检兜。

用法：python tools/check_terms.py unit-02 | --all
退出码：0 通过；1 有违规；2 用法错误。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
NL = chr(10)
BLANK = chr(92) + "n" + chr(92) + "s*" + chr(92) + "n"
TERM_BUDGET = 6  # v3：读者是有从业经验的工程师，需要准确命名而不是被保护
# v3（2026-10-08）：受众改为有从业经验的工程师。
# 编码器 / 自由度 / 减速比 / 背隙 / 闭环 / 执行器 / 里程计 / 点云 / 标称 属于**前置常识**，
# 已移入 knowledge-graph.yaml 的 prerequisites，不再当行话查（否则等于假装读者不懂 PID）。
# 留下的都是"机器人行业特有、跨行业工程师确实没见过"的词。
BLACKLIST = [
    "具身智能", "端到端", "世界模型", "域随机化", "正运动学", "逆运动学",
    "Sim2Real", "VLA", "支撑多边形", "零力矩点", "捕获点", "准直驱",
    "双编码器", "力透明度", "弱磁", "阻抗控制", "全身控制", "动作分块",
    "模仿学习", "流匹配", "本体感知", "代谢代价系数", "模型预测控制",
    "逆动力学", "扩展卡尔曼滤波", "师生蒸馏", "齿隙",  # 不查日常义的「透明度」；技术义用「力透明度」
    
]


def load_graph():
    kg = yaml.safe_load((ROOT / "bible" / "knowledge-graph.yaml").read_text(encoding="utf-8"))
    out = []
    for c in kg.get("concepts") or []:
        names = {c["id"]}
        for part in re.split(r"[（(、/]| vs ", c.get("name") or ""):
            part = part.strip().strip("“”\"\"'")
            if 3 <= len(part) <= 14:
                names.add(part)
        out.append({"id": c["id"], "unit": c.get("introduced_in"), "names": {n for n in names if n}})
    return out


def _has(text: str, name: str) -> bool:
    """纯 ASCII 名按整词匹配，避免 'imu' 命中 'Optimus' 这类假阳性。"""
    if not name:
        return False
    if name.isascii():
        return re.search(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", text, re.I) is not None
    return name in text


def unit_num(uid: str) -> int:
    return int(str(uid).rsplit("-", 1)[-1])


def strip_meta(text: str) -> str:
    """剥掉稿子开头的作者状态块（H1 之后连续的 > 引用行）。
    它会写"本章不许出现某某词"，不剥就自己举报自己。"""
    lines = text.split(NL)
    i = 0
    if i < len(lines) and lines[i].startswith("#"):
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
        i += 1
    return NL.join(lines[i:])


def check_one(md, concepts, cur_num, cur_uid):
    text = strip_meta(md.read_text(encoding="utf-8"))
    paras = [p for p in re.split(BLANK, text) if p.strip()]
    errs = []
    for c in concepts:
        if not c["unit"] or c["unit"] == cur_uid or unit_num(c["unit"]) <= cur_num:
            continue
        hit = next((n for n in c["names"] if n and _has(text, n)), None)
        if hit:
            # v3 例外：**带指向的前向引用合法。** 受众是工程师，允许"先给名字 + 一句它是什么 +
            # 指向展开它的那一章"。判据是首次出现那一段里带（……）式即时解释，或"第 NN 章"式指向。
            first = next((pp for pp in paras if _has(pp, hit) and not pp.lstrip().startswith("#")), "")
            glossed = ("（" in first and len(first.split("（")[-1]) > 8) or re.search(r"第 \d\d? 章", first)
            if not glossed:
                errs.append(f"未定义先用：'{hit}'（{c['id']}）要到 {c['unit']} 才引入，"
                            f"且首次出现那一段没有即时解释或章节指向（{md.name}）")
    here = [c for c in concepts if c["unit"] == cur_uid]
    used = [c["id"] for c in here if any(n and n in text for n in c["names"])]
    if len(used) > TERM_BUDGET:
        errs.append(f"术语预算超：{cur_uid} 出现 {len(used)} 个本章新概念（上限 {TERM_BUDGET}）：" + "、".join(used))
    # 只查**首次出现**那一段有没有即时解释。后面再用同一个词不必反复科普——
    # 要求每段都重解释会逼出糟糕的文风，那不是本工具的目的。
    for w in BLACKLIST:
        for i, para in enumerate(paras, start=1):
            # 小标题不算"首次出现"：标题里出现术语是命名，不是使用；
            # 要求标题里塞解释会产出无法读的排版。
            if w in para and not para.lstrip().startswith("#"):
                if "——" not in para and "（" not in para:
                    errs.append(f"裸行话：'{w}' 首次出现在第 {i} 段，同段无即时解释"
                                f"（加'——它是什么'，或把首次出现挪到有解释的那段）")
                break
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", nargs="?")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    concepts = load_graph()
    drafts = ROOT / "drafts"
    targets = []
    if a.all:
        for d in sorted(drafts.glob("unit-*")):
            targets += [(f, d.name) for f in sorted(d.glob("*.md"))]
    elif a.unit:
        d = drafts / a.unit
        files = sorted(d.glob("*.md"))
        if not files:
            print(f"{d} 下没有稿子", file=sys.stderr)
            return 2
        targets = [(f, a.unit) for f in files]
    else:
        ap.print_help()
        return 2
    total = 0
    for f, uid in targets:
        errs = check_one(f, concepts, unit_num(uid), uid)
        print(("✗" if errs else "✓") + f" {uid} {f.name}")
        for e in errs:
            print("   ", e)
        total += len(errs)
    print(NL + "全部通过" if total == 0 else NL + f"共 {total} 条待处理")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
