#!/usr/bin/env python3
"""tools/fig_text_check.py — 图里写的带单位数字，正文里还在不在。

为什么要有它（2026-10-08）：这一轮正文改了七八个数（反电势 19.17→12.78、悬臂梁刚度
79,000→46 万、模态 22 Hz→54 Hz、触觉 2–3 mm→4.5–5.8 mm、电流 6 A→5 A…），
而图是另一批文件，没人会顺手改。图 17-1 的标签与画面对不上，就是靠人眼偶然发现的；
靠人眼不可复制，所以要一道门：**图的 <text> 里凡是带单位的数字，必须在全书正文里找得到**。

口径（刻意收窄，避免轴刻度刷屏）：
  只看"数字 + 单位"的 token（N·m / Hz / V / mm / ms / rad/s / kWh / A / W / 倍 / 元 …），
  以及 4 位以上的纯数字；坐标轴上的 0.2、0.4、100 这类无单位刻度不参与判定。
  正文侧把 1,234 的逗号去掉、把 ×10^n 的写法归一后再比对。
--selftest 造一张写着 79,000 N/m 的图，正文只有 460,000 N/m，必须报。
用法：python -X utf8 tools/fig_text_check.py [--selftest]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

UNIT = (r"N·m|mN·m|kN·m|N/m|Hz|kHz|rad/s|rad|kWh|Wh|VA|kW|ms|µs|us|mm|cm|kg|kJ|"
        r"℃|°C|°/s|°/hr|Mbps|Klux|bit|倍|万|元|美元|帧|点/s|B|V|A|W|N|s|m|g|°")
RE_FIG_NUM = re.compile(r"(\d[\d.,]*)\s*(" + UNIT + r")")
RE_PLAIN = re.compile(r"\b(\d{4,})\b")


def norm(s: str) -> str:
    return s.replace(",", "").replace("，", "")


def fig_texts(svg_path: str) -> list[str]:
    s = io.open(svg_path, encoding="utf-8").read()
    return [re.sub(r"<[^>]+>", "", t).strip()
            for t in re.findall(r"<text[^>]*>(.*?)</text>", s, re.S)]


def check(fig_dir: str, drafts_dir: str) -> list[dict]:
    # 语料不止正文：图上的数常常来自调研档案（research/、bible/），那也是可追溯的。
    files = glob.glob(os.path.join(drafts_dir, "unit-*", "draft.md"))
    root = os.path.dirname(os.path.abspath(drafts_dir))
    for extra in ("research", os.path.join("..", "research"), "bible"):
        files += glob.glob(os.path.join(root, extra, "*.md"))
    corpus = norm(" ".join(io.open(f, encoding="utf-8").read()
                           for f in files if os.path.exists(f)))
    bad = []
    for svg in sorted(glob.glob(os.path.join(fig_dir, "*.svg"))):
        name = os.path.basename(svg)
        uid = re.match(r"f(\d\d)", name)
        uid = uid.group(1) if uid else "??"
        for line in fig_texts(svg):
            for num, unit in RE_FIG_NUM.findall(line):
                token = norm(num)
                if len(token) < 2 and unit not in ("倍", "°C", "℃"):
                    continue
                if token not in corpus and f"{token} {unit}" not in corpus \
                        and f"{token}{unit}" not in corpus:
                    bad.append({"fig": name, "unit_id": uid, "num": token,
                                "unit": unit, "line": line[:52]})
            for num in RE_PLAIN.findall(line):
                if norm(num) not in corpus:
                    bad.append({"fig": name, "unit_id": uid, "num": norm(num),
                                "unit": "(纯数字)", "line": line[:52]})
    return bad


def selftest() -> int:
    import tempfile
    d = tempfile.mkdtemp(prefix="figcheck_")
    fig = os.path.join(d, "f22-diagnosis.svg")
    io.open(fig, "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60">'
        '<text x="4" y="10">连杆刚度 79,000 N/m</text>'
        '<text x="4" y="24">模态 22 Hz</text>'
        '<text x="4" y="38">现行值 460,000 N/m 与 54 Hz</text>'
        "</svg>\n")
    dd = os.path.join(d, "drafts", "unit-22")
    os.makedirs(dd, exist_ok=True)
    io.open(os.path.join(dd, "draft.md"), "w", encoding="utf-8").write(
        "正文已改成 460,000 N/m 与 54 Hz，旧数不再出现。\n")
    bad = check(d, os.path.join(d, "drafts"))
    stale = {b["num"] for b in bad}
    print("报出的陈旧图内数字：", sorted(stale))
    ok1 = "79000" in stale and "22" in stale
    ok2 = "460000" not in stale and "54" not in stale
    print(("PASS " if ok1 else "FAIL ") + "正文里已消失的数（79,000 / 22 Hz）被抓到")
    print(("PASS " if ok2 else "FAIL ") + "正文里还在的数（460,000 / 54 Hz）不误报")
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    return 0 if (ok1 and ok2) else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = check(os.path.join(root, "assets", "fig"), os.path.join(root, "drafts"))
    print(f"图内带单位数字在全书正文里找不到的：{len(bad)} 处")
    for b in bad:
        print(f"  {b['fig']}（第 {b['unit_id']} 章）｜{b['num']} {b['unit']}｜图上文字：{b['line']}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
