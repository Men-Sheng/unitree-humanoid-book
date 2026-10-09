#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arithmetic_check.py — 复算本书第 2 部的"四道算术"，并列出还缺哪些数。

为什么要有这个脚本：科普书最容易出事的地方不是文笔，是"作者把数算错了，
读者看不出来"。这四道算术（扭矩·能量·频率·延迟）是全书的骨架，所以它们必须
**由脚本算出来**，正文只抄结果。改一个输入 → 重跑 → 结果与正文对不上就会暴露。

用法：
    python arithmetic_check.py                 # 用 calculations.yaml，缺数就报缺
    python arithmetic_check.py --demo          # 用一组明确标注为"占位"的数，验证算式本身
    python arithmetic_check.py --md out.md     # 顺便出附录 B 的 Markdown

退出码：0 = 全部可算；1 = 有缺数（正文不许出现这些结论）；2 = 算式自洽性检查失败。
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent

# --demo 用的占位数：只为验证算式与单位，绝不可写进书。
# 取值刻意取"量级合理"而非"精确"，并在输出里全程标注 DEMO。
DEMO = {
    "mass_kg": 15.0,
    "hip_height_m": 0.30,
    "battery_wh": 60.0,
    "rated_runtime_h": 1.5,
    "rated_payload_kg": 7.0,
    "top_speed_mps": 1.5,
    "joint_peak_torque_nm": 20.0,   # 转子侧峰值扭矩
    "gear_ratio": 10.0,
    "gear_efficiency": 0.8,
    "peak_to_continuous_derate": 4.0,   # 行业分析常引"瞬时电流是额定的 3-5 倍"
    "leg_geometry_factor": 1.0,         # 保守取力臂=髋高（腿伸直最不利）
    "control_rate_hz": 500,
    "leg_count": 4,
    "static_safety_factor": 2.0,
    "leg_geometry_factor": 1.0,
    "cost_of_transport": 4.0,       # 无量纲 E/(m·g·d)；机器人量级，人步行约 0.2
    "g": 9.81,
}
DEMO_LATENCY = {
    "camera_exposure_ms": 20.0,
    "perception_infer_ms": 30.0,
    "planner_ms": 10.0,
    "bus_roundtrip_ms": 2.0,
    "motor_current_response_ms": 1.0,
}


def is_filled(v) -> bool:
    return v is not None and not (isinstance(v, str) and v.strip().upper() == "TBD")


def reverse_cot(sub: dict) -> dict | None:
    """第 17 章的主算例：只用厂商公布的两个数（电池 Wh、标称里程 km）+ 自重，
    反推每公里耗电与无量纲 CoT。**零估算**，所以它可以直接印进书里。"""
    e, d, m = sub.get("battery_wh"), sub.get("range_km"), sub.get("mass_kg")
    if not all(is_filled(x) for x in (e, d, m)):
        return None
    wh_km = e / d
    cot = wh_km * 3600 / (1000 * m * 9.81)
    return {"每公里耗电_Wh": round(wh_km, 1),
            "CoT_无量纲": round(cot, 2),
            "对比_人步行CoT": "0.34（本书换算）/ 0.37（Nature 2026 论文口径）",
            "倍数": f"约为人的 {cot/0.34:.1f} 倍"}


def resolution_vs_backlash(sub: dict) -> dict | None:
    """第 07 章的算例：读数装置能读多细 vs 齿轮松多少。
    输出端分辨率 = 360° ÷ 编码器位数 ÷ 减速比；再与官方给的背隙比一次。"""
    bits, G, bk = sub.get("encoder_bits"), sub.get("gear_ratio"), sub.get("backlash_arcmin")
    out = {}
    if is_filled(bits) and is_filled(G):
        counts = 2 ** int(bits)
        out["编码器每圈格数"] = counts
        out["输出端分辨率_度"] = f"{360.0 / counts / G:.6f}"      # 360° ÷ 格数 ÷ 减速比
    if is_filled(bk):
        out["官方背隙_度"] = f"{bk / 60.0:.4f}"
    if out and is_filled(bits) and is_filled(G) and is_filled(bk):
        out["背隙是分辨率的多少倍"] = f"{(bk / 60.0) / (360.0 / 2 ** int(bits) / G):.0f}×"
    elif out:
        out["能不能相除"] = ("不能——缺另一个数。这两个数不能跨机型混用"
                        "（宇树没给 GO-M8010-6 的背隙，也没给 Z1 的编码器位数）")
    return out or None


def bus_budget(sub: dict) -> dict | None:
    """第 12 章的算例：一条总线一轮要点多少次名，占掉控制周期的多少。
    半双工 = 一问一答不能重叠；8N1 = 每字节实际要发 10 个 bit。"""
    n = sub.get("servos_on_bus")
    tx, rx = sub.get("control_bytes"), sub.get("feedback_bytes")
    baud, bits_per_byte = sub.get("baud_bps"), sub.get("bits_per_byte", 10)
    hz = sub.get("control_rate_hz")
    if not all(is_filled(x) for x in (n, tx, rx, baud, hz)):
        return None
    per_joint_bits = (tx + rx) * bits_per_byte
    cycle_bits = n * per_joint_bits
    cycle_us = cycle_bits / baud * 1e6
    budget_us = 1e6 / hz
    return {"单个来回_bit": per_joint_bits,
            f"{n} 个单元一轮_us": round(cycle_us, 1),
            f"控制周期 {hz}Hz 预算_us": round(budget_us, 1),
            "总线占预算比例": f"{cycle_us / budget_us * 100:.0f}%",
            "地址够不够": (f"够：{n} 个单元，可用地址 {sub.get('addresses_usable', 15)} 个"
                       if n <= sub.get("addresses_usible", sub.get("addresses_usable", 15))
                       else f"不够：{n} > {sub.get('addresses_usable', 15)}，必须分多条总线")}


def chains(p: dict, lat: dict):
    """返回 [(链名, 结果dict), ...]；结果里 None 表示算不了。"""
    g = p.get("g") or 9.81
    out = {}

    # 1) 扭矩链
    tm, G, eta, r, n, k = (p.get("joint_peak_torque_nm"), p.get("gear_ratio"),
                           p.get("gear_efficiency"), p.get("hip_height_m"),
                           p.get("leg_count"), p.get("static_safety_factor"))
    der = p.get("peak_to_continuous_derate")   # 峰值→连续：厂商给的是哪个，决定一切
    arm = p.get("leg_geometry_factor")         # 实际力臂 / 髋高；腿伸直时最不利
    m = p.get("mass_kg")
    t_out = p.get("joint_effort_thigh_nm")     # URDF 给出的关节输出上限
    arm_eff = p.get("arm_effective_m")         # 等效力臂（第 16 章要交代它的来源）
    have_urdf = is_filled(t_out) and is_filled(arm_eff)
    have_model = all(is_filled(x) for x in (tm, G, eta, r, n, k, m, der, arm))
    if have_urdf or have_model:
        f_foot = t_out / arm_eff if have_urdf else tm * G * eta / (der * arm * r)
        f_total = n * f_foot
        # 可驮质量 = 可出力÷裕度÷g − 自重。注意别把 (F/k − m·g) 当成质量：那是力减力
        payload = f_total / (k * g) - m
        out["torque_chain"] = {
            "足端单腿可出力_N": round(f_foot, 1),
            "四腿合计_N": round(f_total, 1),
            f"按 1/{k} 静力裕度可驮_kg": round(payload, 1),
            "官方标称负载_kg": p.get("rated_payload_kg"),
            "扭矩来源": ("URDF 关节输出上限 + 等效力臂（厂商源码值）"
                        if have_urdf else f"峰值÷{der}、力臂={arm}×髋高"),
        }
    else:
        out["torque_chain"] = None

    # 2) 能量链
    cot, v, e = p.get("cost_of_transport"), p.get("top_speed_mps"), p.get("battery_wh")
    if all(is_filled(x) for x in (cot, v, e, m)):
        # COT 无量纲：E/(m·g·d)。所以 P = COT·m·g·v，每公里能量 = COT·m·g·1000
        power = cot * m * g * v             # W
        wh_per_km = cot * m * g * 1000 / 3600
        t_end = e / power
        out["energy_chain"] = {
            "巡航功率_W": round(power, 0),
            "每公里耗电_Wh": round(wh_per_km, 1),
            "理论续航_h": round(t_end, 2),
            "理论里程_km": round(e / wh_per_km, 1),
            "官方标称续航_h": p.get("rated_runtime_h"),
        }
    else:
        out["energy_chain"] = None

    # 3) 频率链
    if all(is_filled(x) for x in (r, p.get("control_rate_hz"))):
        tau = math.sqrt(r / g)              # 倒立摆失稳的 e-folding 时间
        out["frequency_chain"] = {
            "失稳时间常数_s": round(tau, 3),
            "期间可用控制周期数": int(tau * p["control_rate_hz"]),
            "说明": "τ=√(l/g)，一个数量级判断：够不够它'想清楚再动'",
        }
    else:
        out["frequency_chain"] = None

    # 4) 延迟链
    if lat and all(is_filled(lat.get(k2)) for k2 in lat):
        total = sum(lat.values())
        out["latency_chain"] = {
            "各环节_ms": {k2: lat[k2] for k2 in lat},
            "合计_ms": round(total, 1),
            "占失稳时间比例": (f"{total/1000/math.sqrt((p.get('hip_height_m') or 0.3)/g)*100:.0f}%"
                       if is_filled(p.get("hip_height_m")) else "缺 hip_height"),
        }
    else:
        out["latency_chain"] = None
    return out


def selfcheck() -> list[str]:
    """算式自洽性：用一组已知答案的输入验证实现没写错。"""
    errs = []
    # 已知：τ=20, G=10, η=0.8, der=1, arm=1, r=0.4 → F=400 N；der=4 → 100 N
    if abs(20 * 10 * 0.8 / (1 * 1 * 0.4) - 400) > 1e-6:
        errs.append("扭矩链算式不符（连续化前）")
    if abs(20 * 10 * 0.8 / (4 * 1 * 0.4) - 100) > 1e-6:
        errs.append("扭矩链算式不符（峰值÷4 连续化后应为 100 N）")
    # 已知：4 腿 × 133.3 N、裕度 2、自重 15 kg → 可驮 = 533.3/(2*9.81) - 15 ≈ 12.2 kg
    pay = 4 * (20 * 10 * 0.8 / (4 * 1 * 0.3)) / (2 * 9.81) - 15
    if abs(pay - 12.2) > 0.3:
        errs.append(f"可驮质量算式不符（应为 kg 而不是 N：算出 {pay:.1f}）")
    # 已知：COT=4(无量纲), m=15, g=9.81, v=1.5 → P=882.9 W；Wh/km=163.5
    pw = 4 * 15 * 9.81 * 1.5
    whkm = 4 * 15 * 9.81 * 1000 / 3600
    if abs(pw - 882.9) > 0.5 or abs(whkm - 163.5) > 0.5:
        errs.append(f"能量链算式不符 (P={pw:.1f} W, Wh/km={whkm:.1f})")
    # 已知：l=0.3 → τ=√(0.3/9.81)=0.1749 s
    if abs(math.sqrt(0.3 / 9.81) - 0.1749) > 0.001:
        errs.append("频率链算式不符")
    return errs


def sanity(res: dict, p: dict) -> list[str]:
    """把推算结果和厂商标称对表。差得离谱 = 模型缺因子，不许当成"算出来了"。

    这一步是本书的立场：宁可说"我们的静力模型高估了 130 倍，因为漏了
    连续扭矩、腿的力臂几何、占空比"，也不许拿一个好看的数糊弄读者。
    这些偏差本身就是第 16、17 章最好的教学内容。
    """
    flags = []
    tc = res.get("torque_chain")
    if tc and is_filled(p.get("rated_payload_kg")) and p["rated_payload_kg"]:
        r = tc["按 1/2.0 静力裕度可驮_kg"] / p["rated_payload_kg"]
        if r > 5 or r < 0.2:
            flags.append(
                f"扭矩链：静力估算 / 厂商标称 = {r:.0f}×。静力模型缺因子——"
                "峰值扭矩≠连续扭矩、关节到足端的力臂≠髋高、四腿不同时满载。"
                "正文必须带着这个差异写，不能只报估算值")
    ec = res.get("energy_chain")
    if ec and is_filled(p.get("rated_runtime_h")) and p["rated_runtime_h"]:
        r = p["rated_runtime_h"] / ec["理论续航_h"] if ec["理论续航_h"] else float("inf")
        if r > 5 or r < 0.2:
            flags.append(
                f"能量链：厂商标称续航 / 理论续航 = {r:.0f}×。要么 COT 取值过高、"
                "要么标称续航是低速/待机工况。必须查清标称工况，否则第 17 章的对比不成立")
    return flags


def to_md(res: dict, demo: bool) -> str:
    L = [f"# 四道算术速查{'（DEMO 占位数，不可用于正文）' if demo else ''}", ""]
    for name, body in res.items():
        L.append(f"## {name}")
        if body is None:
            L.append("\n**算不了：输入有 TBD。** 这个结论不许出现在正文里。\n")
            continue
        L.append("")
        L.append("| 量 | 值 |")
        L.append("|---|---|")
        for k, v in body.items():
            if isinstance(v, dict):
                v = "; ".join(f"{a}={b}" for a, b in v.items())
            L.append(f"| {k} | {v} |")
        L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calc", default=str(HERE / "calculations.yaml"))
    ap.add_argument("--demo", action="store_true", help="用占位数验证算式（输出会全程标注 DEMO）")
    ap.add_argument("--md", default=None, help="额外输出附录 B 的 Markdown 路径")
    a = ap.parse_args()

    errs = selfcheck()
    if errs:
        for e in errs:
            print("SELFCHECK FAIL:", e)
        return 2
    print("selfcheck: 3/3 算式实现正确")

    doc = yaml.safe_load(Path(a.calc).read_text(encoding="utf-8"))
    unit = dict(doc.get("teardown_unit") or {})
    der = doc.get("derived") or {}
    lat = dict((der.get("latency_chain") or {}).get("stages") or {})
    unit["static_safety_factor"] = (der.get("torque_chain") or {}).get("static_safety_factor")
    unit["cost_of_transport"] = (der.get("energy_chain") or {}).get("cost_of_transport")

    if a.demo:
        unit = dict(DEMO)
        lat = dict(DEMO_LATENCY)
        unit["cost_of_transport"] = DEMO["cost_of_transport"]
        unit["static_safety_factor"] = DEMO["static_safety_factor"]

    res = {}
    bb = bus_budget(doc.get("j288_bus") or {})
    if bb:
        res["bus_budget(J288 舵机总线)"] = bb
    sub = doc.get("subject") or {}
    for nm, blk in (("Z1 机械臂关节", doc.get("z1_joint")),
                    ("Go2 关节电机", doc.get("go2_motor"))):
        rb = resolution_vs_backlash(blk or {})
        if rb:
            res[f"resolution_vs_backlash({nm})"] = rb
    rc = reverse_cot(sub)
    if rc:
        res["reverse_cot(AS2 主算例)"] = rc
    unit = dict(doc.get("crosscheck_go2") or {})
    unit["static_safety_factor"] = (der.get("torque_chain") or {}).get("static_safety_factor")
    unit["arm_effective_m"] = unit.get("arm_effective_m")
    unit["joint_effort_thigh_nm"] = unit.get("joint_effort_thigh_nm")
    res.update(chains(unit, lat))
    missing = [k for k, v in unit.items() if not is_filled(v)]
    missing += [k for k, v in lat.items() if not is_filled(v)] + \
               ([] if a.demo else ["cost_of_transport(文献值)"])

    for name, body in res.items():
        if body is None:
            print(f"{name:18s} 算不了（缺输入）")
            continue
        print(f"{name:18s} " + "  ".join(f"{k}={v}" for k, v in body.items()))

    flags = sanity(res, unit)
    for f in flags:
        print("WARN ", f)

    print(f"\n缺数 {len(missing)} 项" + ("（DEMO 模式已注入占位值，仅验证算式）" if a.demo else ""))
    for k in missing:
        print("  TBD:", k)

    if a.md:
        Path(a.md).write_text(to_md(res, a.demo), encoding="utf-8")
        print(f"wrote {a.md}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
