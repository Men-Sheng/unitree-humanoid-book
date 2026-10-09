import io

P = 'tools/fix_quotes.py'
t = io.open(P, encoding='utf-8').read()

# 撤掉我上一步插错位置的自检块（它挂到了 --selftest 的分支体里，还引用了不存在的函数）
bad_start = '    if "--test-fence-cjk" in sys.argv:'
bad_end = "        return 0 if (ok1 and ok2) else 1\n"
i = t.find(bad_start)
j = t.find(bad_end, i)
assert i > 0 and j > i, (i, j)
t = t[:i] + t[j + len(bad_end):]
print('ok 撤掉插错位置的自检块')

# 也撤掉那条自欺的不变量（右边 replace 是空操作）
bad_assert = '            assert new.replace("\\u201c", \'"\' + \') == old.replace(\', \\\'"\\", \'"\' + \')  + \'"\' + \'), f\n'
t2 = t.replace(
    '            assert new.replace("\\u201c", \'"\').replace("\\u201d", \'"\') == old.replace(\'"\', \'"\', ) , f\n', '')
# 直接按行处理更稳
lines = t.split('\n')
out = []
for l in lines:
    if l.strip().startswith('assert new.replace("') and '== old.replace(' in l:
        out.append('            assert new.count("\\u201c") == new.count("\\u201d"), f')
        out.append('            assert old.count(\'"\') - new.count(\'"\') == n, (f, old.count(\'"\'), new.count(\'"\'), n)')
        continue
    out.append(l)
t = '\n'.join(out)
print('ok 不变量改成可执行的三条（配平 + 只减少了 n 个 ASCII 引号）')

# 把 --test-fence-cjk 放回 main 顶层（与 --fences-cjk-apply 同级），并去掉不存在的函数引用
anchor = 'def main() -> int:\n'
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + '''    if "--test-fence-cjk" in sys.argv:
        bad = ('```' + 'text\\n他说"目标角度是多少"，之后不再发\\n官方写 "it is always 125 microseconds"\\n```' + '\\n')
        new, n = fences_cjk_apply(bad)
        ok1 = n == 2 and '\\u201c目标角度是多少\\u201d' in new
        ok2 = '"it is always 125 microseconds"' in new          # 纯 ASCII 原话不许动
        ok3 = fence_cjk_residue_here = (new.count('\\u201c') == new.count('\\u201d'))
        print(('PASS ' if ok1 else 'FAIL ') + '围栏内含中文的 ASCII 对换成弯引号')
        print(('PASS ' if ok2 else 'FAIL ') + '围栏内纯 ASCII 官方原话不误伤')
        print(('PASS ' if ok3 else 'FAIL ') + '替换后弯引号左右配平')
        return 0 if (ok1 and ok2 and ok3) else 1
''')
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 自检移到 main 顶层')
