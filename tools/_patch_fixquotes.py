import io
import re

P = 'tools/fix_quotes.py'
t = io.open(P, encoding='utf-8').read()

# 1) 补上"围栏内含中文的 ASCII 引号对 → 弯引号"这一半（原来只有反向退回 ASCII 的那半）
anchor = 'def fences_to_ascii(txt: str)'
assert t.count(anchor) == 1
helper = '''CJK_PAIR = re.compile(r'"([^"\\n]*[\\u4e00-\\u9fff][^"\\n]*)"')


def fence_cjk_pairs(block: str, state: list) -> str:
    """围栏内那半边的漏网规则：`_fix_fence_block` 说"围栏里夹的中文说明保持弯引号"，
    可 `convert()` 整段跳过围栏，于是**中文说明在围栏里从来没被换过**。2026-10-09 实测 34 行。
    只动内侧含中文的一对；内侧是纯 ASCII 的（官方原话、命令行、字段名）继续留直引号，
    因为那是要复制去跑的。"""
    def sub(m):
        state[0] += 1
        return '\\u201c' + m.group(1) + '\\u201d'
    return CJK_PAIR.sub(sub, block)


def fences_cjk_apply(txt: str) -> tuple:
    ls = txt.split(chr(10))
    out, fence, blocks, cnt = [], False, [], [0]
    for l in ls:
        if l.startswith("```"):
            if fence:
                out.append(fence_cjk_pairs(chr(10).join(blocks), cnt))
                blocks = []
            fence = not fence
            out.append(l)
            continue
        (blocks if fence else out).append(l)
    if blocks:
        out.append(fence_cjk_pairs(chr(10).join(blocks), cnt))
    return chr(10).join(out), cnt[0]


def fence_cjk_residue(root=ROOT) -> int:
    n = 0
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        n += len(CJK_PAIR.findall(fence_block_text(f)))
    return n


def fence_block_text(path: str) -> str:
    ls = io.open(path, encoding="utf-8").read().split(chr(10))
    fence, keep = False, []
    for l in ls:
        if l.startswith("```"):
            fence = not fence
            continue
        if fence:
            keep.append(l)
    return chr(10).join(keep)


'''
t = t.replace(anchor, helper + anchor)

# 2) 让 --check 也看见围栏里的这一类（关掉"门跳过围栏"那条盲区）
old_check = 'def main() -> int:\n    argv = sys.argv'
assert t.count(old_check) == 1
t = t.replace(old_check, '''def main() -> int:
    if "--fences-cjk-apply" in sys.argv:
        tot = 0
        for f in sorted(glob.glob(os.path.join(ROOT, "drafts", "*", "draft.md"))):
            old = io.open(f, encoding="utf-8").read()
            new, n = fences_cjk_apply(old)
            if not n:
                continue
            assert new.replace("\\u201c", '"').replace("\\u201d", '"') == old.replace('"', '"'), f
            assert new.count("\\u201c") == new.count("\\u201d"), f
            io.open(f, "w", encoding="utf-8", newline="\\n").write(new)
            tot += n
            print("  围栏内中文引号归一 %d 个：%s" % (n, f.split(os.sep)[-2]))
        print("围栏内含中文的 ASCII 引号：共替换 %d 个字符" % tot)
        return 0
    argv = sys.argv''')
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok fix_quotes 加了 --fences-cjk-apply 与 fence_cjk_residue')

# 3) 自检：正例（中文说明在围栏里）与反例（纯 ASCII 原话不许动）
st = io.open(P, encoding='utf-8').read()
old = '    if "--selftest" in sys.argv:'
assert st.count(old) == 1
st = st.replace(old, old + '''
    if "--test-fence-cjk" in sys.argv:
        bad = '```text\\n他说"目标角度是多少"，之后不再发\\n官方写 "it is always 125 microseconds"\\n```\\n'
        new, n = fences_cjk_apply(bad)
        ok1 = n == 2 and '\\u201c目标角度是多少\\u201d' in new
        ok2 = '"it is always 125 microseconds"' in new      # 纯 ASCII 原话必须还是直引号
        ok3 = fence_block_text_from(new).count('"') == 2
        print(('PASS ' if ok1 else 'FAIL ') + '围栏内中文对换成弯引号')
        print(('PASS ' if ok2 else 'FAIL ') + '围栏内纯 ASCII 原话不误伤')
        return 0 if (ok1 and ok2) else 1
''')
io.open(P, 'w', encoding='utf-8', newline='\n').write(st)
print('ok 加了 --test-fence-cjk（负对照 + 正对照）')
