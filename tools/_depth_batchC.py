import io

NL = chr(10)


def insert_after(u, prefix, block):
    p = 'drafts/unit-%s/draft.md' % u
    lines = io.open(p, encoding='utf-8').read().split(NL)
    idx = [k for k, l in enumerate(lines) if l.startswith(prefix)] or \
          [k for k, l in enumerate(lines) if prefix in l]
    if len(idx) != 1:
        print('!! u%s 锚点 %d：%s' % (u, len(idx), prefix[:26]))
        return
    lines[idx[0] + 1:idx[0] + 1] = ['', block.rstrip()]
    io.open(p, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
    print('ok u%s 第 %d 行后插入' % (u, idx[0] + 1))


def replace(u, old, new):
    p = 'drafts/unit-%s/draft.md' % u
    t = io.open(p, encoding='utf-8').read()
    if t.count(old) != 1:
        print('!! u%s count=%d：%s' % (u, t.count(old), old[:36]))
        return
    io.open(p, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new))
    print('ok u%s 替换：%s' % (u, old[:30]))


C40a = '''**这三项都要换算到牛米，才谈得上“可比大小”。** 以死区偷电压那一项为例（第 13 章：100 ns ÷ 50 µs × 24 V = 48 mV [算]），一路上推到关节：

```text
Δi = 48 mV ÷ 0.040 Ω = 1.2 A          （相电阻取第 08 章那条，本书假设 [未]）
k_t(关节侧) = 23.7 N·m ÷ 40 A = 0.5925 N·m/A    （M8010 那两个官方数 [厂]）
Δτ = 1.2 A × 0.5925 = 0.71 N·m        ⇒ 是你要验的 250 mN·m 的 2.8 倍
```

[算]。**但它真正的杀伤力不在大小，在它是加性的而不是乘性的**：命令 23.7 N·m 时这个固定偏差只占 3.0%，命令 1 N·m 时占 71%，命令 0.25 N·m（正是本里程碑要验的那一档）时它是 **285%**——一个 0.71 N·m 的恒定偏差在近零处把指令整个吞掉。**这就是第 13 章那句“过零附近最疼”的确切算术，也是为什么做力控的关节要么上死区补偿、要么把可命令的最小扭矩抬高到一个比它大的地板。** 顺带一条同款换算，**两边都折到关节侧再比**：IM6014 那 0.39 mN·m 是**转子侧**的协议刻度 [厂]，乘上它 12.667 的速比才是关节侧的 4.9 mN·m；0.71 N·m ÷ 0.0049 N·m ≈ **144 倍** [算]，所以“瓶颈在数字之外”这句不是修辞。**但比之前先把两侧对齐**：拿关节侧的偏差去比转子侧的刻度，就又是本章前面那种跨减速比少乘一个 i² 的错。'''

insert_after('40', '还有一个更硬的理由要求你自建电流环', C40a)

replace('40', '一次力矩阶跃响应十几毫秒就有结论',
        '一次力矩阶跃响应要多久才有结论，第 09 章那个 τ_m = J·R ÷ k_t² ≈ 4.9 ms 给了答案：一阶系统到 95% 要 3τ_m = 14.7 ms、到 98% 要 4τ_m = 19.6 ms [算]——**“十几毫秒”是 95% 档，若你的判据是 ±2% 稳态误差，预算就得写 20 ms**，正好占一步支撑相的 10%')

replace('40', '（[算]：4,000 ÷ 100 与 8,000 ÷ 100）', '（[算]：4,000 ÷ 100 与 8,000 ÷ 100）', must=False) if False else None
