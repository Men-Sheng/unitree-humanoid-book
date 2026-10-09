# 已归档：真机核查单 · 开发者手册版

> ⚠️ 2026-10-07 定位调整。这份核查单服务的是『开发者工作流手册』版大纲，验证的是话题名 / 频率 / 权限链。
> 现行大纲是科普书，核查改成了拆解与测量，见 `teardown-measures-01.md`。
> 本文件保留：将来若出第二本（开发者手册），话题全表与兼容矩阵仍然要用它。

## 真机核查单 · 第 1 批（MVP 篇：第 0-2 篇 + 附录 A1/A2）

> 规则（抄 `book-factory` 的 verification-plan）：凡是"本会话确定不了、但现实能回答"的论断，都要写成**别人能执行、并留答案槽**的检查项。不许悄悄把论断改软，也不许"看起来对就当对"。
> **这一批只能你本人跑**——机器人由你操作，我不做无人值守控制。
> 一次开机大约能覆盖 15-20 项。请按组顺序跑，**每组跑完就填**，别攒到最后凭记忆。

## 0. 跑之前先填这张"指纹表"（附录 A2 兼容矩阵的一行原始数据）

| 字段 | 值 | 怎么拿 |
|---|---|---|
| 机型与档位 | ☐ Go2 AIR ☐ Go2 PRO ☐ Go2 EDU ☐ G1 ☐ 其他____ | 机身铭牌 / App 关于页 |
| 固件版本 | ________ | App → 设备信息；或 `unitree_firmware_tools` 读取 |
| 电机/雷达固件 | ________ | 有 Unilidar 时按 `unilidar_sdk2` 打印 |
| 上位机 OS | ________ | `uname -a`（WSL2 要注明 Windows 版本） |
| Python | ________ | `python -V` |
| cyclonedds 版本 | ________ | `ls $CYCLONEDDS_HOME` + 安装时用的 tag；**本书基线 0.10.2** |
| ROS2 发行版 | ☐ 无  humble ☐ foxy | `printenv ROS_DISTRO` |
| 网卡名与 IP | ________ | `ip a`；机器人默认网段 `192.168.123.x` |
| 是否装扩展坞/EDM | ☐ 无 ☐ 有____ | 目视 |
| 采集日期 | ________ | — |

**记录方式**：把每一项的原始输出重定向到文件，别只填结论。
```bash
mkdir -p ~/unitree-book/session-01 && cd ~/unitree-book/session-01
uname -a > 00-os.txt; python -V >> 00-os.txt; ip a > 00-net.txt; printenv | grep -i -E "cyclone|ros" > 00-env.txt
```

---

## A 组：连通性与"能不能收到东西"（对应第 9、10 章）

| # | 检查项 | 命令 | 期望 | 实测 | 影响哪一节 |
|---|---|---|---|---|---|
| A-01 | 机器人可达 | `ping 192.168.123.16 -c 3` | 0% 丢包 | ☐ | 9.2 网络准备 |
| A-02 | DDS 工厂能起 | `python example/helloworld/publisher.py`（另开一终端跑 `subscriber.py`） | 订阅端打印 msg | ☐ | 9.3 第一个收发 |
| A-03 | **不设 CYCLONEDDS_HOME 会怎样** | `unset CYCLONEDDS_HOME; python example/helloworld/subscriber.py` | 记录是"报错"还是"静默收不到" | ☐ | 9.1 那个坑（**这条决定书里怎么写警告**） |
| A-04 | 话题存活与频率 | `python code/tools/dds_topic_probe.py --seconds 20 --out probe-go2` | 至少 1 个 ALIVE | ☐ | **附录 A1** |
| A-05 | 上表里哪些话题其实是死的 | 看 `probe-go2.md` 的 `NO_DATA` 行 | 逐条记录 | ☐ | **附录 A1**（标"未观测到"而不是"不存在"） |
| A-06 | 手机 App 是否抢占用 | 先跑 A-04，再连 App 进运动模式，重复 A-04 | 记录 ALIVE 集合的变化 | ☐ | 11 安全前置 / 12 抢占 |

## B 组：权限判定链（对应第 4、16 章 —— 全书最容易写错的地方）

| # | 检查项 | 命令 | 期望 | 实测 | 影响哪一节 |
|---|---|---|---|---|---|
| B-01 | 能否订阅 `rt/lowstate` | `python dds_topic_probe.py --only rt/lowstate --seconds 10` | EDU：ALIVE ~500Hz；AIR/PRO：？ | ☐ | 16.1 |
| B-02 | `rt/lf/lowstate` 与 `rt/lowstate` 的关系 | `--only rt/lowstate rt/lf/lowstate` | 记录两者各自是否活、字段是否同构 | ☐ | 16.1（**这是"同一话题两个名字"类混淆的根因**） |
| B-03 | `rt/sportmodestate` vs `rt/lf/sportmodestate` | 同上两条话题 | 记录哪个活、频率、`mode` 取值 | ☐ | 10 / 16 |
| B-04 | 低层指令是否被拒 | `python example/go2/low_level/go2_stand_example.py`（**吊架/趴下状态**） | 记录是报错、无反应、还是真的动了 | ☐ | 16.2、11 安全 |
| B-05 | MotionSwitcher 能力清单 | `python example/motionSwitcher/motion_switcher_example.py` | 记下**全部** mode 名与 id | ☐ | 12（这张清单网上没有完整版） |
| B-06 | sport_client 动作覆盖 | `python example/go2/high_level/go2_sport_client.py` 逐个选项 | 记录哪些返回失败/无效果（不同固件差异） | ☐ | 12 |
| B-07 | utlidar 开关 | `python example/go2/high_level/go2_utlidar_switch.py` | 开关前后 A-04 的 ALIVE 集合差异 | ☐ | 28 |

## C 组：数据语义（对应附录 A1 的"单位/坐标系"三栏）

| # | 检查项 | 怎么做 | 期望 | 实测 |
|---|---|---|---|---|
| C-01 | `position` 单位与原点 | 机器人静置已知位置，打印 `position`；再手动挪 1.00 m 复测 | 明确是 m 还是别的、原点在哪、是否随重启归零 | ☐ |
| C-02 | `velocity` 是机体系还是世界系 | 让机器人以固定速度前进，同时改变机身朝向复测 | 一句话判定 | ☐ |
| C-03 | `yaw`/`imu_state` 轴向与符号 | 顺时针旋转机身 90°，记录变化量 | 轴向约定（**全书坐标系约定的锚点**） | ☐ |
| C-04 | 关节编号与物理对应 | 手动掰 0 号腿的髋关节，看 `motor_state` 哪个索引变 | 索引↔关节对照表 | ☐ |
| C-05 | 温度/电压字段量纲 | 打印 `BmsState_` / `motor_state.temperature` | 单位与合理范围 | ☐ |
| C-06 | 故障码在哪看 | 触发一次可恢复告警（如超限），记录 `Error_` 是否出现、话题名 | 话题名 + 码表入口 | ☐ |

## D 组：仿真对照（对应第 14 章 + 附录 A2 的仿真列）

| # | 检查项 | 命令 | 期望 | 实测 |
|---|---|---|---|---|
| D-01 | MuJoCo 能起 | `unitree_mujoco`（钉 **3.3.6**）加载 Go2 配置 | 有窗口、无缺库报错；缺库请贴完整报错 | ☐ |
| D-02 | 同一份订阅代码在仿真下是否可用 | 仿真运行时跑 A-04 | 记录 ALIVE 集合与真机的**差集**（这张差集就是第 14 章的核心表格） | ☐ |
| D-03 | 仿真与真机同网段抢控是否真会发生 | 仿真与真机同时开，跑 B-06 的一个安全动作 | ⚠️ 危险项：**只在吊架下做**，或跳过并记 waiver | ☐ |

## E 组：版本断代（对应第 40 章 + 附录 A2）

| # | 检查项 | 怎么做 | 期望 | 实测 |
|---|---|---|---|---|
| E-01 | 当前固件是否 ≥1.1.15 | 看指纹表 | 决定 WebRTC 那章怎么写 | ☐ |
| E-02 | WebRTC 图传能否拿到帧 | `python example/go2/front_camera/camera_opencv.py` | 有画面 / 报 token 错 / 其他 | ☐ |
| E-03 | cyclonedds 0.10.2 与更新版是否都可用 | 换版本各跑一次 A-04 | 记录"必须 0.10.2"到底是硬约束还是文档惯例 | ☐ |
| E-04 | ROS2 桥话题映射 | 起 `unitree_ros2` 桥后 `ros2 topic list -t` | 完整清单（**附录 A1 的第二数据源**） | ☐ |

---

## 交回方式

跑完把整个 `~/unitree-book/session-01/`（含 `probe-go2.json`、`probe-go2.md`、各 `*.txt`）打包给我，或直接贴文本。我会：

1. 把实测值写进 `bible/sources/`（新增"一手实测"类源，标日期与固件版本）；
2. 用实测**覆盖**任何与文档不一致的论断，并在正文注明"文档说 X，实测为 Y（固件 Z）"——这类句子是这本书最有价值的部分；
3. 没跑/跑不了的项写进 `project-status.yaml` 的 `waivers`，并同步到**附录 A6《本书未验证事项》**，对读者公开；
4. 顺手把 `dds_topic_probe.py` 的 registry 补全（它现在只有 13 条，附录 A1 的目标是 60+ 条）。

## 已知风险与免责

- B-04 / B-06 / D-03 会让机器人**真的动**。请吊架或趴下姿态、清场、手在急停上。
- 我不会替你执行任何一项（不做无人值守控制，也不装开机自启）。
- 若某项你判断"不值得测"，直接说，我记 waiver 而不是猜一个数填进去。
