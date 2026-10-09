import io
import re

# 附录 A 的六处口径缺口 + 第 11 章两处指针/口径 + 第 21、27 章两处引号误用（本轮判定）。
A = 'drafts/unit-41/draft.md'
t = io.open(A, encoding='utf-8').read()

# 1) A.7：「五级」其实是七个，[推] 从未登记
lines = t.split('\n')
for i, l in enumerate(lines):
    if '**五级来源标记**' in l:
        seg = l.split('；')
        out, added = [], False
        for s in seg:
            out.append(s)
            if not added and s.strip().startswith('[查]'):
                out.append('[推] 本书自己的推断，没有一手来源支撑（凡用它处都明写这是推断）')
                added = True
        lines[i] = '；'.join(out).replace('**五级来源标记**', '**七级来源标记**')
        print('A.7 已改；[推] 补入 =', added, '；该行现长', len(lines[i]))
        break
else:
    print('!! A.7 锚点没找到')
t = '\n'.join(lines)

# 2) A.1 符号表：τ 撞车、1/τ 的单位、λ/ρ 撞形——三行登记
anchor = '| τ_e, τ_m | 电、机械时间常数 | s | 09, 12 | τ_e = L/R；τ_m = J·R/k_t² |'
assert t.count(anchor) == 1, ('A.1 τ 锚点', t.count(anchor))
add = anchor + '''
| τ（**裸用，无下标**） | 倒立摆时间常数 √(l/g)；第 35 章一处指 RC 常数 | s | 00, 16, 17, 35, 40 | 本书的区分办法：带 e/m 下标＝电/机械常数；运控与平衡章节里裸 τ＝倒立摆时间常数；第 35 章那一处写作 τ = R·C 已就地标明 |
| 1/τ | 倒立摆的 e-folding 率（发散率），**不是角速度也不是频率** | **s⁻¹** | 00, 24 | G1 髋高 0.66 m ⇒ τ = 0.259 s ⇒ 1/τ = 3.85 s⁻¹ ≈ 0.61 Hz（折 Hz 要 ÷2π） |
| λ（导程角）、ρ（摩擦角） | 第 37 章丝杠自锁判据专用 | ° | 37 | 与磁链 λ_m 撞形：**这两个符号无下标且只在第 37 章的机械一节出现**；同节的 η_正 / η_反 是正/反行程效率，与热效率无关 |'''
t = t.replace(anchor, add)

# 3) A.6：脱字 + 「铜损 ≠ 总损耗」这一格
old = '三者层次不同：电机 ⊂ 关节  执行器系统'
if t.count(old) == 1:
    t = t.replace(old, '三者层次不同：电机 ⊂ 执行器 ⊂ 关节')
    print('A.6 脱字已修（电机 ⊂ 执行器 ⊂ 关节）')
else:
    print('!! A.6 脱字锚点 count=', t.count(old))
anchor2 = '| 确定性 | 稳定 | 确定性 = 时间有界；稳定 = 不发散 |'
assert t.count(anchor2) == 1, ('A.6 锚点', t.count(anchor2))
t = t.replace(anchor2, anchor2 + '\n| 损耗（总） | 铜损 | **总损耗 = 铜损 + 铁损 + 驱动板（导通与开关） + 减速器摩擦**；第 36 章那颗膝的 55 W 是总损耗，第 13 章的 36 W 才是铜损，两者差约 1.5 倍 |')

io.open(A, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 附录 A 四处登记完成')

# 4) 第 11 章：指针指错 + 反电势口径与本书声明的幅值不变约定冲突
P = 'drafts/unit-11/draft.md'
t = io.open(P, encoding='utf-8').read()
old = 'E = (2/3) · k_t · ω = p · λ_m · ω　（幅值不变约定，见 A.4）'
assert t.count(old) == 1, ('u11 锚点1', t.count(old))
t = t.replace(old, 'E = (2/3) · k_t · ω = p · λ_m · ω　（幅值不变约定，见 A.1 的 k_e 行）')
old = '2. **最高转速时母线电压多少？** → 做一次 √3·k_t·ω 检查，看那个转速是否可达（第 08 章）。'
assert t.count(old) == 1, ('u11 锚点2', t.count(old))
t = t.replace(old, '2. **最高转速时母线电压多少？** → 按本书声明的幅值不变约定做一次反电势检查：相电动势幅值 = k_t·ω（A.1 的 k_e 行），**再换算成手册常写的线电压有效值才是可比的**（√3 出现在这一步，不是那一步）。用哪个口径要在纸上写出来——两个口径混用会把这项检查放松 2.6 倍（第 08 章）。')
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 第 11 章两处口径已对齐')

# 5) 第 21 章：代码标识符被当引文；第 27 章：嵌套引号只剩一层
P = 'drafts/unit-21/draft.md'
t = io.open(P, encoding='utf-8').read()
old = '那一行 **“import sapien.physx as physx”**'
assert t.count(old) == 1, ('u21 锚点', t.count(old))
t = t.replace(old, '那一行 **`import sapien.physx as physx`**')
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 第 21 章标识符改为行内代码')

P = 'drafts/unit-27/draft.md'
t = io.open(P, encoding='utf-8').read()
old = "'on the fly'"
n = t.count(old)
t = t.replace(old, '‘on the fly’')
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok 第 27 章内层引号升为 ‘ ’（改 %d 处）' % n)
