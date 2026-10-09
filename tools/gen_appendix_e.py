#!/usr/bin/env python3
"""tools/gen_appendix_e.py — 附录 E.3 的"已引用 URL 清单"由正文收集生成，不靠手抄。

为什么要有它（2026-10-08 第三轮独立审阅）：E.3 的标题写着"100 条"，实际粘了 117 行，
而且条目是从正文手抄过来的，抄的时候把中文注释也粘进 URL 里，出现了
`https://doc-cdn.unitree.com/11/248/en/11_248_en（G1` 这种**半截断的行尾**——
读者照着复制会拿到一个打不开的地址。清单自称"已引用"，就必须真的等于正文引用过的集合。

做法：从 drafts/（不含 E.3 这一块自己）、bible/、research/ 收集 http(s) 链接，
在第一个中文字符或全角标点处截断，去掉行尾英文标点，去重、字典序，重写 E.3 的代码块
和标题里的条数。**只重写这两处**，E 的其它小节（取法、查不到清单、冲突口径）是作者的判断，不碰。

不静默：正文里出现的、清单没收到的 → 加进去；清单里有、正文已经查不到的 → 删掉并逐条打印。
用法：python -X utf8 tools/gen_appendix_e.py [--dry] [--selftest]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFT = os.path.join(ROOT, "drafts", "unit-45", "draft.md")

URL_RE = re.compile(r"https?://[^\s<>\"'`\)\]\}，。、；：！？）】》”]+")
# URL 里第一个中文/全角字符就是正文注释的起点（宇树、CSDN 的链接本身不含中文）
CUT_RE = re.compile(r"[　-〿一-鿿＀-￯]")
TRAIL_RE = re.compile(r"[.,;:!?'\"\\]+$")

CORPUS_DIRS = ["drafts", "bible", "research"]


def clean(url: str) -> str:
    m = CUT_RE.search(url)
    if m:
        url = url[: m.start()]
    return TRAIL_RE.sub("", url)


def exclusion(url: str) -> str:
    """有些地址不该进"参考来源"清单：不是公开可回读的文献，而是读者自己机器的界面或程序接口。
    它们仍留在正文里，只是不冒充参考条目——排除必须显式，逐条打印，不许静默丢。"""
    host = re.split(r"://", url, 1)[-1].split("/", 1)[0].lower()
    path = "/" + url.split("/", 3)[3] if url.count("/") >= 3 else "/"
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", host) or host.startswith(
            ("127.", "10.", "192.168.", "172.16.", "169.254.", "localhost")):
        return "机器本机地址（读者自己的机器人，不是文献）"
    if host.startswith("api.") or path.startswith("/api/") or "/api/" in path[:12]:
        return "程序化接口（查询串里带条件，会随结果变，不是固定页面）"
    if "<" in url or ">" in url:
        return "带占位符的模板地址（要替换参数才能访问，本身打不开）"
    # 只排"根本不是某一页文档"的两种：裸主机名，和 raw 仓库的目录前缀（列目录用，不是文件）。
    # 注意不能顺手把所有以 / 结尾的地址都剔掉——egh0bww1.com/posts/.../、
    # mujoco.readthedocs.io/en/stable/computation/ 这类以 / 结尾的**是**能打开的页面
    # （2026-10-09 独立审稿实测 200），一刀切会误伤真引用。
    if path in ("/", ""):
        return "只有主机名没有路径（是站点首页，不是某一页文献）"
    if host == "raw.githubusercontent.com" and path.endswith("/"):
        return "仓库目录前缀（raw 只发文件，列目录的地址打不开）"
    return ""


def collect() -> tuple[set[str], dict[str, str], dict[str, str]]:
    """返回 (进清单的 URL, 每个 URL 的第一处出处, 被排除的 URL→理由)。"""
    found: dict[str, str] = {}
    skip_self = False
    for d in CORPUS_DIRS:
        for p in sorted(glob.glob(os.path.join(ROOT, d, "**", "*.md"), recursive=True)):
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            in_e3 = False
            for raw in io.open(p, encoding="utf-8", errors="replace").read().split("\n"):
                if raw.startswith("## E.3"):
                    in_e3 = True          # E.3 自己粘的清单不算"正文引用"
                elif raw.startswith("## ") and in_e3:
                    in_e3 = False
                if in_e3:
                    continue
                for m in URL_RE.finditer(raw):
                    u = clean(m.group(0))
                    if len(u) > 12:
                        found.setdefault(u, rel)
    keep = {u: s for u, s in found.items() if not exclusion(u)}
    skip = {u: exclusion(u) for u in found if exclusion(u)}
    return set(keep), keep, skip


def section(lines: list[str]) -> tuple[int, int, int]:
    """E.3 的 (标题行号, ```text 开栏, 闭栏)。"""
    hi = next(i for i, l in enumerate(lines) if l.startswith("## E.3"))
    nxt = next((i for i in range(hi + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    try:
        open_i = next(i for i in range(hi + 1, nxt) if lines[i].startswith("```"))
    except StopIteration:
        raise SystemExit("E.3 里没有代码块，生成器不知道往哪写")
    close_i = next(i for i in range(open_i + 1, nxt) if lines[i].startswith("```"))
    return hi, open_i, close_i


def parse_list(lines: list[str], open_i: int, close_i: int) -> set[str]:
    out = set()
    for l in lines[open_i + 1: close_i]:
        m = URL_RE.search(l)
        if m:
            out.add(clean(m.group(0)))
    return out


def render(urls: set[str]) -> list[str]:
    return sorted(urls)


def build(lines: list[str], urls: set[str], n_skipped: int = 0) -> tuple[list[str], list[str], list[str]]:
    hi, open_i, close_i = section(lines)
    old = parse_list(lines, open_i, close_i)
    added = sorted(urls - old)
    dropped = sorted(old - urls)
    out = lines[: open_i + 1] + render(urls) + lines[close_i:]
    # 标题里的条数跟着实际清单走（原来是手写的 100，与实际的 117 不符）
    if not re.search(r"（\d+ 条", out[hi]):
        raise SystemExit("E.3 标题里没有『（N 条…）』，生成器不猜该往哪写条数")
    out[hi] = re.sub(r"（\d+ 条", f"（{len(urls)} 条", out[hi])
    # 作者写的"另有 N 条按规则不进这张表"里，只有 N 是机器产物
    out = [re.sub(r"另有 \*\*\d+ 条\*\*", f"另有 **{n_skipped} 条**", l)
           if l.startswith("另有 **") else l for l in out]
    return out, added, dropped


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    urls, srcs, skipped = collect()
    lines = io.open(DRAFT, encoding="utf-8").read().rstrip("\n").split("\n")
    new, added, dropped = build(lines, urls, len(skipped))
    print("正文里可回读的 URL：%d 条进清单，%d 条按规则排除（drafts + bible + research）"
          % (len(urls), len(skipped)))
    for u, why in sorted(skipped.items()):
        print("  · 排除 %s —— %s" % (u, why))
    if added:
        print("清单缺失、已补入 %d 条：" % len(added))
        for u in added:
            print("  + %s   ← %s" % (u, srcs.get(u, "?")))
    if dropped:
        print("清单里有、正文已经查不到 %d 条（已移出，若仍要引用请在正文里给出出处）：" % len(dropped))
        for u in dropped:
            print("  - %s" % u)
    if not added and not dropped:
        print("E.3 与正文引用集合一致 ✓")
    if "--dry" in sys.argv:
        print("dry-run：%d 行 → %d 行" % (len(lines), len(new)))
        return 0
    io.open(DRAFT, "w", encoding="utf-8", newline="\n").write("\n".join(new) + "\n")
    return 0


def selftest() -> int:
    corpus = "看 https://example.com/a（这是中文注释） 与 https://example.org/b，还有 https://ex.io/c."
    urls = {clean(m.group(0)) for m in URL_RE.finditer(corpus)}
    fixture = [
        "## E.3 已引用的 URL 清单（100 条，按字典序）",
        "",
        "另有 **0 条**正文里出现的地址按规则**不进这张表**，因为它们不是文献。",
        "",
        "```text",
        "https://example.com/a（这是中文注释）",
        "https://example.org/ghost-only-in-appendix",
        "```",
        "",
        "## E.4 「查不到」清单",
        "作者的话，不许动。",
    ]
    new, added, dropped = build(fixture, urls, 2)
    body = "\n".join(new)
    oi = new.index("```text")
    ci = new.index("```", oi + 1)
    listed = new[oi + 1: ci]
    block = "\n".join(new[oi:ci])
    checks = [
        ("正文有而清单没有的被补入", "https://ex.io/c" in body and "https://ex.io/c" in added),
        ("清单有而正文查不到的被移出", "ghost-only-in-appendix" not in body
         and "https://example.org/ghost-only-in-appendix" in dropped),
        ("粘进 URL 的中文注释被截掉", "https://example.com/a" in listed and "（这是中文注释）" not in block),
        ("标题的条数改成实际值", "（%d 条" % len(urls) in new[0] and "100 条" not in new[0]),
        ("作者写的排除说明保留，只有条数被换算", "因为它们不是文献" in body and "另有 **2 条**" in body),
        ("E.4 之后的小节一个字没动", "作者的话，不许动。" in body and "## E.4" in body),
        ("行尾英文句号被清掉", "https://ex.io/c." not in body),
        ("清单按字典序且无重复", listed == sorted(set(listed))),
        ("机器本机地址被排除规则抓到", bool(exclusion("https://192.168.123.164:60001"))),
        ("程序化接口被排除规则抓到", bool(exclusion("https://api.github.com/search/repositories?q=1"))),
        ("普通厂商页面不会被误排除", exclusion("https://www.st.com/en/mcu/stm32h743ai.html") == ""),
    ]
    bad = 0
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
        bad += 0 if ok else 1
    print("自检 %d/%d" % (len(checks) - bad, len(checks)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
