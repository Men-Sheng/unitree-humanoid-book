# 别家一手抓取表（2026-10-09 起）

这张表补的是 F-30 第 5 条那笔账：第 29–34 章的算术有一批输入是**别家厂商/论文**的口径，
而它们此前只存在于作者蓝图附件的二手转述里，`bible/sources.md` 与 `research/*.md` 没有任何抓取记录。
本表逐条给出：一手 URL、访问日期、**逐字原文**、判定。判定只有四种：**一手证实 / 一手未载 / 只有二手 / 抓取被拦**。

方法照 [[unitree-spec-sources]] 那套：优先官方仓库 raw 页与厂商自己的 blog；`WebFetch` 403/429 时换 curl + 桌面 UA；
阴性结果（"通篇没有 Hz"）也算证据，必须记下载字节数与抓取时间，否则下次无法复现。

| 条目 | 书中现用值 | 一手原文（逐字） | 来源 | 访问日期 | 判定 |
|---|---|---|---|---|---|
| Figure Helix 的 S2 规模 | 7 B VLM | `S2 is built on a 7B-parameter open-source, open-weight VLM` | https://www.figure.ai/news/helix | 2026-10-09 | **一手证实** |
| Figure Helix 的 S1 规模 | 80 M | `S1, an 80M parameter cross-attention encoder-decoder transformer` | 同上 | 2026-10-09 | **一手证实** |
| Figure Helix 的 S2 节奏 | 7–9 Hz | `operating at 7-9 Hz for scene understanding` | 同上 | 2026-10-09 | **一手证实** |
| Figure Helix 的 S1 输出 | 200 Hz | `continuous robot actions at 200 Hz.` | 同上 | 2026-10-09 | **一手证实** |
| Figure Helix 端到端延迟 | 书里没有用它 | — | 同上 | 2026-10-09 | 一手未载（不给数就不写数） |
| GR00T 主干参数量 | 2B–7B 区间内 | `Base model (3B params)` | https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md | 2026-10-09 | **一手证实**（3 B，落得进区间） |
| GR00T 动作时域 | horizon 40 | `action_horizon expanded from 16 to 40` | 同上 | 2026-10-09 | **一手证实** |
| GR00T 状态/动作维度 | 132 维 | `State and action dimensions expanded from 29 to 132` | 同上 | 2026-10-09 | **一手证实** |
| GR00T 显存门槛 | 16 GB 这一档 | `1 GPU with 16 GB+ VRAM (e.g., RTX 4090, L40, H100, Jetson AGX Thor/Orin, DGX Spark).` | 同上 | 2026-10-09 | **一手证实**（原文就是"16 GB+ 起步"，不是"标配 16 GB"） |
| GR00T 推理频率 Hz | 书里未用它 | — | 同上 | 2026-10-09 | 一手未载 |
| **宇树 UnifoLM-WMA-0 的真机侧频率** | 旧稿曾写 15 Hz [厂] | README 全篇 `Hz / ms / control rate / frequency / real-time` **零命中**；只有目录树里一行 `└── unitree_deploy  # Deployment code` | https://raw.githubusercontent.com/unitreerobotics/unifolm-world-model-action/main/README.md | 2026-10-09 | **一手未载** ⇒ 15 Hz 只能当二手量级，[厂] 是错的（正文已于本轮改 [查][未]） |
| π*0.6 的 860 M / 4 B / 5 步 / 63 ms / 50 Hz | 第 29 章用它算 t_step = 63 ÷ 5 = 12.6 ms | 未取到：`physicalintelligence.company` 对 `research/pi-star-0.6` 与 `research` 两页都返回 **429**（带桌面 UA、跟随重定向、curl 亦 429，页面 33,945 字节是拦截页）；arXiv API 用 `"learns from experience" AND "advantage conditioned"` 检索 **0 条** | https://www.physicalintelligence.company/research/pi-star-0.6 | 2026-10-09 | **抓取被拦** ⇒ 这些数仍是二手，正文标记本轮已从 [查] 降为 [推] 并写明"未读到原文" |

## 用法与后续

- 本表是**活页**，每条都要在下一次抓取时重写日期；`rebuild_all.sh` 的第 0 步会把这里的 URL 收进附录 E.3。
- 剩下待抓的一手：**1X（14 B / 11 s / 1 s）、Genie 3（720p / 20–24 fps）、GAIA-2 分辨率、GE-Act（160 M / 200 ms / 54 步）、
  AgiBot World（4000 ㎡ / 100+ 台 / 日产 1000 条 / 26 自由度 / 50–100 ms）、DROID、SmolVLA、π0.5/π0 的流匹配步数**。
  在这些补齐之前，第 29–34 章凡是把它们当**精确输入**的推论都只支持量级与曲线形状——正文每处都写了这句。
- **一条纪律**：`[查]` 的定义是"本书已读到原文"。没读到原文就标 `[查]`，等于替别人签了字。
  本轮据此降级了 π*0.6 那组数（429 拦住），并据此确认了 Helix 与 GR00T 那两组可以标 `[查]`。

| Genie 3 分辨率 | 720p | `resolution of 720p` | https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/ | 2026-10-09 | **一手证实** |
| Genie 3 帧率 | 旧稿写 20–24 fps | `24 frames per second` | 同上 | 2026-10-09 | **一手只写 24 fps** ⇒ 正文删掉 20（多写的那个数没有出处） |
| Genie 3 一致性时长 | 数分钟 | `retaining consistency for a few minutes`（另一句 `few minutes of continuous interaction`） | 同上 | 2026-10-09 | **一手证实**（原文就是"几分钟"，不是分钟数） |
| 1X / GE-Act / GAIA-2 / AgiBot World / SmolVLA | 14 B / 11 s；160 M / 200 ms / 54 步；5 路 448×960；4000 ㎡ 与日产 1000 条；—— | **未取到**：arXiv API 四条检索（`all:"Genie Operator-1"`、`all:"GE-Act"`、`all:"SmolVLA"`、`all:"AGIBOT World"`）**返回空响应**；1X 与 Wayve 的页面本轮未访问 | http://export.arxiv.org/api/query?search_query=all:%22GE-Act%22 | 2026-10-09 | **抓取被拦 / 未取到** ⇒ 这些数继续记 [推]，正文凡以它们为输入的推论只支持量级 |

| 1X 世界模型的角色 | 第 34 章用它讲"评测" | `we have trained a world model that serves as a virtual simulator for our robots.`；`World models solve a very practical and yet often overlooked challenge when building general-purpose robots: evaluation.` | https://www.1x.tech/discover/1x-world-model | 2026-10-09 | **一手证实角色，但 14B / 11 s / 1 s 与任何 Hz 在一手页面里全部 absent** ⇒ 这组数降为 [推]，第 34 章的主线改跑在一手的 24 fps 上 |
| 每步去噪的一手实测 | 第 29 章 t_step、第 30 章"5–10 步" | `after the 10 denoising steps`；`composed of a vision encoder SigLIP with 400M parameters and a large language model Gemma with 2.6B parameters`；`achieve a latency of 27.3 ms given two input views`；`under a single consumer RTX 4090 GPU` | https://arxiv.org/html/2510.26742v1（Running VLAs at Real-time Speed，Dexmal 与 StepFun） | 2026-10-09 | **一手证实** ⇒ 27.3 ÷ 10 = 2.73 ms/步，比二手口径的 12.6 ms 快 4.6 倍 |

| AgiBot World 轨迹数与时长 | 第 33 章口径 B 的两个输入 | `The latest version contains 1,001,552 trajectories, with a total duration of 2976.4 hours.` | https://arxiv.org/html/2503.06669v1 | 2026-10-09 | **一手证实**（10.7 s/条 那条除法成立） |
| AgiBot World 规模与场景 | 217 任务 | `covering 217 specific tasks, 87 skills, and 106 scenes.` | 同上 | 2026-10-09 | **一手证实** |
| 数采基地面积与台数 | 旧稿只有媒体口径 [查] | `spans over 4,000 square meters.`；`A suite of 100 dual-arm humanoid robots is deployed.` | 同上 | 2026-10-09 | **一手证实**（升 [查]） |
| 单条时长 | 第 33 章"30 s 一条" | `episodes typically span approximately 30 seconds, some of which last over 2 minutes.` | 同上 | 2026-10-09 | **一手证实** |
| 日产条数（1,000 条/天之类） | 正文当量级用 | **论文全文没有给任何产出率** | 同上（负面结果） | 2026-10-09 | **一手未载** ⇒ 降 [推]，正文明写"仍属媒体口径" |
| GE-Act 的 160 M / 200 ms / 54 步 | 第 34 章表内 | 未读到：arXiv 站内检索 `Genie Envisioner / GE-Act` **返回 0 条** | — | 2026-10-09 | **抓取未成** ⇒ 降 [推] |
| SmolVLA 的 100 M / 450 M | 第 30 章那条倍数 | 未读到一手页面 | — | 2026-10-09 | **抓取未成** ⇒ 标 [推] |

| Cosmos 的基础模型档位 | 正文"Edge 4B" | `we first build two base models that are 4B and 12B in size, respectively`；`We name them Cosmos-Predict1-4B and Cosmos-Predict1-12B, respectively.`；`without running out of memory on a single NVIDIA A100 GPU with 80GB memory.` | https://arxiv.org/html/2501.03575v3 | 2026-10-09 | **4B 与 12B 一手证实**；但论文里**没有** Nano / Super / Edge 这些档位名，也**没有** Jetson / Orin / Thor 字样 ⇒ 2026 年那套档位名与"可跑"仍是新闻稿口径，降 [推] |
| GAIA-2 的 5 路 448×960 | 第 34 章一处并列举例 | 未读到（arXiv 站内检索只返回一篇无关的 Puffin-World） | — | 2026-10-09 | **抓取未成** ⇒ 继续记 [推]，正文那句已归在"二手栏" |
| π0 的去噪步数与规模 | 第 30 章“5–10 步”、第 29 章的每步成本 | `10 integration steps`；`3.3 billion parameters`；`H=50`；控制频率 50 Hz | https://arxiv.org/html/2410.24164v1 | 2026-10-09 | **一手证实**（5–10 步这个通例有了一手的 10） |
| GAIA-2 的多路与分辨率 | 旧稿 5 路 448×960 [推] | `up to five temporally and spatially consistent camera streams`；`resolution of 448×960`；`each spanning 2 seconds`；`8.4B parameters` | https://arxiv.org/html/2503.20523v1 | 2026-10-09 | **一手证实** ⇒ 升 [查]，并从"二手栏"移到"一手栏" |
| DROID 规模 | 第 33 章 16.6 s 每条的输入 | `76k demonstration trajectories`；`350 hours of interaction data`；`84 tasks`；`564 scenes` | https://arxiv.org/abs/2403.12945 | 2026-10-09 | **一手证实**（`350 × 3,600 ÷ 76,000 = 16.6 s` 成立）；HTML 版 404，用 abs 页读到 |
| GE-Act 的规模 / 步数 / 延迟 | 第 34 章表内 | `GE-Act is a lightweight 160M-parameter autoregressive action decoder`；`54-step torque trajectories within 200 ms on a commodity GPU`；30 Hz；计时 `onboard NVIDIA RTX 4090 GPU` | https://arxiv.org/html/2508.05635v3（Genie Envisioner） | 2026-10-09 | **一手证实**；**且推翻一处分类**：它是自回归解码器，不是流匹配头 ⇒ 第 30 章的代表列表已更正 |
| SmolVLA 的主干 / 专家分栏 | 旧稿 `100 M ÷ 450 M ≈ 4.5 倍` | 一手只给 `4.5亿参数`（450 M 总规模）与动作头 `Flow-Matching Transformer`；**主干与专家分栏未公布** | https://smolvla.net/ | 2026-10-09 | **一手只到总规模** ⇒ 那句倍数删除并说明"没分栏就算不出倍数"；450 M 被旧稿当成主干是用错口径 |
| π0 的积分步数 | 第 30 章“5–10 步” | `10 integration steps`；`3.3 billion parameters`；`H=50`；50 Hz | https://arxiv.org/html/2410.24164v1 | 2026-10-09 | **一手证实** |
| GAIA-2 的多路与分辨率 | 旧稿 [推] | `up to five temporally and spatially consistent camera streams`；`resolution of 448×960`；`each spanning 2 seconds`；`8.4B parameters` | https://arxiv.org/html/2503.20523v1 | 2026-10-09 | **一手证实** ⇒ 升 [查] |
| DROID 规模 | 第 33 章 16.6 s 每条 | `76k demonstration trajectories`；`350 hours of interaction data`；`84 tasks`；`564 scenes` | https://arxiv.org/abs/2403.12945（html v3 返回 404） | 2026-10-09 | **一手证实** |
| ALOHA 每任务演示条数 | 第 29 章"单任务约 50 条演示 [查]" | `With 50 demonstrations for each task,` | https://arxiv.org/abs/2401.02117（Mobile ALOHA） | 2026-10-09 | **一手证实**（同篇另有 `increase success rates by up to 90%`，本书没用到就没写进正文） |
| GraspVLA 的定位 | 第 30、44 章把它当"单卡可训的 VLA 范本" | 一手只读到标题 `GraspVLA: a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data`；**参数量、去噪步数、延迟、演示条数在 abs 页全部 absent** | https://arxiv.org/abs/2505.03233 | 2026-10-09 | **部分一手**（标题级）⇒ 正文涉及它的具体规格若无其它来源，一律记 [推] |

## 尚未逐字回读的 [查]（`tools/check_vendor_ledger.py` 每轮重算，清单在 `verification/vendor-ledger-latest.txt`）

第七轮独立审稿指出：第 29–34 章有约 20 处标了 [查]，但本台账里没有对应的逐字行。
本轮已补的是 ALOHA 与 GraspVLA 两条；**仍欠逐字原文的**（付印前要么补抓、要么降 [推]）：

- Gemini Robotics 的"拉袋 44% / 拉链 40%"与 Figure Helix 2.5 的"30 户家庭零样本 56%"（第 29、38 章）
- GO-2 / ACoT-VLA 的规格（第 30 章）
- GR00T 的 `Cosmos-Reason2-2B`、`flow-matching DiT，16 层`、相对末端位姿、ONNX/TensorRT 导出（第 30 章：本台账只确认 3 B 主干 / horizon 40 / 132 维 / 16 GB+）
- SynGrasp 与 GEN-0 的 >270,000 小时（第 33 章）
- 智元数据工厂"95%+ 合格率"（第 33 章：AgiBot 论文里**没有**产出率与合格率，见上文负面行）
- "用比特而非原子做评估"这句话的出处、Tesla FSD 与 Optimus 共用神经仿真器的原话（第 34 章）

**这些不是"已经查清"，是"已登记未查清"。** 门把它们列成软清单，就是为了不让人把它们当成已通过。
| GR00T 主干与检查点名 | 第 30 章表格、第 34 章分栏句 | `nvidia/GR00T-N1.7-3B`；`Base model (3B params) — zero-shot inference on pretrain embodiments, or finetune for new tasks`；`GR00T's VLM backbone is nvidia/Cosmos-Reason2-2B`；`New VLM backbone: Cosmos-Reason2-2B (Qwen3-VL architecture), replacing the Eagle backbone used in N1.6` | https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md | 2026-10-09 | **一手证实，并修正一处不精确**：3 B 是整个检查点，主干是 2 B |
| GR00T 动作头层数 | 第 30 章 | `Action head remains flow-matching DiT, but changes from 32 to 16 diffusion layers` | 同上 | 2026-10-09 | **一手证实** |
| GR00T 动作空间 | 第 30 章 | `relative end-effector action space shared across robot and human embodiments` | 同上 | 2026-10-09 | **一手证实** |
| GR00T 导出与许可 | 第 30、44 章 | `full-pipeline ONNX and TensorRT export support`；`SPDX-License-Identifier: Apache-2.0` | 同上 | 2026-10-09 | **一手证实** |
| π0 的推理硬件 | 第 30 章那条带宽式的分母 | `The operations were timed on an NVIDIA GeForce RTX 4090 consumer-grade GPU`；表题 `TABLE I: Inference time of our model on a NVIDIA GeForce RTX 4090 GPU.` | https://arxiv.org/html/2410.24164v1 | 2026-10-09 | **一手证实，并推翻本书上一版**：原稿写“它跑在服务器卡上（H100 的 HBM3 约 3.35 TB/s）”，一手是 4090、1008 GB/s |
| π0 那十步到底重算多少权重 | 第 29、30 章“每步读全量权重”那条式子 | `Note that inference can be implemented efficiently by caching the attention keys and values for the prefix and only recomputing the suffix corresponding to the action tokens for each integration step.`；`To speed up inference (which requires multiple forward passes of the action expert), we downsize the action expert to { width =1024, mlp_dim =4096}, resulting in a parameter count of ~300M.` | 同上 | 2026-10-09 | **一手证实**：迭代只重算 300 M 专家，主干作前缀算一次并缓存 KV ⇒ “K × 2P_总 ÷ 带宽”是错的模型，本书已按 P_迭代 改写 |
| π0 的分项计时 | 第 30 章新增那张表 | `image encoders 14 ms`、`observation forward pass 32 ms`、`x10 action forward pass (flow) 27 ms`、`network latency (if off-board) 13 ms`、`total on-board inference 73 ms`、`total off-board inference 86 ms` | 同上 | 2026-10-09 | **一手证实**；14 + 32 + 27 = 73，表自洽 [算] |
| π0 的推理节拍 | 第 30 章“预算是 0.5 s 不是 20 ms” | `for all other robots, which run at 50Hz, we run inference every 0.5 seconds (after executing 25 actions)`；`For the 20Hz UR5e and Franka robots, we run inference every 0.8 seconds (after executing 16 actions)` | 同上 | 2026-10-09 | **一手证实**；上一版把 50 Hz 的执行节拍当成了推理节拍，于是把 14.6% 写成 98% |
| Helix 的部署结构（双进程异步） | 第 30 章“慢的那一半怎么办” | `S1 executes as a separate real-time process, maintaining the critical 200Hz control loop required for smooth whole upper body action`；`S2 operates as an asynchronous background process, consuming the latest observation`；`It continuously updates a shared memory latent vector that encodes the high-level behavioral intent`；`The asynchronous execution model allows both processes to run at their optimal frequencies` | https://www.figure.ai/news/helix | 2026-10-09 | **一手证实**；交接靠共享隐向量，不是节拍同步 |
| Helix S1 的架构定性与权重分栏 | 第 30 章“十步迭代塞不塞得进”“87 倍” | `Helix uses standard architectures - an open source, open weight VLM for System 2 and a simple transformer-based visuomotor policy for S1`；`Using just one set of neural network weights (7B for System 2, 80M for System 1)` | 同上 | 2026-10-09 | **一手证实**；**原文未给 S1 的迭代步数、也未给那两块嵌入式 GPU 的带宽** ⇒ 那两格仍是 [未]，本书上一版用假设的 100 GB/s 推“绝不可能塞进十步”，已撤 |
| Helix 的双 GPU 与训练—部署时序偏移 | 第 30 章 | `efficient model parallel deployment on Figure robots, each equipped with dual low-power-consumption embedded GPUs`；`During training, we add a temporal offset between S1 and S2 inputs. This offset is calibrated to match the gap between S1 and S2's deployed inference latency` | 同上 | 2026-10-09 | **一手证实**（芯片型号、功耗、带宽原文均未给 [未]） |
| SmolVLA / SynGrasp / GEN-0 / Gemini 成功率 / Figure Helix 2.5 / 北京 95% / Tesla 仿真器 | 见正文各处 [查] | **本轮仍未取到**：`export.arxiv.org/api/query`（含 ti: 与 all: 两种写法）对这几条一律返回空响应；厂商页面未逐字访问 | — | 2026-10-09 | **抓取未成** ⇒ 台账保留“尚未逐字回读”标记，`check_vendor_ledger` 会继续把它们列成软清单 |
| Figure 是否公布过 “Helix 2.5” 与那三个成功率（56% / 44% / 40%） | 第 29、38 章的“厂商自陈”措辞 | **反向证据**：`figure.ai/news` 索引逐条读下来，Helix 相关只有 `Helix Loads the Dishwasher`（2025-09-03）、`Helix Learns to Fold Laundry`（2025-08-12）、`Scaling Helix: a New State of the Art in Humanoid Logistics`（2025-06-07），**没有 “Helix 2.5” 这一条目**；`figure.ai/news/helix-2-5` 返回 **404**；`arxiv.org/abs/2503.20925` 与 `2510.16678` 的摘要页里检索不到 44% / 40% / 56% | https://www.figure.ai/news | 2026-10-09 | **抓取未成 + 索引里查不到该条目** ⇒ 第 29、38 章的措辞已从“厂商自陈 / 挑两个能核的”降为**媒体转述 [推]**，并把这条反向证据印进正文 |
| Helix 完全端侧这件事 | 第 30 章表内"完全端侧（双低功耗嵌入式 GPU）" | `Helix is the first VLA that runs entirely onboard embedded low-power-consumption GPUs`；`dual low-power-consumption embedded GPUs` | https://www.figure.ai/news/helix | 2026-10-09 | **一手证实**（但芯片型号与功耗原文未给 ⇒ 那两格仍 [未]） |
| LeRobot 官方文档的循环实测 | 第 29、33 章 | 目标 `30 Hz (33.3 ms budget per tick)`、实测 `29.88 Hz`、`16/1198 ticks 超时（1.3%）`、work mean `18.4 ms` / worst `45.1 ms`、`observe` 占 74% | https://github.com/huggingface/lerobot（`docs/source/il_robots.mdx` 行 420-434，抓取记于 `bible/sources.md` G0） | 2026-10-09 | **一手证实**（是 Hugging Face 的仓库文件，按图例记 [查] 不是 [厂]） |
| GO-2 / ACoT-VLA 的异步双系统 | 第 30 章表内 | **未取到一手**：检索只回到媒体与百科（ai-bot.cn、CSDN、sohu、eefocus），智元官方页无逐字原文 | — | 2026-10-09 | **抓取未成** ⇒ 正文降 [推] |
| Tesla 关于 Optimus 的一手原句（Q4 2024 股东更新） | 第 03/15/39 章可用作量产与手的难度佐证 | `Progress on Optimus hardware and software continued in Q4, including the latest generation hand, robust locomotion and training on additional tasks, ahead of planned pilot production in 2025.` | https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q4-2024-Update.pdf | 2026-10-09 | **一手证实（36 页 PDF，PyMuPDF 抽取全文；这是公司口径的书面更新，不是马斯克个人发言）** |
| Tesla 关于 Optimus 的一手原句（Q1 2025 股东更新） | 同上 | `We remain on track for pilot launch of Robotaxi in Austin by June and builds of Optimus on our Fremont pilot production line in 2025, with wider deployment of bots doing useful work across our factories.` | https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q1-2025-Update.pdf | 2026-10-09 | **一手证实（32 页 PDF）** |
| 马斯克个人关于 FOC / 三相旋转磁场 / 斩波死区 / Clarke-Park / iq 与 id / 三环带宽 / 刚度天花板 / IMU 零偏 / 中间件 的技术表述 | 第 05、07、09、10、11、12、18、24、28 章的题引 | **检索结果：零。** 特斯拉公开材料里与这些主题相关的只有上面两句公司口径的进度描述；`ir.tesla.com` 与 `digitalassets.tesla.com` 的股东更新里没有马斯克对电机控制、功率电子、惯性测量或中间件的任何技术性发言 | — | 2026-10-09 | **一手未载** ⇒ 按作者规矩“读不到原文就不写”，这九章的题引继续留空并在附录 A.7 说明理由；**不用名人名言填空**，因为那九章要的是“死区为什么会偷电压”这类可核对的技术表述 | 
| Wikimedia Commons 上的宇树自由许可照片 | 图 00-2 整机照、图 A-1 王兴兴像、图 02-3 总部 | 检索 `gsrsearch=unitree` 得 54 个文件；取 CC0 `File:Unitree_G1.jpg`（Sayanesy，1380×2326）、CC BY 3.0 `File:Wang Xingxing at the World Economic Forum's 16th Annual Meeting of the New Champions in Tianjin, China.png`（China News Service，578×817）、CC BY-SA 4.0 `File:20260425_Unitree_Headquarter_02.jpg`（Windmemories，1800×1200） | https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=unitree&gsrnamespace=6 | 2026-10-09 | **一手证实（许可与作者由 Commons API 的 extmetadata 直接读出，非网页自述）**；**54 个文件里没有任何关节或电机内部特写** ⇒ 那两格仍只能作者实拍 |
