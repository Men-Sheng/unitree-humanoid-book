import io
import re

B = 'drafts/unit-37/draft.md'
t = io.open(B, encoding='utf-8').read()

# 1) 跨减速比折惯量：把输出端等效惯量除以电机端转子惯量，凭空多乘了 i²
old = '3.27 ÷ (0.489 × 10⁻⁴) ≈ 6.7 万倍'
if t.count(old) == 1:
    t = t.replace(old, '3.27 ÷ (4.89×10⁻⁵ × 22.5² = 0.0248) ≈ 132 倍')
    print('ok u37 惯量折算已改到同一侧（132 倍）')
else:
    print('!! u37 惯量锚点 count=', t.count(old), '→ 打印该行备用')
    for i, l in enumerate(t.split('\n')):
        if '6.7 万倍' in l or '3.27 ÷' in l:
            print(i + 1, l[:170])

# 2) 小结里残留的旧倍数
old2 = '这两个数之间差 20 到 60 倍'
if t.count(old2) == 1:
    t = t.replace(old2, '这两个数之间差 19 到 69 倍')
    print('ok u37 小结倍数与正文一致')
else:
    print('· u37 小结倍数 count=', t.count(old2))

io.open(B, 'w', encoding='utf-8', newline='\n').write(t)

for f in ['drafts/unit-37/draft.md', 'drafts/unit-38/draft.md', 'drafts/unit-39/draft.md', 'drafts/unit-40/draft.md']:
    s = io.open(f, encoding='utf-8').read()
    for m in re.finditer(r'[^\n]*(6\.7 万|66,900|66900|3\.27 ÷)[^\n]*', s):
        print(f.split('unit-')[1][:2], '|', m.group(0)[:150])

print('--- rebuild_all.sh 里 src-docx 相关行 ---')
sh = io.open('tools/rebuild_all.sh', encoding='utf-8').read().split('\n')
for i, l in enumerate(sh):
    if 'src-docx' in l:
        print(i + 1, '|', l[:150])
