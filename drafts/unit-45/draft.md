# 附录 E：参考来源、抓取日期与「查不到」清单

> E.3 的 URL 清单由 `python tools/gen_appendix_e.py` 从 `drafts/`、`bible/`、`research/` 里收集生成，
> 其余小节（取法、「查不到」清单、冲突口径、不可采信清单）是作者的判断，逐条手写。分三段：
> ① 一手来源（官方页面 / 官方仓库文件 / 官方文档中心）；② 二手来源（拆解、研报、论文、媒体）；
> ③ **「查不到」清单**——本书认真找过但没有拿到答案的问题。第三段是本书最重要的部分之一。

## E.1 抓取日期

一手页面与仓库文件的抓取日期是 **2026-10-07 至 2026-10-08**；
**2026-10-09 对个别条目做过回读复核**（`unitree_rl_lab` 的 `LICENCE` 是否存在、moteus 的 README 与
`theory.md` 那三行、以及 `LICENSE`/`LICENCE`/`LICENSE.md` 三种名字在 13 个宇树仓库与 ODrive 上的实测），
逐条记在 `bible/sources.md` 与 `bible/do-not-touch.md` 第 27 条。
型号、价格、开源模型版本与仓库结构在 2026 年下半年变动极快；**发行前必须再做一次全量复核**。

## E.2 一手来源的取法（可复现）

```text
产品与商城：unitree.com/<型号>、unitree.com/cn/<型号>、shop.unitree.com
电机文档：  unitree.com/go1/motor（GO-M8010-6）、unitree.com/IM6014/、unitree.com/A1/motor
文档中心：  support.unitree.com 的前端是 SPA（直接抓只返回 768 字节空壳），但正文可匿名取：
            1) GET https://robot-api.unitree.com/doc/spaces2?locale=en
            2) GET https://robot-api.unitree.com/doc/?space=<SPACE>&locale=en
            3) GET https://doc-cdn.unitree.com/<space>/<id>/<locale>/<space>_<id>_<locale>
               → 返回原始 Markdown
官方仓库：  unitree_sdk2、unitree_ros、unitree_ros2、unitree_mujoco（MJCF 在 unitree_robots/ 下）、
            unitree_rl_gym、unitree_rl_lab、xr_teleoperate、unitree_IL_lerobot、
            unifolm-wla、unifolm-world-model-action、unilidar_sdk
```

**仓库勘误**：`unitree_mjcf` 与 `unitree_motors_sdk` 不存在（404）；`unitree_model` 只有 USD/DAE，不含 URDF/XML。

## E.3 已引用的 URL 清单（144 条，按字典序）

这一节由 `python tools/gen_appendix_e.py` 生成，收集范围是 `drafts/`、`bible/`、`research/`，
去重后按字典序排。规则很简单：**清单必须等于正文真的引用过的集合**——正文出现而清单漏掉的会被补上，
清单里有而正文已经查不到的会被移出，两种增减都会在生成时逐条打印，不存在“悄悄少了一条”。
条目在第一个中文字符处截断，所以不会再出现 `…/11_248_en（G1` 这种半截的行尾。

另有 **12 条**正文里出现的地址按规则**不进这张表**，因为它们不是“某一页文献”，生成时会逐条打印理由：

- **两条本机地址**：`192.168.123.164:60001`、`192.168.123.2:8012`——是读者在自己机器人上打开的控制台；
- **两条程序接口**：`api.github.com/search/…`、`huggingface.co/api/datasets?…`——返回内容随查询串变；
- **四条只有主机名**：`mjbots.com`、`livoxtech.com/`、`docs.quadruped.de`、`doc-cdn.unitree.com/`——站点首页，不是某一页；
- **两条 raw 仓库目录前缀**：`raw.githubusercontent.com/.../unitree_rl_lab/.../` 与 `.../unitree_rl_gym/master/`——
  raw 只发文件，列目录的地址打不开（这两条是研究笔记里当“取法前缀”用的，被正文引用时混了进来）。

反过来有一条边界要说清：**以 `/` 结尾不等于打不开**。`egh0bww1.com/posts/2023-10-24-unitree-go1-collection/`、
`mujoco.readthedocs.io/en/stable/computation/` 这类以斜杠结尾的地址是真页面（2026-10-09 实测 200），
所以生成器只按上面四类精确排除，不敢拿“结尾有没有斜杠”一刀切。它们留在各自的正文处，这里不冒充参考条目。

```text
https://arxiv.org/abs/2401.02117
https://arxiv.org/abs/2403.12945
https://arxiv.org/abs/2410.00425
https://arxiv.org/abs/2505.03233
https://arxiv.org/html/2410.24164v1
https://arxiv.org/html/2501.03575v3
https://arxiv.org/html/2503.06669v1
https://arxiv.org/html/2503.20523v1
https://arxiv.org/html/2508.05635v3
https://arxiv.org/html/2510.26742v1
https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=unitree&gsrnamespace=6
https://damodev.csdn.net/69782b327c1d88441d8fdca1.html
https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/
https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2025-Update.pdf
https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q4-2024-Update.pdf
https://doc-cdn.unitree.com/10/166/en/10_166_en
https://doc-cdn.unitree.com/10/271/en/10_271_en
https://doc-cdn.unitree.com/11/223/en/11_223_en
https://doc-cdn.unitree.com/11/248/en/11_248_en
https://doc-cdn.unitree.com/11/249/en/11_249_en
https://doc-cdn.unitree.com/11/251/en/11_251_en
https://doc-cdn.unitree.com/11/252/en/11_252_en
https://doc-cdn.unitree.com/25/1061/en/25_1061_en
https://doc-cdn.unitree.com/25/1123/en/25_1123_en
https://doc-cdn.unitree.com/27/
https://doc-cdn.unitree.com/27/1135/en/27_1135_en
https://doc-cdn.unitree.com/30/1371/en/30_1371_en
https://doc-cdn.unitree.com/30/1377/en/30_1377_en
https://doc-cdn.unitree.com/30/1378/en/30_1378_en
https://doc-cdn.unitree.com/30/1382/en/30_1382_en
https://doc-cdn.unitree.com/30/1383/en/30_1383_en
https://doc-cdn.unitree.com/8/106/en/8_106_en
https://doc-cdn.unitree.com/8/107/en/8_107_en
https://doc-cdn.unitree.com/8/1484/en/8_1484_en
https://docs.isaacsim.omniverse.nvidia.com/latest/
https://egh0bww1.com/posts/2023-10-24-unitree-go1-collection/
https://finance.sina.cn/2025-02-16/detail-ineksnuy4910269.d.html
https://github.com/Huuhuuw/FAST_LIO_LOCALIZATION_HU
https://github.com/MAVProxyUser/YushuTechUnitreeGo1
https://github.com/TheRobotStudio/SO-ARM100
https://github.com/abizovnuralem/go2_omniverse
https://github.com/abizovnuralem/go2_ros2_sdk
https://github.com/huggingface/lerobot
https://github.com/jizhang-cmu/autonomy_stack_go2
https://github.com/leggedrobotics/rsl_rl.git
https://github.com/legion1581/go2_firmware_tools
https://github.com/legion1581/unitree_webrtc_connect
https://github.com/mjbots/moteus/releases/latest
https://github.com/unitreerobotics/digital_servo
https://github.com/unitreerobotics/point_lio_unilidar
https://github.com/unitreerobotics/unifolm-vla
https://github.com/unitreerobotics/unifolm-world-model-action
https://github.com/unitreerobotics/unilidar_sdk2
https://github.com/unitreerobotics/unitree_actuator_sdk
https://github.com/unitreerobotics/unitree_guide
https://github.com/unitreerobotics/unitree_legged_sdk
https://github.com/unitreerobotics/unitree_lerobot
https://github.com/unitreerobotics/unitree_mjcf
https://github.com/unitreerobotics/unitree_motors_sdk
https://github.com/unitreerobotics/unitree_mujoco
https://github.com/unitreerobotics/unitree_rl_gym
https://github.com/unitreerobotics/unitree_rl_lab
https://github.com/unitreerobotics/unitree_ros
https://github.com/unitreerobotics/unitree_ros2
https://github.com/unitreerobotics/unitree_sdk2
https://github.com/unitreerobotics/unitree_sdk2_python
https://github.com/unitreerobotics/unitree_sim_isaaclab
https://github.com/unitreerobotics/xr_teleoperate
https://huggingface.co/datasets/unitreerobotics/unitree_model
https://k.sina.cn/article_7950358917_1d9e0d98501901bnhc.html
https://k.sina.com.cn/article_7879996653_1d5af34ed02001kkd0.html
https://m.blog.csdn.net/python9snake/article/details/155368686
https://m.blog.csdn.net/u011487024/article/details/162086616
https://m.elecfans.com/article/8187284.html
https://m.hexun.com/tech/2025-08-09/220818502.html
https://m.huxiu.com/article/4863770.html
https://maniskill.readthedocs.io/en/latest/_modules/mani_skill/utils/structs/articulation_joint.html
https://mujoco.readthedocs.io/en/stable/computation/
https://mujoco.readthedocs.io/en/stable/mjx.html
https://news.qq.com/rain/a/20250218A03XNJ00
https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/_api_build/classPxSceneDesc.html
https://oss-global-cdn.unitree.com/static/a0542aa67f4b4b1f9095682e4c5c3292.zip
https://raw.githubusercontent.com/Genesis-Embodied-AI/Genesis/main/README.md
https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md
https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/README.md
https://raw.githubusercontent.com/haosulab/ManiSkill/main/README.md
https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/source/isaaclab/isaaclab/sim/simulation_cfg.py
https://raw.githubusercontent.com/newton-physics/newton/main/README.md
https://raw.githubusercontent.com/unitreerobotics/unifolm-world-model-action/main/README.md
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/g1/g1_23dof.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/g1/g1_29dof.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h1/h1.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h1_2/h1_2_handless.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/h2/h2_mujoco.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_mujoco/main/unitree_robots/r1/R1_C++.xml
https://raw.githubusercontent.com/unitreerobotics/unitree_rl_lab/main/source/unitree_rl_lab/unitree_rl_lab/assets/robots/unitree.py
https://raw.githubusercontent.com/unitreerobotics/unitree_ros/master/robots/g1_description/g1_29dof_rev_1_0.urdf
https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/LowCmd.msg
https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/LowState.msg
https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/MotorCmd.msg
https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/cyclonedds_ws/src/unitree/unitree_hg/msg/MotorState.msg
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/example/g1/g1d/g1d_arm_example.cpp
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/example/g1/low_level/g1_ankle_swing_example.cpp
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/LowCmd_.hpp
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/LowState_.hpp
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/MotorCmd_.hpp
https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/include/unitree/idl/hg/MotorState_.hpp
https://robot-api.unitree.com/doc/?space=
https://robot-api.unitree.com/doc/?space=Motor_SDK_Dev_Guide&locale=en
https://robot-api.unitree.com/doc/spaces2?locale=en
https://sapien-sim.github.io/docs/
https://shop.unitree.com/collections/all
https://shop.unitree.com/products/go1-motor
https://shop.unitree.com/products/unitree-im6014-motor
https://shop.unitree.com/products/unitree-z1
https://shop.unitree.com/sitemap.xml
https://support.unitree.com/home/zh/developer
https://www.1x.tech/discover/1x-world-model
https://www.arterytek.com/cn/product/AT32M416.jsp
https://www.cnblogs.com/flyingsir/p/19220639
https://www.ethercat.org/en/technology.html
https://www.figure.ai/news
https://www.figure.ai/news/helix
https://www.gigadevice.com.cn/product/mcu/mcus-product-selector/gd32m531rbt7
https://www.physicalintelligence.company/research/pi-star-0.6
https://www.st.com/en/microcontrollers-microprocessors/stm32f405rg.html
https://www.st.com/en/microcontrollers-microprocessors/stm32f767bi.html
https://www.st.com/en/microcontrollers-microprocessors/stm32g431cb.html
https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html
https://www.st.com/en/microcontrollers-microprocessors/stm32h723zg.html
https://www.st.com/en/microcontrollers-microprocessors/stm32h743ai.html
https://www.unitree.com/Dex3-1
https://www.unitree.com/Dex5-1
https://www.unitree.com/H2
https://www.unitree.com/IM6014/
https://www.unitree.com/R1
https://www.unitree.com/cn/opensource/
https://www.unitree.com/g1
https://www.unitree.com/go1/motor
https://www.unitree.com/h1
https://www.unitree.com/motor/
https://www.unitree.com/z1
https://zhuanlan.zhihu.com/p/2069008612740031291
https://zhuanlan.zhihu.com/p/29880026964
```

**四足史料分组（非本书解剖对象）**：`https://www.unitree.com/go1/motor` 与
`https://shop.unitree.com/products/go1-motor` 在上面的清单里**保留**——它们讲的是 GO-M8010-6
这颗关节电机，只因宇树把电机文档挂在 Go1 目录下才带这个名字，用途是器件史料（附录 C 的电机表、
第 15 章的器件阶梯），讲的是电机不是狗。另有 7 条早期 Go1/Go2 生态的第三方开发与仿真资源，
2026-10-08 收口时从上面的清单移进这一行，只留名、不进任何一章的论证链：
`egh0bww1.com/posts/2023-10-24-unitree-go1-collection/`、
`github.com/MAVProxyUser/YushuTechUnitreeGo1`、`github.com/abizovnuralem/go2_omniverse`、
`github.com/abizovnuralem/go2_ros2_sdk`、`github.com/jizhang-cmu/autonomy_stack_go2`、
`github.com/legion1581/go2_firmware_tools`、`github.com/Huuhuuw/FAST_LIO_LOCALIZATION_HU`。
本书的解剖对象只有人形：同一清单里的 `unitree.com/g1`、`unitree.com/H2`、`unitree.com/h1`、
`unitree.com/R1` 与它们的消息、模型与文档页才是本书逐条核对过的东西。

## E.4 「查不到」清单

本书认真找过、但**没有拿到官方答案**的问题。它们不是疏漏，是这本书的边界。

**器件与整机**

1. 全系关节电机的**额定（持续）扭矩**——一个型号都没有。
2. 关节驱动板的 **PWM 载波频率、死区时间、是否做死区补偿**。
3. 关节电机的 **绕组电感 L、相电阻 R、转动惯量 J、极对数 p、磁链 λ_m**。
4. 关节电机是 **SPM 还是 IPM**；是否实现**弱磁**。
5. 关节驱动板的 **MCU 型号**（拆解称芯片丝印被抹除）。
6. **IMU 的型号、供应商、量程、零偏稳定性、噪声密度、整机 IMU 采样率、安装位置、g 敏感度**。
7. 编码器的**单圈/多圈**、输出端位数与精度（M8010 官方为单圈；整机页只写“双编码器”）。
8. **电芯型号、化学体系、能量密度、包重、放电倍率（C 数）、循环寿命、BMS 策略**。
9. **整机功耗**（平均与峰值）、**每公里能耗**、**可行驶里程**——因此人形的 CoT 无法计算。
10. 各型号的 **IP 防护等级**（四足侧有 IP54/IP67 口径，人形侧未公布）。
11. **结构模态频率**、连杆截面与材料牌号、热处理与牌号。
12. G1/H1/H2 的**关节总线拓扑**（几条干、每干几台、收发器型号）。

**软件与控制**

13. 整机在线控制律（是否跑 WBC/MPC、求解器、频率）。
14. 出厂固件里关节环路的实际 kp/kd 默认值（仓库里的值是训练默认值）。
15. UnifoLM 的**动作专家规模、动作头形式、是否动作分块、是否双系统、部署方式、逐任务成功率**。
16. 相机是否**硬件同步**、时钟源、是否全局快门。
17. `rt/lowstate` 在人形机型上的确切频率（Go2 上本书实测 500 Hz，不可外推）。
18. ROS 2 Jazzy 的支持状态。

**安全与制度**

19. **急停是单通道还是双通道**、是否走硬件安全回路。
20. **断电时序**（抱闸与断动力的先后、卸扭矩耗时）。
21. **上电默认态**，以及如何检测“断电期间被搬动过”。
22. **有人模式下的力矩与功率限制值**，依据哪条标准条款。
23. 任何一款人形的 **MTBF / 连续作业时长 / 失败恢复机制**。
24. 已获安全认证清单（CE / CR / ISO 10218 / ISO/TS 15062 / IEC 62443）。

**行业与商业**

25. 各家 **GPU 集群规模**、数采工厂真实台数、单条数据成本、数据合格率（北京人形数据基地除外）。
26. 银河通用的 MCU / 总线 / 传感器品牌 / 双臂供应商（完全无公开资料）。
27. 智元减速器路线的最终口径（官方“行星替代谐波”与供应链“来福谐波占比 >90%”两条并存）。
28. Dex1-1 / Dex2-5 / Dex3-1 的官方售价；H1-2 的价格与完整规格。

## E.5 冲突口径登记（本书一律并列，不取平均）

| 项 | 口径 A | 口径 B | 出处 |
|---|---|---|---|
| G1 膝峰值扭矩 | 90（基础页）/ 120（EDU 页与文档） | 139（官方模型与 rl_lab 配置） | [厂] |
| G1 踝峰值扭矩 | 35 / 50 / 25 | 35（N5020-16-parallel） | [厂] |
| G1 hip_roll effort | 139 | 88（同仓库另一 URDF） | [厂] |
| G1 减速方案 | 两级行星 ≈20.58 | 官方型号名 14.3 / 22.5 | [拆] vs [厂] |
| H1 膝峰值扭矩 | 360（产品页） | 300（官方 MJCF/URDF）；200（rl_lab M107-24-2） | [厂] |
| 关节总线 | 官方“全部电机 RS-485” | 拆解“CAN 高低线菊花链” | [厂] vs [拆] |
| IM6014 电压上限 | 75 V | 72 V（同页另一处） | [厂] |
| IM6014 电机 ID | 0~14 + 15 广播 | 0-15（STM32 参数表） | [厂] |
| R1 总自由度 | 26-40 | 20/26/26；“20-26-DOF” | [厂] |
| 智元减速器 | 官方“准直驱+行星替代谐波，BOM ↓30%” | 供应链“来福谐波占比 >90%” | [查] |

## E.6 本书判定为「不可采信」的流传说法

- 网传 H1 售价“9.5 万元”——来源不可靠。
- 宇树存在型号「M107-24」——只查到 M107 与 rl_lab 里的 M107-24-2。
- 宇树「Unitree Mimics」数据集——不存在，最接近的是 UnifoLM-WBT-Dataset。
- 「宇树用国产谐波减速器降本」——在宇树自家产品上只能证到 Z1（官方谐波）与拆解口径的 G1（行星），证据不足。
- 银河通用 ET1 的两套互斥规格（38 DoF/RK3588 与 173 cm/72 DoF/Thor）——疑为自动生成内容。
- 店铺里 $100,000 一档（B2/A2/B1/H2-Plus）——判定为占位价。
