import io

NL = chr(10)

def patch(u, old, new, must=True):
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    n = t.count(old)
    if n != 1:
        print('!! u%s 锚点 count=%d：%s' % (u, n, old[:50]))
        if must:
            return False
        return False
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new))
    print('ok u%s：%s' % (u, old[:42]))
    return True

# ① 分类错误：GE-Act 是自回归解码器，不是流匹配
patch('30',
      'GE-Act。宇树 UnifoLM-WMA-0 的仓库里有',
      'GE-Act **不属于这一类**：一手原文写它是 `a lightweight 160M-parameter autoregressive action decoder`'
      '——**autoregressive**（自回归解码器）[查]，把它列在流匹配代表里是原稿的分类错误，就此更正。'
      '宇树 UnifoLM-WMA-0 的仓库里有')

# ② SmolVLA：450 M 是**总参数**，主干/专家分栏未公布 ⇒ 那一句倍数算不出来
patch('30',
      'SmolVLA 约 100 M ÷ 450 M ≈ 4.5 倍（这两个数是二手口径，本轮没读到一手页面 [推]）',
      'SmolVLA 这一家**算不出这个倍数**：一手只给总规模 `4.5亿参数`（450 M）与动作头是 Flow-Matching Transformer，'
      '主干与动作专家各占多少**没有公布** [未]（旧稿拿 100 M ÷ 450 M 当"专家 ÷ 主干"是用错了口径，'
      '450 M 是总和而不是主干）')

# ③ 范围那句要跟着改口：只有一手的 Helix 撑得住"87 倍"
patch('30',
      '**动作专家比主干小的倍数横跨 4.7–87 倍**：π*0.6 是 860 M ÷ 4 B ≈ 4.7 倍，',
      '**动作专家比主干小多少，公开口径只有两家给得起**：Helix 是 80 M ÷ 7 B ≈ 87 倍（两边都是一手原话）；'
      'π*0.6 是 860 M ÷ 4 B ≈ 4.7 倍（**二手**，官网 429 没读到原文）。')

# ④ 第 34 章 GE-Act 那格：降 [推] 的话要收回，改成一手
patch('34',
      '（160 M、200 ms 出 54 步——**本轮 arXiv 检索这条没有任何结果，一手没读到，降为 [推]**）',
      '（一手：`a lightweight 160M-parameter autoregressive action decoder`、'
      '`54-step torque trajectories within 200 ms on a commodity GPU`、30 Hz，计时在 `onboard NVIDIA RTX 4090 GPU`'
      ' [查]，arXiv 2508.05635v3。**注意它是自回归解码器**，第 30 章原先把它列进流匹配代表是分类错，已更正）')

# ⑤ 分栏那句里 GE-Act 从二手栏搬到一手栏，SmolVLA 改成"未公布分栏"
patch('34',
      '**仍在二手栏**：1X 的 14 B / 11 s / 1 s、GE-Act 的 160 M / 200 ms / 54 步、SmolVLA 的 100 M / 450 M、Cosmos 2026 的 Super / Nano / Edge 档位名。',
      '**仍在二手栏**：1X 的 14 B / 11 s / 1 s、Cosmos 2026 的 Super / Nano / Edge 档位名。'
      '另有两家是**一手但没公布你要的那一格**：SmolVLA 只给总参数 450 M，主干/专家分栏未公布；'
      'GR00T 只给主干 3 B，动作专家规模未单独公布。**没有分栏就算不出倍数，这跟"数不准"是两回事**。')

patch('34',
      'π0 的 `10 integration steps`、`3.3 billion parameters`。',
      'π0 的 `10 integration steps`、`3.3 billion parameters`；GE-Act 的 160 M 自回归解码器与 54 步 ÷ 200 ms。')

# ⑥ 抓取表与来源记录
io.open('research/other-vendor-firsthand.md', 'a', encoding='utf-8', newline=NL).write(NL.join([
    '| GE-Act 的规模 / 步数 / 延迟 | 第 34 章表内 | `GE-Act is a lightweight 160M-parameter autoregressive action decoder`；`54-step torque trajectories within 200 ms on a commodity GPU`；30 Hz；计时 `onboard NVIDIA RTX 4090 GPU` | https://arxiv.org/html/2508.05635v3（Genie Envisioner） | 2026-10-09 | **一手证实**；**且推翻一处分类**：它是自回归解码器，不是流匹配头 ⇒ 第 30 章的代表列表已更正 |',
    '| SmolVLA 的主干 / 专家分栏 | 旧稿 `100 M ÷ 450 M ≈ 4.5 倍` | 一手只给 `4.5亿参数`（450 M 总规模）与动作头 `Flow-Matching Transformer`；**主干与专家分栏未公布** | https://smolvla.net/ | 2026-10-09 | **一手只到总规模** ⇒ 那句倍数删除并说明"没分栏就算不出倍数"；450 M 被旧稿当成主干是用错口径 |',
    '| π0 的积分步数 | 第 30 章“5–10 步” | `10 integration steps`；`3.3 billion parameters`；`H=50`；50 Hz | https://arxiv.org/html/2410.24164v1 | 2026-10-09 | **一手证实** |',
    '| GAIA-2 的多路与分辨率 | 旧稿 [推] | `up to five temporally and spatially consistent camera streams`；`resolution of 448×960`；`each spanning 2 seconds`；`8.4B parameters` | https://arxiv.org/html/2503.20523v1 | 2026-10-09 | **一手证实** ⇒ 升 [查] |',
    '| DROID 规模 | 第 33 章 16.6 s 每条 | `76k demonstration trajectories`；`350 hours of interaction data`；`84 tasks`；`564 scenes` | https://arxiv.org/abs/2403.12945（html v3 返回 404） | 2026-10-09 | **一手证实** |',
    '',
]))
print('ok 抓取表追加 5 行')

io.open('bible/sources.md', 'a', encoding='utf-8', newline=NL).write(NL + (
    '- 2026-10-09 第五轮：Genie Envisioner（arXiv 2508.05635v3）一手读到 GE-Act 是 '
    '`a lightweight 160M-parameter autoregressive action decoder`，输出 `54-step torque trajectories within 200 ms on a commodity GPU`、30 Hz、'
    '计时在 `onboard NVIDIA RTX 4090 GPU` ⇒ 第 34 章那格升 [查]；**同时推翻第 30 章一处分类**（原稿把 GE-Act 列为流匹配代表，实为自回归解码器）。\n'
    '- SmolVLA 官方页只给总规模 `4.5亿参数` 与动作头 `Flow-Matching Transformer`，**主干/专家分栏未公布** '
    '⇒ 旧稿 `100 M ÷ 450 M ≈ 4.5 倍` 不仅没出处，还把总规模当成了主干，是**口径用错**；正文改为明说"算不出倍数"。\n'
    '- 公开口径里能算"专家 ÷ 主干"的只剩两家：Helix 80 M ÷ 7 B ≈ 87 倍（两边一手）、π*0.6 860 M ÷ 4 B ≈ 4.7 倍（二手，官网 429）。\n'))
print('ok sources.md 追加')
