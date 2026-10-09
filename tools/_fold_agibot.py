import io

E = [
    ('33', '它同时给了 1,001,552 条与 2,976.4 小时（arXiv 2503.06669 [查]）：',
     '它同时给了 1,001,552 条与 2,976.4 小时——**2026-10-09 逐字读到论文全文** [查]：'
     '`The latest version contains 1,001,552 trajectories, with a total duration of 2976.4 hours.`、'
     '`covering 217 specific tasks, 87 skills, and 106 scenes.`、`A suite of 100 dual-arm humanoid robots is deployed.`、'
     '`spans over 4,000 square meters.`：'),
    ('33', '公开口径：4,000 ㎡ 数采基地',
     '公开口径（4,000 ㎡ 与 100 台已在论文全文里逐字核到：`spans over 4,000 square meters`、'
     '`A suite of 100 dual-arm humanoid robots is deployed` [查]；**但论文没有给任何“每天产多少条”的产出率**，'
     '只写 `episodes typically span approximately 30 seconds, some of which last over 2 minutes`——'
     '所以“日产 1,000 条”这类数仍属媒体口径 [推]）：4,000 ㎡ 数采基地'),
    ('34', '（160 M、200 ms 出 54 步 [查]）',
     '（160 M、200 ms 出 54 步——**本轮 arXiv 检索这条没有任何结果，一手没读到，降为 [推]**）'),
    ('30', 'SmolVLA 约 100 M ÷ 450 M ≈ 4.5 倍',
     'SmolVLA 约 100 M ÷ 450 M ≈ 4.5 倍（这两个数是二手口径，本轮没读到一手页面 [推]）'),
]
for u, old, new in E:
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    if t.count(old) != 1:
        print('!! u%s count=%d  %s' % (u, t.count(old), old[:40]))
        continue
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    print('ok u%s  %s' % (u, old[:34]))

R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline='\n').write('''
| AgiBot World 轨迹数与时长 | 第 33 章口径 B 的两个输入 | `The latest version contains 1,001,552 trajectories, with a total duration of 2976.4 hours.` | https://arxiv.org/html/2503.06669v1 | 2026-10-09 | **一手证实**（10.7 s/条 那条除法成立） |
| AgiBot World 规模与场景 | 217 任务 | `covering 217 specific tasks, 87 skills, and 106 scenes.` | 同上 | 2026-10-09 | **一手证实** |
| 数采基地面积与台数 | 旧稿只有媒体口径 [查] | `spans over 4,000 square meters.`；`A suite of 100 dual-arm humanoid robots is deployed.` | 同上 | 2026-10-09 | **一手证实**（升 [查]） |
| 单条时长 | 第 33 章"30 s 一条" | `episodes typically span approximately 30 seconds, some of which last over 2 minutes.` | 同上 | 2026-10-09 | **一手证实** |
| 日产条数（1,000 条/天之类） | 正文当量级用 | **论文全文没有给任何产出率** | 同上（负面结果） | 2026-10-09 | **一手未载** ⇒ 降 [推]，正文明写"仍属媒体口径" |
| GE-Act 的 160 M / 200 ms / 54 步 | 第 34 章表内 | 未读到：arXiv 站内检索 `Genie Envisioner / GE-Act` **返回 0 条** | — | 2026-10-09 | **抓取未成** ⇒ 降 [推] |
| SmolVLA 的 100 M / 450 M | 第 30 章那条倍数 | 未读到一手页面 | — | 2026-10-09 | **抓取未成** ⇒ 标 [推] |
''')
print('ok 抓取表追加 7 行（含 3 条负面结果）')

io.open('bible/sources.md', 'a', encoding='utf-8', newline='\n').write('''
- 2026-10-09 第二轮：**arXiv 的 HTML 全文页可稳定读到**（`arxiv.org/html/2503.06669v1`），
  AgiBot World 的 `1,001,552 trajectories / 2976.4 hours / 217 tasks / 87 skills / 106 scenes / 100 dual-arm humanoid robots / 4,000 square meters /
  episodes typically span approximately 30 seconds` 全部逐字核到 ⇒ 第 33 章那条除法与 4,000 ㎡、100 台升为 [查]。
  **负面结果同样存档**：论文没有任何"日产多少条"的产出率 ⇒ 媒体那句降回 [推]；GE-Act 与 SmolVLA 的一手页面本轮检索不到 ⇒ 降 [推]。
''')
print('ok sources.md 追加')

io.open('verification/pending-fixes-2026-10-08.md', 'a', encoding='utf-8', newline='\n').write('''
## F-34 AgiBot 那组数升到一手，三处降回 [推]（2026-10-09）

**升**：第 33 章口径 B 的两个输入（1,001,552 条 / 2,976.4 h）在 arXiv HTML 全文页逐字读到，`10.7 s 每条` 那条除法现在站在原话上；
4,000 ㎡ 与 100 台双臂机、217 任务 / 87 技能 / 106 场景、`episodes typically span approximately 30 seconds` 一并升 [查]。
**降**：论文**没有给任何产出率** ⇒ "日产 1,000 条"这类数从 [查] 降回 [推]，正文改成"论文没给，仍属媒体口径"；
GE-Act 的 160 M / 200 ms / 54 步与 SmolVLA 的 100 M / 450 M 本轮 arXiv 检索 0 条，**一手没读到就降 [推]**，第 30 章那条倍数后面就地注明。
方法结论：**`arxiv.org/html/<id>v1` 比 `export.arxiv.org/api/query` 可靠得多**（后者本轮四条检索全返回空响应），
下次抓别家一手直接走 HTML 全文页 + 逐字引用 + 负面结果也记。
''')
print('ok F-34 已记录')
