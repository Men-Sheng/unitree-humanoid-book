#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/check_kg.py — 校验知识图谱与大纲的依赖顺序 + 每章术语预算。

科普书的两条铁律靠人记是记不住的，所以这里可执行化：
  ① 先现象后命名：一个概念的 requires 必须在**同一章或更早的章**被引入。
     依赖被引入得更晚 → 读者在这一章遇到没定义过的东西 → 掉车。
  ② 每章新术语 ≤6（voice-profile §3，v3 起）。超了就不是"提醒"，是失败。
  ③ 所有引用的 unit 必须存在；reinforced_in 不得早于 introduced_in。

退出码：0 全通过；1 有违规。
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
TERM_BUDGET = 6  # v3：读者是有从业经验的工程师，需要准确命名而不是被保护


def load():
    kg = yaml.safe_load((ROOT / "bible" / "knowledge-graph.yaml").read_text(encoding="utf-8"))
    units = yaml.safe_load((ROOT / "outline" / "units.yaml").read_text(encoding="utf-8"))["units"]
    return kg, units


def unit_num(uid: str) -> int:
    """'unit-16' -> 16；附录 unit-40..44 保持原序。"""
    return int(str(uid).rsplit("-", 1)[-1])


def main() -> int:
    kg, units = load()
    existing = {f"unit-{u['unit']}" for u in units}
    concepts = kg.get("concepts") or []
    intro = {c["id"]: c.get("introduced_in") for c in concepts}
    errs: list[str] = []
    per_unit: dict[str, list[str]] = defaultdict(list)

    for c in concepts:
        cid = c["id"]
        here = intro[cid]
        if here not in existing:
            errs.append(f"{cid}: introduced_in={here} 在 units.yaml 里不存在")
            continue
        per_unit[here].append(cid)
        for dep in c.get("requires") or []:
            if dep not in intro:
                errs.append(f"{cid}: requires 未知概念 {dep}")
                continue
            d_here = intro[dep]
            if d_here not in existing:
                errs.append(f"{dep}: 被 {cid} 依赖，但它自己的 introduced_in={d_here} 无效")
                continue
            if unit_num(d_here) > unit_num(here):
                errs.append(
                    f"顺序违规：{cid}（{here}）依赖 {dep}（{d_here}）——"
                    f"读者会在遇到定义之前先遇到它")
        for r in c.get("reinforced_in") or []:
            if r not in existing:
                errs.append(f"{cid}: reinforced_in={r} 不存在")
            elif unit_num(r) < unit_num(here):
                errs.append(f"{cid}: reinforced_in={r} 早于 introduced_in={here}")

    over = {u: ids for u, ids in per_unit.items() if len(ids) > TERM_BUDGET}
    for u, ids in sorted(over.items(), key=lambda kv: unit_num(kv[0])):
        errs.append(
            f"术语预算超：{u} 引入 {len(ids)} 个新概念（上限 {TERM_BUDGET}）："
            + "、".join(ids) + " —— 拆章、把部分概念降级为'只描述现象不命名'，或后移")

    total = len(concepts)
    covered = len(per_unit)
    print(f"概念 {total} 个，分布在 {covered}/{len(existing)} 章；"
          f"未被任何章引入的概念 0 个（本图即权威清单）")
    dist = sorted(((u, len(ids)) for u, ids in per_unit.items()), key=lambda kv: unit_num(kv[0]))
    print("每章新概念数：" + "  ".join(f"{u.replace('unit-', '')}:{n}" for u, n in dist))

    if errs:
        print(f"\n违规 {len(errs)} 条：")
        for e in errs:
            print("  ✗", e)
        return 1
    print("\n✓ 依赖顺序、术语预算、章节引用全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
