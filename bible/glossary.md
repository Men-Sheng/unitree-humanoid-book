# bible/glossary.md — 中英术语统一（一词一义）

> 官方文档中英分叉、`unitree_guide` 只有中文版，是这本书必须自己解决的事（空白论证第 12 项）。
> 规则：**一个概念一个中文名**，首现写"中文（English）"，此后不再并列。表中"禁用"列里的写法一律视为错误，`lint_style.py` 会按这张表查。
> 状态：种子表，随第 1 篇写完扩到 200 条。

## 1. 核心栈术语

| 统一用法 | 英文 | 定义（本书口径） | 禁用写法 |
|---|---|---|---|
| 通道 | channel | SDK 对"一个 DDS 话题 + 其收发端"的封装 | "管道"（与日志管道混） |
| 话题 | topic | `rt/...` 这样的字符串名字，标识一类消息 | "主题"（Kafka 味） |
| 消息类型 | message type / IDL 类型 | 决定字段布局的 IDL 生成类，如 `SportModeState_` | "消息结构" |
| 域 | DDS domain | `DomainParticipant` 的 domain id，本书基线取 0 | "领域" |
| 参与者 | participant | DDS `DomainParticipant` | 保留英文 |
| 高层运控 | high-level / sport service | 通过 `sport_client` 与 `rt/api/sport/...` 下达动作意图 | "高级控制" |
| 低层控制 | low-level | 直接读写 `rt/lowcmd` / `rt/lowstate` 的关节级通路 | "底层"（可，但全书统一用"低层"） |
| 电机总线 | actuator bus | 电机与驱动板之间的串口/CAN 协议层，比"低层控制"更低 | "驱动总线" |
| 运动模式 | mode / fsm mode | `mode` 字段取值对应的状态机状态 | "步态"（步态是其中一类） |
| 抢占 | arbitration | 多个控制器争同一执行权，由 `motion_switcher` 裁决 | "互斥" |
| 档位 | product tier | AIR / PRO / EDU 三档，决定接口可用性 | "版本"（与固件版本混） |
| 固件版本 | firmware version | 机器人侧软件版本，如 1.1.15 | "系统版本" |
| 图传 | video streaming | WebRTC 相机链路 | "视频流"（可，但标题统一"图传"） |
| 点云 | point cloud | `PointCloud2_` 一类数据 | "激光点" |
| 里程计 | odometry | `robot_odom` 一类位姿估计 | "编码器里程" |
| 地形图 | heightmap | `HeightMap_`，RL 观测输入 | "高度图"（首现并列，此后用"地形图"） |
| 域内发现 | DDS discovery | 不指定对端即可收发匹配的机制 | "广播" |
| 观测归一化 | observation normalization | 策略输入缩放，部署时必须与训练一致 | "标准化"（与 z-score 混） |
| 仿真到真机 | sim2real | 训练→部署的迁移过程 | "虚实迁移" |
| 遥操作 | teleoperation | 人通过 XR/手柄驱动机器人 | "远程操作" |
| 模仿学习 | imitation learning | 从演示数据学策略 | "示教学习" |
| 灵巧手 | dex hand | Dex1-1 / Dex3-1 等末端 | "机械手" |
| 扩展坞 | EDM / payload | 机背算力与载荷接口 | "扩展板" |

## 2. 易混对（正文必须显式区分）

| A | B | 区别要点 | 出现在 |
|---|---|---|---|
| `utlidar` | `unilidar` | 前者是 Go2 自带雷达话题族，后者是宇树独立雷达产品（L1/L2）与 `unilidar_sdk*` | 26、28 |
| `unitree_go` IDL | `unitree_hg` IDL | 两套消息命名空间，低层字段布局不同，**不可混用** | 16、05 |
| `rt/lowstate` | `rt/lf/lowstate` | 实测确认关系（见核查单 B-02），未测前正文不得断言 | 16 |
| `rt/sportmodestate` | `rt/lf/sportmodestate` | 同上（核查单 B-03） | 10、16 |
| `unitree_sdk2` | `unitree_legged_sdk` | 新（DDS）/旧（Go1、A1 时代）两代 SDK，话题与构建方式都不同 | 19 |
| `unitree_rl_gym` | `unitree_rl_lab` | Isaac Gym Preview4（停更）/ Isaac Lab（现役） | 21、22 |
| `unitree_sim_isaaclab` | `unitree_rl_lab` | 前者做数据采集与模仿学习，后者做 RL 训练 | 34、22 |
| 电机型号 `GO-M8010-6` | `IM6014` | 不同代次关节电机，参数与总线不同；**"M107" 不存在**（56 个官方仓库与产品线均无） | 18 |
| `Acquire()` | `Release()` | 控制权获取/释放，与 `CheckSticks()` 的先后关系是安全要点 | 11、12 |

## 3. 单位与记法约定

- 长度 m、角度 **rad**（涉及 `rpy`/`yaw` 时同段注明不是度）、力矩 N·m、温度 °C、电压 V、频率 Hz。
- 关节增益写作 `kp` / `kd`，**并注明是转子侧还是输出侧**（换算含 ÷r²，见第 18 章）。
- 话题一律用反引号原样写：`rt/lowstate`，不翻译、不改大小写。
- 版本号写全：`cyclonedds 0.10.2`、`固件 1.1.15`、`MuJoCo 3.3.6`。首次出现处必须带版本，不许只说"新版"。
- 机型写官方名：Go2（不写"狗2"）、G1、H1、H1_2（下标原样）、B2W、AS2、Z1、A1、Go1。

## 4. 引用与标注用语（与 voice-profile 对齐）

| 场景 | 统一写法 |
|---|---|
| 官方源码给出 | "（`unitree_sdk2_python`，commit `xxxxxxx`）" |
| 官方文档给出 | "（宇树官方文档《页面名》，抓取于 2026-10-XX）" |
| 本书实测 | "（本书实测，Go2 EDU / 固件 1.1.XX，2026-XX-XX）" |
| 未验证 | "（**未验证**，见附录 A6 第 N 条）" |
| 闭源推断 | "（据社区逆向/分析，非官方口径）" |
| 二手博客 | **不得作为事实引用**，只能生成核查项 |
