#!/usr/bin/env python3
"""tools/gen_appendix_b.py — 附录 B 里那四块"跑出来的东西"，真的由脚本重写。

为什么要有它（2026-10-08 第三轮独立审阅）：附录 B 开头自称"由脚本自动生成、不要手改"，
**而仓库里当时没有这个脚本**。结果 B.2 只誊了 10 条自检（脚本已打 19 条）、B.4 写"概念 150 个"
（check_kg 报 158）、B.5 又写 146。承诺了却做不到的清单，比讲错一个数更伤信任。
现在把承诺兑现：这个脚本就是 B 声称的那个生成器。

边界（重要）：只重写**机器产物**——B.2/B.3/B.4 的四个 ```text 块、B.5 表里的概念数、
B.6 的用例条数与用例名清单、以及开头的生成日期。作者写的判断、用途边界、口径说明
（B.1、B.3 的表格与"这…行的用途边界"、B.6 的"四次算错"段）一个字都不碰。

不静默丢行：arithmetic_check 的每一行输出都必须被分到"论证链 / 对照数据 / 缺数脚注"三组之一，
出现未知行头就失败退出——否则以后加一行会在这里无声消失（本项目已因"0 图却不报错"翻过车）。
用法：python -X utf8 tools/gen_appendix_b.py [--dry] [--selftest]
"""
from __future__ import annotations

import datetime
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAFT = os.path.join(ROOT, "drafts", "unit-42", "draft.md")
PY = [sys.executable, "-X", "utf8"]

# B.3 的两块按"这一行吃的是哪个输入块"分组，不是按函数名分组：
# 人形自身可算的量 + 通用器件进论证链；Go2/AS2 那几行只是第 16 章的对照与器件史料。
COMPARE_HEADS = (
    "resolution_vs_backlash(Go2",
    "reverse_cot",
    "torque_chain",
    "energy_chain",
    "frequency_chain",
)
FOOTER_HEADS = ("缺数", "  TBD")
GEN_DATE_RE = re.compile(r"生成时间：\d{4}-\d{2}-\d{2}")


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", timeout=900)
    # arithmetic_check --demo 用 exit 1 表示"还有数没测"（TBD），不是算错；
    # 这里按 stdout 是否有内容判生死，退出码交给下层的门。
    if not (r.stdout or "").strip():
        raise SystemExit(f"生成器拒绝写入空输出：{' '.join(cmd)}（rc={r.returncode}）\n{r.stderr[:400]}")
    return r.stdout


def fence_at(lines: list[str], heading_prefix: str, nth: int = 1,
             stop_prefix: str | None = None) -> int:
    """返回 heading 之后第 nth 个 ```text 开栏的行号。"""
    hi = next(i for i, l in enumerate(lines) if l.startswith(heading_prefix))
    seen = 0
    for i in range(hi + 1, len(lines)):
        if stop_prefix and lines[i].startswith(stop_prefix):
            break
        if lines[i].startswith("```text"):
            seen += 1
            if seen == nth:
                return i
    raise SystemExit(f"找不到 {heading_prefix} 之后第 {nth} 个 ```text 块")


def replace_block(lines: list[str], open_idx: int, body: list[str]) -> list[str]:
    close = next(i for i in range(open_idx + 1, len(lines)) if lines[i].startswith("```"))
    return lines[: open_idx + 1] + body + lines[close:]


def split_arithmetic(out: str) -> tuple[list[str], list[str]]:
    """把 --demo 输出按用途分成（论证链行, 对照行含脚注），并证明每一行都被分到组。"""
    main: list[str] = []
    comp: list[str] = []
    unknown = []
    for line in out.rstrip("\n").split("\n"):
        if not line.strip():
            continue
        if line.startswith(COMPARE_HEADS) or line.startswith(FOOTER_HEADS):
            comp.append(line)
        elif line.startswith(("selfcheck:", "bus_budget", "resolution_vs_backlash(", "latency_chain")):
            main.append(line)
        else:
            unknown.append(line)
    if unknown:
        raise SystemExit("arithmetic_check 出现了没登记过的输出行，生成器不会把它静默丢掉：\n  "
                         + "\n  ".join(x[:120] for x in unknown)
                         + "\n请在 gen_appendix_b.py 的分组表里决定它属于论证链还是对照数据。")
    return main, comp


def selfcheck_cases(foc_out: str) -> tuple[int, int, list[str]]:
    """从 foc_check 的 === selfcheck === 段里取出用例名，返回 (总条数, 负对照条数, 名字)。"""
    m = re.search(r"=== selfcheck ===\n(.*?)(?=\n\n?=== )", foc_out, re.S)
    if not m:
        raise SystemExit("foc_check 没有 === selfcheck === 段，B.6 无法核对")
    names = []
    neg = 0
    for line in m.group(1).split("\n"):
        t = re.match(r"^\s*(ok|FAIL|PASS)\s+(.*)$", line)
        if not t:
            continue
        name = re.split(r"[:：]", t.group(2), 1)[0].strip()
        names.append(name)
        if "必须不被接受" in line:
            neg += 1
    return len(names), neg, names


def arithmetic_selfcheck(out: str) -> int:
    m = re.search(r"selfcheck:\s*(\d+)/(\d+)", out)
    if not m or m.group(1) != m.group(2):
        raise SystemExit("arithmetic_check 自检没有全对，B.6 拒绝抄一个失败的数")
    return int(m.group(1))


def concept_count(kg_out: str) -> tuple[int, int, str]:
    total = re.search(r"概念\s*(\d+)\s*个", kg_out)
    orphan = re.search(r"未被任何章引入的概念\s*(\d+)\s*个", kg_out)
    spread = re.search(r"分布在\s*(\d+/\d+)\s*章", kg_out)
    if not total or not orphan or not spread:
        raise SystemExit("check_kg 的输出格式变了，生成器看不懂，拒绝写附录 B")
    return int(total.group(1)), int(orphan.group(1)), spread.group(1)


def build(new: list[str], foc: str, ar: str, kg: str) -> list[str]:
    n_concepts, n_orphan, spread = concept_count(kg)
    n_cases, n_neg, names = selfcheck_cases(foc)
    ar_cases = arithmetic_selfcheck(ar)
    main, comp = split_arithmetic(ar)

    # B.2 = foc_check 全文（自检 + 逐条推算 + 结论），一字不改
    new = replace_block(new, fence_at(new, "## B.2"), foc.rstrip("\n").split("\n"))
    # B.3 = 两块分组誊抄：先论证链，再对照数据
    i1 = fence_at(new, "## B.3", 1, stop_prefix="## B.4")
    new = replace_block(new, i1, main)
    i2 = fence_at(new, "## B.3", 2, stop_prefix="## B.4")
    new = replace_block(new, i2, comp)
    # B.4 = check_kg 全文
    new = replace_block(new, fence_at(new, "## B.4"), kg.rstrip("\n").split("\n"))

    # B.5 表里那一格的概念数
    hits = [i for i, l in enumerate(new) if "knowledge-graph.yaml" in l and "个概念" in l]
    if len(hits) != 1:
        raise SystemExit(f"B.5 的 knowledge-graph 行应有 1 处，找到 {len(hits)}：不猜改哪一行")
    new[hits[0]] = re.sub(r"\d+ 个概念", f"{n_concepts} 个概念", new[hits[0]])

    # B.6：整个小节是机器产物（作者写的"四次算错"那段在下面原样保留）
    hi = next(i for i, l in enumerate(new) if l.startswith("## B.6"))
    tail = new[hi + 1:]
    keep_from = next((i for i, l in enumerate(tail) if l.startswith("**")), len(tail))
    # 护栏：B.6 抬头之后必须还剩作者写的东西。2026-10-09 独立审稿用变异测试发现，
    # 这一段是"整段重写"，若作者在它后面插一段不带 ** 的正文，就会被吞掉且不报警。
    # 现在要求尾部至少剩 3 个非空行，且首行仍以 ** 开头——被吞掉时这里直接失败。
    rest = [l for l in tail[keep_from:] if l.strip()]
    if keep_from >= len(tail) or not tail[keep_from].startswith("**") or len(rest) < 3:
        raise SystemExit(
            "B.6 小节里作者写的段落少于 3 行（实得 %d）——生成器会整段重写抬头，"
            "这道护栏防止它顺手吞掉后面的正文" % len(rest))
    total_cases = n_cases + ar_cases
    auto = [
        "",
        f"`foc_check.py selfcheck()` 当前含 **{n_cases} 条**已知答案用例"
        + (f"（其中 {n_neg} 条是负对照：故意把错答案喂进去，要求它**不被接受**）" if n_neg else "")
        + f"；`arithmetic_check.py selfcheck()` 另含 **{ar_cases} 条**。合计 {total_cases} 条，"
        + "逐条名字由脚本从输出里取出：",
        "",
    ]
    line, rows = "", []
    for nm in names:
        cand = (line + "、" + nm) if line else nm
        if len(cand) > 62:
            rows.append(line)
            line = nm
        else:
            line = cand
    if line:
        rows.append(line)
    auto += ["`" + r + "`" for r in rows]
    auto += ["", f"（check_kg 侧另有 {n_concepts} 个概念、{n_orphan} 个未被任何章引入。）", ""]
    new = new[: hi + 1] + auto + tail[keep_from:]
    # 作者那句"这 13 条用例已经抓到过…"里的条数也是机器产物，只换数字不动句子
    new = [re.sub(r"这 \d+ 条用例已经抓到", f"这 {total_cases} 条用例已经抓到", l) for l in new]

    # 生成日期
    new = [GEN_DATE_RE.sub(f"生成时间：{datetime.date.today().isoformat()}", l) for l in new]
    return new


def check_markers(old: list[str], new: list[str]) -> None:
    """机器块之外的**标题行与白名单前缀行**不许变化。

    注意它的边界：只锁标题、表格行、`**这`、`本书的写作纪律`、`> `、`（注意` 这几类开头，
    不是逐字看守全部正文（附录 B 开头那句声明已按这个边界如实写）。"""
    def prose(ls):
        return [l for l in ls if l.startswith("#") and not l.startswith("# 附录")]
    if prose(old) != prose(new):
        raise SystemExit("小节标题被改动，生成器越界了")
    # 四块之外的中文正文行必须一字不差。允许被改的只有两处，且都只是数字：
    #   ① "> 生成时间：…"（日期戳）② B.5 表里 knowledge-graph 那一格的概念数。
    # B.6 那句"这 N 条用例已经抓到"的 N 也算第三处。别的任何字变了就是越界。
    def body(ls):
        return [l for l in ls
                if l.startswith(("|", "**这", "本书的写作纪律", "> ", "（注意"))
                and "条用例已经抓到" not in l
                and "生成时间" not in l
                and "knowledge-graph.yaml" not in l]
    if body(old) != body(new):
        raise SystemExit("生成器改动了作者写的正文，越界")


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    foc = run(PY + ["code/tools/foc_check.py"])
    ar = run(PY + ["code/tools/arithmetic_check.py", "--demo"])
    kg = run(PY + ["tools/check_kg.py"])
    old = io.open(DRAFT, encoding="utf-8").read().rstrip("\n").split("\n")
    new = build(list(old), foc, ar, kg)
    check_markers(old, new)
    sizes = {}
    for h in ("## B.2", "## B.3", "## B.4", "## B.6"):
        def block(ls):
            try:
                hi = next(i for i, l in enumerate(ls) if l.startswith(h))
            except StopIteration:
                return 0
            stop = next((i for i in range(hi + 1, len(ls)) if ls[i].startswith("## ")), len(ls))
            return stop - hi
        sizes[h] = (block(old), block(new))
    if "--dry" in sys.argv:
        print("dry-run：%d 行 → %d 行；各小节行数（旧→新）%s" % (len(old), len(new), sizes))
        return 0
    io.open(DRAFT, "w", encoding="utf-8", newline="\n").write("\n".join(new) + "\n")
    n_c, _, _ = selfcheck_cases(foc)
    print("附录 B 已重写：%d 行 → %d 行；foc 自检 %d 条、arithmetic 自检 %d 条、概念 %d 个"
          % (len(old), len(new), n_c, arithmetic_selfcheck(ar), concept_count(kg)[0]))
    return 0


def selftest() -> int:
    """负对照：把一个已知过期的小块喂进 build()，要求它被换成实际输出。"""
    n_cases, n_neg, names = selfcheck_cases(RUN_FOC)
    ar = RUN_AR
    kg = RUN_KG
    fixture = [
        "# 附录 B：全书可复算的数",
        "> 生成时间：2026-01-01",
        "## B.2 第 1 部（一颗关节）与第 2–5 部的推算链",
        "```text",
        "这里是一条早就过期的誊抄",
        "```",
        "## B.3 主算例（人形）与对照数据（arithmetic_check）",
        "**用于本书论证链的行（人形与通用器件；第一行是脚本自检的抬头）**",
        "```text",
        "过期",
        "```",
        "**对照数据（四足产品：只作第 16 章的能量对照与关节器件的史料，非本书解剖对象，不进任何一章的解剖链）**",
        "```text",
        "过期",
        "```",
        "**这五行的用途边界**：作者的话，一个字都不许动。",
        "## B.4 概念依赖与术语预算校验（check_kg）",
        "```text",
        "概念 150 个，分布在 43/46 章",
        "```",
        "## B.5 输入数据表的位置",
        "| 概念依赖图 | `bible/knowledge-graph.yaml` | 146 个概念，v3 人形编号 |",
        "## B.6 自检用例（防脚本自己算错）",
        "旧的一条描述",
        "**这 13 条用例已经抓到过作者本人的四次算错**（CoT 量纲、kg 与 N 混用、参考角）。",
        "这就是本书坚持工具也要被测的理由。",
        "第二段作者的话，也必须活着跑过生成器。",
    ]
    new = build(list(fixture), RUN_FOC, ar, kg)
    joined = "\n".join(new)
    ok1 = "这里是一条早就过期的誊抄" not in joined and "=== selfcheck ===" in joined
    ok2 = "概念 150 个" not in joined and f"概念 {concept_count(kg)[0]} 个" in joined
    ok3 = "146 个概念" not in joined and f"{concept_count(kg)[0]} 个概念" in joined
    ok4 = ("作者的话，一个字都不许动。" in joined and "条用例已经抓到" in joined
           and "也必须活着跑过生成器。" in joined and "这就是本书坚持工具也要被测的理由。" in joined)
    ok5 = "生成时间：2026-01-01" not in joined
    ok6 = "旧的一条描述" not in joined
    ok7 = len(names) == n_cases and f"含 **{n_cases} 条**" in joined
    checks = [
        ("B.2 过期誊抄被换成脚本实际输出", ok1),
        ("B.4 概念 150 被换成实际值", ok2),
        ("B.5 的 146 被换成实际值", ok3),
        ("作者的话与 B.6 的编辑段保留", ok4),
        ("B.6 过期的描述段被重新生成", ok6),
        ("生成日期刷新", ok5),
        (f"B.6 写出实际用例条数 {n_cases}", ok7),
    ]
    # 未知行头必须被拒绝
    try:
        split_arithmetic(RUN_AR + "\nsome_new_function 新加的\n")
        ok8 = False
    except SystemExit:
        ok8 = True
    checks.append(("arithmetic_check 新增未知行会被拒绝而不是静默丢弃", ok8))
    bad = 0
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
        bad += 0 if ok else 1
    check_markers(fixture, new)
    print("自检 %d/%d" % (len(checks) - bad, len(checks)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        RUN_FOC = run(PY + ["code/tools/foc_check.py"])
        RUN_AR = run(PY + ["code/tools/arithmetic_check.py", "--demo"])
        RUN_KG = run(PY + ["tools/check_kg.py"])
    sys.exit(main())
