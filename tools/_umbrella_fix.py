import io

NL = chr(10)


def rep(u, old, new, must=True):
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    n = t.count(old)
    if n != 1:
        print('!! u%s count=%d：%s' % (u, n, old[:44]))
        return False
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new))
    print('ok u%s：%s' % (u, old[:34]))
    return True


rep('30', '异步双系统（低频语义规划 / 高频动作跟随）           [查]',
    '异步双系统（低频语义规划 / 高频动作跟随）           [推]（只见到媒体转述，智元官方页本轮未逐字读到）')

rep('33', '2026 年 9 月的公开口径（媒体与厂商混合，全部标 [推][查]）：',
    '2026 年 9 月的公开口径（媒体与厂商混合）：**本节的数只有两处逐字读到论文原文**'
    '（DROID 与 AgiBot World，见本章证据栏与 `research/other-vendor-firsthand.md`），其余一律按 [推] 用，只比较曲线形状：')

rep('33', '公开可查的数（全部 [查]，且各家口径不同，**不可直接相减**）：',
    '公开可查的数（**除 DROID 与 AgiBot World 已逐字核到之外均为媒体口径 [推]**，且各家口径不同，**不可直接相减**）：')

rep('33', '**最后一个失效条件最硬：以上单价全部是 2026 年 9 月的二手口径** [推][查]。',
    '**最后一个失效条件最硬：以上单价全部是 2026 年 9 月的二手口径** [推]（只有 DROID/AgiBot 的轨迹数与时长读到过原文 [查]）。')

rep('33', '北京人形数据基地提到过 95%+ 的合格率 [查]，这已经是罕见的透明。',
    '北京人形数据基地提到过 95%+ 的合格率 [推]（媒体转述，本书未读到基地官方原文），这已经是罕见的透明——'
    '**透明的是"敢给一个数"，可核对性并没有解决：它既没有分母定义，也没有第三方复算路径。**')

rep('33', '（[算]，输入是 [推][查] 口径，租用价是市场公开价量级。）',
    '（[算]，输入除 DROID/AgiBot 外是 [推] 口径，租用价是市场公开价量级 [行]。）')

# 台账补三行（Helix 端侧 GPU 一手、LeRobot 一手、GO-2 未取到）
R = 'research/other-vendor-firsthand.md'
io.open(R, 'a', encoding='utf-8', newline=NL).write(NL.join([
    '| Helix 完全端侧这件事 | 第 30 章表内"完全端侧（双低功耗嵌入式 GPU）" | `Helix is the first VLA that runs entirely onboard embedded low-power-consumption GPUs`；`dual low-power-consumption embedded GPUs` | https://www.figure.ai/news/helix | 2026-10-09 | **一手证实**（但芯片型号与功耗原文未给 ⇒ 那两格仍 [未]） |',
    '| LeRobot 官方文档的循环实测 | 第 29、33 章 | 目标 `30 Hz (33.3 ms budget per tick)`、实测 `29.88 Hz`、`16/1198 ticks 超时（1.3%）`、work mean `18.4 ms` / worst `45.1 ms`、`observe` 占 74% | https://github.com/huggingface/lerobot（`docs/source/il_robots.mdx` 行 420-434，抓取记于 `bible/sources.md` G0） | 2026-10-09 | **一手证实**（是 Hugging Face 的仓库文件，按图例记 [查] 不是 [厂]） |',
    '| GO-2 / ACoT-VLA 的异步双系统 | 第 30 章表内 | **未取到一手**：检索只回到媒体与百科（ai-bot.cn、CSDN、sohu、eefocus），智元官方页无逐字原文 | — | 2026-10-09 | **抓取未成** ⇒ 正文降 [推] |',
    '',
]))
print('ok 台账补 3 行')

# 门：认 token 之外再加一条——行内出现 arXiv id / URL 时，用它在台账里找
G = 'tools/check_vendor_ledger.py'
t = io.open(G, encoding='utf-8').read()
old = "            hits = [k for k in TOKENS if k in low]"
assert t.count(old) == 1, t.count(old)
t = t.replace(old, "            hits = [k for k in TOKENS if k in low]\n"
                   "            hits += [m.group(0) for m in re.finditer(r'\\d{4}\\.\\d{4,5}', line)]\n"
                   "            hits += [m.group(0) for m in re.finditer(r'https?://[\\w./-]+', line) if m.group(0).rstrip('/') in led]")
io.open(G, 'w', encoding='utf-8', newline=NL).write(t)
print('ok 门增加 arXiv id / URL 两条识别路径')
