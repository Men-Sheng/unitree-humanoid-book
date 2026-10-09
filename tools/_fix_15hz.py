import io

NL = chr(10)
P = 'drafts/unit-34/draft.md'
t = io.open(P, encoding='utf-8').read()

# ① 标题段里那句"真机侧客户端约 15 Hz（…二手口径…）"整段撤下
i = t.index('宇树把 UnifoLM-WMA-0 命名为 World-Model-Action')
j = t.index('## 驾驶侧的那面镜子')
old_block = t[i:j]

new_block = '''宇树把 UnifoLM-WMA-0 命名为 World-Model-Action，官方口径里它有两个用途 [厂]：**既在仿真里合成本体数据，也接动作头做决策**；仓库里确有 `action_model/flow_matching_head/` 这个目录名 [厂]。至于它跑多快：**官方页面与仓库通篇没有 Hz 或 ms** [未]——2026-10-09 逐字回读，`Hz`、`ms`、`control rate`、`frequency`、`real-time` 五个词全部零命中，只有目录树里一行 `unitree_deploy  # Deployment code`（阴性结果记在 `research/other-vendor-firsthand.md`）。

**先撤回本书自己的一处错。** 前一版这一节写着“真机侧客户端约 15 Hz”，并围绕它做了三段推理。本轮去查这句话的出处，查到的结果是：**那个 15 Hz 属于 NVIDIA 的 Cosmos 3 Edge 在 Jetson AGX Thor T5000 上跑策略时的输出频率，跟宇树的 WMA-0 没有任何关系**。本书把别家的一手数字挂到了宇树头上。这类错误比算错更危险，因为它后面跟着一个看起来完全可靠的方括号，而读者没有任何办法察觉。**本书早前犯过同型的一次**：把别处抄来的“L2 内置 IMU 官方标 1 kHz”当事实，后来在第 24 章留了撤回框——这次是同一个毛病的另一种形态：**不是抄错，是把 A 家的一手数写到了 B 家的格子里。**

**同一条论证搬到真正属于它的那组数上，结论不但没变，现在还可核对了。** NVIDIA 官方开发者博客，2026-10-09 逐字读到 [查]：

```text
Cosmos 3 Edge is a 4B omni-model (with a 2B NVIDIA Nemotron-based reasoner)
At roughly 9 GB in BF16, the weights fit in Thor’s on-board memory
On an NVIDIA Jetson AGX Thor T5000, it generates each action chunk in about 1.53 seconds
(running at 640×540 resolution and 15 Hz), while a single chunk covers roughly 2.13 seconds
Because the next chunk is ready before the current one finishes, the arm moves continuously
```

**这六行把本章前面所有抽象判据一次落地。** 逐条对：

```text
每块推理 T_infer = 1.53 s，一块覆盖 2.13 s ⇒ 2.13 ÷ 1.53 = 1.39 > 1
⇒ 第 31 章那条 H·Δt ≥ T_infer 成立，而且是厂商自己说的“下一块在当前块用完前就好了”
输出节拍 15 Hz ⇒ Δt = 1 ÷ 15 = 67 ms   [算]
第 31 章判据：接触密集任务的反应延迟要 < 100 ms ⇒ 67 ms 过
第 16 章判据：τ = 259 ms，要参与平衡得落在 10–100 ms ⇒ 67 ms 在带内，但只勉强
权重 4B × 2 字节 = 8 GB，厂商自报 roughly 9 GB ⇒ 同一件事的两种写法 [算]
```

**67 ms 落在“能参与操作节奏、勉强参与慢速校正、不可能单独守平衡”的那个窄带里**，这正是本书要给“世界模型-动作”这一类东西占的位置——**它是节奏级的参与者，不是稳定性的承担者**；承担稳定性的仍然是第 12 到第 19 章那条 1 kHz 的环路。**而 9 GB 这一条顺手验证了第 26 章的带宽算术**：本书按 4B × 2 字节算出 8 GB，NVIDIA 报 roughly 9 GB（多出的那部分是嵌入与注意力权重之外的东西，本书不细算）——**外部对照比任何自检都硬**。但它同时划出本书一条推理的边界：1.53 s 是在 **Jetson AGX Thor T5000**（板载高带宽内存）上量的，不是第 26 章那张表里 41.6–100 GB/s 的假设档，**不能拿它去反推别的模组**。

回到宇树这一格：**WMA-0 的用途有官方口径 [厂]，许可证是 CC BY-NC-SA、不可商用（见第 32 章），运行频率官方未公布 [未]**。本书因此不给它配任何节拍数；要看“世界模型-动作在端侧到底跑多快”，用上面 NVIDIA 那组一手数当参照，并记住那是**另一家的另一颗芯片**。

'''
t = t[:i] + new_block + t[j:]

# ② 时间线那行原先写“Orin/Thor 可跑”——一手只点名 Thor T5000，Orin 未出现
old = '分 Super 64B、Nano 16B、Edge 4B（Jetson AGX Orin/Thor 可跑） ← 档位名与可跑二字属新闻稿口径 [推]'
new = ('分 Super 64B、Nano 16B、Edge 4B（其中 Edge 4B 与"装得进 Jetson AGX Thor T5000"已一手：'
       '`a 4B omni-model`、`the weights fit in Thor’s on-board memory`；**Orin 未被点名**，Super/Nano 的 64B/16B 仍是新闻稿口径 [推]）')
assert t.count(old) == 1, ('② 锚点', t.count(old))
t = t.replace(old, new)

# ③ 那句"Edge 4B 能在 Orin/Thor 上跑"的算术说明，改成一手版
old = '“Edge 4B”这个档位名和“Orin/Thor 可跑”本书没读到一手出处，属新闻稿口径 [推]。'
new = '“Edge 4B”这个档位现在有一手了（`Cosmos 3 Edge is a 4B omni-model`），而“Orin 上能跑”仍没有——一手只点 Jetson AGX Thor T5000 [查]。'
assert t.count(old) == 1, ('③ 锚点', t.count(old))
t = t.replace(old, new)

io.open(P, 'w', encoding='utf-8', newline=NL).write(t)
print('ok 第 34 章：撤回 15 Hz 张冠李戴，论证搬到 Cosmos 3 Edge 一手数；Orin 那句降回新闻稿')
