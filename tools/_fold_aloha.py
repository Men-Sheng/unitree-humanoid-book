import io

NL = chr(10)
R = 'research/other-vendor-firsthand.md'

io.open(R, 'a', encoding='utf-8', newline=NL).write(NL.join([
    '| ALOHA 每任务演示条数 | 第 29 章"单任务约 50 条演示 [查]" | `With 50 demonstrations for each task,` | https://arxiv.org/abs/2401.02117（Mobile ALOHA） | 2026-10-09 | **一手证实**（同篇另有 `increase success rates by up to 90%`，本书没用到就没写进正文） |',
    '| GraspVLA 的定位 | 第 30、44 章把它当"单卡可训的 VLA 范本" | 一手只读到标题 `GraspVLA: a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data`；**参数量、去噪步数、延迟、演示条数在 abs 页全部 absent** | https://arxiv.org/abs/2505.03233 | 2026-10-09 | **部分一手**（标题级）⇒ 正文涉及它的具体规格若无其它来源，一律记 [推] |',
    '',
    '## 尚未逐字回读的 [查]（`tools/check_vendor_ledger.py` 每轮重算，清单在 `verification/vendor-ledger-latest.txt`）',
    '',
    '第七轮独立审稿指出：第 29–34 章有约 20 处标了 [查]，但本台账里没有对应的逐字行。',
    '本轮已补的是 ALOHA 与 GraspVLA 两条；**仍欠逐字原文的**（付印前要么补抓、要么降 [推]）：',
    '',
    '- Gemini Robotics 的"拉袋 44% / 拉链 40%"与 Figure Helix 2.5 的"30 户家庭零样本 56%"（第 29、38 章）',
    '- GO-2 / ACoT-VLA 的规格（第 30 章）',
    '- GR00T 的 `Cosmos-Reason2-2B`、`flow-matching DiT，16 层`、相对末端位姿、ONNX/TensorRT 导出（第 30 章：本台账只确认 3 B 主干 / horizon 40 / 132 维 / 16 GB+）',
    '- SynGrasp 与 GEN-0 的 >270,000 小时（第 33 章）',
    '- 智元数据工厂"95%+ 合格率"（第 33 章：AgiBot 论文里**没有**产出率与合格率，见上文负面行）',
    '- "用比特而非原子做评估"这句话的出处、Tesla FSD 与 Optimus 共用神经仿真器的原话（第 34 章）',
    '',
    '**这些不是"已经查清"，是"已登记未查清"。** 门把它们列成软清单，就是为了不让人把它们当成已通过。',
    '',
]))
print('ok 台账补 2 行一手 + 一份未回读清单')

# 第 29 章那句 ALOHA：把一手原话补进去
p = 'drafts/unit-29/draft.md'
t = io.open(p, encoding='utf-8').read()
old = 'ALOHA 那类主从臂方案的公开口径是**单任务约 50 条演示** [查]'
assert t.count(old) == 1, t.count(old)
new = ('ALOHA 那类主从臂方案的公开口径是**单任务约 50 条演示**——一手原话 `With 50 demonstrations for each task,`'
       '（Mobile ALOHA，arXiv 2401.02117）[查]')
io.open(p, 'w', encoding='utf-8', newline=NL).write(t.replace(old, new))
print('ok 第 29 章 ALOHA 那句补上一手原话')

# 第 34 章的"比特而非原子"这类无台账引用：先在正文里就地降级，避免替别人签字
p = 'drafts/unit-34/draft.md'
t = io.open(p, encoding='utf-8').read()
for old, new in [
    ('用比特而非原子做评估 [查]', '用比特而非原子做评估 [推]（这句出自作者蓝图附件的转述，本书未读到原话）'),
]:
    if t.count(old) == 1:
        t = t.replace(old, new)
        print('ok 第 34 章：无台账的一句降 [推]')
io.open(p, 'w', encoding='utf-8', newline=NL).write(t)
