import io

# 修上一条命令里被 bash 反引号吞掉的第 33 章那句话，并把第 24 章证据栏的混栏标记改准。
P = 'drafts/unit-33/draft.md'
t = io.open(P, encoding='utf-8').read()
old_start = '**5.6 GB 只是“本体感觉”这一路**'
i = t.index(old_start)
j = t.index('\n', i)
bad = t[i:j]
print('当前（可能被 shell 改坏）:', repr(bad[:170]))
good = ('**5.6 GB 只是“本体感觉”这一路**（这里按 500 Hz 记账是本书假设 [未]：'
        '官方只把 500 Hz 坐实在 `rt/lowcmd` 上，`rt/lowstate` 的确切频率没有取到）。')
t = t[:i] + good + t[j:]
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('改回:', repr(good[:60]), '反引号数', good.count('`'))

P = 'drafts/unit-24/draft.md'
t = io.open(P, encoding='utf-8').read()
old = 'Mid-360S 的 “Built-in IMU Model: ICM40609”、扭矩常数 0.63895 N·m/A [查]'
if t.count(old) != 1:
    print('u24 锚点没找到，人工看：', t.count(old))
else:
    new = ('Mid-360S 的 `Built-in IMU Model: ICM40609`、扭矩常数 0.63895 N·m/A '
           '[查]（这一行是混栏：GO-M8010-6 的 −5~40 ℃ 与 Dex3-1 的 −20~60 ℃ 是宇树器件页 [厂]，'
           'Mid-360S 那两项来自别家官方页，按图例只能记 [查]）')
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    print('ok u24 混栏标记已写清')
