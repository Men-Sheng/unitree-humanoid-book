#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_xrefs.py — 全书交叉引用体检：每个"第 NN 章"都必须指到真实存在的章。

为什么要有：2026-10-08 人工通读时抓到两处失效引用（"第 05 章那张温漂表"——05 章根本没有温度表；
"第 35 章会算它为什么是 1 小时"——35 章明写那个数没公布）。这类错在改定位、重编号之后
一定会批量出现，靠人读不划算。

三档判定：
  BAD   章号不存在（>45 或 <0），或指向自己
  WARN  章号存在，但被引章的标题里找不到引用句给出的关键词
        （写法是 `第 05 章（k_t 温漂）` 这种带括注的才检查；没括注的跳过，避免瞎猜）
  OK    其余

用法：
  python -X utf8 tools/check_xrefs.py            # 全书
  python -X utf8 tools/check_xrefs.py --stats
退出码：有 BAD 就 1。
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAST_UNIT = 45

RE_REF = re.compile(r"第\s*(\d{1,2})\s*章(?:（([^）]{2,28})）)?")
CODE_FENCE = re.compile("^```.*$", re.M)


def titles():
    """从 units.yaml 读 46 章标题；读不到就退回从各 draft 的一级标题。"""
    t = {}
    try:
        import yaml
        d = yaml.safe_load(io.open(os.path.join(ROOT, "outline", "units.yaml"),
                                   encoding="utf-8").read())
        for u in d.get("units", []):
            key = str(u.get("unit") or u.get("id") or "").strip()
            m = re.search(r"(\d{1,2})", key)
            if m and u.get("title"):
                t[int(m.group(1))] = u["title"]
    except Exception:
        pass
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        n = int(os.path.basename(os.path.dirname(p)).replace("unit-", ""))
        if n not in t:
            first = io.open(p, encoding="utf-8").read().split(chr(10))[0]
            t[n] = first.lstrip("# ").strip()
    return t


def frag(w):
    """把一个括注拆成可查的片段：整串、连接词切开后的词、以及长词的前两字。

    为什么要拆：正文写"认证与标准"，引用写"安全与认证"——整串匹配会误报失效。
    前两字这一档是折中：够具体到不像巧合，又不至于把两个话题混成一个。
    """
    parts = [x for x in re.split(r"(?:没有|[与的了是在不])", w) if len(x) >= 2]
    out = [w] + parts + [p[:2] for p in parts if len(p) >= 3]
    return [x for x in out if len(x) >= 2]


def selftest():
    """这个门自己必须先证明它抓得住真失效引用（08 年人工抓到过一例）。"""
    body = {5: "这一章讲洛伦兹力与 sinθ，没有谈温度。",
            35: "本章算电压塌陷：13 串、内阻、掉到复位阈值。"}
    cases = [
        (5, "温漂表", True),          # 真失效：05 章没有温漂 → 必须报
        (35, "电压塌陷", False),      # 真存在 → 不许报
        (5, "洛伦兹力与 sinθ", False),  # 措辞不同但片段命中 → 不许报
    ]
    bad = 0
    for n, gloss, want_flag in cases:
        toks = [w for w in re.split(r"[、,，/；; ]+", gloss) if len(w) >= 2]
        miss = [w for w in toks if not any(f in body[n] for f in frag(w))]
        flagged = bool(toks) and len(miss) == len(toks)
        good = flagged == want_flag
        bad += 0 if good else 1
        print("  第 %02d 章（%s）判为失效=%-5s 期望=%-5s %s"
              % (n, gloss, flagged, want_flag, "ok" if good else "← 判错"))
    print("check_xrefs 自检：%d/%d 通过 → %s"
          % (len(cases) - bad, len(cases), "PASS" if not bad else "FAIL：不许上岗"))
    return 0 if not bad else 1



# ═════════════════════════════════════════════════════════════════════
# --claims：第二种引用失效——"第 NN 章说过 X"，但 X 里的数不在 NN 章。
# 为什么要单独一路：上一路只解析 `第 NN 章（gloss）` 这种带括号的写法，
# 而正文里大量引用是散文式的（"第 13 章说过，一颗 130 W 的大脑"）。
# 判据刻意只盯**数字+单位**：它是句子里唯一可证伪的部分，也是跨章最容易搬错的东西。
# 命中不到就报"待人工判定"，不直接判死——"上一章那个结论"这类无数引用是正常的。
RE_CHAP = re.compile(r"第\s*(\d{1,2})\s*章")
RE_ATTR = re.compile("说过|算过|给过|列过|讲过|那张|那条|那一格|那行|那表|推过|核过|定过|拆过")
RE_NUMUNIT = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:W|kW|VA|Wh|kWh|V|A|mV|N·m|mN·m|N|Hz|kHz|MHz|rad/s|rad|°|ms|µs|us|"
    r"s|min|h|d|B|KB|MB|GB|bit|ppm|%|mm|cm|m|kg|g|℃|°C|元|美元|块)")


def claim_scan(root):
    import glob as _g
    import os as _o
    texts = {}
    for f in _g.glob(os.path.join(root, "drafts", "unit-*", "draft.md")):
        uid = _o.path.basename(_o.path.dirname(f)).split("-")[1]
        texts[uid] = io.open(f, encoding="utf-8").read()
    bad = []
    for uid, body in sorted(texts.items()):
        if uid in ("41", "44"):
            continue
        plain = re.sub(r"`[^`]*`", " ", body)
        for line_no, line in enumerate(plain.split(chr(10)), 1):
            for m in RE_CHAP.finditer(line):
                tgt = m.group(1).zfill(2)
                if tgt == uid or tgt not in texts:
                    continue
                sent = line[max(0, m.end() - 2):m.end() + 40]
                if not RE_ATTR.search(sent):
                    continue
                nums = set(n.strip().replace(",", "") for n in RE_NUMUNIT.findall(sent))
                nums = {n for n in nums if n[:1].isdigit()}
                if not nums:
                    continue
                tgt_txt = texts[tgt].replace(",", "")
                if all(n not in tgt_txt for n in nums):
                    bad.append((uid, line_no, tgt, sorted(nums), re.sub(r"\s+", " ", sent)[:64]))
    return bad


def claim_selftest():
    """故意的错引用必须被抓到。"""
    import os as _o
    import tempfile
    import shutil
    d = _o.path.join(tempfile.gettempdir(), "xr_claims")
    shutil.rmtree(d, ignore_errors=True)
    for uid, body in (("05", "第 13 章说过，一颗 130 W 的大脑会烫手。" + chr(10)),
                      ("13", "这里只有 55 W 的铜损与 24 V 母线，别的数本章不涉及。" + chr(10))):
        pth = os.path.join(d, "drafts", "unit-" + uid)
        os.makedirs(pth, exist_ok=True)
        io.open(_o.path.join(pth, "draft.md"), "w", encoding="utf-8").write(body)
    got = claim_scan(d)
    shutil.rmtree(d, ignore_errors=True)
    hit = bool(got) and got[0][0] == "05" and got[0][2] == "13"
    print(("PASS " if hit else "FAIL ") + "假引用（13 章没有 130 W）被抓到")
    return 0 if hit else 1


RE_DTN = re.compile(r"do-not-touch\.md`?\s*第\s*([\d、,，\s]+?)\s*条")


def dtn_entries():
    """那张表有两种写法：前半是 Markdown 表格行「| 12 |」，v3 之后是有序列表「35. **…**」。
    只认表格行会把 35 以后的条目全判成不存在（本门第一版就这么假报警过一次）。"""
    p = os.path.join(ROOT, "bible", "do-not-touch.md")
    if not os.path.exists(p):
        return set()
    txt = io.open(p, encoding="utf-8").read()
    rows = {int(m.group(1)) for m in re.finditer(r"^\|\s*(\d+)\s*\|", txt, re.M)}
    items = {int(m.group(1)) for m in re.finditer(r"^(\d+)\.\s+\*\*", txt, re.M)}
    return rows | items


def dtn_max():
    e = dtn_entries()
    return max(e) if e else 0


def bible_entry_refs(body):
    """正文里「bible/do-not-touch.md 第 N 条」这类引用，N 必须真的存在于那张表里。
    抓到过的实例：第 01 章引用过不存在的第 40 条（那张表当时只有 34 条）。"""
    have = dtn_entries()
    out = []
    for n, txt in body.items():
        for i, line in enumerate(txt.split(chr(10))):
            for m in RE_DTN.finditer(line):
                for num in re.findall(r"\d+", m.group(1)):
                    if int(num) not in have:
                        out.append((n, i + 1, int(num)))
    return out


def dtn_total(body):
    return sum(len(RE_DTN.findall(t)) for t in body.values())


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if "--claims-selftest" in sys.argv:
        return claim_selftest()
    if "--claims" in sys.argv:
        rows = claim_scan(ROOT)
        print(f"散文式引用（第 NN 章说过 X）里数字在目标章一个都没有的：{len(rows)} 处")
        for uid, ln, tgt, nums, sent in rows:
            print(f"  unit-{uid}:{ln} → 第 {tgt} 章｜数 {nums} 目标章没有｜…{sent}")
        return 0
    stats = "--stats" in sys.argv
    T = titles()
    body = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        n = int(os.path.basename(os.path.dirname(p)).replace("unit-", ""))
        body[n] = io.open(p, encoding="utf-8").read()
    total = ok = bad = warn = 0
    rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md"))):
        me = int(os.path.basename(os.path.dirname(p)).replace("unit-", ""))
        txt = CODE_FENCE.sub("", io.open(p, encoding="utf-8").read())
        for i, line in enumerate(txt.split(chr(10))):
            if line.lstrip().startswith("#"):
                continue
            for m in RE_REF.finditer(line):
                n = int(m.group(1))
                gloss = (m.group(2) or "").strip()
                total += 1
                if n > LAST_UNIT or n < 0:
                    bad += 1
                    rows.append(("BAD", me, i + 1, "章号 %d 不存在" % n, line.strip()[:70]))
                    continue
                if n == me and not re.search(r"本章|就是本章", line):
                    # 书里用章号自指是正常的（"这就是第 06 章的全部因果"），只记不报
                    ok += 1
                    continue
                if gloss and n != me:
                    # 真检查：被引那一章的正文里，到底有没有括注说的这件事。
                    # 抓到过的实例：「第 05 章那张温漂表」——05 章通篇没有温漂。
                    toks = [w for w in re.split(r"[、,，/；; ]+", gloss) if len(w) >= 2]
                    tgt = body.get(n, "")
                    miss = [w for w in toks if not any(
                        f in tgt for f in frag(w))]
                    if toks and len(miss) == len(toks):
                        warn += 1
                        rows.append(("STALE", me, i + 1,
                                     "第 %02d 章正文里没有「%s」" % (n, "、".join(miss)[:26]),
                                     line.strip()[:70]))
                    else:
                        ok += 1
                else:
                    ok += 1
    dtn = bible_entry_refs(body)
    for me, ln, num in dtn:
        bad += 1
        rows.append(("BAD", me, ln, "bible/do-not-touch.md 第 %d 条不存在（现在只有 %d 条）"
                     % (num, dtn_max()), ""))
    print("交叉引用 %d 处：可确认 %d，章号/自指错 %d，**疑似失效引用 %d**"
          % (total, ok, bad, warn))
    print("bible 条目引用：查了 %d 处，失效 %d 处" % (dtn_total(body), len(dtn)))
    if not stats:
        for sev, me, ln, msg, ctx in rows:
            print("  %-5s unit-%02d:%-4d %s ｜ %s" % (sev, me, ln, msg, ctx))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
