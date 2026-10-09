#!/usr/bin/env python3
"""tools/svg_check.py — 图形文字有没有冲出画布，以及给每张图加裁剪兜底。

为什么要有它（2026-10-08 成品 PDF 实测）：
  Chrome 把 `<img src=x.svg>` 打进 PDF 时，**不会**按 viewBox 裁掉超出的内容
  （浏览器里预览会裁，所以 print/proof.mjs 截图看不出来）。结果 f30-vla.svg 第 46 行
  那句 55 个汉字的说明画到了 viewBox 外，成品里有一行字伸进右边留白 4.6 pt。
  也就是说：图里的文字只要比 viewBox 宽，就会在纸上冲出页边 —— 必须量，而且要靠
  成品 PDF 量，不能靠预览。

两件事：
  1. 检查：估算每个 <text> 的左右边界（汉字按 1 个字宽、ASCII 按 0.55，与
     tools/make_figs3.py 的 wlen 同一口径），报出冲出 viewBox 的行。
  2. 兜底：--clip 给每张图加 <clipPath> 包住 viewBox，防止以后又写宽了 ——
     但**兜底不是修好**：被裁掉的字等于没有，所以检查项必须先清零。

--selftest 造一张故意写宽的图，证明检查真的会报。
用法：python -X utf8 tools/svg_check.py [--clip] [--selftest]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

FIG_DIR = "assets/fig"
TOL = 1.0          # viewBox 单位，超出 1 个单位以内算取整噪声
DESC = 0.26        # 基线以下的下伸部估算（字号的倍数）


def wlen(s: str) -> float:
    """显示宽度当量：CJK=1，其余=0.55（与 tools/make_figs3.py 同口径）。"""
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s)


def style_prop(svg: str, prop: str) -> dict:
    """从 <style> 里把 .cls{prop:V} 抠出来，供 class= 的 text 用。"""
    out: dict[str, object] = {}
    for block in re.findall(r"<style[^>]*>(.*?)</style>", svg, re.S):
        for sel, n in re.findall(r"\.([A-Za-z0-9_-]+)\s*\{[^}]*?" + prop + r":\s*([\w.-]+)", block):
            out[sel] = n
    return out


def view_box(svg: str) -> tuple[float, float]:
    m = re.search(r'viewBox="\s*([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)', svg)
    if m:
        return float(m.group(3)), float(m.group(4))
    m = re.search(r'<svg[^>]*\swidth="([\d.]+)"[^>]*\sheight="([\d.]+)"', svg)
    if m:
        return float(m.group(1)), float(m.group(2))
    return 0.0, 0.0


def check_svg(path: str) -> list[dict]:
    svg = io.open(path, encoding="utf-8").read()
    vw, vh = view_box(svg)
    if not vw or not vh:
        return [{"file": path, "text": "<无 viewBox>", "right": 0, "vw": 0, "line": 0}]
    fs_by_class = {k: float(re.match(r"[\d.]+", str(v)).group(0))
                   for k, v in style_prop(svg, "font-size").items()}
    anchor_by_class = {k: str(v) for k, v in style_prop(svg, "text-anchor").items()}
    bad = []
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", svg, re.S):
        attrs, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        txt = body.strip()
        if not txt:
            continue
        x = float(re.search(r'\bx="(-?[\d.]+)"', attrs).group(1)) if re.search(r'\bx="', attrs) else 0.0
        y = float(re.search(r'\by="(-?[\d.]+)"', attrs).group(1)) if re.search(r'\by="', attrs) else 0.0
        fs_m = re.search(r'font-size="([\d.]+)"', attrs)
        fs = float(fs_m.group(1)) if fs_m else 16.0
        if not fs_m:
            cls = re.search(r'class="([^"]+)"', attrs)
            if cls:
                for name in cls.group(1).split():
                    if name in fs_by_class:
                        fs = fs_by_class[name]
                        break
        w = wlen(txt) * fs
        anchor = "start"
        a_m = re.search(r'text-anchor="(\w+)"', attrs)
        if a_m:
            anchor = a_m.group(1)
        else:
            cls = re.search(r'class="([^"]+)"', attrs)
            if cls:
                for name in cls.group(1).split():
                    if name in anchor_by_class:
                        anchor = anchor_by_class[name]
                        break
        left, right = x, x + w
        if anchor == "middle":
            left, right = x - w / 2, x + w / 2
        elif anchor == "end":
            left, right = x - w, x
        line = svg[:m.start()].count("\n") + 1
        if right > vw + TOL or left < -TOL or y + fs * DESC > vh + TOL or y - fs < -TOL:
            bad.append({"file": path, "line": line, "text": txt[:44],
                        "left": round(left, 1), "right": round(right, 1),
                        "bottom": round(y + fs * DESC, 1), "vw": vw, "vh": vh})
    return bad


def clip_svg(path: str) -> bool:
    """给 SVG 包一层 clipPath（幂等：已加过就跳过）。返回是否改动。"""
    svg = io.open(path, encoding="utf-8").read()
    if 'data-clipped="1"' in svg:
        return False
    vw, vh = view_box(svg)
    if not vw or not vh:
        return False
    cid = "vb-" + re.sub(r"\W+", "-", os.path.splitext(os.path.basename(path))[0])
    i = svg.index(">", svg.index("<svg")) + 1
    head = svg[:i]
    body = svg[i:]
    if body.rstrip().endswith("</svg>"):
        body = body.rstrip()[: -len("</svg>")]
    clip = (f'\n<defs data-clipped="1"><clipPath id="{cid}">'
            f'<rect x="0" y="0" width="{vw}" height="{vh}"/></clipPath></defs>\n'
            f'<g clip-path="url(#{cid})">')
    out = head + clip + body + "\n</g>\n</svg>\n"
    io.open(path, "w", encoding="utf-8").write(out)
    return True


TOKEN_RE = re.compile(r"[0-9A-Za-z_\.\+\-/%=()·\*²³¹⁰-₟→←⇒≤≥±×÷\u00b7]+")


def pack_lines(text: str, fs: float, avail: float) -> list[str]:
    """按不可断 token 贪心装箱：数学式、英文词、数字整体不拆，汉字逐字可断。"""
    toks: list[str] = []
    i = 0
    while i < len(text):
        m = TOKEN_RE.match(text, i)
        if m:
            toks.append(m.group(0))
            i = m.end()
        else:
            toks.append(text[i])
            i += 1
    lines: list[str] = []
    cur = ""
    for t in toks:
        if wlen(cur + t) * fs > avail and cur:
            lines.append(cur.strip())
            cur = t
        else:
            cur += t
    if cur.strip():
        lines.append(cur.strip())
    return lines


def fix_svg(path: str, pad: float = 8.0, dry: bool = False) -> list[str]:
    """把冲出 viewBox 的文字行改成多行（或轻微缩字号），必要时长画布。返回改动说明。"""
    svg = io.open(path, encoding="utf-8").read()
    vw, vh = view_box(svg)
    if not vw:
        return []
    fsb = {k: float(re.match(r"[\d.]+", str(v)).group(0))
           for k, v in style_prop(svg, "font-size").items()}
    abc = {k: str(v) for k, v in style_prop(svg, "text-anchor").items()}
    notes: list[str] = []
    out = svg
    max_bottom = 0.0

    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", svg, re.S):
        attrs, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not body or body not in out:
            continue
        xm = re.search(r'\bx="(-?[\d.]+)"', attrs)
        ym = re.search(r'\by="(-?[\d.]+)"', attrs)
        x = float(xm.group(1)) if xm else 0.0
        y = float(ym.group(1)) if ym else 0.0
        fm = re.search(r'font-size="([\d.]+)"', attrs)
        fs = float(fm.group(1)) if fm else 16.0
        anchor = "start"
        am = re.search(r'text-anchor="(\w+)"', attrs)
        cls = re.search(r'class="([^"]+)"', attrs)
        if cls:
            for n in cls.group(1).split():
                if n in fsb and not fm:
                    fs = fsb[n]
                if n in abc:
                    anchor = abc[n]
        if am:
            anchor = am.group(1)
        w = wlen(body) * fs
        right = x + (w if anchor == "start" else w / 2 if anchor == "middle" else x - x + 0)
        if anchor == "end":
            right = x
        max_bottom = max(max_bottom, y + fs * DESC)
        if right <= vw + TOL:
            continue
        avail = max(vw - (x if anchor == "start" else x - w / 2) - pad, fs * 2)
        shrink = avail / right if right else 1.0
        old = m.group(0)
        if shrink >= 0.90:                       # 差一点点：缩字号，不拆行
            new_attrs = attrs if fm else attrs + f' font-size="{fs:.1f}"'
            new_attrs = re.sub(r'font-size="[\d.]+"', f'font-size="{fs*shrink*0.99:.1f}"', new_attrs)
            out = out.replace(old, f"<text{new_attrs}>{body}</text>", 1)
            notes.append(f"{os.path.basename(path)}:{svg[:m.start()].count(chr(10)) + 1} 缩字号 "
                         f"{fs:.1f}→{fs*shrink*0.99:.1f}（原右边界 {right:.0f}/{vw:.0f}）")
            continue
        lines = pack_lines(body, fs, avail)
        if len(lines) < 2:
            lines = [body[:len(body) // 2], body[len(body) // 2:]]
        gap = fs * 1.32
        pieces = []
        for k, ln in enumerate(lines):
            a = attrs
            a = re.sub(r'\by="[\d.]+"', f'y="{y + k * gap:.1f}"', a) if ym else a + f' y="{y + k * gap:.1f}"'
            if not fm:
                a += f' font-size="{fs:.1f}"'
            pieces.append(f"<text{a}>{ln}</text>")
        out = out.replace(old, "\n".join(pieces), 1)
        max_bottom = max(max_bottom, y + (len(lines) - 1) * gap + fs * DESC)
        notes.append(f"{os.path.basename(path)}:{svg[:m.start()].count(chr(10)) + 1} 拆成 {len(lines)} 行"
                     f"（原右边界 {right:.0f}/{vw:.0f}）")

    if max_bottom > vh + TOL:
        new_h = round(max_bottom + 4, 1)
        out = re.sub(r'viewBox="(0 0 [\d.]+ )[\d.]+(")', rf'viewBox="\g<1>{new_h:g}\g<2>', out, count=1)
        notes.append(f"{os.path.basename(path)} 画布加高 {vh:g}→{new_h:g}")
    if out != svg and not dry:
        io.open(path, "w", encoding="utf-8").write(out)
    return notes


def text_boxes(svg: str) -> list[tuple]:
    """所有 <text> 的估算框：(x0, y_top, x1, y_bottom, 文本)。字号从属性或 class 取。"""
    fsb = {k: float(re.match(r"[\d.]+", str(v)).group(0))
           for k, v in style_prop(svg, "font-size").items()}
    boxes = []
    for m in re.finditer(r"<text([^>]*)>(.*?)</text>", svg, re.S):
        attrs, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not body:
            continue
        x = float(re.search(r'x="(-?[\d.]+)"', attrs).group(1)) if re.search(r'x="', attrs) else 0.0
        y = float(re.search(r'y="(-?[\d.]+)"', attrs).group(1)) if re.search(r'y="', attrs) else 0.0
        fm = re.search(r'font-size="([\d.]+)"', attrs)
        fs = float(fm.group(1)) if fm else 16.0
        cls = re.search(r'class="([^"]+)"', attrs)
        if cls and not fm:
            for n in cls.group(1).split():
                if n in fsb:
                    fs = fsb[n]
                    break
        w = wlen(body) * fs
        if re.search(r'text-anchor="middle"', attrs):
            x -= w / 2
        elif re.search(r'text-anchor="end"', attrs):
            x -= w
        boxes.append((x, y - fs * 0.86, x + w, y + fs * DESC, body[:26]))
    return boxes


def box_overflow(path: str, tol: float = 3.0) -> list[str]:
    """文字冲出它自己所在的盒子：某个 rect 包住了文字的落笔点，但装不下整行文字。
    这是成品里最难看的一类缺陷——字压在圆角矩形边框上，浏览器预览看不出来。"""
    svg = io.open(path, encoding="utf-8").read()
    rects = []
    for m in re.finditer(r"<rect([^>]*)/?>", svg):
        a = m.group(1)
        try:
            x = float(re.search(r'x="(-?[\d.]+)"', a).group(1))
            y = float(re.search(r'y="(-?[\d.]+)"', a).group(1))
            w = float(re.search(r'width="([\d.]+)"', a).group(1))
            h = float(re.search(r'height="([\d.]+)"', a).group(1))
        except AttributeError:
            continue
        if w > 4 and h > 4:
            rects.append((x, y, x + w, y + h))
    out = []
    for tx0, ty0, tx1, ty1, txt in text_boxes(svg):
        anchor = ((tx0 + tx1) / 2, (ty0 + ty1) / 2)
        cands = [r for r in rects if r[0] <= anchor[0] <= r[2] and r[1] <= anchor[1] <= r[3]]
        if not cands:
            continue
        r = min(cands, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
        over = max(tx1 - r[2], r[0] - tx0, ty1 - r[3], r[1] - ty0)
        if over > tol:
            out.append(f"{os.path.basename(path)} 文字「{txt}」冲出所在盒子 {over:.0f} 单位")
    return out



def collisions(path: str) -> list[str]:
    """同行重叠：两条 text 的基线差 < 0.55 字号，且水平投影重叠 > 20% 小框宽。
    口径刻意收窄（修前实测 35 处“重叠”里绝大多数是柱状图上下相邻的标签，宽度模型把
    CJK 标点按整字宽算导致假阳性）。这里只抓 --fix 拆行后压在同一基线上的那种真事故。"""
    svg = io.open(path, encoding="utf-8").read()
    fsb = {k: float(re.match(r"[\d.]+", str(v)).group(0))
           for k, v in style_prop(svg, "font-size").items()}
    boxes = []
    for m in re.finditer(r"<text([^>]*)>(.*?)</text>", svg, re.S):
        attrs, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not body:
            continue
        x = float(re.search(r'x="(-?[\d.]+)"', attrs).group(1)) if re.search(r'x="', attrs) else 0.0
        y = float(re.search(r'y="(-?[\d.]+)"', attrs).group(1)) if re.search(r'y="', attrs) else 0.0
        fm = re.search(r'font-size="([\d.]+)"', attrs)
        fs = float(fm.group(1)) if fm else 16.0
        cls = re.search(r'class="([^"]+)"', attrs)
        if cls and not fm:
            for n in cls.group(1).split():
                if n in fsb:
                    fs = fsb[n]
                    break
        w = wlen(body) * fs
        if re.search(r'text-anchor="middle"', attrs):
            x -= w / 2
        elif re.search(r'text-anchor="end"', attrs):
            x -= w
        boxes.append((x, y, x + w, fs, body[:22]))
    out = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            fs = min(a[3], b[3])
            if abs(a[1] - b[1]) > 0.55 * fs:
                continue                     # 不同行，不算
            ow = min(a[2], b[2]) - max(a[0], b[0])
            small = min(a[2] - a[0], b[2] - b[0])
            if ow > 0 and small and ow / small > 0.2:
                out.append(f"{os.path.basename(path)} 同基线 y={a[1]:g} 重叠 {ow:.0f}/{small:.0f}："
                           f"「{a[4]}」×「{b[4]}」")
    return out


def main() -> int:
    args = sys.argv[1:]
    if "--selftest" in args:
        tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "svg_check_selftest.svg")
        io.open(tmp, "w", encoding="utf-8").write(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100">\n'
            '<style>.t{font-size:16px}</style>\n'
            '<text x="10" y="40" class="t">短</text>\n'
            '<text x="10" y="70" class="t">这一行故意写得比 viewBox 宽很多很多很多</text>\n'
            "</svg>\n")
        offenders = check_svg(tmp)
        print("selftest 报告冲出画布的行：", offenders)
        ok1 = len(offenders) == 1 and "故意" in offenders[0]["text"]
        # 修完必须：0 冲出、一个字都不能丢
        fix_svg(tmp)
        after = check_svg(tmp)
        kept = "".join(re.findall(r">([^<]*)</text>", io.open(tmp, encoding="utf-8").read()))
        ok3 = not after and kept.replace(" ", "") == "短这一行故意写得比viewBox宽很多很多很多".replace(" ", "")
        changed = clip_svg(tmp)
        again = clip_svg(tmp)
        ok2 = changed and not again and 'data-clipped="1"' in io.open(tmp, encoding="utf-8").read()
        os.remove(tmp)
        print(("PASS " if ok1 else "FAIL ") + "抓到写宽的文字行")
        print(("PASS " if ok3 else "FAIL ") + "--fix 修完不再冲出，且原文一字不丢")
        print(("PASS " if ok2 else "FAIL ") + "clipPath 兜底且幂等")
        return 0 if (ok1 and ok2 and ok3) else 1

    files = sorted(glob.glob(os.path.join(FIG_DIR, "*.svg")))
    if not files:
        print(f"没找到 {FIG_DIR}/*.svg —— 口径不对，判失败", file=sys.stderr)
        return 1
    if "--fix" in args:
        changed = []
        for f in files:
            changed += fix_svg(f)
        print(f"--fix 改动 {len(changed)} 处：")
        for c in changed:
            print("  " + c)
    if "--clip" in args:
        n = sum(1 for f in files if clip_svg(f))
        print(f"clipPath 兜底：新加 {n} 张，已存在 {len(files) - n} 张")
    all_bad = []
    all_col = []
    all_box = []
    for f in files:
        all_bad += check_svg(f)
        all_col += collisions(f)
        all_box += box_overflow(f)
    import xml.etree.ElementTree as _ET
    xml_bad = []
    for f in files:
        try:
            _ET.parse(f)
        except Exception as e:
            xml_bad.append(f"{os.path.basename(f)} ｜ {str(e)[:60]}")
    print(f"严格 XML 解析：{len(xml_bad)} 张不合法（<img src=x.svg> 走 XML 解析，"
          f"不合法=整张图在成品里消失）")
    for b in xml_bad:
        print("  [XML] " + b)
    print(f"检查 {len(files)} 张图：{len(all_bad)} 行冲出 viewBox，"
          f"{len(all_col)} 处同基线重叠，{len(all_box)} 行文字冲出所在盒子")
    for b in all_bad:
        print(f"  [冲出画布] {os.path.basename(b['file'])}:{b['line']} 右边界 {b['right']}/{b['vw']} "
              f"下边界 {b['bottom']}/{b['vh']} ｜ {b['text']}")
    for b in sorted(set(all_box))[:26]:
        print("  [冲出盒子] " + b)
    print(f"  [冲出盒子] 合计 {len(all_box)} 处")
    for c in all_col[:20]:
        print("  [重叠] " + c)
    if len(all_col) > 20:
        print(f"  [重叠] …另有 {len(all_col) - 20} 处")
    return 0 if not (all_bad or all_col or all_box or xml_bad) else 1


if __name__ == "__main__":
    sys.exit(main())
