# 宇树人形机器人 · 训练栈 / 数据栈 / 模型 / 电源 / 参考实现 数据表

访问日期：**2026-10-08**。规则：只记读到的原文数字；查不到进 F 节「未取到」；冲突不抹平，两栏并列。
分级：**官方仓库文件** / **官方页面** / **官方页面(文档中心)** / **README自陈（厂商口径）** / **二手**。
与 `research/humanoid-specs.md`（下称【前表】）互补，不重复其内容。

## 0. 仓库锚点（本次实测 HEAD commit，核对时以此为准）

| 仓库 | HEAD commit | HEAD 日期 | 分支 |
|---|---|---|---|
| `unitreerobotics/unitree_rl_gym` | `276801e46c5d433564f24658bac64f254b7d2d4b` | 2025-07-25 | master |
| `unitreerobotics/unitree_rl_lab` | `4960b84732b0c2ec593dccbfe963fda1bcd7b1e3` | 2025-11-19 | main |
| `unitreerobotics/xr_teleoperate` | `817fb00c63cde15e5f24a0f8fa08e1e33ed89d3b` | 2026-09-07 | main |
| `unitreerobotics/unitree_lerobot` | `41c2805742de879ddab2d8d6beaeaf215f876395` | 2026-05-25 | main |
| `unitreerobotics/unifolm-wla` | `0a1aa87be8f775c7883fcd27216e3666ac18a8c5` | 2026-09-29 | main |
| `unitreerobotics/unifolm-world-model-action` | `3e198de68de55f93f24b3ad623dd499390aaee45` | 2026-03-18 | main |
| `mjbots/moteus` | `8f747f4ac448d117c1390b77ca2d80c27e751a56` | 2026-09-27 | main |
| `odriverobotics/ODrive` | `3a2e4dd1bfbda9e4c534d5c7d8428a99c361e783` | 2026-01-20 | master |
| `huggingface/lerobot` | `ca69a2068462a37f7cdcb74180927a2f863d2bf7` | 2026-10-07 | main |

**通道勘误（重要）**

| 指令里给的路径 | 实测结论 |
|---|---|
| `unitree_rl_lab` 的 `deploy/robots/g1/g1_23dof.yaml` | **不存在**。真实路径是 **`deploy/robots/g1_23dof/config/config.yaml`**（目录名 `g1_23dof`，文件名 `config.yaml`） |
| `unitree_IL_lerobot` | **与 `unitree_lerobot` 是同一个仓库**：HEAD commit 完全相同（`41c28057…`），`git clone` 走 GitHub 重定向。即 **仓库已改名**，两名字指向同一内容 |
| `unilab` | 未作为宇树仓库出现（本次未找到同名官方仓库） |
| `github.com/ODrive-robots/ODrive` | **Repository not found**。正确 org 是 **`odriverobotics/ODrive`** |
| `www.livoxtech.com/mid360`、`/cn/mid360` | **均 404**（2026-10-08）。Livox 产品线页现在只列 `/mid-360l`、`/mid-360s`、`/mid-70`；**原版 Mid-360 已不在产品页目录里** |
| `github.com/unitreerobotics/unifolm-world-model-action` 的 README 内链 | README 正文里的配置链接指向 **`github.com/unitreeerobotics/unitree-world-model`**（另一个仓库名），与本仓库名不一致 |

---

## A. 强化学习训练栈（sim2real 章）

### A1. `unitree_rl_gym`（legged_gym / Isaac Gym 路线）

**支持机型（README 原文，`README.md` 行 9）**
> "This is a repository for reinforcement learning implementation based on Unitree robots, supporting Unitree **Go2, H1, H1_2, and G1**."

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| 训练环境目录（实测） | `legged_gym/envs/g1/`、`legged_gym/envs/go2/`、`legged_gym/envs/h1/`、`legged_gym/envs/h1_2/`（各含 `*_config.py`；`h1_2` 另带 `README.md`） | 仓库文件树（HEAD `276801e`） | 官方仓库文件 |
| `--task` 取值 | `(go2, g1, h1, h1_2)` | `README.md` 行 48 | 官方仓库文件 |
| 部署配置（Mujoco / 实机各 3 份） | `g1.yaml`, `h1.yaml`, `h1_2.yaml` | `deploy/deploy_mujoco/configs/`、`deploy/deploy_real/configs/` | 官方仓库文件 |
| **Go2 是人形以外的四足**，不属于本书人形口径 | — | 同上 | — |
| 许可证 | **BSD 3-Clause**；版权行 `Copyright (c) 2016-2023 HangZhou YuShu TECHNOLOGY CO.,LTD. ("Unitree Robotics")` | `LICENSE` | 官方仓库文件 |
| 子目录二次许可 | `legged_gym/LICENSE` = ETH Zurich / NVIDIA（2021）版权，即 legged_gym 本体沿用上游许可 | `legged_gym/LICENSE` | 官方仓库文件 |
| 预训练权重（签入仓库） | `deploy/pre_train/g1/motion.pt`、`h1/motion.pt`、`h1_2/motion.pt`（共 3 个） | 文件树 | 官方仓库文件 |

**训练侧 G1 参数（`legged_gym/envs/g1/g1_config.py`，类 `G1RoughCfg`）**

| 参数 | 值 | 推导含义 | 行 |
|---|---|---|---|
| `sim.dt` | `0.005`（继承基类 `LeggedRobotCfg.sim`） | 物理步长 5 ms | `envs/base/legged_robot_config.py:155` |
| `control.decimation` | `4` | 每策略步 4 次 sim 更新 | `g1_config.py:57` |
| **策略输出周期** | **0.005 × 4 = 0.02 s ⇒ 50 Hz** | 与 `deploy_real/configs/g1.yaml` 的 `control_dt: 0.02` 相互印证 | 两文件 |
| `control.control_type` | `'P'` | 位置型混合控制 | 40 |
| `control.action_scale` | **0.25** | 注释原文 `# action scale: target angle = actionScale * action + defaultAngle` | 55 |
| `control.stiffness` | `{hip_yaw:100, hip_roll:100, hip_pitch:100, knee:150, ankle:40}` N·m/rad | — | 42-47 |
| `control.damping` | `{hip_yaw:2, hip_roll:2, hip_pitch:2, knee:4, ankle:2}` | 源码注单位写作 `[N*m/rad] [N*m*s/rad]` | 48-53 |
| `asset.file` | `resources/robots/g1_description/**g1_12dof.urdf**` | **训练用 12dof 简化模型** | 60 |
| `num_actions` / `num_observations` / `num_privileged_obs` | **12 / 47 / 50** | — | 25/23/24 |
| `init_state.pos` | `[0.0, 0.0, 0.8]` m | — | 5 |
| `rewards.soft_dof_pos_limit` | `0.9` | — | 69 |
| `rewards.base_height_target` | `0.78` m | — | 70 |
| **policy 结构** | `init_noise_std=0.8`；`actor_hidden_dims=[32]`、`critic_hidden_dims=[32]`、`activation='elu'`；`policy_class_name="ActorCriticRecurrent"`；`rnn_type='lstm'`、`rnn_hidden_size=64`、`rnn_num_layers=1` | **G1 部署的是 LSTM 策略**，MLP 只有 32 宽 | 91-108 |
| `max_iterations` | `10000`；`experiment_name='g1'` | — | 105-108 |

**H1 / H1-2 训练参数（同仓库）**

| 机型 | `sim.dt` | `decimation` | 策略频率 | `action_scale` | 文件 |
|---|---|---|---|---|---|
| H1 | 0.005（基类） | 4 | **50 Hz** | 0.25 | `legged_gym/envs/h1/h1_config.py` |
| H1-2 | **0.0025**（`class sim(LeggedRobotCfg.sim): dt = 0.0025`） | **8** | **0.02 s ⇒ 50 Hz** | 0.25 | `legged_gym/envs/h1_2/h1_2_config.py` |
| 实机/Mujoco 部署（三机型统一） | — | — | `control_dt: 0.02`（50 Hz） | — | `deploy/deploy_real/configs/{g1,h1,h1_2}.yaml` 行 2 |
| Mujoco 侧仿真步长 | `simulation_dt: 0.002`（三文件行 8，**与 Isaac Gym 的 0.005/0.0025 不同**） | — | — | — | `deploy/deploy_mujoco/configs/*.yaml` |

H1 训练增益（`h1_config.py`）：stiffness `{hip_yaw 150, hip_roll 150, hip_pitch 150, knee 200, ankle 40, torso 300, shoulder 150, elbow 100}`；damping `{hip×3:2, knee:4, ankle:2, torso:6, shoulder:2, elbow:2}`。
H1-2 训练增益（`h1_2_config.py`，键名带 `_joint`）：stiffness `{hip_yaw 200, hip_roll 200, hip_pitch 200, knee 300, ankle_pitch 40, ankle_roll 40}`；damping `{hip×3:2.5, knee:4, ankle_pitch 2.0, ankle_roll 2.0}`。

**域随机化清单（本节的落点）**

| 参数 | 基类默认（`envs/base/legged_robot_config.py`，`class domain_rand` 行 92-99） | G1 覆盖（`g1_config.py` 行 28-35） | H1 覆盖 | H1-2 覆盖 |
|---|---|---|---|---|
| `randomize_friction` | True | True | True | True |
| `friction_range` | `[0.5, 1.25]` | **[0.1, 1.25]** | [0.1, 1.25] | [0.1, 1.25] |
| `randomize_base_mass` | **False** | **True** | True | True |
| `added_mass_range` | `[-1., 1.]` | **[-1., 3.]**（单位 kg，加在 base） | [-1., 3.] | [-1., 3.] |
| `push_robots` | True | True | True | True |
| `push_interval_s` | 15 | **5** | 5 | 5 |
| `max_push_vel_xy` | 1. | **1.5**（m/s） | 1.5 | 1.5 |
| 观测噪声（`class noise`，行 137-147） | `add_noise=True`，`noise_level=1.0`；`noise_scales = {dof_pos 0.01, dof_vel 1.5, lin_vel 0.1, ang_vel 0.2, gravity 0.05, height_measurements 0.1}` | 继承（G1 未覆盖） | 继承 | 继承 |
| 观测缩放（`class normalization.obs_scales`，行 127-136） | `{lin_vel 2.0, ang_vel 0.25, dof_pos 1.0, dof_vel 0.05, height_measurements 5.0}`；`clip_observations 100.`、`clip_actions 100.` | G1 deploy yaml 另给 `ang_vel_scale 0.25 / dof_vel_scale 0.05 / dof_pos_scale 1.0 / cmd_scale [2.0,2.0,0.25]`（见【前表】C4.1） | — | — |

> **口径提示（不要抹平）**：`unitree_rl_gym` 的域随机化只有 **摩擦、base 质量、推力** 三类物理量 + 观测噪声，**没有**电机力度误差、连杆质量/惯量、PD 增益、延迟、地面恢复系数等条目。任何"宇树 RL 训练随机化了 N 项物理参数"的写法，此处 N ≤ 3。

**安装版本（`doc/setup_en.md`，官方仓库文件）**：推荐 NVIDIA 驱动 **525 或更新**（行 7）；`conda install pytorch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 pytorch-cuda=12.1`（行 56）；Isaac Gym 从 NVIDIA 官网手动下载（行 65，**README 未写 Isaac Gym 的版本号**）；`rsl_rl` 用 `git clone https://github.com/leggedrobotics/rsl_rl.git`（行 96，**未 pin commit/版本**）。

### A2. `unitree_rl_lab`（Isaac Lab 路线）

**支持的机器人（README 原文，`README.md` 行 13）**
> "Currently supports Unitree **Go2**, **H1** and **G1-29dof** robots."

**实测注册的 gym task 全集（HEAD `4960b84`，只有 5 个）**

| gym id | 类型 | 注册文件 |
|---|---|---|
| `Unitree-Go2-Velocity` | locomotion（四足，非人形） | `source/unitree_rl_lab/unitree_rl_lab/tasks/locomotion/robots/go2/__init__.py` |
| **`Unitree-H1-Velocity`** | locomotion 人形 | `…/tasks/locomotion/robots/h1/__init__.py` |
| **`Unitree-G1-29dof-Velocity`** | locomotion 人形 | `…/tasks/locomotion/robots/g1/29dof/__init__.py` |
| **`Unitree-G1-29dof-Mimic-Dance-102`** | mimic 人形 | `…/tasks/mimic/robots/g1_29dof/dance_102/__init__.py` |
| **`Unitree-G1-29dof-Mimic-Gangnanm-Style`** | mimic 人形 | `…/tasks/mimic/robots/g1_29dof/gangnanm_style/__init__.py` |

- **无 H2、无 R1、无 H1-2 的训练环境**：`source/` 下 grep `UNITREE_H2`/`UNITREE_R1`/`UNITREE_H1_2_CFG` **0 命中**；含 `h1_2`/`r1`/`h2` 字样的文件只有 5 个：`deploy/robots/g1_23dof/main.cpp`、`deploy/robots/g1_29dof/main.cpp`、`deploy/robots/h1_2/{config/config.yaml,main.cpp}`、`README.md`。分级：官方仓库文件。
- **`tasks/locomotion/robots/g1/` 下只有 `29dof/`**，**不存在 `23dof/` 的 env cfg**。`source/…/tasks/locomotion/robots/g1/__init__.py` 是**空文件**。⇒ 【前表】C4.2 里写的「locomotion：`robots/g1/`（子目录 `23dof`,`29dof`）」在本次 HEAD **不成立**，属仓库版本变化；两栏并列。
- **资产侧** `UNITREE_G1_23DOF_CFG` 存在于 `assets/robots/unitree.py`（行 298），但**没有对应的 gym 注册任务**；`deploy/robots/g1_23dof/` 的 C++ 部署器与 `config.yaml` 齐备，`policy_dir` 指向 `../../../logs/rsl_rl/unitree_g1_23dof_velocity`。⇒ **23dof 有部署、无训练配置**，这是官方仓库内的真实缺口。

**G1 29dof locomotion 关键数值（`tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py`）**

| 项 | 值 | 行 |
|---|---|---|
| `decimation` | **4** | 376 |
| `sim.dt` | **0.005** | 379 |
| 策略步长 | 导出代码原文 `cfg["step_dt"] = env.cfg.sim.dt * env.cfg.decimation` ⇒ **0.02 s = 50 Hz** | `utils/export_deploy_cfg.py:29` |
| `episode_length_s` | 20.0 | 377 |
| `num_envs` | 4096（训练）／ play 配置 32 | 358, 402 |
| `action scale` | `JointPositionActionCfg(asset_name="robot", joint_names=[".*"], scale=0.25, use_default_offset=True)` | ActionsCfg |
| `soft_joint_pos_limit_factor` | `0.9`（`UnitreeArticulationCfg` 类属性） | `assets/robots/unitree.py:30` |
| 速度指令范围 | `ranges lin_vel_x=(-0.1,0.1), lin_vel_y=(-0.1,0.1), ang_vel_z=(-0.1,0.1)`；`limit_ranges lin_vel_x=(-0.5,1.0), lin_vel_y=(-0.3,0.3), ang_vel_z=(-0.2,0.2)`；play cfg 用 `limit_ranges` | CommandsCfg / 405 |
| 高度扫描 | `RayCasterCfg` 栅格 `resolution=0.1, size=[1.6,1.0]`，挂在 `torso_link`，`offset z=20.0`，`update_period = decimation*dt = 0.02` | 68-75, 387 |

**该环境实际启用的域随机化（`class EventCfg`，行 87-156）——只有 4 条，逐条抄**

| EventTerm | func | mode | 随机对象与范围 |
|---|---|---|---|
| `physics_material` | `mdp.randomize_rigid_body_material` | startup | 所有 `body_names=".*"`：`static_friction_range (0.3, 1.0)`、`dynamic_friction_range (0.3, 1.0)`、`restitution_range (0.0, 0.0)`、`num_buckets 64` |
| `add_base_mass` | `mdp.randomize_rigid_body_mass` | startup | 仅 `body_names="torso_link"`：`mass_distribution_params (-1.0, 3.0)`、`operation "add"`（kg） |
| `base_external_force_torque` | `mdp.apply_external_force_torque` | reset | `torso_link`：`force_range (0.0, 0.0)`、`torque_range (-0.0, 0.0)` ⇒ **实际关闭** |
| `reset_base` | `mdp.reset_root_state_uniform` | reset | `pose_range x(-0.5,0.5) y(-0.5,0.5) yaw(-3.14,3.14)`；`velocity_range` 全部 `(0.0, 0.0)` |
| `reset_robot_joints` | `mdp.reset_joints_by_scale` | reset | `position_range (1.0, 1.0)`、`velocity_range (-1.0, 1.0)` |
| `push_robot` | `mdp.push_by_setting_velocity` | interval | `interval_range_s (5.0, 5.0)`、`velocity_range x(-0.5,0.5) y(-0.5,0.5)` |

观测加噪（`Unoise = AdditiveUniformNoiseCfg`）：`base_ang_vel (−0.2,0.2)`、`projected_gravity (−0.05,0.05)`、`joint_pos_rel (−0.01,0.01)`、`joint_vel_rel (−1.5,1.5)`；`enable_corruption=True`；`history_length=5`。
**未启用的随机化**（EventCfg 里没有对应条目）：执行器增益/力度误差、连杆惯量、摩擦系数 Fs/Fd、通信延迟、地面参数、电机温度模型。⇒ rl_lab 的 sim2real 主要靠 **质量 + 摩擦 + 推力 + 观测噪声 + 5 帧历史**，这一点值得在书里写实。

**执行器模型（`assets/robots/unitree_actuators.py`）——电机家族映射的最强证据**

`UnitreeActuator(DelayedPDActuator)` 带 **摩擦模型 + 延迟 + T-N 曲线限力**。参数语义（原文 docstring）：
- `X1` = "Maximum Speed at Full Torque(T-N Curve Knee Point) Unit: rad/s"
- `X2` = "No-Load Speed Test Unit: rad/s"
- `Y1` = "Peak Torque Test(**Torque and Speed in the Same Direction**) Unit: N*m"
- `Y2` = "Peak Torque Test(**Torque and Speed in the Opposite Direction**) Unit: N*m"
- `Fs` 静摩擦、`Fd` 动摩擦、`Va` 摩擦完全激活速度（默认 0.01）
- 摩擦施加式（源码）：`τ_friction = Fs·tanh(q̇/Va) + Fd·q̇`；限力按 `X1/X2` 分段（`_compute_effort_limit`）

| 型号类名 | X1 | X2 | Y1（同向峰值） | Y2（反向峰值） | Fs | Fd | armature (kg·m²) |
|---|---|---|---|---|---|---|---|
| `UnitreeActuatorCfg_M107_15` | 14.0 | 25.6 | **150.0** | **182.8** | 0 | 0 | 0.063259741 |
| `UnitreeActuatorCfg_M107_24` | 8.8 | 16 | **240** | **292.5** | 0 | 0 | 0.160478022 |
| `UnitreeActuatorCfg_Go2HV` | 13.5 | 30 | 20.2 | 23.4 | 0 | 0 | — |
| `UnitreeActuatorCfg_N7520_14p3` | 22.63 | 35.52 | **71** | **83.3** | 1.6 | 0.16 | 0.01017752 |
| `UnitreeActuatorCfg_N7520_22p5` | 14.5 | 22.7 | **111.0** | **131.0** | 2.4 | 0.24 | 0.025101925 |
| `UnitreeActuatorCfg_N5010_16` | 27.0 | 41.5 | 9.5 | 17.0 | 0 | 0 | 0.0021812 |
| `UnitreeActuatorCfg_N5020_16` | 30.86 | 40.13 | **24.8** | **31.9** | 0.6 | 0.06 | 0.003609725 |
| `UnitreeActuatorCfg_W4010_25` | 15.3 | 24.76 | **4.8** | **8.6** | 0.6 | 0.06 | 0.00425 |

齿轮级惯量注记（源码 docstring 原文，单位 kg·m²）：N7520-14.3 `rotor 0.489e-4 / gear_1 0.098e-4 ratio 4.5 / gear_2 0.533e-4 ratio 48/22+1`；N7520-22.5 `rotor 0.489e-4 / gear_1 0.109e-4 ratio 4.5 / gear_2 0.738e-4 ratio 5.0`；N5020-16 `rotor 0.139e-4 / gear_1 0.017e-4 ratio 46/18+1 / gear_2 0.169e-4 ratio 56/16+1`；W4010-25 `rotor 0.068e-4 / gear_1 ratio 5 / gear_2 ratio 5`；N5010-16 `rotor 0.084e-4 / gear_1 0.015e-4 ratio 4 / gear_2 0.068e-4 ratio 4`。
armature 定义原文：`armature = J2 + J1 * i2^2 + Jr * (i1 * i2)^2`。

**电机 → 关节 映射（G1，`assets/robots/unitree.py`；与【前表】B6.5 一致，此处补 mimic 口径）**

| 电机型号 | 关节（`joint_names_expr`） | 29dof velocity cfg：effort/vel/Kp/Kd | 29dof **mimic** cfg：effort/vel/Kp/Kd | 23dof cfg |
|---|---|---|---|---|
| **N7520-14.3** | `.*_hip_pitch_.*`, `.*_hip_yaw_.*`, `waist_yaw_joint` | 88 / 32.0 / hip **100.0**, waist_yaw **200.0** / hip **2.0**, waist_yaw **5.0** | 类名换成按型号派生：hip_pitch/hip_yaw/waist_yaw = **88 / 32.0 / 40.179 / 2.5579** | 同 29dof |
| **N7520-22.5** | `.*_hip_roll_.*`, `.*_knee_.*` | **139** / 20.0 / hip_roll 100.0, knee **150.0** / hip_roll 2.0, knee **4.0** | 139 / 20.0 / **99.098** / **6.3088** | 同 29dof |
| **N5020-16** | `.*_shoulder_.*`, `.*_elbow_.*`, `.*_wrist_roll.*`, `.*_ankle_.*`, `waist_roll_joint`, `waist_pitch_joint` | **25** / 37 / **40.0**（标量）/ 肩肘腕roll **1.0**，ankle **2.0**，waist_* **5.0** | feet(ankle) **50 / 37.0 / 28.501 / 1.814**；waist_roll/pitch **50 / 37.0 / 28.501 / 1.814**；arms **25 / 37 / 14.251 / 0.9072** | 10 个臂关节 25/37/40.0/1.0 |
| **N5020-16-parallel** | `.*ankle.*`（**仅 23dof**） | — | — | **35 / 30 / 40.0 / 2.0** |
| **W4010-25** | `.*_wrist_pitch.*`, `.*_wrist_yaw.*` | **5** / **22** / **40.0** / **1.0** | **5 / 22 / 16.778 / 1.0681** | — |

派生增益常数（`unitree.py` 行 513-529，原文）：
`NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz`；`DAMPING_RATIO = 2.0`；
`STIFFNESS = ARMATURE * NATURAL_FREQ²` ⇒ 5020 **14.25062309787429**、7520-14 **40.17923847137318**、7520-22 **99.09842777666113**、4010 **16.77832748089279**；
`DAMPING = 2.0 * DAMPING_RATIO * ARMATURE * NATURAL_FREQ` ⇒ 5020 **0.907222843292423**、7520-14 **2.5578897650279457**、7520-22 **6.3088018534966395**、4010 **1.06814150219**；
`ARMATURE_5020 0.003609725 / _7520_14 0.010177520 / _7520_22 0.025101925 / _4010 0.00425`。
⇒ **mimic 用的是「按 10 Hz 自然频率从 rotor 惯量推出来的物理 PD」，velocity locomotion 用的是「手调整数 PD（100/150/200/40）」。同一仓库两套增益，务必分开引用。**

**mimic 的逐关节 action_scale（仓库内唯一给出的逐关节动作尺度）**
生成规则（`unitree.py` 行 706-717，原文）：`UNITREE_G1_29DOF_MIMIC_ACTION_SCALE[n] = 0.25 * effort_limit_sim[n] / stiffness[n]`；
`tracking_env_cfg.py` 行 129：`JointPositionActionCfg(..., scale=UNITREE_G1_29DOF_MIMIC_ACTION_SCALE, use_default_offset=True)`。
落地值（`deploy/robots/g1_29dof/config/policy/mimic/dance_102/params/deploy.yaml`）：
`scale: [0.548, 0.548, 0.548, 0.351, 0.351, 0.439, 0.548, 0.548, 0.439, 0.351, 0.351, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.439, 0.0745, 0.0745, 0.0745, 0.0745]`
校验（本次逐位算过）：0.25×88/40.179=**0.548**（hip_pitch/hip_yaw/waist_yaw）、0.25×139/99.098=**0.351**（hip_roll/knee）、0.25×50/28.501=**0.439**（ankle、waist_roll/pitch）、0.25×25/14.251=**0.439**（肩/肘/腕roll）、0.25×5/16.778=**0.0745**（腕 pitch/yaw）✓
同文件：`step_dt: 0.02`；`stiffness` 完整 29 项原文：`[40.2, 99.1, 40.2, 99.1, 28.5, 28.5, 40.2, 99.1, 40.2, 99.1, 28.5, 28.5, 40.2, 28.5, 28.5, 14.3, 14.3, 14.3, 14.3, 14.3, 16.8, 16.8, 14.3, 14.3, 14.3, 14.3, 14.3, 16.8, 16.8]`（0-based：idx0-14 为腿+腰，idx15-19 与 22-26 是 14.3＝N5020，idx20-21 与 27-28 是 16.8＝W4010）；`damping: [2.56, 6.31, 2.56, 6.31, 1.81, 1.81, 2.56, 6.31, 2.56, 6.31, 1.81, 1.81, 2.56, 1.81, 1.81, 0.907×5, 1.07×2, 0.907×5, 1.07×2]`。

**velocity 版部署参数（`deploy/robots/g1_29dof/config/policy/velocity/v0/params/deploy.yaml`）**
`step_dt: 0.02`；`scale` 全部 **0.25**（29 项）；`stiffness: [100,100,100,150,40,40, 100,100,100,150,40,40, 200,200,200, 40×14]`；`damping: [2,2,2,4,2,2, 2,2,2,4,2,2, 5,5,5, 10×14]`；`commands.base_velocity.ranges: lin_vel_x [-0.5,1.0], lin_vel_y [-0.3,0.3], ang_vel_z [-0.2,0.2], heading: null`；观测项 `base_ang_vel scale [0.2,0.2,0.2] hist 5 / projected_gravity [1,1,1] hist 5 / velocity_commands [1,1,1] hist 5 / joint_pos_rel 1.0×29 hist 5 / joint_vel_rel 0.05×29 hist 5 / last_action 1.0×29 hist 5` ⇒ **策略输入维数 = 6 项 × 29/3 关节 × 5 帧 = 375**。
`joint_ids_map: [0, 6, 12, 1, 7, 13, 2, 8, 14, 3, 9, 15, 22, 4, 10, 16, 23, 5, 11, 17, 24, 18, 25, 19, 26, 20, 27, 21, 28]`

> **⚠ 工程陷阱（官方仓库文件实测，可直接印进书里）**：`export_deploy_cfg.py` 里 `stiffness` / `damping` 是 **按 SDK 电机序号排**（源码 `stiffness[joint_ids_map] = asset.data.…`），而 **`default_joint_pos` 和 `actions.*.scale` / `.offset` 是按 Isaac Lab 仿真关节序排**（源码未做重排），二者靠 `joint_ids_map` 桥接。逐位验证：`map[9]=3 → SDK3=left_knee → default_joint_pos[9]=0.3` ✓、`map[15]=16 → left_shoulder_roll → 0.25` ✓、`map[21]=18 → left_elbow → 0.97` ✓。把 deploy.yaml 当同一个索引序读就会全部错位。
> **⚠ 同仓库不一致（并列，勿择一）**：`deploy.yaml`(velocity) 的 `stiffness[13],[14]`（SDK 13/14 = waist_roll/waist_pitch）= **200**，`damping` 臂部 = **10.0**；而 `assets/robots/unitree.py` 的 `UNITREE_G1_29DOF_CFG` 对同一批关节写的是 `N5020-16 stiffness=40.0`、`damping 臂=1.0`。`deploy/robots/g1_29dof/config/config.yaml` 的 FixStand 与 deploy.yaml 一致（200 / 10），与 unitree.py 不一致。

**`deploy/robots/g1_23dof/config/config.yaml`（指令要的"真实路径"文件，全文只有 FSM 增益，无 action_scale）**

| FSM | 项 | 值（原文顺序即 SDK 电机序，6/6/3/7/7 分行） |
|---|---|---|
| Passive | `id` | 1；`mode[]` 全 **1**；`kd[]` 全 **3** |
| FixStand | `id` | 2；`kp = [100,100,100,150,40,40, 100,100,100,150,40,40, 200,200,200, 40×7, 40×7]`；`kd = [2,2,2,4,2,2, 2,2,2,4,2,2, 5,5,5, 10×7, 10×7]`；`ts: [0, 3]`；`qs = [[], [-0.1,0,0,0.3,-0.2,0, -0.1,0,0,0.3,-0.2,0, 0,0,0, 0,0.25,0,0.97,0.15,0,0, 0,-0.25,0,0.97,-0.15,0,0]]` |
| Velocity | `id` 3，`type: RLBase`，`policy_dir: ../../../logs/rsl_rl/unitree_g1_23dof_velocity` |
| 迁移条件 | `Passive→FixStand: LT + up.on_pressed`；`FixStand→Passive: LT + B.on_pressed`；`FixStand→Velocity: RB + X.on_pressed`；`Velocity→Passive: LT + B.on_pressed` |
| **该文件里没有的** | **`action_scale`、`step_dt`、电机型号名** —— 全仓库 `g1_23dof` 目录下也没有 velocity 版 `deploy.yaml`（`config/policy/` 目录不存在） |
| `deploy/robots/g1_23dof/include/Types.h` 全文只有 4 行 | `using LowCmd_t = unitree::robot::g1::publisher::LowCmd;` / `using LowState_t = unitree::robot::g1::subscription::LowState;`（含 2 行 include）。⇒ **不含任何电机映射** |

其他 deploy 配置（同格式）：`b2`、`go2`、`go2w`、`h1`、`h1_2`、`g1_29dof`（另有 2 个 mimic 的 `params/deploy.yaml`）。`h1` 的 Passive `mode[] = [10,10,10,10,10,10, 10,10,10, 1,1, 1,1,1,1, 1,1,1,1]`（髋/膝/躯干用 **0x0A**、踝/臂用 **0x01**，与【前表】C2 的 G1 伺服模式口径一致）。

**版本 pin（README 徽章与代码，官方仓库文件）**

| 组件 | 官方给出的口径 | 来源 |
|---|---|---|
| **Isaac Sim** | 徽章 `IsaacSim-5.1.0` | `README.md` 行 3（**badge，非 requirements**） |
| **Isaac Lab** | 徽章 `IsaacLab-2.3.0` | `README.md` 行 4 |
| rsl_rl | **未 pin 版本**。代码按 Isaac Lab 2.x 的封装写：`from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoActorCriticCfg, RslRlPpoAlgorithmCfg`（`RslRlPpoAlgorithmCfg` 是 rsl_rl **v4/v5** 时代的类名）；`play.py` 注释 `# version 2.3 onwards / # version 2.2 and below` 只是向后兼容分支 | `tasks/locomotion/agents/rsl_rl_ppo_cfg.py`、`scripts/rsl_rl/play.py` 行 137-142 |
| onnxruntime（部署用） | `deploy/thirdparty/onnxruntime-linux-x64-**1.22.0**/`（目录名 + `VERSION_NUMBER` 文件） | 文件树 |
| Python | `requires-python = ">=3.10"` | `source/unitree_rl_lab/pyproject.toml` 行 12 |
| 许可证 | 徽章 `license-Apache2.0`；`pyproject.toml` 行 13 `license = { text = "Apache 2.0" }`；仓库根许可文件名是 **`LICENCE`（英式拼写，不是 LICENSE）** | `README.md` 行 5、`pyproject.toml`、文件树 |
| **版本号自相矛盾** | `pyproject.toml` `version = "0.2.1"`；`source/unitree_rl_lab/config/extension.toml` `version = "0.1.0"`；`docs/CHANGELOG.rst` 最新条目 `0.2.1 (2025-07-17)`，其上 `0.2.0 (2025-07-17)`「Added support for **beyond_mimic** … Added **delay & friction model support for unitree_actuator**」，`0.1.0 (2025-07-01)` initial | 三处官方文件 |
| PPO 超参 | locomotion：`num_steps_per_env=24`、`max_iterations=50000`、`save_interval=100`、`empirical_normalization=False`、actor/critic `[512,256,128]` elu、`init_noise_std=1.0`、`entropy_coef=0.01`、`lr=1e-3` adaptive、`gamma 0.99`、`lam 0.95`、`desired_kl 0.01`；mimic 同结构但 `max_iterations=30000`、`save_interval=500`、`entropy_coef=0.005` | `tasks/locomotion/agents/rsl_rl_ppo_cfg.py`、`tasks/mimic/agents/rsl_rl_ppo_cfg.py` |

**README 自己写的工作流（原文引用，行 88-141）**
> "## Deploy
> After the model training is completed, we need to perform **sim2sim** on the trained strategy in **Mujoco** to test the performance of the model. Then deploy **sim2real**."
> ### Setup → 安装依赖 + `git clone unitree_sdk2` + `cmake .. -DBUILD_EXAMPLES=OFF && sudo make install` + `cd unitree_rl_lab/deploy/robots/g1_29dof && mkdir build && cd build && cmake .. && make`
> ### Sim2Sim → 安装 `unitree_mujoco`；把 `/simulate/config.yaml` 的 `robot` 设为 g1、`domain_id` 设 0、`enable_elastic_hand` 设 1、`use_joystck` 设 1；`./unitree_mujoco`，另一终端 `./g1_ctrl`；操作序列原文：「1. press **[L2 + Up]** to set the robot to stand up / 2. Click the mujoco window, and then press **8** to make the robot feet touch the ground. / 3. Press **[R1 + X]** to run the policy. / 4. … press **9** to disable the elastic band.」
> ### Sim2Real → "You can use this program to control the robot directly, but make sure the on-borad control program has been closed."（原文拼写 on-borad）→ `./g1_ctrl --network eth0`
> 训练/回放（行 76-85）：`./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Velocity`（等价 `python scripts/rsl_rl/train.py --headless --task …`）、`-p` 为 play、`-l` 列出任务。

各步使用的仿真器（按仓库自己的文字与代码归属）：

| 步骤 | rl_gym | rl_lab |
|---|---|---|
| Train | **Isaac Gym**（`doc/setup_en.md` 明确要求下载 isaacgym） | **Isaac Sim / Isaac Lab**（README 徽章 + `import isaaclab`） |
| Play（验证） | Isaac Gym 内可视化 | Isaac Sim 内可视化 |
| Sim2Sim | **MuJoCo**（`deploy/deploy_mujoco/deploy_mujoco.py`） | **unitree_mujoco**（需另装，走 `rt/lowcmd` DDS） |
| Sim2Real | `deploy_real.py`（Python，`unitree_sdk2_python`）或 `cpp_g1`（LibTorch） | C++ `g1_ctrl`（unitree_sdk2 + **onnxruntime 1.22.0**） |

rl_gym README 原文（行 28-35，可直接引）：
> "The basic workflow … is: `Train` → `Play` → `Sim2Sim` → `Sim2Real`
> - **Train**: Use the Gym simulation environment … Real-time visualization during training is not recommended to avoid reduced efficiency.
> - **Play**: Use the Play command to verify the trained policy and ensure it meets expectations.
> - **Sim2Sim**: Deploy the Gym-trained policy to other simulators to ensure it's not overly specific to Gym characteristics.
> - **Sim2Real**: Deploy the policy to a physical robot to achieve motion control."

### A3. 特权观测 / teacher-student 蒸馏（本次落点）

**rl_gym：非对称 actor-critic（有 privileged obs，无蒸馏）**

| 事实 | 值/原文 | 文件:行 |
|---|---|---|
| 机制开关的注释（原文） | `num_privileged_obs = None # if not None a priviledge_obs_buf will be returned by step() (critic obs for assymetric training). None is returned otherwise` | `legged_gym/envs/base/legged_robot_config.py:7` |
| G1 / H1 / H1-2 的 `num_privileged_obs` | **50 / 44 / 50** | `envs/g1/g1_config.py:24`、`envs/h1/h1_config.py:31`、`envs/h1_2/h1_2_config.py:39` |
| G1 策略观测 47 维拆解（源码拼接顺序） | `base_ang_vel(3) · projected_gravity(3) · commands[:, :3]*commands_scale(3) · (dof_pos-default_dof_pos)(12) · dof_vel(12) · actions(12) · sin_phase(1) · cos_phase(1)` = **47** | `legged_gym/envs/g1/g1_env.py:73-80` |
| G1 特权观测 50 维 | 上述 47 前面加 `base_lin_vel * obs_scales.lin_vel(3)` = **50** ⇒ **唯一特权量是基座线速度** | `g1_env.py:82-91` |
| 特权观测的载体 | `base_task.py:47` 建 `privileged_obs_buf`；`legged_robot.py:78-80` 一并 clip；`base_task.py:75-76` `get_privileged_observations()` | 官方仓库文件 |
| **蒸馏** | **未搜到**：全仓库 `grep -niE "distill|teacher|student"` **0 命中** | 官方仓库文件 |
| 导出网络类型（README 行 81-84） | 「Standard networks (MLP) are exported as `policy_1.pt`. RNN networks are exported as `policy_lstm_1.pt`.」 | `README.md` |

**rl_lab：critic 组 + 已接线但未被任何配置使用的 DistillationRunner**

| 事实 | 值/原文 | 文件:行 |
|---|---|---|
| 非对称观测分组 | `class ObservationsCfg` 下 `policy: PolicyCfg`（无 `base_lin_vel`）与 `critic: CriticCfg`（**含 `base_lin_vel`，且无噪声、`enable_corruption` 不设**）；注释原文 `# privileged observations` | `tasks/locomotion/robots/g1/29dof/velocity_env_cfg.py:188-235`（h1 同 234 行；go2 同 264 行） |
| mimic 的特权组更宽 | `class PrivilegedCfg(ObsGroup)`：`command, motion_anchor_pos_b, motion_anchor_ori_b, body_pos, body_ori, base_lin_vel, base_ang_vel, joint_pos, joint_vel, actions`；policy 组只有 `motion_command, motion_anchor_ori_b, base_ang_vel, joint_pos_rel, joint_vel_rel, last_action`；`critic: PrivilegedCfg = PrivilegedCfg()` | `tasks/mimic/robots/g1_29dof/dance_102/tracking_env_cfg.py:138-170`（gangnam 同行号） |
| **蒸馏代码存在** | `train.py` 两处 `if agent_cfg.resume or agent_cfg.algorithm.class_name == "Distillation":`（行 165、188）；`play.py` `elif agent_cfg.class_name == "DistillationRunner": from rsl_rl.runners import DistillationRunner`（行 121-124）与 `elif hasattr(policy_nn, "student_obs_normalizer")`（行 144-145） | `scripts/rsl_rl/{train,play}.py` |
| **但没有任何配置启用它** | locomotion 与 mimic 的两个 `BasePPORunnerCfg` 都只用 `RslRlPpoAlgorithmCfg`；`train.py` 实际只 `runner = OnPolicyRunner(env, agent_cfg.to_dict(), …)`（**无 DistillationRunner 分支**）。⇒ **仓库里 teacher-student 是"从 Isaac Lab 模板继承下来的接口挂点"，没有可跑的蒸馏示例** | 同上 |

---

## B. 遥操作与数据采集（数据经济学章）

### B1. `xr_teleoperate`

| 项 | 值（原文优先） | 来源 | 分级 |
|---|---|---|---|
| 定位 | "implements **teleoperation** control of a **Unitree humanoid robot** using **XR (Extended Reality) devices** (such as Apple Vision Pro, PICO 4 Ultra Enterprise, or Meta Quest 3)" | `README.md` 行 51 | 官方仓库文件 |
| 许可证 | **Apache License 2.0**，`Copyright [2025] [HangZhou YuShu TECHNOLOGY CO.,LTD. ("Unitree Robotics")]` | `LICENSE` | 官方仓库文件 |
| 支持机型（README 表格，全部标 "✅ Complete"） | G1 (29 DoF)、**G1 (23 DoF)**、H1 (4-DoF arm)、H1_2 (7-DoF arm)、**H2 (7-DoF arm)**、**R1 (5-DoF arm)**、**R1 (7-DoF arm)**；末端：Dex1-1 gripper、Dex3-1 dexterous hand、Inspire dexterous hand、BrainCo dexterous hand | `README.md` 行 67-120 | 官方仓库文件 |
| `--arm` 可选值 | `G1_29` `G1_23` `H1_2` `H1` `H2` `R1_A5` `R1_A7`（默认 `G1_29`） | 行 227 | 官方仓库文件 |
| `--ee` 可选值 | `dex1` `dex1_internal` `dex3` `inspire_ftp` `inspire_dfx` `brainco`（默认 None） | 行 228 | 官方仓库文件 |
| **控制/录制频率** | `--frequency`：**"Set the FPS for recording and control"**，默认 **30.0**；源码 `parser.add_argument('--frequency', type=float, default=30.0, help='control and record \'s frequency')`；主循环 `sleep_time = max(0, (1/args.frequency) - time_elapsed)` | `README.md` 行 224；`teleop/teleop_hand_and_arm.py` 行 76、524 | 官方仓库文件 |
| **延迟** | **README/源码未给出任何 ms 或 Hz 的端到端延迟数值**（只有上面这个 30 Hz 的循环周期）。⇒ 「遥操作延迟」：**未取到** | 全仓库 grep | — |
| 输入/显示模式 | `--input-mode`：`hand`（hand tracking，默认）/ `controller`；`--display-mode`：`immersive`（默认）/ `ego` / `pass-through` | 行 225-226 | 官方仓库文件 |
| 网络/地址 | `--img-server-ip` 默认 **192.168.123.164**（PC2）；`--network-interface` 给 CycloneDDS；XR 端访问 `https://192.168.123.2:8012/?ws=wss://192.168.123.2:8012`；WebRTC 头相机预览 `https://192.168.123.164:60001`；防火墙放行 **8012** | 行 229-230、304、322、176 | 官方仓库文件 |
| 录制触发方式 | `--record`：「Press **r** to start teleoperation, then **s** to start recording; press **s** again to stop and save the episode. Press **s** repeatedly to repeat the process.」；`--task-dir` 默认 `./utils/data/`；`--task-name` 默认 `pick cube`；`--task-goal` 默认 `pick up cube.`；`--task-desc` 默认 `task description`；`--task-steps` 默认 `step1: do this; step2: do that;` | 行 240-245 | 官方仓库文件 |
| 录制落盘结构 | 每 episode 一目录 `episode_XXXX/`，含 `colors/`、`depths/`、`audios/`、`data.json`；`add_item(colors, depths, states, actions, tactiles, audios, sim_state)`；颜色/深度存 `.jpg`（文件名 `{idx:06d}_{key}.jpg`），音频存 `audio_{idx:06d}_{mic}.npy`；`data.json` 三段 `"info"/"text"/"data"` | `teleop/utils/episode_writer.py` 行 105-126、129-196 | 官方仓库文件 |
| info 段固定字段 | `version "1.0.0"`、`date`（当天）、`author "unitree"`、`image {width,height,fps=self.frequency}`、`depth {…fps}`、**`audio {sample_rate: 16000, channels: 1, format: "PCM", bits: 16}`**、`joint_names{left_arm,left_ee,right_arm,right_ee,body}`、`tactile_names{left_ee,right_ee}`、`sim_state ""` | 同上 行 66-87 | 官方仓库文件 |
| 默认图像尺寸 | `image_size=[640, 480]`；`frequency=30`（`EpisodeWriter.__init__` 默认参数） | 行 14 | 官方仓库文件 |
| 依赖（`requirements.txt`） | 存在该文件；README 指定 conda 环境 `python=3.10 pinocchio=3.1.0 numpy=1.26.4 -c conda-forge` | `README.md` 行 134 | 官方仓库文件 |
| 必需硬件（`Device.md` §5.1，原文表） | **G1 1 台**（备注 "Developer computing unit version required"）、**XR 设备 1 台**（Apple Vision Pro / PICO 4 Ultra Enterprise / Quest 3 / Quest 3S）、**路由器 1**（"Recommended: at least WiFi6 support"）、**用户计算机 1**（"Recommended x86-64 architecture"；仿真模式按 Isaac Sim 4.5.0 官方硬件建议）、**头相机 1**（"Monocular camera (built-in Realsense D435i)" 或外接双目）、**USB3.0 线 1**（Type-C 双直头，约 0.2 m） | `Device.md` 行 14-71 | 官方仓库文件 |
| 数据采集可选硬件（§5.2，官方口径「Parameters, links, etc. are for **reference only**」） | 双目 **60 FPS / 125° FOV / 60 mm baseline**；或双目 **30 FPS / 125° FOV / 60 mm baseline**；腕部 **RealSense D405 ×2**（+ USB3.0 hub）；腕部单目 **60FPS / 160° FOV ×2**；头壳两种尺寸 **Classic Head (98mm) / Renewed Head (88mm)**；支架注明适配 **M4010 wrist motor** | `Device.md` 行 74-246 | 官方仓库文件 |
| 运动模式限制（原文） | "Note: Only `Regular mode` (R1+X) is supported, `Running mode` (R2+A) is not supported."；安全：右控 A = 退出遥操作，双摇杆按下 = 软急停（切阻尼模式）"max speed is limited in the code" | `README.md` 行 236、471-477 | 官方仓库文件 |
| 退出行为（原文） | "In **Debug Mode**: After pressing the exit key, both arms will return to the robot's **initial pose** within **5 seconds**… In **Motion Mode**: … within 5 seconds" | 行 487-489 | 官方仓库文件 |
| Dex1 内置走线的限制（原文） | "This mode controls the left and right grippers through motor indices **31 and 33** in the G1 low-level command… **Whether the internally wired grippers can be controlled through `rt/arm_sdk` has not yet been verified**; therefore, using `--motion` at the same time is currently unsupported." | 行 463 | 官方仓库文件 |
| 版本历史 | **v1.6 (2026.7.29)**：支持 H2、支持 R1（R1_A5/R1_A7）、BrainCo 控制器输入、默认改用 head-yaw-relative arm reference；v1.5 (2025.12.29) 仿真模式；v1.4 (2025.11.21) 图像服务换成 teleimager、支持 WebRTC；v1.3 (2025.10.14) IPC 模式 | `CHANGELOG.md`、`README.md` 行 39-45 | 官方仓库文件 |
| 录制数据去向（原文） | "Recorded data is stored in `xr_teleoperate/teleop/utils/data` by default, with usage instructions at this repo: **unitree_IL_lerobot**" | 行 358 | 官方仓库文件（README 仍写旧仓库名） |
| 引用元信息 | BibTeX `year = {2024}`, `note = {Accessed: 2026-02}` | 行 557-564 | 官方仓库文件 |
| 子模块 | `teleop/robot_control/dex-retargeting`、`teleop/teleimager`、`teleop/televuer`（三个 gitlink，见 `.gitmodules`） | 文件树 | 官方仓库文件 |

### B2. `unitree_lerobot`（＝ `unitree_IL_lerobot`，同一仓库）

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| 名称 | `unitree_IL_lerobot` **重定向到 `unitree_lerobot`，HEAD 同一 commit `41c28057…`** | `git clone` 实测 | 官方仓库文件 |
| 许可证 | **Apache-2.0**；`Copyright [2024] [… ("Unitree Robotics")]`；`pyproject.toml` `license = { text = "Apache-2.0" }`、`version = "0.3.0"`、`requires-python = ">=3.10,<3.11"` | `LICENSE`、`pyproject.toml` | 官方仓库文件 |
| 定位（原文） | "This repository is used for `lerobot training validation`(Supports LeRobot datasets version **2.0 and above**.) and `unitree data conversion`." | `README.md` 行 41 | 官方仓库文件 |
| **pin 的 LeRobot 版本** | 原文：「The code in the `lerobot repository` for training; its corresponding **commit version number is `0878c68`**」（`README.md` 行 47 / `docs/README_zh.md` 行 26）。子模块 URL `https://github.com/huggingface/lerobot`（`.gitmodules`）。⇒ **README 的 commit 号与 pyproject 的 v0.3.0 不匹配同一时间点，属 README自陈** | 官方仓库文件 |
| **支持的策略（README 第 3 节逐条给命令）** | `--policy.type=` **`act`**、**`diffusion`**、**`pi0`**、**`pi05`**、**`groot`**（共 5 条训练命令示例）。pi05 额外要求 `--policy.pretrained_path=lerobot/pi05_base`、`compile_model=true`、`gradient_checkpointing=true`、`dtype=bfloat16`、`device=cuda`；groot 用 `--policy.tune_diffusion_model=false` | `README.md` 行 200-270 | 官方仓库文件 |
| Release Note 原文 | v0.3：「Update `lerobot dataset v3.0`」「More policy support(`pi05`, `groot`)」；v0.2：新增 brainco / inspire1 灵巧手的数据转换与模型部署、数据集回放、`unitree_sim_isaaclab` 仿真验证；v0.1：G1 + Dex1 + Dex3 | `README.md` 行 20-38 | 官方仓库文件 |
| 数据格式（两段） | ① **原始录制格式**：`datasets/<task_name>/episode_0001/{audios/, colors/, depths/, data.json}`；② **转换后** = Hugging Face **LeRobotDataset**（v2.1 或 v3.0） | 行 160-200 | 官方仓库文件 |
| 数据编辑器 | `data_editor/data_editor_EN.py` / `_CN.py`，需 `pip install PyQt5`；功能：**Trim Selected Range**、**Delete Current Episode** | 行 120-155 | 官方仓库文件 |
| `--robot_type` 全集（`constants.py` 的 `ROBOT_CONFIGS`，行 490-502） | `Unitree_Z1_Single`、`Unitree_Z1_Dual`、`Unitree_G1_Dex1`、`Unitree_G1_Dex1_Sim`、`Unitree_G1_Dex3`、`Unitree_G1_Brainco`、`Unitree_G1_Inspire`、`Unitree_G1_MoveibleLift_Dex1_UseWaist`、`Unitree_G1_MoveibleLift_Dex1_NoUseWaist`、`Unitree_G1_Lift_Dex1_UseWaist`、`Unitree_G1_Lift_Dex1_NoUseWaist`、`Unitree_Arm_L1` ⇒ **共 12 种；无 H1/H2/R1** | `unitree_lerobot/utils/constants.py` | 官方仓库文件 |
| 实机推理脚本 | `eval_robot/eval_g1.py`（真机）与 `eval_g1_sim.py`（仿真）；参数含 `--frequency=30`、`--arm="G1_29"`、`--ee="dex3"`、`--send_real_robot`、`--save_data`、`--max_episodes=1200` | README 行 275-320 | 官方仓库文件 |
| 直接加载的示例数据集 | `unitreerobotics/G1_Dex3_ToastedBread_Dataset`；默认下载位置 `~/.cache/huggingface/lerobot/unitreerobotics` | README 行 95-100 | 官方仓库文件 |

### B3. Hugging Face `huggingface.co/unitreerobotics` 数据集

API：`https://huggingface.co/api/datasets?author=unitreerobotics&limit=1000&full=true`，采集时刻 **2026-10-08**。分页核验：`limit=100→100`、`limit=500→200`、`limit=1000→200`、`skip=199→1 条`、`skip=200→0 条`。

| 项 | 值 | 分级 |
|---|---|---|
| **数据集总数** | **200** | 官方页面（HF API） |
| 按名字族 | **G1 系 191**（其中 `G1_WBT*` 59、`G1_Dex1_*` 约 120、`G1_Dex3_*`、`G1_Brainco_*` 等）、**Z1 系 6**（`Z1_StackBox_Dataset`、`Z1_Dual_Dex1_StackBox_Dataset`、`…_V2`、`Z1_Dual_Dex1_CleanupPencils_Dataset`、`Z1_Dual_Dex1_PourCoffee_Dataset`、`Z1_Dual_Dex1_FoldClothes_Dataset`）、**其它 3**（`unitree_model`、`unitree_sim_isaaclab_usds`、`RoboCupFootball_Dataset`） | 官方页面（HF API） |
| **H1 / H2 / R1 数据集** | **0 个**：200 个 id 里正则搜 `R1|H1|H2|HSR|humanoid` **无命中** ⇒ 「宇树公开的人形数据集实际上只有 G1（加少量 Z1 机械臂）」 | 官方页面（HF API） |
| 许可标注 | 逐个抓取 `cardData.license`（200 次单条 API）：**`apache-2.0` 64 个、无 license 字段 136 个**；`gated` 全部 **False**（200/200）、`disabled` 全 False | 官方页面（HF API） |
| 无 license 的 136 个主要是 | **44 个 `G1_WBT_*`** + **90 个 `G1_Dex1_<任务名>`（宇树 WLA/OneShot 系列长任务名）** + `unitree_model`。抽到有 license 的样本：`G1_Dex3_ToastedBread_Dataset`、`G1_Dex1_Stack_Block`、`G1_WBT_Brainco_Collect_Plates_Into_Dishwasher`、`G1_Dex1_DiverseManip_SingleArm_128x128`、`Z1_Dual_Dex1_StackBox_Dataset`、`G1_Dex1_MountCamera_Dataset`、`unitree_sim_isaaclab_usds` 均为 **apache-2.0** ⇒ **同一 org 内两种标注状态并存，属真实情况** | 官方页面（HF API） |
| **被 rl_lab 依赖的 `unitree_model`（USD 资产）没有 license 字段** | 而 `unitree_rl_lab/README.md` 第 43-46 行让使用者 `git clone https://huggingface.co/datasets/unitreerobotics/unitree_model`。**引用链上没有许可声明** | 官方页面 + 官方仓库文件 |
| 数据格式 | 抽样 `meta/info.json`：`G1_Dex3_ToastedBread_Dataset` → `codebase_version = v3.0`、`robot_type = Unitree_G1`、`fps = 30.0`、`total_episodes = 418`、`total_frames = 352022`、features 11 键；`G1_WBT_Inspire_Empty_Folder_In_Cabinet` → `codebase_version = v3.0`、`robot_type = unitree_g1_inspire`、`fps = 30`、`total_episodes = 200`、`total_frames = 264038`、features 46 键 | 官方仓库文件（HF raw） |
| tag 口径 | 有 license 的 64 个多带 `format:parquet`（60 个 `format:parquet`、2 个 `format:imagefolder`）；`modality:tabular/timeseries/video` | 官方页面（HF API） |
| 下载量 | 单页 `downloads` 求和（该字段是月度窗口值）：**183,128**；Top5：`G1_Dex3_ToastedBread_Dataset` 6813、`G1_Dex1_Stack_Block` 3055、`G1_WBT_Brainco_Collect_Plates_Into_Dishwasher` 2616、`G1_WBT_Inspire_Put_Clothes_into_Washing_Machine` 2481、`G1_Dex1_Wipe_Table` 2302 | 官方页面（HF API） |
| 时间跨度（抽样 createdAt） | `G1_Dex3_ToastedBread_Dataset` 2025-02-19（modified 2025-09-16）；`Z1_StackBox_Dataset` 2025-05-27；`G1_Dex1_DiverseManip_DualArm_256x256` 2026-03-18；`G1_WBT_Inspire_Empty_Folder_In_Cabinet` 2026-09-13；`unitree_model` 2025-07-14（modified 2026-05-20） | 官方页面（HF API） |

---

## C. UnifoLM 模型（「宇树的大脑」章）

### C1. `unifolm-wla`（UnifoLM-WLA-1.0）

| 项 | 值 | 来源（仓库文件路径 / URL） | 分级 |
|---|---|---|---|
| LICENSE 文件 | **存在**，11,538 B，正文是 **Apache License Version 2.0** 全文 | `unifolm-wla/LICENSE`（HEAD `0a1aa87`） | 官方仓库文件 |
| 许可声明（README 原文） | "Except where otherwise noted, this project is released under the **Apache License 2.0**. Third-party components remain subject to their original licenses." | `README.md` 行 77-80 | 官方仓库文件 |
| pyproject 许可 | `license = "Apache-2.0"`；`version = "1.0.1"`；`requires-python = ">=3.12,<3.14"`；`Development Status :: 3 - Alpha` | `pyproject.toml` | 官方仓库文件 |
| NOTICE | `UnifoLM-WLA / Copyright (c) 2016-2025 HangZhou YuShu TECHNOLOGY CO.,LTD. ("Unitree Robotics")`；含 starVLA、Qwen-Image 致谢 | `NOTICE` | 官方仓库文件 |
| 第三方许可清单 | **starVLA = MIT**；**Qwen-Image = Apache 2.0**；**OpenVLA = MIT**（具体文件 `unifolm_wla/training/trainer_utils/overwatch.py` 自述来自 OpenVLA） | `THIRD_PARTY_LICENSES.md` | 官方仓库文件 |
| **参数量** | **6B** — 原文 "next-generation general-purpose humanoid robot foundation model **with 6B parameters**" | `README.md` 行 15 | **README自陈（厂商口径）** |
| **训练数据小时** | **约 2,500 小时真机数据** — 原文 "**Trained on approximately 2,500 hours of high-quality real-robot data**" | 同上 | **README自陈** |
| **任务数** | **64 个任务** — 原文 "a single model coordinates **64 tasks** spanning desktop manipulation and whole-body manipulation" | 同上 | **README自陈** |
| 中文口径（同一页） | "宇树科技全面升级的新一代通用人形机器人基础模型，拥有 **6B 参数**…通过**约 2,500 小时**高质量真机数据训练，**单模型统筹 64 个任务**，覆盖桌面操作与全身移动操作，适配二指夹爪及多种五指灵巧手" | `README_zh.md` 行 15 | **README自陈** |
| 末端 | "supports two-finger grippers and multiple five-finger dexterous hands" | `README.md` 行 15 | README自陈 |
| 发布日期 | News 四条：**Sep 28, 2026** 发布 `UnifoLM-WLA-1.0-Base` + 微调代码；**Sep 20, 2026** 发布模型模块与 action expert 训练代码；**Sep 11, 2026** 发布 `UnifoLM-ER-1` 权重；**Sep 11, 2026** 发布 `UnifoLM-ER-Flow` 权重 | `README.md` 行 33-36 | 官方仓库文件 |
| Citation year | `@misc{unifolm-wla-1.0, author={Unitree}, title={UnifoLM-WLA-1.0: One Model Driven, Whole-Body Coordination}, year={2026}}` | 行 61-65 | 官方仓库文件 |
| 权重/数据集入口 | HF collection `unifolm-wla-10`；模型 `UnifoLM-WLA-1.0-Base`、`UnifoLM-ER-1`、`UnifoLM-ER-Flow`；数据集 collection `UniBot-V1 Challenge Dataset`、`UnifoLM-WBT-Dataset`、`UnifoLM-Dex1-Dataset`（链接给的 collection slug，**不等于单个 dataset id**） | 行 41-51 | 官方仓库文件 |
| 结构 | VLM 骨干走 `unifolm_wla/model/modules/vlm/QWen3.py`；动作头 `model/modules/action_model/` 下有 `DiT_modules/mmdit.py`、`MMDiT_ActionHeader.py`、`flow_matching_head/{action_encoder,cross_attention_dit}.py`；训练入口 `unifolm_wla/training/train_unifolm_wla.py`；DeepSpeed ZeRO-2/3 配置；微调脚本 `examples/unifolm_wla/train_files/run_{finetune,lora_finetune}_mmdit_frozen_vlm.sh`、`run_multi_source_train_mmdit_from_scratch.sh`；训练配置 `config/training/mmdit_finetune_frozen_vlm.yaml`、`mmdit_lora_frozen_vlm.yaml`、`unifolm_wla_pretrain_multisource.yaml` | 文件树 | 官方仓库文件 |
| 依赖（关键 pin） | `transformers==5.5.3`、`accelerate==1.13.0` | `pyproject.toml` | 官方仓库文件 |
| 多源数据适配 | `dataloader/multi_source_dataset/configs/unitree.yaml`、`stats/stats.json`、`stats/relative_stats.json`；含 **SE(3) 工具** `se3_utils.py`、FPS 采样 `fps_utils.py` | 文件树 | 官方仓库文件 |
| 部署侧 | `model_server/action_server_wbc_msgpack_unitree.py`、`unifolm_wla_action_adapter.py`、`tools/msgpack_numpy.py`（**WBC + msgpack**） | 文件树 | 官方仓库文件 |
| **仓库内未给** | 参数量的**结构拆解**、评测基准的**分数表**、2,500 h 的**任务/机器人构成**、训练算力/GPU 数 | — | 见 F 节 |
| ⚠ 措辞冲突 | `NOTICE` 版权行写 **2016-2025**，而 README 的新闻与 Citation 全是 **2026** | 两文件 | 官方仓库文件（并列） |

### C2. `unifolm-world-model-action`（UnifoLM-WMA-0）

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| LICENSE 文件 | **存在**，21,369 B，正文首行 **"Attribution-NonCommercial-ShareAlike 4.0 International"**，第 3 行 `Copyright (c) 2016-2025 HangZhou YuShu TECHNOLOGY CO.,LTD. ("Unitree Robotics")` ⇒ **CC BY-NC-SA 4.0（禁止商用）** | `unifolm-world-model-action/LICENSE`（HEAD `3e198de`） | 官方仓库文件 |
| **⚠ 同仓库许可自相矛盾** | `pyproject.toml` 写 **`license = { text = "BSD-3-Clause" }`**，与 LICENSE 文件的 **CC BY-NC-SA 4.0** 不一致。⇒ 书里若引用"UnifoLM 可商用"就是**讲错**；两个都是官方文件，必须并列 | `LICENSE` vs `pyproject.toml` | 官方仓库文件 |
| 版本 | `name = "unifolm_wma"`, `version = "0.0.1"`；`requires-python = "==3.10.18"`（严格等号）；`authors = Unitree Embodied AI R&D Team` | `pyproject.toml` | 官方仓库文件 |
| 定位（原文） | "**UnifoLM-WMA-0** is Unitree's open-source **world-model–action** architecture spanning multiple types of robotic embodiments… Its core component is a world-model… provides two key functions: (a) **Simulation Engine** – operates as an interactive simulator to generate synthetic data for robot learning; (b) **Policy Enhancement** – connects with an action head and, by predicting future interaction processes with the world-model, further optimizes decision-making performance." | `README.md` 行 14 | README自陈 |
| **参数量** | **仓库内未声明任何参数量**（README/README_cn/configs 全文无 parameter/B/亿 之类口径）；configs 只有 `in_channels: 8 / in_channels: 3` 等结构参数 | `configs/{train,inference}/*.yaml` | — |
| **训练数据小时** | **未声明** | — | — |
| **任务数** | **未声明具体数字**。只列 **5 个**用于实验的开源数据集（Z1_StackBox、Z1_DualArm_StackBox、Z1_DualArm_StackBox_V2、Z1_DualArm_Cleanup_Pencils、G1_Pack_Camera） | `README.md` 行 62-70 | 官方仓库文件 |
| 发布日期 | News 两条：**Sep 15, 2025** 发布训练/推理代码 + `UnifoLM-WMA-0` 权重；**Sep 22, 2025** 发布与 Unitree 机器人配合的**部署代码** | `README.md` 行 27-29 | 官方仓库文件 |
| 开源计划 | Training / Inference / Checkpoints / Deployment 四项全 `[x]` | 行 31-36 | 官方仓库文件 |
| 权重两个 | `UnifoLM-WMA-0-Base`（"Fine-tuned on **Open-X** dataset"）、`UnifoLM-WMA-0-Dual`（"Fine-tuned on **five Unitree opensource dataset** in both decision-making and simulation modes"） | 行 55-58 | README自陈 |
| 数据格式 | 原文 "first to have the data following the **Huggingface LeRobot V2.1** dataset format" | 行 72 | 官方仓库文件 |
| 额外数据集 | 4 个 `G1_Dex1_DiverseManip_{Dual,Single}Arm_{256x256,128x128}`；原文："**Each episode lasts approximately 30 seconds**. Available image resolutions: **256×256 and 128×128**"，G1 + 7-DOF dexterous arm | 行 68-75 | README自陈 |
| 依赖（关键 pin） | `torch==2.3.1`、`torchvision==0.18.1`、`transformers==4.40.1`、`pytorch-lightning==1.9.3`、`diffusers==0.30.2`、`xformers==0.0.27`、`numpy==1.24.2`、`gradio==4.39.0`、`open-clip-torch==2.22.0`、`kornia==0.7.3`、`decord==0.6.0`、`einops==0.8.0`、`tensorflow-graphics==2021.12.3`、`fairscale==0.4.13` | `pyproject.toml` | 官方仓库文件 |
| 部署 | `unitree_deploy/` 目录存在；安装需 `conda install pinocchio=3.2.0`、`ffmpeg=7.1.1`，并 `pip install -e external/dlimp`（子模块） | `README.md` 行 37-52 | 官方仓库文件 |
| ⚠ README 内链不一致 | README 里的配置链接写成 `github.com/unitreeerobotics/**unitree-world-model**/blob/main/configs/train/config.yaml`（另一个仓库名），与本仓库名不符 | `README.md` 行 131 | 官方仓库文件 |

### C3. UnifoLM 家族清点（GitHub Search API 实测）

`https://api.github.com/search/repositories?q=org:unitreerobotics+unifolm` → **total_count = 3**。宇树 org 下含 "unifolm" 的公开仓库共 **3 个**（本次取到名字的 2 个：`unifolm-world-model-action`、`unifolm-wla`；第 3 个本次未记录名字，需复核）。另：`www.unitree.com` 各页脚出现 **"Unifolm OS"** 词条（页面导航文本，非仓库）。

---

## D. 电池 / 功耗 / 安全（瓶颈章）

### D1. G1 / H1 / H1-2 / H2 / R1 电池与充电器（官方页面 + 文档中心）

| 机型 | 串数（cell count） | 容量 | 能量 | 最高/充电电压 | 充电器电流 | 标称续航 | 电池块数 | 来源 | 分级 |
|---|---|---|---|---|---|---|---|---|---|
| **G1 / G1 EDU** | **"13 string lithium battery"**（Power Supply 行） | **9000 mAh** | **页面未给 Wh**（13S × … 不自行折算） | 文档中心规格表未给电压；**充电器 54V** | **5 A**（Charger 54V 5A） | **About 2h**（Battery Life） | 1（快拆） | `www.unitree.com/g1`；doc-cdn `11/223` 行 297/304/305 | 官方页面 / 官方页面(文档中心) |
| **H1** | **未给串数** | **15 Ah** | **0.864 KWh**（宣传块 "Battery capacity: 864Wh, quickly replaceable"） | **Max Voltage 67.2 V**（不是充电电压，是最高电压） | **未给** | **页面与文档中心均未给整机续航小时数**（"Endurance" 行只填了容量 864Wh） | **2 块**（Quick Start 原文 "Insert the **2 batteries** into the battery slot"；"Short-press the power button of the **two** batteries once at the same time"） | `www.unitree.com/h1`；doc-cdn `10/166:152`；`10/168` | 官方页面 / 官方页面(文档中心) |
| **H1-2** | 未给 | **15 Ah** | **0.864 KWh** | Max Voltage **67.2 V** | 未给 | 未给 | 未给（同 H1 表述） | doc-cdn `10/271:154` | 官方页面(文档中心) |
| **H2 / H2 EDU** | 未给；类型原文 **"Premium Lithium Battery with Low Internal Resistance"** | **15 Ah** | **0.972 KWh** | **Maximum Voltage: 75.6 V**；对外直连电池口电压范围 **54–75.6 V** | 充电器一栏只写 **YES**（无数值） | **About 3h** | 未给 | `www.unitree.com/H2`；doc-cdn `25/1061` 行 42-58 | 官方页面 / 官方页面(文档中心) |
| **R1 AIR / Basic / EDU** | **未给** | **未给**（无 mAh/Ah） | **未给** | **未给** | 充电器一栏只写 **Yes**（无数值） | **Approx. 1h**（三档同） | 未给（快拆电池 Yes） | `www.unitree.com/R1`；doc-cdn `27/1135` 行 254/261/262/264 | 官方页面(文档中心) |

> 换算提示（**不作为事实，仅作核对线索**）：13S × 4.2 V = 54.6 V ≈ G1 充电器 54 V；G1 若按 54 V × 9 Ah ≈ 486 Wh，但**官方从未写这个 486 Wh**，引用时需注明是推算。

### D2. 整机的「峰值 / 平均功率」

| 问题 | 结论 |
|---|---|
| 官方页面是否为 G1/H1/H2/R1 **整机**给出 peak / average 电功率（W）？ | **没有。** 四张页面的规格表里 "Power" 一词只出现在 **Basic Computing Power / High Computing Power Module / Control and Perception Computing Power**（都是算力，不是电功率），以及宣传语 "extremely powerful power"。 |
| 官方文档中心是否给出？ | **没有整机功耗行。** 唯一接近的是 **H2 的电接口注记**（原文）：「The total power of the above **external power output** ports (excluding the direct battery power output) shall not exceed **500 W**」，以及直连电池口 **54–75.6 V / 10 A 额定**；R1 对外供电 **24 V/3 A、36 V/5 A**；H2 的 Jetson 模块自身 **40 W~130 W**（Thor）/ **10 W~25 W**（Orin NX），这是**算力模块**功耗不是整机。 |
| 关节级峰值力矩（不是功率） | 见【前表】C3/B6，四套口径并列。 |
| 灵巧手（部件级） | Dex3-1「The Maximum Power Is: **400W@3s**」（【前表】B5 已录）⇒ 官方对手部给过瞬时电功率，对**整机**没有。 |
| 四足对照 | AS2/B2 等页面同样只给算力与续航；未取到整机 W 数。 |

### D3. IP 防护等级 / 工作温度 / 安全认证 —— **「官方未发布」本身就是一条事实**

| 问项 | 结论（检索范围与证据） |
|---|---|
| **G1 / H1 / H1-2 / H2 / R1 整机 IP 防护等级** | **未发布。** 已逐页 grep：4 个产品页（`/g1` `/h1` `/H2` `/R1`）、5 个文档中心 About 页（`11/223`、`10/166`、`10/271`、`25/1061`、`27/1135`）、4 个 Operation Guide / Quick Start（`11/227`、`10/168`、`25/1102`、`27/1144`）、G1 FAQ（`11/242`，15,729 B 里 `IP数字` 0 命中）、G1 Debugging Specification（`11/241`）、G1 Common Mistakes（`11/308`）、H2 Debugging（`25/1260`）。命中的 "IP" 全是 **IP 地址**（`IP：192.168.123.120` 等）。**"IP44/IP54/IP65/IP67" 字样在人形相关官方页面中一处都没有。** |
| **人形整机工作温度范围** | **未发布（除一个部件）。** 唯一 `℃` 命中是 **H2 双目相机** 的 `Operating temp. −20 to +60℃ / −30~+70℃`（部件级，非整机）。G1/H1/R1 的 About 页与 Quick Start 均无温度行。 |
| **CE / CR / ISO 10218 / ISO 13482 / FCC / UL / CCC** | **未发布。** 同一批页面 grep `certif`、`ISO `、`\bCE\b`、`FCC`、`UL`、`regulat` 均 **0 命中**。 |
| 官方给出的**唯一**安全相关表述 | ① 文档中心 G1 脚注 [8]（原文）：**"This product is a civilian robot. We kindly request that all users refrain from making any dangerous modifications or using the robot in a hazardous manner."**；② G1 脚注 [6]（原文，注意官网中文机翻痕迹）："The humanoid robot has a complex structure and **extremely powerful power**. Users are asked to keep a sufficient safe distance…"；③ G1 脚注 [9]："Please visit Unitree Robotics Website for more related terms and policies, and **comply with local laws and regulations**."；④ H1/G1 Quick Start：**"Please use the protective rack to hang the G1/H1 to ensure safety"**（必须用保护架吊装）；⑤ R1 文档给出**外接急停口**定义（`External E-Stop Pin No.（左到右）= 1: STOP / 2: NC / 3: GND`）——这是官方唯一的硬件安全接口规格；⑥ xr_teleoperate 的红色 Warning 清单（保持安全距离 / A 键退出 / 双摇杆=软急停）。 |
| 已发布的唯一器件级认证 | **L1/L2 激光雷达**：`Human eye safety level = Class 1 (IEC60825-1:2014) Human eye safety`；抗眩光 `>100Klux`；`Operating environment Indoor/outdoor`。**Livox Mid-360S / Mid-360L**：`IP67`、`Operating Temperature −20°C to 55°C`（360S）/ `−20°C to 65°C`（360L）、`Laser Safety Class 1 (IEC60825-1:2014)` ⇒ **对比之下，宇树机器人本体的 IP 与温度是空白**。 |
| **保修期（官方页面表格行，已发布）** | G1 **8 months** / G1 EDU **18 months**；H2 **8 Months** / H2 EDU **12 Months**；R1 AIR **6 Months** / R1 **8 Months** / R1 EDU **12 Months**；**H1 与 H1-2 页面没有 Warranty Period 行**（`www.unitree.com/h1` 全文无 "Warranty"）；部件：IM6014 **3 month**（产品页）。三处脚注措辞均为 "For more detailed warranty terms, please read/refer to the product warranty brochure / Product Warranty Manual" ⇒ **细则不在网页上**。 |
| **热插拔免责（原文）** | H1 与 H1-2 文档 About 页：**"Hot swapping may cause equipment failure, and such failures are not covered under warranty."** |
| **MTBF / 使用寿命 / 设计寿命** | **完全未发布。** 全部检索页面 grep `MTBF`、`lifetime`、`operating hours`、`design life` ⇒ 人形相关 0 命中（`life` 只命中 `Battery Life`）。 |

### D4. 电池相关的商城与配件价

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| R1 Battery | **$500.00 USD** | `shop.unitree.com/collections/all` | 官方页面（商城） |
| Go2 Battery | $500.00 USD；Unitree Go1 Battery 出现 $850.00 / $600.00 两个价 | 同上 | 官方页面（商城） |
| **G1 / H1 / H2 电池单卖** | **商城无对应商品条目**（`collections/all` 里含 "Battery" 的只有上面 3 条） | 同上（2026-10-08 抓取，该视图枚举 23 个商品条目） | 官方页面（商城） |
| `shop.unitree.com/products.json` | **HTTP 429**（本次仍被限流） | — | — |

---

## E. 读者可以自己复现的开源参考实现（结语 12 个月计划章）

### E1. moteus（mjbots）

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| 最新版本 | GitHub `releases/latest` → **`rust/v0.5.5`**；`CHANGELOG.md` 按组件独立发版：**firmware 1.1.1 — 2026-08-04**（"Unreleased" 之上最新条目） | `https://github.com/mjbots/moteus/releases/latest`；`CHANGELOG.md` | 官方仓库文件 / 官方页面 |
| 许可证 | **Apache License 2.0**（仓库根 `LICENSE` 首两行 "Apache License / Version 2.0, January 2004"） | `moteus/LICENSE` | 官方仓库文件 |
| MCU | README 规格表 CPU 行 = **STM32G4**（原文 `CPU | STM32G4 | - | - | -`） | `README.md` | 官方仓库文件 |
| 通信 | **`5Mbps CAN-FD`**（Communications 行，r4.11 列） | `README.md` | 官方仓库文件 |
| **控制环频率** | **`Control Rate | 15-30kHz`**（r4.11） | `README.md` | 官方仓库文件 |
| PWM 开关频率 | **`PWM Switching Rate | 15-60kHz`**；`docs/reference/theory.md` 行 11："the switching frequency (**by default 30kHz**)" | 两文件 | 官方仓库文件 |
| 电流能力 | r4.11：Uncooled phase **12 A** / Cooled **32 A** / **Peak 100 A**；c1：5 / 14 / 20 A；n1：9 / 26 / 100 A；x1：25 / 62 / 120 A | `README.md` | 官方仓库文件 |
| 电压 / 峰值电功率 | r4.11：**10-44 V，Peak Electrical Power 900W @ 30V**；c1：10-51 V，250W @ 28V；n1：10-54 V，**1.3kW @ 36V**；x1：10-54 V，1kW @ 36V | `README.md` | 官方仓库文件 |
| 质量 / 尺寸 | r4.11 **14.2 g**、46×53 mm；c1 8.9 g、38×38×9 mm；n1 14.6 g、46×46×8 mm；x1 23.8 g、56×56×10 mm | `README.md` | 官方仓库文件 |
| 目录结构（读者要复刻的层次） | `hw/controller/`(r4.11 PCB)、`hw/c1`、`hw/n1`、`hw/x1`、`fw/`(无刷控制固件)、`lib/`(客户端)、`utils/`(诊断)、`tools/`(bazel) | `README.md` | 官方仓库文件 |
| 作者自述风险（原文） | "**WARNING**: This is not just a software project. It includes designs for moderately high power electronics. It has not yet burned down my (or anyone's that I know of) house, but there are no guarantees." | `README.md` | 官方仓库文件 |
| 销售渠道 | "Assembled and tested boards can be purchased at: https://mjbots.com"（**页内未列单价**） | `README.md` | 官方仓库文件 |
| 依赖注 | 最新提交 `8f747f4` "Upgrade to a newer mjlib"（2026-09-27）；构建用 Bazel + CMake 双轨 | `git log` | 官方仓库文件 |

### E2. ODrive

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| 最新 release | **`fw-v0.5.6`**（`releases/latest` 重定向）；`CHANGELOG.md` 顶部 `## [0.5.6] - **2023-04-29**` | `github.com/odriverobotics/ODrive/releases/latest`；`CHANGELOG.md` | 官方仓库文件 / 官方页面 |
| **⚠ release 与 main 不同步** | 仓库 HEAD 是 2026-01-20 的提交（`3a2e4dd` "update deprecated action dependencies"），但**最新正式 release 仍是 2023-04-29 的 v0.5.6**；v0.5.2-rc1/rc2 等 rc 标签仍在。⇒ 书写"ODrive 当前版本"时要说清是 release 还是 main | `git log` + `git ls-remote --tags` | 官方仓库文件 |
| 许可证 | **MIT License**（`Copyright (c) 2016-2018 ODrive Robotics`） | `LICENSE.md` | 官方仓库文件 |
| MCU | **`Firmware/MotorControl/main.cpp:19`  `#if defined(STM32F405xx)`**；板级目录 `Firmware/Board/v3/` ⇒ **v3.x 板用 STM32F405**。仓库内 **没有 v4/S1/Pro 的板目录**，故 **ODrive v4/S1/Pro 的 MCU 本次不可从官方仓库核实** | 两处仓库文件 | 官方仓库文件 |
| CAN | 官方文档原文：「It has low jitter and low latency, because there is no host computer. It is relatively fast (**CAN 2.0b supports 1 Mbps**）」；`docs/can-guide.rst` 速率表只有 **125 / 250 / 500 / 1000 kbps**（**无 CAN FD**） | `docs/can-guide.rst` 行 45、75-87 | 官方仓库文件 |
| **控制环频率** | `docs/control.rst` 原文：「the time difference between controller loops is a constant … **it is always 125 microseconds (8kHz)**」 | `docs/control.rst` 行 ~72 | 官方仓库文件 |
| 控制结构 | 官方口径是 **级联三环**：position(P) → velocity(PI) → **current(PI)**；原文 "The motor controller is a **cascaded style position, velocity and current control loop**"；`current_gain`/`current_integrator_gain` 由 `motor.config.current_control_bandwidth` **自动设定**；输出单位已改为 **扭矩 N·m**（`torque_constant` 换算） | `docs/control.rst` 行 11-60 | 官方仓库文件 |
| **⚠ 与宇树 IM6014 的架构对照（可作书内分析，但注意措辞）** | ODrive 文档明确说是**传统级联三环**；宇树 IM6014 文档明确说 **"are not the traditional cascaded three-loop architecture of servo drives, but rather parameter trimming based on a single hybrid control formula"**（见【前表】A2）。两者互为反例，可以并排讲 | 【前表】+ 本节 | 官方页面(文档中心) / 官方仓库文件 |
| 文档站 | `docs/` 在本仓库内是 `.rst` 源（sphinx），可直接引用；`docs/specifications.rst` 基本是机械尺寸图与表格，**电性参数（电压/电流）不在此文件正文** | 文件树 | 官方仓库文件 |

### E3. LeRobot / SO-101

| 项 | 值 | 来源 | 分级 |
|---|---|---|---|
| LeRobot 最新 release | **v0.6.1**（`releases/latest`） | GitHub | 官方页面 |
| LeRobot 许可证 | **Apache License 2.0**（`Copyright 2024 The Hugging Face team`） | `lerobot/LICENSE` | 官方仓库文件 |
| SO-101 官方文档 | `docs/source/so101.mdx`（同目录另有 `so100.mdx`）；官方措辞 "we explain how to assemble our flagship robot, the SO-101"、"from **affordable arms** like the SO-ARM101 to full humanoids" | 两文件 | 官方仓库文件 |
| **BOM 出处（关键）** | **LeRobot 文档本身不给价**：`so101.mdx` 原文 "Follow this **[README](https://github.com/TheRobotStudio/SO-ARM100)**. It contains the **bill of materials**, with a link to source the parts" ⇒ 价格必须引上游仓库 | `docs/source/so101.mdx` | 官方仓库文件 |
| **BOM 总价（上游 README 表，2026-10-08 抓到）** | **Leader + Follower 全套：US $229.88 ／ EU €226.3 ／ 中国 ￥1343.16 ／ 日本 ￥44,530**；**Follower 单臂：US $121.94 ／ EU €124.3 ／ ￥682.23 ／ ￥24,414** | `https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/README.md`（行 77-102） | 官方仓库文件（第三方上游） |
| BOM 明细（US 单价） | STS3215 舵机（7.4V）：全套 **7 个 1/345 (C001) + 2 个 1/191 (C044) + 3 个 1/147 (C046)**，单只 **$13.89**（EU €12.2 / ￥97.72 / ￥2,980 JPY）；Motor Control Board（Waveshare）**$10.6** ×2；USB-C 线 $7；电源 $10 ×2；台夹 $9；螺丝刀 $6。**注意表头自注 "prices and items may vary depending on geographic location"，且含螺丝刀等非零件项，与"纯 BOM"不等** | 同上 | 官方仓库文件 |
| 减速比（SO-101 follower/leader） | follower **6× STS3215 with 1/345 gearing**；leader 六轴分别 **1/191（base/shoulder pan、elbow flex）、1/345（shoulder lift）、1/147（wrist flex、wrist roll、gripper）**，原文理由 "to make sure it can both sustain its own weight and it can be moved without requiring much force" | `docs/source/so101.mdx` | 官方仓库文件 |
| 通信 / 电机总线 | 舵机为 **Feetech 总线舵机**，需 `pip install -e ".[feetech]"`；每只舵机需设唯一 id 与一致波特率（README 有专节；**页内未给具体波特率数值**） | `so101.mdx` | 官方仓库文件 |
| **官方支持的策略清单（v0.6.1 实测）** | `docs/source/` 下策略文档共 **19** 篇：**act, diffusion, dm05, evo1, fastwam, fineart_vla, groot, lawam, molmoact2, multi_task_dit, pi0, pi05, rtc, sarm, smolvla, tdmpc, vla_jepa, vqbet, walloss** | `docs/source/policy_*_README.md` | 官方仓库文件 |
| 代码侧策略包 | `src/lerobot/policies/` 下含 act、diffusion、dm05、evo1、fastwam、fineart_vla、groot、lawam、molmoact2、multi_task_dit、pi0、pi05、pi0_fast、rtc、smolvla、tdmpc、gaussian_actor、lingbot_va、factory 等 | 文件树 | 官方仓库文件 |
| 数据集格式 | **LeRobotDataset**：原文 "Every dataset uses the standardized LeRobotDataset format (**synchronized video + action/state data**) and can be streamed directly from the Hugging Face Hub"；v3 说明见 `docs/source/lerobot-dataset-v3.mdx`（含「DROID converts in 34 minutes」等） | `docs/source/index.mdx`、`lerobot-dataset-v3.mdx` | 官方仓库文件 |
| 训练节奏实测值（可引用的硬数字） | `docs/source/il_robots.mdx` 原文样例：target **30 Hz（33.3 ms budget per tick）**，实测 **29.88 Hz**，**16/1198 ticks 超时（1.3%）**，work mean **18.4 ms** / worst **45.1 ms**，`observe` 占循环工作 **74%**、worst **40 ms**；并警告 "a session that ran at 25 Hz still produces a dataset that _claims_ 30" | `docs/source/il_robots.mdx` 行 420-434 | 官方仓库文件 |
| 其他价格线索（同页可引） | `docs/source/openarm.mdx` 原文 "**$6,500 USD** for a complete bimanual system" | 官方仓库文件 |

### E4. Livox Mid-360（G1/H1/H1-2 用的补盲雷达）

**⚠ 现状（2026-10-08 实测）**：`livoxtech.com/mid360` 与 `/cn/mid360` **均 404**；首页产品栏只有 `/mid-360l`、`/mid-360s`、`/mid-70`。⇒ **原版 "Mid-360" 已从官网产品目录撤下**；书里若写"官方在售 Mid-360"需按本节口径核对。宇树文档中心对它的称呼是 **LIVOX-MID360**（【前表】B1）与 **MID-360**（H1/H1-2）。

| 项 | **Mid-360S** | **Mid-360L** | 来源 |
|---|---|---|---|
| FOV | Horizontal **360°**，Vertical **−7°~52°**（typical）；宣传口径 **360°×59°** | Horizontal **360°**，Vertical **−10°~34°**（typical）；宣传口径 **360°×44°** | `livoxtech.com/mid-360{s,l}/specs`（官方页面） |
| **点频 Point Rate** | **200,000 points/s (first return)** | **100,000 points/s (first return)** | 同上 |
| Frame Rate | **10 Hz (typical)** | **10 Hz (typical)** | 同上 |
| 测距 | **40 m @10%** reflectivity (typical, @100 klx)；cut-off **100 m**；盲区 **0.1 m**（0.1–0.2 m 数据仅供参考） | **45 m @10%**；cut-off **100 m**；盲区 **0.1 m** | 同上 |
| 精度 | Range precision (1σ) **≤2 cm @10 m**、**≤4 cm @0.2 m**；Angular Precision 栏**页内空白** | **≤3 cm @10 m**、**≤5 cm @0.2 m**；Angular 栏空白 | 同上 |
| **IMU** | 原文 **"Built-in IMU Model: ICM40609"** — **官方页未给 IMU 采样率** | 同：**ICM40609**，无采样率 | 同上 |
| 激光安全 / 波长 | **Class 1 (IEC60825-1:2014)**；**905 nm**；发散角 25.2°(H)×8°(V) FWHM；最大激光功率"可能超过 70 W" | Class 1 (IEC60825-1:2014)；905 nm；发散角 **9°×22°**；>65 W | 同上 |
| **IP 等级 / 工作温度** | **IP67**；**−20 °C to 55 °C** | **IP67**；**−20 °C to 65 °C** | 同上 |
| 功耗 / 供电 | **6.5 W**；**9~27 V DC**；注：−20~0 °C 时自动进入自加热，**峰值功率可达 14 W** | **4.2 W**；**12~27 V DC** | 同上 |
| 尺寸 / 质量 | 65×65×60 mm / **265 g** | 65×65×63 mm / **245 g** | 同上 |
| 数据口 / 同步 | **100 BASE-TX Ethernet**；**IEEE 1588-2008 (PTPv2), GPS**；抗干扰 Available | 同 + GPS 描述为 (UTC time + PPS pulse) | 同上 |
| **官方价格** | **未取到**：产品页与 specs 页无价格，`/store` **404**；Mid-70 页有 "Buy Now" 入口，Mid-360 系列页无 | 同 | — |

### E5. Unitree 自研 4D LiDAR L1 / L2（`www.unitree.com/LiDAR`、`/L2`）

| 项 | **L1** | **L2** | 备注 |
|---|---|---|---|
| 官方价 | **From $249**（L1 PM）；**L1 RM From $309** | **$419** | 与商城一致（商城：`Unitree 4D LiDAR L1` $249 / $309；`L2` $419） |
| FOV | **360° × 90°** | **360° × 96°** | 页内宣传块 |
| 采样频率 / 有效频率 | **Sampling 43200 points/s ／ Effective 21600 points/s** | **Sampling 128000 points/s ／ Effective 64000 points/s** | **两个是不同指标，不是冲突**；宣传块用的是 Effective（L1 21600、L2 64000），L2 页另有"较 L1 提升 200%"措辞 |
| 圆周 / 垂直扫描频率 | **11 Hz ／ 180 Hz** | **5.55 Hz（可定制调整）／ 216 Hz** | 官方表格行 |
| 测距 | L1 PM 20m@90% / 10m@10%；L1 RM 30m@90% / 15m@10% | **30 m@90%、15 m@10%** | — |
| 精度 / 距离分辨率 | 测量精度 **±2.0 cm**；距离分辨率 **8 mm** | 精度 **≤2.0 cm**；距离分辨率 **4.5 mm**（"较 L1 提升 78%"） | — |
| 盲区 | **0.05 m** | **0.05 m** | 对比表给竞品 0.1 m / 0.3 m |
| **IMU** | **3-axis acceleration + 3-axis gyroscope**（内置） | 同 | **采样率官方未给** |
| 通信 | **TTL UART** | **ENET UDP / TTL UART** | — |
| 4D 数据 | 3D position + 1D grayscale | 同（**supports 2D mode**） | — |
| 激光安全 | **Class 1 (IEC60825-1:2014) Human eye safety** | 同 | 这是人形配件里唯一官方认证表述 |
| 抗眩光 | **>100 Klux**（原文 "Achieve stable … under 100Klux outdoor light"） | 同 | — |
| 功耗 | **6 W** | **10 W** | 对比表：深度相机 5 W、广角 3D 雷达 12 W |
| 尺寸 / 质量 | **75×75×65 mm ／ 230 g** | **75×75×65 mm ／ 230 g** | — |
| 扫描方式 | Non-contact **brushless rotating mirror** scanning、非重复扫描 | 同 | — |
| SLAM 口径（原文） | "SLAM based on Unitree 4D LiDAR L1, **only use its pointcloud & built-in IMU, do not use other positioning sensors**" | "Utilize only L2 and its built-in IMU, without employing other positioning sensors, to map using the **POINT-LIO algorithm**" | 官方开源 SLAM |
| 对比表里的价格锚 | "A depth camera **$359** ／ A wide-angle 3D radar **$700+**"；L1 页原文 "**Achieving the same effect, with less than 1/10 of the price**" | L2 页同样表 | **厂商自陈的比价** |

---

## F. 未取到 / 不可核实（本次）

1. **`unitree_rl_lab` 的 rsl_rl 版本 pin**：仓库任何文件（`pyproject.toml`、`extension.toml`、`docker/Dockerfile`、`unitree_rl_lab.sh`）都**没有写 rsl_rl 的版本号或 commit**。只有 README 徽章 **IsaacSim 5.1.0 / IsaacLab 2.3.0**，属**徽章口径**而非依赖声明。rsl_rl 版本只能从 import 的类名（`RslRlPpoAlgorithmCfg`）反推为 4.x/5.x 时代，**不作为可印事实**。
2. **`unitree_rl_gym` 的 Isaac Gym 版本号**：`doc/setup_en.md` 只说"从 NVIDIA 官网下载 Isaac Gym"，**未写 Preview 3/4**。PyTorch pin 为 2.3.1，驱动建议 ≥525。
3. **G1-23dof 的训练配置**：当前 HEAD 无 `tasks/locomotion/robots/g1/23dof/`，也没有 `g1_23dof` 的 `policy/**/deploy.yaml`；**23dof 的 action_scale / step_dt 在 rl_lab 里取不到**（只有部署侧 FSM 增益）。
4. **`deploy/robots/g1_23dof/config/config.yaml` 里没有 `action_scale`、没有电机型号名、没有 `step_dt`** —— 指令预期的"逐关节 action_scale + 电机家族映射"在这个文件里**不存在**；能给的只有 FixStand kp/kd（见 A2 表）。
5. **H2 / R1 的 RL 训练与部署**：`unitree_rl_lab`、`unitree_rl_gym` 均**无任何 H2 / R1 环境或部署配置**（R1/H2 仅在 `xr_teleoperate` 的遥操作侧支持）。书里不能写"宇树发布了 H2/R1 的开源 RL 训练例程"。
6. **蒸馏（teacher-student）**：两仓库都**没有可跑的蒸馏流程**。rl_lab 只有 `DistillationRunner` / `algorithm.class_name == "Distillation"` 的**接口挂点**（`scripts/rsl_rl/{train,play}.py`），`train.py` 里实例化的仍然只有 `OnPolicyRunner`；rl_gym 全仓库 0 命中 distill/teacher/student。
7. **遥操作端到端延迟**：`xr_teleoperate` 未给任何 ms/帧延迟数值，只有 `--frequency` 默认 **30.0** 的循环周期。
8. **`unitree_sim_isaaclab` 的具体版本/任务清单**：本次未展开（xr_teleoperate README 给了示例任务名 `Isaac-PickPlace-Cylinder-G129-Dex3-Joint` 与 `--robot_type g129`，未核实该仓库版本 pin）。
9. **UnifoLM-WLA-1.0 的 6B / 2,500 h / 64 tasks 的可验证依据**：三个数**只出现在 README（英中双语）正文**，仓库里没有 config、权重清单、技术报告或评测表能独立核对；HF collection 页与 `UnifoLM-WLA-1.0-Base` 模型卡的参数量本次未抓取核对。⇒ 必须标注为 **厂商自陈**。
10. **UnifoLM-WMA-0 的参数量 / 训练小时数 / 任务数**：**仓库内完全未声明**。只有"Open-X 微调 Base"、"5 个数据集微调 Dual"、"episode 约 30 s"、"256×256 与 128×128"这几条。
11. **UnifoLM 两仓库的发布日期是否等于权重发布日期**：README 的 News 日期是仓库自述；未与 HF 侧 `createdAt` 交叉核验（`UnifoLM-*` 模型卡的 HF `createdAt` 本次未取）。
12. **G1 / H1 / H2 / R1 整机 IP 防护等级、整机工作温度范围、CE/CR/ISO 10218/ISO 13482/FCC/UL/CCC 认证**：**官方未发布**（检索范围见 D3，逐页 grep 为 0 命中）。这是"查不到"，不是"不存在于任何纸质材料"——官方脚注反复指向需要另行索取的 **product warranty brochure / 二次开发手册**。
13. **H1 / H1-2 的保修期**：`www.unitree.com/h1` 全文无 "Warranty"；文档中心 About_H1 / About_H1-2 亦无保修行。**H1 系列保修期：官方页面未发布。**
14. **整机 MTBF / 设计寿命 / 大修周期**：全部检索页面 0 命中。
15. **G1 / H1 / H2 / R1 的峰值 vs 平均电功率（整机）**：**未发布**；仅有 H2 对外供电 ≤500 W、直连电池 54–75.6 V/10 A、R1 对外 24 V/3 A 与 36 V/5 A、Dex3-1 400 W@3 s、Jetson 模组 40–130 W 等**部件/接口级**数字。
16. **R1 电池的容量、电压、串数**：官方页面与文档中心只写 "Lithium Battery"、"Smart Battery (Quick Release) Yes"、"Charger Yes"、"Battery Life Approx. 1h"（【前表】D-11 已记，本次复核仍无）。
17. **H1 的整机续航（小时）**：页面 "Endurance" 行填的是容量 864 Wh，文档中心无续航行。
18. **Livox Mid-360 原版规格页 / 官方价格**：`/mid360` 404；`/store` 404；Mid-360S / Mid-360L 页**不显示价格**。IMU 采样率两页都未给（只给型号 ICM40609）。
19. **Unitree L1 / L2 的 IMU 采样率**：官方页只写"3-axis acceleration + 3-axis gyroscope"，**无 Hz**。
20. **ODrive v4 / S1 / Pro 的 MCU 与 CAN-FD 支持**：`odriverobotics/ODrive` master 仓库里只有 `Firmware/Board/v3/` 与 STM32F405 条件编译；**新版硬件的 MCU/CAN 能力本次不可由官方仓库核实**。`docs/specifications.rst` 正文主要是机械尺寸，电性参数不在其中。
21. **SO-101 的官方价格**：LeRobot 不给价；上游 `SO-ARM100` 的 $229.88 / $121.94 是 **BOM 表求和**（含螺丝刀、台夹），且表头声明"价格与物件因地区而异"，**不是官方定价**。SO-ARM100 仓库本身的 license 本次 API 未取到（未核实）。
22. **`unitree_lerobot` README 里的 lerobot commit `0878c68`** 与 pyproject 版本号、与 `lerobot` v0.6.1 是否同一时间点，**未交叉核实**（README 自述值）。
23. **HF 无 license 字段的 136 个数据集，其正文是否另有许可声明**：仅抽查了 6 个（均 apache-2.0）；**未逐一读完 136 个 README**，所以「无 license 元数据」是 API 层面的事实，不等于「完全没有许可文字」。
24. **`github.com/unitsreerobotics` org 下 unifolm 仓库的第 3 个名字**：Search API `total_count=3`，本次只稳定取到 2 个名字，第 3 个未记录（需复核）。

---

## G. 来源清单

**官方仓库文件（GitHub raw，均以 §0 的 commit 为准）**
- `unitree_rl_lab/main`：`README.md` · `pyproject.toml` · `LICENCE` · `unitree_rl_lab.sh` · `docker/Dockerfile` · `docker/.env.base` · `source/unitree_rl_lab/pyproject.toml` · `source/unitree_rl_lab/config/extension.toml` · `source/unitree_rl_lab/docs/CHANGELOG.rst` · `…/assets/robots/unitree.py` · `…/assets/robots/unitree_actuators.py` · `…/tasks/__init__.py` · `…/tasks/locomotion/agents/rsl_rl_ppo_cfg.py` · `…/tasks/locomotion/robots/{g1/29dof,h1,go2}/{__init__.py,velocity_env_cfg.py}` · `…/tasks/mimic/agents/rsl_rl_ppo_cfg.py` · `…/tasks/mimic/robots/g1_29dof/{dance_102,gangnanm_style}/tracking_env_cfg.py` · `…/tasks/locomotion/mdp/observations.py` · `…/utils/export_deploy_cfg.py` · `scripts/rsl_rl/{train,play}.py` · `deploy/robots/{g1_23dof,g1_29dof,h1,h1_2}/config/config.yaml` · `deploy/robots/g1_29dof/config/policy/velocity/v0/params/deploy.yaml` · `deploy/robots/g1_29dof/config/policy/mimic/dance_102/params/deploy.yaml` · `deploy/robots/g1_23dof/include/Types.h` · `deploy/thirdparty/onnxruntime-linux-x64-1.22.0/VERSION_NUMBER`
- `unitree_rl_gym/master`：`README.md` · `LICENSE` · `legged_gym/LICENSE` · `doc/setup_en.md` · `legged_gym/envs/base/{base_config.py,legged_robot_config.py,legged_robot.py,base_task.py}` · `legged_gym/envs/{g1,g1,g1_2,h1,h1_2}/{h1,h1_2,g1}_config.py` · `legged_gym/envs/{g1,h1,h1_2}/*_env.py` · `deploy/deploy_real/configs/{g1,h1,h1_2}.yaml` · `deploy/deploy_mujoco/configs/*.yaml`
- `xr_teleoperate/main`：`README.md` · `LICENSE` · `CHANGELOG.md` · `Device.md` · `requirements.txt` · `teleop/teleop_hand_and_arm.py` · `teleop/utils/episode_writer.py`
- `unitree_lerobot/main`：`README.md` · `docs/README_zh.md` · `LICENSE` · `pyproject.toml` · `.gitmodules` · `unitree_lerobot/utils/convert_unitree_json_to_lerobot.py` · `unitree_lerobot/utils/constants.py` · `data_editor/data_editor_{EN,CN}.py`
- `unifolm-wla/main`：`README.md` · `README_zh.md` · `LICENSE` · `NOTICE` · `THIRD_PARTY_LICENSES.md` · `pyproject.toml` · `docs/*` · `unifolm_wla/**` · `model_server/**`
- `unifolm-world-model-action/main`：`README.md` · `README_cn.md` · `LICENSE` · `pyproject.toml` · `configs/{train,inference}/*.yaml` · `unitree_deploy/`
- `mjbots/moteus/main`：`README.md` · `LICENSE` · `CHANGELOG.md` · `docs/reference/theory.md`
- `odriverobotics/ODrive/master`：`LICENSE.md` · `CHANGELOG.md` · `docs/control.rst` · `docs/can-guide.rst` · `docs/specifications.rst` · `Firmware/MotorControl/main.cpp` · `Firmware/Board/v3/`
- `huggingface/lerobot/main`：`LICENSE` · `docs/source/{so101,so100,index,il_robots,lerobot-dataset-v3,openarm}.mdx` · `docs/source/policy_*_README.md` · `src/lerobot/policies/`
- `TheRobotStudio/SO-ARM100/main`：`README.md`（BOM 表）
- `unitreerobotics/unitree_IL_lerobot` → 重定向到 `unitree_lerobot`（同 HEAD）

**官方页面**
- 人形：https://www.unitree.com/g1 ｜ /h1 ｜ /H2 ｜ /R1 ｜ /LiDAR ｜ /L2 ｜ /opensource
- 文档中心（正文 Markdown）：`robot-api.unitree.com/doc/spaces2?locale=en`（空间清单，本次取到 **Humanoid Robot / Open Source Adaptation / Quadruped Robot / Robotic Arms / Components / Perception / SLAM Navigation** 七组共 26 个空间）；人形 About：`doc-cdn.unitree.com/11/223`（G1）· `10/166`（H1）· `10/271`（H1-2）· `25/1061`（H2）· `27/1135`（R1）；操作与调试：`11/227`（G1 Quick Start）· `11/241`（G1 Debugging）· `11/242`（G1 FAQ）· `11/308`（G1 Common Mistakes）· `10/168`（H1 Quick Start）· `10/195`（H1 FAQ）· `10/197`（H1 Debug Guide）· `25/1102`（H2 Quick Start）· `25/1260`（H2 Debugging）· `27/1144`（R1 Quick Start）
- 商城：https://shop.unitree.com/collections/all （电池与雷达价；`products.json` 仍 429）
- Hugging Face：`https://huggingface.co/api/datasets?author=unitreerobotics&limit=1000&full=true`（200 条）；单条 `api/datasets/unitreerobotics/<id>`；raw `datasets/unitreerobotics/<id>/raw/main/meta/info.json` 与 `/raw/main/README.md`
- GitHub API：`api.github.com/search/repositories?q=org:unitreerobotics+unifolm`（total_count=3）；`releases/latest` 重定向解析：`mjbots/moteus` → `rust/v0.5.5`、`odriverobotics/ODrive` → `fw-v0.5.6`、`huggingface/lerobot` → `v0.6.1`
- Livox：https://www.livoxtech.com/ ｜ `/mid-360s` ｜ `/mid-360s/specs` ｜ `/mid-360l` ｜ `/mid-360l/specs` ｜ `/mid-70` ｜（`/mid360`、`/cn/mid360`、`/store` = **404**）

**本地留存的抓取件（可复核，非发布物）**：`research/../repos/{unitree_rl_gym,unitree_rl_lab,xr_teleoperate,unitree_lerobot,unifolm-wla,unifolm-world-model-action,ext_moteus,ext_ODrive,ext_lerobot,il}/`（`--filter=blob:none` 浅克隆 + sparse-checkout，已排除 STL/USD/npz/onnx/so 等二进制）；`files/rl_lab/`、`files/rl_gym/`、`files/unitree/`（产品页与 doc-cdn 正文快照）、`files/hf_full.json`（200 条数据集原始 API 响应）、`files/hf_lic.json`（200 条逐条许可查询结果）、`files/livox_extract.txt`、`files/lidar_tables.txt`、`files/soarm100_readme.md`。