import io
import subprocess
import sys

# 1) 第 37 章：把"跨减速比除惯量"的旧检查项也改掉，并扫残留
B = 'drafts/unit-37/draft.md'
t = io.open(B, encoding='utf-8').read()
old = '- [ ] 用 J = 2 × 343 ÷ 14.5² 复算 3.27 kg·m²，再除 4.89 × 10⁻⁵，看 6.7 万倍这个量级（3.27 ÷ 4.89e-5 = 66,900）'
if t.count(old) == 1:
    new = ('- [ ] 用 J = 2 × 343 ÷ 14.5² 复算 3.27 kg·m²，**再把它和转子惯量折算到同一侧**：'
           '4.89 × 10⁻⁵ × 22.5² = 0.0248 ⇒ 3.27 ÷ 0.0248 = 132 倍。'
           '直接除 4.89 × 10⁻⁵ 得 66,900 是错的——那跨了 22.5:1 的减速比，凭空多乘 i² = 506 倍（附录 A 的 J 行就为这一格写的）')
    t = t.replace(old, new)
    print('ok 第 37 章检查项已改成同侧折算')
else:
    print('!! 检查项锚点 count=', t.count(old))
for pat in ['6.7 万倍', '66,900', '20 到 60 倍', '20–60 倍']:
    hits = [i + 1 for i, l in enumerate(t.split('\n')) if pat in l]
    print('残留 %-10s %s' % (pat, hits))
io.open(B, 'w', encoding='utf-8', newline='\n').write(t)

# 2) 交稿包目录必须先清空；HTML 属性引号要还原；章名不许重复
S = 'tools/rebuild_all.sh'
sh = io.open(S, encoding='utf-8').read()
echo4 = '  echo "── 4/9 交稿包（src-docx + 授权清单 + CIP 说明）"'
assert sh.count(echo4) == 1, ('step4 echo 锚点', sh.count(echo4))
guard = echo4 + '''
  # 2026-10-09 实测事故：src-docx 从不清空，旧文件名的同一章留了一整份，
  # pandoc 拿 *.md 打包 ⇒ 交稿 docx 里第 24 章出现两遍。构建产物目录一律先清再生成。
  n_before=$(ls submission/src-docx/*.md 2>/dev/null | wc -l)
  find submission/src-docx -maxdepth 1 -name '*.md' -delete 2>/dev/null || true'''
sh = sh.replace(echo4, guard)

apply_line = '  $PY tools/fix_quotes.py --apply "submission/src-docx/*.md" || fail "交稿包引号归一"'
assert sh.count(apply_line) == 1, ('fix_quotes --apply 锚点', sh.count(apply_line))
sh = sh.replace(apply_line, apply_line + '''
  $PY tools/protect_html_attrs.py "submission/src-docx/*.md" || fail "HTML 属性引号还原"
  NB=$n_before $PY - <<'PYDOCX'
import collections
import glob
import io
import os
c = collections.Counter()
for p in sorted(glob.glob('submission/src-docx/*.md')):
    for line in io.open(p, encoding='utf-8').read().split('\\n'):
        if line.startswith('# '):
            c[line.strip()] += 1
            break
dup = [k for k, n in c.items() if n > 1]
if dup:
    raise SystemExit('交稿包里有重名章（多半是旧文件没清掉）：%s' % dup[:3])
now = len(glob.glob('submission/src-docx/*.md'))
nb = int(os.environ.get('NB', '0'))
if nb and now < nb:
    raise SystemExit('清空后生成器少写了文件：%d < %d，交稿包会缺章' % (now, nb))
if now < 45:
    raise SystemExit('交稿包只剩 %d 个 md（应 ≥45：46 章 + 封面等），不敢拿去打包' % now)
bad = [p for p in glob.glob('submission/src-docx/*.md')
       if any('=' + chr(8220) in l for l in io.open(p, encoding='utf-8'))]
if bad:
    raise SystemExit('HTML 属性引号仍是弯引号，pandoc 会吞掉 class：%s' % bad[:3])
print('交稿包 %d 个 md、章名唯一（%d 个一级标题）；HTML 属性引号 ASCII ✓' % (now, sum(c.values())))
PYDOCX''')
io.open(S, 'w', encoding='utf-8', newline='\n').write(sh)
print('ok rebuild_all.sh：清空 src-docx + 还原属性引号 + 章名唯一/属性引号两道新检')

# 3) do-not-touch 追加两条（构建产物目录、属性引号），沿用它的编号列表格式
D = 'bible/do-not-touch.md'
d = io.open(D, encoding='utf-8').read()
assert '107. ' not in d
add = '''
## 第六轮独立审稿（2026-10-09，107–109）

107. **构建产物目录必须先清空再生成。** `submission/src-docx/` 从不清空，改名后的旧章文件留了一份，而 pandoc 按 `*.md` 打包 ⇒ **交稿 docx 里第 24 章出现两遍**（document.xml 同时有「前庭：IMU」与「前庭与状态估计」），门当时仍是绿的。产物目录里的残留文件不是"无害的旧副本"，它是会被打包出去的。
108. **`fix_quotes --apply` 只保护 Markdown 链接目标，不保护 HTML 属性引号**（那套保护写在 build.mjs 渲染层）。结果 `000-cover.md` 的 `<div class="cover-kicker">` 变成弯引号，pandoc 吞掉 class，封面排版无声丢失。现在链条里有 `tools/protect_html_attrs.py` + 一道"属性引号必须还是 ASCII"的检。**中文句子里包英文原话的弯引号是允许的**（GB/T 15834 与第 00 章图例都这样定），别照"审阅说 58 处违例"去 blanket 回退。
109. **转动惯量必须标明折算到哪一侧。** 第 37 章曾用输出端等效惯量 3.27 kg·m² 直接除电机轴转子惯量 4.89×10⁻⁵，得"6.7 万倍"——跨了 22.5:1 的减速比，凭空多乘 i² = 506；同侧折算后是 132 倍，且与本章自己的能量比 343 J ÷ 2.6 J = 132 独立对上。附录 A.1 已加 J 的折算行。
'''
io.open(D, 'a', encoding='utf-8', newline='\n').write(add)
print('ok do-not-touch 追加 107–109')

# 4) 新工具的自检
r = subprocess.run([sys.executable, '-X', 'utf8', 'tools/protect_html_attrs.py', '--selftest'],
                   capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip() or r.stderr.strip())
sys.exit(r.returncode)
