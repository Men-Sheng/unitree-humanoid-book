#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/make_figs.py — 生成第 0–2 部的自绘矢量图（SVG）。

为什么用 SVG 而不是 matplotlib PNG：
  1. 书里这些图是**示意图**，不是数据图；线条与文字必须绝对清晰到 1000 lpi。
  2. SVG 里的文字是文本节点，由 Paged.js/Chrome 用正文同一款 Noto Serif/Sans SC 渲染，
     不会出现图内字体与正文不一致，也不会引入第二套字体子集（PDF-X 预检少一个坑）。
  3. 手写的图 = 可 diff、可复跑、可被作者改。政策见 bible/images.md（自绘 45% 这一条腿）。

版式约定：viewBox 1000 x H，线宽 2，字号 22/18/16，全部用 font-family 继承正文。
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "fig"
OUT.mkdir(parents=True, exist_ok=True)

SANS = "'Noto Sans SC','Microsoft YaHei',sans-serif"
SERIF = "'Noto Serif SC',serif"
MONO = "'Cascadia Mono','Consolas',monospace"
INK = "#111"
GREY = "#666"
LIGHT = "#ddd"
ACC = "#1a4f8a"     # 强调：结构线
RED = "#a52020"     # 强调：失效/不可达
GREEN = "#1d6b3a"   # 强调：可达/正确
NL = chr(10)


class Fig:
    def __init__(self, w=1000, h=560):
        self.w, self.h = w, h
        self.parts = []

    def head(self):
        self.parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="100%" font-family="{SANS}" fill="{INK}">')
        self.parts.append(
            '<style>text{font-family:%s}.m{font-family:%s;font-size:17px}'
            '.s{font-size:16px;fill:%s}.t{font-size:21px;font-weight:600}'
            '.h{font-size:23px;font-weight:700}.tiny{font-size:14px;fill:%s}'
            'line,path,rect,circle,polygon{vector-effect:non-scaling-stroke}</style>'
            % (SANS, MONO, GREY, GREY))

    @staticmethod
    def esc(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

    def text(self, x, y, s, cls="", fill=None, anchor="start", family=None, size=None):
        s = self.esc(s)
        f = f' fill="{fill}"' if fill else ""
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        st = f' font-size="{size}"' if size else ""
        fam = f' font-family="{family}"' if family else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" class="{cls}"{f}{a}{st}{fam}>{s}</text>')

    def line(self, x1, y1, x2, y2, stroke=INK, w=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{stroke}" stroke-width="{w}"{d}/>')

    def arrow(self, x1, y1, x2, y2, stroke=INK, w=2, dash=None):
        self.line(x1, y1, x2, y2, stroke, w, dash)
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 11
        for da in (math.radians(152), math.radians(-152)):
            self.parts.append(
                f'<line x1="{x2}" y1="{y2}" x2="{x2 + L*math.cos(ang+da):.1f}" '
                f'y2="{y2 + L*math.sin(ang+da):.1f}" stroke="{stroke}" stroke-width="{w}"/>'.replace('y2="', 'y2="', 1))

    def rect(self, x, y, w, h, stroke=INK, fill="none", sw=2, rx=6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def poly(self, pts, stroke=INK, fill="none", w=2, dash=None):
        s = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" '
                          f'stroke-width="{w}" stroke-linejoin="round"{d}/>')

    def path(self, d, stroke=INK, w=2, fill="none", dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
                          f'stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def circle(self, cx, cy, r, stroke=INK, fill="none", w=2):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{w}"/>')

    def save(self, name):
        self.parts.append("</svg>")
        p = OUT / name
        p.write_text(NL.join(self.parts), encoding="utf-8")
        print(f"  wrote assets/fig/{name}  ({p.stat().st_size//1024 + (1 if p.stat().st_size%1024 else 0)} KB)")


# ═════════════════════════════════════════════════════════════════════ F-00-1
def f00_time_domains():
    f = Fig(1000, 470)
    f.head()
    f.text(30, 34, "横轴为对数刻度的周期（毫秒）。层与层之间稳定相差 5–10 倍，这不是设计偏好，是每一层各自的物理时间常数。", cls="s")

    x0, x1 = 250, 950
    top, bot = 100, 380
    # 对数轴：0.02 ms .. 200 ms
    def X(ms):
        lo, hi = math.log10(0.02), math.log10(300)
        return x0 + (math.log10(ms) - lo) / (hi - lo) * (x1 - x0)

    f.line(x0, bot, x1, bot, GREY, 1)
    for ms, lab in [(0.05, "0.05"), (0.2, "0.2"), (1, "1"), (5, "5"), (20, "20"), (100, "100"), (300, "300")]:
        f.line(X(ms), bot, X(ms), bot + 6, GREY, 1)
        f.text(X(ms), bot + 24, lab, cls="tiny", anchor="middle")
    f.text((x0 + x1) / 2, bot + 48, "周期（毫秒，对数刻度）", cls="s", anchor="middle")

    rows = [
        ("⑥ 功率与机械", "MOSFET 开关", 0.05, RED),
        ("⑤ 关节伺服", "电流环（估）", 0.5, RED),
        ("⑤ 关节伺服", "指令刷新 1–6 kHz", 1.0, ACC),
        ("④ 全身控制", "WBC / MPC 量级", 1.0, ACC),
        ("整机总线", "rt/lowcmd 500 Hz", 2.0, ACC),
        ("⑤ 关节伺服", "策略 50 Hz", 20, GREEN),
        ("③ 任务与决策", "VLA 5–10 Hz", 150, GREEN),
    ]
    y = top
    for layer, what, ms, col in rows:
        f.text(30, y + 5, layer, cls="m", size=16)
        f.text(150, y + 5, what, cls="s", size=15)
        f.circle(X(ms), y, 6, col, col, 2)
        f.line(X(ms), y + 8, X(ms), bot, LIGHT, 1, "3,4")
        y += 38
    f.text(x0, bot + 66, "受半导体开关速度限制", cls="tiny", fill=RED)
    f.text(x0 + 186, bot + 66, "受电感 L/R 与惯量 J 限制", cls="tiny", fill=ACC)
    f.text(x0 + 452, bot + 66, "受重力 √(l/g) 限制", cls="tiny", fill=GREEN)
    f.text(x0 + 640, bot + 66, "受内存带宽限制", cls="tiny", fill=GREEN)
    f.save("f00-time-domains.svg")


# ═════════════════════════════════════════════════════════════════════ F-05-1
def f05_sin_theta():
    f = Fig(1000, 430)
    f.head()

    # 左：几何
    cx, cy = 170, 235
    f.line(cx - 110, cy, cx + 110, cy, GREY, 2)
    f.arrow(cx + 104, cy, cx + 118, cy, GREY, 2)
    f.text(cx + 122, cy + 5, "B（转子磁钢）", cls="s", fill=GREY)
    for th, col, lab in [(90, GREEN, "θ=90° 最大"), (45, ACC, ""), (10, RED, "")]:
        r = 78
        ex, ey = cx + r * math.cos(math.radians(th)), cy - r * math.sin(math.radians(th))
        f.arrow(cx, cy, ex, ey, col, 2.5)
    f.arc_note = None
    f.text(cx - 6, cy - 92, "m（定子磁矩）", cls="s", fill=ACC)
    f.circle(cx, cy, 6, INK, INK, 2)
    f.text(cx - 110, cy + 118, "θ = m 与 B 的夹角", cls="tiny")
    f.text(cx - 110, cy + 140, "|τ| = N·I·A·B·sinθ", cls="m")

    # 右：曲线
    ox, oy, W, H = 400, 330, 520, 210
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H - 10, GREY, 1)
    pts = []
    for i in range(181):
        th = math.radians(i)
        pts.append((ox + i / 180 * W, oy - math.sin(th) * H))
    f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), INK, 2.5)
    for deg, lab in [(0, "0°"), (30, "30°"), (90, "90°"), (150, "150°"), (180, "180°")]:
        x = ox + deg / 180 * W
        f.line(x, oy, x, oy + 5, GREY, 1)
        f.text(x, oy + 22, lab, cls="tiny", anchor="middle")
        s = math.sin(math.radians(deg))
        f.line(x, oy, x, oy - s * H, LIGHT, 1, "3,4")
        f.text(x + 4, oy - s * H - 6, f"{s:.2f}", cls="tiny", fill=GREY)
    f.text(ox - 14, oy - H + 4, "1.0", cls="tiny", anchor="end")
    f.text(ox - 14, oy + 4, "0", cls="tiny", anchor="end")
    f.text(ox + W / 2, oy - H - 22, "扭矩保留比例 sinθ", cls="s", anchor="middle")

    # 结论框
    f.rect(400, 96, 520, 60, ACC, "#f4f8fd", 2)
    f.text(414, 120, "θ = 90° 才有最大扭矩；θ → 0° 时力全花在把电机「压扁」上，", cls="m", size=18)
    f.text(414, 142, "　　 一分扭矩不出。FOC 的全部工作 = 让 θ 永远停在 90°。", cls="m", size=18)
    f.save("f05-sin-theta.svg")


# ═════════════════════════════════════════════════════════════════════ F-07-1
def f07_rotating_field():
    f = Fig(1000, 430)
    f.head()

    cx, cy, R = 250, 250, 130
    f.circle(cx, cy, R, LIGHT, "none", 1)
    axes = [("A", 0), ("B", 120), ("C", 240)]
    for name, ang in axes:
        a = math.radians(ang)
        f.arrow(cx - R * math.cos(a), cy + R * math.sin(a),
                cx + R * math.cos(a), cy - R * math.sin(a), GREY, 1.5)
        f.text(cx + (R + 16) * math.cos(a), cy - (R + 16) * math.sin(a) + 5,
               name + " 相绕组轴", cls="s", fill=GREY)
    th = 37
    comps = []
    for name, ang in axes:
        i = math.cos(math.radians(th - ang))
        comps.append((name, i))
        a = math.radians(ang)
        if abs(i) > 0.02:
            f.arrow(cx, cy, cx + i * R * 0.62 * math.cos(a), cy - i * R * 0.62 * math.sin(a),
                    ACC, 2)
    ar = math.radians(th)
    f.arrow(cx, cy, cx + R * 0.95 * math.cos(ar), cy - R * 0.95 * math.sin(ar), RED, 3.5)
    f.text(cx + R * 0.95 * math.cos(ar) + 8, cy - R * 0.95 * math.sin(ar) - 8,
           "合成矢量 F", cls="t", fill=RED)
    f.text(30, 402, "虚线圆 = 幅值恒等于相电流峰值 I（幅值不变变换约定下）。合成矢量的模不随 θ 变，方向 = θ。", cls="s")

    # 右：三相电流波形
    ox, oy, W, H = 560, 250, 400, 120
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy - H, ox, oy + H, GREY, 1)
    cols = {"A": ACC, "B": GREEN, "C": "#8a5a00"}
    for k, (name, off) in enumerate([("A", 0), ("B", -120), ("C", 120)]):
        pts = []
        for i in range(0, 361, 4):
            x = ox + i / 360 * W
            y = oy - math.cos(math.radians(i + off)) * H * 0.9
            pts.append((x, y))
        f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), cols[name], 2)
        f.text(ox + W + 8, oy - math.cos(math.radians(360 + off)) * H * 0.9 + 5,
               name, cls="m", fill=cols[name])
    for i, lab in [(0, "0"), (90, "θ=90°"), (180, "180°"), (270, "270°"), (360, "360°")]:
        f.text(ox + i / 360 * W, oy + H + 22, lab, cls="tiny", anchor="middle")
    f.text(ox, oy - H - 14, "相电流 i（时间差 120°）", cls="s")
    f.text(560, 400, "空间上差 120° 的三个绕组 × 时间上差 120° 的三个正弦 = 一个匀速旋转、模恒定的矢量。", cls="s")
    f.save("f07-rotating-field.svg")


# ═════════════════════════════════════════════════════════════════════ F-08-1
def f08_hexagon():
    f = Fig(1000, 470)
    f.head()

    cx, cy, R = 300, 265, 165
    f.line(cx - R - 40, cy, cx + R + 40, cy, LIGHT, 1)
    f.line(cx, cy - R - 40, cx, cy + R + 40, LIGHT, 1)
    f.text(cx + R + 44, cy + 5, "α", cls="m")
    f.text(cx - 6, cy - R - 46, "β", cls="m")
    pts = []
    for k in range(6):
        a = math.radians(60 * k)
        pts.append((cx + R * math.cos(a), cy - R * math.sin(a)))
    f.poly(pts, ACC, "#f2f7fd", 2.5)
    for k, (px, py) in enumerate(pts):
        f.circle(px, py, 6, ACC, "#fff", 2)
        f.text(px * 1.0 + (px - cx) * 0.13, py + (py - cy) * 0.13,
               f"V{k+1}", cls="m", fill=ACC, anchor="middle")
    f.circle(cx, cy, 6, GREY, GREY, 2)
    f.text(cx + 8, cy + 20, "V0 / V7（零矢量）", cls="tiny", fill=GREY)
    # 内切圆
    r_in = R * math.cos(math.radians(30))
    f.circle(cx, cy, r_in, GREEN, "none", 2, )
    f.parts[-1] = f.parts[-1].replace('stroke-width="2"', 'stroke-width="2" stroke-dasharray="6,4"')
    f.text(cx - r_in * 0.72, cy - r_in * 0.72, "SVPWM 线性区", cls="s", fill=GREEN)
    f.text(cx - r_in * 0.72, cy - r_in * 0.72 + 20, "V_相 ≤ V_bus/√3", cls="m", fill=GREEN, size=16)
    # SPWM 圆
    f.circle(cx, cy, R / 2, RED, "none", 2)
    f.parts[-1] = f.parts[-1].replace('stroke-width="2"', 'stroke-width="2" stroke-dasharray="3,3"')
    f.text(cx + R * 0.16, cy + R * 0.36, "SPWM 只到这里 V_bus/2", cls="tiny", fill=RED)
    # 目标矢量
    a = math.radians(24)
    f.arrow(cx, cy, cx + r_in * 0.86 * math.cos(a), cy - r_in * 0.86 * math.sin(a), INK, 3)
    f.text(cx + r_in * 0.9 * math.cos(a) + 6, cy - r_in * 0.9 * math.sin(a), "V_target", cls="m")

    # 右：伏秒平衡 + 包络
    f.rect(620, 96, 350, 130, ACC, "#f7fafd", 2)
    f.text(636, 122, "伏秒平衡（PWM 合法性的全部依据）", cls="t", size=19)
    f.text(636, 152, "V = L · di/dt", cls="m")
    f.text(636, 176, "⇒ Δi = (V/L)·Δt　只记得 ∫Vdt", cls="m")
    f.text(636, 206, "V_平均 = d · V_bus，d = t_on / T", cls="m")

    ox, oy, W, H = 640, 400, 310, 120
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H - 8, GREY, 1)
    f.arrow(ox, oy, ox + W * 0.98, oy - H, RED, 2, "5,4")
    f.text(ox + W * 0.55, oy - H * 0.92, "电压受限", cls="tiny", fill=RED)
    f.text(ox + 10, oy - H * 0.35, "τ 峰值", cls="tiny", fill=ACC)
    f.line(ox, oy - H * 0.86, ox + W * 0.30, oy - H * 0.86, ACC, 2.5)
    f.line(ox + W * 0.30, oy - H * 0.86, ox + W * 0.98, oy, ACC, 2.5)
    f.text(ox - 4, oy + 22, "0", cls="tiny", anchor="end")
    f.text(ox + W, oy + 22, "ω", cls="tiny", anchor="middle")
    f.text(ox + W * 0.30, oy - H * 0.86 - 10, "X1（T-N 折点）", cls="tiny", anchor="middle")
    f.text(ox + 6, oy - H - 20, "两个角点不可同时达到", cls="s", fill=RED)
    f.save("f08-voltage-hexagon.svg")


# ═════════════════════════════════════════════════════════════════════ F-09-1
def f09_two_lowpass():
    f = Fig(1000, 400)
    f.head()

    ox = 60
    # (a) PWM 方波
    def wave(x0, y0, w, h, kind):
        p = []
        if kind == "pwm":
            for i in range(12):
                xx = x0 + i * (w / 12)
                d = 0.5 + 0.34 * math.sin(i / 12 * 2 * math.pi)
                p.append((xx, y0)); p.append((xx, y0 - h * d))
                p.append((xx + w / 24, y0 - h * d)); p.append((xx + w / 24, y0))
        elif kind == "ripple":
            for i in range(60):
                xx = x0 + i * (w / 60)
                base = math.sin(i / 60 * 2 * math.pi * 0.5) * h * 0.06
                tri = ((i % 5) / 5 - 0.5) * h * 0.16
                p.append((xx, y0 - h * 0.5 - base - tri))
        else:
            for i in range(60):
                xx = x0 + i * (w / 60)
                p.append((xx, y0 - h * 0.5 - math.sin(i / 60 * math.pi) * h * 0.42))
        return "M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in p)

    W, H = 250, 150
    for i, (title, kind, sub, col) in enumerate([
        ("① 施加的电压（20 kHz 方波）", "pwm", "只有开和关", RED),
        ("② 绕组电流（电感积分之后）", "ripple", "平均 + 纹波", ACC),
        ("③ 转子转速（惯量再积分一次）", "smooth", "几乎看不到开关", GREEN)]):
        x0 = ox + i * 320
        y0 = 250
        f.line(x0, y0, x0 + W, y0, GREY, 1)
        f.path(wave(x0, y0, W, H, kind), col, 2 if kind != "pwm" else 2)
        f.text(x0, 100, title, cls="t", size=18)
        f.text(x0, y0 + 26, sub, cls="s", fill=col)
        if i < 2:
            f.arrow(x0 + W + 6, y0 - H / 2, x0 + W + 60, y0 - H / 2, GREY, 2)
            f.text(x0 + W + 8, y0 - H / 2 - 12, "∫ dt", cls="m", fill=GREY)
    f.text(ox, 340, "τ_e = L/R（零点几毫秒）　→　τ_m = J·R/k_t²（几毫秒）　→　角度再积分一次（几十毫秒起）", cls="m")
    f.text(ox, 368, "每一级都比上一级慢 10–100 倍。所以「平均」不是近似技巧，是这台机器本身的结构。", cls="s")
    f.save("f09-two-lowpass.svg")


# ═════════════════════════════════════════════════════════════════════ F-10-1
def f10_clarke_park():
    f = Fig(1000, 520)
    f.head()

    # 左：几何
    cx, cy, R = 190, 300, 120
    f.line(cx - R - 20, cy, cx + R + 20, cy, GREY, 1)
    f.line(cx, cy - R - 20, cx, cy + R + 20, GREY, 1)
    f.text(cx + R + 24, cy + 5, "α", cls="m"); f.text(cx + 4, cy - R - 24, "β", cls="m")
    for ang, col, lab in [(0, GREY, "d 轴（磁钢方向）"), (90, RED, "q 轴（做功方向）")]:
        a = math.radians(ang)
        f.arrow(cx, cy, cx + R * math.cos(a), cy - R * math.sin(a), col, 2.5)
        f.text(cx + (R + 6) * math.cos(a) - 30, cy - (R + 6) * math.sin(a) - 8, lab, cls="tiny", fill=col)
    for ang in (120, 240):
        a = math.radians(ang)
        f.line(cx - R * 0.8 * math.cos(a), cy + R * 0.8 * math.sin(a),
               cx + R * 0.8 * math.cos(a), cy - R * 0.8 * math.sin(a), LIGHT, 1, "4,4")
    th = 62
    a = math.radians(th)
    f.arrow(cx, cy, cx + R * 0.92 * math.cos(a), cy - R * 0.92 * math.sin(a), INK, 3.5)
    f.text(cx + R * 0.95 * math.cos(a) + 6, cy - R * 0.95 * math.sin(a), "i 矢量", cls="m")
    # 投影
    f.line(cx + R * 0.92 * math.cos(a), cy - R * 0.92 * math.sin(a),
           R * 0.92 * math.cos(a) + cx, cy, ACC, 1.5, "4,3")
    f.line(cx + R * 0.92 * math.cos(a), cy - R * 0.92 * math.sin(a),
           cx, cy - R * 0.92 * math.sin(a), GREEN, 1.5, "4,3")
    f.text(cx + R * 0.5, cy + 20, "i_d", cls="m", fill=ACC, anchor="middle")
    f.text(cx - 22, cy - R * 0.5, "i_q", cls="m", fill=GREEN, anchor="middle")
    f.text(60, 440, "i_d = i_α cosθ + i_β sinθ　（沿磁钢，不产生扭矩）", cls="m", size=17)
    f.text(60, 466, "i_q = −i_α sinθ + i_β cosθ　（垂直磁钢，全部做功）", cls="m", size=17)
    f.text(60, 496, "τ = (3/2)·p·λ_m·i_q　⇒　要多少扭矩，就给多少 i_q", cls="t", size=18, fill=RED)

    # 右：信号流（作者那张图的正确版）
    x0, y0, bw, bh, gap = 520, 90, 200, 46, 12
    boxes = [
        ("q_ref, dq_ref, τ_ff", GREY), ("混合公式 → τ_cmd", ACC),
        ("τ_cmd ÷ k_t = i_q_ref", ACC), ("电流 PI ×2 (i_d,i_q)", RED),
        ("逆 Park", RED), ("逆 Clarke / SVPWM 配时", RED),
        ("6 × MOSFET 半桥", GREEN), ("三相绕组 → 磁场 → 扭矩", GREEN),
    ]
    for i, (lab, col) in enumerate(boxes):
        y = y0 + i * (bh + gap)
        f.rect(x0, y, bw, bh, col, "#fbfbfd", 2)
        f.text(x0 + bw / 2, y + bh / 2 + 6, lab, cls="m", fill=col, anchor="middle", size=16)
        if i < len(boxes) - 1:
            f.arrow(x0 + bw / 2, y + bh, x0 + bw / 2, y + bh + gap, col, 1.6)
    fx = x0 + bw + 130
    f.rect(fx, y0 + 3 * (bh + gap), 130, bh * 2 + gap, GREY, "#f7f7f7", 2)
    f.text(fx + 65, y0 + 3 * (bh + gap) + 34, "Park", cls="m", anchor="middle", fill=GREY)
    f.text(fx + 65, y0 + 3 * (bh + gap) + 58, "Clarke", cls="m", anchor="middle", fill=GREY)
    f.arrow(fx, y0 + 4 * (bh + gap) + 12, x0 + bw, y0 + 4 * (bh + gap) + 12, GREY, 1.6)
    f.rect(fx, y0 + 6 * (bh + gap), 130, bh, GREY, "#f7f7f7", 2)
    f.text(fx + 65, y0 + 6 * (bh + gap) + 28, "编码器 θ", cls="m", anchor="middle", fill=GREY)
    f.parts.append(f'<path d="M {fx+65} {y0+6*(bh+gap)} V {y0+18} H {x0+bw+8}" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5,4"/>')
    f.text(fx + 72, y0 + 6 * (bh + gap) - 22, "θ 送进每一次正/逆变换", cls="tiny", fill=RED)
    f.text(520, 500, "θ 错 5° ⇒ 扭矩只掉 0.38%，但 8.7% 的电流变成无用的磁化电流（第 10 章）。", cls="s", fill=RED)
    f.save("f10-clarke-park.svg")


# ═════════════════════════════════════════════════════════════════════ F-12-1
def f12_cascade_vs_formula():
    f = Fig(1000, 430)
    f.head()

    def box(x, y, w, h, lab, col, sub=""):
        f.rect(x, y, w, h, col, "#fbfcfe", 2)
        f.text(x + w / 2, y + h / 2 - 2, lab, cls="t", fill=col, anchor="middle", size=17)
        if sub:
            f.text(x + w / 2, y + h / 2 + 18, sub, cls="tiny", fill=GREY, anchor="middle")

    # 左：级联
    f.text(60, 78, "A　级联三环（教科书 / ODrive 官方口径）", cls="h", size=19)
    y = 100
    for i, (lab, sub) in enumerate([("位置环", "P 或 PI"), ("速度环", "PI"), ("电流环", "PI")]):
        box(60, y + i * 78, 150, 56, lab, ACC, sub)
        if i < 2:
            f.arrow(135, y + i * 78 + 56, 135, y + (i + 1) * 78, ACC, 2)
            f.text(145, y + i * 78 + 68, "给定", cls="tiny", fill=GREY)
    box(250, y + 2 * 78, 130, 56, "SVPWM", GREEN)
    box(410, y + 2 * 78, 110, 56, "电机", GREEN)
    f.arrow(210, y + 2 * 78 + 28, 250, y + 2 * 78 + 28, ACC, 2)
    f.arrow(380, y + 2 * 78 + 28, 410, y + 2 * 78 + 28, GREEN, 2)
    f.parts.append(f'<path d="M 465 {y+2*78+56} V {y+30} H 210" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="5,4"/>')
    f.text(300, y + 18, "反馈：编码器 / 电流", cls="tiny", fill=GREY)
    f.text(60, y + 3 * 78 + 6, "三个环、六个整定参数；积分项会替你兜住稳态误差。", cls="s")

    # 右：单公式
    f.text(560, 78, "B　单条混合公式（宇树 IM6014 官方口径）", cls="h", size=19)
    f.rect(560, 100, 400, 92, RED, "#fdf6f6", 2)
    f.text(576, 132, "τ = τ_ff + k_p(q_des − q) + k_d(ω_des − ω)", cls="m", fill=RED, size=19)
    f.text(576, 158, "官方称 hybrid control formula；位置/速度模式只是", cls="tiny", fill=GREY)
    f.text(576, 178, "对同一式子做 parameter trimming，不是加环。", cls="tiny", fill=GREY)
    box(620, 214, 140, 56, "电流环", RED, "只有比例增益")
    box(800, 214, 130, 56, "FOC→桥", GREEN)
    f.arrow(760, 242, 800, 242, RED, 2)
    f.arrow(760, 192, 760, 214, RED, 2)
    f.text(560, 300, "τ ÷ k_t = i_q_ref　⇒　没有独立的速度环，也没有位置环。", cls="s")
    f.rect(560, 320, 400, 66, RED, "#fff", 2, dash="5,4")
    f.text(576, 346, "后果：纯比例必有静差 ⇒", cls="t", size=18, fill=RED)
    f.text(576, 370, "　　 前馈 τ_ff 不是可选项，是唯一能消静差的手段", cls="s", fill=RED)
    f.text(60, 366, "级联的「内环 ≥ 外环 5–10 倍」判据在 B 里只作用一处：", cls="s")
    f.text(60, 392, "混合公式（kHz 量级）→ 电流环（kHz 量级）。位置与速度不再是环。", cls="s")
    f.save("f12-cascade-vs-formula.svg")


# ═════════════════════════════════════════════════════════════════════ F-14-1
def f14_backlash_floor():
    f = Fig(1000, 400)
    f.head()

    ox, oy, W = 90, 300, 820
    f.line(ox, oy, ox + W, oy, GREY, 1)
    bars = [("电机端 15 bit 编码器", 0.010986, ACC, "0.011°"),
            ("折算到输出端（÷20.58）", 0.000534, GREEN, "0.00053°"),
            ("谐波减速器背隙（Z1 官方 6 弧分）", 0.1, RED, "0.1°")]
    import math as _m
    def X(v):
        lo, hi = _m.log10(0.0002), _m.log10(0.5)
        return ox + (_m.log10(v) - lo) / (hi - lo) * W
    for i, (lab, v, col, txt) in enumerate(bars):
        y = oy - 40 - i * 62
        f.rect(X(0.00025), y - 16, X(v) - X(0.00025), 32, col, col + "22", 2)
        f.text(ox, y - 28, lab, cls="s")
        f.text(X(v) + 8, y + 6, txt, cls="m", fill=col)
    for v, lab in [(0.0005, "0.0005"), (0.005, "0.005"), (0.05, "0.05"), (0.5, "0.5")]:
        f.line(X(v), oy, X(v), oy + 6, GREY, 1)
        f.text(X(v), oy + 24, lab, cls="tiny", anchor="middle")
    f.text(ox + W / 2, oy + 48, "角度误差（°，对数刻度）", cls="s", anchor="middle")
    f.line(X(0.000534), oy - 164, X(0.1), oy - 164, GREY, 1.5)
    f.text((X(0.000534) + X(0.1)) / 2, oy - 176, "187 倍", cls="t", fill=RED, anchor="middle")
    f.text(ox, oy - 210, "把编码器从 15 bit 换到 20 bit，一点用都没有——地板不在那里。", cls="h", size=19)
    f.save("f14-backlash-floor.svg")


# ═════════════════════════════════════════════════════════════════════ F-15-1
def f15_one_motor_two_gears():
    f = Fig(1000, 400)
    f.head()

    f.rect(60, 90, 250, 120, ACC, "#f3f8fd", 2)
    f.text(80, 122, "N7520 电机", cls="h")
    f.text(80, 148, "rotor 惯量 0.489e-4 kg·m²", cls="m", size=16)
    f.text(80, 170, "满扭矩转子侧 ≈ 6.16 N·m", cls="m", size=16, fill=RED)
    f.text(80, 192, "（φ75 × 叠厚 20 mm）", cls="tiny", fill=GREY)

    for i, (ratio, out, y, joints) in enumerate([
            ("14.3 : 1", "88 N·m", 88, "髋俯仰 · 髋偏航 · 腰偏航"),
            ("22.5 : 1", "139 N·m", 178, "髋侧摆 · 膝")]):
        f.rect(400, y, 170, 78, GREEN, "#f4faf6", 2)
        f.text(485, y + 32, "减速 " + ratio, cls="t", fill=GREEN, anchor="middle", size=18)
        f.text(485, y + 58, "输出 " + out, cls="m", fill=GREEN, anchor="middle")
        f.arrow(310, 150, 400, y + 39, ACC, 2)
        f.text(600, y + 45, joints, cls="s")
        f.line(570, y + 39, 596, y + 39, GREY, 1.5)

    f.rect(640, 250, 320, 110, RED, "#fdf6f6", 2)
    f.text(656, 278, "反推回转子侧：", cls="t", size=18, fill=RED)
    f.text(656, 306, "88 ÷ 14.3 = 6.15 N·m", cls="m")
    f.text(656, 330, "139 ÷ 22.5 = 6.18 N·m　→ 差 0.4%", cls="m", fill=RED)
    f.arrow(485, 256, 640, 300, GREY, 1.5, "5,4")

    f.text(60, 250, "型号名里那个数字就是减速比。两档输出差 58%，", cls="s")
    f.text(60, 274, "而差异全部来自一级齿轮——电机是同一颗。", cls="s")
    f.text(60, 320, "另外两档：N5020-16 → 25 N·m（肩/肘/腕滚/踝），", cls="s")
    f.text(60, 344, "　　　　W4010-25 → 5 N·m（腕俯仰/偏航）。", cls="s")
    f.text(60, 382, "手腕只有 5 N·m：它不需要扛重量，只需要把掌摆到该在的朝向。", cls="t", size=18)
    f.save("f15-one-motor-two-gears.svg")


# ═════════════════════════════════════════════════════════════════════ F-18-1
def f18_three_ceilings():
    f = Fig(1000, 420)
    f.head()

    ox, oy, W, H = 130, 330, 700, 230
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    f.text(ox + W / 2, oy + 30, "刚度 kp（N·m/rad，对数）", cls="s", anchor="middle")
    f.text(ox - 14, oy - H / 2, "可实现的刚度上限", cls="s", anchor="middle", size=16)

    def LX(v):
        lo, hi = math.log10(1), math.log10(1e6)
        return ox + (math.log10(v) - lo) / (hi - lo) * W
    for v, lab in [(1, "1"), (10, "10"), (100, "100"), (1e3, "1k"), (1e4, "10k"), (1e5, "100k"), (1e6, "1M")]:
        f.line(LX(v), oy, LX(v), oy + 5, GREY, 1)
        f.text(LX(v), oy + 22, lab, cls="tiny", anchor="middle")

    ceilings = [("① 协议量程", 25.6, RED, "M8010 kp ≤ 25.599"),
                ("①′ 协议量程", 410.7, RED, "IM6014 kp ≤ 410.7"),
                ("② 执行器饱和", 3970, ACC, "τ_max ÷ 允许误差 2°"),
                ("③ 稳定性 ω_n", 79000, GREEN, "= J·(ω_c/5)²，J=0.05")]
    for i, (lab, v, col, note) in enumerate(ceilings):
        y = oy - 40 - i * 46
        f.line(ox, y, LX(v), y, col, 3)
        f.parts.append(f'<path d="M {LX(v)} {y} h 14" stroke="{col}" stroke-width="3"/>')
        f.text(ox + 8, y - 8, lab, cls="m", fill=col, size=17)
        f.text(LX(v) + 20, y + 5, note, cls="tiny", fill=col)
    f.rect(600, 96, 340, 84, GREEN, "#f4faf6", 2)
    f.text(616, 122, "官方数已验（附录 C.2a）：", cls="t", size=18, fill=GREEN)
    f.text(616, 148, "ω_n = √(kp/armature) = 62.8 rad/s", cls="m")
    f.text(616, 170, "四档电机全部 = 10.00 Hz，偏差 0.0%", cls="m", fill=GREEN)
    f.text(30, 400, "小关节先撞①，大关节先撞②；③ 在高惯量负载 + 硬位置控制时才咬人。", cls="s")
    f.save("f18-three-ceilings.svg")


# ═════════════════════════════════════════════════════════════════════ F-21-1
def f21_pipeline():
    f = Fig(1000, 400)
    f.head()

    steps = [("Train", "Isaac Gym / Isaac Lab\n1000+ 并行环境", ACC),
             ("Play", "同一仿真器回放", ACC),
             ("Sim2Sim", "换到 MuJoCo\n专抓「拟合了仿真器」", RED),
             ("Sim2Real", "rt/lowcmd 500 Hz\n策略 50 Hz", GREEN)]
    for i, (lab, sub, col) in enumerate(steps):
        x = 50 + i * 240
        f.rect(x, 80, 200, 90, col, "#fbfcfe", 2)
        f.text(x + 100, 110, lab, cls="h", fill=col, anchor="middle")
        for j, ln in enumerate(sub.split("\n")):
            f.text(x + 100, 134 + j * 20, ln, cls="tiny", anchor="middle")
        if i < 3:
            f.arrow(x + 200, 125, x + 240, 125, GREY, 2)
    f.text(50, 200, "Sim2Sim 看起来傻：已经能走了为什么再换个仿真器走一遍？因为它防的是「策略学到的是仿真器的接触算法，不是走路」。", cls="s")

    f.rect(50, 226, 430, 130, GREEN, "#f4faf6", 2)
    f.text(66, 252, "官方 EventCfg 里【有】的随机化", cls="t", size=18, fill=GREEN)
    for j, s in enumerate(["地面摩擦　　[0.1, 1.25]", "附加质量　　[−1, +3] kg",
                           "随机推力　　每 5 s / 1.5 m/s", "观测噪声 + 5 帧历史"]):
        f.text(66, 280 + j * 20, s, cls="m", size=16)
    f.rect(520, 226, 430, 130, RED, "#fdf6f6", 2)
    f.text(536, 252, "官方【没有】随机化的（= 本书前面证明过的不确定源）", cls="t", size=17, fill=RED)
    for j, s in enumerate(["k_t 随温度漂（第 04、36 章）", "通信延迟（第 12、27 章）",
                           "关节摩擦 Fs/Fd 的变化（第 14 章）", "连杆惯量（第 18 章）"]):
        f.text(536, 280 + j * 20, "✗　" + s, cls="m", size=16, fill=RED)
    f.text(50, 380, "随机化清单就是这个策略的能力边界声明。四个 ✗ 恰好对应第 5 部的热、总线、磨损、漂移。", cls="h", size=19)
    f.save("f21-pipeline-dr.svg")


# ═════════════════════════════════════════════════════════════════════ F-38-1
def f38_compound():
    f = Fig(1000, 400)
    f.head()

    ox, oy, W, H = 110, 320, 700, 240
    f.line(ox, oy, ox + W, oy, GREY, 1)
    f.line(ox, oy, ox, oy - H, GREY, 1)
    for i, lab in enumerate(["0", "20", "40", "60", "80", "100"]):
        x = ox + i / 5 * W
        f.line(x, oy, x, oy + 5, GREY, 1)
        f.text(x, oy + 22, lab, cls="tiny", anchor="middle")
    f.text(ox + W / 2, oy + 46, "连续动作次数 N", cls="s", anchor="middle")
    for i, lab in enumerate(["0", "25", "50", "75", "100"]):
        y = oy - i / 4 * H
        f.line(ox - 5, y, ox, y, GREY, 1)
        f.text(ox - 12, y + 5, lab, cls="tiny", anchor="end")
    f.text(ox - 46, oy - H / 2, "全对概率 %", cls="s", anchor="middle", size=16)

    for p, col, dash in [(0.999, GREEN, None), (0.99, ACC, None), (0.95, RED, "6,4"), (0.90, "#8a5a00", "3,3")]:
        pts = []
        for n in range(0, 101):
            pts.append((ox + n / 100 * W, oy - (p ** n) * H))
        f.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), col, 2.5, dash=dash)
        v = p ** 100 * 100
        f.text(ox + W + 10, oy - min(max(p ** 100, 0.004), 1) * H + 5,
               f"{p:.0%} → {v:.1f}%" if v >= 0.05 else f"{p:.0%} → ≈0", cls="m", fill=col, size=16)
    f.rect(560, 90, 340, 78, RED, "#fdf6f6", 2)
    f.text(576, 116, "一条流水线一小时 ≈ 60–120 次动作。", cls="s")
    f.text(576, 140, "「95% 成功率」= 每小时必然出错一次以上。", cls="t", size=18, fill=RED)
    f.text(110, 380, "若要求 1000 次动作整体成功 90%，需要单次 99.99%——那不是模型能力，是系统工程。", cls="s")
    f.save("f38-compound-decay.svg")


# ═════════════════════════════════════════════════════════════════════ F-16-1
def f16_pendulum():
    f = Fig(1000, 420)
    f.head()

    # 左：四足
    f.line(60, 300, 440, 300, GREY, 2)
    f.rect(140, 190, 220, 50, ACC, "#f3f8fd", 2)
    for x in (165, 220, 300, 355):
        f.line(x, 240, x, 300, ACC, 3)
        f.circle(x, 300, 5, ACC, ACC, 2)
    f.text(250, 178, "四足：重力走结构骨架", cls="t", anchor="middle", fill=ACC)
    f.text(250, 330, "支撑多边形 = 四个接触点的凸包", cls="s", anchor="middle")
    f.text(250, 354, "站立时关节力矩 ≈ 0（抱闸锁住即可）", cls="s", anchor="middle", fill=GREEN)

    # 右：双足
    f.line(560, 300, 940, 300, GREY, 2)
    f.rect(700, 150, 60, 100, RED, "#fdf6f6", 2)
    f.line(715, 250, 700, 300, RED, 3); f.line(745, 250, 760, 300, RED, 3)
    f.circle(700, 300, 5, RED, RED, 2); f.circle(760, 300, 5, RED, RED, 2)
    f.parts.append(f'<ellipse cx="700" cy="302" rx="26" ry="7" fill="{RED}22" stroke="{RED}" stroke-width="1.5"/>')
    f.parts.append(f'<ellipse cx="760" cy="302" rx="26" ry="7" fill="{RED}22" stroke="{RED}" stroke-width="1.5"/>')
    f.arrow(730, 150, 730, 100, GREY, 2)
    f.text(738, 128, "重心", cls="tiny", fill=GREY)
    f.parts.append(f'<path d="M 730 150 L 700 300" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5,4" fill="none"/>')
    f.text(640, 240, "正在往前倒", cls="tiny", fill=RED)
    f.text(730, 330, "支撑多边形 = 两只脚掌（走路时只剩一只）", cls="s", anchor="middle")
    f.text(730, 354, "每个腿腰关节必须每一毫秒都在闭环出力", cls="s", anchor="middle", fill=RED)

    f.rect(300, 372, 400, 40, ACC, "#fff", 2)
    f.text(500, 398, "τ = √(l/g)：G1 髋高 0.66 m ⇒ 0.259 s 内必须做点什么", cls="t", anchor="middle", size=18)
    f.text(60, 415, "", cls="tiny")
    f.save("f16-quad-vs-biped.svg")


def main():
    for fn in (f00_time_domains, f05_sin_theta, f07_rotating_field, f08_hexagon,
               f09_two_lowpass, f10_clarke_park, f12_cascade_vs_formula,
               f14_backlash_floor, f15_one_motor_two_gears, f18_three_ceilings,
               f21_pipeline, f38_compound, f16_pendulum):
        fn()
    print(f"\n共 {len(list(OUT.glob('*.svg')))} 幅 SVG 在 assets/fig/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
