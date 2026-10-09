import io

S = 'tools/rebuild_all.sh'
t = io.open(S, encoding='utf-8').read()
old = """if nb and now < nb - 1:
    raise SystemExit('清空后生成器少写了 %d 个文件（清空前 %d，现在 %d），交稿包会缺章' % (nb - now, nb, now))
if len(c) < 46:
    raise SystemExit('交稿包只有 %d 个一级标题（应 ≥46 章），不敢拿去打包' % len(c))"""
new = """if nb and now < nb - 1:
    raise SystemExit('清空后生成器少写了 %d 个文件（清空前 %d，现在 %d），交稿包会缺章' % (nb - now, nb, now))
# 缺章由上面这条兜（少 1 个＝正是被清掉的重复副本，少 2 个以上就是真缺）；
# 标题解析只用于查重复，不按它卡总数——有些产物文件（封面、CIP 说明）本来就没有 `# ` 行。
if now < 45:
    raise SystemExit('交稿包只剩 %d 个 md（应 ≥45），不敢拿去打包' % now)"""
if t.count(old) == 1:
    io.open(S, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    print('ok 守卫：缺章交给文件数比对，标题只用于查重')
else:
    print('!! 锚点 count=', t.count(old))
