#!/usr/bin/env python3
"""tools/check_vendor_ledger.py — 「[查]」必须能在别家一手台账里找到逐字引用。

为什么需要它：第 29–34 章大量以别家厂商的数为输入，正文用 [查] 表示"本书已读到原文"。
本轮补了 `research/other-vendor-firsthand.md`（逐字原文 + URL + 日期）之后，第七轮独立审阅仍然指出：
**有一批 [查] 在台账里没有对应行**（ALOHA 的 50 条演示、Figure/Gemini 的成功率、GO-2、GEN-0、SynGrasp、
北京 95% 合格率、Tesla 的共用仿真器等）。这些其实是作者蓝图附件里的二手转述——按图例应记 [推]。
这道门把这件事变成可复查的清单：**每章每一处 [查]， enclosing 行里出现的厂商标 token 必须在台账里也出现**；
对不上就列进清单（不判死——token 匹配精度有限，判死会让人学会忽略它，同 check_xrefs --claims 的理由）。
但台账文件缺失、或全书一处 [查] 都没读到，就是门自己在空跑 ⇒ 硬失败。

用法：python -X utf8 tools/check_vendor_ledger.py [--verbose] [--selftest]
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "research", "other-vendor-firsthand.md")
UNITS = ["29", "30", "31", "32", "33", "34"]
TOKENS = ["helix", "gr00t", "pi*", "π*", "smolvla", "gaia", "cosmos", "droid", "agibot",
          "1x", "genie", "ge-act", "gen-0", "graspvla", "syngrasp", "aloha", "figure",
          "gemini", "go-1", "go-2", "acot", "tesla", "wayve", "nvidia", "智元", "宇树",
          "unifolm", "lerobot", "umi", "moteus", "odrive", "physicalintelligence", "π0"]
MIN_CLAIMS = 6


def ledger_text():
    if not os.path.exists(LEDGER):
        return None
    return io.open(LEDGER, encoding="utf-8").read().lower()


def check():
    led = ledger_text()
    if led is None:
        return None, [], ["台账不存在：research/other-vendor-firsthand.md —— 这道门没输入"]
    if len(led.strip()) < 500:
        return None, [], ["台账只有 %d 字符，不可能覆盖全书的 [查]：这道门现在等于没跑" % len(led)]
    n_claims = 0
    orphan = []
    for u in UNITS:
        p = os.path.join(ROOT, "drafts", "unit-%s" % u, "draft.md")
        if not os.path.exists(p):
            orphan.append((u, 0, "章文件缺失"))
            continue
        for ln, line in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
            if "[查]" not in line:
                continue
            n_claims += 1
            low = line.lower()
            hits = [k for k in TOKENS if k in low]
            hits += [m.group(0) for m in re.finditer(r'\d{4}\.\d{4,5}', line)]
            hits += [m.group(0) for m in re.finditer(r'https?://[\w./-]+', line) if m.group(0).rstrip('/') in led]
            if not hits:
                orphan.append((u, ln, "有 [查] 但认不出厂商标，需人工看一眼"))
                continue
            miss = [k for k in hits if k not in led]
            if miss:
                orphan.append((u, ln, "台账里没有这几家的逐字行：%s ｜ %s"
                               % ("、".join(miss), re.sub(r"\s+", " ", line.strip())[:64])))
    return n_claims, orphan, []


def selftest():
    """四条明确断言：有台账的不误报、没台账的被抓、无厂商 token 的只进清单、台账缺失时自曝没输入。"""
    led = ("| helix | `S2 is built on a 7B-parameter VLM` | figure.ai |\n"
           "| gr00t | `Base model (3B params)` | github |\n"
           "π0 `10 integration steps`；droid `76k demonstration trajectories`；cosmos `4B omni-model`；"
           "agibot `1,001,552 trajectories`；gaia `448×960`；smolvla 450m；unifolm 零命中\n")

    def miss_of(line):
        low = line.lower()
        hits = [k for k in TOKENS if k in low]
        return hits, [k for k in hits if k not in led]

    h1, m1 = miss_of('Helix 的 S1 是 80M [查]')
    ok1 = h1 and not m1
    h2, m2 = miss_of('Gemini Robotics 自陈 44% [查]')
    ok2 = h2 == ['gemini'] and m2 == ['gemini']
    h3, m3 = miss_of('这一行有 [查] 但认不出是谁家的数')
    ok3 = h3 == [] and m3 == []
    real = os.path.exists
    os.path.exists = lambda p: False if str(p).endswith('other-vendor-firsthand.md') else real(p)
    n_empty, orphan_empty, hard_empty = check()
    os.path.exists = real
    ok4 = n_empty is None and len(hard_empty) == 1
    for label, x in [('有台账的 [查] 不误报', ok1), ('没台账的 [查] 被抓到', ok2),
                     ('认不出厂商时不硬判', ok3), ('台账缺失时门自曝没输入', ok4)]:
        print(('PASS ' if x else 'FAIL ') + label)
    bad = [ok1, ok2, ok3, ok4].count(False)
    print('自检 %d/4' % (4 - bad))
    return 0 if bad == 0 else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    verbose = "--verbose" in sys.argv
    n, orphan, hard = check()
    if hard:
        for h in hard:
            print("✗ " + h)
        return 1
    if n < MIN_CLAIMS:
        print("✗ 只认出 %d 处 [查]（应 ≥%d）：正则或章清单失效，这道门现在等于没跑" % (n, MIN_CLAIMS))
        return 1
    print("别家一手台账比对：%d 处 [查] 参与检查，台账里找不到逐字行的 %d 处" % (n, len(orphan)))
    for u, ln, msg in orphan[:20]:
        print("  · 第 %s 章 行 %d：%s" % (u, ln, msg))
    if orphan:
        print("  （清单不判死：token 匹配精度有限。但这些 [查] 在付印前要么补逐字原文，要么降 [推]）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
