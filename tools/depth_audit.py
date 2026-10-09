#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""depth_audit.py — v3 深度门：量化"讲到 FOC 那个水平没有"。

作者 2026-10-08 的标准是："磁场←电流←PWM 导通时间"这种一路问到"那这个又靠什么"
的链条。这个脚本把那条标准变成可机检的五个信号，对每章打分并列出短板。

五个信号（每章，按每千字归一）：
  A 追问链   —— 「那……又靠什么 / 为什么 / 凭什么 / 再往下 / 根子」句式的数量
  B 公式密度 —— 含 = 的行（去掉 markdown 表格、标题与代码块后的正文）
  C 底座词   —— 是否落到物理/器件层（磁场、洛伦兹、电子、电阻、熵、磁饱和…）
  D 边界句   —— 是否写了代价与失效条件（但、代价、不再、超出、饱和、上限、失效…）
  E 可代入数 —— 带单位的数，读者能自己复算
另外报告：机器狗/四足 与 人形 的相对提及，防止主题再次漂回四足。

自检：--selftest 用一段"已知厚"与一段"已知薄"的样本文本验证打分方向，
测不出差异的度量不许上岗（本项目已因指标虚高误判过一次）。

用法：
  python -X utf8 tools/depth_audit.py
  python -X utf8 tools/depth_audit.py --worst 8
  python -X utf8 tools/depth_audit.py --selftest
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CODE_FENCE = re.compile("^```.*$", re.M)

ASK_WORDS = [
    "又靠什么", "是靠什么", "为什么", "凭什么", "根子", "再往下", "往下追",
    "再挖", "下一层", "追到底", "追到根", "问题又来了", "那这个呢",
    # 第二版补：工程师式反问。第 06 章整章在追问（"这件事有没有更笨的做法？"
    # "那么步进电机呢"），但旧词表一个都不认，把一章好稿判成 9.20 分的薄稿。
    "有没有", "能不能", "行不行", "够不够", "值不值", "怎么办",
    "那么", "如果", "会不会", "凭什么不", "什么情况下", "多久",
    "多快", "多远", "多贵", "差多少",
]
BASE_WORDS = [
    # —— 电磁与器件（第一性原理层）——
    "磁场", "磁通", "洛伦兹", "安培", "楞次", "法拉第", "电子", "空穴", "定子",
    "转子", "绕组", "霍尔", "电阻", "电容", "电感", "MOSFET", "IGBT", "三极管",
    "PN 结", "半导体", "晶格", "声子", "熵", "自由能", "光速", "普朗克",
    "玻尔兹曼", "傅里叶", "奈奎斯特", "香农", "库仑", "焦耳", "摩擦角",
    "杨氏模量", "铁芯", "磁饱和", "涡流", "趋肤", "压电", "MEMS", "微分",
    "积分", "特征值", "雅可比", "协方差", "反电动势", "磁链", "铜损", "铁损",
    # —— 信号与总线（工程底层）——
    "差分", "共模", "阻抗", "终端电阻", "收发器", "位时间", "时钟", "抖动",
    "采样", "量化", "混叠", "信噪比", "带宽", "延迟", "丢包", "仲裁",
    "串行", "并行", "寄存器", "中断", "DMA", "缓存", "流水线", "地址",
    # —— 计算与学习（算力底层）——
    "浮点", "FP16", "FP8", "INT8", "矩阵乘", "算子", "参数量", "权重",
    "梯度", "损失", "收敛", "过拟合", "分布", "采样温度", "token",
    "显存", "内存带宽", "功耗", "频率", "核", "张量",
    # —— 力学与热学（机械底层）——
    "惯量", "力矩", "扭矩", "刚度", "阻尼", "谐振", "屈曲", "疲劳", "磨损",
    "润滑", "传动比", "角速度", "线速度", "重心", "支撑面", "摩擦圆",
    "导热", "热阻", "温升", "散热", "熔点", "退磁", "剩磁", "居里",
    # —— 度量与经济（可复算的账）——
    "单价", "成本", "工时", "良品率", "标定", "重复精度", "分辨率",
    "不确定度", "置信", "样本", "口径",
]
BOUND_WORDS = [
    "代价", "但是", "不再", "超出", "饱和", "上限", "失效", "崩溃", "会烧",
    "击穿", "撑不住", "不适用", "前提是", "假设了", "误差来自", "做不到",
    "换来的", "换来的是", "这个近似在",
]
NUM_UNIT = (
    r"N\[?·\u00b7\]?m|V|A|mH|uH|\u00b5H|nF|\u00b5F|uF|mF|\u03a9|ohm|rad/s|Hz|"
    r"kHz|MHz|GHz|mm|cm|kg|\u00b0C|℃|bps|Mbps|GB|TB|bit|rpm|ms|\u00b5s|ns|min|W|J"
)
RE_NUM_CN = re.compile(
    r"\d+(?:\.\d+)?\s*(?:万|千)?\s*"
    r"(?:牛[·]?米|毫牛|千牛|牛|安培|毫安|安|伏特|毫伏|伏|特斯拉|毫特|匝|赫兹|千赫|兆赫|"
    r"毫米|厘米|微米|米|千克|公斤|克|瓦|毫瓦|千瓦|焦耳|焦|摄氏度|转每分|转/分|"
    r"比特|字节|位|个百分点|小时|分钟|毫秒|微秒|纳秒|秒|次|台|档|级|元|万元|美元|"
    r"kWh|Wh|mAh|Ah|TOPS|GFLOPS|TFLOPS|km/h|m/s|%|倍)")
RE_ASK = re.compile("|".join(ASK_WORDS))
RE_BASE = re.compile("|".join(BASE_WORDS))
RE_BOUND = re.compile("|".join(BOUND_WORDS))
RE_NUM = re.compile(r"\d+(?:\.\d+)?\s*(?:" + NUM_UNIT + r")")
RE_EQ_LINE = re.compile(r"[A-Za-z\u4e00-\u9fff]\s*=")


def body_lines(text):
    body = CODE_FENCE.sub("", text)
    out = []
    for line in body.split(chr(10)):
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("#") or s.startswith(">"):
            continue
        out.append(line)
    return chr(10).join(out)


def audit_text(raw):
    body = body_lines(raw)
    han = len(re.findall(r"[\u4e00-\u9fff]", body))
    k = 1000.0 / max(han, 1)
    ask = len(RE_ASK.findall(body))
    eq = len([l for l in body.split(chr(10)) if RE_EQ_LINE.search(l)])
    base = len(RE_BASE.findall(body))
    bound = len(RE_BOUND.findall(body))
    nums = len(RE_NUM.findall(body)) + len(RE_NUM_CN.findall(body))
    score = (
        min(ask * k, 4) + min(eq * k, 4) + min(base * k, 4)
        + min(bound * k, 3) + min(nums * k, 3)
    )
    return {
        "han": han, "ask": ask, "eq": eq, "base": base, "bound": bound,
        "num": nums, "score": round(score, 2),
    }


def audit(path):
    raw = io.open(path, encoding="utf-8").read()
    d = audit_text(raw)
    d["unit"] = os.path.basename(os.path.dirname(path))
    d["dog"] = len(re.findall("机器狗|四足", raw))
    d["human"] = len(re.findall("人形", raw))
    d["weak"] = d["score"] < 9.0
    return d


THICK_SAMPLE = """
扭矩为什么正比于电流？因为导线在磁场里受力 F = B·I·l，力乘力臂就是扭矩。
那磁场又是靠什么？靠转子上的永磁体和定子绕组电流共同合成。
为什么定子电流能控制方向？因为三相电流在空间上互差 120°，合成矢量的方向
由每相导通的时间占比决定。改变导通时间，就合成了任意方向任意大小的磁场。
这里有个代价：PWM 频率越高开关损耗越大，P_sw 正比于 f_sw，铁芯也会提前饱和。
实测 k_t = 0.64 N·m/A，相电阻 0.16 Ω，电感 0.05 mH，电气时间常数 0.31 ms。
"""

THIN_SAMPLE = """
这一章介绍关节电机。关节电机是机器人的核心部件，性能非常重要。
宇树用了自己研发的电机，效果很好，行业领先。我们下一章继续讲减速器。
"""

# 附录 A（符号/术语/单位表）与附录 D（去哪继续学）按体例就不该有推导链，
# 排除在深度门外，否则门会被"该薄的章"污染。
EXCLUDE = {"unit-41", "unit-44"}


def selftest():
    a = audit_text(THICK_SAMPLE)
    b = audit_text(THIN_SAMPLE)
    ok = a["score"] > b["score"] + 3
    print("样本A（应厚）%.2f  样本B（应薄）%.2f  差 %.2f → %s" % (
        a["score"], b["score"], a["score"] - b["score"],
        "PASS" if ok else "FAIL：度量分不出厚薄，不许上岗"))
    print("  A: 追问%d 公式%d 底座%d 边界%d 数字%d" % (
        a["ask"], a["eq"], a["base"], a["bound"], a["num"]))
    print("  B: 追问%d 公式%d 底座%d 边界%d 数字%d" % (
        b["ask"], b["eq"], b["base"], b["bound"], b["num"]))
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    worst_n = None
    if "--worst" in args:
        worst_n = int(args[args.index("--worst") + 1])
    files = sorted(glob.glob(os.path.join(ROOT, "drafts", "unit-*", "draft.md")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in EXCLUDE]
    if not files:
        print("no drafts found")
        return 1
    rows = [audit(f) for f in files]
    print("%-9s %6s %5s %5s %6s %6s %5s %6s %7s" % (
        "unit", "汉字", "追问", "公式", "底座", "边界", "数字", "狗/人", "深度分"))
    for r in rows:
        flag = "  ← 薄" if r["weak"] else ""
        print("%-9s %6d %5d %5d %6d %6d %5d %5s/%-3s %7.2f%s" % (
            r["unit"], r["han"], r["ask"], r["eq"], r["base"], r["bound"],
            r["num"], r["dog"], r["human"], r["score"], flag))
    scores = sorted(r["score"] for r in rows)
    thinned = [r for r in rows if r["weak"]]
    print(chr(10) + "全书正文汉字 %d；深度分中位 %.2f；<9.0 的章 %d/%d" % (
        sum(r["han"] for r in rows), scores[len(scores) // 2],
        len(thinned), len(rows)))
    print("机器狗/四足提及 %d 次 vs 人形 %d 次" % (
        sum(r["dog"] for r in rows), sum(r["human"] for r in rows)))
    if thinned:
        print(chr(10) + "待加深（按分数升序）：")
        order = sorted(thinned, key=lambda r: r["score"])
        if worst_n:
            order = order[:worst_n]
        for r in order:
            miss = []
            if r["ask"] < 3:
                miss.append("追问链少")
            if r["eq"] < 3:
                miss.append("缺公式")
            if r["base"] < 4:
                miss.append("未落到底层器件/物理")
            if r["bound"] < 3:
                miss.append("没写边界与代价")
            if r["num"] < 4:
                miss.append("可代入的数少")
            print("  %s  %.2f  %s" % (r["unit"], r["score"],
                                      "、".join(miss) or "综合偏薄"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
