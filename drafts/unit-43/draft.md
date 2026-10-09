# 附录 C：器件与人形参数表

> 本附录把全书引用过的参数集中在一处，便于查。**每一格都带来源标记**；空白格表示官方未公布（[未]），本书不填。
> **C.4a（关节 MCU 选型表）与 C.5 逐格回到原厂页面核对，抓取日期 2026-10-08**；核到但易腐的数（单价、库存、NRND 状态）另标 [查] 并写明日期，核不到的格子写“未核到”。

## C.1 人形与类人形整机

| 项 | H1 | H1-2 | G1 | G1 EDU | R1 | H2 |
|---|---|---|---|---|---|---|
| 身高 | 约 1.8 m | — | 1.32 m | 1.32 m | — | 1.82 m |
| 体重 | 约 47 kg | — | 35 kg | 35 kg | — | 70 kg |
| 自由度构成 | 腿 5×2 + 臂 4×2 + 腰 1 | 腿 12 + 臂 14 + 腰 1 | 腿 6×2 + 腰 1 + 臂 5×2 | 同 + 腰可 +2 + 手 7 + 腕 2 | 腿 12 + 臂 10 + 腰 2 + 头 2 | 腿 12 + 臂 14 + 腰 3 + 头 2 |
| 膝峰值扭矩 | 360 [厂] / 300 [厂模型] | 360 | 90 | 120 [厂] / 139 [厂模型] | 60（URDF） | 360 |
| 髋峰值扭矩 | 220 / 200（模型） | 220 | 139 或 88（两 URDF 冲突） | 同 | 60（URDF） | 360 |
| 踝峰值扭矩 | 59 / 40（模型） | 75×2 | 35 / 50 / 25（多口径） | 同 | 33 / 50 | 66.88（模型） |
| 腰峰值扭矩 | — | 220 | — | +2 自由度档 | 60 | 180 |
| 臂/肩峰值扭矩 | 75 | 肩肘 120 / 腕 30 | 25（N5020-16） | 同 | — | 120；肩俯仰 130（模型） |
| 官方扭矩密度口径 | 189 N·m/kg（峰值） | — | — | — | — | — |
| 电池 | 15 Ah / 0.864 kWh / 最大 67.2 V（⇒ 16 串，[算]） | — | 13 串 / 9000 mAh / 充 54 V 5 A | 同 | 未公布 | 15 Ah / 0.972 kWh / 75.6 V（⇒ 18 串，[算]） |
| 续航 | **未公布小时数**（`Endurance` 行填的是 864Wh） | — | 约 2 h | 约 2 h | **约 1 h** | **未公布小时数** |
| 反推平均功率 | **不给**（除数读不到） | — | ≈216 W | ≈216 W | — | **不给**（除数读不到） |
| 反推功率密度 | **不给** | — | ≈6.2 W/kg | ≈6.2 W/kg | — | **不给** |
| 感知 | 3D 雷达 + 深度相机 | 同 | 深度相机 + 3D 雷达 + 4 麦 + 5 W 扬声器 | 同 | 双目（R1）/ 单目（R1 AIR） | 大 FOV 仿人双目（基线 60 mm、12/10 bit RAW、F2.0、焦距 1.53/2.67 mm、−20~+60 ℃） |
| 计算 | Intel i5（平台）+ i7（开发）；可选 i7 或 Orin NX，最多 3 块 | — | “多品牌可选，例如 Orin” | 文档中心 PC2：Jetson Orin NX / 16G / 8×A78AE / 1024 Ampere + 32 TC / 918 MHz | — | 可选 Jetson Thor（T5000，2070 TFLOPS FP4-Sparse）或 Orin NX 16G（100 TOPS） |
| 关节总线 | RS-485（官方对全系电机口径） | 同 | 同 | 同 | 同 | 同 |
| 参考价 | 店铺现标 $90,000（注“联系实价”） | 未公布 | ¥8.5 万起 / $13,500 | ¥16.9–30.9 万 | ¥9,900 起 / $4,900 | ¥19.9 万含税 / $29,900 |
| IP 防护 | [未] | [未] | [未] | [未] | [未] | [未] |
| 额定（持续）扭矩 | **[未]（全系无一公布）** | | | | | |

## C.2 一体化关节与微型执行器

| 型号 | 峰值扭矩 | 减速比 | 供电 | 编码器 | 总线 / 帧长 / CRC | 质量 | 尺寸 | 价格 |
|---|---|---|---|---|---|---|---|---|
| GO-M8010-6 | 23.7 N·m（40 A） | 1:6.33 | 12–30 V（推荐 24 V） | 单圈绝对值 15 bit | RS-485 4 Mbps；17 B 下 / 16 B 上；CRC16_CCITT；ID 0–14 + 15 广播 | 530 g | 96.5×92.5×42.3 mm | **$369** |
| IM6014（N6014B-12.6） | 34.4（反）/ 31.7（同）N·m | 3:38 = 12.667 | 24–75 V | **双**绝对值 15 bit | RS-485 6/4 Mbps；20 B 下（0xFE 0xEE）/ 26 B 上（0xFC 0xEE）；CRC32-MPEG2 | 535 g | φ65×60 mm | 店铺标价存疑 |
| F-1515-108 | 0.76 N·m（理想值） | 1:108 | [未] | [未] | [未] | 45 g | 34.8×23.1×23.3 mm | [未] |
| F-1515-214 | 1.498 N·m（理想值） | 1:214 | [未] | [未] | [未] | 45 g | 同上 | [未] |
| SV1-25 / J288 数字舵机 | 1.5 N·m | 288.35:1 | [未] | [未] | 私有串口协议 | 19.5–39 g | — | $15 起 / SV1-25 $229 |
| **G1 关节电机家族**（`unitree_rl_lab` 配置） | | | | | | | | |
| N7520-14.3 | 88 N·m（模型限幅） | 14.3 | [未] | [未] | 走整机 `rt/lowcmd` | [未] | φ75×20 级 | — |
| N7520-22.5 | 139 N·m | 22.5 | [未] | [未] | 同 | [未] | 同 | — |
| N5020-16 | 25 N·m | 16 | [未] | [未] | 同 | [未] | φ50×20 级 | — |
| N5020-16-parallel | 35 N·m（踝） | 16 | [未] | [未] | 同 | [未] | 同 | — |
| W4010-25 | 5 N·m | 25 | [未] | [未] | 同 | [未] | φ40×10 级 | — |
| M107（H1/H1-2） | 膝 360 / 髋 220 / 踝 59 | [未] | [未] | [未] | [未] | 反推 ≈1.9 kg/单元（用官方 189 N·m/kg） | [未] | — |

**指令量化（一手）**

```
M8010 ：位置 int32，raw = (θ/2π)×32768（q15）；kp、kd int16，raw = (k/25.6)×32768
        允许范围 0.0 ≤ kp, kd ≤ 25.599
IM6014：转矩 int16，2560 = 1 N·m（绝对上限 2¹⁵/2560 = 12.8 N·m 转子侧）
        位置 int32，32768/2π = 1 rad；k_pos int16，12800 = 1 N·m/(rad/s)
        输出侧范围：outputTor −162.133~162.128 N·m；Kp 0~410.725；Kd 0~102.681
多字节一律小端
```



## C.2a 官方电机模型参数（取自 `unitree_rl_lab/source/.../assets/robots/unitree_actuators.py`，[厂]）

**这一张表是本书唯一一处能拿到「宇树关节的摩擦与惯量」的地方——它不在产品页上，在训练仓库里。**

模型：`UnitreeActuator`（继承 `DelayedPDActuator`），带摩擦、延迟与 T-N 曲线限力。

```
τ_friction = Fs · tanh(q̇ / Va) + Fd · q̇        Va 默认 0.01 rad/s
armature   = J2 + J1·i2² + Jr·(i1·i2)²           折算到关节（输出）轴的等效惯量
限力按 X1 / X2 分段；X1 = Maximum Speed at Full Torque（T-N 曲线折点），rad/s
```

| 型号 | X1 | X2 | Y1 同向峰值 | Y2 反向峰值 | Fs | Fd | armature (kg·m²) |
|---|---|---|---|---|---|---|---|
| M107_15 | 14.0 | 25.6 | 150.0 | 182.8 | 0 | 0 | 0.063259741 |
| M107_24 | 8.8 | 16 | 240 | 292.5 | 0 | 0 | 0.160478022 |
| Go2HV | 13.5 | 30 | 20.2 | 23.4 | 0 | 0 | — |
| **N7520-14.3** | 22.63 | 35.52 | **71** | **83.3** | 1.6 | 0.16 | 0.01017752 |
| **N7520-22.5** | 14.5 | 22.7 | **111.0** | **131.0** | 2.4 | 0.24 | 0.025101925 |
| N5010-16 | 27.0 | 41.5 | 9.5 | 17.0 | 0 | 0 | 0.0021812 |
| **N5020-16** | 30.86 | 40.13 | **24.8** | **31.9** | 0.6 | 0.06 | 0.003609725 |
| **W4010-25** | 15.3 | 24.76 | **4.8** | **8.6** | 0.6 | 0.06 | 0.00425 |

**齿轮级惯量（源码 docstring 原文，单位 kg·m²）**

```
N7520-14.3  rotor 0.489e-4 / gear_1 0.098e-4 ratio 4.5 / gear_2 0.533e-4 ratio 48/22+1
N7520-22.5  rotor 0.489e-4 / gear_1 0.109e-4 ratio 4.5 / gear_2 0.738e-4 ratio 5.0
N5020-16    rotor 0.139e-4 / gear_1 0.017e-4 ratio 46/18+1 / gear_2 0.169e-4 ratio 56/16+1
W4010-25    rotor 0.068e-4 / gear_1 ratio 5 / gear_2 ratio 5
N5010-16    rotor 0.084e-4 / gear_1 0.015e-4 ratio 4 / gear_2 0.068e-4 ratio 4
```

**把上面那行齿轮级惯量代进 armature 的式子，口径这件事就自己站住了**（N7520-22.5：J2 = gear_2 = 0.738e-4，J1 = gear_1 = 0.109e-4 且 i2 = 5.0，Jr = rotor = 0.489e-4 且 i1·i2 = 4.5 × 5.0 = 22.5）[算]：

```
armature = 0.738e-4 + 0.109e-4 × 5.0² + 0.489e-4 × (4.5 × 5.0)² = 0.0251019 kg·m²
```

**逐项是 0.0000738 + 0.002725 + 0.02476，和 0.0251019——对上官方那个 0.025101925，八位有效数字里只差最后一位。** 换句话说，这个 armature 就是**把三级惯量全部搬到输出轴上**加出来的数（转子那一项被乘大了 506 倍，是它的主导项）。反过来把 0.025102 除以 22.5 的平方（= 506.25）折回电机轴，得 4.96 × 10⁻⁵ kg·m²，比 rotor 单独的 4.89 × 10⁻⁵ 只多出两级齿轮折算下来的 0.07 × 10⁻⁵——**同一批数，两种读法各自闭合，而只有“输出轴”这一读法与式子的写法一致** [算]。

**口径读错会怎样：`code/tools/foc_check.py` 的 `armature_side_check()` 的四行输出（2026-10-08 跑，PASS）** [算]

```
N7520_14p3: 速比 14.3、kp 40.179、armature 0.010178 ⇒ 按关节侧 10.00 Hz；若按电机侧 143 Hz
N7520_22p5: 速比 22.5、kp 99.098、armature 0.025102 ⇒ 按关节侧 10.00 Hz；若按电机侧 225 Hz
N5020_16:   速比 16、kp 14.251、armature 0.003610 ⇒ 按关节侧 10.00 Hz；若按电机侧 160 Hz
W4010_25:   速比 25、kp 16.778、armature 0.004250 ⇒ 按关节侧 10.00 Hz；若按电机侧 250 Hz
```

同一个 kp、同一个 armature，两种读法差整整一个速比倍（√(i²) = i）。**四档里只有“按关节侧”这一列全部落在 10.00 Hz，而官方 mimic 配置的注释写的就是 10 Hz 固有频率**；按电机侧读给出 143 / 225 / 160 / 250 Hz，与官方那句注释差一到两个数量级。**所以只有按关节（输出）侧读才对得上官方那句 10 Hz。** 本书第一版在这里把它标成“折算到电机轴”——**式子照抄无误、标注写反**，而一句标注会把第 18 章整条 ω_n 推导读反方向，因此这条检查已被固化进脚本（脚本注释同步改正），本表按关节侧读。

**读这张表的四个要点**（本书正文用到处均已标注）：

一，**N7520 两档的 rotor 惯量相同（0.489e-4 kg·m²），齿轮第二级速比不同（48/22+1 ≈ 3.18 对 5.0）**——这正是第 14 章「同一颗电机、两个齿轮」那条发现的下半部分证据。

二，**M107 系列的 Fs/Fd 都是 0**，即官方仿真里 H1/H1-2 的关节**不建模摩擦**；而 G1 用的 N7520/N5020/W4010 都有非零 Fs/Fd。**这解释了两台机器在 sim2real 上的不同难度：G1 的摩擦被建模了，H1 的没有。**

三，**Y1 与 Y2 不同（同向与反向峰值）**，例如 N7520-22.5 是 111.0 与 131.0——**官方承认电机正反转的扭矩上限不对称**。而产品页只给一个“峰值扭矩”。第 08 章那条“角点值不可当工作点”在这里有了第二个层次：**连正反向都不是同一个数。**

四，**armature 就是第 18 章里那个 J**（折算到**关节/输出轴**，不是电机轴——式子里 Jr 乘的是
(i1·i2)²，已经把减速比算进去了）。**因为它本来就是输出侧口径，所以第 18 章那道 ω_n = √(kp/J)
可以直接代，不必再乘或再除速比**；口径别搞错，搞错会把第 18 章整条推导读反：
`code/tools/foc_check.py` 的 `armature_side_check()` 就是钉这件事的——
同一个 kp 按关节侧读是 10.00 Hz（对上官方注释），按电机侧读是 225 Hz（差整整一个速比，四行的机器证明见本节上面）。有了它，本章那道“ω_n = √(kp/J)”的天花板**第一次可以用官方数算**：以 N7520-22.5 为例，mimic 配置给的 Kp = 99.098、armature = 0.025101925，则

```
ω_n = √(99.098 / 0.025101925) = 62.8 rad/s ⇒ 62.8 ÷ 2π = 10.00 Hz
```

**正好等于官方 mimic 配置注释里的“10 Hz 固有频率”** [算][厂]。也就是说：**宇树自己就是用第 18 章那条式子反推 kp 的。** 这条验证是本书第 1 部与第 2 部之间最干净的一次闭环。

## C.2b 关节里那颗 MCU：选型表与“为什么要 FPU”

第 27 章说关节层是“MCU + FOC + 现场总线”，这一张表给的就是那句话的器件落点。
**每一格都标了出处；核不到的格子写“未核到”，不猜。**

| 型号 | 内核 / 主频 | 硬件 FPU | 高分辨率定时器 | CORDIC / FMAC | ADC 与 PWM 硬件联动 | CAN-FD | 本书为什么列它 |
|---|---|---|---|---|---|---|---|
| **STM32F413RGT6** | Cortex-M4F，主频 未核到 | 有（M4F 带 FPU） | 未核到 | 未核到 | 未核到 | 未核到 | **宇树官方 IM6014 通信示例所用型号** [厂] |
| STM32G4 系列（G431 / G474 两档） | Cortex-M4，两页都写 “up to 170 MHz”、“213 DMIPS” | 单精度（G474 页原文 “single-precision floating-point unit (FPU)”） | **G431 页 0 次 HRTIM；G474 页原文 “HRTIM … 184 ps resolution, 12 PWM”** | 两档都有（页原文 “(CORDIC … and FMAC unit for filter functions)”） | 系列页有 “A flexible interconnect matrix allows autonomous communication between peripherals and saves CPU resources.”（逐路触发路径只在其互连矩阵表里，本轮未取到 → 见 C.4a） | **G431 1× FDCAN、G474 3× FDCAN**（参数表 CAN (FD) = 1 / 3） | 开源参照实现 moteus 用的就是 STM32G4；**逐格与 URL 见下面 C.4a** |
| **GD32F50MxxG** | Cortex-M33，最高 252 MHz [拆] | 未核到 | 报道称官方称“1 路 32 位高精度定时器” [拆] | 未核到 | 报道称 3 路 12 位 ADC、12 通道并行 [拆] | 报道称**标配 2 路 CAN-FD** [拆] | 国产电机专用料，报道称官方明写面向“人形机器人、协作机械臂、灵巧手” [拆] |
| **GD32M531 系列** | Cortex-M33 / 180 MHz（官方选型表） | 未核到（本轮抓到的官方页段落无 FPU 字样） | 选型表无 HRTM 行；“Advanced TM (16bit) 2” | 无 CORDIC/FMAC；有 “TMU 1” 与“空间矢量PWM硬件加速器” | 官方页只给 ADC/DAC/比较器集成这句 → 触发绑定未核到 | **1× CAN 2.0B，无 FD** | 电机专用料，官方把“机器人关节”列为应用场景；**逐格见 C.4a** |
| **AT32M416 / M412** | 页原文 “ARM® Cortex®-M4主频最高180MHz” | “内建单精度浮点运算单元(FPU)与数字信号处理器(DSP)” | 无 HRTIM / 无移相字样；“1个16位8通道高级定时器…带死区控制和紧急双向剎车功能” | 页面无 → 未核到 | 页面无 → 未核到 | **M416 “1 x CAN-FD”；M412 “1个CAN”（无 FD 字样）** | 国产电机专用料的另一家；**逐格与 URL 见 C.4a** |

出处：宇树官方文档 `STM32 HAL Communication Example`（doc-cdn `30/1377`，抓取 2026-10-08）；
兆易创新 GD32F50MxxG 发布报道（电子发烧友，2026-08-05，二手转述官方稿）——**这一行的口径是二手转述，本书标 [行] 不升 [厂]**。
ST 官网的 G431 / G474 / H743 / H723 / F405 / F767 六个产品页、兆易创新的 GD32M531 官方选型表与发布页、
雅特力的 AT32M416 / AT32M412 产品页，**本轮（2026-10-08）都已回读核到**，逐格出处见 C.4a 的来源列。
（本书第一版这一节里写的“ST 官网 G474 产品页抓取超时所以留空”已经不成立，已按核到的原文填上。）

**那颗“建议带 FPU”值多少钱？** 官方示例原文是：
IM6014 的 STM32 例程基于 STM32F413RGT6，“如果移植到其他 MCU 型号，建议使用带 FPU 的 MCU” [厂]。
这句话不是客套，是一道可以在纸上算完的账。FOC 每个控制周期要做的事是固定的：
两次 Clarke/Park 正逆变换（每次含正弦、余弦与两三次乘法）加两路 PI，
粗算 **约 30 次浮点乘加**。按本书假设（假设，不是厂商数据）：

```
软浮点一次乘加 ≈ 100 个时钟周期；170 MHz ⇒ 100 ÷ 1.7e8 ≈ 0.59 µs
30 次 ⇒ 约 17.7 µs，占 10 kHz 环（100 µs）预算的 17.7%
带 FPU 一次乘加 ≈ 流水线 4–6 个周期 ⇒ 30 × 5 ÷ 1.7e8 ≈ 0.9 µs，占比约 0.9%
```

**换句话说：没有 FPU，光是“把电流旋到正确的坐标系里”这一件事，就要吃掉你近两成的控制预算。**
再叠上第 13 章那条死区与采样窗、第 27 章那条 250 ns 位时间，就不难理解为什么
“能跑 FOC 的 MCU”和“能跑点灯的 MCU”在选型上是两个世界。
（17.7% 与 0.9% 是本书按上述假设的推算 [算]，不是任何厂商的实测数据；
换主频或换浮点库，两个数都会变，变的是量级不是结论。
算法本身：100 ÷ 1.7e8 = 0.588e-6 s = 0.588 µs；0.588 µs × 30 = 17.65 µs；17.65 ÷ 100 = 17.7%。
带 FPU 取 5 个周期：5 ÷ 1.7e8 = 0.0294 µs；× 30 = 0.88 µs；0.88 ÷ 100 = 0.88%。）

**这张表怎么读**：先看 FPU 那一列，再看“ADC 与 PWM 硬件联动”——
第 13 章讲过采样时刻错开一个死区就会引入 48 mV 量级的电压误差，
所以真正决定电流环质量的不是主频，而是**ADC 触发能不能由 PWM 计数器硬件发出**，
让采样点稳定落在 PWM 周期的中点，而不是靠软件在 ISR 里“大概什么时候读一下”。
CAN-FD 那一列对应第 27 章：宇树官方明确目前生产的电机走 RS-485，
而行业里 5 Mbps CAN-FD 是另一条路线（moteus），两者的位时间差一个数量级。


## C.3 灵巧手与机械臂

| 型号 | 自由度 | 触觉 | 传动 / 电机 | 总线 | 价格 |
|---|---|---|---|---|---|
| Dex1-1 | [未] | 可选相机版 | 5 N·m / 1:25 电机 | [未] | [未] |
| Dex2-5 | [未] | — | [未] | [未] | [未] |
| Dex3-1 | 主动：拇 3 / 食 2 / 中 2 | **9 阵列 / 33 压力传感器**，量程 10–2500 g，不损坏最大承受 20 kg | F-1515 系列（近端齿轮） | [未] | [未] |
| Dex5-1 / 1P | [未] | **94 个触觉点**（需再核） | **空心杯电机** | [未] | [未] |
| Dex5-S | 22 DOF | — | — | — | 3.99 万元起（媒体口径） |
| Z1 AIR / PRO | 6 DoF 臂 | — | **谐波减速器，减速比 60+，背隙 ≈6 弧分** | RS-485 | $15,999 |
| Z1 关节电机 | — | — | 峰值 33 N·m，15 bit 编码器，力控精度 ≈0.2 N·m，控制频率 1 kHz，φ65×52 mm，405 g，24 V 推荐 | 同 | 含在整机 |
| R1-7a | 7 轴 | — | IM6014（J3–J5） | [未] | ¥9,900 起 / 店铺 $750 起 |

**Z1 官方脚注（原文，本书第 14 章的支点）**

> Since the reduction ratio used by each joint is relatively low, the position control stiffness of the whole machine is low. If the control mode is not optimized, there will be large position control error and shaking when the manipulator moves.

## C.4 感知与算力（可买到的器件）

| 器件 | 关键参数 | 价格 |
|---|---|---|
| 宇树 L1 | 360°×90°，20 m@90% / 10 m@10%，±2.0 cm，21,600 点/s，11/180 Hz，盲区 0.05 m | **¥999 / $249** |
| 宇树 L2 | 360°×96°，30 m@90% / 15 m@10%，≤2.0 cm，64,000 点/s，内置 6 轴 IMU（采样率官方未公布 [未]），4.5 mm 分辨率，100 Klux，Class 1 | **¥1,799 / $419** |
| Livox Mid-360 | 360°×59°，40 m@10%，265 g，IP67 | ¥3,999 |
| RealSense D435i | 87°×58°@90 fps + IMU | $334 |
| Orbbec Gemini 335 | 0.26–3 m | $304 |
| Jetson Orin NX 16 GB | 1024 CUDA / 32 TC / 8×A78AE，100 TOPS | ¥5,499（模组） |
| Jetson AGX Thor DevKit | T5000：2070 TFLOPS(FP4)、128 GB、14×Neoverse-V3AE、40–130 W、**模组自带 4×CAN** | $3,499 → $5,499 |
| 地瓜 RDK S100 | 80 TOPS BPU + 6×A78AE + **4×Cortex-R52 实时核**、板载 CAN/CAN-FD | ¥2,499（预售） |
| 地瓜 RDK X5 | 10 TOPS、板载 1×CAN-FD、PoE、Wi-Fi6 | ¥549（4G）/ ¥699（8G） |
| STM32G431CBT6 | 170 MHz M4 + CORDIC/FMAC（**无 HRTIM**，见 C.4a 的更正） | ¥21.96 |
| 纳芯微 NSi6602B | 隔离半桥 4 A / 6 A 峰值 | ¥7.61 |
| 麦歌恩 MT6816CT | 14-bit SPI 磁编码器，25,000 rpm | 无公开挂牌价 |
| Microchip LAN9252TI | EtherCAT 从站控制器（SPI 接口 ESC） | ¥87.42 |
| 达妙 DM-J8009-2EC | 额定 20 / 峰值 40 N·m，双编码器，CAN/CAN-FD | ¥1,475–2,398 |
| 小米 CyberGear 微电机 | 关节级无刷微电机 + 驱动器一体，市面另一条“买得到”的路线；**官方参数与价格本轮未取到可回读页面** [未] | 未核到 |
| 因时 RH56DFX | 6 DoF / 12 关节，6 力传感，0.5 N 分辨率，RS-485 | ¥22,200 |
| 灵心巧手 L20 / O6 | 21 DoF 腱绳 / 6 DoF | ¥4.99 万 / ¥6,666（Lite ¥3,999） |
| 六维力（坤维 / 蓝点 / 宇立） | 国产已降至约 ¥5,000/台 量级 | 询价 |
| 帕西尼触觉阵列 | 单价从十万级降至 ¥199 起 | ¥199 |

**C.4 这一张表的标记约定**（本章开头承诺“每一格都带来源标记”，这张表按来源分组集中标，逐行标会挤爆版面）：

- 宇树 L1 / L2 与 Thor T5000、RDK 的参数与价格：**[厂]**，取自各自官方页面，抓取日期 2026-10-07/08；
- 因时 RH56DFX（¥22,200）、灵心巧手、帕西尼、坤维/蓝点/宇立六维力、达妙、麦歌恩、纳芯微、STM32G431、LAN9252 这些**第三方器件**：参数与挂牌价来自**厂商自己的页面或经销报价**，本书按 [查] 记（他方一手可回读，不是宇树官方），抓取日期 2026-10-08；
- Livox Mid-360 的 ¥3,999 取自已 404 的旧页面，**本书标 [推] 并列为待复验**，不要当现行报价引用；
- 小米 CyberGear 本轮**没有取到可回读的官方参数页**，写 [未]，价格一格留“未核到”。

C.4a（关节 MCU 选型表）与 C.5 是**逐格回原厂核对**的，标记写在格内。

## C.4a 关节 MCU 选型表（本书逐格回原厂核对）

> **这张表存在的理由**：第 13 章说过“为什么是 G4 这一档”，那句话原来只挂在三个外设名字上。下面把它变成一次可对照的判断——**每格只填原厂页面上写着的字，核不到的格子留空并写“未核到”**。本轮（2026-10-08）逐行回读的来源是各家**产品页 / 官方选型表 / 官方发布页**；ST 的数据手册 PDF 本轮取不到可解析的原文，所以凡是只有手册里才有的表格行（例如互连矩阵的每一条触发路径）一律写“未核到”，不假引。单价例外，来自分销商页面，另标 [查] 并写抓取日期。
>
> **口径先说死**：宇树关节板用的是哪颗 MCU，官方从未公布 [未]。**这张表不是“宇树的选型”，是“你要替它选型时的对照表”。**

| 型号 | 内核 / 最高主频 | FPU | 高分辨率定时器（没有它 = 软件移相的代价） | CORDIC / FMAC | ADC 触发能否硬件绑定 PWM | CAN / CAN-FD 外设个数 | 封装 / 单价 | 来源（抓取 2026-10-08） |
|---|---|---|---|---|---|---|---|---|
| **STM32G431CBT6** | Cortex-M4 / 170 MHz（页原文 “with 213 DMIPS”） | 页原文 “Arm 32-bit Cortex-M4 CPU with FPU”（单精度由 M4 架构定义） | **无 HRTIM**：产品页全文 0 次 “HRTIM”。定时器清单页原文 “14 timers”，含 “2 x 16-bit 8-channel advanced motor control timers”、“2 x 16-bit timers with up to four IC/OC/PWM”、“1 x 16-bit timer with 2 x IC/OCs”、“2 x 16-bit timers with IC/OC/OCN/PWM”、“2 x 16-bit basic timers”、“1 x 32-bit + 2 x 16-bit”、“1 x low-power timer” | **两者都有**（页原文 “The devices embed peripherals allowing mathematical/arithmetic function acceleration (CORDIC for trigonometric functions … and FMAC unit for filter functions)”） | 系列页原文有一句 **“A flexible interconnect matrix allows autonomous communication between peripherals and saves CPU resources.”**；但“哪一路 TIM 触发哪一路 ADC”那一行只存在于数据手册的 interconnection matrix 表里，**本轮未取到该表原文 → 该行未核到** | **1× FDCAN**（页原文 “One FDCAN” / “1 x FDCAN controller supporting flexible data rate”；参数表 CAN (FD) = 1、CAN (2.0) = “-”) | ST 页 “9 packages from 32-pin to 100-pin”，Budgetary Price 栏为 “-” ⇒ **官方价未核到**；分销商：立创商城 item 549633 = ¥21.96（商品编号 C529355，2026-10-08）[查] | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32g431cb.html 与系列页 …/stm32g4-series.html [查] |
| **STM32G474RET6** | Cortex-M4 / 170 MHz（页原文 “213 DMIPS”） | 页原文 “features a single-precision floating-point unit (FPU)” | **有 HRTIM**：产品页原文 **“HRTIM (Hi-Resolution and complex waveform builder): 6 x16-bit counters, 184 ps resolution, 12 PWM”**，Description 段又写 “high resolution timer with 184 ps resolution”；另有 “3 x 16-bit 8-channel advanced motor control timers” | 两者都有（页原文 “(CORDIC for trigonometric functions and FMAC unit for filter functions).”） | 同一句系列页互连矩阵原文适用；ADC 侧页原文给 “5 x 12-bit ADCs 0.25 µs, up to 42 channels. Resolution up to 16-bit with hardware oversampling, 0 to 3.6 V conversion range”。**HRTIM→ADC 那一行触发路径：本轮未取到手册表原文 → 未核到** | **3× FDCAN**（页原文 “3 x FDCAN controller supporting flexible data rate”；参数表 CAN (FD) = 3、CAN (2.0) = “-”） | ST 页 “9 packages from 48-pin to 128-pin”、状态 “Active”；分销商：立创商城 item 538858 = ¥62.4、封装 LQFP-64(10×10)、编号 C521608（2026-10-08）[查] | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html [查] |
| **STM32H743AII6** | Cortex-M7 / 480 MHz（页原文 “1027 DMIPS”） | **双精度**（页原文 “supports Arm double-precision (IEEE 754 compliant) and single-precision”） | **无 “HRTIM” 字样**，但页上明列一句 **“1× high-resolution timer (2.1 ns max resolution)”**（同页还有 “2× 16-bit advanced motor control timers”、“10× 16-bit general-purpose”、“5× 16-bit low-power”、“2× 32-bit”）⇒ **2.1 ns 对 184 ps 差 11.4 倍**，这就是 H7 这一档做移相时要付的步进 | 无（页上 0 次 CORDIC / FMAC） | 页未给触发路径表 → **未核到** | **2× CAN，都带 FD，其中 1 路 TT-CAN**（页原文 “2× CAN controllers: 2 with CAN FD, 1 with time-triggered CAN (TT-CAN)”） | 页给 “UFBGA 169 7x7x0.6 P 0.5 mm”；Budgetary Price “-” ⇒ 单价 **未核到** | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32h743ai.html [查] |
| **STM32H723ZGT6** | Cortex-M7 / 550 MHz（页未列 DMIPS ⇒ 未核到） | 双精度（页原文 “supports Arm double-precision (IEEE 754 compliant) and single-precision”） | **无 HRTIM、也无 “high-resolution timer” 字样**（0 次）；定时器是 “Seventeen 16-bit (including 5 x low power 16-bit timer available in stop mode) and four 32-bit timers” | **两者都有**——H7 里只有 72x/73x 这一档把 G4 的数学加速器搬上来了（页原文 “(CORDIC coprocessor for trigonometric functions and FMAC unit for filter functions).”） | 页未给触发路径表 → **未核到** | **3× CAN-FD**（特性行页原文 “1× FD/TTCAN and 2x FDCANs”；参数表 CAN (FD) = 3、CAN (2.0) = “-”） | 页给 “UFBGA 144 7x7x0.6 P 0.5 mm” 与 “LQFP 144 20x20x1.4 mm”；Budgetary Price “-” ⇒ 单价 **未核到** | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32h723zg.html [查] |
| **STM32F405RGT6** | Cortex-M4 / 168 MHz（页原文 “210 DMIPS/1.25 DMIPS/MHz”） | 单精度（页原文 “The Cortex-M4 core features a floating-point unit (FPU) single precision”） | **无 HRTIM**（0 次）；页原文 “twelve general-purpose 16-bit timers including two PWM timers for motor control, two general-purpose 32-bit timers” | **都没有**（0 次） | 页未给触发路径表 → **未核到** | **2× CAN 2.0，无 FD**（页原文 “Up to 2 × CAN interfaces (2.0B Active)”；参数表 CAN (2.0) = 2、CAN (FD) = “-”）—— 附录 D 里 ODrive v3.x 用的就是这颗，官方口径 CAN 2.0b 1 Mbps、无 FD [查] | 页给 “LQFP 64 10x10x1.4 mm”；单价 **未核到** | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32f405rg.html [查] |
| **STM32F767BIT6** | Cortex-M7 / 216 MHz（页原文 “462 DMIPS/2.14 DMIPS/MHz”） | 双精度（页原文 “features a floating point unit (FPU), which supports Arm double-precision and single-precision”） | **无 HRTIM**（0 次）；页原文 “Up to 18 timers: up to thirteen 16-bit (1x low-power 16-bit timer available in Stop mode) and two 32-bit timers” | 都没有（0 次） | 页未给触发路径表 → **未核到** | **3× CAN 2.0，无 FD**（页原文 “3 × CANs (2.0B Active)”；参数表 CAN (2.0) = 3、CAN (FD) = “-”） | 页给 “LQFP 208 28x28x1.4 mm”；**该页状态栏 “NRND — Not recommended for New Design”**；Budgetary Price “-” ⇒ 单价 **未核到** | ST 产品页 https://www.st.com/en/microcontrollers-microprocessors/stm32f767bi.html [查] |
| **GD32M531RBT7**（电机专用） | Cortex-M33 / 180 MHz（官方选型表 “Core Cortex®-M33”、“Max Speed (MHz) 180”；官方发布页 “Coremark®跑分达705、DMIPS达267”） | **未核到**：本轮抓到的官方选型表与发布页段落都没有 FPU 字样（要定性须查数据手册） | **官方选型表里没有 HRTM 这一行**；定时器三行是 “Advanced TM (16bit) 2”、“GPTM (16bit) 4”、“CPTM (16bit) 3”；发布页口径是 **“GD32M531定位双电机控制”**，并把“机器人关节”列为应用场景 | 无 CORDIC/FMAC 字样；**替代物是选型表的 “TMU 1” 与发布页的“内置三角函数运算及空间矢量PWM硬件加速器”** | 选型表给 “12bit ADC Units (CHs) 2(16)”，发布页给“集成高速、高精度ADC、DAC、模拟比较器等电机专属模块”；**至于 ADC 触发能否由定时器硬件发出（含“硬件移相”那一层），本轮在官方页未取到原文 → 未核到** | **1× CAN 2.0B，无 FD**（选型表 “CAN 2.0B 1”，页上无 CAN-FD 行） | 选型表 “Package LQFP64”、“Flash 128K / RAM 32K”；发布页 “支持2.7V~5.5V宽电压供电，工作温度覆盖-40℃~105℃”；单价 **未核到** | 兆易创新官方选型表 https://www.gigadevice.com.cn/product/mcu/mcus-product-selector/gd32m531rbt7 与官方发布页 …/about/news-and-event/media-coverage/gd32m531-motor-control-mcu-leader [查] |
| **AT32M416 系列**（电机专用；料号后缀按该页订购信息选） | 页原文 “ARM® Cortex®-M4主频最高180MHz” | 页原文 **“内建单精度浮点运算单元(FPU)与数字信号处理器(DSP)”** | **无 HRTIM、无移相字样**；页给 **“1个16位8通道高级定时器，可组成4对互补通道PWM输出，带死区控制和紧急双向剎车功能”** | 页上无 CORDIC/FMAC 字样 → **未核到** | 页未给 ADC 触发路径 → **未核到** | **1× CAN-FD**（页原文 “1 x CAN-FD”；同族 AT32M412 那一页给的是 “1个CAN”，无 CAN-FD 字样） | 页列 “LQFP48 7 x 7 mm / QFN48 6 x 6 mm / LQFP32 7 x 7 mm / QFN32 4 x 4 mm / TSSOP24 7.8 x 4.4 mm”；单价 **未核到** | 雅特力官方产品页 https://www.arterytek.com/cn/product/AT32M416.jsp 与 …/AT32M412.jsp [查] |

**这张表要先解决的一个错**：本书上一版在 C.4 里把 STM32G431CBT6 写成“CORDIC/FMAC/**HRTIM**”。本轮回读 ST 产品页：stm32g431cb.html 全文 `HRTIM` 出现 **0 次**，而带 HRTIM 的是 G474/G473 那一档（stm32g474re.html 直接把它写进 Key features：“HRTIM … 6 x16-bit counters, 184 ps resolution, 12 PWM”）。**C.4 那一行已就地改正并指向本表。** 这条更正连带一处正文待办：第 13 章把 G431 描述成“带 HRTIM 所以被选中”的那句同样需要改（本次任务不许动别的章，已登记给主控）。**本轮没能核到的两件事也写在这里，别当成已定案**：其一，ST 数据手册 PDF（DS12589 / DS12288）本轮取不到可解析的原文，所以“G431 手册全文 0 次 HRTIM”这类只有手册才能证的话，本书只写到产品页那一层；其二，开源参照实现 moteus 的官方口径是 **STM32G4**（这一条由本书附录 D 与前几轮核对记录承载，本轮未能复查 README 原文）。

**为什么这五栏（FPU / 高分辨率定时器 / 数学加速器 / ADC 触发能否硬件绑定 / CAN-FD 数）值得单列？** 因为它们各自卡在一条具体的链上，每一环都能往下再问一次：

一，**高分辨率定时器买的是什么？** 买的是死区与相移的**步进**。用本书已有的两个数算一次：第 13 章的载波口径是 20 kHz，周期

```
T = 1 / 20 kHz = 50 µs
```

（[算]。）普通 16 位定时器的最小步进是

```
Δt_16bit = 50 µs ÷ 2^16 = 763 ps
```

（[算]。）HRTIM 官方给 184 ps ⇒ **763 ÷ 184 ≈ 4.15 倍分辨率**。再看它落在死区上：第 13 章的死区口径 100 ns，用 16 位定时器只有 100 ns ÷ 0.763 ns ≈ 131 个格可分配，HRTIM 有 100 ÷ 0.184 ≈ 543 格。**同一份“死区补偿表”，能写的精细度差 4 倍**——这就是没有 HRTIM 时“软件移相”要付的代价：你只能在 763 ps 的格子里挪，剩下的误差直接乘进扭矩纹波（第 13 章那条 48 mV 死区误差的另一个来源）。

H743 那一行给了第三种答案，值得单独算一次：ST 页原文 “1× high-resolution timer (2.1 ns max resolution)”。**2.1 ns ÷ 0.184 ns ≈ 11.4 倍**——它比 G474 的 HRTIM 粗一个数量级，但比 16 位定时器的 763 ps 细 **763 ÷ 2.1 ≈ 363 倍** [算]。**“有没有高分辨率定时器”不是一个布尔值，而是一列分辨率数**，选型时真正要比的是“这一档步进落在我 100 ns 的死区上给几格”。

二，**没有 HRTIM 的那几颗靠什么补？** 靠把 ADC 触发绑到定时器上的那套互连矩阵——这一条本书只核到了**系列页那一句**：ST 的 STM32G4 系列页原文 **“A flexible interconnect matrix allows autonomous communication between peripherals and saves CPU resources.”** [厂]。**具体到哪一路定时器触发哪一路 ADC 的那张表在数据手册里，本轮取不到原文，所以那一格写“未核到”**（这正是这张表留空的原因，不是疏忽）。**为什么这件事必须是硬件的？** 因为采样窗口只有微秒量级（第 13 章）：软件在 PWM 翻转后再去启动 ADC，抖动就是纹波电流里的确定性误差，而“省 CPU 资源”那句话说到底就是**把采样时刻的确定性从软件手里拿走**。国产两家在这一栏本轮只给到外设计数：GD32M531 官方发布页写“集成高速、高精度ADC、DAC、模拟比较器等电机专属模块”、AT32M416 官方页只给高级定时器那句“带死区控制和紧急双向剎车功能”——**两家的“触发能否硬件绑定 PWM”本书都没核到，不许拿 ST 的结论替它们填空**。

三，**数学加速器买的是什么？** CORDIC 买的是 Park 与逆 Park 里那两次 sin/cos 不做浮点库调用（第 10 章那条链：读角 → Park → PI → 逆 Park），FMAC 买的是滤波器不占 CPU 循环。**GD32 这一档给了同功能的另一种命名**（TMU + SVPWM），AT32 那一档页面上则两个都没写——**这一栏空着的格子，读作“未核到”，不读作“没有”**。

四，**CAN-FD 的个数决定一条总线挂几个关节。** 第 27 章已经算过 RS-485 那条链的预算；这里只补一条选型事实：**G431 只有 1 路 FDCAN**——一颗芯片做一条总线，要多关节就必须多芯片或分时；**G474 3 路、H723 3 路、H743 2 路**，而 **F405 / F767 / GD32M531 的 CAN 不支持 FD**（参数表 CAN (FD) 为空）。宇树官方对全系电机的口径是 RS-485、单总线最多 15 台、6000 Hz [厂]，智元公开的是 EtherCAT 主站转 3× CAN-FD 5 Mbps [查]——**“3 路 CAN-FD”这个外设数量，正好是那种一次选型就能用上的判据**。

**单价这一栏为什么只有两个数？** 因为 ST 产品页的 Budgetary Price 栏在本书抓取的页面上是空的（“-”），分销商价属易腐信息：本书只给核到当天的两条（G431 ¥21.96、G474 ¥62.40，均为立创商城 2026-10-08 页面），**其余一律留空**。而这两条恰好是本表最有用的一格：**同一族里，“要不要 HRTIM”的差价是 2.8 倍**（62.40 ÷ 21.96 ≈ 2.84，[算]）——“为什么是 G4 这一档”于是变成一个可以摊到关节 BOM 上算的取舍，而不是一句外设清单。第 03 章说过执行器占整机 BOM 的 40–60%，一颗 40 元差价 × 23 个关节 ≈ 920 元 [算] 就是这次取舍的绝对额度。

**这张表在什么时候不管用**：它只覆盖“关节里的 FOC 那一层”。主频最高的那颗（H723 550 MHz、双精度 FPU）看着最强，但它没有 HRTIM、封装是 LQFP-144（20×20 mm）——**塞不进一个 φ75×20 级的关节**（对照 C.2 里 N7520 的尺寸口径）。所以这张表的正确读法是按列问“我这一路要什么”，不是按行找“最强的那颗”。宇树自己怎么选，官方未公布 [未]。

## C.5 对照：同期其他厂商的公开口径（仅列可核项）

```
智元 PowerFlow R86-3 ：60 N·m 额定 / 200 峰值 / 1.28 kg / 行星 48:1
智元 PowerFlow R86-2 ：20 / 80 N·m / 0.81 kg / 16:1
智元 精灵 G2        ：全关节力矩传感器 ≤0.02 N·m、≥5 kHz；1652 Wh / 约 4 h；185 kg
智元 灵犀 X1 DCU     ：EtherCAT 1 kHz ↔ 3×CAN-FD 5 Mbps
AGILINK OmniHand    ：16 DoF / 510 g
AGILINK Ultra-T     ：22 主动 + 三维触觉 0.01 N
AGILINK Ultra-M     ：全直驱视触觉 0.005 N
开源 moteus r4.11    ：100 A 峰值 / 900 W@30 V / 14.2 g / STM32G4 / 5 Mbps CAN-FD / $94
开源 ODrive S1       ：12–48 V / 40 A 连续 / CAN+USB / $149
开源 LeRobot SO-101  ：6 DoF，主从遥操 + 模仿学习（模仿学习 = 看人怎么做的录像照着学，第 29 章），Apache-2.0，从臂 ¥682
```

（以上全部 [查]，来自各家公开页面或仓库；本书不比较优劣，只作量级对照。）

## C.6 这张表里最该被记住的一栏

**“额定（持续）扭矩”与“IP 防护”两栏，在宇树整个人形产品线上是空的。**

而同期对照厂商的那几行里，智元 PowerFlow 明确写了“60 N·m **额定** / 200 峰值”。**这是一个可以直接拿去问厂商的差别。**

第 36 章解释了厂商为什么不给；第 37 章解释了制度为什么没要求它给。**两者合起来，就是这本书认为这个行业还年轻的最硬证据。**
