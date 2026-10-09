#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/make_figs3.py — 补四张"方法层"与第 11/19/26 章的图。

为什么补这四张：
  F-04-1 是全书的"深度尺"——把作者要求的那句"每一跳再问一次那这个又靠什么"
         画成一张可指认的图，读者拿它去量后面每一章。
  F-11-1 补 d-q 平面：第 11 章讲 i_q 管扭矩、i_d 管磁场，没有正交分解图就只能在文字里绕。
  F-19-1 补"可编程弹簧"：刚度是软件写的，必须把 k_p 与 ω_n 画在同一张图上。
  F-26-1 补内存墙：大脑只有几 Hz 的原因不是算得慢，是读得慢。

版式纪律（第一版四张图全部因文字压字返工，规则写在这里）：
  · 顶部说明一律拆两行，单行显示宽度 ≤ 55 个汉字当量。
  · 右侧文字块从 x=600 起，单行 ≤ 21 个汉字当量，行距 24。
  · 宽度用 wrap() 量出来，不靠肉眼估；ASCII 连续段当一个 token 不拆断。
  · 图内不写"图 NN-1"标题（图题由 outline/figures.yaml 的 caption 承载）。
"""
from __future__ import annotations

import math
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from make_figs import Fig, INK, GREY, LIGHT, ACC, RED, GREEN, MONO, SERIF  # noqa: E402


def wlen(s):
    """显示宽度，以汉字=1、ASCII=0.55 计（16 px 字号下的粗略当量）。"""
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s)


def tokens(s):
    out, i = [], 0
    while i < len(s):
        m = re.match(r"[0-9A-Za-z_\.\+\-/%=()·\*]+", s[i:])
        if m:
            out.append(m.group(0))
            i += len(m.group(0))
        else:
            out.append(s[i])
            i += 1
    return out


def wrap(s, maxw):
    """按显示宽度折行；先按空格断，再按 token 硬断。"""
    lines, cur = [], ""
    for tk in tokens(s):
        if tk == " ":
            cand = cur + " "
        else:
            cand = cur + tk
        if wlen(cand.strip()) > maxw and cur.strip():
            lines.append(cur.strip())
            cur = tk if tk != " " else ""
        else:
            cur = cand
    if cur.strip():
        lines.append(cur.strip())
    return lines


def para(f, x, y, s, maxw, cls="s", dy=22, **kw):
    for ln in wrap(s, maxw):
        f.text(x, y, ln, cls=cls, **kw)
        y += dy
    return y


# ══════════════════════════════════════════════════════════ F-04-1 深度尺
def f04_depth_ruler():
    f = Fig(1000, 500)
    f.head()
    y = para(f, 30, 34, "本书的挖法：从任意一层往下问“那这个又靠什么”，问到不能再问为止。"
             "下面五层是全书骨架，箭头下面的问句就是每一章的正文。", 55, dy=24)

    layers = [
        ("任务层", ["抓住那只杯子"], "1–10 Hz"),
        ("轨迹层", ["手指 60 mm/s"], "50–200 Hz"),
        ("力矩层", ["τ = 12 N·m"], "1 kHz"),
        ("电流层", ["i_q = 18.8 A"], "10–20 kHz"),
        ("器件层", ["高侧管导通", "37 %"], "40 kHz PWM"),
    ]
    bw, gap, x0 = 176, 6, 40
    top = 108
    for i, (name, wants, rate) in enumerate(layers):
        x = x0 + i * (bw + gap)
        f.rect(x, top, bw, 104, stroke=ACC if i < 4 else RED,
               fill="#fbf4f4" if i == 0 else "#f4f7fb")
        f.text(x + bw / 2, top + 28, name, cls="h", anchor="middle")
        f.text(x + bw / 2, top + 56, wants[0], cls="m", anchor="middle")
        if len(wants) > 1:
            f.text(x + bw / 2, top + 76, wants[1], cls="m", anchor="middle")
        f.text(x + bw / 2, top + 94, "刷新 " + rate, cls="tiny", anchor="middle")
        if i < 4:
            f.arrow(x + bw + 1, top + 52, x + bw + gap - 1, top + 52, w=2)

    qs = ["那『抓』靠什么", "轨迹靠什么执行", "12 N·m 靠什么", "电流谁来调"]
    ans = [
        ["靠关节把扭矩送到", "指腹，不是靠", "“用力”这个字"],
        ["靠每个关节给一条", "扭矩指令，", "不是给位置"],
        ["靠垂直于转子的", "磁场：τ = k_t·i_q", "（第 05、11 章）"],
        ["靠改 MOSFET 导通", "时间：伏秒平衡", "（第 08 章）"],
    ]
    for i in range(4):
        cx = x0 + (i + 1) * (bw + gap) - bw / 2 - gap / 2 + 4
        f.text(cx, 246, qs[i], cls="s", anchor="middle", fill=RED)
        f.line(cx, 256, cx, 278, stroke=RED, w=1, dash="4 4")
        for j, ln in enumerate(ans[i]):
            f.text(cx, 300 + j * 22, ln, cls="s", anchor="middle")

    f.line(40, 386, 960, 386, stroke=LIGHT, w=2)
    f.text(40, 414, "问到底的四块地砖（全书所有推算最终落在这里）：", cls="t")
    floors = [
        "τ = k_t·i　洛伦兹力 F = B·I·ℓ，力臂换成扭矩",
        "τ = m × B　只有垂直分量出力，sinθ 定大小与方向",
        "伏秒平衡　改导通时间 = 改平均电压 = 合成任意矢量",
        "香农 / 奈奎斯特　信息与控制带宽的下限，省不掉",
    ]
    for i, t in enumerate(floors):
        f.text(40 + (i % 2) * 470, 444 + (i // 2) * 26, "· " + t, cls="s")
    f.save("f04-depth-ruler.svg")


# ══════════════════════════════════════════════════════════ F-11-1 d-q 平面
def f11_dq_plane():
    f = Fig(1000, 590)
    f.head()
    para(f, 30, 34, "定子电流矢量被拆成两个互相垂直的分量：q 轴那一份出扭矩，"
         "d 轴那一份只改磁场。这一步是纯数学旋转，不耗能——它只是换了一双眼睛"
         "看同一组三相电流。", 55, dy=24)

    cx, cy, R = 250, 320, 148
    f.arrow(cx - R - 34, cy, cx + R + 30, cy, stroke=GREY, w=1)
    f.arrow(cx, cy + R + 34, cx, cy - R - 30, stroke=GREY, w=1)
    f.text(cx + R + 34, cy - 8, "d 轴", cls="s", fill=GREY)
    f.text(cx + 8, cy - R - 34, "q 轴", cls="s", fill=GREY)
    f.circle(cx, cy, R, stroke=ACC, w=2)
    r2 = 92
    f.path("M %d,%d a %d,%d 0 1,0 %d,0 a %d,%d 0 1,0 %d,0" % (
        cx - r2, cy, r2, r2, 2 * r2, r2, r2, -2 * r2), stroke=RED, w=2, dash="7 6")

    beta = math.radians(64)
    px, py = cx + R * math.cos(beta), cy - R * math.sin(beta)
    f.arrow(cx, cy, px, py, w=3)
    f.text(px + 10, py - 6, "i_s", cls="t")
    f.line(px, py, px, cy, stroke=GREEN, w=1, dash="5 4")
    f.line(px, py, cx, py, stroke=RED, w=1, dash="5 4")
    f.arrow(cx, cy, px - 6, cy, stroke=GREEN, w=2)
    f.arrow(cx, cy, cx, py + 6, stroke=RED, w=2)
    f.circle(cx, cy, 4, fill=INK, stroke=INK)

    # 标注一律放到圆外，用虚线引到被指的那条线
    f.text(46, 176, "电流极限圆", cls="s", fill=ACC)
    f.text(46, 198, "|i_s| ≤ I_max", cls="m", fill=ACC)
    f.text(46, 220, "由发热决定", cls="tiny", fill=GREY)
    f.line(150, 206, cx - 104, cy - 100, stroke=ACC, w=1, dash="3 3")
    f.text(46, 470, "电压极限圆：转速一高就收缩", cls="s", fill=RED)
    f.line(150, 458, cx - 62, cy + 68, stroke=RED, w=1, dash="3 3")
    f.text(cx + R + 40, cy + 30, "i_q 出扭矩", cls="s", fill=GREEN)
    f.text(cx - 16, (cy + py) / 2, "i_d", cls="s", fill=RED, anchor="end")
    f.text(46, 506, "β = atan2(i_d, i_q)：最大扭矩每安培角", cls="tiny")

    rx = 600
    f.text(rx, 150, "表贴式（L_d = L_q）", cls="t")
    f.text(rx, 178, "τ = 1.5 · p · λ_m · i_q", cls="m")
    para(f, rx, 206, "⇒ 扭矩只由 i_q 决定，i_d 不出力。", 21, dy=22)
    f.text(rx, 254, "代入 GO-M8010-6", cls="t")
    f.text(rx, 282, "k_t = 23.7 ÷ 40 = 0.64 N·m/A", cls="m")
    para(f, rx, 310, "⇒ 要 12 N·m 就给 i_q ≈ 18.8 A；"
         "这 18.8 A 与转速无关，只与是否垂直有关。", 21, dy=22)
    f.line(rx, 380, 960, 380, stroke=LIGHT, w=2)
    f.text(rx, 408, "内置式（IPM）多一项磁阻扭矩", cls="t")
    f.text(rx, 436, "τ = 1.5 p [λ_m i_q", cls="m")
    f.text(rx, 460, "　　　+ (L_d − L_q) i_d i_q]", cls="m")
    para(f, rx, 488, "⇒ 负的 i_d 反而加扭矩，这才是 MTPA 角不为零的原因。", 21, dy=22)
    para(f, rx, 540, "代价：电压极限圆把电流圆吞掉时，只能加大负 i_d 削弱磁场（弱磁），"
         "用发热换转速。人形关节不需要超基速，所以几乎不用弱磁。", 21, dy=22)
    f.save("f11-dq-plane.svg")


# ══════════════════════════════════════════════════════════ F-19-1 可编程弹簧
def f19_programmable_spring():
    f = Fig(1000, 470)
    f.head()
    para(f, 30, 34, "同一个电机，改三个数就换一种“材质”。物理上没有任何东西被换掉，"
         "换掉的是误差到扭矩的映射——刚度是软件写的。", 55, dy=24)

    # 左：机械类比（画在 40–430 的带里）
    wall = 70
    f.text(40, 96, "它等效于这样一根弹簧", cls="t")
    f.line(wall, 120, wall, 300, stroke=INK, w=3)
    for i in range(11):
        f.line(wall - 12, 128 + i * 17, wall, 120 + i * 17, stroke=INK, w=1)
    pts = [(wall, 168)]
    for i in range(9):
        pts.append((wall + 16 + i * 10, 168 + (13 if i % 2 == 0 else -13)))
    pts.append((wall + 16 + 9 * 10, 168))
    d = "M %.1f,%.1f" % pts[0] + "".join(" L %.1f,%.1f" % p for p in pts[1:])
    f.path(d, stroke=INK, w=2)
    f.text(wall + 20, 132, "k_p（刚度）", cls="s")
    bx = wall + 126
    f.line(wall + 16 + 9 * 10, 168, bx + 84, 168, stroke=INK, w=2)   # 弹簧 → 质量块
    f.line(wall, 250, bx, 250, stroke=INK, w=2)                      # 墙 → 阻尼
    f.line(bx, 250, bx + 26, 250, stroke=INK, w=2)
    f.rect(bx + 26, 236, 32, 28, stroke=INK, rx=2)
    f.line(bx + 58, 250, bx + 84, 250, stroke=INK, w=2)
    f.line(bx + 42, 236, bx + 42, 216, stroke=INK, w=2)
    f.text(bx - 4, 208, "k_d（阻尼）", cls="s")
    f.rect(bx + 84, 150, 66, 140, stroke=ACC, fill="#f4f7fb")
    f.text(bx + 117, 226, "J", cls="t", anchor="middle")
    f.text(bx + 117, 312, "负载惯量", cls="s", anchor="middle")
    f.arrow(bx + 156, 220, bx + 214, 220, stroke=RED, w=2)
    f.text(bx + 185, 206, "外力", cls="s", fill=RED, anchor="middle")
    f.text(40, 344, "推它，它让；撤力，它回。让多少、回多快，全由 k_p 与 k_d 说了算。", cls="tiny")

    # 右：公式与三档对照
    mx = 500
    f.text(mx, 96, "控制器里真正跑的式子（宇树口径：一条混合公式）", cls="t")
    f.text(mx, 126, "τ = τ_ff + k_p (q_des − q) + k_d (ω_des − ω)", cls="m")
    para(f, mx, 154, "位置误差 → 乘 k_p → 直接变扭矩，中间没有独立的位置环。", 24, dy=22)
    f.line(mx, 184, 960, 184, stroke=LIGHT, w=2)
    f.text(mx, 212, "为什么“软”和“硬”是同一台机器", cls="t")
    cols = [
        ("想要", "擦桌子", "端住水杯", "敲键抓抛"),
        ("k_p", "几十", "一两百", "数百"),
        ("被推", "让很多", "让一点", "几乎不让"),
        ("回位", "慢", "快", "立刻顶回"),
        ("代价", "误差大", "谐振余量", "齿隙放大"),
    ]
    cw = 118
    for r, row in enumerate(cols):
        yy = 244 + r * 26
        f.text(mx, yy, row[0], cls="s", fill=GREY)
        for j in range(3):
            f.text(mx + 96 + j * cw, yy, row[j + 1], cls="s")
    f.text(mx + 96, 382, "软", cls="s", fill=GREEN)
    f.text(mx + 96 + cw, 382, "中", cls="s", fill=GREY)
    f.text(mx + 96 + 2 * cw, 382, "硬", cls="s", fill=RED)

    f.line(40, 404, 960, 404, stroke=INK, w=2)
    f.text(40, 430, "上限从哪来：ω_n = √(k_p / J)。刚度翻 4 倍，固有频率只翻 2 倍；", cls="s")
    f.text(40, 452, "但它很快会撞上编码器分辨率、齿隙与 1 kHz 采样——撞上就是振荡。（第 12、14 章）", cls="s")
    f.save("f19-programmable-spring.svg")


# ══════════════════════════════════════════════════════════ F-26-1 内存墙
def f26_memory_wall():
    f = Fig(1000, 560)
    f.head()
    para(f, 30, 34, "人形机器人上的“大脑”只有几 Hz，不是因为算子跑不动，是因为权重读不进来。"
         "自回归解码每出一个 token，都要把整个模型的权重重读一遍。", 55, dy=24)

    f.rect(60, 108, 210, 214, stroke=GREEN, fill="#f2f8f3")
    f.text(165, 140, "算力这一侧", cls="t", anchor="middle", fill=GREEN)
    f.text(165, 172, "6B × 2 GFLOP", cls="m", anchor="middle")
    f.text(165, 196, "≈ 12 GFLOP / token", cls="s", anchor="middle")
    f.line(84, 216, 246, 216, stroke=LIGHT, w=2)
    f.text(165, 242, "Thor 级 NPU：", cls="s", anchor="middle")
    f.text(165, 266, "10¹⁵ FLOPS 量级 [厂]", cls="m", anchor="middle")
    f.text(165, 296, "单看算力：微秒级", cls="s", anchor="middle", fill=GREEN)

    f.rect(290, 108, 230, 214, stroke=RED, fill="#fbf3f3")
    f.text(405, 140, "内存这一侧（真瓶颈）", cls="t", anchor="middle", fill=RED)
    f.text(405, 172, "权重 6B × 2 B = 12 GB", cls="m", anchor="middle")
    f.text(405, 196, "每 token 全读一遍", cls="s", anchor="middle")
    f.line(314, 216, 496, 216, stroke=LIGHT, w=2)
    f.text(405, 242, "假设带宽 100 GB/s", cls="s", anchor="middle")
    f.text(405, 266, "12 ÷ 100 = 120 ms", cls="m", anchor="middle")
    f.text(405, 296, "⇒ ≤ 8.3 Hz [算]", cls="s", anchor="middle", fill=RED)

    rx = 560
    f.text(rx, 132, "两根柱子差了约 10⁷ 倍。", cls="t")
    para(f, rx, 158, "所以先动的不是“更快的 NPU”，而是三件事：", 22, dy=22)
    opts = [
        ("量化", ["FP16 → FP8/INT4：读的字节", "数按比例降，速度近乎线性涨；", "代价是量化误差与校准。"]),
        ("动作分块", ["一次前向输出 H 步动作，把", "H·Δt ≥ T_infer 当成硬约束", "（第 31 章）。"]),
        ("异步双系统", ["大脑低频给目标，小脑高频给", "扭矩。大脑慢没关系，只要它", "给的东西能被跟住。"]),
    ]
    yy = 208
    for name, ls in opts:
        f.text(rx, yy, name, cls="t", fill=ACC)
        for j, ln in enumerate(ls):
            f.text(rx + 118, yy + j * 21, ln, cls="s")
        yy += len(ls) * 21 + 20

    f.line(40, 486, 960, 486, stroke=INK, w=2)
    f.text(40, 512, "本图的“100 GB/s”是数量级假设，不是任何厂商公布的实测带宽；"
           "宇树未公布模型在机内的实际推理频率 [未]。", cls="s")
    f.text(40, 536, "12 GB 权重与 120 ms 这条除法在附录 B 有可复算脚本"
           "（code/tools/foc_check.py 的 llm_memory_time）。", cls="s")
    f.save("f26-memory-wall.svg")



def main():
    print("tools/make_figs3.py")
    f04_depth_ruler()
    f11_dq_plane()
    f19_programmable_spring()
    f26_memory_wall()


if __name__ == "__main__":
    main()
