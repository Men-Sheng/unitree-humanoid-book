# CIP 与交稿说明

## 一、CIP 数据块（请出版社按本社模板核对后填写）

```
人形机器人：从一颗关节往下挖 ／ 〔作者〕著．— 〔城市〕：〔出版社〕，〔2026. 　〕
　　〔页〕　；　21 cm × 15 cm（大 32 开）
　ISBN 〔　　　　　　　　　〕
　Ⅰ．人…　Ⅱ．①〔作者〕　Ⅲ．①人形机器人—普及读物
　Ⅳ．①TP242.6
　中国版本图书馆 CIP 数据核字（〔2026〕）第〔　　　　〕号
```

**需要出版社填的空**：作者名、出版地与社名、出版年月、总页码、ISBN、CIP 核字号。
**需要作者定的事**：书名是否沿用、分类是否按"普及读物"还是"工程技术"（本书按 v3 定位
更接近"工程技术—机器人"而非"普及读物"，建议改第三级为 ①人形机器人—机器人结构 ②控制技术）。

## 二、字数与结构（由脚本统计，非自报）

```
章数：46（第 0–5 部 40 章 + 尾声 1 章 + 附录 A–E 5 章）
中文字符：205,999 个（脚本统计排版源 print/src 里的全部汉字，**含表格与图注**；
　　　　　不含表格与代码块的正文净字数由 `tools/depth_audit.py` 另行统计并随稿提供）
图：38 幅登记在册，其中 36 幅已落地（全部自绘矢量），2 幅待作者实拍
表：全书约 90 张对照表与参数表
可复算数：16 条推算链 + 10 条自检用例，脚本随稿提供
```

## 三、开本与版式（已按印厂常规参数设定，可直接改）

```
成品尺寸：145 mm × 210 mm（大 32 开）
版心：宽 110 mm（左右边距 20 / 15 mm，含订口），高约 176 mm
正文：Noto Serif SC 9.6 pt，行距 1.72
标题与图注：Noto Sans SC
页码：书口侧居中；章首页无页眉
图片：300 dpi，TIF 无压缩 RGB；矢量源文件另附（SVG）
```

## 四、已知排版限制（必须让编辑知道，不要当成作者疏忽）

1. **正文目前左对齐，不是两端对齐。** 本排版管线（Chrome + Paged.js）无法对中日韩文本
   做 justify——已穷举 `line-break` × `word-break` 组合验证，中文会在行尾留下大空档。
   若出版社要求两端对齐，需在 InDesign 或 LaTeX 里重排；本书稿的文字、结构、图与表可直接搬。
2. **PDF 文本层的 ToUnicode 有缺陷。** 子集化后的 Noto Serif SC 使"人"被抽取为 U+2F00，
   用 pypdf 检索"人形机器人"会假报缺失。**版面本身是正确的**（已逐页目视核对）。
   付印前请过一遍 PDF-X preflight；若编辑需要复制文字，请以 docx 为准。
3. **长字体名称导致 PDF 警告** `name token is longer than specification`。
   这是嵌入字体的命名问题，多数印厂可处理，但 PDF/X-1a 预检可能报错，需转档。
4. **书里没有一张真机照片。** 这是政策决定（官方素材 0 张，未取得授权），不是遗漏。
   三幅待补的实拍位已在 `图片授权清单.md` 中逐条列出规格。

## 五、随稿脚本与自检门（编辑与印厂不需要，但审稿人可能想验）

本书的验收纪律是"可以不讲，但不能讲错"。为此每一处标注为 [算] 的数都由脚本产出，
且脚本自带**已知答案自检**（度量本身要先证明自己能用）。一条命令跑完全部重建与全部门：

```
bash tools/rebuild_all.sh            # 草稿 → 排版源 → 图片 → PDF → 交稿包 → docx → 六道门
bash tools/rebuild_all.sh --gates    # 只跑门
```

逐条：

```
python code/tools/foc_check.py            # 第 1 部全部推算链 + 已知答案自检（当前 10/10）
python code/tools/arithmetic_check.py --demo
python tools/check_terms.py --all         # 先现象后命名 / 每章 6 个新词预算 / 行话即时解释
python tools/check_kg.py                  # 概念依赖顺序与每章引入数（图即权威清单）
python tools/depth_audit.py --selftest    # 深度度量自证：厚样本 18.00 / 薄样本 0.00
python tools/depth_audit.py               # 每章追问链、公式密度、是否落到底层、边界与代价、可代入的数
python tools/number_provenance.py --selftest  # 数源门自证：能抓出算错的等式
python tools/number_provenance.py         # 书稿里每个带单位的数，须能对上脚本输出或一手资料
python tools/build_book.py --drafts       # 装配排版源
cd print && node build.mjs                # 出 PDF
cd print && node rasterize.mjs            # 出 300 dpi 图片包
```

`number_provenance.py` 的判法是"宁可误报不漏报"：正文里同行写了算式的（`23 × 369 = 8,487`）
自动放行，没写算式又找不到出处的数一律列出。当前全书剩 7 处列出项，均为
"在别处已推导、此处只是复述"的量，已逐条人工核过（记录在 `verification/pending-fixes-2026-10-08.md`）。
