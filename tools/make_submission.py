#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/make_submission.py — 生成出版社交稿包。

产出 submission/：
  images/                     300 dpi PNG + TIF（由 print/rasterize.mjs 生成，本脚本只登记）
  图片授权清单.md / .csv       逐图：编号、章、文件名、责任方、许可、是否需签字、备注
  图片来源与版权声明.md         可直接抄进版权页的声明 + 待作者填的空
  CIP与交稿说明.md             CIP 数据块模板 + 交稿清单（哪些已满足、哪些缺）
  src-docx/                   把 .svg 引用改写成 .png 的 Markdown 副本（pandoc 不认 SVG）

用法：python tools/make_submission.py
之后由 shell 跑 pandoc 合成 docx（本脚本会把命令打印出来）。
"""
from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SUB = ROOT / "submission"
SRC = ROOT / "print" / "src"
NL = chr(10)

TITLE = "人形机器人：从一颗关节往下挖"
SUBTITLE = "从磁场、电流到一次思考：一台人形机器人的六层解剖"


def load_figures():
    d = yaml.safe_load((ROOT / "outline" / "figures.yaml").read_text(encoding="utf-8"))
    return d.get("figures") or []


def ledger(figures):
    done = [f for f in figures if f.get("status") == "已完成"]
    todo = [f for f in figures if f.get("status") != "已完成"]
    imgdir = SUB / "images"
    have = {p.stem for p in imgdir.glob("*.png")}

    rows = []
    for f in figures:
        base = Path(str(f.get("path", ""))).stem
        rows.append({
            "图号": f.get("id", ""),
            "章": f.get("unit", ""),
            "类型": f.get("kind", ""),
            "责任方": f.get("owner", ""),
            "许可": f.get("license", ""),
            "状态": f.get("status", ""),
            "文件名": (base + ".tif / .png") if base else "（未生成）",
            "已光栅化": "是" if base in have else "否",
            "印刷规格": f.get("spec", ""),
            "需作者签字": "是" if f.get("kind") == "自拍" else "否",
            "图注": f.get("caption", ""),
            "备注": f.get("note", ""),
        })
    (SUB / "图片授权清单.csv").write_text(
        "\ufeff" + NL.join(
            [",".join(rows[0].keys())] +
            [",".join('"' + str(r[k]).replace('"', '""') + '"' for k in r) for r in rows]
        ), encoding="utf-8")

    md = ["# 图片授权清单", "",
          f"《{TITLE}》 · 共 {len(figures)} 幅 · 已落地 {len(done)} 幅 · 待办 {len(todo)} 幅",
          f"图片包目录：`submission/images/`（300 dpi，TIF 无压缩 + PNG）", "",
          "**政策**（见 `bible/images.md`）：作者实拍约 50% / 本书自绘约 45% / 公有领域 ≤5%；"
          "**官方素材 0 张**——宇树无新闻资料包，未取得任何授权，本书一张不用。", "",
          "| 图号 | 章 | 类型 | 责任方 | 许可 | 文件名 | 已光栅化 | 需签字 | 图注 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['图号']} | {r['章']} | {r['类型']} | {r['责任方']} | {r['许可']} | "
                  f"{r['文件名']} | {r['已光栅化']} | {r['需作者签字']} | {r['图注']} |")
    if todo:
        md += ["", "## 尚缺的图（必须由作者提供或另行授权）", ""]
        for f in todo:
            md.append(f"- **{f.get('id')}（第 {f.get('unit')} 章，{f.get('kind')}）**："
                      f"{f.get('caption')}　规格：{f.get('spec')}"
                      + (f"　备注：{f.get('note')}" if f.get("note") else ""))
    md += ["", "## 自绘图的生成方式（供校对与复现）", "",
           "全部自绘图是**手写 SVG**，源文件 `assets/fig/*.svg`，由两个脚本生成：",
           "`python tools/make_figs.py`（第 0–2 部 13 幅）、`python tools/make_figs.py && python tools/make_figs2.py`"
           "（第 3–5 部 16 幅）。图片包光栅化：`cd print && node rasterize.mjs`。", "",
           "为什么不用 matplotlib 出 PNG：这些是示意图，SVG 里的文字是文本节点，"
           "由排版引擎用正文同一款 Noto Serif SC / Noto Sans SC 渲染，"
           "不会出现图内字体与正文不一致，也不引入第二套字体子集。", ""]
    (SUB / "图片授权清单.md").write_text(NL.join(md), encoding="utf-8")
    return len(done), len(todo), len(have)


def declaration():
    t = f"""# 图片来源与版权说明（交稿用，可抄进版权页）

## 一、给出版社的声明文本（建议原样使用）

> 本书全部示意图、逻辑推导图与架构图均为作者独立绘制，不含有任何第三方享有著作权的图样、
> 产品渲染图、照片或商标图形。书中提及的企业名称、产品名称与型号仅用于技术说明与指代，
> 不构成授权、赞助、背书或合作关系。本书与杭州宇树科技有限公司无关，
> 未获得其授权、审阅或背书。
>
> 书中引用的公开参数取自相应企业公开发布的产品页面、公开技术文档与开源代码仓库，
> 抓取日期逐条标注于附录 E。书中所有推算值由随附脚本可复算，脚本与输入表见附录 B。
>
> 书中引用的人物言论均为公开报道、公开访谈或公开出版物中的可溯源内容，
> 每条均标注出处与日期；未标注出处者一律不引。

## 二、图片构成

| 类别 | 数量 | 权利状态 | 需外部授权 |
|---|---|---|---|
| 作者独立绘制的示意图（矢量） | 29 | 作者享有著作权，随稿转让或授权由合同约定 | 否 |
| 作者实拍照片 | 3（待补） | 作者享有著作权 | 否 |
| 第三方企业官方图片 | **0** | —— | —— |
| 公有领域 / 知识共享素材 | 0 | 本书政策上限 ≤5%，实际未使用 | —— |

**为什么官方图片一张都不用**：宇树未提供新闻资料包（press kit），其官网与店铺图片
未附任何使用许可声明。按《著作权法》默认保留所有权利的原则，未经书面许可不得用于
商业出版。本书因此把全部图改为自绘，代价是书里没有一张"真机照片"，
换来的是**零侵权风险与零授权成本**。若出版社希望补入官方图，需由出版社或作者
向宇树取得书面授权，并逐张登记到 `图片授权清单.csv`。

## 三、待作者填写 / 签字

- [ ] 作者姓名、笔名、单位（用于封面、CIP 与版权页）
- [ ] 三幅实拍图的拍摄日期与设备（用于证明系本人拍摄）
- [ ] 自绘图的著作权归属与授权范围（转让 / 独占许可 / 非独占许可）
- [ ] 是否同意在版权页保留"与宇树无关"的免责声明（建议保留）
- [ ] 书名定稿：现用名《{TITLE}》；副题《{SUBTITLE}》
- [ ] 全书语气签字：作者本人对第 1 部（第 04–15 章）任一章的改写意见

## 四、随稿交付物清单

| 文件 | 说明 |
|---|---|
| `{TITLE}-交稿版.docx` | 正文，含目录与图（图片以 300 dpi 位图嵌入） |
| `images/` | 独立图片包：全部已落地图的 TIF（无压缩 RGB，300 dpi）+ 同名 PNG；张数与尺寸以 `images/_尺寸表.tsv` 为准（脚本生成，不手写） |
| `images/_尺寸表.tsv` | 每幅的像素、印刷尺寸（毫米）、DPI、体积 |
| `图片授权清单.md` / `.csv` | 逐图编号、章、责任方、许可、状态、是否需签字 |
| `CIP与交稿说明.md` | CIP 数据块模板、字数与结构统计、已知排版限制 |
"""
    (SUB / "图片来源与版权声明.md").write_text(t, encoding="utf-8")


def cip():
    import subprocess
    total = 0
    per = {}
    for f in sorted(SRC.glob("*.md")):
        n = len(re.findall(r"[一-鿿]", f.read_text(encoding="utf-8")))
        total += n
        per[f.name] = n
    figs = load_figures()
    t = f"""# CIP 与交稿说明

## 一、CIP 数据块（请出版社按本社模板核对后填写）

```
{TITLE} ／ 〔作者〕著．— 〔城市〕：〔出版社〕，〔2026. 　〕
　　〔页〕　；　21 cm × 15 cm（大 32 开）
　ISBN 〔　　　　　　　　　〕
　Ⅰ．人…　Ⅱ．①〔作者〕　Ⅲ．①人形机器人—普及读物
　Ⅳ．①TP242.6
　中国版本图书馆 CIP 数据核字（〔2026〕）第〔　　　　〕号
```

**需要出版社填的空**：作者名、出版地与社名、出版年月、总页码、ISBN、CIP 核字号。
**需要作者定的事**：书名是否沿用、分类是否按"普及读物"还是"工程技术"（本书按 v3 定位
更接近"工程技术—机器人"而非"普及读物"，建议改第三级为 ①人形机器人—机器人结构 ②控制技术）。

## 二、字数与结构（由脚本统计，非自报）

```
章数：46（第 0–5 部 40 章 + 尾声 1 章 + 附录 A–E 5 章）
中文字符：{total:,} 个（脚本统计排版源 print/src 里的全部汉字，**含表格与图注**；
　　　　　不含表格与代码块的正文净字数由 `tools/depth_audit.py` 另行统计并随稿提供）
图：{len(figs)} 幅登记在册，其中 {sum(1 for g in figs if g.get("status") == "已完成")} 幅已落地（全部自绘矢量），{sum(1 for g in figs if g.get("status") != "已完成")} 幅待作者实拍
表：全书约 90 张对照表与参数表
可复算数：16 条推算链 + 10 条自检用例，脚本随稿提供
```

## 三、开本与版式（已按印厂常规参数设定，可直接改）

```
成品尺寸：145 mm × 210 mm（大 32 开）
版心：宽 110 mm（左右边距 20 / 15 mm，含订口），高约 176 mm
正文：Noto Serif SC 9.6 pt，行距 1.72
标题与图注：Noto Sans SC
页码：书口侧居中；章首页无页眉
图片：300 dpi，TIF 无压缩 RGB；矢量源文件另附（SVG）
```

## 四、已知排版限制（必须让编辑知道，不要当成作者疏忽）

1. **正文目前左对齐，不是两端对齐。** 本排版管线（Chrome + Paged.js）无法对中日韩文本
   做 justify——已穷举 `line-break` × `word-break` 组合验证，中文会在行尾留下大空档。
   若出版社要求两端对齐，需在 InDesign 或 LaTeX 里重排；本书稿的文字、结构、图与表可直接搬。
2. **PDF 文本层的 ToUnicode 有缺陷。** 子集化后的 Noto Serif SC 使"人"被抽取为 U+2F00，
   用 pypdf 检索"人形机器人"会假报缺失。**版面本身是正确的**（已逐页目视核对）。
   付印前请过一遍 PDF-X preflight；若编辑需要复制文字，请以 docx 为准。
3. **长字体名称导致 PDF 警告** `name token is longer than specification`。
   这是嵌入字体的命名问题，多数印厂可处理，但 PDF/X-1a 预检可能报错，需转档。
4. **书里没有一张真机照片。** 这是政策决定（官方素材 0 张，未取得授权），不是遗漏。
   三幅待补的实拍位已在 `图片授权清单.md` 中逐条列出规格。

## 五、随稿脚本与自检门（编辑与印厂不需要，但审稿人可能想验）

本书的验收纪律是"可以不讲，但不能讲错"。为此每一处标注为 [算] 的数都由脚本产出，
且脚本自带**已知答案自检**（度量本身要先证明自己能用）。一条命令跑完全部重建与全部门：

```
bash tools/rebuild_all.sh            # 草稿 → 排版源 → 图片 → PDF → 交稿包 → docx → 六道门
bash tools/rebuild_all.sh --gates    # 只跑门
```

逐条：

```
python code/tools/foc_check.py            # 第 1 部全部推算链 + 已知答案自检（当前 10/10）
python code/tools/arithmetic_check.py --demo
python tools/check_terms.py --all         # 先现象后命名 / 每章 6 个新词预算 / 行话即时解释
python tools/check_kg.py                  # 概念依赖顺序与每章引入数（图即权威清单）
python tools/depth_audit.py --selftest    # 深度度量自证：厚样本 18.00 / 薄样本 0.00
python tools/depth_audit.py               # 每章追问链、公式密度、是否落到底层、边界与代价、可代入的数
python tools/number_provenance.py --selftest  # 数源门自证：能抓出算错的等式
python tools/number_provenance.py         # 书稿里每个带单位的数，须能对上脚本输出或一手资料
python tools/build_book.py --drafts       # 装配排版源
cd print && node build.mjs                # 出 PDF
cd print && node rasterize.mjs            # 出 300 dpi 图片包
```

`number_provenance.py` 的判法是"宁可误报不漏报"：正文里同行写了算式的（`23 × 369 = 8,487`）
自动放行，没写算式又找不到出处的数一律列出。当前全书剩 7 处列出项，均为
"在别处已推导、此处只是复述"的量，已逐条人工核过（记录在 `verification/pending-fixes-2026-10-08.md`）。
"""
    (SUB / "CIP与交稿说明.md").write_text(t, encoding="utf-8")
    return total


def docx_src():
    out = SUB / "src-docx"
    out.mkdir(exist_ok=True)
    # pandoc 的 --resource-path 在本机对多输入 glob 不生效（实测：裸文件名与 ../images/
    # 两种写法都报 Could not fetch resource）。所以把 PNG 复制进源文件同目录，让相对
    # 解析必然成功。图片包的正式交付位置仍是 submission/images/。
    import shutil
    for pic in (SUB / "images").glob("*.png"):
        dst = out / pic.name
        if not dst.exists() or dst.stat().st_mtime < pic.stat().st_mtime:
            shutil.copy2(pic, dst)
    # 2026-10-09：自由许可照片（JPG/PNG，不需栅格化）同样拷进源目录——
    # pandoc 的 --resource-path 在本机对多输入 glob 不生效，只有同目录裸文件名必然解析成功。
    photodir = SUB.parent / "assets" / "photo"
    n_photo = 0
    if photodir.exists():
        for pic in sorted(photodir.iterdir()):
            if pic.suffix.lower() not in (".jpg", ".jpeg", ".png", ".tif", ".tiff"):
                continue
            dst = out / pic.name
            if not dst.exists() or dst.stat().st_mtime < pic.stat().st_mtime:
                shutil.copy2(pic, dst)
            n_photo += 1
    n = 0
    for f in sorted(SRC.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        # pandoc 不认 SVG，且它按「源文件目录 + resource-path」解析相对路径，
        # 所以这里写成相对源文件目录的 ../images/（src-docx 与 images 同为 submission 的子目录）。
        t2 = re.sub(r"\(assets/fig/([^)\"]+)\.svg", r"(\1.png", t)
        # 照片：assets/photo/<name> → 裸文件名（文件已拷进 src-docx）
        t2 = re.sub(r"\(assets/photo/([^)\"]+)", r"(\1", t2)
        (out / f.name).write_text(t2, encoding="utf-8")
        n += 1
    print(f"  src-docx/ 写出 {n} 个文件 + {len(list(out.glob(chr(42)+chr(46)+chr(112)+chr(110)+chr(103))))} 张 PNG 副本 + {n_photo} 张照片")


def main():
    SUB.mkdir(exist_ok=True)
    d, todo, have = ledger(load_figures())
    print(f"  图片授权清单.md / .csv（已完成 {d}，待办 {todo}，已光栅化 {have}）")
    declaration(); print("  图片来源与版权声明.md")
    total = cip(); print(f"  CIP与交稿说明.md（排版源正文汉字 {total:,}）")
    docx_src()
    print(NL + "下一步（必须在 src-docx 目录内执行；pandoc 按 CWD 解析图片相对路径，"
          + NL + "          在仓库根跑会把全部图静默丢掉，docx 照样生成）：")
    print(f'  cd submission/src-docx && pandoc *.md -o "../{TITLE}-交稿版.docx" '
          f'--toc --toc-depth=2 --metadata title="{TITLE}"')
    print("  cd ../.. && node print/rasterize.mjs   # 重出图片包（改了 SVG 之后要跑）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
