import io

NL = chr(10)
Q = chr(34)
OPEN = u'“'
CLOSE = u'”'
P = 'tools/fix_quotes.py'
t = io.open(P, encoding='utf-8').read()

# ---- ① 修那条自欺的形状不变量：右边是 old.replace('"','"')，空操作 ----
bad = '            assert new.replace("\\u201c", \'"\').replace("\\u201d", \'"\') == old.replace(\'"\', \'"\'), f'
assert t.count(bad) == 1, ('① 锚点', t.count(bad))
good = ('            assert new.replace("\\u201c", \'"\' + \'").replace("\\u201d", \'"\' + \'") == '
        'old.replace("\\u201c", \'"\' + \'").replace("\\u201d", \'"\' + \'"\'), f')
# 直接按字符拼一条干净行（每个字符字面量都要在自己的引号里）：
SQ = chr(39)
a1 = SQ + OPEN + SQ          # '“'
a2 = SQ + CLOSE + SQ         # '”'
q2 = SQ + Q + SQ             # '"'
good = ('            assert new.replace(' + a1 + ', ' + q2 + ').replace(' + a2 + ', ' + q2 + ') == '
        'old.replace(' + a1 + ', ' + q2 + ').replace(' + a2 + ', ' + q2 + '), f')
t = t.replace(bad, good)
print('① 改后：', good.strip())

# ---- ② 加"跨段未闭合"检查（不检单行，避免把换行散文判成错） ----
helper = '''

def cross_paragraph(root=ROOT):
    """弯引号必须**在同一个段落组里成对**。跨段闭合意味着：某个引号开了没在本段关，
    是归一化按顺序赋号时配错对的唯一硬症状。
    不检"单行配平"——散文折行与表格行本来就跨行成对（第 27、28 章那 4 处就是），
    按行检会天天假报警。围栏与行内代码跳过。"""
    bad = []
    for f in sorted(glob.glob(os.path.join(root, "drafts", "*", "draft.md"))):
        s = io.open(f, encoding="utf-8").read()
        ls = s.split(chr(10))
        fence = fence_mask(ls)
        for g in paragraph_groups(ls, fence):
            depth = 0
            for i in g:
                if fence[i]:
                    continue
                sp = protected(ls[i])
                for j, ch in enumerate(ls[i]):
                    if in_spans(j, sp):
                        continue
                    if ch == OPEN:
                        depth += 1
                    elif ch == CLOSE:
                        depth -= 1
                    if depth < 0:
                        break
                if depth < 0:
                    break
            if depth != 0:
                bad.append((os.path.basename(os.path.dirname(f)), g[0] + 1, depth,
                            ls[g[0]].strip()[:56]))
    return bad

'''
anchor = 'def apply_glob(pattern: str) -> int:'
assert t.count(anchor) == 1, ('② 锚点', t.count(anchor))
t = t.replace(anchor, helper.lstrip('\n') + NL + anchor)

# 把检查接进 --check
old_check = '''        print("引号体例：中文里残留 ASCII 直引号 %d 处；弯引号不配平的文件 %d 个" % (len(r), len(bal)))'''
assert t.count(old_check) == 1, ('② print 锚点', t.count(old_check))
new_check = '''        xp = cross_paragraph()
        print("引号体例：中文里残留 ASCII 直引号 %d 处；弯引号不配平的文件 %d 个；跨段未闭合 %d 处"
              % (len(r), len(bal), len(xp)))
        for u, ln, d, txt in xp[:6]:
            print("    跨段：", u, "行", ln, "净差", d, txt)'''
t = t.replace(old_check, new_check)
t = t.replace('        return 1 if (r or bal) else 0', '        return 1 if (r or bal or xp) else 0')

# 自检：正例（同段成对）与负例（跨段闭合）。插在 --check 分支之前，与它同级。
st_anchor = '    if "--check" in sys.argv:'
assert t.count(st_anchor) == 1, ('② 自检锚点', t.count(st_anchor))
t = t.replace(st_anchor, st_anchor + '''
    if "--test-cross-paragraph" in sys.argv:
        good_txt = '甲段\\u201c你好\\u201d收尾。\\n\\n乙段没有引号。\\n'
        bad_txt = '甲段\\u201c开了没关\\n\\n乙段\\u201d在别处关上。\\n'
        ok1 = _count_groups(good_txt) == 0
        ok2 = _count_groups(bad_txt) == 1
        print(('PASS ' if ok1 else 'FAIL ') + '同段成对不误报')
        print(('PASS ' if ok2 else 'FAIL ') + '跨段闭合被抓到')
        return 0 if (ok1 and ok2) else 1
''')
# 自检用的临时计数器：把 cross_paragraph 的循环套到一个字符串上
t = t.replace('def cross_paragraph(root=ROOT):', '''def _count_groups(text):
    ls = text.split(chr(10))
    fence = fence_mask(ls)
    n = 0
    for g in paragraph_groups(ls, fence):
        depth = 0
        for i in g:
            if fence[i]:
                continue
            sp = protected(ls[i])
            for j, ch in enumerate(ls[i]):
                if in_spans(j, sp):
                    continue
                if ch == OPEN:
                    depth += 1
                elif ch == CLOSE:
                    depth -= 1
        if depth != 0:
            n += 1
    return n


def cross_paragraph(root=ROOT):''')
io.open(P, 'w', encoding='utf-8', newline=NL).write(t)
print('② 已加 cross_paragraph 门 + 两条对照自检')
