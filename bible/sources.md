# bible/sources.md — 素材索引（grounding library）

> 规则：每条素材必须写 `authoritative-for`（它在哪个问题上权威）、`known-wrong`（已知它哪里错）、`version-drift`（它跟哪个版本已不一致）。
> Technical Reviewer 用这三栏区分"错误"与"版本漂移"——漂移不触发 REVISE 回环。
> 抓取日期：主体 2026-10-07 与 2026-10-08；**2026-10-09 的回读复核单列在文末 G0**。`[核]`=读到原始文本；`[推]`=二手或推断，引用时必须在正文标注。

## A. 官方代码仓库（license 与版本事实的权威源）

| # | 源 | license（读正文确认） | authoritative-for | known-wrong / 坑 | version-drift |
|---|---|---|---|---|---|
| A1 | [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) 1.4k★/fork 392，push 2026-09 | BSD-3-Clause **[核，我独立复核]** | DDS 通道初始化、C++ 客户端契约、官方测试环境（Ubuntu 20.04 + gcc 9.4 + CMake 3.10，装 `/opt/unitree_robotics`） | **open issues = 0**，问题在官方无处沉淀；非默认安装路径要手加 `CMAKE_PREFIX_PATH` | 需记 commit |
| A2 | [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) 816★ | BSD-3 | Python 侧 ChannelSubscriber/Service 客户端、`CYCLONEDDS_HOME` 前置 | 未在 Python 3.12 验证（本书保守钉 3.10 **[推]**） | 需记 commit |
| A3 | [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) 854★，push 2026-07 | BSD-3 | `unitree_go`/`unitree_api` 消息定义、`cyclonedds_ws` 构建步骤 | **编译 cyclonedds 时终端不能 source ROS2**（须注释 `.bashrc`） | humble 可跳过自编译，foxy 必须 **[核 README_zh]** |
| A4 | [unitree_ros](https://github.com/unitreerobotics/unitree_ros) 1579★ | BSD-3 | URDF/xacro（`robots/go2_description`）、Gazebo 资产 | 与 ros2 侧消息不通用 | 需记 commit |
| A5 | [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco) 1230★ | BSD-3 | **MuJoCo 3.3.6** 钉版、支持机型清单（Go2/B2/H1/B2w/Go2w/G1/H2/AS2）、地形与 heightmap | 依赖 Boost/Spdlog/yaml-cpp/GLFW3，装不上时报错不指向根因 | MuJoCo 升版即漂移 |
| A6 | [unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym) 3586★，**2025-07 停更** | BSD-3 | Train→Play→Sim2Sim→Sim2Real 流程、`policy_1.pt`/`policy_lstm_1.pt` 产物名 | 依赖 NVIDIA **已停发的 Isaac Gym Preview 4** | 重心已转 rl_lab/mjlab **[核]** |
| A7 | [unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab) 1386★，push 2026-05 | Apache-2.0 | Isaac Lab 版训练、Go2/H1/G1-29dof、`./unitree_rl_lab.sh -l/-t`、USD 从 HF 下载 | GPU 仅测 3080/3090/4090；RTX 50 需 Isaac Sim 5.0.0 | Isaac Lab 版本敏感 |
| A8 | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) 558★ | Apache-2.0（宇树版权头；GitHub 显示 NOASSERTION） | 数据采集/模仿学习管线 | README 明确警告：**与真机共用 DDS 话题，同网段会抢控** | 同上 |
| A9 | [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate) 1688★，push 2026-09 | Apache-2.0* | AVP/Quest 遥操作、pinocchio **3.1.0**、conda **py3.8**、灵巧手 service 部署 | 版本一换即崩 | — |
| A10 | [unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot) 773★ | Apache-2.0* | LeRobot v2.0+ 数据格式与转换、pi05/groot、G1+Dex1/Dex3 真机部署、README 有更新日志 | LeRobot 上游版本升级会破坏数据兼容 | 快变 |
| A11 | [unilidar_sdk2](https://github.com/unitreerobotics/unilidar_sdk2) 106★ | BSD-3 | L2 4D 雷达、`unilidar/cloud`、`unilidar/imu`、**sdk 2.0.2 / hw 1.1.1.1 / fw 2.3.3.0** 三者匹配 | 与 L1 的 sdk 不通用 | 固件升版即漂移 |
| A12 | [point_lio_unilidar](https://github.com/unitreerobotics/point_lio_unilidar) 532★ | **GPL-2.0（传染）** | 官方 LIO | 链进闭源交付物即违规——**这是本书第 38 章的实例** | — |
| A13 | [unitree_actuator_sdk](https://github.com/unitreerobotics/unitree_actuator_sdk) 139★ | BSD-3 | GO-M8010-6/A1/B1 总线协议、转子侧↔输出侧 kp/kd ÷r²、A1/B1 的 26.07 与 ×100 换算常数 | 换算常数易被抄错 | — |
| A14 | [digital_servo](https://github.com/unitreerobotics/digital_servo) 6★ | **无 LICENSE 文件**；README 正文：`Provided by Unitree for non-commercial research, education, and DIY development. For commercial mass-production use, contact Unitree official for formal authorization.` **[核，我独立复核]** | J288/S288：半双工 TTL 8N1 **6 Mbps**、ID 0–15（15 为广播）、`specs/protocol.md` 含包格式 + CRC32 | **不可商用**——引用只能"参考不可复制" | — |
| A15 | [unitree_legged_sdk](https://github.com/unitreerobotics/unitree_legged_sdk) 437★，**2024-03 停** | BSD-3 | Go1/A1 低层旧契约 | 已停更，勿用于新项目 | 与 SDK2 话题不通用 |
| A16 | [unitree_guide](https://github.com/unitreerobotics/unitree_guide) 634★，2024-07 | BSD-3 | 旧 MPC 步态实现 | README 自述推荐 Ubuntu 18.04 + ROS Melodic（已老）；官方自认文档 **"only Chinese version now"** **[核原话]** | — |
| A17 | [unifolm-world-model-action](https://github.com/unitreerobotics/unifolm-world-model-action) 1163★ | **CC BY-NC-SA 4.0（禁商用）** | 世界模型权重与训练 | 禁商用 | — |
| A18 | [unifolm-vla](https://github.com/unitreerobotics/unifolm-vla) 637★ | **无 LICENSE** | VLA | 无授权声明 → 只能参考 | — |

`*` = GitHub 侧显示 NOASSERTION，读正文为 Apache-2.0 + 宇树版权头。**结论：不能只看 GitHub 的 license 标签。**

## B. 官方文档站

| # | 源 | authoritative-for | known-wrong / 缺陷 |
|---|---|---|---|
| B1 | [support.unitree.com/home/zh/developer](https://support.unitree.com/home/zh/developer)（Go2/B2） | 高层运控接口（`sports_services`）、ROS2 服务、Obtain SDK、AI motion service、Payload/module_update | **SPA**：正文走 `robot-api.unitree.com/doc`，匿名抓取为空白 **[核]** → 无法离线、无 sitemap、不可机器读取；中英分叉（`/main/zh` vs `/main/en`） |
| B2 | `…/G1_developer/*`、`…/H1_developer/*`、`…/R1_developer/*` | G1/H1/R1 各自 SDK 概览、遥控、语音助手；**R1 有一处孤立的 architecture_description 页** | 同上；跨层无主线 |
| B3 | `…/Algorithm_Practice` | unitree_guide 实践 | 只有中文 |
| B4 | [unitree.com/cn/opensource](https://www.unitree.com/cn/opensource/) | 官方开源总入口 | 与仓库实际状态不同步（停更仓库仍列） |
| B5 | 旧 `unitreerobotics.github.io` | — | **2022-04 已废弃且无 LICENSE**，不得作为依据 **[核]** |

## C. 已有图书（定位对照，也是"空白"的证据）

| # | 源 | 事实 | 对本书的意义 |
|---|---|---|---|
| C1 | 《四足机器人控制算法——建模、控制与实践》 | 卞泽坤、王兴兴编著；杭州宇树科技组编；机械工业出版社；2023；ISBN 978-7-111-71474-3；**155 页**；丛书"普通高等教育人工智能与机器人工程专业系列教材"；TP24 **[核：出版社页 + 辽工大 OPAC + 西南石油 OPAC 三处一致]** | 经典运控理论的**权威前置**；第 20 章指向它，不复述。同时证明"第一本宇树书"的说法不成立 |
| C2 | 《具身智能机器人基础与应用》 | 向丹、张明文、韩震峰等；机工社；2026-07-30；ISBN 978-7-111-81573-0；第 8 章"具身智能机器人宇树 G1 的应用"，配 Unitree Explore APP **[核]** | G1 只 1 章且到 APP 级 → 本书第 6 篇的空白成立 |
| C3 | 《人形机器人技术基础与应用》 | 左国玉、张伟；机工社；2025-02-07；ISBN 978-7-111-77270-5；268 页 **[核]** | 纯仿真，无宇树真机/ROS/DDS → 不构成竞品 |
| C4 | 《ROS 2 智能机器人开发实践》（胡春旭、李乔龙，机工社/古月居，2025，ROS2 Jazzy + Gazebo） | **[核存在]** | **中文 ROS2 实操的最强对标**（写作水准参照，非内容重叠） |
| C5 | Raibert《Legged Robots That Balance》MIT 1986；Kim & Wensing《Design of Dynamic Legged Robots》SIAM 2017 | **[核]** | 足式理论经典；均不涉及宇树软件栈 |
| C6 | OpenLibrary `unitree robot` → `numFound=0`（2026-10-07）；Packt/O'Reilly/Manning/Springer/Amazon 限定搜索零结果 | **[核]** | 英文无专书的依据。Google Books API 撞日配额，**未能二次交叉验证 [说明]** |

## D. 社区实现（可运行代码的权威源，但互相矛盾）

| # | 源 | license | authoritative-for | 缺陷 |
|---|---|---|---|---|
| D1 | [go2_ros2_sdk](https://github.com/abizovnuralem/go2_ros2_sdk) 1048★ | BSD-2 | **Go2 固件断代事实的记录源**：README 记 1.1.7 起速率与 URDF 行为变化、**1.1.15 起 WebRTC 静态 token → 每机唯一 AES-128** | 与官方话题命名有偏差；API 与 D2/D3 互不兼容 |
| D2 | [unitree_webrtc_connect](https://github.com/legion1581/unitree_webrtc_connect) 410★ | MIT | WebRTC 图传/指令通路（AIR/PRO 唯一路） | 依赖固件版本 |
| D3 | [autonomy_stack_go2](https://github.com/jizhang-cmu/autonomy_stack_go2) 551★ | **无 LICENSE** | `utlidar/cloud`、`utlidar/imu` 用法、Go2 全自主参考 | 只能参考不可复制 |
| D4 | [go2_omniverse](https://github.com/abizovnuralem/go2_omniverse) 1080★ | BSD-2 | Isaac 侧 Go2 桥接与导航测试台 | — |
| D5 | [FAST_LIO_LOCALIZATION_HU](https://github.com/Huuhuuw/FAST_LIO_LOCALIZATION_HU) 918★ | **无 LICENSE** | Go2 上可跑的 LIO+定位工程 | 同上 |
| D6 | [unitree_firmware_tools](https://github.com/legion1581/go2_firmware_tools) 187★ | **无 LICENSE** | 固件读取/回滚实践 | 风险操作，本书只描述不指导 |
| D7 | [docs.quadruped.de](https://www.docs.quadruped.de)（MyBotShop GmbH，©2026 维护） | 站点条款 | 按机型（Go1/Go2/A1/B2/Z1/H2）整理的文档聚合，**目前最强免费替代** | 宇树文档的**镜像转载**：无版本矩阵、无 RL/遥操作主线、无中文 |
| D8 | [MAVProxyUser/YushuTechUnitreeGo1](https://github.com/MAVProxyUser/YushuTechUnitreeGo1) 469★（TeX，2025-04 停） | 需查 | Go1 时代笔记 | 硬件已过时 |
| D9 | [egh0bww1.com GO1 整理](https://egh0bww1.com/posts/2023-10-24-unitree-go1-collection/)、[cnblogs Go2 资料汇总](https://www.cnblogs.com/flyingsir/p/19220639) | — | 线索索引 | 单人视角、无维护 |
| D10 | [知乎·深度解析 Unitree 运控服务接口 V2.0](https://damodev.csdn.net/69782b327c1d88441d8fdca1.html)、[CycloneDDS 踩坑](https://m.blog.csdn.net/python9snake/article/details/155368686)、[Go2 Air 底层解锁](https://zhuanlan.zhihu.com/p/2069008612740031291)、[47 项目全景](https://m.blog.csdn.net/u011487024/article/details/162086616)、[宇树开源整理](https://zhuanlan.zhihu.com/p/29880026964) | — | 现象线索 | **二手，只能当"待核查假设"，不可作为事实引用**；CSDN 存在批量 AI 生成文（`gitblog_*`） **[核现象]** |

## G. 器件与规格一手来源（2026-10-07 抓取，全表见 research/unitree-hardware.md）

| # | 源 | 类型 | authoritative-for |
|---|---|---|---|
| G1 | `www.unitree.com/cn/<slug>`（go2 / As2 / g1 / h1 / H2-D / R1 / b2 / LiDAR / go1/motor …，**slug 大小写敏感**） | 厂商产品页，HTML 可直接抓 | 全系规格表：质量、尺寸、续航、里程、负载、速度、防护、价格档 |
| G2 | `shop.unitree.com` | 厂商商城 | USD 价目：Go2 $1,600 起、AS2 $3,100 起、G1 $13,500、H2 $29,900、R1 $4,900、Z1 $15,999、L1 $249 / L2 $419、**GO-M8010-6 电机单卖 $369**；H1 $90,000 标"联系实价"；B2/A2/B1 的 $100,000 判为**占位价不可用** |
| G3 | `unitree_ros` 全系 URDF | 厂商源码 | **逐关节 effort / velocity 上限**（Go2 大腿 23.7、小腿 45.43 N·m，30.1 rad/s；G1 膝 139；H1 髋 200/膝 300；H2 髋膝 360；B2 200/320）——比营销页硬得多 |
| G4 | `unitree_mujoco` MJCF | 厂商源码 | 逐连杆质量（Go2 `go2.xml`：base_link 6.921、大腿 1.152×4、小腿 0.678×4、脚掌 0.241352×4 kg），**合计 15.206 kg**，与官方 15 kg 自洽（2026-10-08 逐行复核 XML 得） |
| G5 | `unitree_sdk2` 源码 + `unitree_hg` IDL | 厂商源码 | 频率链（`go2_low_level.cpp dt=0.002` = 500 Hz；sport 高层 50 Hz）、字段清单（含 `MainBoardState.fan_state`、doubleIMU） |
| G6 | 充电头网 Go2 拆解报告 | 第三方拆解 | RK3588S + 2×4 GB LPDDR4X + 64 GB eMMC + PMIC RK806-1 + 移远 4G + 必联蓝牙；电池 BT2-05 实测 29.6 V / 8000 mAh / **236.8 Wh** |
| G7 | G1 拆解汇编（中邮证券 / SemiAnalysis / Munro / Nikkei） | 第三方拆解 | 轴承点名洛阳佰纳 CRBT355A；BOM ≈ ¥41,574；两级行星 ≈20.58 |
| G8 | Nature 2026-09-23（KAIST RAIBO2，DOI 10.1038/s41586-026-11102-5） | 论文 | 四足 CoT 0.25 vs 人 0.37；马拉松实测 |
| G9 | Z1 官方文档 | 厂商 | **唯一官方明示的减速器参数**：谐波、减速比 60+、背隙 6 弧分，且官方自评"低速比→位置刚度低" |
| G11 | `unitree_sdk2_python/example/**`（go2 / g1 / h1 / h2 / b2 / as2 / a2 / r1 / motionSwitcher / front_camera 等分机型示例） | 厂商源码 | 接口形状与真实话题字面量；第 4 部"只给路标不给代码"的判断依据 |
| G12 | `unitreerobotics/digital_servo` 的 `specs/protocol.md` | 厂商源码 | **唯一公开的完整报文格式**：6 Mbps 固定、8N1、半双工、ID 0-15（15 广播不回应）、控制包 20 B / 反馈包 26 B、CRC32 4 B、timeout 位、mode 0 = 停止并锁扭矩、减速比 70070/243≈288.35。⚠ 该仓库无 LICENSE 且 README 明示非商用 → 只引用参数 |
| G10 | `support.unitree.com` | 厂商 SPA | **确认不可机器读取**（正文 API 返回空壳）→ IMU 型号与采样率、遥控/图传延迟、急停回路与功能安全认证、电芯型号、全系噪声 dB、官方里程、多圈编码器全部 **[未找到]**，不用二手值填 |

## F. 行业研报与二手数据（**只能当线索，进正文前必须追一手来源**）

| # | 源 | 给出的数 | 本书怎么用 | 风险 |
|---|---|---|---|---|
| F1 | 虎嗅《拆解机器人"肉身"》 https://m.huxiu.com/article/4863770.html | 执行器占成本约 **51%**；瞬时电流是额定的 **3-5 倍**；发热 **9-25 倍**；空翻时关节温升 **10→50 ℃**；STM32 约 **1 kHz** 控制 | 第 6/16/17/27 章的锚点候选；**"瞬时电流 3-5 倍"与本书自己算出的"静力模型高估 131×"互相印证**（都是"峰值≠连续"） | 二手研报，未追到其原始出处；**引用前必须找到一手（厂商手册或论文）**，否则正文只能写"行业分析普遍估计为…" |
| F2 | 新浪《人形机器人核心零部件：电机、减速器、传感器详解》 | 三类核心件的成本与技术路线分布 | 附录 A 的对照参考 | 同上 |
| F3 | B 站《机器人硬件很简单，先熟悉减速器、电机、传感器》 | 器件科普视频，说明"器件层内容活在视频里、没沉淀成书" | 佐证空白论证，不作数据来源 | 视频不可核对 |
| F4 | 豆瓣检索"宇树" → 15 条结果全部与宇树无关 | 空白论证的关键证据 | manifesto §2.2 | 检索式与日期需记录（2026-10-07） |
| F5 | 《揭开机器人的面纱》（机工社 2016，ISBN 978-7-111-52130-3）；《人形机器人简史》（机工社 2026-08）；刘云浩《具身智能》（中信 2025，7.2/150）；Rus《心与芯》（中信 2025，7.7/63）；DK《遇见未来：机器人》（2018，86 款真机型、无宇树、8-14 岁） | 竞品清单 | manifesto §2.2 空白论证 | 部分书目"评价人数不足"，评分不代表质量 |
| F6 | 标杆技法与**翻车现场**：《编码》9.3（后 7 章难度突升被差评）、《万物运转的秘密》9.3、《万物解释者》7.2（为省术语牺牲精确）、《What If?》8.0（笑与严谨分层）、《万物简史》8.6（幽默加在人身上）、《人类尸体的奇异生活》7.7、《数学之美》8.7（问题驱动章标题；印刷错误多）、《规模》7.9（单规律过度外推） | 写作规范 | `bible/voice-profile.md` §6.5 的四条规则 | 差评是抽样观察，不是系统评价 |

## E. 未核实 / 明确存疑（禁止写入正文，除非先核查）

| 项 | 状态 |
|---|---|
| OpenRobotEcho / DeepRoboticsLab 社区 Wiki（GO1 时代） | **本次检索未找到在线站点** [未核] |
| `audio2text` 是否有独立官方仓库 | 未找到，[推] |
| CVE-2026-27509 / 27510（宇树 RCE） | **未核实**，仅见于二手安全号 [推] |
| 官方是否有 ONNX / Unity 策略导出文档 | 未找到 → [推]，第 23 章必须自己给出并标"本书做法" |
| 《四足仿生机器人基本原理及开发教程》（ISBN 978-7-302-64022-6）出版年份、是否用宇树整机 | 未核 |
| 《Modern Robotics》中译本的出版社 | 当当 + 北邮/同济 OPAC 有条目，出版社未核 |
| Leanpub 中国作者收款可行性 | 未核 |
| 国内出版社（机工/电社/图灵）一手投稿规范 | 未获取（图灵帮助页年代久远） |

## F. 摄取规则（Phase 1 执行）

1. 主 agent **不读**原始素材；每个 subagent 领 3-5 条源，回结构化摘要：`事实 | 出处 | 版本/commit | license | 属于哪一栏（authoritative-for / known-wrong / version-drift）`。
2. **话题名、消息类型、字段单位一律从 IDL 源码 grep**（A1/A2/A3），不接受 README 或博客作为唯一依据。
3. 任何进入正文的技术论断必须挂一个源编号（A/B/C/D 系列）；挂不上的进 `verification/` 或 `waivers`。
4. D10 类二手源只能生成核查项，不能生成正文句子。


---

## 追加（2026-10-08，人形一手复验）：宇树文档中心的一手取法

**关键发现：`support.unitree.com` 是 SPA，但正文可以匿名拿到。**

```
1. GET https://robot-api.unitree.com/doc/spaces2?locale=en      → 所有文档 space 列表
2. GET https://robot-api.unitree.com/doc/?space=<SPACE>&locale=en → 该 space 的目录（含 doc id）
3. GET https://doc-cdn.unitree.com/<space>/<id>/<locale>/<space>_<id>_<locale>
       → 返回**原始 Markdown**，无 JS、无鉴权
```

已用此路径取到并引用的一手页面（示例）：`8/1484` About M8010、`8/107` RS-485 协议（帧长/CRC/量化）、`8/106` Control Mode、`30/1371` IM6014 规格、`30/1383` IM6014 协议、`30/1377` STM32 参数表、`30/1378` Motor configuration。

**`30/1377`（2026-10-08 抓取，标题 *STM32 HAL Communication Example*）是全书关于"关节里那颗 MCU"的唯一一手出处**，三条硬信息：

- 官方例程基于 **STM32F413RGT6**，并明写"如果移植到其他 MCU 型号，**建议使用带 FPU 的 MCU**"；
- **UART 外设必须支持 6 Mbps / 4 Mbps**，且经 UART-to-485 模块（TX=PA9、RX=PA10、RE/DE=PA11）——这是第 27 章"4 Mbps 不是随便挑的"的官方佐证；
- 参数量程表：`id` 0–15、`outputTor` ±162.133、`outputSpd` ±253.973、`outputPos` ±32508.539、`Kp` **0–410.725**。
  这个 Kp 上限与 `code/tools/foc_check.py` 里独立登记的 IM6014 `kp_max = 410.725` **逐位吻合**，互为交叉验证。

另新增二手来源：**兆易创新 GD32F50MxxG 电机控制 MCU**（电子发烧友 2026-08-05，
`https://m.elecfans.com/article/8187284.html`）——Cortex-M33 最高 252 MHz、
"单芯片集成三相栅极驱动器"、"标配 2 路 CAN-FD"、1 MB Flash / 128 KB RAM、3 路 12 位 ADC，
官方定位明写"面向人形机器人、协作机械臂、灵巧手"。**这是媒体转述官方稿，标 [行]/[推]，
不得当宇树事实**；ST 官网 G474 产品页 2026-10-08 抓取超时，故附录 C.2b 的 G4 三格留空。

**EtherCAT 器件链的一手来源 = ETG 官网技术页**（`https://www.ethercat.org/en/technology.html`，
2026-10-08 抓取），第 27 章"如果你真要用 EtherCAT"一节的四句引文全部出自此页：
"reads the data addressed to it 'on the fly', and inserts its data in the frame as the frame
is moving downstream"；"The frame is delayed only by hardware propagation delay times"；
"The time from the first DC SubDevice is cyclically distributed to all other devices"；
ESC 可为 ASIC/FPGA/集成 MCU，应用接口列 SPI、8/16 位并口、32 位并行 I/O；
CoE 提供 "Object Dictionary, PDO Mapping (Process Data Objects) and SDO (Service Data Objects)"。
**CiA402 的对象字典索引号本书一律不写**：2026-10-08 检索到的中文资料全是博客级，
没有 CiA/ETG 规范原文；这类编号写错会被懂行的人当场发现，属于"可以不讲，不能讲错"的范畴。
`design.ros2.org/articles/rosbag2_storage_plugins.html` 与
`docs.ros.org/en/humble/Tutorials/Advanced/rosbag2/recording.html` **两个链接都返回 404**，
第 33 章的 rosbag2/MCAP 段落因此只引用 `github.com/ros2/rosbag2` README 里能读到的话
（record/play/convert/info、SQLite 与 MCAP 两种后端、播放自动识别后端、`--topics`/`--exclude-topics`），
**README 没写默认后端，书里就不替它断言**。

**仓库勘误（一手核对）**：
- `github.com/unitreerobotics/unitree_mjcf` **不存在（404）**。官方 MJCF 在 **`unitree_mujoco`** 仓库 `unitree_robots/<model>/` 下。
- `unitree_motors_sdk` 不存在。电机文档走上面的文档中心路径。
- `unitree_model` 仓库只有 USD/DAE（`G1/29dof`、`B2`、`Go2`、`H1/h1`、`H2`、`H2_Plus`），**不含 URDF/XML**。
- 官方 URDF 在 `unitree_ros/robots/`：`g1_description/` 下有 **22 个 G1 URDF 变体**（23dof / 29dof / rev_1_0 / lock_waist / mode_10~18 / with_hand / inspire_hand / dual_arm / comp / pl）。**同一个仓库里两个 G1 URDF 对 hip_roll 给了 139 与 88 两个不同的 effort** —— 引用时必须指明是哪一个文件。

**新增一手数据点（可直接引用，均 [厂]）**：
- `MotorCmd.msg` = `uint8 mode / float32 q / float32 dq / float32 tau / float32 kp / float32 kd / uint32 reserve`；`unitree_hg` 的 `motor_cmd`/`motor_state` 是 **35 元素定长数组**。
- `MotorState.msg` 含 **`tau_est`**（估计扭矩）、`ddq`、`temperature int16[2]`、`vol`、`sensor uint32[2]`。
- M8010 帧长 17 B（下行）/16 B（上行），CRC16_CCITT 覆盖前 15/14 B；ID 0~14，15 = 广播无响应；多字节小端。
- IM6014 帧长 20 B（头 0xFE 0xEE，CRC32-MPEG2）/26 B（头 0xFC 0xEE 不计入 CRC）；量化 2560 = 1 N·m、32768/2π = 1 rad、k_pos 12800 = 1 N·m/(rad/s)。
- M8010 kp/kd 允许范围 **0.0–25.599**；IM6014 输出侧 Kp 0–410.725、Kd 0–102.681。
- 官方 `unitree_rl_lab` G1 配置：关节电机 **N7520-14.3（88 N·m）/ N7520-22.5（139）/ N5020-16（25）/ W4010-25（5）/ N5020-16-parallel（踝 35）**；`decimation 4 × sim.dt 0.005` ⇒ 策略 50 Hz；`action_scale 0.25`。
- `rt/lowcmd` / `rt/lowstate` 500 Hz（文档口径）+ SDK `control_dt_ = 0.002` 印证。
- Z1 官方脚注原文（低减速比 ⇒ 位置控制刚度低 ⇒ 不优化会抖）—— 见第 14 章。

**未复验到位、正文已降级处理的项**：G1 各关节额定扭矩、G1/H1/H2 的 PWM 载波频率与死区、IM6014 内部控制环频率、R1 电池容量与电压、H1-2 与 Dex3-1/Dex5-1 价格、全系电芯型号。以上在正文中一律标 [未]，不得当事实陈述。

## G0. 2026-10-09 回读复核（逐条，HTTP 状态与字节数都是当场实测）

| 复核项 | 地址 | 结果 | 影响 |
|---|---|---|---|
| `unitree_rl_lab` 的许可文件 | `raw.githubusercontent.com/unitreerobotics/unitree_rl_lab/main/LICENCE` | **200，11,362 B**，前两行 "Apache License / Version 2.0, January 2004"；同仓库 `LICENSE` → 404 | 作废 do-not-touch 第 27 条旧写法（曾记"无许可文件"）；附录 D.2 那一行改正 |
| ODrive 的许可文件 | `raw/.../ODrive/master/{LICENSE,LICENCE,LICENSE.md}` | 前两个 404，**`LICENSE.md` 200** | 附录 D.6 判据①补"扩展名也要试" |
| moteus 的三行规格 | `raw/mjbots/moteus/main/README.md`、`docs/reference/theory.md` | README：`Control Rate 15-30kHz`、`PWM Switching Rate 15-60kHz`；theory.md：`switching frequency (by default 30kHz)`；全文 `bandwidth` **0 命中** | 附录 D.1 那三条原样保留；第 44 章"README 没给电流环带宽的数"成立 |
| 宇树 13 个仓库的许可文件名 | GitHub raw 逐个试四种名字 | 12 个有（`LICENSE` / `LICENCE` / `LICENSE.md` 三种命名都出现过），只有 `digital_servo` 四种全 404（限制写在 README 正文） | 附录 D.2 的"部分宇树仓库无 LICENSE"改为精确说法 |
| 附录 E.3 里的四条可疑地址 | `doc-cdn.unitree.com/`、`mjbots.com`、两条 `raw.../<dir>/` | 首页/目录，不是某一页文献 | `gen_appendix_e.py` 新增两类排除规则，E.3 从 131 → 125 条 |


## G1. 2026-10-09 别家一手抓取（新文件 `research/other-vendor-firsthand.md`）

F-30 第 5 条那笔账开始还。逐字原文、URL、访问日期与新文件里那张表。本轮结果分三类：

- **一手证实**：Figure Helix 的 `7B-parameter ... VLM` / `80M parameter cross-attention encoder-decoder transformer` /
  `operating at 7-9 Hz` / `continuous robot actions at 200 Hz`（figure.ai/news/helix）；
  GR00T 的 `Base model (3B params)` / `action_horizon expanded from 16 to 40` /
  `State and action dimensions expanded from 29 to 132` / `1 GPU with 16 GB+ VRAM (e.g., RTX 4090, L40, H100, Jetson AGX Thor/Orin, DGX Spark)`
  （Isaac-GR00T 仓库 README raw 页）。**注意最后一条原文是"16 GB+ 起步"，不是"标配 16 GB"**。
- **一手未载**：宇树 `unifolm-world-model-action` README 里 `Hz / ms / control rate / frequency / real-time` **全部零命中**
  ⇒ 旧稿那句"真机侧客户端约 15 Hz [厂]"没有一手支撑，正文已降为 [查][未] 并写明是二手量级。
- **抓取被拦**：`physicalintelligence.company` 的 `research/pi-star-0.6` 与 `research` 两页，对 WebFetch 与带桌面 UA 的
  curl 一律 **429**（拦截页 33,945 字节）；arXiv API 用 `"learns from experience" AND "advantage conditioned"` 检索 **0 条**
  ⇒ π*0.6 的 860 M / 4 B / 5 步 / 63 ms 仍是二手，第 29 章的标记本轮由 [查] 降为 [推]。

**一条纪律同步写进口径**：`[查]` 的定义是"本书已读到原文"。抓取被拦 ≠ 读到原文，所以必须降级——
不能因为"这数大家都这么写"就替厂商签字。

- 2026-10-09 补充：DeepMind Genie 3 博客**一手读到**（720p / `24 frames per second` / `retaining consistency for a few minutes`），
  据此删掉旧稿"20–24 fps"里那个没有出处的 20。同一轮里 arXiv API 对 `Genie Operator-1` / `GE-Act` / `SmolVLA` / `AGIBOT World`
  四条检索**全部返回空**（不是 404，是空响应），1X 与 Wayve 的厂商页本轮未访问成功 ⇒ 这批数继续记 [推]，**不许因"常见"而升 [查]**。

- 2026-10-09 第二轮：**arXiv 的 HTML 全文页可稳定读到**（`arxiv.org/html/2503.06669v1`），
  AgiBot World 的 `1,001,552 trajectories / 2976.4 hours / 217 tasks / 87 skills / 106 scenes / 100 dual-arm humanoid robots / 4,000 square meters /
  episodes typically span approximately 30 seconds` 全部逐字核到 ⇒ 第 33 章那条除法与 4,000 ㎡、100 台升为 [查]。
  **负面结果同样存档**：论文没有任何"日产多少条"的产出率 ⇒ 媒体那句降回 [推]；GE-Act 与 SmolVLA 的一手页面本轮检索不到 ⇒ 降 [推]。

- 2026-10-09 第三轮：`arxiv.org/html/2501.03575v3`（Cosmos World Foundation Model Platform）逐字读到
  `two base models that are 4B and 12B in size`、`Cosmos-Predict1-4B / -12B`、`single NVIDIA A100 GPU with 80GB memory`。
  ⇒ **4B 这个输入升一手**，正文那条 8 GB ÷ 16 GB 的算术不再依赖"Edge 4B 能在 Orin/Thor 上跑"；
  档位名 Super/Nano/Edge 与 Orin/Thor 那句**一手没有**，降 [推]。GAIA-2 的分辨率一手未取到，仍 [推]。

- 2026-10-09 第四轮（arXiv 全文页 / abs 页）：π0 `10 integration steps` + `3.3 billion parameters` + `H=50` + 50 Hz（2410.24164）；GAIA-2 `up to five … camera streams`、`resolution of 448×960`、`each spanning 2 seconds`、`8.4B parameters`（2503.20523）；DROID `76k demonstration trajectories`、`350 hours of interaction data`、`84 tasks`、`564 scenes`（2403.12945，**html v3 是 404，abs 页可用**）。⇒ 第 30 章"5–10 步"、第 33 章 16.6 s 每条、第 34 章 GAIA-2 那组数升 [查]。仍未取到：GE-Act、SmolVLA、Cosmos 2026 的 Super/Nano/Edge 档位名、1X 的 11 s。

- 2026-10-09 第五轮：Genie Envisioner（arXiv 2508.05635v3）一手读到 GE-Act 是 `a lightweight 160M-parameter autoregressive action decoder`，输出 `54-step torque trajectories within 200 ms on a commodity GPU`、30 Hz、计时在 `onboard NVIDIA RTX 4090 GPU` ⇒ 第 34 章那格升 [查]；**同时推翻第 30 章一处分类**（原稿把 GE-Act 列为流匹配代表，实为自回归解码器）。
- SmolVLA 官方页只给总规模 `4.5亿参数` 与动作头 `Flow-Matching Transformer`，**主干/专家分栏未公布** ⇒ 旧稿 `100 M ÷ 450 M ≈ 4.5 倍` 不仅没出处，还把总规模当成了主干，是**口径用错**；正文改为明说"算不出倍数"。
- 公开口径里能算"专家 ÷ 主干"的只剩两家：Helix 80 M ÷ 7 B ≈ 87 倍（两边一手）、π*0.6 860 M ÷ 4 B ≈ 4.7 倍（二手，官网 429）。
