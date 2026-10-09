# 宇树人形机器人 · 一手规格数据表（Humanoid Primary-Source Spec Sheet）

访问日期：2026-10-08。证据分级：**官方页面** / **官方仓库文件** / **官方文档中心** / **二手**。
规则：只记读到的原文数字；查不到进「未取到」；冲突不抹平，两栏并列。

## 0. 抓取通道说明（重要，影响后续核对）

| 站点 | 纯抓取是否可用 | 结论 |
|---|---|---|
| `support.unitree.com/home/en/...` | **前端 SPA，直接抓只返回 768 字节空壳**（`<div id="root"></div>`，标题「宇树科技 文档中心」） | 但**内容可拿**：见下两行 |
| `https://robot-api.unitree.com/doc/spaces2?locale=en` | 可用，返回全部文档空间与目录树 | 官方页面（站点自己的后端 API） |
| `https://robot-api.unitree.com/doc/?space=<Space>&locale=en` | 可用，目录里每个节点带 `url` 字段指向真实正文 | 官方页面 |
| `https://doc-cdn.unitree.com/<id>` | 可用，返回**原始 Markdown 正文** | 官方文档中心（本表中标 **官方页面(文档中心)**） |
| `https://www.unitree.com/motor/` | **404**（该路径已不存在） | 正确路径是 `https://www.unitree.com/go1/motor` |
| `https://www.unitree.com/IM6014/` | 可用（Nuxt SSR，正文在 HTML 里） | 官方页面 |
| `https://github.com/unitreerobotics/unitree_mjcf` | **404 — 该仓库不存在** | MJCF 实际在 `unitree_mujoco` 仓库 |
| `https://github.com/unitreerobotics/unitree_motors_sdk` | **404 — 该仓库不存在** | 电机文档只在文档中心 |
| `api.github.com` | 本网络出口未认证 **60 次/小时已耗尽**，返回 `API rate limit exceeded` | 改用 `raw.githubusercontent.com` + `git clone --filter=blob:none`，均可用 |
| `shop.unitree.com`（curl） | 对 `shop.unitree.com` 直连 curl 出现 `schannel: SSL/TLS handshake failed`；`.json` 端点持续 `429 local_rate_limited` | 改用 WebFetch 可取；`products.json?limit=250` 被限流 |

`www.unitree.com` 人形/部件页可达清单（均 HTTP 200，正文 SSR 可解析）：
`/g1` `/h1` `/H2` `/R1` `/Dex3-1` `/Dex5-1` `/z1` `/go1` `/go1/motor` `/A1/motor` `/IM6014/` `/DigitalServo`

---

## A. 关节 / 执行器电子学

### A1. Unitree GO-M8010-6

两处官方来源互相印证：产品页 `https://www.unitree.com/go1/motor`（页面标题写 "GO Motor - Bionic Robot Joint Motor"）
与文档中心 `About the GO-M8010-6 Motor`。

| 项 | 值 | 单位 | 来源 | 分级 |
|---|---|---|---|---|
| 型号 | GO-M8010-6 | — | https://www.unitree.com/go1/motor | 官方页面 |
| 集成构成（原文） | "It integrates a brushless motor, reducer, single-turn absolute encoder, and FOC driver board." | — | https://robot-api.unitree.com/doc/?space=Motor_SDK_Dev_Guide&locale=en → `About M8010`，正文 `https://doc-cdn.unitree.com/8/1484/en/8_1484_en`（更新 2026-07-20 15:10:26） | 官方页面(文档中心) |
| 四合一中文口径 | 无刷电机 + 减速器 + **单圈**绝对值编码器 + FOC 驱动板 | — | 同上 | 官方页面(文档中心) |
| 产品页构成措辞 | "perfectly matched to the reduction. It has a built-in FOC control algorithm, a built-in temperature sensor and an absolution value encoder."（原文 absolution 为官网拼写） | — | https://www.unitree.com/go1/motor | 官方页面 |
| 最大扭矩 | 23.7 | N·m | 两源一致：https://www.unitree.com/go1/motor ；doc-cdn `8/1484` | 官方页面 / 官方页面(文档中心) |
| 「额定转矩」 | 官网与文档中心**均无 rated/continuous torque 字样**，只有 Maximum Torque | — | 同上 | — |
| 峰值扭矩 | 官网未使用 "peak torque" 一词，仅 "Maximum Torque 23.7NM"，并注明 "Measured at 24°C"、"at a reduction ratio of 6.33" | — | https://www.unitree.com/go1/motor | 官方页面 |
| 转矩常数 | 0.63895 | N·m/A | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 最大转速 | 30 | rad/s (@24VDC / 24V supply) | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 最大电流 | 40 A（产品页 "Maximum Current"）／文档中心写作 "Maximum Phase Current 40A" | A | https://www.unitree.com/go1/motor ；doc-cdn `8/1484` | 官方页面 / 官方页面(文档中心) |
| 减速比 | 1:6.33 | — | 两源一致（文档中心另有 "rotor to output side … is 6.33"） | 官方页面 / 官方页面(文档中心) |
| 重量 | About 530g／Approx. 530g | g | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 尺寸 | 96.5 × 92.5 × 42.3 | mm | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 通信方式 | RS-485（文档中心：RS485，半双工） | — | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 波特率 | 产品页 "Communication Baud Rate 4Mbps"；文档中心 "4.0 Mbit/s" | bit/s | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 串口格式 | 8 数据位 / 无校验 / 1 停止位（文档中心 "Serial Format 8N1"） | — | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 通信控制频率 | 6000 | Hz | 两源一致（文档中心 "Communication Control Frequency 6000 Hz"） | 官方页面 / 官方页面(文档中心) |
| 编码器分辨率 | 15 | bit | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 编码器单/多圈 | 文档中心：**single-turn absolute encoder（单圈绝对值）**；产品页仅写 "absolution value encoder"，未注明单/多圈 | — | doc-cdn `8/1484`；https://www.unitree.com/go1/motor | 官方页面(文档中心) |
| 命令/反馈位置字段 | 协议表中 `cmd.position` 与 `feedback.position` 均标注 "**multi-turn accumulated**"（多圈累加）——与上一条的「单圈绝对值编码器」**并存于官方文档，属措辞差异，勿自行统一** | — | https://doc-cdn.unitree.com/8/107/en/8_107_en（`Communication Protocol`，更新 2026-07-09 21:48:09） | 官方页面(文档中心) |
| 工作电压 | 12V～30VDC，24VDC recommend／文档中心 "12V ~ 30V DC, 24V DC recommended" | V | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 绝对最大电压 | 60 | V | doc-cdn `8/1484` | 官方页面(文档中心) |
| 过压保护电压 | 45 | V | doc-cdn `8/1484` | 官方页面(文档中心) |
| 示例程序最低供电 | 24V / 5A | — | doc-cdn `8/1484` "Minimum Supply for Demo Examples" | 官方页面(文档中心) |
| 推荐线缆 | ≥18AWG，长度 <1m | — | doc-cdn `8/1484` | 官方页面(文档中心) |
| 电机 ID | 0~14；15 = 广播（无响应） | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 单总线电机数 | Up to 15 | — | doc-cdn `8/1484` | 官方页面(文档中心) |
| 控制帧长度 | 17 | Byte | 两源：doc-cdn `8/1484` + `8/107` | 官方页面(文档中心) |
| 反馈帧长度 | 16 | Byte | 同上 | 官方页面(文档中心) |
| 校验 | CRC16_CCITT；控制帧覆盖前 15 Byte，反馈帧覆盖前 14 Byte；多字节小端 | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 帧头 | 下行 0xFE 0xEE；上行 0xFD 0xEE | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 环境温度 | -5℃ ~ 40℃ | ℃ | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 价格 | 369.00 USD（SKU `R2-DO52-LF16`） | USD | https://shop.unitree.com/products/go1-motor | 官方页面（商城） |
| 感知反馈（原文） | "Torque, Angle, Angular Velocity, Temperature" | — | https://www.unitree.com/go1/motor "Motor Perceptual Feedback" | 官方页面 |
| 控制指令（原文） | **"Torque, Angle, Angular Velocity, Stiffness, Damping"** | — | https://www.unitree.com/go1/motor "Motor Control Instruction"；doc-cdn `8/1484` 同文 "Motor Commands" | 官方页面 / 官方页面(文档中心) |
| 控制模式列表（工作模式位域原文） | `mode.mode` 3 bit：**`0` locked; `1` FOC closed-loop; `2` encoder calibration; `3~7` reserved** | — | https://doc-cdn.unitree.com/8/107/en/8_107_en | 官方页面(文档中心) |
| 控制模式列表（文档叙述） | About 页：**"Users can send position, velocity, torque, and hybrid force-position control commands through high-speed RS485 communication."** | — | doc-cdn `8/1484` | 官方页面(文档中心) |
| `Control Mode` 章节列出的模式 | Position mode / Speed mode / Damping mode / Torque mode / Zero torque mode | — | https://doc-cdn.unitree.com/8/106/en/8_106_en（更新 2023-12-29 17:57:50） | 官方页面(文档中心) |
| 混合控制公式 | `τ = τ_ff + k_p(q_des − q) + k_d(q̇_des − q̇)` | — | doc-cdn `8/1484` "Control Model" | 官方页面(文档中心) |
| 命令量化：转矩 | `int16`，raw = τ × 256（q8）；建议物理范围 **−4 ≤ τ ≤ 4 N·m**（转子侧） | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 命令量化：速度 | `int16`，raw = (ω / 2π) × 256；建议范围 **−804.00 ≤ ω ≤ 804.00 rad/s**（转子侧） | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 命令量化：位置 | `int32`，raw = (θ / 2π) × 32768（q15）；建议范围 **−411774.0 ≤ θ ≤ 411774.0 rad** | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 命令量化：kp | `int16`，raw = (k_p / 25.6) × 32768；范围 **0.0 ≤ k_p ≤ 25.599** | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 命令量化：kd | `int16`，raw = (k_d / 25.6) × 32768；范围 **0.0 ≤ k_d ≤ 25.599** | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 反馈温度 | `int8`，−128~127，1 = 1 ℃ | ℃ | doc-cdn `8/107` | 官方页面(文档中心) |
| 反馈错误位（3 bit） | 0 normal;1 overheat;2 overcurrent;3 overvoltage;4 encoder fault;5 bus undervoltage;6 winding overheat;7 not calibrated | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 反馈足端力原始值 | 12 bit，0~4095 | — | doc-cdn `8/107` | 官方页面(文档中心) |
| 单位换算注记 | "Control values in the SDK and protocol are defined on the **motor rotor side**, not the output side."；输出→转子乘 6.33 | — | doc-cdn `8/1484` | 官方页面(文档中心) |
| TN 曲线测试条件 | 转子侧、24V 供电 | — | doc-cdn `8/1484` | 官方页面(文档中心) |
| 官方 3D 模型下载 | `GO-M8010-6电机3D模型STP`（unitree-firmware.oss-cn-hangzhou.aliyuncs.com） | — | doc-cdn `8/1484` | 官方页面(文档中心) |

> 写作提示：产品页的「Motor Control Instruction」列表里**没有 FOC 这个词**，FOC 出现在文档中心的 `mode.mode` 位域（`1 = FOC closed-loop`）和 About 页的 "FOC driver board"。不要把两者合成一句「控制模式：位置/速度/转矩/FOC」。

### A2. Unitree IM6014

| 项 | 值 | 单位 | 来源 | 分级 |
|---|---|---|---|---|
| 集成构成（原文） | "It integrates a **brushless motor**, planetary reducer, **dual encoders**, and an **FOC driver board** internally" | — | https://doc-cdn.unitree.com/30/1371/en/30_1371_en （`About IM6014`，更新 2026-09-16 16:53:40） | 官方页面(文档中心) |
| 型号（文档中心表内） | **N6014B-12.6** | — | https://www.unitree.com/IM6014/ ；doc-cdn `30/1371` | 官方页面 |
| 通信 | RS485 | — | doc-cdn `30/1371`；产品页 "High Speed RS-485 Communication" | 官方页面 / 官方页面(文档中心) |
| 波特率 | **6Mbps/4Mbps**（文档中心）；产品页 "6000000bps/4000000bps" | bit/s | doc-cdn `30/1371`；https://www.unitree.com/IM6014/ | 官方页面 / 官方页面(文档中心) |
| 出厂默认波特率 | 6 Mbps，可改 6000000 / 4000000 | bit/s | https://doc-cdn.unitree.com/30/1378/en/30_1378_en（`Motor configuration`） | 官方页面(文档中心) |
| 串口格式 | 8 数据位 / None 校验 / 1 停止位（产品页写 "(8bit, 1stop, No Parity)"） | — | 两源一致 | 官方页面 / 官方页面(文档中心) |
| **总线最大轮询频率** | **10000** | Hz | doc-cdn `30/1371` "Max Bus Polling Frequency" | 官方页面(文档中心) |
| 供电电压 | **24V~75V**（规格表） | V | doc-cdn `30/1371` | 官方页面(文档中心) |
| 供电电压（同页冲突口径） | "M6014 supports wide voltage input from **`24V` to `72V`**"（原文写 M6014） | V | **同一文档同页** Power Supply Notes | 官方页面(文档中心) |
| 产品页口径 | "Input Voltage 24v~75v" | V | https://www.unitree.com/IM6014/ | 官方页面 |
| 过压保护阈值 | 85 | V | doc-cdn `30/1371` | 官方页面(文档中心) |
| 欠压保护阈值 | 16 | V | doc-cdn `30/1371` | 官方页面(文档中心) |
| 最大线电流 | 40 | A | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 峰值扭矩（转矩与转速反向） | **34.4** | N·m | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 峰值扭矩（转矩与转速同向） | **31.7** | N·m | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 曲线注释 | "The torque shown in the figure is **rotor-side** torque; output-side torque = rotor-side torque × **12.66**"；测试条件 60V 供电 | — | doc-cdn `30/1371` | 官方页面(文档中心) |
| 产品页曲线措辞 | "25°C ambient, 60V, 12.66 gear ratio — 31.7 Nm peak torque, 54.2 rad/s" | — | https://www.unitree.com/IM6014/ | 官方页面 |
| 减速比 | **3:38**（=12.667）；协议页写作 `3/38`，同一段又出现 `38/3` | — | doc-cdn `30/1371`；https://doc-cdn.unitree.com/30/1383/en/30_1383_en | 官方页面(文档中心) |
| 空载最大转速（60V） | 54.2 | rad/s | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 编码器类型 | **Dual Absolute Encoders**（双绝对值） | — | doc-cdn `30/1371`；产品页 "Rotor, output end, dual absolute value encoder" | 官方页面 / 官方页面(文档中心) |
| 编码器分辨率 | **15** | bit | 两源一致（产品页仅标 "Rotor End Encoder Resolution 15bit"） | 官方页面 / 官方页面(文档中心) |
| 转子端惯量 | 0.000024796937 | kg·m² | doc-cdn `30/1371` | 官方页面(文档中心) |
| 输出端惯量 | 0.025392063 | kg·m² | doc-cdn `30/1371` | 官方页面(文档中心) |
| 重量 | 535 | g | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 尺寸 | φ65 × 60 | mm | 两源一致（产品页表头写作 "Dimensions (W x H x D) φ65*60mm"） | 官方页面 / 官方页面(文档中心) |
| 最低工作温度 | −20 | ℃ | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 驱动板过热阈值 | 90（产品页：超过即关机并报过热错误） | ℃ | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 绕组过热阈值 | 130 | ℃ | 两源一致 | 官方页面 / 官方页面(文档中心) |
| 控制算法（产品页） | "Hybrid Control" | — | https://www.unitree.com/IM6014/ | 官方页面 |
| 齿轮/外壳材质 | 金属齿轮；铝合金 + 高强工程塑料外壳 | — | https://www.unitree.com/IM6014/ | 官方页面 |
| 协议类型 | "RS-485 Multidrop Bus"；ID **0-14**（产品页） | — | https://www.unitree.com/IM6014/ | 官方页面 |
| 协议 ID（文档中心） | 命令帧 "**Motor ID: 0~14, 15 broadcast**"；反馈帧 "0~14, 15 reserved" | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 协议 ID（STM32 参数表） | `id` 范围写作 **0-15** — 与上面 0~14 + 15 广播的口径不同 | — | https://doc-cdn.unitree.com/30/1377/en/30_1377_en | 官方页面(文档中心) |
| 下行控制帧 | **20** Byte（头 0xFE 0xEE，含 CRC32-MPEG2） | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 上行状态帧 | **26** Byte（头 0xFC 0xEE，**不计入 CRC**） | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| CRC 算法 | CRC32-MPEG2，多项式 0x04c11db7；命令帧含帧头、状态帧不含帧头 | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 命令量化：转矩 | `int16`，**2560 = 1 N·m**；绝对上限 2¹⁵/2560 = **12.8 N·m**（转子侧） | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 命令量化：速度 | `int16`，**64/2π = 1 rad/s** | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 命令量化：位置 | `int32`，**32768/2π = 1 rad** | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 命令量化：k_pos | `int16`，**12800 = 1 N·m/(rad/s)**，0~32767（−32768~−1 保留） | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 命令量化：k_spd | `int16`，**51200 = 1 N·m/(rad/s)**，0~32767 | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 工作模式位（`status`，3 bit） | **0 = Stop（上电默认）/ 1 = FOC / 2~7 = Reserved** | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 超时保护 | `timeout`=1 时，超过 **1s** 未收到命令进入模式 0 | s | doc-cdn `30/1383` | 官方页面(文档中心) |
| 反馈字段 | torque/speed/pos、`temp1` 驱动温度 int8 −100~127、`temp2` 绕组温度 uint8 0~255、`vol` 0~255（2 LSB = 1 V）、MError(位映射，触发后 status=0)、MWarning(3 bit) | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 字节序 | 多字节小端（low byte first） | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| RS485 终端电阻 | 120 Ω，电缆两端各并一个 | Ω | https://doc-cdn.unitree.com/30/1383/en/30_1383_en | 官方页面(文档中心) |
| 输出/转子换算 | 转矩 ×r、速度 ÷r、位置 ÷r、Kp 与 Kd ×r² | — | doc-cdn `30/1383` | 官方页面(文档中心) |
| 价格 | **两处官方口径冲突**：产品页 `https://shop.unitree.com/products/unitree-im6014-motor` = **269.00 USD**；商城列表页同一商品显示 **$10.00 USD** | USD | 两个都是 shop.unitree.com | 官方页面（商城），**冲突保留** |
| 保修（产品页） | 3 month | — | https://www.unitree.com/IM6014/ | 官方页面 |

#### IM6014 控制模式清单（原文，文档中心 `Control Mode`，更新 2026-06-30 18:04:19）
来源：https://doc-cdn.unitree.com/30/1382/en/30_1382_en ｜ 分级：官方页面(文档中心)

- 底层唯一控制目标是**输出转矩**；混合控制公式 `τ = τ_ff + k_p × (p_des − p) + k_d × (ω_des − ω)`
- 5 个控制量：`τ_ff` 前馈转矩 N·m、`p_des` 期望角位置 rad、`ω_des` 期望角速度 rad/s、`k_p` 位置刚度 N·m/(rad/s)、`k_d` 速度刚度 N·m/(rad/s)
- **6 种模式**（参数组合表）：
  | 模式 | τ_ff | 位置刚度 | 期望位置 | 速度刚度 | 期望速度 |
  |---|---|---|---|---|---|
  | Zero Torque Mode | 0 | 0 | 0 | 0 | 0 |
  | Pure Torque Mode | 前馈转矩 | 0 | 0 | 0 | 0 |
  | Damping Mode | 0 | 0 | 0 | 速度刚度 | 0 |
  | Velocity Mode | 0 | 0 | 0 | 速度刚度 | 期望角速度 |
  | Position Mode | 0 | 位置刚度 | 期望位置 | 速度刚度 | 0 |
  | Torque-Position Hybrid Mode | 前馈转矩 | 位置刚度 | 期望位置 | 速度刚度 | 期望角速度 |
- 关键定性结论（原文）：**"The 'Position Mode' and 'Velocity Mode' of the Unitree IM6014 are not the traditional cascaded three-loop architecture of servo drives, but rather parameter trimming based on a single hybrid control formula."**；**"the IM6014 motor's underlying layer only provides a current loop interface with proportional gain"**；驱动 "internally only performs proportional operations and torque synthesis, then directly hands it over to the **FOC current loop** for execution"
- 注：`Zero Torque Mode` 条目在该英文页仍残留中文原文「**零力矩模式**：实时抵消反电动势…表现为近似"零阻力"自由拨动状态」

#### IM6014 STM32 例程要求（文档中心 `STM32 Example`，更新 2026-07-20 15:05:28）
来源：https://doc-cdn.unitree.com/30/1377/en/30_1377_en ｜ 分级：官方页面(文档中心)

- 例程基于 **STM32F413RGT6**；"If porting to other MCU models, it is recommended to use an MCU with an **FPU**."
- 硬件要求原文：**"The MCU UART peripheral needs to support baud rates of `6Mbps`/`4Mbps`"**；**"The UART-to-485 module needs to support baud rates of `6Mbps`/`4Mbps`"**
- 接线：TX→PA9，RX→PA10，RE/DE→PA11，5V/GND，A/B 到电机
- 例程下载：https://oss-global-cdn.unitree.com/static/a0542aa67f4b4b1f9095682e4c5c3292.zip
- 输出侧参数范围（原文表）：`outputTor` −162.133~162.128 N·m；`outputSpd` −253.973~253.965；`outputPos` −32508.539~32508.539；`Kp` 0~410.725；`Kd` 0~102.681；`mode` 0-1；`timeout` 0-1
- 上电位置模式：出厂默认 "Factory Mode"，另有 "High-Precision Mode"（需限定角度范围） — doc-cdn `30/1378`

---

## B. 人形产品线

### B1. G1（https://www.unitree.com/g1 ｜ G1 SDK 文档中心 `About G1` https://doc-cdn.unitree.com/11/223/en/11_223_en ，更新 2026-09-17 10:23:53）

**自由度拆解（官方页面表，G1 / G1 EDU 两栏）**

| 项 | G1 | G1 EDU |
|---|---|---|
| Total Degrees of Freedom（Joint Freedom） | 23 | 23 - 43 |
| Single Leg DoF | 6 | 6 |
| Waist DoF | 1 | 1 +（Optional 2 additional waist degrees of freedom） |
| Single Arm DoF | 5 | 5 |
| Single Hand DoF | / | 7（Optional Force control of three-fingered hand）+ 2（Optional 2 additional wrist DoF） |
| Head DoF | 官方页面表**未列** | 未列 |

> 拆解原文（同页 Dex3-1 注）："The thumb has 3 active degrees of freedom; the index finger has 2 active degrees of freedom; the middle finger has 2 active degrees of freedom."
> 官方页面给出的膝/髋/腰/肩/肘/腕**各自数量未在页面拆开**；按 URDF/MJCF 可数出：髋 3（pitch/roll/yaw）+ 膝 1 + 踝 2 = 6/腿；肩 3 + 肘 1 + 腕 3 = 7/臂（29dof 版本）；23dof 版本臂 5（肩 3 + 肘 1 + 腕 roll 1）。

**关节角范围（原文，官方页面「Extra Large Joint Movement Space」）**

| 部位 | G1 | G1 EDU |
|---|---|---|
| Waist | Z ±155° | Z ±155°、X ±30°、Y ±30° |
| Knee | 0~165° | 0~165° |
| Hip | P ±154°、R −30~+170°、Y ±158° | P ±154°、R −30~+170°、Y ±158° |
| Wrist | —（G1 无腕 pitch/yaw） | P ±92.5°、Y ±92.5° |

**尺寸 / 重量 / 电源 / 传感 / 算力（官方页面表）**

| 项 | 值 |
|---|---|
| Height, Width and Thickness（Stand） | 1320 × 450 × 200 mm |
| Height, Width and Thickness（Fold） | 690 × 450 × 300 mm |
| Weight (With Battery) | About 35kg（G1）／About 35kg+（EDU）。文档中心表写 "About 35kg / About 35kg" |
| Calf + Thigh Length | 0.6 M |
| Arm Span | About 0.45 M |
| 关节轴承 | Industrial grade crossed roller bearings |
| 关节电机 | Low inertia high-speed internal rotor PMSM |
| Joint Encoder | Dual encoder |
| 供电 | **13 string lithium battery**（文档中心同文） |
| 电池 | Smart Battery (Quick Release) **9000mAh** |
| 充电器 | **54V 5A** |
| 续航 | About 2h |
| 基础算力 | 8-core high-performance CPU |
| 高算力模块 | G1：/ ；EDU：Multiple brands and models available, such as Orin, etc.（文档中心表写作 **"NVIDIA Jetson Orin"**） |
| 传感 | Depth Camera + 3D LiDAR；4 Microphone Array；5W Speaker；WiFi 6、Bluetooth 5.2 |
| 走线 | Full Joint Hollow Electrical Routing；Local air cooling |
| 保修 | 8 months（G1）／18 months（EDU） |
| 价格 | **Price from $13.5K**；表内 "US $13.5K"，EDU "Contact sales"（均 Tax and Shipping cost excluded） |
| 商城价 | Unitree G1 – **G1 $13,500.00 USD**；**G1 Pro $21,500.00 USD**（变体原价 1350000 / 2150000，分单位） — https://shop.unitree.com/collections/all |

**传感器具体型号（文档中心 `About G1`，官方页面(文档中心)）**
- **LIVOX-MID360**："The G1 head is equipped with **LIVOX-MID360** laser radar … FOV level of up to 360° and a maximum vertical angle of **59°**"
- **D435i**："The G1 head is equipped with a **D435i** depth camera"；图注 "MID360+D435i Merged FOV"
- **PC2 = Jetson Orin NX 16GB**：官方表格行 `Model | Jetson Orin NX`；`graphic memory Memory | 16G`；`Memory | 16G`；`CPU | Arm® Cortex®-A78AE`；`Number of threads | 8`；`Max largest rate | 2 GHz`；`Cache | 2MB L2 + 4MB L3`；`GPU | 1024 NVIDIA Ampere architecture Gpus with 32 Tensor cores`；`Maximum dynamic frequency of graphics card | 918MHz`；`Gaussian and Neuro Accelerator | 3.0`
  - 附注原文："Unitree does not deploy services on the NVIDIA Jetson Orin module."／"CPU modules may ship to a more advanced version with no less than the above performance."

**G1 关节电机相关表述（文档中心，两处口径）**
- "The G1 joint adopts Unitree self-developed motor … The **maximum torque of the motor is 120N.m** … equipped with **dual encoders**"（doc-cdn `11/223`）
- 同页规格表：**Maximum Torque of Knee Joint【1】 = 90N.m（G1）／120N.m（G1 EDU）**；脚注 [1] "The maximum torque of the joint motors of the whole machine is different. This is the maximum torque of the largest joint motor among them."

**SDK 关节序号与位置限位（文档中心 `Joint serial number and joint limit`，官方页面(文档中心)）**
索引 0–28（29dof 消息序）：`L_LEG_HIP_PITCH 0, L_LEG_HIP_ROLL 1, L_LEG_HIP_YAW 2, L_LEG_KNEE 3, L_LEG_ANKLE_PITCH 4, L_LEG_ANKLE_ROLL 5, R_LEG_HIP_PITCH 6, R_LEG_HIP_ROLL 7, R_LEG_HIP_YAW 8, R_LEG_KNEE 9, R_LEG_ANKLE_PITCH 10, R_LEG_ANKLE_ROLL 11, WAIST_YAW 12, WAIST_ROLL 13, WAIST_PITCH 14, L_SHOULDER_PITCH 15, L_SHOULDER_ROLL 16, L_SHOULDER_YAW 17, L_ELBOW 18, L_WRIST_ROLL 19, L_WRIST_PITCH 20, L_WRIST_YAW 21, R_SHOULDER_PITCH 22, R_SHOULDER_ROLL 23, R_SHOULDER_YAW 24, R_ELBOW 25, R_WRIST_ROLL 26, R_WRIST_PITCH 27, R_WRIST_YAW 28`

限位（rad，原文）：

| 关节 | limit(rad) |
|---|---|
| HIP_PITCH（左右） | −2.5307 ~ 2.8798 |
| HIP_ROLL 左 | −0.5236 ~ 2.9671 |
| HIP_ROLL 右 | −2.9671 ~ 0.5236 |
| HIP_YAW | −2.7576 ~ 2.7576 |
| KNEE | −0.087267 ~ 2.8798 |
| ANKLE_PITCH | −0.87267 ~ 0.5236 |
| ANKLE_ROLL | −0.2618 ~ 0.2618 |
| WAIST_YAW | −2.618 ~ 2.618 |
| WAIST_ROLL / WAIST_PITCH | −0.52 ~ 0.52 |
| SHOULDER_PITCH | −3.0892 ~ 2.6704 |
| SHOULDER_ROLL 左 | −1.5882 ~ 2.2515；右 −2.2515 ~ 1.5882 |
| SHOULDER_YAW | −2.618 ~ 2.618 |
| ELBOW | −1.0472 ~ 2.0944 |
| WRIST_ROLL | −1.972222054 ~ 1.972222054 |
| WRIST_PITCH / WRIST_YAW | −1.614429558 ~ 1.614429558 |

另有一份 **23dof 的 12 关节消息序 + 伺服模式**表（`Joint Motor Sequence`，https://doc-cdn.unitree.com/11/249/en/11_249_en ）：索引 0–8（hip_roll/pitch/knee、腰 yaw、hip_yaw）`Servo Mode = 0x0A`，索引 10–19（ankle、shoulder×3、elbow）`Servo Mode = 0x01`，索引 9 = `-`（空位）。

**G1 官方模型文件里的逐关节力矩上限（最强证据）— 见 B6**

### B2. H1 / H1-2（https://www.unitree.com/h1 ；文档中心 About_H1 https://doc-cdn.unitree.com/10/166/en/10_166_en 更新 2026-03-12 23:02:14 ；About_H1-2 https://doc-cdn.unitree.com/10/271/en/10_271_en 更新 2026-03-12 23:03:12）

| 项 | H1 | H1-2 |
|---|---|---|
| Key Dimensions | (1520+285)mm × 570mm × 220mm | (1503+285)mm × 510mm × 287mm |
| Thigh and Calf Length | 400mm × 2 | 400mm × 2 |
| Total Arm Length | 338mm × 2 | 685mm |
| DOF of Each Leg | 5（Hip × 3 + Knee × 1 + Ankle × 1） | 6（Hip ×3 + Knee ×1 + Ankle ×2） |
| DOF of Each Arm | 4（Expandable） | 7（Shoulder ×3 + Elbow ×1 + Wrist ×3） |
| Total Weight | About 47kg | About 70kg |
| 高度（页面宣传块） | "Height about 180CM" | "Height about 178CM" |
| Ultimate Torque of Joint Unit | Knee About **360N.m**，Hip About **220N.m**，Ankle About **59N.m**，Arm Joint About **75N.m** | Knee About **360N.m**，Hip About **220N.m**，Waist Joint About **220N.m**，Ankle Joint About **75x2N.m** |
| Peak Torque Density | 189N.m/Kg | 189N.m/Kg |
| Mobility | Moving speed of **3.3m/s (world record)**, Potential mobility **> 5m/s** | Moving speed **<2m/s** |
| Battery | capacity **15Ah (0.864KWh)**, Max Voltage **67.2V** | 同：15Ah(0.864KWh), Max Voltage 67.2V |
| 页面宣传块 | "Battery capacity: 864Wh, quickly replaceable" | — |
| 算力 | Standard: Intel Core i5(Platform Function), Intel Core i7(User Development)；Optional: Intel Core i7 or such as **Orin NX**, etc. | Standard 同；Optional: Intel Core i7 or **Orin NX (Maximum up to 3 devices)** |
| 传感 | 3D LIDAR + Depth Camera（"360° depth perception"） | 3D LIDAR + Depth Camera |
| 灵巧手 | Optional | Optional **Dex5-1** or other ambidextrous hands |
| 臂关节峰值（H1-2） | / | Shoulder About **120N.m**, Elbow About **120N.m**, Wrist About **30N.m** |
| 臂正常负载（H1-2） | / | Peak: About **21Kg**; Rated: About **7Kg** |
| 关节轴承 | Industrial grade crossed roller bearings | 同 |
| 核心电机 | Low inertia high-speed internal rotor PMSM | 同 |
| 最大关节力矩（宣传块） | "Maximum Joint Torque 360N.m" | "Maximum Torque of Leg Joint 360N.m"；"Maximum Torque of Arm Joint 120N.m"；"Degree of freedom 27" |

**M107 关节电机（文档中心 About_H1 原文）**："The H1 robot uses the self-developed **M107** joint motor by Unitree … The **maximum torque of this motor is 360N.m**, and the **maximum tension (under equivalent conditions of 3.5cm force arm) is 10000N**. The motor is designed with a hollow axle … also equipped with **dual encoders**"

**H1 文档中心关节编号与限位（原文，官方页面(文档中心)）**

| 编号 | 关节 | 限位 |
|---|---|---|
| 0 | right_hip_roll_joint | −0.43~+0.43 rad |
| 1 | right_hip_pitch_joint | −3.14~+2.53 rad |
| 2 | right_knee_joint | −0.26~+2.05 rad |
| 3 | left_hip_roll_joint | −0.43~+0.43 rad |
| 4 | left_hip_pitch_joint | −3.14~+2.53 rad |
| 5 | left_knee_joint | −0.26~+2.05 rad |
| 6 | torso_joint | −2.35~+2.35 rad |
| 7 | left_hip_yaw_joint | −0.43~+0.43 rad |
| 8 | right_hip_yaw_joint | −0.43~+0.43 rad |
| 10 | left_ankle_joint | −0.87~+0.52 rad |
| 11 | right_ankle_joint | −0.87~+0.52 rad |
| 12 | right_shoulder_pitch_joint | −2.87~+2.87 rad |
| 13 | right_shoulder_roll_joint | −3.11~+0.34 rad |
| 14 | right_shoulder_yaw_joint | −4.45~+1.3 rad |
| 15 | right_elbow_joint | −1.25~+2.61 rad |
| 16 | left_shoulder_pitch_joint | −2.87~+2.87 rad |
| 17 | left_shoulder_roll_joint | −0.34~+3.11 rad |
| 18 | left_shoulder_yaw_joint | −1.3~+4.45 rad |
| 19 | left_elbow_joint | −1.25~+2.61 rad |

**H1 整机自由度（文档中心原文）**："The single arm has 4 degrees of freedom … The single leg has 5 degrees of freedom … The waist has 1 degree of freedom … The entire robot has a total of **19 degrees of freedom**, consisting of **19 joint motors**"（注意：页面宣传块给 H1-2 是 27 DoF）

**H1 板载计算机（文档中心表格原文）**
| | PC 1（Motion Control Computing Unit） | PC 2 / PC 3（Development Computing Unit） |
|---|---|---|
| Model | i5-1235U | i7-1255U / i7-1265U |
| Cores / Threads | 10 / 12 | 10 / 12 |
| Max Turbo | 4.40 GHz | 4.70 GHz & 4.80 GHz |
| Memory | 8GB | 16GB & 32GB |
| Memory Type | LPDDR5 5200 MT/s (dual-channel) | 同 |
| Cache | 12 MB Intel® Smart Cache | 同 |
| Storage | 500GB or more | 同 |
| IP Address | unaccessable | 原文 `192.168.123.162\163`；页内注：PC3 为选配，地址 192.168.123.163 |

**商城价**：Unitree H1（Contact us for the real price）– **$90,000.00 USD** — https://shop.unitree.com/collections/all ｜ 官方页面（商城）

### B3. H2（https://www.unitree.com/H2 ；文档中心 About H2 https://doc-cdn.unitree.com/25/1061/en/25_1061_en 更新 2026-09-03 17:17:27）

| 项 | H2 | H2 EDU |
|---|---|---|
| Height, Width and Thickness（Stand） | 1820 × 456 × 218 mm | 同 |
| Weight (With Battery) | About 70kg | About 70kg |
| Degree of Freedom (Total Joints) | 31 | 31 |
| Single Leg / Single Arm / Waist / Head DoF | 6 / 7 / 3 / 2 | 同 |
| Dexterous Hand | / | Dexterous Hand (Multiple Model Options) |
| Bionic Head with Facial Features | YES | YES |
| Max Torque of Arm Joint | 120 N.m | 120 N.m |
| Max Torque of Leg Joint | **360 N.m** | 360 N.m |
| Arm Maximum Payload | Peak: ~15 kg; Rated: ~7 kg | 同 |
| Calf + Thigh Length | **1045 mm** | 同 |
| Forearm + Upper Arm Length | **690 mm** | 同 |
| 材料 | Aircraft-Grade Aluminum + Titanium Alloy + High-Strength Engineering Plastics | 同 |
| 电池容量 | **15Ah (0.972KWh)** | 同 |
| 电池电压 | **Maximum Voltage: 75.6 V** | 同 |
| 续航 | About 3h | 同 |
| 基础算力 | PC1：Intel Core i5（Platform Capabilities）；PC2：Intel Core i7（Custom Development） | 同 |
| 高算力模块 | / | Multiple brands and models available, such as **Thor**, etc. |
| 传感 | Humanoid Binocular Camera with Wide Field of View；Array Microphone + High-Power Speaker；WiFi 6 / BT 5.2 | 同 |
| 散热 / 走线 | Local air cooling | 同 |
| 保修 | 8 Months | 12 Months |
| 价格 | **$29,900**（Tax and Shipping cost excluded） | Contact Sales |
| 宣传页 | "31 degrees of freedom, 360N·m joint torque"；"Powered by a **2070 TOPS** chip" | — |

**H2 文档中心 DoF 拆解原文**："Each arm has **7 DoF**: 3 for the shoulder joint, **2 for the elbow joint** and 2 for the wrist joint. Each leg has **6 DoF**: 3 for the hip joint, 1 for the knee joint and 2 for the ankle joint. The waist features 3 DoF and the head has 2 DoF. … a total of **31 DoF**, driven by **31 joint motors**"
（注意：与产品页 "Single Arm 7" 一致，但官方页面未拆 elbow=2；文档中心明确 elbow 2）

**H2 算力模块选项（文档中心表格，原文）**
| Computing Module | **Jetson Thor（T5000）** | **Jetson Orin NX（16GB）** |
|---|---|---|
| AI performance | **2070 TFLOPS (FP4-Sparse)** | **100 TOPS** |
| GPU | 2560-core NVIDIA Blackwell + 5th-gen Tensor Cores, MIG with 10 TPCs | 1024-core NVIDIA Ampere, 32 Tensor Cores |
| GPU Max frequency | 1.57 GHz | 918 MHz |
| CPU | 14-core Arm Neoverse-V3AE, 1MB L2/core, 16MB shared L3 | 8-core Arm Cortex-A78AE v8.2, 2MB L2 + 4MB L3 |
| CPU Max frequency | 2.6 GHz | 2 GHz |
| Visual Accelerator | 1 个 PVA v3（原文中英混排） | 1x PVA v2 |

**H2 对外供电接口（文档中心，原文）**：`[1] GXT30(2)-M VBAT+485 → 54–75.6V/10A（Battery power output, direct connection to battery + RS-485 to PC2）`；`[2]/[11] 24V+CAN → 24V/10A`；`[10] 12V+485 → 12V/10A`；注 1「以上对外供电口总功率（不含直连电池）不超过 **500 W**」；注 2「直连电池电压随电量变化，范围 **54–75.6V**，额定电流 **10A**」
**H2 双目相机（文档中心表）**：`Output data 12bit RAW / 10-bit RAW`；`Baseline 60mm / 60.00 ± 0.5 mm`；`Operating temp. −20 to +60℃ / −30~+70℃`；`F-number F2.0`；`Focal Length 1.53 mm / 2.67 mm`；`Depth of Field 0.15 m~INF (Focus distance 0.4 m) / 0.4m-INF`

**商城价**：Unitree H2 – **$29,900.00 USD**；Unitree H2 Plus – **$100,000.00 USD** — https://shop.unitree.com/collections/all ｜ 官方页面（商城）

### B4. R1（https://www.unitree.com/R1 ；文档中心 about_R1 https://doc-cdn.unitree.com/27/1135/en/27_1135_en 更新 2026-08-04 20:56:55）

| 项 | R1 AIR | R1 | R1 EDU |
|---|---|---|---|
| 价格 | **$4,900** | **$5,900** | Contact Sales |
| Height, Width and Thickness（Stand） | 1230 × 357 × 190 mm | 同 | 同 |
| Weight (With Battery) | About 27kg | About 29kg | About 29kg |
| Total DoF | 20 | **26** | **26-40**（官方页面）／文档中心表格三栏写 **20 / 26 / 26** — **冲突，保留** |
| Single Leg DoF | 6 | 6 | 6 |
| Single Arm DoF | 4 | 5 | 5 |
| Waist DoF | / | 2 | 2 |
| Head DoF | / | 2 | 2 |
| Dexterous Hand | / | / | Optional |
| Joint Output Bearing | Crossed roller bearings, Double Hook Ball Bearings | 同 | 同 |
| Joint Motor | Low inertia high-speed internal rotor PMSM | 同 | 同 |
| 「Maximum Torque of Arm Joint【1】」 | **官方页面此行值是 "About 2kg"**（单位与行名不匹配，疑官网表格错位；文档中心同字段写作 "Max Arm Payload [1] Approx. 2kg"） | 同 | 同 |
| Calf + Thigh Length | 600 | 600 | 600（**官方页面未带单位**） |
| Forearm + Upper Arm Length | 420 | 420 | 420（同上，无单位） |
| Joint Movement Space | Knee Joint：−10°~+139°；Hip Joint：Y ±157°, P −168°~+146°, R −60°~+100°；Waist Joint：Y ±150°, R ±30° | 同 | 同（EDU 栏**未列 Waist Joint**） |
| Electrical Routing | Hollow + Internal Routing | 同 | 同 |
| Joint Encoder | **Dual + single encoder** | 同 | 同 |
| 散热 | Local air cooling | 同 | 同 |
| 供电 | Lithium battery（未给 mAh/串数/电压） | 同 | 同 |
| 基础算力 | 8-Core High-Performance Processor | 同 | 同 |
| 高算力模块 | / | / | Optional **NVIDIA Jetson Orin (40-100TOPS)**（文档中心原文；官方页面 "such as Orin(40-100TOPS), etc."） |
| 相机 | Monocular camera | Binocular camera | Binocular camera |
| 麦克风/喇叭 | 4-Mic Array / YES | 同 | 同 |
| 续航 | About 1h | About 1h | About 1h |
| 保修 | 6 Months | 8 Months | 12 Months |
| 宣传块 | "≤123cm agile form, ultra-lightweight at about 29kg"；"20-26-DOF … its 2-DOF head"；"Price from $4,900" | | |

**R1 文档中心补充**：
- 关节电机原文："R1 joints use Unitree self-developed motors … hollow shaft design … equipped with **dual encoders**"
- 相机参数（文档中心）：`Depth Resolution 544*448`；`Depth Map Frame Rate 10Hz`；`RGB Frame Rate 30Hz`；`Resolution 13 Million Pixels`
- Dex3-1 相关（R1 文档 `Basic Services Interface`）：`rt/dex3/(left or right)/cmd` 类型 `unitree_hg::msg::dds_::HandCmd_`，状态 topic `rt/dex3/(left or right)/state` 类型 `HandState_`

**商城价**：Unitree R1 – **$4,900.00 USD**；Unitree R1-D – **$4,290.00 USD**；R1 Battery **$500.00 USD**；Unitree R1-7a 机械臂 **$750.00 USD**（列表页另一处标题价 "1650.00 USD"，变体 "R1-7a" 原价 165000 / "R1-7a(Student Price)" 75000，**单位口径不一致，保留**） — https://shop.unitree.com/collections/all ｜ 官方页面（商城）

### B5. Dex3-1 / Dex5-1 / Z1

#### Dex3-1（https://www.unitree.com/Dex3-1 ｜ G1 文档中心 `Dex3-1 Dexterous Hand` https://doc-cdn.unitree.com/11/251/en/11_251_en 更新 2025-02-10 11:56:17）

| 项 | 值（原文） |
|---|---|
| 自由度 | 7 DoF = **6 micro brushless force control joint direct drive + 1 micro brushless force control joint gear drive**；Thumb ×3, Index ×2, Middle ×2 |
| 触觉 | **one hand with 33 tactile sensors**；`Number of Pressure Sensors 9 (Total of 33 Pressure Sensors)` |
| 阵列分辨率 | 2×2 (Palm) ×3；2×2 (Single Finger Pad) ×3；3×1 (Single Fingertip) ×3 |
| 感知范围 | 10g–2500g |
| 最大承受（不损坏） | 20kg |
| 重量 | 710g |
| 尺寸 | 175 × 88 × 77 mm（"flat state" 脚注 [1]） |
| 关节角 | Thumb0 −60°~60°；Thumb1 −35°~60°；Thumb2 0~100°；Index0/Middle0 0°~90°；Index1/Middle1 0°~100° |
| 指尖重复定位精度 | ±2mm |
| 工作电压 | 12~58V |
| 静态电流 | 58V @ 0.2A |
| 最大电流 | 10A |
| 通信接口 | USB2.0 |
| 工作温度 | −20℃ ~ 60℃ |
| 负载（手掌向下/向左，常温，抓 5cm 圆硬物） | The Maximum Weight is 500g；The Maximum Power Is: 400W@3s |
| 通信速率 | **1000Hz** |
| 整包字节 | Sender：1234 bytes；Receiver：1270 bytes |
| 感知反馈 | Joint Mode, Joint Position, Joint Velocity, Joint Torque, Joint Temperature, Voltage and Current, **Sensor Pressure Value, Sensor Temperature Value**, imu Data |
| 控制反馈 | Joint Mode, Joint Position, Joint Velocity, Joint Torque, Joint Stiffness Coefficient, Joint Damping Coefficient |
| 微型力控关节型号 | **F-1515-108** 与 **F-1515-214** |
| 该关节参数 | Weight 45g；Size 34.8×23.1×23.3mm；减速比 1:108 / 1:214；Max Torque(Ideal) 0.76 / 1.498 Nm；Max Torque(Actual) 同向 0.49 / 0.86 Nm，反向 1.37 / 3.1 Nm；Max Rotational Speed 23 / 11 rad/s；Max Line Current 4.76A；Communication Control Frequency 1000Hz；Method of Communication **High Speed Unibus**；Encoder **Rotor Absolute Value Encoder**；Working Voltage 12-24V；工作温度 −20~60℃ |
| G1 搭配 | G1 EDU 栏：7（Optional Force control of three-fingered hand）+ 2（Optional 2 additional wrist degrees of freedom）；"**Dex3-1 can optionally be installed with tactile sensor arrays**" |

**价格**：**未取到**（见 D 节）

#### Dex5-1（https://www.unitree.com/Dex5-1）

| 项 | Dex5-1 | Dex5-1P |
|---|---|---|
| 自由度 | **20 Degrees of freedom (16 active+4)**；Thumb ×4, Index ×3, Middle ×3, Ring ×3, Little ×3 | 同 |
| 传动 | 12 self-developed micro force-controlled composite transmission joints (enables robot to achieve tactile proprioception) + 4 micro force-controlled joint gear transmission | 同 |
| 触觉 | 页面宣传块 "94 tactile sensors per hand; supports secondary development of tactile algorithms"；表格 `Number of Pressure Sensors`：Dex5-1 = **/**，Dex5-1P = **12 (94 pressure sensors in total)** | — |
| 阵列分辨率（Dex5-1P） | 2×5 (Palm)；2×3 (Single Finger Pad) ×5；2×3 (Single Fingertip) ×5；2×3 (Single Finger Root) ×4 | — |
| 感知范围 / 最大承受 | 10g-2500g / 20kg（Dex5-1 栏为 `/`） | — |
| 重量 | 1100g | 1100g |
| 尺寸 | 217.3 × 127.5 × 72.1 mm（"The final shipped version may vary."） | 同 |
| 关节角 | Thumb0 −33.5°~39°；Thumb1 0°~100°；Thumb2 0°~110°；Thumb3 0°~92°；四指 Knuckle0 −22°~22°，Knuckle1 0°~90°，Knuckle2 0°~95°，Knuckle3 0°~81°（Coupling with finger joint 2） | 同 |
| 四指侧摆 | ±22° | ±22° |
| 最小握持直径 | 10mm | 10mm |
| 指尖重复定位精度 | ±1mm | ±1mm |
| 指尖力 | 10N | 10N |
| 工作电压 | 24V~60V | 同 |
| 静态电流 | 58V@0.2A | 同 |
| 最大电流 | 58V@4A | 同 |
| 通信接口 | USB2.0 | 同 |
| 工作温度 | −20℃ ~ 60℃ | 同 |
| 负载 | Palm facing down：**3.5kg**；Palm facing left：**4.5kg** | 同 |
| 通信速率 | 1000Hz | 1000Hz |
| 整包字节 | Sender 1234 bytes / Receiver 1270 bytes | 同 |
| 感知反馈 | Dex5-1：Joint Mode/Position/Velocity/Torque/Temperature, Voltage and Current, **imu Data**（**无压力/温度传感器字段**）；Dex5-1P：额外含 Sensor Pressure Value, Sensor Temperature Value | — |
| 控制反馈 | Joint Mode, Joint Position, Joint Velocity, Joint Torque, Joint Stiffness Coefficient, Joint Damping Coefficient | 同 |

**价格**：**未取到**

#### Z1（https://www.unitree.com/z1）

| 项 | 值 |
|---|---|
| 型号 | Z1 AIR / Z1 PRO，均 **6 Axis** |
| 重量 | 4.3kg / 4.5kg |
| 负载 | 2kg / ≥3kg |
| Reach | 740mm |
| Repeatability | ～0.1mm |
| 供电 | Voltage 24V，Current > 20A |
| 接口 | Ethernet |
| 用户操作系统 | Ubuntu |
| 功率 | MAX 500w |
| 力反馈与碰撞检测 | Provide |
| 控制接口 | Position + Force Control |
| 关节范围/速度 | J1 ±150° 180°/s；J2 0-180° 180°/s；J3 −165°-0 180°/s；J4 ±80° 180°/s；J5 ±85° 180°/s；J6 ±160° 180°/s |
| **Z1 关节电机（页面 "FUNCTION / PARAMETER" 表）** | Backlash ～6 arcmin；Communication Method RS 485；**Maximum Torque 33N·m**；**Encoder Resolution 15bit**；Weight 405g；Size Φ65*52mm；**Force Control Accuracy ～0.2N·m**；**Control Frequency 1KHz**；Reducer **Harmonic Reducer**；Bearing Industrial grade cross roller；Reduction Ratio **60+**；Motor Sensing Feedback Torque, Angle, Angular Velocity；Voltage 24V(Recommend)；Motor Control Command **Torque, Angle, Angular Velocity, Stiffness, Damping** |
| 官方脚注 [2]（原文） | "Since the reduction ratio used by each joint is relatively low, the position control stiffness of the whole machine is low. If the control mode is not optimized, there will be large position control error and shaking when the manipulator moves." |
| 价格 | **$15,999.00 USD**（https://shop.unitree.com/products/unitree-z1）；商城列表页同价 |

### B6. 官方模型仓库逐关节 effort / 力矩上限（最强证据）

**仓库勘误**：`unitree_mjcf` 与 `unitree_motors_sdk` **不存在（404）**。官方 MJCF 在 **`unitree_mujoco`** 仓库的 `unitree_robots/` 目录下；官方 URDF 在 **`unitree_ros`** 仓库 `robots/` 下。`unitree_model` 仓库只放 USD/DAE（27 个文件；目录：`G1/29dof`、`B2`、`Go2`、`H1/h1`、`H2`、`H2_Plus`），**不含 XML/URDF**。

存在的模型文件（`git ls-tree -r` 实测清单，仅列人形相关）：
```
unitree_robots/g1/g1_23dof.xml        unitree_robots/g1/g1_29dof.xml
unitree_robots/g1/scene.xml           unitree_robots/g1/scene_23dof.xml   unitree_robots/g1/scene_29dof.xml
unitree_robots/h1/h1.xml              unitree_robots/h1/scene.xml         unitree_robots/h1/scene_terrain.xml
unitree_robots/h1_2/h1_2_handless.xml unitree_robots/h1_2/scene.xml
unitree_robots/h2/h2_mujoco.xml       unitree_robots/h2/scene.xml
unitree_robots/r1/R1_C++.xml          unitree_robots/r1/scene.xml
（另有 a2/ as2/ b2/ b2w/ go2/ go2w/ 与 terrain_tool/scene.xml）
```
`unitree_ros/robots/` 人形目录实测清单：`g1_description/`（22 个 URDF：`g1_23dof.urdf`, `g1_23dof_rev_1_0.urdf`, `g1_23dof_mode_10.urdf`, `g1_29dof.urdf`, `g1_29dof_rev_1_0.urdf`, `g1_29dof_lock_waist*.urdf`, `g1_29dof_mode_11/12/13/14/15/16/18.urdf`, `g1_29dof_with_hand.urdf`, `g1_29dof_with_hand_rev_1_0.urdf`, `g1_29dof_rev_1_0_with_inspire_hand_DFQ/FTP.urdf`, `g1_comp.urdf`, `g1_dual_arm.urdf`, `g1_pl.urdf`, `inspire_hand/*_hand.urdf`）、`g1_d_description/g1_d.urdf`、`g1_with_brainco_hand/`、`h1_description/urdf/h1.urdf|h1_with_hand.urdf`、`h1_2_description/h1_2.urdf|h1_2_handless.urdf|h1_2_with_FTP_hand.urdf`、`h2_description/H2.urdf|H2_dae.urdf|H2_loop.urdf`、`h2_plus/H2_Plus.urdf`、`h2d_description/h2d.urdf`、`r1_description/R1.urdf`、`r1_air_description/R1_AIR.urdf`、`r1_a5_description/r1_a5.urdf`、`r1_a7_description/r1_a7.urdf`、`r1_7a_description/R1_7a.urdf`、`r1d_description/r1d.urdf`、`z1_description/`、`dexterous_hand_description/dex2_5/…`

#### B6.1 G1 官方 MJCF 逐关节（motor actuator `ctrlrange`，单位 N·m）
文件（两文件 29dof/23dof 的 motor 段**完全相同**）：
- https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/g1/g1_29dof.xml
- https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/g1/g1_23dof.xml
分级：官方仓库文件

| 关节 | ctrlrange |
|---|---|
| left/right_hip_pitch | −88 ~ 88 |
| left/right_hip_roll | −88 ~ 88 |
| left/right_hip_yaw | −88 ~ 88 |
| left/right_knee | **−139 ~ 139** |
| left/right_ankle_pitch | −50 ~ 50 |
| left/right_ankle_roll | −50 ~ 50 |
| waist_yaw | −88 ~ 88 |
| waist_roll / waist_pitch | −50 ~ 50 |
| shoulder_pitch / shoulder_roll / shoulder_yaw / elbow / wrist_roll（左右） | −25 ~ 25 |
| wrist_pitch / wrist_yaw（左右） | −5 ~ 5 |

其余：`<compiler angle="radian" meshdir="meshes"/>`；`<body name="pelvis" pos="0 0 0.793">`。
默认类共 5 组：**`torso_motor` / `leg_motor` / `ankle_motor` / `arm_motor` / `wrist_motor`**（类名直接对应官方对关节电机的分组）。
每组内均为 `<joint damping="0.05" armature="0.01" frictionloss="0.2"/>`，**唯一例外 `wrist_motor` 的 `frictionloss="0.1"`**。
**关节 `<joint>` 标签本身不写 effort/velocity**，力矩上限只在 motor 的 ctrlrange 上。

#### B6.2 G1 官方 URDF 逐关节 `effort` / `velocity`（分级：官方仓库文件）
文件：https://raw.githubusercontent.com/unitreerobotics/unitree_ros/master/robots/g1_description/g1_29dof_rev_1_0.urdf

| 关节 | effort (N·m) | velocity (rad/s) | lower~upper (rad) | origin xyz（相对父件，m） |
|---|---|---|---|---|
| left/right_hip_pitch | 88 | 32 | −2.5307 ~ 2.8798 | 0 ±0.064452 −0.1027 |
| **left/right_hip_roll** | **139** | 20 | 左 −0.5236~2.9671；右 −2.9671~0.5236 | 0 ±0.052 −0.030465，rpy `0 -0.1749 0` |
| left/right_hip_yaw | 88 | 32 | −2.7576 ~ 2.7576 | 0.025001 0 −0.12412 |
| left/right_knee | 139 | 20 | −0.087267 ~ 2.8798 | −0.078273 ±0.0021489 −0.17734，rpy `0 0.1749 0` |
| left/right_ankle_pitch | **35** | **30** | −0.87267 ~ 0.5236 | 0 ∓9.4445E-05 −0.30001 |
| left/right_ankle_roll | 35 | 30 | −0.2618 ~ 0.2618 | 0 0 −0.017558 |
| waist_yaw | 88 | 32 | −2.618 ~ 2.618 | 0 0 0 |
| waist_roll | 35 | 30 | −0.52 ~ 0.52 | −0.0039635 0 **0.044** |
| waist_pitch | 35 | 30 | −0.52 ~ 0.52 | 0 0 0 |
| shoulder_pitch / shoulder_roll / shoulder_yaw / elbow / wrist_roll | 25 | 37 | 见 B1 限位表 | shoulder_pitch origin `0.0039563 ±0.10022 0.24778`（MJCF 同文件写 **0.23778** — 见下）|
| wrist_pitch / wrist_yaw | 5 | 22 | −1.614429558 ~ 1.614429558 | 0.038 0 0 / 0.046 0 0 |

**同一官方仓库内冲突（务必保留，不要择一）**：`robots/g1_description/g1_29dof_with_hand.urdf` 与 `g1_23dof_rev_1_0.urdf` 中 **hip_roll 的 effort = 88**，而 `g1_29dof_rev_1_0.urdf` 中 **hip_roll effort = 139**。实测（同文件同关节）：

| 文件 | left_hip_roll_joint effort | left_knee_joint | left_ankle_pitch | waist_roll |
|---|---|---|---|---|
| `g1_29dof_rev_1_0.urdf` | **139** | 139 | 35 | 35 |
| `g1_29dof_with_hand.urdf` | **88** | 139 | 35 | 35 |

`g1_23dof_rev_1_0.urdf` 分组：139（hip_roll+knee 共 4 个）/ 88（5 个）/ 35（4 个踝）/ 25（10 个臂）— 无 wrist_pitch/yaw。
`g1_29dof_with_hand.urdf` 另有内置三指手关节：thumb_0 **2.45 N·m @3.14 rad/s**（左右 2 个），thumb_1/thumb_2/middle_0/middle_1 等 **1.4 N·m @12 rad/s**（12 个）。

#### B6.3 G1 / H1 / H2 / R1 其它官方模型逐关节

**H1** — https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h1/h1.xml （`<motor class="h1">`）
knee **±300**；hip_roll/hip_pitch/hip_yaw/torso **±200**；ankle **±40**；shoulder_pitch/shoulder_roll **±40**；shoulder_yaw/elbow **±18**；另有一个 `not_use_joint`（无 ctrlrange）。
限位：hip_yaw/hip_roll ±0.43；hip_pitch −3.14~2.53；knee −0.26~2.05；ankle −0.87~0.52；torso −2.35~2.35；shoulder_pitch ±2.87；shoulder_roll 左 −0.34~3.11 / 右 −3.11~0.34；shoulder_yaw 左 −1.3~4.45 / 右 −4.45~1.3；elbow −1.25~2.61。

**H1-2** — https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h1_2/h1_2_handless.xml
knee **±300**；hip_pitch/hip_roll/hip_yaw/torso **±200**；ankle_pitch **±60**；ankle_roll **±40**；shoulder_pitch/shoulder_roll **±40**；shoulder_yaw/elbow **±18**；wrist_roll/pitch/yaw **±19**。
`unitree_ros/master/robots/h1_2_description/h1_2_handless.urdf` 分组：300@14（knee×2）、**200@23**（hip×6 + torso）、**60@9**（ankle_pitch×2）、40@9（ankle_roll×2 + shoulder_pitch/roll×4）、**19@31.4**（wrist×6）、18@20（shoulder_yaw + elbow ×4）。

**H2** — https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h2/h2_mujoco.xml
hip_pitch/hip_roll/hip_yaw/knee **±360**；ankle_pitch **±66.88**；ankle_roll **±19**；waist_yaw **±120**；waist_roll/waist_pitch **±180**；shoulder_pitch **±130**；shoulder_roll/yaw/elbow/wrist_roll **±60**；wrist_pitch/wrist_yaw **±10**；head_pitch/head_yaw **±50**。
`unitree_ros/master/robots/h2_description/H2.urdf` 分组：360@20（hip×6 + knee×2）、180@28.375（waist_roll/pitch）、130@21.9（shoulder_pitch×2）、120@28.375（waist_yaw）、66.88@28.61（ankle_pitch×2）、60@18.7（shoulder_roll/yaw, elbow, wrist_roll ×8）、50@10（head×2）、19@100.7（ankle_roll×2）、10@37.7（wrist_pitch/yaw ×4）。

**R1** — https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/r1/R1_C++.xml （文件名含 `+`，实际抓取需百分号编码为 `R1_C%2B%2B.xml`）
hip_pitch/hip_roll/hip_yaw/knee **±88/±88/±88/±139**（hip 三项 ±88，knee ±139）；ankle_pitch/ankle_roll **±50**；waist_yaw **±88**；waist_roll **±50**；`waist_pitch_joint`、`left/right_wrist_pitch_joint`、`left/right_wrist_yaw_joint` 四个 motor **没有 ctrlrange**（无上限声明）；shoulder×3/elbow/wrist_roll **±25**。
`unitree_ros/master/robots/r1_description/R1.urdf` 分组：**60@18.8（14 个关节：hip×6 + knee×2 + shoulder_pitch/roll×4 + elbow×2）**、**50@30（ankle_pitch/roll ×4）**、**33@33.4（8 个：shoulder_yaw, elbow, wrist_roll 等）**。
> 注意 R1 的 MJCF（hip 88 / knee 139 / shoulder 25）与 URDF（hip 60 / knee 60 / shoulder_pitch 60, shoulder_yaw/elbow 33）**成组不同**，两个都是官方仓库文件，属仓库间不一致，需并列。

#### B6.4 官方 MJCF 关节几何（G1 29dof，`<body pos>`，单位 m，官方仓库文件）
`pelvis 0 0 0.793`；hip_pitch `0 ±0.064452 −0.1027`；hip_roll `0 ±0.052 −0.030465`；hip_yaw `0.025001 0 −0.12412`；knee `−0.078273 ±0.0021489 −0.17734`；ankle_pitch `0 ∓9.4445e-05 −0.30001`；ankle_roll `0 0 −0.017558`；waist_yaw（无 pos）；waist_roll `−0.0039635 0 0.035`；torso `0 0 0.019`；shoulder_pitch `0.0039563 ±0.10022 0.23778`；shoulder_roll `0 ±0.038 −0.013831`；shoulder_yaw `0 ±0.00624 −0.1032`；elbow `0.015783 0 −0.080518`；wrist_roll `0.1 ±0.00188791 −0.01`；wrist_pitch `0.038 0 0`；wrist_yaw `0.046 0 0`。
> 与 URDF 的差异（两源并列）：`waist_roll` z = **0.035**（MJCF）vs **0.044**（URDF rev_1_0）；`shoulder_pitch` z = **0.23778**（MJCF）vs **0.24778**（URDF rev_1_0）。
> 由 hip_yaw→knee (−0.17734, 含 x −0.078273) 与 knee→ankle_pitch (−0.30001) 可得官方模型里的大腿/小腿关节偏置；**不要**据此自行折算成营销页的 "Calf + Thigh Length 0.6M"。

#### B6.5 G1 关节电机型号名（官方仓库文件，unitree_rl_lab）
文件：https://raw.githubusercontent.com/unitreerobotics/unitree_rl_lab/main/source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py
`UNITREE_G1_29DOF_CFG.actuators` 的键名给出电机型号（**这是官方仓库里唯一给出 G1 关节电机型号名的地方**）：

| 型号名 | 关节（joint_names_expr） | effort_limit_sim | velocity_limit_sim | stiffness | damping | armature |
|---|---|---|---|---|---|---|
| **N7520-14.3** | `.*_hip_pitch_.*`, `.*_hip_yaw_.*`, `waist_yaw_joint` | **88** | **32.0** | hip 100.0 / waist_yaw 200.0 | hip 2.0 / waist_yaw 5.0 | 0.01 |
| **N7520-22.5** | `.*_hip_roll_.*`, `.*_knee_.*` | **139** | **20.0** | hip_roll 100.0 / knee 150.0 | hip_roll 2.0 / knee 4.0 | 0.01 |
| **N5020-16** | `.*_shoulder_.*`, `.*_elbow_.*`, `.*_wrist_roll.*`, `.*_ankle_.*`, `waist_roll_joint`, `waist_pitch_joint` | **25** | **37** | 40.0 | shoulder/elbow/wrist_roll 1.0；ankle 2.0；waist_* 5.0 | 0.01 |
| **W4010-25** | `.*_wrist_pitch.*`, `.*_wrist_yaw.*` | **5** | （见文件） | — | — | — |

`UNITREE_G1_23DOF_CFG` 的键名同样是 N7520-14.3 / N7520-22.5 / N5020-16，另加 **N5020-16-parallel**：`.*ankle.*` → **effort_limit_sim 35, velocity 30, stiffness 40.0, damping 2.0, armature 0.01**（与 URDF 的 35/30 一致，与 29dof 模型文件 N5020-16 的 25/37 不同）。

`UNITREE_H1_CFG`（同文件）：
| 型号名 | 关节 | effort_limit | velocity_limit | stiffness | damping |
|---|---|---|---|---|---|
| GO2HV-1 | `.*ankle.*`, shoulder_pitch, shoulder_roll | 40 | 9 | ankle 40.0 / shoulder 100.0 | 2.0 |
| GO2HV-2 | shoulder_yaw, elbow | 18 | 20 | 50 | 2.0 |
| **M107-24-1** | `.*_knee_.*` | **300.0** | 14.0 | 200.0 | 4.0 |
| **M107-24-2** | `.*_hip_.*`, `torso_joint` | **200** | 23.0 | hip 150.0 / torso 300.0 | hip 2.0 / torso 6.0 |
（`armature=0.01`；`joint_sdk_names` 顺序即消息序，索引 9 为空字符串 `""`）

---

## C. 人形控制栈数字

### C1. DDS 消息字段（官方仓库文件 + 官方头文件，一致）

**`MotorCmd_`** — https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/MotorCmd_.hpp（译注：源 IDL 文件名 `MotorCmd_.idl`，Cyclone DDS v0.10.2 生成）
| 字段 | 类型 |
|---|---|
| `mode` | uint8（默认 0） |
| `q` | float32 |
| `dq` | float32 |
| `tau` | float32 |
| `kp` | float32 |
| `kd` | float32 |
| `reserve` | uint32 |

**`LowCmd_`** — https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/LowCmd_.hpp
`mode_pr` uint8 · `mode_machine` uint8 · `motor_cmd` **`std::array<MotorCmd_, 35>`** · `reserve` `uint32[4]` · `crc` uint32

**`MotorState_`** — https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/MotorState_.hpp
`mode` uint8 · `q` float32 · `dq` float32 · **`ddq` float32** · **`tau_est` float32** · `temperature` `int16[2]` · `vol` float32 · `sensor` `uint32[2]` · `motorstate` uint32 · `reserve` `uint32[4]`

**`LowState_`** — https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/LowState_.hpp
`version` `uint32[2]` · `mode_pr` uint8 · `mode_machine` uint8 · `tick` uint32 · `imu_state` IMUState_ · `motor_state` **`std::array<MotorState_, 35>`** · `wireless_remote` `uint8[40]` · `reserve` `uint32[4]` · `crc` uint32

**ROS2 等价定义**（官方仓库文件；数组同为 35）：
- https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/LowCmd.msg → `uint8 mode_pr / uint8 mode_machine / MotorCmd[35] motor_cmd / uint32[4] reserve / uint32 crc`
- https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/MotorCmd.msg → `uint8 mode / float32 q / float32 dq / float32 tau / float32 kp / float32 kd / uint32 reserve`
- https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/MotorState.msg → `uint8 mode / float32 q / float32 dq / float32 ddq / float32 tau_est / int16[2] temperature / float32 vol / uint32[2] sensor / uint32 motorstate / uint32[4] reserve`
- https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/LowState.msg → `uint32[2] version / uint8 mode_pr / uint8 mode_machine / uint32 tick / IMUState imu_state / MotorState[35] motor_state / uint8[40] wireless_remote / uint32[4] reserve / uint32 crc`
（分支：`master`。`unitree_hg/msg/` 下另有 `BmsCmd/BmsState/HandCmd/HandState/IMUState/MainBoardState/PressSensorState/…`）

### C2. Topic 名与控制频率

| 事实 | 值 | 来源 | 分级 |
|---|---|---|---|
| 低层下发 topic | `rt/lowcmd`，类型 `unitree_hg::msg::dds_::LowCmd_`；控制全身关节电机（不含灵巧手）、电池等 | https://doc-cdn.unitree.com/11/252/en/11_252_en（G1 `DDS Services Interface`，更新 2025-11-24 16:24:25）；同文 https://doc-cdn.unitree.com/25/1123/en/25_1123_en（H2）、R1 文档 | 官方页面(文档中心) |
| 低层回传 topic | `rt/lowstate`（LowState_，IMU + motors）；**另有低频版 `rt/lf/lowstate`**；`rt/lf/mainboardstate`（MainBoardState_） | 同上 | 官方页面(文档中心) |
| **G1 例程默认下发频率** | 原文：**"A low-level command sending thread that executes periodically, calling the function `G1Example::LowCommandWriter` at a default frequency of **500Hz**."**；"A user-defined control logic thread, the motor control thread, calling `G1Example::Control` at a default frequency of **500Hz**." | https://doc-cdn.unitree.com/11/248/en/11_248_en（G1 `Basic Motion Routine`，更新 2026-07-20 15:28:44） | 官方页面(文档中心) |
| R1 同口径 | 同样两句，**500Hz** | https://doc-cdn.unitree.com/27/... `R1_developer_basic_motion_routine.md` | 官方页面(文档中心) |
| SDK 源码交叉验证 | `control_dt_;  // [2ms]`；`control_dt_(0.002)`；`CreateRecurrentThreadEx("command_writer", UT_CPU_ID_NONE, **2000**, &G1Example::LowCommandWriter, this)`；`CreateRecurrentThreadEx("control", …, **2000**, &G1Example::Control, this)` — 周期 **2000 µs** ⇒ 500 Hz | https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/example/g1/low_level/g1_ankle_swing_example.cpp （行 152/175/202/203）；`g1_dual_arm_example.cpp` 行 153/172/211/214 同 | 官方仓库文件 |
| G1-D 例程 | `double control_dt = 0.002;`（同 500 Hz） | https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/example/g1/g1d/g1d_arm_example.cpp 行 265 | 官方仓库文件 |
| `G1_NUM_MOTOR` | `const int G1_NUM_MOTOR = 29;`（例程侧 29；DDS 数组是 35） | 同上 `g1_ankle_swing_example.cpp` | 官方仓库文件 |
| **`rt/lowstate` 的确切频率** | **未取到**（文档中心只区分 `rt/lowstate` 与 `rt/lf/lowstate`「low-frequency mode」，未给 Hz；SDK 是回调驱动） | — | — |
| 命令字段实际写法语义 | `motor_cmd().at(i).tau() = mc->tau_ff.at(i); .q() = mc->q_target.at(i); .dq() = mc->dq_target.at(i); .kp() = mc->kp.at(i); .kd() = mc->kd.at(i);` | https://doc-cdn.unitree.com/11/248/en/11_248_en；`g1_ankle_swing_example.cpp` | 官方页面(文档中心) / 官方仓库文件 |
| CRC 计算 | `dds_low_command.crc() = Crc32Core((uint32_t *)&dds_low_command, (sizeof(dds_low_command) >> 2) - 1);` | 同上 | 官方页面(文档中心) |
| SDK 例程默认 Kp/Kd（G1，长 29，按消息序） | 原文 `std::array<float, G1_NUM_MOTOR> Kp{ 60, 60, 60, 100, 40, 40, // legs` `60, 60, 60, 100, 40, 40, // legs` `60, 40, 40, // waist` `40, 40, 40, 40, 40, 40, 40, // arms` `40, 40, 40, 40, 40, 40, 40 // arms }`；`Kd{ 1, 1, 1, 2, 1, 1, // legs` `1, 1, 1, 2, 1, 1, // legs` `1, 1, 1, // waist` `1, 1, 1, 1, 1, 1, 1, // arms` `1, 1, 1, 1, 1, 1, 1 // arms }`（源文件行 67-73 与 76-82） | https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/example/g1/low_level/g1_ankle_swing_example.cpp | 官方仓库文件 |

### C3. 文档里的 G1 力矩上限值

| 表述 | 数值 | 来源 | 分级 |
|---|---|---|---|
| 「最大膝关节力矩」 | G1 **90 N.m**；G1 EDU **120 N.m**（脚注 [1]：整机各关节电机最大扭矩不同，此为其最大者的值） | https://www.unitree.com/g1 ；文档中心 https://doc-cdn.unitree.com/11/223/en/11_223_en | 官方页面 / 官方页面(文档中心) |
| 「G1 关节电机最大扭矩」 | **120 N.m**（关节电机小节正文，未指明哪个关节） | doc-cdn `11/223` | 官方页面(文档中心) |
| 官方 URDF `effort`（g1_29dof_rev_1_0.urdf） | hip_pitch/yaw 88，hip_roll **139**，knee **139**，ankle 35，waist_yaw 88，waist_roll/pitch 35，肩/肘/腕roll 25，腕 pitch/yaw 5 | https://raw.githubusercontent.com/unitreerobotics/unitree_ros/master/robots/g1_description/g1_29dof_rev_1_0.urdf | 官方仓库文件 |
| 官方 URDF `effort`（g1_29dof_with_hand.urdf, g1_23dof_rev_1_0.urdf） | hip_roll **88**（与上行冲突），其余同 | …/g1_29dof_with_hand.urdf ；…/g1_23dof_rev_1_0.urdf | 官方仓库文件 |
| 官方 MJCF `ctrlrange`（g1_29dof.xml, g1_23dof.xml） | hip 三项 88，knee **139**，ankle **50**，waist_yaw 88，waist_roll/pitch **50**，臂 25，腕 pitch/yaw 5 | https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/g1/g1_29dof.xml ；…/g1_23dof.xml | 官方仓库文件 |
| 官方 RL 配置 `effort_limit_sim` | hip_pitch/yaw + waist_yaw 88；hip_roll + knee **139**；shoulder/elbow/wrist_roll/**ankle**/**waist_roll/pitch** 25；wrist_pitch/yaw 5（29dof）；23dof 踝 **35** | https://raw.githubusercontent.com/unitreerobotics/unitree_rl_lab/main/source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py | 官方仓库文件 |

**四处口径的踝关节上限互不相同（并列，勿择一）**：产品页未列 → URDF **35** → MJCF **50** → rl_lab 29dof 模型 **25** → rl_lab 23dof 模型 **35**。
**膝关节四处口径**：产品页 90/120 → 文档中心正文 120 → URDF **139** → MJCF **139** → rl_lab **139**。

### C4. 强化学习仓库口径

#### C4.1 `unitree_rl_gym`（https://github.com/unitreerobotics/unitree_rl_gym ，分支默认）

| 项 | 值 | 文件（raw URL 前缀 `https://raw.githubusercontent.com/unitreerobotics/unitree_rl_gym/master/`） |
|---|---|---|
| 支持机型（README 原文） | "supporting Unitree **Go2, H1, H1_2, and G1**" | `README.md` 行 9 ｜ 官方仓库文件 |
| `--task` 取值 | `(go2, g1, h1, h1_2)` | `README.md` 行 48 ｜ 官方仓库文件 |
| 实机部署配置名 | `g1.yaml`, `h1.yaml`, `h1_2.yaml` | `README.md` 行 134；目录实测 `deploy/deploy_mujoco/configs/` 与 `deploy/deploy_real/configs/` 各 3 个同名文件 ｜ 官方仓库文件 |
| **G1 实机控制周期** | **`control_dt: 0.02`** ⇒ 策略输出 **50 Hz** | `deploy/deploy_real/configs/g1.yaml` ｜ 官方仓库文件 |
| G1 msg_type / imu_type | `"hg"` / `"pelvis"` | 同上 |
| G1 topic | `lowcmd_topic: "rt/lowcmd"`；`lowstate_topic: "rt/lowstate"` | 同上 |
| G1 模型路径默认 | `{LEGGED_GYM_ROOT_DIR}/deploy/pre_train/g1/motion.pt` | 同上 |
| G1 腿部关节索引/增益 | `leg_joint2motor_idx: [0…11]`；`kps: [100,100,100,150,40,40, 100,100,100,150,40,40]`；`kds: [2,2,2,4,2,2, 2,2,2,4,2,2]`；`default_angles: [-0.1,0,0,0.3,-0.2,0, -0.1,0,0,0.3,-0.2,0]` | 同上 |
| G1 臂+腰 | `arm_waist_joint2motor_idx: [12,13,14, 15,16,17,18,19,20,21, 22,23,24,25,26,27,28]`；`arm_waist_kps: [300,300,300, 100,100,50,50,20,20,20, 100,100,50,50,20,20,20]`；`arm_waist_kds: [3,3,3, 2,2,2,2,1,1,1, 2,2,2,2,1,1,1]`；`arm_waist_target` 全 0 | 同上 |
| G1 观测/动作尺度 | `ang_vel_scale: 0.25`；`dof_pos_scale: 1.0`；`dof_vel_scale: 0.05`；**`action_scale: 0.25`**；`cmd_scale: [2.0,2.0,0.25]`；`num_actions: 12`；`num_obs: 47`；`max_cmd: [0.8,0.5,1.57]` | 同上 |
| 训练侧 G1 配置 | `control_type = 'P'`；**`action_scale = 0.25`**；**`decimation = 4`**；`stiffness {hip_yaw 100, hip_roll 100, hip_pitch 100, knee 150, ankle 40}`；`damping {hip_yaw 2, hip_roll 2, hip_pitch 2, knee 4, ankle 2}`；`num_observations 47`/`num_privileged_obs 50`/`num_actions 12`；`soft_dof_pos_limit 0.9`；`base_height_target 0.78`；模型文件 `resources/robots/g1_description/g1_12dof.urdf` | `legged_gym/envs/g1/g1_config.py` ｜ 官方仓库文件 |
| **sim dt（策略频率推导）** | 基类 `class sim: dt = 0.005; substeps = 1; gravity [0,0,-9.81]` ⇒ 控制周期 = decimation 4 × 0.005 = **0.02 s ⇒ 50 Hz**（与 deploy yaml 的 0.02 相符） | `legged_gym/envs/base/legged_robot_config.py` ｜ 官方仓库文件 |
| 注释原文 | `# decimation: Number of control action updates @ sim DT per policy DT`；`# action scale: target angle = actionScale * action + defaultAngle` | 同上 |
| H1 训练增益 | `control_type='P'`；stiffness {hip_yaw 150, hip_roll 150, hip_pitch 150, knee 200, ankle 40, torso 300, shoulder 150, elbow 100}；damping {hip 2×3, knee 4, ankle 2, torso 6, shoulder 2, elbow 2} | `legged_gym/envs/h1/h1_config.py` ｜ 官方仓库文件 |
| C++ 实机例程位置 | `deploy/deploy_real/cpp_g1`，运行 `./g1_deploy_run {net_interface}` | `README.md` 行 145-176 |

#### C4.2 `unitree_rl_lab`（https://github.com/unitreerobotics/unitree_rl_lab ，分支 `main`）

| 项 | 值 | 文件（raw 前缀 `https://raw.githubusercontent.com/unitreerobotics/unitree_rl_lab/main/source/unitree_rl_lab/unitree_rl_lab/`） |
|---|---|---|
| 支持机型（tasks 目录实测） | locomotion：`robots/g1/`（子目录 `23dof`,`29dof`）、`robots/go2/`、`robots/h1/`；mimic：`robots/g1_29dof/`（`dance_102`,`gangnanm_style`）。`assets/robots/unitree.py` 定义 `UNITREE_H1_CFG`, `UNITREE_G1_23DOF_CFG`, `UNITREE_G1_29DOF_CFG`, `UNITREE_G1_29DOF_MIMIC_CFG`（**未搜到 `UNITREE_H1_2_CFG`**）。deploy 配置目录实测：`b2`, `go2`, `go2w`, `h1`, `h1_2`, `g1_23dof`, `g1_29dof` | 官方仓库文件 |
| **G1 29dof 策略频率** | `self.decimation = 4`；`self.sim.dt = 0.005` ⇒ **50 Hz**；`self.sim.render_interval = self.decimation`；`height_scanner.update_period = self.decimation * self.sim.dt` | `tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py`（行 376/379/380/386/387）｜ 官方仓库文件 |
| go2 / h1 / mimic 同 | 三处同样 `decimation = 4`、`sim.dt = 0.005` | `tasks/locomotion/robots/go2/velocity_env_cfg.py`(385/388)、`.../h1/velocity_env_cfg.py`(387/390)、`tasks/mimic/robots/g1_29dof/{dance_102,gangnanm_style}/tracking_env_cfg.py`(331/334) |
| G1 29dof 动作尺度 | `JointPositionAction = mdp.JointPositionActionCfg(asset_name="robot", joint_names=[".*"], **scale=0.25**, use_default_offset=True)` | `tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py`（ActionsCfg）｜ 官方仓库文件 |
| mimic 动作尺度 | 用字典 `UNITREE_G1_29DOF_MIMIC_ACTION_SCALE`，由 `effort_limit_sim / stiffness` 逐关节算出（`scale=UNITREE_G1_29DOF_MIMIC_ACTION_SCALE`，`use_default_offset=True`） | `assets/robots/unitree.py` 行 706 起；`tasks/mimic/robots/g1_29dof/dance_102/tracking_env_cfg.py` 行 129 |
| 动作空间尺寸 | `num_actions: 12` | rl_gym G1 配置（注意是 **g1_12dof.urdf**，仅腿+腰） |
| 参考动作数据率 | `G1_Take_102.bvh_60hz.npz`、`G1_gangnam_style_V01.bvh_60hz.npz`；转换命令示例 `csv_to_npz.py -f …_60hz.csv --input_fps 60`；deploy yaml `fps: 60` | `tasks/mimic/robots/g1_29dof/dance_102/tracking_env_cfg.py` 行 90-91；`deploy/robots/g1_29dof/config/config.yaml` |
| 实机 FixStand 增益（29dof，按消息序 29 长） | `kp: [100,100,100,150,40,40, 100,100,100,150,40,40, 200,200,200, 40×7, 40×7]`；`kd: [2,2,2,4,2,2, 2,2,2,4,2,2, 5,5,5, 10×7, 10×7]`；Passive `mode[]` 全 1，`kd` 全 3 | `deploy/robots/g1_29dof/config/config.yaml` ｜ 官方仓库文件 |
| 默认站立姿态 `qs` | `[-0.1,0,0,0.3,-0.2,0, -0.1,0,0,0.3,-0.2,0, 0,0,0, 0,0.25,0,0.97,0.15,0,0, 0,-0.25,0,0.97,-0.15,0,0]` | 同上 |
| FSM id | Passive 1 / FixStand 2 / Velocity 3 (`type: RLBase`) / Mimic_Dance_102 101 / Mimic_Gangnam_Style 102 | 同上 |
| 资产引用 | `UNITREE_MODEL_DIR`：`G1/29dof/usd/g1_29dof_rev_1_0/g1_29dof_rev_1_0.usd`、`H1/h1/usd/h1.usd`；注释掉的 URDF 路径 `unitree_ros/robots/g1_description/g1_29dof_rev_1_0.urdf`、`robots/h1_description/urdf/h1.urdf` | `assets/robots/unitree.py` ｜ 官方仓库文件 |

#### C4.3 其他官方 RL/仿真仓库（实测存在，规格未展开）
`unitree_mujoco`（Mjcf 见 B6）、`unitree_rl_mjlab`、`unitree_sim_isaaclab`、`unitree_model`、`unitree_sdk2_python`、`unitree_ros`、`unitree_ros2`、`xr_teleoperate`、`unifolm-wla`、`unifolm-world-model-action`、`teleimager`、`televuer`、`UniArmL1`、`unitree_slam`、`unitree_lerobot`、`dex1_1_service`、`brainco_hand_service`、`.r1-7a_sdk`。

---

## D. 未取到 / 不可核实

**明确查不到、且不打算用推测值填充：**

1. **GO-M8010-6 的额定（rated / continuous）转矩**：官网与文档中心只有 `Maximum Torque 23.7 N·m`，无 rated/continuous 行。
2. **GO-M8010-6 命令的位置/速度/转矩「分辨率」的官方字面数值**：只有量化系数（转矩 ×256、速度 256/2π、位置 32768/2π、kp/kd 32768/25.6）与「建议物理范围」；未出现 "resolution" 一词的独立条目。
3. **GO-M8010-6 是否多圈**：文档中心 About 页写 **single-turn**（单圈）绝对值编码器，而协议页把 `position` 标为 **multi-turn accumulated**。这是官方两页的措辞冲突，**不是我的推断**；无第三处官方口径可裁决。
4. **IM6014 的「多个峰值扭矩变体」**：官方 `https://www.unitree.com/IM6014/` 与文档中心 `30/1371` 只给 **一个型号 `N6014B-12.6`（3:38）**。**其它减速比/峰值扭矩变体（如常见的 −14/−20/−25 说法）在本次抓取的全部官方来源中均未出现**，无法核实，也不应写入。
5. **IM6014 的「控制频率」独立条目**：产品页无 `Control Frequency` 行；文档中心给的是 **`Max Bus Polling Frequency 10000 Hz`**（总线轮询上限），不等于内部控制环频率。IM6014 内部控制环频率：**未取到**。
6. **IM6014 供电电压**：同一文档中心页同时出现 **24V~75V**（规格表）与 **24V~72V**（供电注记，且原文把型号写成 "M6014"）。两值并列，不取其一。
7. **IM6014 电机 ID**：产品页 **0-14**；协议页 **0~14 + 15 广播 / 15 保留**；STM32 页参数表 **`id` 0-15**。三处并列。
8. **G1 官方页面的膝/髋/腰/肩/肘/腕「各自个数」拆表**：页面只给 leg 6 / arm 5 / waist 1 / hand 7+2(EDU)，**未给 shoulder/elbow/wrist 各自数量**（须从 URDF/MJCF 数，已在 B1 注明推导来源）。
9. **G1 `rt/lowstate` 的确切 Hz**：文档中心与 SDK 均未标注（仅有 `rt/lf/lowstate` "low-frequency mode" 字样，无数值）。500 Hz 只对 **`rt/lowcmd` 下发线程与控制线程**成立。
10. **G1 EDU 的 "PC2 = Jetson Orin NX 16GB" 是否标配**：`https://www.unitree.com/g1` 表里 EDU 的高算力模块只写 "Multiple brands and models available such as Orin, etc."；文档中心表写 "NVIDIA Jetson Orin"；16G 只出现在文档中心 Jetson Orin NX 参数小节。**官方未写"标配/选配"的确切措辞到 16GB 这一档**，请勿写成定式配置。
11. **R1 电池容量 / 电压 / 串数**：官方页面与文档中心都只写 "Lithium battery"、"Smart Battery (Quick Release) Yes"、续航 "About 1h"，**无 mAh / V / 串数**。
12. **R1 整机总扭矩、各关节额定扭矩**：官方页面表 "Maximum Torque of Arm Joint【1】" 一格填的是 **"About 2kg"**（疑为官网表格错位，文档中心同字段是 "Max Arm Payload"）。**R1 的 N·m 级关节力矩：官方页面与文档中心未给**，只有模型文件里的 88/139/50/25（MJCF）与 60/50/33（URDF）两套。
13. **R1 总自由度**：官方页面 "26-40"（EDU 栏）与文档中心表格 "20 / 26 / 26" 冲突；宣传块又写 "20-26-DOF"。三处并列。
14. **Dex3-1 / Dex5-1 的价格**：`www.unitree.com/Dex3-1`、`/Dex5-1` 页面**无任何价格字符串**；`shop.unitree.com` 商品 sitemap 的 33 个 URL 中**不含任何 Dex 灵巧手**（`products.json?limit=250` 持续 `429 local_rate_limited`，未能穷举）。**灵巧手价格：未取到**。
15. **IM6014 价格**：商品页 **269.00 USD** vs 商城列表页 **$10.00 USD**（疑占位价）。两者并列，不可采信单一值。
16. **Z1 是否仍在售 / 关节电机型号名**：`https://www.unitree.com/z1` 的 FUNCTION 表未标电机型号名；商城 `/products/unitree-z1` 给出 **$15,999.00 USD**。
17. **H1 / H1-2 的「价格」**：`www.unitree.com/h1` 页面**无价格字符串**；商城列表页 "Unitree H1（Contact us for the real price）– $90,000.00 USD"（商品名自带「以真实价联系我们」注记）。**H1-2 价格：完全未取到**。
18. **H2 / H1-2 / R1 官方文档中心的逐关节力矩上限（N·m）表格**：H2/R1 文档只给 DoF 拆解、编号与角度限位，未给逐关节力矩；力矩只有模型文件版本（见 B6.3）。
19. **G1 各关节 link lengths 的官方命名长度**：官方模型只给关节 origin 偏置（B6.4），无 "thigh length = X" 的具名条目；营销页只给 "Calf + Thigh Length 0.6M"。
20. **`unitree_mjcf` / `unitree_motors_sdk` 仓库内容**：**两仓库 404，不存在**（本任务指令给的路径需更正为 `unitree_mujoco` / 文档中心 `Motor_IM6014 Development Guide`）。
21. **`www.unitree.com/motor/`**：**404**，正文在 `/go1/motor`（GO-M8010-6）与 `/IM6014/`（IM6014）、`/A1/motor`（A1）。

**明确「不要用」的常见二手口径**（本次全部官方来源均无出处）：
- G1 使用「IM6014」电机；G1 使用「Livox Mid-360 + RealSense D435i」的厂商全称组合写法（官方文档写作 **LIVOX-MID360** 与 **D435i**，非 "Intel RealSense"）。
- G1 EDU「标配 Jetson Orin NX 16GB」。
- H1 膝 360 N·m 出现在任何官方**模型文件**里（模型文件是 300；360 只出现在官方页面/文档中心的 "Ultimate Torque" 描述行）。

---

## E. 来源清单（全部 URL）

**官方页面（产品/商城）**
- https://www.unitree.com/go1/motor ｜ /IM6014/ ｜ /A1/motor ｜ /DigitalServo
- https://www.unitree.com/g1 ｜ /h1 ｜ /H2 ｜ /R1 ｜ /Dex3-1 ｜ /Dex5-1 ｜ /z1 ｜ /go1 ｜ /opensource
- https://shop.unitree.com/products/go1-motor ｜ /products/unitree-im6014-motor ｜ /products/unitree-z1
- https://shop.unitree.com/collections/all （商品名 + 价格列表页）
- https://shop.unitree.com/sitemap.xml ｜ /sitemap_products_1.xml?from=7531883266281&to=9417046032617

**官方文档中心（support.unitree.com 的后端，正文 Markdown）**
- 目录 API：`https://robot-api.unitree.com/doc/spaces2?locale=en`；`https://robot-api.unitree.com/doc/?space=<Space>&locale=en`
- IM6014（Space `Motor_IM6014 Development Guide`，注意 space 名含空格）：
  https://doc-cdn.unitree.com/30/1371/en/30_1371_en （About）· `30/1375` （Overview）· `30/1367`（Line connection）· `30/1381`（Quick Start）· **`30/1382`（Control Mode）**· `30/1378`（Motor configuration）· **`30/1383`（Motor Protocol）**· **`30/1377`（STM32 Example）**
- M8010（Space `Motor_SDK_Dev_Guide`）：**`8/1484`（About M8010）**· `8/100`（Overview）· `8/102`（Line connection）· `8/156`（Get SDK）· `8/159`（Quick Start）· `8/106`（Control Mode）· **`8/107`（Communication Protocol）**· `8/105`（C++）· `8/157`（Python）· `8/785`（STM32）· `8/103`（FW/ID）· `8/158`（Debug Assistant）· `8/162`（FAQ）· `8/1483`（Download）
- G1（Space `G1_developer`）：**`11/223`（About G1）**· `11/248`（Basic Motion Routine）· `11/249`（Joint Motor Sequence）· `11/252`（DDS Services Interface）· `11/266`（LiDAR Routine）· `11/267`（Depth Camera Routine）· `11/251`（Dex3-1）· `11/243`（RL Control Routine）· `11/247`（Arm Control）· `11/241`（Debugging Spec）· `11/308`（Common Mistakes）
- H1（Space `H1_developer`）：**`10/166`（About H1）**· **`10/271`（About H1-2）**· `10/175`（DDS）· `10/181`（Joint Motor Sequence）
- H2（Space `H2_developer`）：**`25/1061`（About H2）**· `25/1132`（Basic Services）· `25/1123`（DDS）· `25/1117`（Joint Motor Sequence）
- R1（Space `R1_developer`）：**`27/1135`（About R1）**· `27/1144`（Quick Start）· R1 `basic_motion_routine` / `basic_services_interface`

**官方仓库文件（raw.githubusercontent.com）**
- `unitree_mujoco/main/unitree_robots/`：`g1/g1_29dof.xml` · `g1/g1_23dof.xml` · `h1/h1.xml` · `h1_2/h1_2_handless.xml` · `h2/h2_mujoco.xml` · `r1/R1_C++.xml`
- `unitree_ros/master/robots/`：`g1_description/g1_29dof_rev_1_0.urdf` · `g1_description/g1_29dof_with_hand.urdf` · `g1_description/g1_23dof_rev_1_0.urdf` · `h1_2_description/h1_2_handless.urdf` · `h2_description/H2.urdf` · `r1_description/R1.urdf`
- `unitree_sdk2/main/include/unitree/idl/hg/`：`LowCmd_.hpp` · `LowState_.hpp` · `MotorCmd_.hpp` · `MotorState_.hpp` · `IMUState_.hpp` · `HandCmd_.hpp` · `HandState_.hpp` · `BmsCmd_.hpp` · `BmsState_.hpp` · `PressSensorState_.hpp`
- `unitree_sdk2/main/example/g1/low_level/g1_ankle_swing_example.cpp` · `g1_dual_arm_example.cpp` · `example/g1/g1d/g1d_arm_example.cpp`
- `unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/`：`LowCmd.msg` · `LowState.msg` · `MotorCmd.msg` · `MotorState.msg`
- `unitree_rl_lab/main/source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py` · `tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py` · `deploy/robots/g1_29dof/config/config.yaml` · `deploy/robots/g1_23dof/config/config.yaml`
- `unitree_rl_gym/master/README.md` · `legged_gym/envs/g1/g1_config.py` · `legged_gym/envs/base/legged_robot_config.py` · `deploy/deploy_real/configs/g1.yaml` · `deploy/deploy_mujoco/configs/g1.yaml`
- `unitree_model/main/`（仅 USD/DAE，无 XML）
