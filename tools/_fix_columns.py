import io

NL = chr(10)
P = 'drafts/unit-34/draft.md'
lines = io.open(P, encoding='utf-8').read().split(NL)
idx = [i for i, l in enumerate(lines) if l.startswith('这批数从这一版起分成两栏看')]
assert len(idx) == 1, idx
new = ('这批数从这一版起分成两栏看。**已升到一手**（逐字读过厂商页面或论文原文）：Genie 3 的 720p / 24 fps / 数分钟一致性；'
       'Helix 的 7 B / 80 M / 7–9 Hz / 200 Hz；GR00T 的 3 B 主干 / horizon 40 / 132 维 / 16 GB+ 起步；'
       'GAIA-2 的 `up to five temporally and spatially consistent camera streams`、`resolution of 448×960`、`8.4B parameters`；'
       'DROID 的 `76k demonstration trajectories`、`350 hours of interaction data`、`84 tasks`、`564 scenes`；'
       'π0 的 `10 integration steps`、`3.3 billion parameters`。**仍在二手栏**：1X 的 14 B / 11 s / 1 s、'
       'GE-Act 的 160 M / 200 ms / 54 步、SmolVLA 的 100 M / 450 M、Cosmos 2026 的 Super / Nano / Edge 档位名。'
       '**取数的手艺也记一笔**：`export.arxiv.org/api/query` 四条检索全返回空响应，'
       '换 `arxiv.org/html/<id>` 全文页与 `arxiv.org/abs/<id>` 就读到了（html 有版本坑：某篇的 v3 是 404，abs 页可用）。'
       '成功与失败都逐条记在 `research/other-vendor-firsthand.md` 与 `bible/sources.md` 的 G1 节。')
lines[idx[0]] = new
io.open(P, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
print('ok 分栏那句重写（GAIA-2 / DROID / π0 移到一手栏，二手栏只剩真没取到的）')

# 上一句"一，多数是论文与新闻稿级"里，GAIA-2 已经带上了"已读到原文"，
# 那么那句的总起就得改口，否则又是自相矛盾。
t = NL.join(lines)
old = '**一，多数是论文与新闻稿级。**'
new2 = '**一，这批数里多数曾是论文与新闻稿级，但已经开始分化（见下面那句分栏）。**'
if t.count(old) == 1:
    io.open(P, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new2))
    print('ok 总起句同步改口')
else:
    print('· 总起句 count=%d，未改' % t.count(old))
