import io

NL = chr(10)
E = [
    # π0：一手实证 10 个积分步
    ('30', '流匹配通常 5–10 步。',
     '流匹配通常 5–10 步。**π0 给出一手实证**：论文原话 `10 integration steps`、`3.3 billion parameters`，'
     '动作时域 `H=50`、控制频率 50 Hz [查]（arXiv 2410.24164）。'),
    # GAIA-2：从二手栏升到一手（两处）
    ('34', 'GAIA-2 的 5 路 448×960',
     'GAIA-2 的 `up to five temporally and spatially consistent camera streams`、`resolution of 448×960`、'
     '`each spanning 2 seconds`、`8.4B parameters`（**2026-10-09 已读到 Wayve 论文原文** [查]，'
     'arXiv 2503.20523；旧稿这组数属二手，现已升一手）'),
    # DROID 与 AgiBot 的数已一手，别的仍是媒体口径
    ('33', '所有单价、时长、轨迹数、GPU 卡数与天数来自媒体报道、论文与厂商宣传页 [推][查]，'
     '**本书只取数量级与曲线形状**',
     '轨迹数与时长里，**DROID 与 AgiBot World 已逐字读到论文原文** [查]'
     '（DROID：`76k demonstration trajectories`、`350 hours of interaction data`、`84 tasks`、`564 scenes`；'
     'AgiBot：`1,001,552 trajectories`、`2976.4 hours`）；'
     '而**单价、GPU 卡数与天数仍来自媒体报道与厂商宣传页** [推]——'
     '本书只取数量级与曲线形状'),
]
for u, old, new in E:
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    n = t.count(old)
    if n == 0:
        print('!! u%s 锚点没找到：%s' % (u, old[:44]))
        continue
    t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t)
    print('ok u%s 替换 %d 处：%s' % (u, n, old[:36]))

# 第 34 章那句"分栏"里，把 GAIA-2 从二手挪到一手
p = 'drafts/unit-34/draft.md'
t = io.open(p, encoding='utf-8').read()
old = '**仍在二手栏、且本轮没能升到一手的**：1X 的 14 B / 11 s / 1 s、GE-Act 的 160 M / 200 ms / 54 步、GAIA-2 的 5 路 448×960、'
new = '**仍在二手栏、且本轮没能升到一手的**：1X 的 14 B / 11 s / 1 s、GE-Act 的 160 M / 200 ms / 54 步、'
if t.count(old) == 1:
    t = t.replace(old, new)
    t = t.replace('GR00T 的 3 B 主干 / horizon 40 / 132 维 / 16 GB+ 起步。',
                  'GR00T 的 3 B 主干 / horizon 40 / 132 维 / 16 GB+ 起步；GAIA-2 的五路 448×960 与 8.4 B；'
                  'DROID 的 76k 条 / 350 h / 84 任务 / 564 场景；π0 的 10 个积分步。')
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t)
    print('ok 第 34 章的分栏句子把 GAIA-2 移进一手栏（并补 DROID、π0）')
else:
    print('!! 分栏锚点 count=%d' % t.count(old))

R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline=NL).write(NL.join([
    '| π0 的去噪步数与规模 | 第 30 章“5–10 步”、第 29 章的每步成本 | `10 integration steps`；`3.3 billion parameters`；`H=50`；控制频率 50 Hz | https://arxiv.org/html/2410.24164v1 | 2026-10-09 | **一手证实**（5–10 步这个通例有了一手的 10） |',
    '| GAIA-2 的多路与分辨率 | 旧稿 5 路 448×960 [推] | `up to five temporally and spatially consistent camera streams`；`resolution of 448×960`；`each spanning 2 seconds`；`8.4B parameters` | https://arxiv.org/html/2503.20523v1 | 2026-10-09 | **一手证实** ⇒ 升 [查]，并从"二手栏"移到"一手栏" |',
    '| DROID 规模 | 第 33 章 16.6 s 每条的输入 | `76k demonstration trajectories`；`350 hours of interaction data`；`84 tasks`；`564 scenes` | https://arxiv.org/abs/2403.12945 | 2026-10-09 | **一手证实**（`350 × 3,600 ÷ 76,000 = 16.6 s` 成立）；HTML 版 404，用 abs 页读到 |',
    '',
]))
print('ok 抓取表追加 3 行')

io.open('bible/sources.md', 'a', encoding='utf-8', newline=NL).write(NL + (
    '- 2026-10-09 第四轮（arXiv 全文页 / abs 页）：π0 `10 integration steps` + `3.3 billion parameters` + `H=50` + 50 Hz'
    '（2410.24164）；GAIA-2 `up to five … camera streams`、`resolution of 448×960`、`each spanning 2 seconds`、`8.4B parameters`'
    '（2503.20523）；DROID `76k demonstration trajectories`、`350 hours of interaction data`、`84 tasks`、`564 scenes`'
    '（2403.12945，**html v3 是 404，abs 页可用**）。⇒ 第 30 章"5–10 步"、第 33 章 16.6 s 每条、第 34 章 GAIA-2 那组数升 [查]。'
    '仍未取到：GE-Act、SmolVLA、Cosmos 2026 的 Super/Nano/Edge 档位名、1X 的 11 s。\n'))
print('ok sources.md 追加')
