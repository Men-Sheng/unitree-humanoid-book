import io

# 把 2026-10-09 别家一手抓取的结果写回正文标记：Helix/GR00T 升级为已读到原文的 [查]，
# π*0.6 那组数因为官网 429 拦住，按本书自己的定义从 [查] 降回 [推]。
E = [
    ('29', 'π*0.6 公开口径是 H100 单卡 5 个去噪步、一块 63 ms [查]',
     'π*0.6 的公开口径是 H100 单卡 5 个去噪步、一块 63 ms——**这组数本书没有读到原文**：'
     '官网 `research/pi-star-0.6` 与 `research` 两页对带桌面 UA 的请求一律返回 429，arXiv 检索 0 条，'
     '所以按本书图例只能记 [推]（二手转述，未读到原文），用它的推论只支持量级'),
    ('30', 'Helix 是 80 M ÷ 7 B ≈ 87 倍',
     'Helix 是 80 M ÷ 7 B ≈ 87 倍（**7 B 与 80 M 都是 Figure 自己那篇 blog 的原话**，'
     '2026-10-09 逐字核过：`S2 is built on a 7B-parameter open-source, open-weight VLM`、'
     '`S1, an 80M parameter cross-attention encoder-decoder transformer`、`operating at 7-9 Hz`、'
     '`continuous robot actions at 200 Hz` [查]）'),
    ('34', '**没有检索到任何 Hz 或 ms 的运行频率** [未]',
     '**没有检索到任何 Hz 或 ms 的运行频率**（README 全篇 `Hz`、`ms`、`control rate`、`frequency`、`real-time` '
     '五个词零命中，只有目录树里一行 `unitree_deploy  # Deployment code`）[未]'),
]
for u, old, new in E:
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    if t.count(old) != 1:
        print('!! u%s 锚点 count=%d：%s' % (u, t.count(old), old[:44]))
        continue
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    print('ok u%s 标记已按抓取结果调整' % u)

SRC = 'bible/sources.md'
io.open(SRC, 'a', encoding='utf-8', newline='\n').write('''

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
''')
print('ok sources.md 追加 G1 抓取记录')

PF = 'verification/pending-fixes-2026-10-08.md'
io.open(PF, 'a', encoding='utf-8', newline='\n').write('''
## F-32 别家一手抓取表开工（2026-10-09）

新建 `research/other-vendor-firsthand.md`（会被第 0 步收进附录 E.3）。本轮 12 格里：
一手证实 8 格（Helix 四条 + GR00T 四条）、一手未载 2 格（WMA-0 的频率、GR00T 的 Hz）、抓取被拦 1 组（π*0.6 全部四个数）。
据此动了三处正文标记：第 30 章 Helix 那处补上逐字原文并确认可标 [查]；第 34 章 WMA-0 的"零命中"写成可复现的阴性记录；
第 29 章 π*0.6 那组数按 `[查]=已读到原文` 的定义**降回 [推]**，并写明 429 与 arXiv 0 条这两条失败路径。
**仍未抓的一手**：1X（14 B / 11 s / 1 s）、Genie 3（720p / 20–24 fps）、GAIA-2 分辨率、GE-Act、AgiBot World 的数采口径、
DROID、SmolVLA、π0/π0.5 的流匹配步数。这些补齐前，第 29–34 章以它们为输入的推论只支持量级——正文每处都挂着这句。
''')
print('ok pending-fixes 追加 F-32')
