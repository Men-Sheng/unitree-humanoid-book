import io

NL = chr(10)
STAR = 'π' + chr(92) + '*0.6'   # 正文里必须这么写，否则 Markdown 吃掉星号（第 113 条）
FAIL = []


def sub(u, old, new, must=True):
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    old = old.replace('PIST', STAR)
    new = new.replace('PIST', STAR)
    n = t.count(old)
    if n != 1:
        FAIL.append((u, n, old[:52]))
        return False
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new))
    print('ok u%s：%s' % (u, old[:38]))
    return True


R = 'research/other-vendor-firsthand.md'
T = 'research/humanoid-stack-specs.md'

sub('29', '0.6%、60%、85%、17%、12.6 ms 是 [算]',
    '0.6%、60%、85%、17%、12.6 ms 是 [算]；**而 12.6 ms 的输入（63 ms/块、5 去噪步）本身是二手**——官网对带桌面 UA 的请求返回 429，本书未读到原文 [推]，所以这条除法只支持量级')

sub('30', '机器人端只执行，推理在 GPU 侧（可 websocket 远程） [查]',
    '机器人端只执行，推理在 GPU 侧（可 websocket 远程） [推]（官网 429，未读到原文）')

sub('30', 'SmolVLA     总 450M         +  动作专家约 100M',
    'SmolVLA     总 450M 一手；主干与专家如何分栏未公布 [未]')

sub('30', 'GE-Act      160M 并行 flow-matching 解码器',
    'GE-Act      160M 自回归动作解码器 [查]（原稿曾写 flow-matching，已按一手收回）')

sub('30', '各家主干型号、参数、频率、horizon、部署门槛，全部来自厂商公开仓库/论文/产品页 [查][厂]，本书逐条标注',
    '各家主干型号、参数、horizon、部署门槛里，已逐字读到原文的记 [查]（Helix、GR00T、GAIA-2、DROID、π0、Cosmos 3 Edge，逐条原文见 `' + R + '`）；PIST 那一组的 63 ms/5 步/50 Hz 是 [推]（官网 429 未读到）。**[厂] 只留给宇树，别家一律不用**')

sub('30', '高 10–40 倍', '高 5–40 倍（5–10 Hz 对 50–200 Hz 两个端点之比）', must=False)

sub('31', '而 PIST 公开口径是 63 ms/块（H100 单卡 5 去噪步）[查]',
    '而 PIST 公开口径是 63 ms/块（H100 单卡 5 去噪步）[推]（官网 429，本书没读到原文）')

sub('31', 'π 系官方就是这么做的 [查]',
    'π 系官方就是这么做的 [推]；同型做法有一手原话可引：NVIDIA 写 `Because the next chunk is ready before the current one finishes, the arm moves continuously` [查]（第 34 章摊开）')

sub('34', '要生成的：5 s × 20 帧/s = 100 帧；每帧 1,280 × 720 × 3 = 2.76×10⁶ B（8-bit RGB）',
    '要生成的：5 s × 24 帧/s = 120 帧（24 是一手：Genie 3 原文 `24 frames per second`）；每帧 1,280 × 720 × 3 = 2.76×10⁶ B（8-bit RGB）')

sub('34', '          ⇒ 100 × 2.76×10⁶ = 2.8×10⁸ B', '          ⇒ 120 × 2.76×10⁶ = 3.3×10⁸ B')

sub('34', '比值     = 2.8×10⁸ ÷ 2.9×10⁴ ≈ 10⁴ 倍', '比值     = 3.3×10⁸ ÷ 2.9×10⁴ ≈ 1.1×10⁴ 倍')

sub('34', '控制要的：5 s × 50 Hz × 29 关节 × 4 B = 2.9×10⁴ B（G1 的 29 个关节角，FP32）',
    '控制要的：5 s × 50 Hz × 29 个自由度 × 4 B = 2.9×10⁴ B（G1 取官方 `g1_29dof` 那一版的 29；第 03 章 BOM 里的 23 是**关节模组数**，两个口径不是一回事，别混用）')

sub('34', '- [ ] 再算一遍表示的量级：5 s × 20 fps × 1,280 × 720 × 3 B ≈ 2.8×10⁸ B',
    '- [ ] 再算一遍表示的量级：5 s × 24 fps（一手）× 1,280 × 720 × 3 B ≈ 3.3×10⁸ B')

sub('34', '宇树 WMA-0 两用与 15 Hz [厂]（自陈）',
    '宇树 WMA-0 的两用口径 [厂]（自陈）；**15 Hz 已撤回**——那是 NVIDIA Cosmos 3 Edge 在 Thor T5000 上的数，宇树 WMA-0 的页面与仓库对 Hz 零命中 [未]')

sub('34', '1 kHz 的关节环，第 12、27 章那条总线的节拍 [厂]',
    '1 kHz 的关节环（这个量级来自腿式控制综述 [行]，宇树未公布 [未]），对 1 ms 这个本书自选的分母')

sub('33', '3,600 ÷ 4.2 ≈ 868', '3,600 ÷ 4.2 ≈ 857')

sub('30', '宇树 UnifoLM-WMA-0 的仓库里有 `action_model/flow_matching_head/` 这个目录 [厂]，但官方文字口径从未确认动作头形式 [未]',
    '宇树 org 下**另一族**仓库 `unifolm-wla` 的结构记录里有 `unifolm_wla/model/modules/action_model/flow_matching_head/` 这组目录名 [厂]；**WMA-0 自己的文件清单里没有它**（旧稿把两族混成一族，本轮按 `' + T + '` 的逐仓库清点改正）。两家的官方文字都没确认动作头形式 [未]',
    must=False)

sub('34', '仓库里确有 `action_model/flow_matching_head/` 这个目录名 [厂]',
    '（更正：`flow_matching_head/` 那组目录名记在宇树**另一族**仓库 `unifolm-wla` 的结构清单里，WMA-0 自己的清单没有 [厂]；旧稿把两族混成一族）',
    must=False)

sub('31', '这张分层表沿用第 00 章',
    '这张表是本章按推理节奏重切的，编号与第 00 章那张六层表不一致（那里的 ③ 是任务与决策、⑤ 是关节伺服）',
    must=False)

print('\n未匹配（没改）%d 条：' % len(FAIL))
for u, n, o in FAIL:
    print('  u%s count=%d  %s' % (u, n, o))
