import io

NL = chr(10)

# ---- ① 新门的自检改成四条明确断言（上一版我把期望值绕晕了） ----
P = 'tools/check_vendor_ledger.py'
t = io.open(P, encoding='utf-8').read()
i = t.index('def selftest():')
j = t.index('def main():')
new_st = '''def selftest():
    """四条明确断言：有台账的不误报、没台账的被抓、无厂商 token 的只进清单、台账缺失时自曝没输入。"""
    led = ("| helix | `S2 is built on a 7B-parameter VLM` | figure.ai |\\n"
           "| gr00t | `Base model (3B params)` | github |\\n"
           "π0 `10 integration steps`；droid `76k demonstration trajectories`；cosmos `4B omni-model`；"
           "agibot `1,001,552 trajectories`；gaia `448×960`；smolvla 450m；unifolm 零命中\\n")

    def miss_of(line):
        low = line.lower()
        hits = [k for k in TOKENS if k in low]
        return hits, [k for k in hits if k not in led]

    h1, m1 = miss_of('Helix 的 S1 是 80M [查]')
    ok1 = h1 and not m1
    h2, m2 = miss_of('Gemini Robotics 自陈 44% [查]')
    ok2 = h2 == ['gemini'] and m2 == ['gemini']
    h3, m3 = miss_of('这一行有 [查] 但认不出是谁家的数')
    ok3 = h3 == [] and m3 == []
    real = os.path.exists
    os.path.exists = lambda p: False if str(p).endswith('other-vendor-firsthand.md') else real(p)
    n_empty, orphan_empty, hard_empty = check()
    os.path.exists = real
    ok4 = n_empty is None and len(hard_empty) == 1
    for label, x in [('有台账的 [查] 不误报', ok1), ('没台账的 [查] 被抓到', ok2),
                     ('认不出厂商时不硬判', ok3), ('台账缺失时门自曝没输入', ok4)]:
        print(('PASS ' if x else 'FAIL ') + label)
    bad = [ok1, ok2, ok3, ok4].count(False)
    print('自检 %d/4' % (4 - bad))
    return 0 if bad == 0 else 1


'''
t = t[:i] + new_st + t[j:]
io.open(P, 'w', encoding='utf-8', newline=NL).write(t)
print('ok 自检重写为四条断言')

# ---- ② 第 30 章那句把 Helix 说了两遍、尾巴还挂着一句"一到两个数量级"，整行重写 ----
Q = 'drafts/unit-30/draft.md'
lines = io.open(Q, encoding='utf-8').read().split(NL)
idx = [k for k, l in enumerate(lines) if l.startswith('**动作专家比主干小多少，公开口径只有两家给得起**')]
assert len(idx) == 1, idx
k = idx[0]
removed = lines[k]
lines[k] = ('**动作专家比主干小多少，公开口径只有两家给得起。** Helix 是 80 M ÷ 7 B ≈ 87 倍——两个数都是 Figure 自己那篇博客的原话：'
            '`S2 is built on a 7B-parameter open-source, open-weight VLM`、`S1, an 80M parameter cross-attention encoder-decoder '
            'transformer`、`operating at 7-9 Hz for scene understanding`、`continuous robot actions at 200 Hz.` [查]。'
            'π\\*0.6 是 860 M ÷ 4 B ≈ 4.7 倍，但这组数**本书没读到原文**（官网对带桌面 UA 的请求返回 429），按图例只能记 [推]。'
            'SmolVLA 这一家算不出这个倍数：一手只给总规模 `4.5亿参数`（450 M）与动作头是 Flow-Matching Transformer，'
            '主干与专家如何分栏**没有公布** [未]——旧稿拿 100 M ÷ 450 M 当"专家 ÷ 主干"，是把总数当成了主干。'
            '所以"动作专家比主干小一到两个数量级"这句通例不成立：**够得着一个数量级以上的只有 Helix 一家**，'
            '另一家不到 5 倍；本书按这个事实重写判据——动作专家要小得多，是为了让它能跑在高频（下面讲），'
            '但"小多少"目前没有跨厂商的通例可给。')
io.open(Q, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
print('ok 第 30 章那句重写（去掉重复与悬尾；原句 %d 字符已弃用）' % len(removed))

# ---- ③ 把新门接进第 8 步（软清单，缺台账才判死） ----
S = 'tools/rebuild_all.sh'
sh = io.open(S, encoding='utf-8').read()
anchor = '$PY tools/blueprint_coverage.py || fail'
i = sh.index(anchor)
end = sh.index(NL, i) + 1
add = ('  $PY tools/check_vendor_ledger.py --selftest >/dev/null || fail "check_vendor_ledger 自检"' + NL +
       '  $PY tools/check_vendor_ledger.py || fail "别家一手的 [查] 与台账对不上（见 research/other-vendor-firsthand.md）"' + NL)
sh = sh[:end] + add + sh[end:]
io.open(S, 'w', encoding='utf-8', newline=NL).write(sh)
print('ok 新门接进第 8 步')
