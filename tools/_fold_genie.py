import io

# Genie 3 三条数升到一手（DeepMind 博客逐字）；其余未升的写明本轮抓取失败的具体原因。
P = 'drafts/unit-34/draft.md'
t = io.open(P, encoding='utf-8').read()
pairs = [
    ('Genie 3 的 20–24 fps@720p', 'Genie 3 的 24 fps@720p（**已回读到 DeepMind 原文**，逐字：`resolution of 720p`、`24 frames per second`、`retaining consistency for a few minutes` [查]；旧稿多写了一个 20，原文没有）'),
    ('Genie 3 的 20–24 fps@720p 与预览状态', 'Genie 3 的 24 fps@720p 与预览状态'),
]
for old, new in pairs:
    n = t.count(old)
    if n == 0:
        print('· 跳过（已改或无此串）：', old[:34])
        continue
    t = t.replace(old, new)
    print('ok 替换 %d 处：%s' % (n, old[:34]))

anchor = '**二，权重能不能拿到，本身是变量。**'
if t.count(anchor) == 1:
    ins = ('这批数从这一版起分成两栏看。**已升到一手**（逐字读过厂商自己的页面）：Genie 3 的 720p / 24 fps / 数分钟一致性；'
           'Helix 的 7 B / 80 M / 7–9 Hz / 200 Hz；GR00T 的 3 B 主干 / horizon 40 / 132 维 / 16 GB+ 起步。'
           '**仍在二手栏、且本轮没能升到一手的**：1X 的 14 B / 11 s / 1 s、GE-Act 的 160 M / 200 ms / 54 步、GAIA-2 的 5 路 448×960、'
           'Cosmos 的档位划分——arXiv API 那四条检索全返回空、厂商页面对本机的请求限流，失败细节逐条记在 `bible/sources.md` 的 G1 节。'
           '**这两栏的差别不是数准不准，是出了错能不能追责**：一手栏可以给 [查]，二手栏只配 [推]。\n\n')
    t = t.replace(anchor, ins + anchor)
    print('ok 第 34 章新增“一手/二手分栏”一条')
else:
    print('!! 锚点 count=', t.count(anchor))
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline='\n').write('''
| Genie 3 分辨率 | 720p | `resolution of 720p` | https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/ | 2026-10-09 | **一手证实** |
| Genie 3 帧率 | 旧稿写 20–24 fps | `24 frames per second` | 同上 | 2026-10-09 | **一手只写 24 fps** ⇒ 正文删掉 20（多写的那个数没有出处） |
| Genie 3 一致性时长 | 数分钟 | `retaining consistency for a few minutes`（另一句 `few minutes of continuous interaction`） | 同上 | 2026-10-09 | **一手证实**（原文就是"几分钟"，不是分钟数） |
| 1X / GE-Act / GAIA-2 / AgiBot World / SmolVLA | 14 B / 11 s；160 M / 200 ms / 54 步；5 路 448×960；4000 ㎡ 与日产 1000 条；—— | **未取到**：arXiv API 四条检索（`all:"Genie Operator-1"`、`all:"GE-Act"`、`all:"SmolVLA"`、`all:"AGIBOT World"`）**返回空响应**；1X 与 Wayve 的页面本轮未访问 | http://export.arxiv.org/api/query?search_query=all:%22GE-Act%22 | 2026-10-09 | **抓取被拦 / 未取到** ⇒ 这些数继续记 [推]，正文凡以它们为输入的推论只支持量级 |
''')
print('ok 抓取表追加 Genie 3 三条与本轮失败记录')

S = 'bible/sources.md'
io.open(S, 'a', encoding='utf-8', newline='\n').write('''
- 2026-10-09 补充：DeepMind Genie 3 博客**一手读到**（720p / `24 frames per second` / `retaining consistency for a few minutes`），
  据此删掉旧稿"20–24 fps"里那个没有出处的 20。同一轮里 arXiv API 对 `Genie Operator-1` / `GE-Act` / `SmolVLA` / `AGIBOT World`
  四条检索**全部返回空**（不是 404，是空响应），1X 与 Wayve 的厂商页本轮未访问成功 ⇒ 这批数继续记 [推]，**不许因"常见"而升 [查]**。
''')
print('ok sources.md 追加本轮失败与 Genie 3 记录')
