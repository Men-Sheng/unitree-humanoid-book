import io

P = 'tools/blueprint_coverage.py'
t = io.open(P, encoding='utf-8').read()

old = '''def rows(md: str):
    for line in md.split("\\n"):
        if not line.startswith("| ") or line.startswith("|---") or "蓝图条目" in line:
            continue'''
new = '''def rows(md: str):
    """只读**归属表**（章号那一列是 `26, 39, 43` 这种清单）。

    文档里还有别的表，最典型的是 2026-10-09 追加的「逐格人工判定」一节：它的第一列也是条目名，
    第二列却写成 `00:双目@34 / 03:深度相机@128` 这种"章:词@行号"。上一版把它当归属表读，
    于是"视觉与深度"这种**没有括号的简称**被当判别词去全书搜——搜不到，判成虚标格子。
    门自己造了一条假指控。现在两道保险：带 `@` 的行跳过；条目名不在正文里的简称行也跳过
    （真表的条目名一律带括号里的判别词）。"""
    skip_section = False
    for line in md.split("\\n"):
        if line.startswith('#'):
            skip_section = ('人工判定' in line) or ('判别词' in line)
            continue
        if skip_section:
            continue
        if not line.startswith("| ") or line.startswith("|---") or "蓝图条目" in line:
            continue
        if '@' in line:
            continue'''
assert t.count(old) == 1, t.count(old)
io.open(P, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
print('ok blueprint_coverage 只读归属表，"人工判定"那一节不再被当章号清单')
