#!/usr/bin/env python3
"""tools/pdf_qa.py — 印前 QA：直接量**成品 PDF**，不量浏览器里的预览 DOM。

为什么换口径（2026-10-08 的教训）：print/proof.mjs 量的是 Paged.js preview() 出来的
DOM。它的 .pagedjs_page_content 在 preview 路径下会给长行 <pre>/<table> 报出 1964 px
的固有宽度（版心只有 416 px），14 处"溢出"全部是同一个 +1548 px 偏移 —— 那是预览布局
的产物，不是印到纸上的东西。成品 PDF 才是交稿物，所以这里用 PyMuPDF 直接读 PDF 的
坐标：墨到哪儿、有没有越过裁口、有没有冲进页边距，一量就知道。

口径（来自 print/style.css）：
  页面 145 × 210 mm（大 32 开）；版心 110 × 176 mm
  单数页（recto/右页）margin: 上17 右15 下17 左20 mm
  双数页（verso/左页）margin: 上17 右20 下17 左15 mm
  封面 margin 0

三类判定，严重度不同：
  PAST_TRIM     墨越过裁口（<1pt 容差）——真缺陷，印出来会被裁掉，必须修
  IN_MARGIN_X   水平方向冲出留白（页边空白），>4pt 才算 ——排版缺陷，必须修
  SIZE_MISMATCH 页面尺寸不等于 145×210 ——必须修
  NEAR_EMPTY    整页正文 <40 字 ——章末留空是设计，列出来让人确认，不判失败
  VERTICAL      版心外的纵向内容：页眉页脚本来就在出血区，只统计不判失败

--selftest 里塞了故意的错答案（越界的文字 + 空页），证明这个量尺真的能抓到东西。
用法：python -X utf8 tools/pdf_qa.py [--selftest] [pdf 路径]
"""
from __future__ import annotations

import sys

import fitz  # PyMuPDF

MM = 25.4  # pt per inch / mm per inch -> 1 mm = 72/25.4 pt
PT_PER_MM = 72.0 / MM

PAGE_W_MM, PAGE_H_MM = 145.0, 210.0
TOP_BM, BOT_BM = 17.0, 17.0          # 上下页边距（左右页相同）
TRIM_TOL = 1.0                        # pt，越过裁口的容差
MARGIN_TOL = 4.0                      # pt，冲出留白的容忍（表格边框取整之类）
HARD_MARGIN = 8.0                     # pt，超过它才算硬缺陷：留白有 15–20 mm，
                                      # ≤8 pt（2.8 mm）是 CJK 行末取整级差异，不越裁口也不压字，
                                      # 只有 URL/长路径那种 15–21 pt 的才是真毛病
COVER_PAGE = 1


def content_box(pno: int, n_pages: int) -> tuple[float, float, float, float]:
    """返回该页版心的 (x0, y0, x1, y1)，单位 pt。pno 从 1 开始。"""
    if pno == COVER_PAGE:
        return 0.0, 0.0, PAGE_W_MM * PT_PER_MM, PAGE_H_MM * PT_PER_MM
    inner = pno % 2 == 1              # 单数页是右页（recto），订口在左
    left = (20.0 if inner else 15.0) * PT_PER_MM
    right = (PAGE_W_MM - (15.0 if inner else 20.0)) * PT_PER_MM
    top = TOP_BM * PT_PER_MM
    bottom = (PAGE_H_MM - BOT_BM) * PT_PER_MM
    return left, top, right, bottom


def page_bboxes(pg) -> list[tuple[str, float, float, float, float, str]]:
    """页面上所有"有墨"的东西：文字、图片、矢量图形。"""
    out: list[tuple[str, float, float, float, float, str]] = []
    for w in pg.get_text("words"):     # (x0,y0,x1,y1,word,block,line,word_no)
        out.append(("TEXT", w[0], w[1], w[2], w[3], str(w[4])[:48]))
    for im in pg.get_image_info():
        b = im["bbox"]
        out.append(("IMG", b[0], b[1], b[2], b[3], f"image {im.get('width')}x{im.get('height')}"))
    for d in pg.get_drawings():
        r = d["rect"]
        # 整页背景矩形（画到裁口的底色/框）不是缺陷，忽略
        if r.width >= pg.rect.width - 2 and r.height >= pg.rect.height - 2:
            continue
        if r.width < 0.5 or r.height < 0.5:
            continue
        out.append(("DRAW", r.x0, r.y0, r.x1, r.y1, d.get("type", "draw")))
    return out


def audit(pdf_path: str, verbose_limit: int = 30) -> dict:
    doc = fitz.open(pdf_path)
    res = {
        "pdf": pdf_path, "pages": doc.page_count,
        "past_trim": [], "in_margin_x": [], "margin_soft": [], "size_mismatch": [],
        "near_empty": [], "vertical_only": [], "figure_missing": [],
    }
    expected = (PAGE_W_MM * PT_PER_MM, PAGE_H_MM * PT_PER_MM)
    for i, pg in enumerate(doc):
        pno = i + 1
        if abs(pg.rect.width - expected[0]) > 0.6 or abs(pg.rect.height - expected[1]) > 0.6:
            res["size_mismatch"].append(
                {"page": pno, "w": round(pg.rect.width, 2), "h": round(pg.rect.height, 2)})
        cx0, cy0, cx1, cy1 = content_box(pno, doc.page_count)
        for kind, x0, y0, x1, y1, label in page_bboxes(pg):
            rec = {"page": pno, "kind": kind, "label": label,
                   "x0": round(x0, 1), "x1": round(x1, 1),
                   "y0": round(y0, 1), "y1": round(y1, 1), "side": ""}
            sides = []
            if x1 > pg.rect.width - TRIM_TOL: sides.append(("右越裁口", x1 - pg.rect.width))
            if x0 < TRIM_TOL:                 sides.append(("左越裁口", TRIM_TOL - x0))
            if y1 > pg.rect.height - TRIM_TOL: sides.append(("下越裁口", y1 - pg.rect.height))
            if y0 < TRIM_TOL:                 sides.append(("上越裁口", TRIM_TOL - y0))
            if sides:
                worst = max(sides, key=lambda t: t[1])
                rec["side"], rec["over"] = worst[0], round(worst[1], 1)
                res["past_trim"].append(rec)
            elif x1 > cx1 + MARGIN_TOL or x0 < cx0 - MARGIN_TOL:
                right_over, left_over = x1 - cx1, cx0 - x0
                rec["side"] = "右冲出留白" if right_over > left_over else "左冲出留白"
                rec["over"] = round(max(right_over, left_over), 1)
                res["in_margin_x" if rec["over"] > HARD_MARGIN else "margin_soft"].append(rec)
            elif y1 > cy1 + MARGIN_TOL or y0 < cy0 - MARGIN_TOL:
                rec["side"] = "下" if y1 - cy1 > cy0 - y0 else "上"
                res["vertical_only"].append(rec)
        txt = pg.get_text().strip()
        import re as _re
        for fig_id in sorted(set(_re.findall(r"图 (\d\d-\d)", txt))):
            # 图正常渲染时这一串只出现在 figcaption 里一次；图片加载失败时 Chrome 会把
            # <img alt> 一起印出来 → 同一页两次。2026-10-08 就是靠这条抓到 12 张图消失。
            if txt.count(f"图 {fig_id}") >= 2:
                res["figure_missing"].append({"page": pno, "label": f"图 {fig_id}",
                                              "chars": len(txt)})
        if len(txt) < 40 and pno != COVER_PAGE and pno != doc.page_count:
            res["near_empty"].append({"page": pno, "chars": len(txt), "head": txt[:34]})
    doc.close()

    print(f"PDF {res['pages']} 页 ｜ 版心口径 145×210 mm，版心 110×176 mm")
    print(f"页面尺寸不符      {len(res['size_mismatch'])} 处")
    print(f"墨越过裁口        {len(res['past_trim'])} 处  ← 真缺陷，印出来缺字")
    print(f"水平冲出留白(硬)  {len(res['in_margin_x'])} 处 >{HARD_MARGIN:.0f} pt ← 排版缺陷，必须修")
    print(f"水平冲出留白(软)  {len(res['margin_soft'])} 处 ≤{HARD_MARGIN:.0f} pt ← 落在 15–20 mm 留白内，不越裁口")
    print(f"纵向出血区有内容  {len(res['vertical_only'])} 处（页眉/页脚/页码，设计如此）")
    print(f"图没渲染出来      {len(res['figure_missing'])} 处  ← 只剩 alt 文本，必须修")
    print(f"疑似空页 <40 字   {len(res['near_empty'])} 处  ← 需人确认是不是章末留空")
    for r in res["figure_missing"][:14]:
        print(f"  [缺图] 页 {r['page']} {r['label']} 的 alt 文本被印出来了")
    for r in res["size_mismatch"][:verbose_limit]:
        print(f"  [尺寸] 页 {r['page']} 实测 {r['w']}×{r['h']} pt，应为 "
              f"{round(PAGE_W_MM*PT_PER_MM,2)}×{round(PAGE_H_MM*PT_PER_MM,2)} pt")
    for key, title in (("past_trim", "越裁口"), ("in_margin_x", "冲出留白"),
                       ("margin_soft", "留白内软项")):
        rows = res[key]
        for r in rows[:verbose_limit if key != "margin_soft" else 8]:
            print(f"  [{title}] 页 {r['page']} {r['kind']} {r['side']} "
                  f"x {r['x0']}→{r['x1']} y {r['y0']}→{r['y1']} 越界 {r['over']} pt ｜ {r['label']}")
        if len(rows) > verbose_limit:
            print(f"  [{title}] …另有 {len(rows) - verbose_limit} 处")
    for r in res["near_empty"][:12]:
        print(f"  [空页] 页 {r['page']} ｜ {r['chars']} 字 ｜ {r['head']}")
    hard = (len(res["past_trim"]) + len(res["in_margin_x"]) + len(res["size_mismatch"])
            + len(res["figure_missing"]))
    print(f"硬缺陷合计 {hard} 处")
    for key in ("past_trim", "in_margin_x"):
        kinds: dict[str, int] = {}
        for r in res[key]:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
        if kinds:
            print(f"  {key} 构成：" + " ".join(f"{k}×{v}" for k, v in sorted(kinds.items())))
    return res


def selftest() -> int:
    """故意的错答案必须被抓到，干净页必须不被抓到。"""
    import os
    import tempfile

    path = os.path.join(tempfile.gettempdir(), "pdf_qa_selftest.pdf")
    doc = fitz.open()
    w, h = PAGE_W_MM * PT_PER_MM, PAGE_H_MM * PT_PER_MM
    n = 5

    doc.new_page(width=w, height=h)                    # 1 = 封面占位（gate 对封面放行）

    p = doc.new_page(width=w, height=h)                # 2 = 干净页（双数页）
    cx0, cy0, cx1, cy1 = content_box(2, n)
    p.insert_text((cx0 + 2, 200), "clean sentence inside the content box, long enough", fontsize=9)
    p.insert_text((cx0 + 2, 220), "second line still inside", fontsize=9)
    p.draw_line(fitz.Point(cx0, 300), fitz.Point(cx1 - 1, 300), width=0.6)

    p = doc.new_page(width=w, height=h)                # 3 = 越裁口的长行
    cx0, cy0, cx1, cy1 = content_box(3, n)
    # 先放一行足够长的正常文字，让这一页不被判成空页（保证两类判定互不串台）
    p.insert_text((cx0 + 2, 120), "a normal line long enough to keep this page non-empty", fontsize=9)
    p.insert_text((cx1 - 20, 220), "X" * 90, fontsize=9)

    p = doc.new_page(width=w, height=h)                # 4 = 空页
    cx0, cy0, cx1, cy1 = content_box(4, n)
    p.insert_text((cx0 + 2, 200), "x", fontsize=9)

    p = doc.new_page(width=w + 12, height=h)           # 5 = 尺寸不符
    p.insert_text((60, 200), "size", fontsize=9)
    doc.save(path)
    doc.close()

    sys.stdout.write("── selftest（故意错答案）\n")
    res = audit(path, verbose_limit=5)
    trimmed = {r["page"] for r in res["past_trim"]}
    margined = {r["page"] for r in res["in_margin_x"]}
    empty = {r["page"] for r in res["near_empty"]}
    sized = {r["page"] for r in res["size_mismatch"]}
    ok = [
        ("抓到越裁口（页 3）", trimmed == {3}),
        ("抓到尺寸不符（页 5）", sized == {5}),
        ("抓到空页（页 4）", empty == {4}),
        ("干净页 2 零误报", 2 not in trimmed and 2 not in margined and 2 not in empty),
        ("封面页 1 不参与空页判定", 1 not in empty),
    ]
    bad = 0
    for name, good in ok:
        print(("PASS " if good else "FAIL ") + name)
        if not good:
            bad += 1
    print(f"实测：越裁口页 {sorted(trimmed)} ｜ 冲出留白页 {sorted(margined)} ｜ "
          f"空页 {sorted(empty)} ｜ 尺寸 {sorted(sized)}")
    os.remove(path)
    return 0 if bad == 0 else 1


def probe(pdf_path: str, pno: int) -> None:
    """把一页的几何 dump 出来：谁画在什么坐标。判定器只说“越界了”，
    要修东西得先知道越界的是谁。"""
    doc = fitz.open(pdf_path)
    pg = doc[pno - 1]
    cx0, cy0, cx1, cy1 = content_box(pno, doc.page_count)
    print(f"页 {pno} ｜ 页面 {pg.rect.width:.1f}×{pg.rect.height:.1f} pt ｜ "
          f"版心 x {cx0:.1f}→{cx1:.1f} y {cy0:.1f}→{cy1:.1f}")
    print("── 矢量图形（按面积从大到小）")
    ds = []
    for d in pg.get_drawings():
        r = d["rect"]
        ds.append((abs(r.width * r.height), d))
    ds.sort(key=lambda t: -t[0])
    for area, d in ds[:18]:
        r = d["rect"]
        print(f"  {d.get('type','?')} x {r.x0:7.1f}→{r.x1:7.1f} y {r.y0:6.1f}→{r.y1:6.1f} "
              f"fill={d.get('fill')} stroke={d.get('color')} items={len(d.get('items', []))}")
    print("── 最右的 8 个文字块")
    ws = sorted(pg.get_text("words"), key=lambda w: -w[2])[:8]
    for w in ws:
        print(f"  x {w[0]:7.1f}→{w[2]:7.1f} y {w[1]:6.1f} ｜ {str(w[4])[:60]}")
    print("── 图片")
    for im in pg.get_image_info():
        b = im["bbox"]
        print(f"  x {b[0]:7.1f}→{b[2]:7.1f} y {b[1]:6.1f}→{b[3]:6.1f} ｜ {im.get('width')}x{im.get('height')}")
    print("── 该页文本（前 300 字）")
    print(pg.get_text()[:300].replace("\n", " ⏎ "))
    doc.close()


def shots(pdf_path: str, res: dict, out_dir: str, dpi: int = 170, limit: int = 14) -> None:
    """把判定为缺陷的页从**成品 PDF** 渲染成 PNG —— 人眼核对要有真东西可看，
    不是浏览器预览。"""
    import os

    os.makedirs(out_dir, exist_ok=True)
    pages = sorted({r["page"] for r in res["past_trim"] + res["in_margin_x"]})[:limit]
    doc = fitz.open(pdf_path)
    for pno in pages:
        pix = doc[pno - 1].get_pixmap(dpi=dpi)
        out = os.path.join(out_dir, f"p{pno:03d}-defect.png")
        pix.save(out)
    doc.close()
    print(f"已渲染 {len(pages)} 页到 {out_dir}：{', '.join(str(x) for x in pages)}")


def main() -> int:
    args = [a for a in sys.argv[1:]]
    default_pdf = "print/人形机器人：从一颗关节往下挖.pdf"
    if "--selftest" in args:
        return selftest()
    if "--probe" in args:
        i = args.index("--probe")
        pno = int(args[i + 1])
        rest = args[:i] + args[i + 2:]
        pdf = rest[0] if rest else default_pdf
        probe(pdf, pno)
        return 0
    pdf = next((a for a in args if not a.startswith("--")), default_pdf)
    res = audit(pdf)
    if "--shots" in args:
        shots(pdf, res, "print/proof-pdf")
    hard = (len(res["past_trim"]) + len(res["in_margin_x"]) + len(res["size_mismatch"])
            + len(res["figure_missing"]))
    return 0 if hard == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
