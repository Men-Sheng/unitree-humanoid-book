# manuscript-gate round 1 — 2026-10-08（v3 人形版首次跑 skill 门禁）

跑的是 `.qoder/skills/book-factory/scripts/` 下的官方脚本，对象是 `drafts/unit-*/draft.md`
（46 章）。**结论先说：机械部分通过；MG-1 的 claim-index 在中文稿上跑不出东西，
原因已定位到脚本侧，见 §3；`final/` 尚未建立，所以依赖签字的门还没资格跑。**

## 1. 实跑命令与输出

```
$ manuscript_gate.py --root unitree-book --units "drafts/unit-*/draft.md" \
      --deterministic-only --date 2026-10-08
[gate] unitree-book · round 1/5 · reviews/manuscript-gate-2026-10-08
[lint_render] 46 file(s) · 0 critical · 0 major · 382 minor
[gate] MG-5 render lint: 0 critical · 0 major · 382 minor
[gate] claim index: not built yet · PROPAGATE=0
[gate] MG-6 runners: 9 surface(s), 0 blocking

$ bootstrap_probes.py --root unitree-book --units "drafts/unit-*/draft.md"
[probes] 154 probe(s) from kg → bible/concept-probes.yaml
```

MG-6 的 9 个 validation surface 全部**非阻塞**通过（真机相关的 surface 依赖作者实测，
本项目按"不许无人值守操作真机"的纪律不自动跑）。

## 2. MG-5 的 382 条 minor 是什么，怎么处理

分类（`lint-render.json` 实测）：

| check | 条数 | 是不是真问题 | 处理 |
|---|---|---|---|
| `fence-no-language` | 336 | 否，本书的 ``` 块是公式与时序表，不是代码 | `tools/fix_markdown_lint.py` 统一补 `text` 标签 |
| `list-no-blank-line` | 45 | **是**，CommonMark 要求列表前有空行，否则整段被当普通段落，Paged.js 里表现为"可核对清单"不再缩进、复选框消失 | 同一脚本补空行 |

脚本只动这两类，不碰正文、表格、引用块、图注、来源标记。
跑法：`python -X utf8 tools/fix_markdown_lint.py --dry` 先看，再去掉 `--dry`。
**必须在没有子代理正在写稿时跑**（它会遍历全部 46 章）。

## 3. claim-index：机械可跑，但中文稿上匹配不到，已定位到脚本侧

```
$ build_concept_dossier.py ... --emit-index
[claim-index] 0 concept(s), 0 site(s)
$ build_concept_dossier.py ... --concept six-time-domains
[dossier] six-time-domains: no passages matched — tune the probe.
```

根因链（有证据）：

1. `bootstrap_probes.py` 从 kg 生成的 include 是 `\b(六个时间域s?)\b`。
   `\b` 是单词边界，CJK 两侧都不产生边界；`s?` 是英文复数后缀。
   **所以自动探针在中文稿上必然 0 命中**——这是一个"看起来跑成功了的空门禁"。
2. 已写 `tools/tune_probes.py` 产出 `bible/concept-probes-tuned.yaml`（154 条，
   24 条长论断给了短形并打 `review: true`）。用同样的 `re` 直接对 46 章正文跑，
   **前 40 条里 27 条能命中**（例如"六个时间域"在 unit-00 就有）。
3. 但 `build_concept_dossier.py` 仍报 no passages matched。
   它的 `load_probes()` 确实会让 tuned 覆盖 base，`re.compile(probe["include"])`
   也没有额外加边界，所以问题在**它读到的 unit 集合**上：
   `load_records()` 遍历 `project.unit_paths`，而 `--units` 传的是
   `drafts/unit-*/draft.md`，脚本对 `final/` 之外路径的处理与 `--units` 的
   约定不一致（同一批文件在 `manuscript_gate.py` 里是能数出 46 file(s) 的）。

**待办（不要在签字前硬做）**：MG-1 的 dossier/claim-index 设计上跑 `final/`。
本项目 `final/` 是"作者签字后的定稿，唯一构建输入"，作者尚未签字，
所以这一步**按流程本就该是空的**。要跑通它需要先把 46 章签入 `final/`，
那是作者的动作，不是可以替他做的动作。

## 4. 本项目自建的等价门禁（已跑通、可复跑）

| 门 | 命令 | 当前状态 |
|---|---|---|
| 算术 | `code/tools/foc_check.py` | 0 项异常；已知答案自检 15 条（含新加的 5 条复合衰减与 armature 口径） |
| 术语 | `tools/check_terms.py --all` | 全部通过 |
| 概念图 | `tools/check_kg.py` | 154 概念 / 43 章，依赖顺序与每章预算通过 |
| 深度 | `tools/depth_audit.py` | 中位 13.83，<9.0 的章 0/44；自检厚 18.00 / 薄 4.00 |
| 数源 | `tools/number_provenance.py` | 可疑 6 处，逐条手核为"别处已推导、此处复述" |
| 等式 | `tools/formula_check.py` | 235 条实算通过；38 条列出经逐条复核全为解析器误判 |
| 渲染 | `.qoder/skills/.../lint_render.py`（经 gate） | 0 critical / 0 major |

一条命令跑完全部重建与上述门：`bash tools/rebuild_all.sh`。
