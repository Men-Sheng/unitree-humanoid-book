import io

# 2026-10-09 抓取结果落到正文：1X 那组数没在一手页面出现 ⇒ 降级并把结论换到一手能核的地上；
# 顺带用一条一手 VLA 实测（10 步 / 27.3 ms / RTX 4090）给"迭代多步要多少钱"一个可复算的锚。
P = 'drafts/unit-34/draft.md'
t = io.open(P, encoding='utf-8').read()
old = '1X 公开的技术口径（[查]）：'
assert t.count(old) == 1, ('u34 锚点', t.count(old))
new = ('1X 那组数**本书没有读到一手出处**：2026-10-09 直接打开官方世界模型页面，逐字只拿到 '
       '`we have trained a world model that serves as a virtual simulator for our robots.` 与 '
       '`World models solve … evaluation.` 两句，**没有 14B、没有 11 s、没有任何 Hz** [未]。'
       '所以下面这串按二手量级读（[推]），本章的结论不靠它成立——靠的是后面那条一手的 24 fps：')
t = t.replace(old, new)

old = '**0.42 倍实时，就是它比世界慢两倍以上。** 再把它放进这本书熟悉的频率阶梯里除三遍：'
assert t.count(old) == 1, ('u34 锚点2', t.count(old))
new = ('**先别急着用这个 0.42。** 它是二手数算出来的，只当量级。**真正立得住的那条除法是下面这个，它的输入全部是原话：**\n\n'
       '```text\n'
       'Genie 3 官方博客原话：24 frames per second，resolution of 720p [查]\n'
       '⇒ 一帧的节奏 = 1 ÷ 24 = 41.7 ms\n'
       '对照第 21 章 50 Hz 的策略环：41.7 ÷ 20 = 2.1 拍\n'
       '对照第 12、27 章那条 1 kHz 关节环：41.7 ÷ 1 = 41.7 拍\n'
       '```\n\n'
       '**这条不需要 11 s 那个数**：就算一个逐帧生成的世界模型真的达到 24 fps 的显示节奏，'
       '它也追不上控制节拍——**帧与拍对不齐，就不成闭环**，因为环要求每一拍都有对应的状态更新。'
       '而真实生成远慢于 24 fps（那句 11 s 说的就是这个差距，只是本书没读到原文，所以只当量级）。'
       '把那两个二手的 12 s 放进熟悉的频率阶梯里再除三遍，看的是同一件事的另一面（**只做量级，别当厂商规格**）：')
t = t.replace(old, new)
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 第 34 章：11 s 降为量级，主线换成一手 24 fps 的除法')

P = 'drafts/unit-30/draft.md'
t = io.open(P, encoding='utf-8').read()
old = '扩散可能几十步，流匹配通常 5–10 步。'
assert t.count(old) == 1, ('u30 锚点', t.count(old))
new = ('扩散可能几十步，流匹配通常 5–10 步。**一条一手能核的样本**：论文《Running VLAs at Real-time Speed》'
       '（arXiv 2510.26742，Dexmal 与 StepFun）报 `after the 10 denoising steps`，主干是 '
       '`a vision encoder SigLIP with 400M parameters and a large language model Gemma with 2.6B parameters`，'
       '两个输入视角下 `achieve a latency of 27.3 ms`、硬件是 `under a single consumer RTX 4090 GPU` [查] '
       '⇒ 每步 27.3 ÷ 10 = 2.73 ms。这个数后面第 29 章要用来对照端侧的带宽账。')
t = t.replace(old, new)
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 第 30 章：给 5–10 步补上一条一手实测')

P = 'drafts/unit-29/draft.md'
t = io.open(P, encoding='utf-8').read()
old = '即 t_step = 63 ÷ 5 = 12.6 ms'
if t.count(old) == 1:
    new = ('即 t_step = 63 ÷ 5 = 12.6 ms。**同一个量有一手能核的对照**：arXiv 2510.26742 报 10 个去噪步在单张 RTX 4090 上 '
           '`a latency of 27.3 ms` ⇒ 每步 2.73 ms [查]，比那个二手口径还快 4.6 倍——**所以"每步十几毫秒"不是瓶颈，'
           '把 12.6 ms 换成 2.73 ms，下面那条与带宽的对比只会更极端**')
    t = t.replace(old, new)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    print('ok 第 29 章：补上一条一手对照，并说明它只会加强结论')
else:
    print('!! 第 29 章锚点 count=', t.count(old))

R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline='\n').write('''
| 1X 世界模型的角色 | 第 34 章用它讲"评测" | `we have trained a world model that serves as a virtual simulator for our robots.`；`World models solve a very practical and yet often overlooked challenge when building general-purpose robots: evaluation.` | https://www.1x.tech/discover/1x-world-model | 2026-10-09 | **一手证实角色，但 14B / 11 s / 1 s 与任何 Hz 在一手页面里全部 absent** ⇒ 这组数降为 [推]，第 34 章的主线改跑在一手的 24 fps 上 |
| 每步去噪的一手实测 | 第 29 章 t_step、第 30 章"5–10 步" | `after the 10 denoising steps`；`composed of a vision encoder SigLIP with 400M parameters and a large language model Gemma with 2.6B parameters`；`achieve a latency of 27.3 ms given two input views`；`under a single consumer RTX 4090 GPU` | https://arxiv.org/html/2510.26742v1（Running VLAs at Real-time Speed，Dexmal 与 StepFun） | 2026-10-09 | **一手证实** ⇒ 27.3 ÷ 10 = 2.73 ms/步，比二手口径的 12.6 ms 快 4.6 倍 |
''')
print('ok 抓取表追加两条')

io.open('verification/pending-fixes-2026-10-08.md', 'a', encoding='utf-8', newline='\n').write('''
## F-33 世界模型那一节换到一手地基（2026-10-09）

1X 官方页面**只有角色两句原话**（virtual simulator / evaluation），`14B`、`11 s`、`1 s`、任何 Hz 全部没有 ⇒
第 34 章那句"1X 公开的技术口径（[查]）"改成明写"未读到一手出处"，并把 0.42× 实时率降为量级参考；
**主线换成一条输入全是原话的除法**：Genie 3 `24 frames per second` ⇒ 一帧 41.7 ms，
对照 50 Hz 策略环（20 ms）是 2.1 拍、对照 1 kHz 关节环是 41.7 拍 ⇒ **帧与拍对不齐就不成闭环**，
这个结论不需要 11 s 那个数。另一手样本补进第 30、29 章：arXiv 2510.26742 的
`after the 10 denoising steps` + `a latency of 27.3 ms` + `single consumer RTX 4090` ⇒ 2.73 ms/步，
比 π*0.6 那个二手口径的 12.6 ms 还快 4.6 倍——**用它替换只会让带宽那条结论更极端，不会反转**，所以写进去了。
''')
print('ok F-33 已记录')
