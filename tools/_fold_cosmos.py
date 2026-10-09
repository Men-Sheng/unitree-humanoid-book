import io

P = 'drafts/unit-34/draft.md'
t = io.open(P, encoding='utf-8').read()
E = [
    ('         分 Super 64B、Nano 16B、Edge 4B（Jetson AGX Orin/Thor 可跑）',
     '         分 Super 64B、Nano 16B、Edge 4B（Jetson AGX Orin/Thor 可跑） ← 档位名与"可跑"是新闻稿口径 [推]'),
    ('而“Edge 4B 能在 Orin/Thor 上跑”这一条，与第 26 章的带宽算术一致：4B × 2 字节 = 8 GB，16 GB 模组装得下。',
     '“Edge 4B”这个档位名和“Orin/Thor 可跑”本书没读到一手出处，属新闻稿口径 [推]。**但 4B 这个数是一手的**：'
     'NVIDIA 那篇平台论文原话 `we first build two base models that are 4B and 12B in size, respectively` 与 '
     '`We name them Cosmos-Predict1-4B and Cosmos-Predict1-12B, respectively.` [查]——论文里只有 4B 与 12B 两档，'
     '没有 Nano / Super / Edge 这些名字，也没有任何 Jetson/Orin/Thor 字样。**所以这条算术不靠那半句**：'
     '4B × 2 字节 = 8 GB，16 GB 的模组装得下（没算 KV 与激活，是量级判断）[算]。'),
    ('**证据等级**：Cosmos 三阶段与 4B/Edge 档位',
     '**证据等级**：Cosmos 三阶段时间线，其中 4B 与 12B 两档是一手（arXiv 2501.03575v3 逐字：'
     '`two base models that are 4B and 12B in size`），而 Super 64B / Nano 16B / Edge 4B 这套档位名与“Orin/Thor 可跑”'),
]
for old, new in E:
    n = t.count(old)
    if n != 1:
        print('!! count=%d  %s' % (n, old[:48]))
        continue
    t = t.replace(old, new)
    print('ok  %s' % old[:44])
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline='\n').write('''
| Cosmos 的基础模型档位 | 正文"Edge 4B" | `we first build two base models that are 4B and 12B in size, respectively`；`We name them Cosmos-Predict1-4B and Cosmos-Predict1-12B, respectively.`；`without running out of memory on a single NVIDIA A100 GPU with 80GB memory.` | https://arxiv.org/html/2501.03575v3 | 2026-10-09 | **4B 与 12B 一手证实**；但论文里**没有** Nano / Super / Edge 这些档位名，也**没有** Jetson / Orin / Thor 字样 ⇒ 2026 年那套档位名与"可跑"仍是新闻稿口径，降 [推] |
| GAIA-2 的 5 路 448×960 | 第 34 章一处并列举例 | 未读到（arXiv 站内检索只返回一篇无关的 Puffin-World） | — | 2026-10-09 | **抓取未成** ⇒ 继续记 [推]，正文那句已归在"二手栏" |
''')
print('ok 抓取表追加 2 行')

io.open('bible/sources.md', 'a', encoding='utf-8', newline='\n').write('''
- 2026-10-09 第三轮：`arxiv.org/html/2501.03575v3`（Cosmos World Foundation Model Platform）逐字读到
  `two base models that are 4B and 12B in size`、`Cosmos-Predict1-4B / -12B`、`single NVIDIA A100 GPU with 80GB memory`。
  ⇒ **4B 这个输入升一手**，正文那条 8 GB ÷ 16 GB 的算术不再依赖"Edge 4B 能在 Orin/Thor 上跑"；
  档位名 Super/Nano/Edge 与 Orin/Thor 那句**一手没有**，降 [推]。GAIA-2 的分辨率一手未取到，仍 [推]。
''')
print('ok sources.md 追加')

io.open('verification/pending-fixes-2026-10-08.md', 'a', encoding='utf-8', newline='\n').write('''
## F-35 Cosmos：把 4B 与"Edge 能在 Orin 上跑"拆开（2026-10-09）

一手论文只写 `4B and 12B in size` 与 `Cosmos-Predict1-4B / -12B`，通篇没有 Nano / Super / Edge，也没有 Jetson / Orin / Thor。
第 34 章原先把"Edge 4B（Orin/Thor 可跑）"整条当 [查]，现在**拆成两截**：
`4B` 升一手并附逐字；档位名与"可跑"降 [推]，并注明"正文那条 8 GB ÷ 16 GB 模组的算术不靠后半句"（4B × 2 = 8 GB 是 [算]）。
**方法上的收获**：一个厂商口径要拆到"哪一半有原话、哪一半是新闻稿"，否则一半被证伪会连累另一半可用的数；
第 26 章的带宽账正好只需要 4B 那一半，所以拆完之后论证反而更干净。
''')
print('ok F-35 已记录')
