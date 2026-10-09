#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/make_figs2.py — 第二批自绘图（第 3–5 部 + 成本/换向/时序/热）。

复用 make_figs.Fig，保证两批图的字号、配色、线宽完全一致（同一本书不能有两套图形语言）。
图内一律不写「图 NN-1 标题」——编号与标题由 <figcaption> 承担。
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from make_figs import Fig, ACC, RED, GREEN, GREY, INK, LIGHT, MONO  # noqa: E402


# ───────────────────────────────────────────────────────── F-03-1 成本结构
def f03_bom():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "把整机售价拆开：会动的部分贵，聪明的部分便宜", cls="s")
    ox, oy, W = 90, 300, 830
    f.line(ox, oy, ox + W, oy, GREY, 1)
    segs = [("23 个关节模组", 8487, ACC, "按 GO-M8010-6 零售价 369 美元 × 23（上界）"),
            ("感知（雷达+相机+IMU）", 600, GREEN, "拆解口径 <600 美元"),
            ("算力（Orin NX 级）", 750, GREEN, "拆解口径 ≈750 美元"),
            ("能源 + 结构 + 线缆 + 装配", 3663, GREY, "余量，本书推算")]
    x = ox
    for lab, v, col, note in segs:
        w = v / 13500 * W
        f.rect(x, oy - 90, w, 90, col, col + "33", 2)
        f.text(x + 6, oy - 100, f"${v:,}", cls="m", fill=col, size=17)
        f.text(x + 6, oy + 22, lab, cls="tiny", fill=col)
        f.text(x + 6, oy + 42, note, cls="tiny", fill=GREY)
        x += w
    f.line(ox + W, oy - 110, ox + W, oy + 50, RED, 1.5, "4,4")
    f.text(ox + W, oy - 122, "整机零售 $13,500", cls="t", fill=RED, anchor="end")
    f.rect(300, 150, 420, 40, ACC, "#fff", 2)
    f.text(510, 176, "关节 ≈ 63%　·　感知+算力 ≈ 10%", cls="t", anchor="middle", size=18)
    f.text(90, 372, "口径提示：8,487 美元是「全部用零售价」的上界；批量自产成本约为其一半（本书假设）。两种读法都给出同一个结论。", cls="tiny")
    f.save("f03-bom.svg")


# ───────────────────────────────────────────────────────── F-06-1 换向器
def f06_commutation():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "同一件事（维持定子场与转子场正交）的两种做法", cls="s")

    # 左：有刷
    cx, cy, R = 200, 200, 80
    f.circle(cx, cy, R, GREY, "none", 2)
    for k in range(8):
        a = math.radians(k * 45)
        f.line(cx + (R - 12) * math.cos(a), cy - (R - 12) * math.sin(a),
               cx + R * math.cos(a), cy - R * math.sin(a), GREY, 1.5)
    f.arrow(cx - R * 0.7, cy, cx + R * 0.7, cy, ACC, 3)
    f.text(cx, cy - R - 14, "定子磁场（永磁，固定）", cls="tiny", fill=ACC, anchor="middle")
    f.arrow(cx, cy + R * 0.6, cx + 40, cy - 40, RED, 3)
    f.text(cx + 46, cy - 44, "转子磁矩 m", cls="tiny", fill=RED)
    f.rect(96, 296, 210, 46, RED, "#fdf6f6", 2)
    f.text(201, 316, "换向器 + 碳刷", cls="t", fill=RED, anchor="middle", size=18)
    f.text(201, 334, "每转一圈撞一次自己", cls="tiny", fill=RED, anchor="middle")
    f.text(60, 366, "优点：不需要知道角度——它的位置就是转子的位置，物理耦合。", cls="tiny")

    # 右：无刷
    cx2 = 640
    f.circle(cx2, cy, R, GREY, "none", 2)
    for ang in (0, 120, 240):
        a = math.radians(ang)
        f.line(cx2 - R * 0.85 * math.cos(a), cy + R * 0.85 * math.sin(a),
               cx2 + R * 0.85 * math.cos(a), cy - R * 0.85 * math.sin(a), ACC, 1.6)
    f.arrow(cx2, cy, cx2 + 58, cy - 46, GREEN, 3)
    f.text(cx2 + 62, cy - 50, "合成矢量（软件决定）", cls="tiny", fill=GREEN)
    f.arrow(cx2, cy, cx2 - 20, cy - 72, RED, 3)
    f.text(cx2 - 96, cy - 78, "转子磁钢", cls="tiny", fill=RED)
    f.rect(520, 296, 250, 46, GREEN, "#f4faf6", 2)
    f.text(645, 316, "FOC + 编码器", cls="t", fill=GREEN, anchor="middle", size=18)
    f.text(645, 334, "没有磨损件，但必须知道 θ", cls="tiny", fill=GREEN, anchor="middle")
    f.rect(800, 120, 180, 150, GREY, "#f7f7f7", 2)
    for i, lab in enumerate(["θ 从编码器来", "→ 会被装配误差污染", "→ 会被齿隙误导", "→ 掉电会丢失", "→ 要产线标定"]):
        f.text(812, 148 + i * 26, lab, cls="tiny", fill=GREY if i else INK)
    f.text(60, 388, "无刷化的本质：把磨损件换成信息。换来的是一整类新故障——信息错。", cls="t", size=18)
    f.save("f06-commutation.svg")


# ───────────────────────────────────────────────────────── F-13-1 时序轴
def f13_timing():
    f = Fig(1000, 520)
    f.head()
    f.text(30, 30, "一个开关周期（T = 50 µs，20 kHz）里的四件事", cls="s")
    ox, W = 150, 700
    def X(us):
        return ox + us / 50.0 * W

    lanes = [("上管栅极", 100, ACC), ("下管栅极", 170, GREEN), ("绕组电流", 250, INK)]
    for name, y, col in lanes:
        f.text(ox - 12, y + 6, name, cls="m", anchor="end", size=16)

    # 上管：0–30 µs 高；下管：30.1–48 µs 高（中间 100 ns 死区，图上放大成可见宽度）
    def digital(y, base, on_segments, col):
        pts = []
        for us in range(0, 501):
            t = us / 10.0
            lvl = 1 if any(a <= t < b for a, b in on_segments) else 0
            pts.append((X(t), y - lvl * 34))
        f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), col, 2.5)
    digital(100, 0, [(0, 30)], ACC)
    digital(170, 0, [(31, 48)], GREEN)

    # 死区带（画在两条栅极线之间）
    f.rect(X(29.2), 52, X(31.8) - X(29.2), 130, RED, "#fdf6f6", 1.5)
    f.text(X(31.8) + 8, 66, "死区：两管都不开，电流只能走体二极管", cls="tiny", fill=RED)
    f.text(X(31.8) + 8, 86, "ΔV = (t_dead / T) · V_bus = 48 mV", cls="m", fill=RED, size=16)

    # 绕组电流：一条缓慢变化的线 + 高频纹波
    pts = []
    for us in range(0, 501):
        t = us / 10.0
        base = 22 * math.sin(math.radians(t * 3.0))
        ripple = 7 * (((t * 20) % 1) - 0.5) * 2
        pts.append((X(t), 250 - base - ripple))
    f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), INK, 1.8)

    # 采样窗
    f.rect(X(36), 210, X(46) - X(36), 74, GREEN, "#f4faf6", 2, dash="5,4")
    f.text((X(36) + X(46)) / 2, 202, "ADC 采样窗", cls="m", fill=GREEN, anchor="middle", size=16)
    f.circle(X(41), 250 - 22 * math.sin(math.radians(41 * 3.0)), 5, RED, RED, 2)
    f.text(X(47) + 14, 300, "硬件触发，落在下管导通窗中点", cls="tiny", fill=GREY)

    # 时间轴
    f.line(ox, 320, ox + W, 320, GREY, 1)
    for t in (0, 10, 20, 30, 40, 50):
        f.line(X(t), 320, X(t), 326, GREY, 1)
        f.text(X(t), 344, f"{t} µs", cls="tiny", anchor="middle")

    # 两条失效注记
    f.rect(150, 366, 810, 88, RED, "#fdf6f6", 2)
    f.text(166, 392, "两处最容易出事的接缝：", cls="t", size=18, fill=RED)
    f.text(166, 418, "① 死区偷走的电压方向恒与电流相反 ⇒ 过零处出现台阶：示波器看得见，力控上表现为按压过零抖一下", cls="m", size=16)
    f.text(166, 442, "② 采样落在开关沿上 ⇒ 电流环噪声随占空比变化，低速大电流最严重，常被误诊为「PI 没调好」", cls="m", size=16)
    f.text(150, 478, "死区宽度在本图上被放大约 10⁴ 倍（真实 100 ns 在 50 µs 周期里只有 0.2% 宽），否则肉眼看不见。", cls="tiny")
    f.text(150, 500, "宇树未公布任何一款关节的载波频率与死区时间 [未]；本图给的是判据与机理，不是它的实现。", cls="tiny")
    f.save("f13-timing.svg")


# ───────────────────────────────────────────────────────── F-17-1 ZMP 三工况
def f17_zmp():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "p_x = x − z·ẍ/(z̈+g)：同一条式子的三种工况，与「脚该迈到哪」", cls="s")
    ox, oy = 110, 300
    for i, (lab, xacc, col, note) in enumerate([
            ("站着不动", 0.0, ACC, "ZMP = 重心投影"),
            ("往前加速", 0.35, GREEN, "ZMP 跑到投影之前 ⇒ 才能往前倒"),
            ("往前刹车", -0.35, RED, "ZMP 后退；退到脚掌边缘就到极限")]):
        x = ox + i * 290
        f.line(x - 60, oy, x + 60, oy, GREY, 2)
        f.parts.append(f'<ellipse cx="{x}" cy="{oy+2}" rx="52" ry="8" fill="{col}22" stroke="{col}" stroke-width="1.5"/>')
        top = oy - 150
        f.line(x, oy, x + xacc * 90, top, INK, 3)
        f.circle(x + xacc * 90, top, 9, INK, INK, 2)
        f.text(x + xacc * 90 + 14, top + 5, "重心", cls="tiny")
        zx = x + xacc * 90 * 0.0 + (0 if xacc == 0 else (xacc * 250))
        zx = x + (0 if xacc == 0 else math.copysign(min(abs(xacc) * 260, 52), xacc))
        f.arrow(zx, oy + 30, zx, oy + 8, col, 3)
        f.text(zx, oy + 46, "ZMP", cls="m", fill=col, anchor="middle", size=16)
        f.text(x, oy - 178, lab, cls="t", fill=col, anchor="middle")
        f.text(x, oy + 68, note, cls="tiny", anchor="middle")
    f.rect(110, 60, 800, 44, GREY, "#f7f7f7", 2)
    f.text(126, 88, "ZMP 出界 = 需要地面「拉」一脚，而地面不给拉力 ⇒ 脚缘离地 ⇒ 开始转动。这就是它唯一的失效方式。", cls="m", size=17)
    f.rect(110, 116, 800, 52, ACC, "#f3f8fd", 2)
    f.text(126, 138, "捕获点　x_cap = x + ẋ/ω₀ ，ω₀ = √(g/(z−z_foot)) = 1/τ", cls="m", fill=ACC)
    f.text(126, 160, "G1：ω₀ = 3.85 rad/s ⇒ 0.3 m/s 要把脚放到投影之前 78 mm；0.6 m/s ⇒ 156 mm。迈不到就停不下来。", cls="tiny")
    f.text(110, 386, "三个前提会破：脚不是完全贴合的刚性面（不平地面）· 机体不是刚体（23 个有齿隙的关节）· 摩擦锥只管压不管滑（冰面）。", cls="tiny")
    f.save("f17-zmp.svg")


# ───────────────────────────────────────────────────────── F-22-1 诊断表
def f22_diag():
    f = Fig(1000, 430)
    f.head()
    f.text(30, 30, "抖成什么样 → 仿真里缺的是哪一样 → 唯一的正解", cls="s")
    rows = [
        ("固定频率抖，与步频无关，带载加重", "结构模态（仿真里连杆是刚的）", "改结构，或把带宽压到 f_m/3", RED),
        ("落地冲击峰值远大于仿真", "接触求解器差异", "软足垫 / 重新随机化接触参数", ACC),
        ("低速位置误差大，换向有顿挫", "齿隙 + 静摩擦", "提高传动刚度或前馈补偿", ACC),
        ("过零有台阶，且与电周期同步", "死区（第 13 章）", "死区补偿（有限度）", GREEN),
        ("快速动作跟不上，降 kp 反而更稳", "延迟分布", "降低控制带宽，别指望调参", GREEN)]
    y = 70
    f.text(40, y - 12, "症状", cls="t", fill=GREY, size=16)
    f.text(430, y - 12, "仿真里不存在的那一样", cls="t", fill=GREY, size=16)
    f.text(760, y - 12, "唯一正解", cls="t", fill=GREY, size=16)
    for sym, miss, fix, col in rows:
        f.rect(30, y, 940, 52, col, "#fbfcfe", 2)
        f.text(44, y + 24, sym, cls="m", size=16)
        f.text(430, y + 24, miss, cls="m", size=16, fill=col)
        f.text(760, y + 24, fix, cls="m", size=16)
        f.line(420, y + 4, 420, y + 48, LIGHT, 1)
        f.line(750, y + 4, 750, y + 48, LIGHT, 1)
        y += 58
    f.rect(30, y + 6, 940, 44, RED, "#fdf6f6", 2)
    f.text(46, y + 34, "最有价值的一列是最后一列：五行里有四行「调参数调不出来」。承认这一点，比调出来但不知道为什么更有价值。", cls="t", size=17, fill=RED)
    f.save("f22-diagnosis.svg")


# ───────────────────────────────────────────────────────── F-23-1 双目误差
def f23_depth():
    f = Fig(1000, 380)
    f.head()
    f.text(30, 30, "ΔZ = Z²·Δd/(f·B)：误差随距离平方涨，而同步误差的杀伤力更大", cls="s")
    ox, oy, W, H = 110, 290, 560, 200
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    B, fp, dd = 0.060, 672, 0.5
    pts = []
    for i in range(1, 81):
        Z = i / 10
        dz = Z * Z * dd / (fp * B)
        pts.append((ox + Z / 8 * W, oy - min(dz / 0.5, 1) * H))
    f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), ACC, 2.5)
    for Z in (0.5, 1, 2, 4, 6, 8):
        x = ox + Z / 8 * W
        dz = Z * Z * dd / (fp * B)
        f.line(x, oy, x, oy - min(dz / 0.5, 1) * H, LIGHT, 1, "3,4")
        f.text(x, oy + 22, f"{Z:g}", cls="tiny", anchor="middle")
        f.text(x + 4, oy - min(dz / 0.5, 1) * H - 6, f"{dz*100:.1f} cm", cls="tiny", fill=ACC)
    f.text(ox + W / 2, oy + 44, "距离 Z（米）", cls="s", anchor="middle")
    f.text(ox - 12, oy - H + 6, "50", cls="tiny", anchor="end")
    f.text(ox - 12, oy + 4, "0", cls="tiny", anchor="end")
    f.text(ox - 46, oy - H / 2, "深度误差（cm）", cls="s", anchor="middle", size=15)

    f.rect(700, 80, 270, 200, RED, "#fdf6f6", 2)
    f.text(716, 108, "另一条轴：不同步", cls="t", fill=RED)
    for i, s in enumerate(["v_相对 = 1 m/s", "Δt = 20 ms", "f = 672 px，Z = 1 m", "⇒ 伪视差 13.4 px", "   ÷ 精度假设 0.5 px", "   = 27 倍噪声"]):
        f.text(716, 136 + i * 24, s, cls="m", size=16, fill=RED if i >= 3 else INK)
    f.text(110, 356, "读法：50 cm 处能分辨 3 mm（够抓杯子）；4 m 处误差 20 cm（判断不了远处物体）。所以相机与雷达不是冗余，是互补的两个方向。", cls="tiny")
    f.save("f23-depth-error.svg")


# ───────────────────────────────────────────────────────── F-24-1 零偏积分
def f24_imu():
    f = Fig(1000, 380)
    f.head()
    f.text(30, 30, "陀螺管高频、加速度计管低频：融合不是加分项，是必需", cls="s")
    ox, oy, W, H = 110, 290, 560, 200
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    for b, col, lab in [(0.1, GREEN, "零偏 0.1 °/s"), (1.0, RED, "零偏 1 °/s")]:
        pts = [(ox + t / 60 * W, oy - min(b * t / 60, 1) * H) for t in range(0, 61)]
        f.path("M " + " L ".join(f"{a:.1f},{b2:.1f}" for a, b2 in pts), col, 2.5)
        f.text(ox + W - 6, oy - min(b, 1) * H + 18, lab, cls="m", fill=col, anchor="end")
    for t in (0, 10, 20, 30, 40, 50, 60):
        f.text(ox + t / 60 * W, oy + 22, str(t), cls="tiny", anchor="middle")
    f.text(ox + W / 2, oy + 44, "时间（秒）", cls="s", anchor="middle")
    for v, lab in [(0, "0"), (30, "30°"), (60, "60°")]:
        f.text(ox - 12, oy - v / 60 * H + 5, lab, cls="tiny", anchor="end")
    f.text(ox - 46, oy - H / 2, "姿态误差", cls="s", anchor="middle", size=15)
    f.line(ox, oy - 10 / 60 * H, ox + W, oy - 10 / 60 * H, RED, 1.5, "6,4")
    f.text(ox + 8, oy - 10 / 60 * H - 8, "重心容差约 1–3°（本书按几何估读）⇒ 10 秒内就吃光", cls="tiny", fill=RED)

    f.rect(700, 80, 270, 200, ACC, "#f3f8fd", 2)
    f.text(716, 108, "为什么必须融合", cls="t", fill=ACC)
    for i, s in enumerate(["陀螺：几秒内很准", "　　 但误差线性累积", "加速度计：几十秒后仍准", "　　 但只在静止时能定「竖直」", "⇒ 频段互补", "⇒ 卡尔曼不是加分项"]):
        f.text(716, 136 + i * 24, s, cls="m", size=16)
    f.text(110, 356, "宇树只公布字段与「双 IMU」结构；型号、零偏稳定性、整机 IMU 采样率全部未公布 [未]。所以这一张图给的是判据，不是它的指标。", cls="tiny")
    f.save("f24-imu-bias.svg")


# ───────────────────────────────────────────────────────── F-27-1 总线
def f27_bus():
    f = Fig(1000, 420)
    f.head()
    f.text(30, 30, "三条总线，两种哲学：同步 vs 成本", cls="s")
    # 左：宇树 RS-485 主从
    f.rect(40, 60, 440, 150, ACC, "#f3f8fd", 2)
    f.text(56, 86, "宇树：RS-485 主从轮询", cls="t", fill=ACC)
    f.rect(60, 106, 90, 40, ACC, "#fff", 2)
    f.text(105, 132, "主控", cls="m", anchor="middle", fill=ACC)
    for i in range(5):
        x = 220 + i * 50
        f.rect(x, 106, 40, 40, GREY, "#fff", 1.5)
        f.text(x + 20, 132, str(i + 1), cls="tiny", anchor="middle", fill=GREY)
    f.line(150, 126, 220, 126, ACC, 2)
    f.line(220, 126, 440, 126, ACC, 2)
    for i in range(5):
        f.line(240 + i * 50, 126, 240 + i * 50, 106, ACC, 1.5)
    f.text(56, 172, "一主多从 · 半双工 · 无仲裁 · 无内建错误管理", cls="tiny")
    f.text(56, 194, "官方帧长：下行 17 B / 上行 16 B；ID 0–14，15 = 广播", cls="m", size=16)

    # 右：EtherCAT 手拉手
    f.rect(520, 60, 440, 150, GREEN, "#f4faf6", 2)
    f.text(536, 86, "工业界：EtherCAT 逐站转发", cls="t", fill=GREEN)
    f.rect(540, 106, 80, 40, GREEN, "#fff", 2)
    f.text(580, 132, "主站", cls="m", anchor="middle", fill=GREEN)
    for i in range(5):
        x = 650 + i * 60
        f.rect(x, 106, 44, 40, GREY, "#fff", 1.5)
        f.text(x + 22, 132, str(i + 1), cls="tiny", anchor="middle", fill=GREY)
        if i:
            f.line(x - 16, 126, x, 126, GREEN, 2)
    f.line(620, 126, 650, 126, GREEN, 2)
    f.text(536, 172, "全双工以太网 · DC 分布式时钟亚微秒对齐 · 每站一颗 ESC", cls="tiny")
    f.text(536, 194, "ESC 约 ¥87/颗 对 RS-485 收发器约 2 元 ⇒ 23 关节差约 1,955 元", cls="m", size=16)

    # 下：带宽算术
    f.rect(40, 232, 920, 120, RED, "#fdf6f6", 2)
    f.text(56, 260, "一次除法就能判断厂商那个赫兹数指的是什么（GO-M8010-6 官方帧长）", cls="t", size=18, fill=RED)
    f.text(56, 288, "15 台 × 6000 Hz × (17 + 16) B × 8 = 23.76 Mbps　÷　官方 4 Mbps　=　5.9 倍　⇒ 全双工全量交换不可能", cls="m")
    f.text(56, 314, "反过来：4 Mbps ÷ (15 × 33 B × 8) = 1010 Hz　——　与官方 Z1 页标的 Control Frequency 1 kHz 撞在同一处", cls="m", fill=RED)
    f.text(40, 378, "人形不需要「23 个关节同一纳秒动作」，因为每个关节是独立闭环、总线只下发给定值。", cls="t", size=18)
    f.text(40, 404, "所以 RS-485 不是选错了；它缺的那个能力，恰好是这台机器不需要的。", cls="s")
    f.save("f27-bus.svg")


# ───────────────────────────────────────────────────────── F-28-1 栈对照
def f28_stack():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "同样的字节，中间隔了几层：每一层都要付时间利息", cls="s")
    def col(x, title, layers, col_):
        f.text(x + 150, 68, title, cls="t", anchor="middle", fill=col_)
        y = 84
        for lab, hot in layers:
            h = 44
            f.rect(x, y, 300, h, col_ if hot else GREY, "#fdf6f6" if hot else "#fbfbfd", 2)
            f.text(x + 150, y + 28, lab, cls="m", anchor="middle", fill=col_ if hot else INK)
            y += h + 6
    col(120, "ROS 2 应用", [("你的节点（rclcpp）", 0), ("ROS 2 图：话题 / 服务 / 参数", 1), ("rmw 抽象层", 1), ("CycloneDDS 序列化 + 网络", 0)], ACC)
    col(580, "宇树 SDK2 应用", [("你的代码", 0), ("unitree_sdk2 主题与请求响应", 1), ("CycloneDDS 序列化 + 网络", 0)], RED)
    f.rect(120, 320, 760, 40, GREY, "#f7f7f7", 2)
    f.text(500, 346, "下面都是同一台机器：rt/lowcmd 500 Hz → 关节 MCU 内环路 kHz → PWM 20 kHz", cls="m", anchor="middle", fill=GREY)
    f.text(120, 384, "少一层就少一次序列化、少一次拷贝、少一份不确定性。这不是偏好：关键路径是确定性的时候，抽象层要付利息。", cls="tiny")
    f.save("f28-stack.svg")


# ───────────────────────────────────────────────────────── F-29-1 多峰
def f29_multimodal():
    f = Fig(1000, 380)
    f.head()
    f.text(30, 30, "演示里一半从左边抓、一半从右边抓，MSE 会学成「抓中间」", cls="s")
    ox, oy, W, H = 90, 280, 380, 190
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.text(ox + W / 2, oy + 24, "标签：杯子放哪（米）", cls="tiny", anchor="middle")
    for v in (-0.2, 0.2):
        x = ox + W / 2 + v / 0.3 * (W / 2)
        f.parts.append(f'<path d="M {x-30} {oy} Q {x} {oy-H} {x+30} {oy} Z" fill="{ACC}33" stroke="{ACC}" stroke-width="2"/>')
        f.text(x, oy - H - 6, "左" if v < 0 else "右", cls="m", fill=ACC, anchor="middle")
    f.line(ox + W / 2, oy, ox + W / 2, oy - H, RED, 2, "6,4")
    f.text(ox + W / 2, oy + 44, "MSE 最优解 = 条件均值 = 0", cls="t", fill=RED, anchor="middle", size=17)
    f.text(ox + W / 2, oy + 68, "而 0 处是桌沿：放不进去，也不算失败样本", cls="tiny", fill=RED, anchor="middle")

    f.rect(520, 70, 440, 200, GREEN, "#f4faf6", 2)
    f.text(536, 98, "三条出路：把「均值」换成「分布」", cls="t", fill=GREEN)
    for i, (lab, sub) in enumerate([
            ("自回归离散 token", "π0-FAST / GO-1 隐动作　复用 LLM 工具链，但序列长"),
            ("扩散 diffusion", "几十步去噪　分布建模好，但慢"),
            ("流匹配 flow matching", "5–10 步积分　当前主流（π、GR00T、GraspVLA、UnifoLM）")]):
        f.text(536, 130 + i * 46, lab, cls="m", fill=GREEN)
        f.text(536, 150 + i * 46, sub, cls="tiny")
    f.text(90, 320, "一条判据：任务的所有正确做法之间差距很小 ⇒ MSE 够用；差距是离散互斥的 ⇒ MSE 一定失败。", cls="t", size=18)
    f.text(90, 348, "看一个策略项目的损失函数，就能看出作者有没有理解自己的任务分布。", cls="s")
    f.save("f29-multimodal.svg")


# ───────────────────────────────────────────────────────── F-30-1 VLA
def f30_vla():
    f = Fig(1000, 420)
    f.head()
    f.text(30, 30, "全行业两年内收敛到同一张图：四个部件，动作头三选一", cls="s")
    boxes = [("① VLM 主干", "1.8B–7B　看懂场景、理解指令", ACC, "下界=先验容量　上界=端侧内存带宽"),
             ("② 动作专家", "80M–1B　专职生成动作，比主干小 1–2 个数量级", RED, "小，才能跑高频"),
             ("③ 动作头（三选一）", "流匹配 / 扩散　·　离散 token　·　小回归 visuomotor", GREEN, "多峰→前两种；要 200 Hz→第三种"),
             ("④ 分块 + 异步双系统", "一次输出 H 步；边执行边算下一块", ACC, "块长 = 延迟容忍度")]
    y = 60
    for lab, sub, col, note in boxes:
        f.rect(60, y, 400, 62, col, "#fbfcfe", 2)
        f.text(76, y + 26, lab, cls="t", fill=col, size=18)
        f.text(76, y + 48, sub, cls="tiny")
        f.text(480, y + 36, note, cls="m", fill=GREY, size=16)
        if y < 60 + 3 * 68:
            f.arrow(260, y + 62, 260, y + 68, col, 2)
        y += 68
    f.rect(60, y, 400, 56, GREEN, "#f4faf6", 2)
    f.text(260, y + 24, "⑤ 关节层（第 12 章那条链）", cls="t", fill=GREEN, anchor="middle", size=18)
    f.text(260, y + 44, "kp/kd 在两块之间做局部纠错", cls="tiny", fill=GREEN, anchor="middle")

    f.rect(520, 60, 440, 300, GREY, "#f7f7f7", 2)
    f.text(536, 88, "公开口径的几个数", cls="t")
    rows = [("Figure Helix", "S2 7B @7–9 Hz　S1 80M @200 Hz　全端侧"),
            ("π*0.6", "Gemma3-4B + 860M flow　63 ms/块（H100）"),
            ("GR00T N1.7-3B", "horizon 40　状态/动作 132 维　端侧 16 GB+"),
            ("SmolVLA", "450M（含约 100M 动作专家）　CPU 也能跑"),
            ("宇树 UnifoLM-WLA", "6B　约 2500 h　64 任务　Apache-2.0"),
            ("银河 AstraBrain", "WBC 0.5：8040 万参数、384 专家蒸馏、ONNX")]
    for i, (a, b) in enumerate(rows):
        f.text(536, 118 + i * 38, a, cls="m", size=16, fill=ACC)
        f.text(536, 136 + i * 38, b, cls="tiny")
    f.text(60, 396, "为什么必须双系统：主干比平衡慢。第 17 章 τ = 0.259 s，第 26 章推理 ≥ 120 ms —— 两个数一比，架构就定了。", cls="t", size=18)
    f.save("f30-vla.svg")


# ───────────────────────────────────────────────────────── F-31-1 块长双向界
def f31_chunk():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "块长有两个相反的界：一个来自推理时间，一个来自世界的变化速度", cls="s")
    ox, oy, W, H = 130, 300, 760, 210
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    for Hh in range(4, 81, 4):
        x = ox + (Hh - 4) / 76 * W
        f.text(x, oy + 22, str(Hh), cls="tiny", anchor="middle")
    f.text(ox + W / 2, oy + 46, "动作块长度 H（步，Δt = 20 ms）", cls="s", anchor="middle")
    f.text(ox - 46, oy - H / 2, "时间（毫秒）", cls="s", anchor="middle", size=15)
    def Y(ms):
        return oy - min(ms / 1600, 1) * H
    f.path(f"M {ox} {Y(200)} L {ox+W} {Y(1600)}", RED, 2.5)
    f.text(ox + W - 10, Y(1560) - 10, "平均反应延迟 = H·Δt / 2", cls="m", fill=RED, anchor="end")
    f.path(f"M {ox} {Y(160)} L {ox+W} {Y(160)}", GREEN, 2.5, dash="6,4")
    f.text(ox + 10, Y(160) - 10, "一次推理 T_infer（端侧 ≈160 ms）", cls="m", fill=GREEN)
    f.path(f"M {ox} {Y(100)} L {ox+W} {Y(100)}", ACC, 2, dash="3,3")
    f.text(ox + 10, Y(100) + 18, "世界能等你多久：接触/平衡需要 10–100 ms", cls="tiny", fill=ACC)
    xl = ox + (32 - 4) / 76 * W
    f.line(xl, oy, xl, oy - H, INK, 1.5, "5,4")
    f.text(xl, oy - H - 8, "可行窗口在这里", cls="t", anchor="middle", size=17)
    f.rect(600, 90, 300, 90, RED, "#fdf6f6", 2)
    f.text(616, 118, "H = 40 的读法", cls="t", fill=RED)
    f.text(616, 144, "一块覆盖 800 ms", cls="m")
    f.text(616, 168, "平均反应 400 ms > τ = 259 ms", cls="m", fill=RED)
    f.text(130, 376, "所以 VLA 在结构上不能承担平衡与接触密集任务——不是模型不够大，是 H·Δt 这个乘数不允许。", cls="t", size=18)
    f.save("f31-chunk-window.svg")


# ───────────────────────────────────────────────────────── F-33-1 数据成本
def f33_data():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "三条数据路线的成本曲线形状不同：这才是路线之争的真正内容", cls="s")
    ox, oy, W, H = 130, 300, 700, 210
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    f.text(ox + W / 2, oy + 26, "累计可用数据量（小时）", cls="s", anchor="middle")
    f.text(ox - 46, oy - H / 2, "累计成本", cls="s", anchor="middle", size=15)
    f.path(f"M {ox} {oy} L {ox+W} {oy-H}", RED, 3)
    f.text(ox + W - 8, oy - H - 10, "真机遥操：线性，每次都付（¥4,000–8,000 / 可用小时）", cls="m", fill=RED, anchor="end")
    f.path(f"M {ox} {oy-H*0.72} Q {ox+W*0.25} {oy-H*0.66} {ox+W} {oy-H*0.62}", GREEN, 3)
    f.text(ox + 10, oy - H * 0.80, "仿真合成：前重后轻，建好之后边际 ≈ 电费", cls="m", fill=GREEN)
    f.path(f"M {ox} {oy} L {ox+W*0.98} {oy-H*0.14}", ACC, 3, dash="7,4")
    f.text(ox + W * 0.62, oy - H * 0.20, "人类视频：便宜（约 ¥100/h），但迁移成本未计", cls="m", fill=ACC)
    f.rect(560, 90, 340, 96, GREY, "#f7f7f7", 2)
    f.text(576, 116, "换算成同一个单位才可比", cls="t")
    f.text(576, 142, "10 亿帧 ÷ 30 fps ÷ 3600 = 9,259 小时", cls="m", size=16)
    f.text(576, 166, "270,000 小时是它的 29 倍", cls="m", size=16, fill=RED)
    f.text(130, 376, "看到任何数据集宣传，先做这一步换算。「轨迹 / 帧 / 小时」是三种度量，混着报是行业常态。", cls="t", size=18)
    f.save("f33-data-cost.svg")


# ───────────────────────────────────────────────────────── F-35-1 串数反推
def f35_series():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "厂商没说的化学体系，用两次除法推出来", cls="s")
    rows = [("G1", "13 串 / 9000 mAh / 充 54 V", "54.0 ÷ 13 = 4.15 V", "≈ 0.43 kWh（推）", ACC),
            ("H1", "15 Ah / 0.864 kWh / 最大 67.2 V", "67.2 ÷ 16 = 4.20 V", "0.864 ÷ 15 ÷ 16 = 3.60 V", GREEN),
            ("H2", "15 Ah / 0.972 kWh / 最大 75.6 V", "75.6 ÷ 18 = 4.20 V", "0.972 ÷ 15 ÷ 18 = 3.60 V", GREEN),
            ("R1", "容量与电压未公布 [未]", "—", "续航约 1 h", GREY)]
    y = 70
    for m, spec, d1, d2, col in rows:
        f.rect(40, y, 920, 52, col, "#fbfcfe", 2)
        f.text(56, y + 32, m, cls="t", fill=col, size=19)
        f.text(140, y + 22, spec, cls="m", size=16)
        f.text(140, y + 42, d1 + "　·　" + d2, cls="tiny", fill=col)
        y += 58
    f.rect(40, y + 8, 440, 100, RED, "#fdf6f6", 2)
    f.text(56, y + 36, "4.20 V 终止 / 3.60 V 标称 ⇒", cls="t", fill=RED)
    f.text(56, y + 62, "钴基或三元锂，不是磷酸铁锂", cls="t", size=19, fill=RED)
    f.text(56, y + 88, "（LFP 是 3.2 / 3.65，16 串只能到 58.4 V）", cls="tiny")
    f.rect(520, y + 8, 440, 100, GREY, "#f7f7f7", 2)
    f.text(536, y + 36, "代价三条，各对应本书一章：", cls="t")
    for i, s in enumerate(["循环寿命短（第 37 章保修）", "热稳定性差（第 36 章热）", "电压平台斜率大 ⇒ 易塌陷（第 13 章）"]):
        f.text(536, y + 62 + i * 20, "·　" + s, cls="m", size=16)
    f.text(40, 388, "两条完全独立的路径（最大电压÷串数、能量÷容量÷串数）落在同一组数上——这就是本书敢写这句推断的理由。", cls="tiny")
    f.save("f35-series.svg")


# ───────────────────────────────────────────────────────── F-36-1 热
def f36_thermal():
    f = Fig(1000, 420)
    f.head()
    f.text(30, 30, "T_结 = T_环境 + P×(R₁+R₂+R₃)，而 R₃ 被四个产品约束推到最大", cls="s")
    # 热路
    boxes = [("绕组 / 磁钢", "铜损 I²R", RED, 60), ("机壳内壁", "导热胶·装配", ACC, 260),
             ("外壳外壁", "开关损耗", ACC, 460), ("环境", "自然对流", GREEN, 660)]
    y = 110
    for lab, sub, col, x in boxes:
        f.rect(x, y, 150, 70, col, "#fbfcfe", 2)
        f.text(x + 75, y + 30, lab, cls="t", fill=col, anchor="middle", size=18)
        f.text(x + 75, y + 54, sub, cls="tiny", anchor="middle")
        if x < 660:
            f.arrow(x + 150, y + 35, x + 200, y + 35, GREY, 2)
    for i, r in enumerate(["R₁", "R₂", "R₃"]):
        f.text(235 + i * 200, y - 12, r, cls="m", fill=RED, anchor="middle")
    f.text(60, 220, "R₃ 为什么最大：密封（不能有进气口）· 外形要像人腿（不能有大散热鳍）· 面积按 L² 缩而发热按 L³ 涨 · 无风扇（要开孔、会坏）", cls="tiny")
    f.text(60, 244, "自然对流约 5–10 W/(m²·K)，强制风冷约 25–100 ⇒ 去掉风扇等于把换热能力砍到 1/5–1/10。", cls="tiny")

    # 正反馈环
    cx, cy, R = 250, 330, 52
    f.circle(cx, cy, R, RED, "none", 2)
    for i, lab in enumerate(["电流 ↑", "铜损 ↑", "温度 ↑", "k_t ↓"]):
        a = math.radians(-90 + i * 90)
        f.text(cx + (R + 26) * math.cos(a), cy - (R + 26) * math.sin(a) + 5, lab, cls="m", fill=RED, anchor="middle", size=16)
    for i in range(4):
        a0 = math.radians(-45 + i * 90)
        f.parts.append(f'<path d="M {cx+R*math.cos(a0):.1f} {cy-R*math.sin(a0):.1f} A {R} {R} 0 0 1 {cx+R*math.cos(a0+math.radians(60)):.1f} {cy-R*math.sin(a0+math.radians(60)):.1f}" fill="none" stroke="{RED}" stroke-width="2"/>')
    f.text(cx, cy + 6, "没有自限机制", cls="t", fill=RED, anchor="middle", size=17)
    f.rect(420, 268, 540, 130, RED, "#fdf6f6", 2)
    f.text(436, 296, "温升 80 °C 时（行业通识系数）", cls="t", fill=RED)
    f.text(436, 322, "铜阻 +0.393 %/°C ⇒ 涨 31%", cls="m")
    f.text(436, 346, "剩磁 −0.11 %/°C ⇒ 扭矩少 8.8% ⇒ 电流再涨 9.6%", cls="m")
    f.text(436, 370, "合起来：同一扭矩下铜损涨 58%。越过磁钢上限后退磁不可逆，而控制器不知道。", cls="m", size=16)
    f.text(60, 412, "这就是「额定扭矩」不是一个数的原因：它是占空比、姿态、环境温度与外壳覆盖的函数。", cls="t", size=18)
    f.save("f36-thermal.svg")


# ───────────────────────────────────────────────────────── F-39-1 分工
def f39_jobs():
    f = Fig(1000, 400)
    f.head()
    f.text(30, 30, "六层的拥挤度与门槛：钱和人现在压在哪一层", cls="s")
    rows = [("③ 决策 / 大脑", "极挤", 0.95, RED, "万卡算力 + 博士密度 + 融资叙事中心"),
            ("④ 全身控制", "中", 0.5, ACC, "RL 路线把显式控制的人吸走了"),
            ("① 感知", "中", 0.45, ACC, "器件成熟，缺的是同步与标定工程"),
            ("② 状态估计", "低", 0.3, GREY, "学术成熟，工程岗位少"),
            ("⑤ 关节伺服", "缺", 0.18, GREEN, "会 FOC + 会总线 + 会实时的人极少"),
            ("⑥ 功率与热", "最缺", 0.1, GREEN, "会画功率板、会算热、会做减速器的人最少")]
    y = 66
    for lab, tag, w, col, note in rows:
        f.text(40, y + 22, lab, cls="t", size=18)
        f.rect(230, y, int(w * 300), 30, col, col + "33", 2)
        f.text(230 + int(w * 300) + 10, y + 22, tag, cls="m", fill=col)
        f.text(560, y + 22, note, cls="tiny")
        y += 42
    f.rect(40, y + 6, 920, 74, GREY, "#f7f7f7", 2)
    f.text(56, y + 32, "为什么 ⑤⑥ 缺而 ③ 挤：① 成果不可发表（「连续跑六个月没坏」没有投稿渠道）", cls="m", size=16)
    f.text(56, y + 56, "② 失败方式致命（当场冒烟、摔机）③ 需要四五个专业在同一个人身上复合", cls="m", size=16)
    f.text(40, 384, "所以选方向的问题不是「哪家更先进」，而是「哪一层还没有人做好」。", cls="t", size=18)
    f.save("f39-jobs.svg")


def main():
    for fn in (f03_bom, f06_commutation, f13_timing, f17_zmp, f22_diag, f23_depth,
               f24_imu, f27_bus, f28_stack, f29_multimodal, f30_vla, f31_chunk,
               f33_data, f35_series, f36_thermal, f39_jobs):
        fn()
    print("第二批完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
