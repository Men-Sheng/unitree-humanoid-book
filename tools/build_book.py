#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/build_book.py — 把 drafts/ 里的章稿装配成可付印的书稿（print/src/）。

为什么要有这个脚本：`final/*.md` 是唯一真源，PDF 只是它的一个投影。
本脚本负责"投影"这件事——封面、版权页、目录、章号、图号、语录块——
**它不新增任何事实**，只做排版装配。所以它可以反复跑，跑完的 print/src/ 是一次性产物。

用法：
    python tools/build_book.py              # 装配 + 报告缺什么
    python tools/build_book.py --drafts     # 连未定稿的 drafts 一起排（看版式用）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
NL = chr(10)
SRC = ROOT / "print" / "src"

# 章标题里的"第 05 章　"前缀要剥掉——章号由版式统一生成，不能靠作者手打
PREFIX = re.compile(r"^第\s*\d+\s*章[\s　]+")
APPENDIX_PREFIX = re.compile(r"^附录\s*([A-Z])[\s　：:]+")
STATUS_BLOCK = re.compile(r"^#\s+.*\n+^>\s*状态：.*?(?:\n>\s*.*?)*\n(?=\n)", re.M | re.S)


def load_units():
    units = yaml.safe_load((ROOT / "outline" / "units.yaml").read_text(encoding="utf-8"))["units"]
    return units


def safe_name(t: str) -> str:
    """文件名清洗：Windows 不允许反斜杠、冒号、星号、问号、尖括号、竖线；中文冒号换成连字符。"""
    import re as _re
    bad = _re.escape(chr(92) + "/:*?" + chr(34) + "<>|") + chr(9) + chr(13)
    t = _re.sub("[" + bad + "]", "", t)
    return t[:14].replace(" ", "").replace(chr(65306), "-")


def load_quotes():
    """每章的语录块。文件不存在时返回空表——**宁缺不假**。"""
    f = ROOT / "bible" / "quotes.yaml"
    if not f.exists():
        return {}
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    return {str(k): v for k, v in (data.get("quotes") or {}).items()}


def load_figures():
    f = ROOT / "outline" / "figures.yaml"
    if not f.exists():
        return {}
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    out = {}
    for item in data.get("figures") or []:
        out.setdefault(str(item.get("unit", "")), []).append(item)
    return out


def clean_body(md: Path) -> str:
    """剥掉作者状态块与 H1（H1 由版式重建），返回正文。"""
    text = md.read_text(encoding="utf-8")
    lines = text.split("\n")
    i = 0
    if i < len(lines) and lines[i].startswith("#"):
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    # H1 之后紧接的连续 > 引用行，默认是"作者状态块"（"状态：初稿 v1…"），成书里不印。
    # 但 2026-10-09 直接量成品 PDF 才发现：附录 A/C/D/E 的开头引用块写的是**给读者看的口径声明**
    # （"凡正文与本表不一致以本表为准""空白格表示官方未公布"），也被这条规则一起丢掉了。
    # 所以现在只剥以"状态："开头的引用块，其余原样交给版式印成"小节说明"。
    first = lines[i].lstrip(">").strip() if i < len(lines) else ""
    if first.startswith("状态："):
        while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
            i += 1
    body = "\n".join(lines[i:]).strip()
    body = re.sub(r"\n---\n\s*$", "", body)
    return body


def quote_block(unit_id: str, quotes: dict) -> str:
    q = quotes.get(unit_id)
    if not q:
        return ""
    def g(k):
        v = q.get(k, "")
        return str(v).strip() if v is not None else ""
    text, src, date, kind = g("text"), g("source"), g("date"), g("kind")
    lines = ["> [!QUOTE]", ">"]
    for para in text.split("\n\n"):
        lines.append(f"> {para.strip()}")
        lines.append(">")
    tail = " — ".join(x for x in (g("speaker") or "王兴兴", src, date) if x)
    if kind:
        tail += f"（{kind}）"
    lines.append(f"> {tail}")
    return "\n".join(lines) + "\n\n"


def figure_block(unit_id: str, figures: dict, avail: set) -> str:
    out = []
    for f in figures.get(unit_id, []):
        path, cap = f.get("path", ""), f.get("caption", "")
        if not path:
            continue
        if path not in avail:
            out.append(f"<!-- 缺图：{path}｜{cap}｜责任：{f.get('owner','?')}｜许可：{f.get('license','?')} -->\n\n")
            continue
        out.append(f"![{cap}]({path} \"{cap}\")\n\n")
    return "".join(out)


def split_first_paragraph(body: str) -> tuple[str, str]:
    m = re.search(r"\n##\s", body)
    if not m:
        return body, ""
    return body[: m.start()], body[m.start():]


def cover_and_front(units) -> list[Path]:
    files = []
    n_ch = sum(1 for u in units if not u["unit"] >= "40")
    words = sum(u["target_words"] for u in units)
    cover = f"""<div class="cover">

<div class="cover-kicker">工程 · 技术栈解剖</div>

<div class="cover-title">人形机器人：从一颗关节往下挖</div>

<div class="cover-sub">从磁场、电流到一次思考：一台人形机器人的六层解剖</div>

<div class="cover-meta">

〔作者名〕　著

排版稿 · 未定稿 · 2026-10　|　全书 {len(units)} 章 · 约 {words/10000:.1f} 万字

</div>
</div>
"""
    files.append(("000-cover.md", cover))

    colophon = f"""<div class="frontmatter">


<div class="cip">

**图书在版编目（CIP）数据**

人形机器人：从一颗关节往下挖：从磁场、电流到一次思考 / 〔作者〕著．— 〔城市〕：〔出版社〕，〔2026.X〕

ISBN 〔978-7-XXX-XXXXX-X〕

Ⅰ．①机…　Ⅱ．①〔作者〕　Ⅲ．①机器人—普及读物　Ⅳ．①TP24-49

〔出版社版本图书馆数据核字（2026）第 XXXXXX 号〕

</div>

**〔出版社〕出版发行**
地址：〔　〕　邮编：〔　〕
经销：新华书店　印刷：〔　〕
开本：787 mm × 1092 mm　1/32（成品 145 mm × 210 mm）
印张：〔　〕　字数：{words/1000:.0f} 千字　版次：2026 年〔　〕月第 1 版
印次：〔　〕　定价：〔　〕元

**本书排版与字体**
正文：思源宋体（Noto Serif SC）；标题与表格：思源黑体（Noto Sans SC）。
二者均为 SIL Open Font License 1.1，允许商用出版与嵌入，无需另行购买授权。

**关于本书与宇树科技的关系**
本书为独立作者撰写的技术解剖类读物，**与杭州宇树科技有限公司无关，未获得其授权、审阅或背书**；书中全部参数以厂商截至 2026-10-07 公开页面与公开仓库为准，不构成采购或投资依据。
Unitree、宇树及其产品型号为各自所有者的商标。书中涉及厂商公布的数据均标注抓取日期；
厂商未公布的数据一律写明"未公布"，不以推测填充。

**关于图片**
本书图片分三类，逐张在图注与附录中标明来源与许可：① 作者实拍；② 本书自绘示意图；
③ 经许可或依合理引用原则使用的第三方图片。任何未获授权的图片不会进入成书版。

</div>
"""
    files.append(("010-colophon.md", colophon))

    files.append(("020-toc.md", """<div class="toc-page">

## Contents

<nav id="toc"></nav>

</div>
"""))
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", action="store_true", help="用 drafts/ 里的稿子（未定稿）排版")
    a = ap.parse_args()
    srcdir = ROOT / ("drafts" if a.drafts else "final")
    SRC.mkdir(parents=True, exist_ok=True)
    for old in SRC.glob("*.md"):
        old.unlink()

    units = load_units()
    quotes = load_quotes()
    figs = load_figures()
    assets = {str(p.relative_to(ROOT)).replace(chr(92), "/")
              for p in (ROOT / "assets").rglob("*")}
    assets = assets if (ROOT / "assets").exists() else set()   # Windows 反斜杠归一化：台账用正斜杠

    made, missing, no_quote = [], [], []

    for name, text in cover_and_front(units):
        (SRC / name).write_text(text, encoding="utf-8")
        made.append(name)

    # 附录：语录出处一览（正文只留短署名，完整标题与 URL 集中在这里，便于出版社核校）
    if quotes:
        rows = ["# 附录：语录出处一览 {.appendix}", "",
                "正文各章的语录块只写「媒体 · 日期」，完整出处集中于此，便于核校。", "",
                "| 章 | 说话人 | 完整出处 | 日期 | 类型 | 链接 |", "|---|---|---|---|---|---|"]
        for uid in sorted(quotes):
            qq = quotes[uid]
            rows.append("| 第 {} 章 | {} | {} | {} | {} | {} |".format(
                uid, str(qq.get("speaker") or "王兴兴"),
                str(qq.get("source", "")).replace("|", "/"), str(qq.get("date", "")),
                str(qq.get("kind", "")), str(qq.get("url", ""))))
        (SRC / "900-quotes-sources.md").write_text(NL.join(rows) + NL, encoding="utf-8")
        made.append("900-quotes-sources.md")

    for u in units:
        uid = u["unit"]
        cand = list((srcdir / f"unit-{uid}").glob("*.md")) if (srcdir / f"unit-{uid}").exists() else []
        if not cand:
            missing.append(uid)
            continue
        body = clean_body(cand[0])
        title = u["title"]
        m = APPENDIX_PREFIX.match(title)
        if m:
            title = APPENDIX_PREFIX.sub("", title)
        else:
            title = PREFIX.sub("", title)
        head = f"# {title}" + (" {.appendix}" if m else "")
        if uid == "00":
            head = f"# {title} {{.unnumbered}}"

        first, rest = split_first_paragraph(body)
        qb = quote_block(uid, quotes)
        if not qb:
            no_quote.append(uid)
        fg = figure_block(uid, figs, assets)
        text = head + "\n\n" + first.strip() + "\n\n" + (qb if qb else "") + (fg if qb or fg else "") + rest.strip() + "\n"
        out = SRC / f"{100+int(uid):03d}-{safe_name(title)}.md"
        out.write_text(text, encoding="utf-8")
        made.append(out.name)

    print(f"装配 {len(made)} 个文件 → print/src/")
    print(f"缺稿 {len(missing)} 章：{', '.join(missing) if missing else '无'}")
    print(f"语录块空缺 {len(no_quote)} 章（bible/quotes.yaml 不存在或该章无可溯源语录 → 宁缺不假）")
    allf = load_figures()
    todo = [f for lst in allf.values() for f in lst if str(f.get('status')) != '已完成']
    nolic = [f for lst in allf.values() for f in lst if not f.get('license')]
    print(f"图：台账 {sum(len(v) for v in allf.values())} 幅，其中待拍/待绘/待授权 {len(todo)} 幅，缺 license 字段 {len(nolic)} 幅（assets/ 现有 {len(assets)} 个文件）")
    print("      → 图片是这本书的硬成本：逐幅任务单见 outline/figures.yaml，政策见 bible/images.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
