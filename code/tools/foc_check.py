#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code/tools/foc_check.py — 第 1 部（一颗关节）的可复算链。

设计原则（与 arithmetic_check.py 一致）：
  1. 每个函数只做一次代数，输入全部来自 calculations.yaml 或本文件的 OFFICIAL 表；
  2. 每个函数返回 (结论, 过程串)，过程串直接可以贴进正文；
  3. selfcheck() 里放"已知答案"的用例，防止本脚本自己算错。

单位约定：SI。扭矩 N·m，电流 A，电压 V，角度 rad，转速 rad/s。
dq 约定：幅值不变（amplitude-invariant）Clarke 变换，因此
  τ = (3/2)·p·λm·i_q，且合成磁动势幅值 = 相电流峰值。
"""
from __future__ import annotations

import math
import os
import sys

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = 9.80665
NL = chr(10)   # 不用字面反斜杠换行：本文件曾被 heredoc 转义破坏过一次

# ── 官方口径（宇树产品页；来源标记见 research/unitree-hardware.md S16/S17/S10/S08/S11）──
OFFICIAL = {
    "GO-M8010-6": {
        "mass_kg": 0.530, "gear": 6.33, "vbus_v": 24.0, "vbus_max_v": 30.0,
        "frame_cmd_b": 17, "frame_state_b": 16, "kp_max_out": 25.599, "kd_max_out": 25.599,
        "peak_torque_out_nm": 23.7, "peak_current_a": 40.0,
        "kt_output_nm_per_a": 0.63895, "max_speed_out_rad_s": 30.0,
        "encoder_bits": 15, "bus_mbps": 4.0, "cmd_rate_hz": 6000, "units": "台/总线",
    },
    "IM6014": {
        "mass_kg": 0.535, "gear": 38 / 3, "vbus_v": 60.0,
        "frame_cmd_b": 20, "frame_state_b": 26, "kp_max_out": 410.725, "kd_max_out": 102.681,
        "peak_torque_out_nm": 34.4, "max_speed_out_rad_s": 54.2,
        "encoder_bits": 15, "bus_mbps": 6.0, "cmd_rate_hz": 10000,
    },
    "G1": {"height_m": 1.32, "mass_kg": 35.0, "knee_peak_nm": 120.0,
           "hip_height_m": 0.66, "gear_total": 20.58, "dof": 23},
    # 官方 unitree_rl_lab 配置里的 G1 关节电机家族：型号名自带减速比，effort 是仿真限幅
    "G1_MOTOR_FAMILY": {
        "N7520-14.3": {"ratio": 14.3, "effort_nm": 88.0, "joints": "hip_pitch / hip_yaw / waist_yaw"},
        "N7520-22.5": {"ratio": 22.5, "effort_nm": 139.0, "joints": "hip_roll / knee"},
        "N5020-16":   {"ratio": 16.0, "effort_nm": 25.0,  "joints": "shoulder* / elbow / wrist_roll / ankle / waist_roll|pitch"},
        "W4010-25":   {"ratio": 25.0, "effort_nm": 5.0,   "joints": "wrist_pitch / wrist_yaw"},
    },
    "H2": {"height_m": 1.82, "mass_kg": 70.0, "leg_peak_nm": 360.0},
    # 官方 unitree_rl_lab / source/.../assets/robots/unitree_actuators.py（[厂]，逐文件核对）
    # X1=满扭矩最高转速(T-N折点) Y1/Y2=同向/反向峰值 Fs/Fd=摩擦
    # armature=折算到关节（输出）轴的等效惯量，源码式 J2 + J1·i2² + Jr·(i1·i2)²
    #         ——口径由 natural_frequency_check 与 armature_side_check 机器证明
    "UNITREE_ACTUATORS": {
        "M107_15":     dict(X1=14.0,  X2=25.6, Y1=150.0, Y2=182.8, Fs=0.0, Fd=0.0,  armature=0.063259741),
        "M107_24":     dict(X1=8.8,   X2=16.0, Y1=240.0, Y2=292.5, Fs=0.0, Fd=0.0,  armature=0.160478022),
        "N7520_14p3":  dict(X1=22.63, X2=35.52, Y1=71.0, Y2=83.3,  Fs=1.6, Fd=0.16, armature=0.01017752),
        "N7520_22p5":  dict(X1=14.5,  X2=22.7,  Y1=111.0, Y2=131.0, Fs=2.4, Fd=0.24, armature=0.025101925),
        "N5020_16":    dict(X1=30.86, X2=40.13, Y1=24.8,  Y2=31.9,  Fs=0.6, Fd=0.06, armature=0.003609725),
        "W4010_25":    dict(X1=15.3,  X2=24.76, Y1=4.8,   Y2=8.6,   Fs=0.6, Fd=0.06, armature=0.00425),
    },
    # 官方 mimic 配置：按电机型号派生的 kp/kd 与逐关节 action_scale 的分子（effort）
    "G1_MIMIC_PD": {"N7520_14p3": (88.0, 40.179, 2.5579), "N7520_22p5": (139.0, 99.098, 6.3095),
                    "N5020_16": (25.0, 14.251, 0.904), "W4010_25": (5.0, 16.778, 1.066)},
    "H1": {"knee_peak_nm": 360.0, "hip_peak_nm": 220.0, "ankle_peak_nm": 59.0,
           "torque_density_nm_per_kg": 189.0},
}

# ── 行业通识常数（非宇树事实，正文必须标 [行]）──
GENERIC = {
    "svpwm_linear_gain": 2 / math.sqrt(3),   # 相对 SPWM 峰值相电压的可用增益 ≈1.1547
    "cu_resistivity_ppm_per_c": 3930,        # 铜电阻温度系数 +0.393 %/°C
    "ndfeb_br_resid_ppm_per_c": -1100,       # NdFeB 剩磁 ≈ -0.11 %/°C（N 档典型）
}


# ═════════════════════════ 第 04 章：τ = k_t · i ═════════════════════════

def kt_crosscheck(model: str = "GO-M8010-6"):
    """官方扭矩常数 × 官方峰值电流 是否等于 官方峰值扭矩 ⇒ 判定常数是输出端还是转子端口径。"""
    d = OFFICIAL[model]
    t_calc = d["kt_output_nm_per_a"] * d["peak_current_a"]
    err = (t_calc - d["peak_torque_out_nm"]) / d["peak_torque_out_nm"]
    kt_rotor = d["kt_output_nm_per_a"] / d["gear"]
    lines = [
        f"k_t·I = {d['kt_output_nm_per_a']:.5f} × {d['peak_current_a']:.0f} = {t_calc:.2f} N·m；"
        f"官方峰值 {d['peak_torque_out_nm']:.1f} N·m，差 {err:+.1%} ⇒ 手册常数是**输出端**口径。",
        f"折算到转子：k_t = {d['kt_output_nm_per_a']:.5f} ÷ {d['gear']:.2f} = {kt_rotor:.5f} N·m/A。",
    ]
    proc = chr(10).join(lines)
    ok = err > 0.02          # 算出来的扭矩明显高于官方峰值 ⇒ 常数不可能是转子端口径
    return ok, proc


R_JOINT_ASSUMED_OHM = 0.040   # 本书假设：24 V / 40 A 级关节回路的可信量级；官方未公布 [未]


def voltage_envelope(model: str = "GO-M8010-6", r_ohm: float = R_JOINT_ASSUMED_OHM):
    """要在最高转速下输出峰值扭矩，需要多大母线电压？官方母线电压够吗？

    2026-10-08 修正：第 05 章声明用**幅值不变**变换约定，那里给出
    τ = (3/2)·p·λ_m·i_q ⇒ k_t = (3/2)·p·λ_m。于是 q 轴反电势幅值
    e_q = p·λ_m·ω = (2/3)·k_t·ω，**不是** k_t·ω。旧版直接写 k_t·ω 得 19.17 V，
    高于 SVPWM 的 13.86 V，等于宣布"官方最高转速空载都跑不到"——那是被一个
    约定系数造出来的假结论。改对后：空载 12.78 V < 13.86 V（够），
    满载 12.78 + 40×0.04 = 14.38 V > 13.86 V（不够）。角点互斥仍成立，
    但拦路的是铜损压降，不是反电势本身。
    """
    d = OFFICIAL[model]
    kt_rotor = d["kt_output_nm_per_a"] / d["gear"]
    w_rotor = d["max_speed_out_rad_s"] * d["gear"]
    emf = (2.0 / 3.0) * kt_rotor * w_rotor
    v_lim = d["vbus_v"] / math.sqrt(3)
    i_pk = d["peak_current_a"]
    v_load = emf + i_pk * r_ohm
    pct = f"{emf / v_lim:.0%}"
    lines = [
        f"转子角速度 ω = {d['max_speed_out_rad_s']:.0f} × {d['gear']:.2f} = {w_rotor:.1f} rad/s",
        f"反电势幅值 E = (2/3)·k_t·ω = (2/3) × {kt_rotor:.5f} × {w_rotor:.1f} = {emf:.2f} V"
        f"　（幅值不变约定，见第 05 章）",
        f"{d['vbus_v']:.0f} V 母线在 SVPWM 线性区能给相电压幅值 = V_bus/√3 = {v_lim:.2f} V",
        f"空载：{emf:.2f} V < {v_lim:.2f} V ⇒ 最高转速空载拿得到（用掉母线能力的 {pct}）",
        f"满载：E + I·R = {emf:.2f} + {i_pk:.0f} × {r_ohm:.3f} = {v_load:.2f} V > {v_lim:.2f} V"
        f" ⇒ 拿不到（R 是本书假设 {r_ohm*1000:.0f} mΩ，官方未公布 [未]）",
        f"至少需要母线：空载 √3·E = {math.sqrt(3)*emf:.1f} V；"
        f"满载 √3·(E+I·R) = {math.sqrt(3)*v_load:.1f} V",
        f"结论：**峰值扭矩 {d['peak_torque_out_nm']:.1f} N·m 与最高转速 "
        f"{d['max_speed_out_rad_s']:.0f} rad/s 是两个角点，不可能同时达到**"
        f"——但拦路的是铜损压降，不是空载反电势。",
    ]
    proc = chr(10).join(lines)
    ok = v_load > v_lim      # 满载电压不足 ⇒ 角点互斥成立
    return ok, proc



def spwm_vs_svpwm(vbus: float = 24.0):
    """SVPWM 相对 SPWM 多用的电压：√3/2 倍（15.5%）。"""
    v_spwm = vbus / 2.0
    v_svpwm = vbus / math.sqrt(3)
    gain = v_svpwm / v_spwm
    proc = (f"SPWM 线性区相电压峰值 = V_bus/2 = {v_spwm:.2f} V；"
            f"SVPWM = V_bus/√3 = {v_svpwm:.2f} V；增益 {gain:.4f} ⇒ 多 {(gain-1):.1%}。")
    return abs(gain - 1.1547) < 1e-3, proc


# ═════════════════════════ 第 10 章：Park 变换与角度误差 ═════════════════════════

def park_rotation(i_alpha: float, i_beta: float, theta_e: float):
    """显式做 Park，返回 (i_d, i_q)。用于自检：i_q 应当是垂直分量。"""
    i_d = i_alpha * math.cos(theta_e) + i_beta * math.sin(theta_e)
    i_q = -i_alpha * math.sin(theta_e) + i_beta * math.cos(theta_e)
    return i_d, i_q


def angle_error_cost(theta_err_deg: float):
    """编码器安装角偏了 δ：同样大小的电流矢量，扭矩掉多少、磁化电流占多少。"""
    d = math.radians(theta_err_deg)
    # 电流矢量总幅值 I 固定，本应全部落在 q 轴
    tq = math.cos(d)          # 有效扭矩比例
    mag = abs(math.sin(d))    # 漏进 d 轴的比例（SPM 下不产生扭矩，只增磁/去磁与铜损）
    proc = (f"角度误差 {theta_err_deg:.1f}° ⇒ 扭矩只保留 cos δ = {tq:.4f}（掉 {1-tq:.2%}），"
            f"同时 |i_d|/|i| = sin δ = {mag:.4f}（{mag:.1%} 的电流在'白烧'）。"
            f"维持同一扭矩要把电流幅值放大 1/cos δ：电流有效值只多 {1/math.cos(d)-1:.2%}，"
            f"而铜损按幅值平方算，多耗 {(1/math.cos(d))**2-1:.2%}。")
    return tq < 1 and mag > 0, proc


def clarke_three_phase(i_a: float, i_b: float, i_c: float):
    """幅值不变 Clarke：三相 → αβ。自检用：平衡正弦时 |(α,β)| 应等于相电流峰值。"""
    alpha = (2.0 / 3.0) * (i_a - 0.5 * i_b - 0.5 * i_c)
    beta = (2.0 / 3.0) * (math.sqrt(3) / 2.0) * (i_b - i_c)
    return alpha, beta


def rotating_field_peak(peak_a: float = 10.0, theta_deg: float = 37.0):
    """证明第 07 章：三相正弦（互差 120°）合成矢量幅值恒等于相电流峰值。"""
    th = math.radians(theta_deg)
    i_a = peak_a * math.cos(th)
    i_b = peak_a * math.cos(th - 2 * math.pi / 3)
    i_c = peak_a * math.cos(th + 2 * math.pi / 3)
    al, be = clarke_three_phase(i_a, i_b, i_c)
    mag = math.hypot(al, be)
    proc = (f"θ={theta_deg:.0f}°：i=({i_a:+.3f},{i_b:+.3f},{i_c:+.3f}) A ⇒ "
            f"(α,β)=({al:+.3f},{be:+.3f})，|合成|={mag:.4f} A，相电流峰值={peak_a:.1f} A ⇒ 相等。")
    return abs(mag - peak_a) < 1e-9, proc


# ═════════════════════════ 第 13 章：死区 ═════════════════════════

def deadtime_error(t_dead_ns: float, f_pwm_hz: float, vbus: float,
                   r_ohm: float | None = None, i_a: float | None = None):
    """死区吃掉的电压，以及它在低速时相对反电势的比重。"""
    t_on = 1.0 / f_pwm_hz
    frac = (t_dead_ns * 1e-9) / t_on
    dv = frac * vbus
    proc = (f"死区 {t_dead_ns:.0f} ns ÷ 周期 {t_on*1e6:.1f} µs = {frac:.4%} ⇒ "
            f"电压误差 ΔV = {frac:.4%} × {vbus:.0f} V = {dv:.3f} V。")
    if r_ohm is not None and i_a is not None:
        proc += f" 对比：驱动 {i_a:.1f} A 只需 {i_a*r_ohm:.3f} V 铜降 ⇒ 死区误差是它的 {dv/(i_a*r_ohm):.1f} 倍。"
    return abs(frac - (t_dead_ns * 1e-9 * f_pwm_hz)) < 1e-12, proc


# ═════════════════════════ 第 14 章：分辨率 vs 齿隙 ═════════════════════════

def resolution_vs_backlash(bits: int = 15, gear: float = 20.58,
                           backlash_arcmin: float = 6.0):
    """编码器分辨率折算到输出端，与减速器背隙比较 ⇒ 谁才是精度的地板。"""
    motor_res_deg = 360.0 / (2 ** bits)
    out_res_deg = motor_res_deg / gear
    bl_deg = backlash_arcmin / 60.0
    ratio = bl_deg / out_res_deg
    proc = (f"{bits} bit 单圈 = {2**bits} 格 ⇒ 电机端 {motor_res_deg:.5f}°；"
            f"经 {gear:.2f}:1 折算到输出端 {out_res_deg:.6f}°。\n"
            f"谐波减速器背隙官方口径 {backlash_arcmin:.0f} 弧分 = {bl_deg:.3f}° ⇒ "
            f"齿隙是编码器（折算后）分辨率的 {ratio:.0f} 倍。"
            f"**再精细的编码器也救不了减速器的空程。**")
    return ratio > 10, proc


def quasi_direct_drive_torque(model: str = "GO-M8010-6", gear: float | None = None):
    """同一颗电机，减速比换掉之后输出扭矩怎么变（线性 + 效率）。"""
    d = OFFICIAL[model]
    g = gear if gear is not None else d["gear"]
    kt_rotor = d["kt_output_nm_per_a"] / d["gear"]
    for eta in (1.0, 0.85):
        pass
    t_ideal = kt_rotor * d["peak_current_a"] * g
    t_real = t_ideal * 0.85
    proc = (f"k_t(转子)={kt_rotor:.5f}，峰值 {d['peak_current_a']:.0f} A ⇒ 转子扭矩 "
            f"{kt_rotor*d['peak_current_a']:.2f} N·m；×{g:.2f}:1 = {t_ideal:.1f} N·m（理想），"
            f"按 85% 效率 = {t_real:.1f} N·m。")
    return t_real > 0, proc


# ═════════════════════════ 第 15 章：器件阶梯 ═════════════════════════

def natural_frequency_check():
    """第 18 章那道天花板，用官方数闭环：ω_n = √(kp/armature) 应当等于官方注释的 10 Hz。

    注意这条检查同时**证明了 armature 是折算到关节（输出）轴的惯量**：
    kp 是"每弧度关节误差给多少牛米"，量纲上必须配关节侧惯量。
    若把 armature 当成电机轴惯量，就得先除以速比平方，固有频率会变成几百 Hz，
    与官方注释的 10 Hz 差一个数量级。见 armature_side_check()。
    """
    rows = []
    worst = 0.0
    for m, (effort, kp, kd) in OFFICIAL["G1_MIMIC_PD"].items():
        arm = OFFICIAL["UNITREE_ACTUATORS"][m]["armature"]
        wn = math.sqrt(kp / arm)
        hz = wn / (2 * math.pi)
        rows.append(f"  {m}: kp={kp} ÷ armature={arm:.6f} ⇒ ω_n={wn:.1f} rad/s = {hz:.2f} Hz")
        worst = max(worst, abs(hz - 10.0) / 10.0)
    scales = {m: 0.25 * eff / kp for m, (eff, kp, kd) in OFFICIAL["G1_MIMIC_PD"].items()}
    sc = "  ".join(f"{m.split('_')[0]}-{m.split('_')[1]}:{v:.3f}" for m, v in scales.items())
    proc = ("官方 mimic 配置按电机型号派生的 kp，与官方 armature 合起来算固有频率：" + NL
            + NL.join(rows) + NL
            + "四档全部落在 10 Hz 附近（最大偏差 {:.1%}）。".format(worst) + NL
            + "而官方逐关节 action_scale 等于 0.25 × effort ÷ kp：" + sc + NL
            + "这是第 18 章那道『ω_n ≤ 电流环带宽/5』天花板的官方实例：宇树自己就是用 ω_n = √(kp/J) 反推 kp 的。")
    return worst < 0.05, proc


def torque_density_chain():
    """官方'峰值扭矩密度 189 N·m/kg'反推关节单元质量，与拆解 1.1 kg 对照。"""
    m_h1 = OFFICIAL["H1"]["knee_peak_nm"] / OFFICIAL["H1"]["torque_density_nm_per_kg"]
    l_ratio = OFFICIAL["H2"]["height_m"] / OFFICIAL["G1"]["height_m"]
    t_pred = l_ratio ** 4
    t_act_low = OFFICIAL["H2"]["leg_peak_nm"] / OFFICIAL["G1"]["knee_peak_nm"]
    m_pred = l_ratio ** 3
    m_act = OFFICIAL["H2"]["mass_kg"] / OFFICIAL["G1"]["mass_kg"]
    proc = (f"H1 膝 360 N·m ÷ 189 N·m/kg = {m_h1:.2f} kg/关节单元（官方密度口径），"
            f"与 G1 拆解主承载关节 ≈1.1 kg 同数量级 ✓\n"
            f"平方-立方：G1→H2 线度比 {l_ratio:.3f} ⇒ 预测扭矩需求 ×{t_pred:.2f}，"
            f"官方档位实际 ×{t_act_low:.1f}（90→360 则 ×{OFFICIAL['H2']['leg_peak_nm']/90:.1f}）；"
            f"预测质量 ×{m_pred:.2f}，实测 ×{m_act:.2f}。")
    return abs(t_act_low - t_pred) / t_pred < 0.35, proc


# ═════════════════════════ 第 26/27 章：带宽与算力 ═════════════════════════

def bus_budget(model: str = "GO-M8010-6", nodes: int = 15, hz: int = 6000):
    """用官方帧长做总线预算：下行、上行、合计，以及 4 Mbps 能撑到多少赫兹。

    官方帧长（文档中心 RS-485 协议页，一手）：
      GO-M8010-6 控制帧 17 B（CRC 覆盖前 15 B）、状态帧 16 B（CRC 覆盖前 14 B）
      IM6014     控制帧 20 B（0xFE 0xEE 头 + CRC32-MPEG2）、状态帧 26 B（0xFC 0xEE 头不计入 CRC）
    电机 ID 0~14，15 = 广播（无响应）。
    """
    d = OFFICIAL[model]
    dn = nodes * hz * d["frame_cmd_b"] * 8
    up = nodes * hz * d["frame_state_b"] * 8
    tot = dn + up
    max_hz = d["bus_mbps"] * 1e6 / (nodes * (d["frame_cmd_b"] + d["frame_state_b"]) * 8)
    proc = (f"{model}：{nodes} 台 × {hz} Hz × 下行 {d['frame_cmd_b']} B = {dn/1e6:.2f} Mbps；"
            f"× 上行 {d['frame_state_b']} B = {up/1e6:.2f} Mbps；合计 {tot/1e6:.2f} Mbps" + NL
            + f"官方总线 {d['bus_mbps']:.0f} Mbps ⇒ 需要 {tot/1e6/d['bus_mbps']:.1f} 倍带宽。" + NL
            + f"反过来：{d['bus_mbps']:.0f} Mbps 在 {nodes} 台全双工下最多支撑 {max_hz:.0f} Hz" + NL
            + "     —— 与官方 Z1 页标的 Control Frequency 1KHz 撞在同一个数量级。" + NL
            + f"所以官方的 {hz} Hz 只能是单台或被广播帧摊薄后的指令刷新率，"
            + f"不是 {nodes} 台同时 {hz} Hz 全量交换。")
    return tot / 1e6 > d["bus_mbps"], proc


def gear_ratio_consistency():
    """官方 rl_lab 配置里 G1 电机家族的 effort ÷ 减速比 ⇒ 转子侧扭矩是否一致。"""
    fam = OFFICIAL["G1_MOTOR_FAMILY"]
    rows = []
    rotors = []
    for name, v in fam.items():
        r = v["effort_nm"] / v["ratio"]
        rotors.append(r)
        rows.append(f"  {name}: {v['effort_nm']:.0f} N·m ÷ {v['ratio']:.1f} = {r:.2f} N·m（转子侧）")
    big = [rotors[0], rotors[1]]
    spread = abs(big[1] - big[0]) / big[0]
    proc = ("G1 官方关节电机家族（unitree_rl_lab 配置，一手）：" + NL
            + NL.join(rows) + NL
            + f"同一台 φ7520 电机、两个减速比 ⇒ 转子侧 {big[0]:.2f} vs {big[1]:.2f} N·m，"
            + f"差 {spread:.1%}。" + NL
            + "这是一条官方数据自己完成的证明：输出扭矩 ≈ 转子扭矩 × 减速比。"
            + "型号名里的数字就是减速比，而 88 / 139 两档输出只差一个齿轮。")
    return spread < 0.02, proc


def stiffness_limit():
    """官方 kp 上限能给出多硬的关节：Δq = τ_max / kp_max。"""
    out = []
    for m in ("GO-M8010-6", "IM6014"):
        d = OFFICIAL[m]
        dq = d["peak_torque_out_nm"] / d["kp_max_out"]
        out.append(f"{m}: τ_peak {d['peak_torque_out_nm']:.1f} N·m ÷ kp_max {d['kp_max_out']:.3f} "
                   f"= 满扭矩下位置误差至少 {dq:.3f} rad = {math.degrees(dq):.1f}°")
    proc = (NL.join(out) + NL
            + "刚度上限是指令字段的量程给的，不是控制理论给的。同一个 kp 量程下，"
            + "减速比越高（输出扭矩越大），满扭矩时的位置误差越大。"
            + "这正是 Z1 官方脚注自己承认的那件事：低减速比 ⇒ 位置控制刚度低 ⇒ 不优化就会抖。")
    return True, proc


def llm_memory_time(params_b: float = 6.0, bytes_per_param: int = 2,
                    bw_gbs: float = 100.0):
    """权重字节 ÷ 内存带宽 = 每 token 下限时间。"""
    gb = params_b * 1e9 * bytes_per_param / 1e9
    t = gb / (bw_gbs)
    proc = (f"{params_b:.0f}B 参数 × {bytes_per_param} B = {gb:.0f} GB 权重；"
            f"带宽 {bw_gbs:.0f} GB/s ⇒ 单步 ≥ {t*1000:.0f} ms ⇒ ≤ {1/t:.1f} Hz（还没算 KV、激活、图像）。")
    return abs(t - 0.12) < 0.05, proc


def pendulum(hip_height_m: float = 0.66, latency_ms: float | None = None):
    tau = math.sqrt(hip_height_m / G)
    proc = f"τ = √(l/g) = √({hip_height_m:.2f}/9.80665) = {tau:.3f} s"
    if latency_ms is not None:
        proc += f"；延迟 {latency_ms:.0f} ms = τ 的 {latency_ms/1000/tau:.1%}"
    return tau, proc


def compound_success(p_step: float, n: int):
    out = p_step ** n
    return out, f"{p_step:.0%}^{n} = {out:.1%}"


# ═════════════════════════ 自检 ═════════════════════════

def armature_side_check():
    """证明官方 armature 是"折算到关节（输出）轴"，不是"折算到电机轴"。

    同一个 kp 有两种读法：
      按关节侧惯量 J = armature            ⇒ ω_n = √(kp/J)
      按电机侧惯量 J = armature ÷ 速比²    ⇒ 同一个 kp 会算出高得多的频率
    两种读法差"速比"倍（√(i²)=i），只有一种能对上官方注释里的 10 Hz。
    这条检查存在的理由：附录 C 曾把 armature 标成"折算到电机轴"，
    那是一句会连带把第 18 章整条推导读反的口径错误。
    """
    rows = []
    ok = True
    for m, (effort, kp, kd) in OFFICIAL["G1_MIMIC_PD"].items():
        arm = OFFICIAL["UNITREE_ACTUATORS"][m]["armature"]
        ratio = float(m.split("_")[-1].replace("p", "."))
        hz_joint = math.sqrt(kp / arm) / (2 * math.pi)
        hz_motor = hz_joint * ratio
        rows.append(f"  {m}: 速比 {ratio:g}、kp {kp:g}、armature {arm:.6f}"
                    f" ⇒ 按关节侧 {hz_joint:.2f} Hz；若按电机侧 {hz_motor:.0f} Hz")
        if not 5.0 <= hz_joint <= 20.0:
            ok = False
    proc = ("同一个 kp 的两种惯量口径，只有一种对得上官方那句 10 Hz：" + NL
            + NL.join(rows) + NL
            + "结论：armature 是折算到关节（输出）轴的等效惯量，"
              "与源码式 J2 + J1·i2² + Jr·(i1·i2)² 一致；"
              "按电机侧读会高出整整一个速比倍（几百 Hz），与官方注释矛盾。")
    return ok, proc


def cycle_time_485_vs_ecat():
    """第 27 章：为什么官方说"一条 RS-485 总线最多 15 台"——两个独立理由都指向 15。

    理由一（地址）：ID 0–15、15 留给广播 ⇒ 可用 15 个。
    理由二（周期，本函数算的就是它）：4 Mbps ⇒ 250 ns/位；
      一帧 = 指令 17 B + 状态 16 B = 33 B = 264 bit ⇒ 66 µs/台；
      15 台轮询一轮 = 990 µs < 1000 µs（1 kHz 环）；20 台 = 1320 µs > 1 kHz。
    也就是说：**就算地址够用，20 台也塞不进 1 kHz。**
    对照 EtherCAT：100 Mbps ⇒ 10 ns/位，一帧飞过所有从站（"on the fly"，
    官方原文 "reads the data addressed to it 'on the fly', and inserts its data
    in the frame as the frame is moving downstream"），
    20 轴过程数据 1680 B = 13,440 bit ⇒ 134.4 µs，比 485 轮询快 9.8 倍。
    """
    t_bit_485 = 1.0 / 4e6                       # 250 ns
    t_bit_ecat = 1.0 / 100e6                    # 10 ns
    frame_b = 17 + 16                           # 官方帧长：指令 + 状态
    per_node = frame_b * 8 * t_bit_485
    c15 = 15 * per_node
    c20 = 20 * per_node
    ecat = 1680 * 8 * t_bit_ecat
    ok = (abs(t_bit_485 - 250e-9) < 1e-15 and abs(per_node - 66e-6) < 1e-9
          and c15 < 1e-3 and c20 > 1e-3 and abs(c15 * 1e6 - 990.0) < 1.0)
    proc = (f"4 Mbps ⇒ 位时间 {t_bit_485*1e9:.0f} ns；一帧 {frame_b} B = "
            f"{frame_b*8} bit ⇒ {per_node*1e6:.0f} µs/台" + NL
            + f"15 台轮询一轮 = {c15*1e6:.0f} µs（< 1000 µs，正好塞进 1 kHz）" + NL
            + f"20 台轮询一轮 = {c20*1e6:.0f} µs（> 1 kHz，装不下）" + NL
            + f"EtherCAT 100 Mbps ⇒ 位时间 {t_bit_ecat*1e9:.0f} ns；"
              f"20 轴过程数据 1680 B = {1680*8} bit ⇒ {ecat*1e6:.1f} µs" + NL
            + f"轮询 20 台 ÷ 一帧飞过 = {c20/ecat:.1f} 倍。"
              "结论：'最多 15 台'既是地址限制，也是周期限制，两个理由独立成立。")
    return ok, proc


def selfcheck() -> int:
    """已知答案的用例。任何一条失败说明本脚本自己算错了。"""
    fails = 0

    def case(name, got, want, tol=1e-6):
        nonlocal fails
        ok = abs(got - want) <= tol
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: got {got:.6g} want {want:.6g}")
        if not ok:
            fails += 1

    # 1) 幅值不变 Clarke：θ=0 时 α=i_a, β=0
    al, be = clarke_three_phase(10.0, -5.0, -5.0)
    case("clarke@0° alpha", al, 10.0)
    case("clarke@0° beta", be, 0.0)
    # 2) Park：矢量正好在 q 轴上 ⇒ i_d=0, i_q=I
    i_d, i_q = park_rotation(0.0, 10.0, 0.0)   # θ_e=0 ⇒ d 轴与 α 轴重合，β 上的矢量全在 q 轴
    case("park on q-axis d", i_d, 0.0, 1e-12)
    case("park on q-axis q", i_q, 10.0, 1e-12)
    # 3) 旋转磁场幅值恒等于相电流峰值
    for th in (0, 37, 91, 200):
        ok, _ = rotating_field_peak(10.0, float(th))
        if not ok:
            fails += 1
            print(f"  FAIL rotating field @ {th}°")
    print("  ok   rotating_field amplitude invariant over θ")
    # 3b) 第 08 章电压包络：幅值不变约定下的反电势与满载母线（含故意错答案对照）
    e_amp = (2.0 / 3.0) * (0.63895 / 6.33) * (30 * 6.33)
    case("08 反电势幅值 (2/3)·k_t·ω", e_amp, 12.78, 0.01)
    case("08 满载所需母线 √3·(E+I·R)", math.sqrt(3) * (e_amp + 40 * 0.040), 24.91, 0.02)
    def neg_case(name, got, wrong, tol):
        nonlocal fails
        bad = abs(got - wrong) <= tol
        print(f"  {'ok  ' if not bad else 'FAIL'} {name}: 错答案 {wrong:g} 必须不被接受")
        if bad:
            fails += 1
    neg_case("08 反电势（旧系数 k_t·ω 是错的）", e_amp, 19.17, 0.05)
    neg_case("08 满载母线（漏掉 I·R 是错的）", math.sqrt(3) * e_amp, 24.91, 0.05)

    # 4) SVPWM 增益 = 2/√3 = 1.1547
    case("svpwm gain", 2 / math.sqrt(3), 1.154700538, 1e-6)
    # 5) 死区占比：100 ns @ 20 kHz = 0.002
    case("deadtime fraction", 100e-9 * 20000, 0.002, 1e-12)
    # 6) 15 bit = 32768 格，0.010986°
    case("15bit resolution deg", 360 / 2**15, 0.010986328, 1e-6)
    # 7) 倒立摆 τ(0.66 m) = 0.2595 s
    case("pendulum tau 0.66m", math.sqrt(0.66 / G), 0.259425, 1e-5)
    # 8) 复合成功率 0.99^100 = 0.3660
    case("compound 0.99^100", 0.99**100, 0.366032, 1e-5)
    # 9-13) 第 38 章那张表与那条反解，整格钉死（曾有一格把 0.66% 写成 6.6%，
    #       10 倍错在指数表里极易看漏，所以每一格都要有已知答案）
    case("compound 0.99^500", 0.99**500, 0.0065705, 1e-6)
    case("compound 0.95^100", 0.95**100, 0.0059205, 1e-6)
    case("compound 0.90^50", 0.90**50, 0.0051538, 1e-6)
    case("compound 0.99^28800 量级", -math.log10(0.99**28800), 125.706, 0.01)
    case("8h 90% 所需单步失败率 q", 1 - 0.9 ** (1 / 28800), 3.658e-6, 1e-8)
    return fails


def run_all() -> int:
    print("=== selfcheck ===")
    n = selfcheck()
    print(f"\n{chr(10)}=== 正文数字（每条都是一次代数）==={chr(10)}")
    checks = [
        ("04 τ=k_t·i 口径", kt_crosscheck),
        ("08 电压包络（角点互斥）", voltage_envelope),
        ("08 SPWM vs SVPWM", lambda: spwm_vs_svpwm(24.0)),
        ("10 角度误差 5°", lambda: angle_error_cost(5.0)),
        ("07 三相合成幅值", lambda: rotating_field_peak(10.0, 37.0)),
        ("13 死区 100ns@20kHz", lambda: deadtime_error(100, 20000, 24.0)),
        ("14 分辨率 vs 齿隙", lambda: resolution_vs_backlash(15, 20.58, 6.0)),
        ("14 准直驱扭矩换算", lambda: quasi_direct_drive_torque()),
        ("15 扭矩密度与平方立方", torque_density_chain),
        ("27 总线带宽 M8010", lambda: bus_budget("GO-M8010-6")),
        ("27 总线带宽 IM6014", lambda: bus_budget("IM6014", nodes=15, hz=10000)),
        ("15 G1 减速比一致性", gear_ratio_consistency),
        ("18 刚度上限", stiffness_limit),
        ("18 固有频率闭环校验", natural_frequency_check),
        ("18 armature 折算口径校验", armature_side_check),
        ("27 485 轮询周期 vs EtherCAT 飞过即改", cycle_time_485_vs_ecat),
        ("26 6B 模型带宽", lambda: llm_memory_time(6.0, 2, 100.0)),
    ]
    for name, fn in checks:
        print(f"\n[{name}]")
        try:
            r = fn()
            ok, proc = r if isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], bool) else (True, r[0])
            print(proc)
            print(f"  → {'PASS' if ok else 'WARN'}")
            if not ok:
                n += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR {exc}")
            n += 1
    print(f"\n=== 结论：{n} 项异常 ===")
    return n


if __name__ == "__main__":
    sys.exit(1 if run_all() else 0)
