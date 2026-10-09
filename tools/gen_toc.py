#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/gen_toc.py — 从 outline/units.yaml 生成 toc.md（人读目录）。

单一真源是 yaml；本脚本只排版，不新增事实。跑法：
    python tools/gen_toc.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):  # Windows GBK 控制台
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# 叙述尺度 → 人话标签。这是本书的骨架原则：整体 → 局部 → 底层 → 回到整体 → 再往深里问
ZOOM = {
    "whole": "整体", "part": "局部", "base": "底层",
    "cross": "横切", "deep": "深究", "epilogue": "尾声", "appendix": "附录",
}

ROADMAP = """| 你是谁 | 必读 | 说明 |
|---|---|---|
| 做算法 / 模型 / 数据 | 00 → 02 → 26 → 27 → 28 → 29-34 → 附录 B | 但请至少补 04 与 12：那两章告诉你模型输出的数在机器里被谁执行 |
| 做硬件 / 嵌入式 / 电力电子 | 00 → 04-15 → 27 → 35-37 → 附录 C | 第 1 部是全书技术核心 |
| 做机械 / 结构 / 减速器 | 02 → 03 → 14 → 15 → 16 → 18 → 22 → 36 | 齿隙、模态、热是三条主线 |
| 想转行进机器人行业 | 00 → 04 → 05 → 07 → 08 → 10 → 12 → 14 → 40 | 八章走完就懂一颗关节；40 是十二个月路线 |
| 只想看懂新闻里那些人形 | 00 → 02 → 16 → 26 → 33 → 38 | 零公式路线，遇到推导看结论即可 |
"""

CONTRACT = """
## 每章动笔前必须填的"叙述契约"

科普书的失败方式不是写错，是**尺度跳层**（读者还在"腿"这一层，作者已经到"电流"那一层）和**类比越界**（类比好笑得开始说谎）。所以每章先填这张卡：

```yaml
contract:
  reader_enters_knowing:   # 读者进这一章时已经知道什么（引前章编号）
  zoom:                    # 本章尺度：整体 / 局部 / 底层 / 横切 / 深究
  zoom_step:               # 相对上一章是"往下看一层"还是"横向换一个例子"，不许跳两级
  one_thing:               # 读者读完只记住一句话，就是这句
  anchor_number:           # 本章唯一必须能复算的数（来源标记：厂/拆/算/查）
  analogy:                 # 主类比，最多一个
  analogy_breaks_at:       # 这个类比在哪里开始说谎 —— 必填，不许空
  terms_introduced:        # 新术语，硬上限 3 个，且必须先有现象再给名字
  deliberately_out:        # 这一章故意不讲什么
  humor_devices:           # 允许的手法：自嘲 / 反差 / 拟物 / 荒谬假设 / 具体到难为情的细节
  code:                    # none | pseudo —— 全书不出现可复制的工程代码
  sources:                 # 挂 bible/sources.md 编号
  accumulate:              # 第 1 部专用（《编码》法）：本章结束时读者手里有什么、还缺什么
  checkable_list:          # 章末可核对清单：每个关键数字一行（值 | 厂/拆/算/查 | 算式或量具 | 日期）
```

`analogy_breaks_at` 是硬要求：**每个类比都必须写出它失效的地方**。这是"幽默但不失真"最省事的机制——读者知道边界，作者也就不会滑过去。

`accumulate` 是第 1 部的叙述轴：像《编码》那样**每章只加一个新机制**，章末回答"现在它能做什么、还缺什么"。第 1 部 10 章已经填好这条（见 `outline/units.yaml`），它保证读者永远知道自己在第几层。

三条从别人翻车现场抄来的红线，写进每章自检：① 第 4 部**难度不许突升**（换例子不换叙述者）；② 单一规律章（21）必须写**它解释不了什么**；③ 真机数据章（25-31）必须写**这台做不到什么**，否则就是品牌软文。
"""


def main() -> int:
    units = yaml.safe_load(
        (ROOT / "outline" / "units.yaml").read_text(encoding="utf-8"))["units"]
    for u in units:
        if not isinstance(u["unit"], str):
            print("units.yaml 里的 unit 必须加引号（08/09 会被 YAML 当八进制失败、"
                  "00-07 当整数）", file=sys.stderr)
            return 1
    tot = sum(x["target_words"] for x in units)
    spine = [x for x in units if x["part"].startswith(("第 0", "第 1", "第 2"))]
    spine_w = sum(x["target_words"] for x in spine)

    L = ["# 目录（Phase 2 草稿，待你批准）\n",
         "> 本文件由 `python tools/gen_toc.py` 从 `outline/units.yaml` 生成，改目录请改 yaml 再重跑。\n",
         "> **尺度** = 叙述所在的层级（整体 / 局部 / 底层 / 横切 / 深究）。全书顺序就是一条往下钻的路线："
         "先看见一台机器，再拆开它，再问它凭什么站得住；然后横向换几个机型验证同一套原理；最后给想再深一层的人。",
         "> **门禁** = `gate_critical`（写完必须过 3 个盲评 agent 的反驳）；**实测** = 本章有只有亲手量/亲眼看到才能填的数；"
         "**代码** = pseudo 表示只出现伪流程，全书 `real` 代码为零。\n",
         f"> 共 {len(units)} 章，{tot/10000:.1f} 万字（约 {tot/450:.0f} 页正文）；"
         f"{sum(1 for x in units if x['gate_critical'])} 章过门禁、"
         f"{sum(1 for x in units if x.get('needs_measure'))} 章需要实测、"
         f"{sum(1 for x in units if x.get('code') == 'none')}/{len(units)} 章零代码。\n",
         "\n## 四条读者路线\n", ROADMAP, "\n## 分部目录\n",
         "| # | 章 | 尺度 | 门禁 | 实测 | 代码 | 千字 |",
         "|---|---|---|---|---|---|---|"]

    cur = None
    for x in units:
        if x["part"] != cur:
            cur = x["part"]
            L.append(f"| **—** | **{cur}** | | | | | |")
        L.append("| {} | {} | {} | {} | {} | {} | {:.1f} |".format(
            x["unit"], x["title"], ZOOM.get(x.get("zoom", ""), x.get("zoom", "")),
            "★" if x["gate_critical"] else "",
            "✓" if x.get("needs_measure") else "",
            x.get("code", "none"),
            x["target_words"] / 1000))

    L.append("\n## 每章的锚点数与主类比（草稿，数字待 research/unitree-hardware.md 填入）\n")
    L.append("| # | 锚点数（来源标记） | 主类比 |")
    L.append("|---|---|---|")
    for x in units:
        if x.get("anchor_number") or x.get("analogy"):
            L.append("| {} | {} | {} |".format(
                x["unit"], (x.get("anchor_number") or "—").replace("|", "/"),
                (x.get("analogy") or "—").replace("|", "/")))

    L.append(CONTRACT)
    L.append(f"""
## 分期：这本书可以一次发完，也可以拆两本

**第一批可发布 = 第 0-2 部（unit 00-24）= {len(spine)} 章、{spine_w/10000:.1f} 万字。**
骨架是**向下挖到不可商量的物理约束，再一层层建回来**：六个时间域（00）→ 人形产品线（02-03）→ 一颗关节从电流挖到 MOSFET（04-15）→ 从关节建回姿态（16-22）→ 感知与算力（23-28）→ 大脑与数据（29-34）→ 撑不住的地方（35-39）。书名暂定《人形机器人：从一颗关节往下挖》，待作者定。
第 3 部（全系列横切）+ 第 4 部（再往深里问）+ 尾声 + 附录作为第二册或"扩展篇"，等第一批的读者反馈再定——**因为第 3 部的每个数字都要重新核一遍厂商口径，那是最容易被产品迭代打脸的部分。**

## 批准清单（你签字前不写一个字正文）

- [ ] **尺度顺序**成立吗：整体(00-03) → 局部(04-13) → 底层(14-24) → 横切(25-31) → 深究(32-37)。这是你说的"从整体走向局部走向底层"，我把它变成了硬约束（每章契约里的 `zoom_step` 不许跳两级）
- [ ] 第 1 部（器件拆解，10 章 4.2 万字）和第 3 部（全系列横切，7 章 3 万字）是重点，占比够不够？要不要再加"拆解深度"（例如单独一章讲驱动板与 MOSFET、一章讲热设计）
- [ ] 45 章里有没有不必写的——**删章比加章重要**
- [ ] 第 4 部只留 6 章、全部零工程代码（只有伪流程）：这个"少代码"的度对不对
- [ ] 三条读者路线是否真覆盖你说的"科普读者为主、轻度爱好者与工作者次之"
- [ ] 分两本发（先 25 章 10.3 万字）还是一次写完 45 章
- [ ] 书名（`manifesto.md` §1 三个候选）
""")
    out = ROOT / "toc.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out} — {len(units)} 章 / {tot/10000:.1f} 万字；第一批 {len(spine)} 章 / {spine_w/10000:.1f} 万字")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
