# 《人形机器人：从一颗关节往下挖》— 项目根

> 版本 v3（2026-10-08）。前两版《…机器狗为什么踢不倒》（v2，四足科普）与开发者手册（v1）
> **均已被作者推翻**，理由与过程记在 `manifesto.md` §2。旧 README 的 v2 内容不再适用。

Phase 状态见 `project-status.yaml`（机器可读）。当前：**46 章全部成稿、两轮一手复验已跑、
交稿包已产出；深度门与来源门在跑；未过 manuscript-gate。**

## 先读这四个文件

| 文件 | 作用 |
|---|---|
| `manifesto.md` | 宪法：这本书是什么、凭什么存在、边界、已定决定、风险 |
| `bible/scope.md` | 范围：讲什么、**故意不讲什么**、深度政策、完成的定义 |
| `outline/toc.md` | 46 章目录 + 锚点数（由 `tools/gen_toc.py` 从 `outline/units.yaml` 生成） |
| `submission/CIP与交稿说明.md` | 给出版社的交稿清单：结构统计、四条已知印刷局限、脚本清单 |

## 这本书的验收线（作者 2026-10-08 原话）

> 技术再给我讲解深刻一点……比如 FOC(磁场定向控制) 的位置 速度 扭矩 本质是
> 被一个垂直于转子的磁场控制。磁场由电流控制。改变外面电流导通的时间，可以合成
> 为任意方向任意大小的磁场，来控制此转子。**你要讲到这种水平才。**
> 目标读者是**有一定相关从业经验基础、但没有接触过机器人的科技爱好者和工程师**。
> 另外：**只主要讲人形机器人**，不要讲那么多机器狗。

这条线被拆成了每章的 `dig` 四问（栈 / 机制 / 底座 / 边界），见 `outline/units.yaml`。

## 一条命令重建全部产物

```bash
bash tools/rebuild_all.sh          # 草稿 → print/src → SVG 栅格化 → PDF → 交稿包 → docx → 5 道门
bash tools/rebuild_all.sh --gates  # 只跑门
```

## 目录约定（book-factory `book-technical` profile）

```text
manifesto.md  scope 与宪法
bible/        scope.md sources.md glossary.md voice-profile.md images.md
              do-not-touch.md（75 条事实红线）continuity-tracker.md
              knowledge-graph.yaml archive-scope-v2-quadruped.md（作废留档）
outline/      units.yaml ← 单一真源；toc.md 与 figures.yaml 由它派生
              archive-units-{developer-manual,popsci-quadruped}.yaml（v1/v2 骨架）
drafts/       unit-NN/draft.md  ← 46 章正文
drafts-quadruped-popsci/        ← v2 旧稿，不参与构建
research/     一手规格核对表、蓝图覆盖核对、语录检索轮次
code/tools/   arithmetic_check.py foc_check.py calculations.yaml ← 全书 [算] 数的出处
tools/        build_book.py gen_toc.py make_figs*.py check_terms.py check_kg.py
              depth_audit.py number_provenance.py make_submission.py rebuild_all.sh
print/        build.mjs rasterize.mjs png2tif.py style.css → 印型 PDF
submission/   交稿包：docx + images/(300 dpi TIF+PNG) + 授权清单 + 声明 + CIP 说明
verification/ 核查单、深度作业单、复验记录
```

## 门禁（每个都真跑，不许口头宣布通过）

| 门 | 命令 | 判什么 |
|---|---|---|
| 算术 | `python -X utf8 code/tools/foc_check.py` | 每个 [算] 数能复现，含已知答案自检（当前 15 条） |
| 术语 | `python -X utf8 tools/check_terms.py --all` | 先现象后命名、每章 6 个新词预算、首现给解释 |
| 图谱 | `python -X utf8 tools/check_kg.py` | 158 概念的引入/使用顺序不许倒挂 |
| 引用 | `python -X utf8 tools/check_xrefs.py` | 652 处"第 NN 章"必须指到真实章节，且括注说的事真在那一章里 |
| 深度 | `python -X utf8 tools/depth_audit.py` | 追问链、公式密度、是否落到底层、边界与代价、可代入的数 |
| 数源 | `python -X utf8 tools/number_provenance.py` | 书稿里每个带单位的数，要么在一手资料/脚本里，要么删 |
| 等式 | `python -X utf8 tools/formula_check.py` | 把正文每个"算式 = 结果"真算一遍，抓算错 |
| 渲染 | `manuscript_gate.py --deterministic-only` | book-factory 的 MG-5/MG-6（0 critical / 0 major 才算过） |

**每道门都有 `--selftest`，且自检里必须有"故意做错"的反例**——
度量抓不到错误就等于没有度量。这条纪律已经抓到过作者本人五次算错与三次度量自身有偏。

## 四条不可协商的纪律

1. **你可以不讲，但不能讲错。** 每个数字带来源标记：[厂] 官方；[拆] 第三方拆解/券商，只当数量级；
   [行] 教科书与行业通识，**不是宇树事实**；[算] 本书推算，附录 B 有脚本；[未] 查不到。
   "查不到"是合法答案，且必须出现在附录 E。
2. **不把话塞进厂商嘴里。** 引号里必须是逐字引文，语录块必须写清出处与日期。
3. **冲突不抹平。** 官方口径与拆解口径不一致时两条都列，写明取哪条或"待复验"。
4. **每个类比必须写它在哪里开始说谎**（`analogy_breaks_at`），不填不许用。

## 还缺什么（不粉饰）

- 3 幅图要作者本人实拍（全身定妆照、腿部关节逐个特写、GO-M8010-6 拆机照）。
- 36 章没有可溯源且主题吻合的王兴兴语录——宁缺不假，正在第三轮检索。
- 书名、3 段文风校准样本、拆机以哪台机器为准：等作者签字。
- manuscript-gate（contract cards / digest / Critic 计分 + blind verify / claim-index）尚未对 v3 跑过。
- 8 个 `[算]` 量需要真机测量才能闭合（见 `verification/teardown-measures-*.md`，由作者自己跑）。
