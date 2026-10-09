#!/usr/bin/env python3
"""把 pandoc 产出的 docx 调到与印型 PDF 同一套页面参数。

为什么需要这一步：pandoc 默认不写 <w:pgSz>/<w:pgMar>，Word 会按本机默认纸
（A4/Letter）排版，而本书的印型是 145 × 210 mm、版心 110 × 176 mm。交稿方
打开 Word 看到的分页与页边距如果和 PDF 不是一套，"照着 Word 改再回 PDF"
就会两边漂。这里只做**能在 Word 里等价表达**的三件事：页面尺寸、页边距、
中日韩字体族。排版引擎不同（Word 的换行 vs Paged.js），完全逐字同页不可
能，本工具不假装能做到——它保证的是"同一张纸、同一块版心、同一支字"。

自检：--verify 打印改后的 sectPr 与字体，不改文件。
"""
import io
import re
import sys
import zipfile
import shutil
import os

MM = 1440 / 25.4          # twips per mm
PAGE_W = round(145 * MM)  # 8220
PAGE_H = round(210 * MM)  # 11906
SIDE = round(17.5 * MM)   # (145 - 110) / 2
TOPBOT = round(17 * MM)   # (210 - 176) / 2
HEADFOOT = round(12 * MM)
CJK_FONT = "宋体"
LATIN_FONT = "Times New Roman"

DOCX = os.path.join("submission", "人形机器人：从一颗关节往下挖-交稿版.docx")


def sect_patch(xml):
    add = ('<w:pgSz w:w="%d" w:h="%d" w:orient="portrait"/>'
           '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
           'w:header="%d" w:footer="%d" w:gutter="0"/>'
           % (PAGE_W, PAGE_H, TOPBOT, SIDE, TOPBOT, SIDE, HEADFOOT, HEADFOOT))
    m = re.search(r"<w:sectPr\b[^>]*>", xml)
    if not m:
        raise SystemExit("document.xml 里没有 sectPr，无法设置页面尺寸")
    # 已有的先删，避免两套并存（pandoc 偶尔会留 pgSz）
    body = re.sub(r"<w:pgSz\b[^>]*/>|<w:pgMar\b[^>]*/>", "", xml[m.end():])
    return xml[:m.end()] + add + body, "sectPr"


def font_patch(xml):
    fonts = ('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
             % (LATIN_FONT, LATIN_FONT, CJK_FONT, CJK_FONT))
    if "<w:docDefaults>" in xml:
        # docDefaults 里已有 rPrDefault 就用它，没有就补一个
        if "<w:rPrDefault>" in xml:
            xml2 = re.sub(r"<w:rPrDefault>(\s*)<w:rPr>", r"<w:rPrDefault>\1<w:rPr>" + fonts,
                          xml, count=1)
            if xml2 == xml:      # rPrDefault 存在但没有 rPr
                xml2 = xml.replace("<w:rPrDefault>", "<w:rPrDefault><w:rPr>" + fonts + "</w:rPr>", 1)
            return re.sub(r"<w:rPr>((?:(?!</w:rPr>)[\s\S])*?)<w:rFonts[^>]*/>",
                          r"<w:rPr>\1" + fonts, xml2), "docDefaults"
        xml2 = xml.replace("<w:docDefaults>", "<w:docDefaults><w:rPrDefault><w:rPr>" + fonts + "</w:rPr></w:rPrDefault>", 1)
        return xml2, "docDefaults(new)"
    raise SystemExit("styles.xml 没有 docDefaults")


def main():
    verify = "--verify" in sys.argv
    src = DOCX
    if not os.path.exists(src):
        raise SystemExit("找不到 " + src)
    z = zipfile.ZipFile(src)
    names = z.namelist()
    doc = z.read("word/document.xml").decode("utf-8")
    sty = z.read("word/styles.xml").decode("utf-8")
    z.close()                       # Windows 上没关的句柄会锁住文件，os.replace 直接 Access denied
    doc, a = sect_patch(doc)
    sty, b = font_patch(sty)
    print("patched:", a, "+", b,
          "| page %d x %d twips = %.0f x %.0f mm" % (PAGE_W, PAGE_H, PAGE_W / MM, PAGE_H / MM),
          "| margins L/R %.1f mm  T/B %.0f mm" % (SIDE / MM, TOPBOT / MM),
          "| eastAsia=%s ascii=%s" % (CJK_FONT, LATIN_FONT))
    if verify:
        print("sectPr head:", re.search(r"<w:sectPr[\s\S]{0,220}", doc).group(0)[:220])
        return
    tmp = src + ".tmp"
    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            data = zin.read(n)
            if n == "word/document.xml":
                data = doc.encode("utf-8")
            elif n == "word/styles.xml":
                data = sty.encode("utf-8")
            zout.writestr(n, data)
    zin.close()
    try:
        os.replace(tmp, src)
    except PermissionError:          # 目标被占用/被杀软锁住时，先删再改名
        os.remove(src); os.rename(tmp, src)
    # 复验：重新打开，确认页面参数真的在文件里
    x = zipfile.ZipFile(src).read("word/document.xml").decode("utf-8")
    assert '<w:pgSz' in x and '<w:pgMar' in x, "写回后 sectPr 里没有 pgSz/pgMar"
    s = zipfile.ZipFile(src).read("word/styles.xml").decode("utf-8")
    assert 'w:eastAsia="%s"' % CJK_FONT in s, "写回后 styles.xml 没有中文字体"
    n_media = len([q for q in zipfile.ZipFile(src).namelist() if q.startswith("word/media/")])
    print("写回复验通过：pgSz/pgMar 在 document.xml，中文字体在 styles.xml，内嵌图 %d 张" % n_media)
    # 顺手把 docx 里漏出的代码围栏数出来——那是真格式错误
    t = re.sub(r"<[^>]+>", "", x)
    if "```" in t:
        print("!! docx 正文里漏出 ``` 围栏 %d 处，这是格式错误，必须修源文件" % t.count("```"))
        raise SystemExit(1)
    print("docx 正文无漏出的 ``` 围栏")


main()
