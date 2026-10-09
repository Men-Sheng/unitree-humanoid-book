import glob
import io
import os
import re
import sys

sys.path.insert(0, 'tools')
import fix_quotes as fq  # noqa: E402  用它的 CJK_PAIR 与 fence_cjk_residue

NL = chr(10)
QUO = chr(34)   # ASCII 直引号
OPEN = u'“'
CLOSE = u'”'


def convert_file(path):
    ls = io.open(path, encoding='utf-8').read().split(NL)
    out, fence, blocks, n = [], False, [], 0
    for l in ls:
        if l.startswith('```'):
            if fence:
                blk = NL.join(blocks)
                new_blk, cnt = CJK_PAIR_ALL(blk)
                n += cnt
                out.append(new_blk)
                blocks = []
            fence = not fence
            out.append(l)
            continue
        (blocks if fence else out).append(l)
    if blocks:
        blk = NL.join(blocks)
        new_blk, cnt = CJK_PAIR_ALL(blk)
        n += cnt
        out.append(new_blk)
    return NL.join(out), n


CJK_PAIR_ALL = None


def _init():
    global CJK_PAIR_ALL
    pat = fq.CJK_PAIR

    def run(blk):
        cnt = [0]

        def sub(m):
            cnt[0] += 1
            return OPEN + m.group(1) + CLOSE
        return pat.sub(sub, blk), cnt[0]
    CJK_PAIR_ALL = run


_init()

total = 0
touched = []
for path in sorted(glob.glob('drafts/unit-*/draft.md')):
    old = io.open(path, encoding='utf-8').read()
    new, n = convert_file(path)
    if not n:
        continue
    # 三条后置条件：弯引号成对增加、ASCII 引号恰好少 2n、去掉弯引号后正文逐字不变
    ok_open = new.count(OPEN) - old.count(OPEN) == n
    ok_close = new.count(CLOSE) - old.count(CLOSE) == n
    ok_ascii = old.count(QUO) - new.count(QUO) == 2 * n
    flat_old = old.replace(OPEN, QUO).replace(CLOSE, QUO)
    flat_new = new.replace(OPEN, QUO).replace(CLOSE, QUO)
    ok_shape = flat_old == flat_new
    if not (ok_open and ok_close and ok_ascii and ok_shape):
        print('SKIP %s n=%d open=%s close=%s ascii=%s shape=%s'
              % (path, n, ok_open, ok_close, ok_ascii, ok_shape))
        continue
    io.open(path, 'w', encoding='utf-8', newline=NL).write(new)
    total += n
    touched.append(os.path.basename(os.path.dirname(path)))

print('转换完成：%d 对，涉及 %d 章' % (total, len(touched)))
print('fence_cjk_residue 现在 =', fq.fence_cjk_residue())

S = 'tools/rebuild_all.sh'
t = io.open(S, encoding='utf-8').read()
lines = t.split(NL)
idx = [i for i, l in enumerate(lines) if '--fences-check' in l and 'fix_quotes' in l]
if len(idx) != 1:
    print('!! 门锚点没定位到（%s），门不接，只交正文' % idx)
else:
    i = idx[0]
    pad = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
    gate = [
        pad + '$PY - <<\'PYFENCE\'',
        pad + 'import sys',
        pad + 'sys.path.insert(0, "tools")',
        pad + 'import fix_quotes as fq',
        pad + 'n = fq.fence_cjk_residue()',
        pad + 'print("围栏内含中文的 ASCII 引号对：%d 处" % n)',
        pad + 'if n:',
        pad + '    raise SystemExit("围栏里的中文说明还在用直引号（门以前跳过围栏，现在不跳）")',
        pad + 'PYFENCE || fail "围栏内引号体例"',
    ]
    lines[i + 1:i + 1] = gate
    io.open(S, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
    print('ok 门已接进第 7 步（在第 %d 行之后）' % (i + 1))
