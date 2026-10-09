#!/usr/bin/env bash
# tools/rebuild_all.sh — 一条命令把 46 章草稿重建成"可印 PDF + 出版社交稿包"。
#
#   bash tools/rebuild_all.sh            # 全量重建（先重生成附录 B/E，再 9 道门）
#   bash tools/rebuild_all.sh --gates    # 只跑门，不重建产物
#
# 顺序是硬性的：草稿 → print/src → SVG 栅格化 → PDF → 交稿包 → docx。
# 每一步失败就停，绝不留下"看起来成功了"的半成品——本项目已经因 pandoc 静默
# 产出 0 图 docx 翻过一次车（见 bible/do-not-touch.md 67、68）。
set -euo pipefail
cd "$(dirname "$0")/.."
PY="python -X utf8"
fail() { echo; echo "!! 失败：$*"; exit 1; }

if [ "${1:-}" != "--gates" ]; then
  echo "── 0/9 附录 B/E 由工具输出重生成（先誊数，再装配）"
  # 这两个生成器就是附录 B/E 自称的那个"生成脚本"。它们只改机器产物：
  # B 的四个 ```text 块 + 两处计数，E.3 的 URL 清单 + 标题条数；作者写的判断段落一改就失败。
  # 放在最前面：附录改了正文，PDF 才会跟着变；跑第二次不再改动（已实测幂等）。
  $PY tools/gen_appendix_b.py || fail "gen_appendix_b.py"
  $PY tools/gen_appendix_e.py > verification/appendix-e-latest.txt 2>&1 \
      || fail "gen_appendix_e.py（明细见 verification/appendix-e-latest.txt）"
  head -1 verification/appendix-e-latest.txt

  echo "── 1/9 草稿 → print/src"
  # --drafts 是必须的：build_book.py 默认读 final/（作者定稿目录），而 final/ 现在只有
  # 一个 docx，没有 unit-NN/*.md。不带这个 flag 它会"成功"装配出 4 个文件，
  # 然后由下面的 print/src 计数门拦下（2026-10-08 实测）。
  $PY tools/build_book.py --drafts || fail "build_book.py --drafts"

  # 图内文字一旦冲出 viewBox，Chrome 打 PDF 时不会裁它，字就印到页边外（2026-10-08 实测）。
  # 所以栅格化之前先用真实字宽量一遍。修图的工具是 print/svg_grow.mjs 与 print/svg_boxfit.mjs，
  # 它们是**一次性修复**，不进这条链（反复跑会把字号叠乘越缩越小）。
  echo "── 1b/9 图形几何核对（Chrome 真实字宽：图内文字不许冲出画布）"
  ( cd print && node svg_metrics.mjs --json ) || fail "svg_metrics.mjs（图内文字冲出画布 = 会印到页边外）"

  echo "── 2/9 SVG → PNG/TIF（300 dpi）"
  ( cd print && node rasterize.mjs ) || fail "rasterize.mjs"

  # 先验源再渲染：print/src 会被并发的 build_book 清空重写，
  # 在它的空窗里跑 build.mjs 会得到一个 10 页 PDF 而退出码仍是 0。
  N_SRC=$(ls print/src/*.md 2>/dev/null | wc -l)
  [ "$N_SRC" -ge 50 ] || fail "print/src 只有 $N_SRC 个文件（应为 50）：有并发构建在写，等它结束后重跑"

  echo "── 3/9 印型 PDF（145×210 mm）"
  ( cd print && node build.mjs ) || fail "build.mjs"

  N_AFTER=$(ls print/src/*.md 2>/dev/null | wc -l)
  [ "$N_AFTER" -ge 50 ] || fail "渲染期间 print/src 掉到 $N_AFTER 个文件：这次 PDF 不可信"
  SZ=$(stat -c %s print/*.pdf | head -1)
  [ "$SZ" -gt 5000000 ] || fail "PDF 只有 $SZ 字节（正常约 14 MB）：大概率是渲染了一半的源，产物不可信"
  # 成品 PDF 才是交稿物：墨有没有越过裁口、有没有冲出留白，量它，不量浏览器预览。
python -X utf8 - <<'PYSTAR' || fail "π*0.6 的星号在成品里丢了（Markdown 把它当强调语法）"
import fitz, re, glob
pdf = glob.glob("print/*从一颗关节往下挖.pdf")[0]
txt = "".join(pg.get_text() for pg in fitz.open(pdf))
lost = len(re.findall(r"π0[.]6", txt))
kept = txt.count("π*0.6")
print("印本里 π*0.6 完好 %d 处；星号丢失 %d 处" % (kept, lost))
if lost:
    raise SystemExit("星号被吃掉 %d 处：把同段紧跟的粗体去掉，或给星号加转义" % lost)
PYSTAR
  echo "── 3b/9 印前几何核对（量成品 PDF）"
  $PY tools/pdf_qa.py > verification/pdf-qa-latest.txt 2>&1     || fail "pdf_qa.py（清单见 verification/pdf-qa-latest.txt）"
  sed -n '1,6p' verification/pdf-qa-latest.txt

  echo "── 4/9 交稿包（src-docx + 授权清单 + CIP 说明）"
  # 2026-10-09 实测事故：src-docx 从不清空，旧文件名的同一章留了一整份，
  # pandoc 拿 *.md 打包 ⇒ 交稿 docx 里第 24 章出现两遍。构建产物目录一律先清再生成。
  n_before=$(ls submission/src-docx/*.md 2>/dev/null | wc -l)
  find submission/src-docx -maxdepth 1 -name '*.md' -delete 2>/dev/null || true
  $PY tools/make_submission.py || fail "make_submission.py"

  echo "── 4b/9 交稿包引号体例（docx 走 pandoc，不经过 build.mjs 的渲染层）"
  $PY tools/fix_quotes.py --apply "submission/src-docx/*.md" || fail "交稿包引号归一"
  $PY tools/protect_html_attrs.py "submission/src-docx/*.md" || fail "HTML 属性引号还原"
  NB=$n_before $PY - <<'PYDOCX'
import collections
import glob
import io
import os
c = collections.Counter()
for p in sorted(glob.glob('submission/src-docx/*.md')):
    for line in io.open(p, encoding='utf-8').read().split('\n'):
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
PYDOCX

  echo "── 5/9 docx（必须在 src-docx 目录里跑，pandoc 按 CWD 找图）"
  ( cd submission/src-docx && pandoc *.md \
      -o "../人形机器人：从一颗关节往下挖-交稿版.docx" \
      --toc --toc-depth=2 \
      --metadata title="人形机器人：从一颗关节往下挖" ) || fail "pandoc"
fi

echo "── 5b/9 docx 页面参数与围栏体检（与印型同一张纸：145×210 mm、版心 110×176 mm）"
$PY tools/fix_docx_layout.py || fail "docx 页面参数 / 正文漏出代码围栏"

echo "── 6/9 门：算术可复算"
$PY code/tools/foc_check.py | tail -3 || fail "foc_check"
# arithmetic_check 用 exit 1 表示"还有数没测"（TBD），不是"算错了"。
# 只有出现 FAIL/异常/不一致 才算门不过；TBD 数量如实报出来，等作者真机测。
if $PY code/tools/arithmetic_check.py > /tmp/ac.txt 2>&1; then
  echo "   arithmetic_check：全部闭合"
elif grep -qi "FAIL\|异常\|不一致\|ERROR" /tmp/ac.txt; then
  tail -20 /tmp/ac.txt; fail "arithmetic_check 有算错的项"
else
  echo "   arithmetic_check：无算错项；$(grep -c TBD /tmp/ac.txt) 项 TBD 待真机测量（见 verification/teardown-measures-*.md）"
fi

echo "── 7/9 门：术语预算、概念顺序、交叉引用"
$PY tools/check_terms.py --all || fail "check_terms"
# 引号体例：中文句子里不许混 ASCII 直引号（交稿物一致性），弯引号必须配平。
# 一次性归一化用 `python tools/fix_quotes.py`（同 svg_grow 的道理：修复脚本不进链，检查进链）。
# 但 --apply 这一条**在链里**：交稿 docx 的图片标题用的是 pandoc 语法引号，
# 第一版把它一起换成弯引号 ⇒ pandoc 静默丢图（0 图 / 0.6 MB），所以这里先自证再改。
$PY tools/fix_quotes.py --selftest || fail "fix_quotes 度量本身失效"
$PY tools/fix_quotes.py --check || fail "fix_quotes --check（引号体例不一致）"
# 围栏里是字面量（`imu_type = "pelvis"`、官方英文原话），弯引号会让读者复制下来跑不通。
$PY tools/fix_quotes.py --fences-check || fail "fix_quotes --fences-check（代码块里出现弯引号）"
$PY - <<'PYFENCE' || fail "围栏内引号体例（中文说明不许用 ASCII 直引号）"
import sys
sys.path.insert(0, "tools")
import fix_quotes as fq
n = fq.fence_cjk_residue()
print("围栏内含中文的 ASCII 引号对：%d 处" % n)
if n:
    raise SystemExit("围栏里的中文说明还在用直引号（门以前跳过围栏，现在不跳）")
PYFENCE
$PY tools/check_kg.py || fail "check_kg"
$PY tools/check_xrefs.py --selftest || fail "check_xrefs 度量本身失效"
# 原来写的是 `check_xrefs.py | head -12`：在 set -o pipefail 下这条流水线的退出码是
# 左边那个门的，一旦它按设计返回非 0（比如真报了失效引用），整条重建链会在这里中止，
# 而且 head 提前关管道还会造成 SIGPIPE。formula_check 已经踩过一次，这里一并改掉。
$PY tools/check_xrefs.py > verification/xrefs-latest.txt 2>&1 || fail "check_xrefs（明细见 verification/xrefs-latest.txt）"
head -3 verification/xrefs-latest.txt
# 散文式引用（"第 NN 章说过 X"）的数字核对。这是**审阅清单，不是硬门**：
# 精度约五成，剩下的多是"把本章的数套进那一章的方法"（合法用法）。
# 判死会让人学会忽略它，所以只报不拦——但每轮都要看这个数有没有涨。
$PY tools/check_xrefs.py --claims | head -1 || true

echo "── 8/9 门：附录承诺的数与图里的数"
# 附录 B/E 写了"由脚本生成""131 条""22 条用例"这类承诺。这道门当场把工具再跑一遍核对，
# 并且规定：附录不许声称由仓库里不存在的脚本生成；找不到任何承诺时它自曝"等于没跑"。
$PY tools/appendix_drift.py --selftest || fail "appendix_drift 度量本身失效"
$PY tools/appendix_drift.py > verification/appendix-drift-latest.txt 2>&1 \
    || fail "appendix_drift（附录的数字与工具实际输出不一致，见 verification/appendix-drift-latest.txt）"
tail -1 verification/appendix-drift-latest.txt
# 图是手画的，正文改了它不会跟着变：图内每个带单位的数都必须在语料里存在，否则就是没改的旧图。
$PY tools/fig_text_check.py --selftest || fail "fig_text_check 度量本身失效"
$PY tools/fig_text_check.py > verification/fig-text-latest.txt 2>&1 \
    || fail "fig_text_check（图内数字与正文脱节，见 verification/fig-text-latest.txt）"
head -1 verification/fig-text-latest.txt
# 附录 A 写了"41 个正文章里 32 章有语录、9 章留空、5 条非逐字"。这句话本身是个可核对的事实，
# 以后加/删一条语录就会过期，所以由 quote_coverage 当场拿 quotes.yaml 重算一遍。
$PY tools/quote_coverage.py --selftest || fail "quote_coverage 度量本身失效"
$PY tools/quote_coverage.py > verification/quote-coverage-latest.txt 2>&1 \
    || fail "quote_coverage（附录 A 的语录达成度与 quotes.yaml 不一致）"
tail -1 verification/quote-coverage-latest.txt
# 蓝图覆盖矩阵那句"可自己复跑"：判别词由条目名自动取，重扫全书比对表里记的章号。
# 只有"某行全书搜不到任何词"判失败（真虚标）；"记了某章但没搜到词"是待看清单，不判死。
$PY tools/blueprint_coverage.py --selftest || fail "blueprint_coverage 度量本身失效"
$PY tools/blueprint_coverage.py > verification/blueprint-coverage-latest.txt 2>&1 \
    || fail "blueprint_coverage（覆盖矩阵里有虚标格子，见 verification/blueprint-coverage-latest.txt）"
# 第 33 批：别家一手的 [查] 必须在 research/other-vendor-firsthand.md 里有逐字原文（第七轮独立审稿指出有一批 [查] 无台账）。
# 软清单不判死（按行匹配 token 精度有限）；只有台账缺失或读不到任何 [查] 才算门在空跑。
$PY tools/check_vendor_ledger.py --selftest || fail "check_vendor_ledger 度量本身失效"
$PY tools/check_vendor_ledger.py > verification/vendor-ledger-latest.txt 2>&1 \
    || fail "check_vendor_ledger（台账缺失或 [查] 覆盖异常，见 verification/vendor-ledger-latest.txt）"
head -1 verification/blueprint-coverage-latest.txt

echo "── 9/9 门：深度 + 数源 + 产物实数核验"
$PY tools/depth_audit.py --selftest || fail "depth_audit 度量本身失效"
$PY tools/depth_audit.py | tail -25
# 数源门把脚本运行输出当语料，所以先重生成
$PY code/tools/foc_check.py > code/tools/foc_check_output.txt 2>&1 || true
$PY code/tools/arithmetic_check.py > code/tools/arithmetic_check_output.txt 2>&1 || true
$PY tools/number_provenance.py --selftest || fail "number_provenance 度量本身失效"
# 原来是 `number_provenance.py | head -20`：head 提前关管道会 SIGPIPE，pipefail 下这条流水线
# 的退出码就是左边那个门的，同一个坑在 check_xrefs 与 formula_check 上各踩过一次，这里一并改成写文件。
$PY tools/number_provenance.py > verification/numbers-latest.txt 2>&1 || true   # 只报，不 fail：误报由人逐条判，见 verification/pending-fixes-*.md
head -8 verification/numbers-latest.txt
# 把正文里每个"算式 = 结果"真的算一遍（链式等式会误报，已判过的记录在 pending-fixes F-10）
$PY tools/formula_check.py --selftest || fail "formula_check 度量本身失效"
# 20 条 ✗ 是解析器伪阳性（表格行、⇒ 链式、上标、2π 这类），已逐条分诊在
# verification/pending-fixes-2026-10-08.md 的 F-10/F-13。这里用**预算**而不是忽略：
# 基线 20 条以内放行，多出来的必须看 —— 那说明出现了新的真算式错误。
# 顺带修掉一个真 bug：原来写的是 `$PY formula_check.py | head -6`，在 set -o pipefail 下
# 这条流水线的退出码是 formula_check 的（它按设计返回 1），整条重建链会在最后一步被中止。
$PY tools/formula_check.py > verification/formula-latest.txt 2>&1 || true
head -2 verification/formula-latest.txt
N_BAD=$(grep -c "✗" verification/formula-latest.txt || true)
[ "$N_BAD" -le 20 ] || fail "formula_check 有 $N_BAD 条算式对不上，超过已分诊基线 20 条"
echo "  已分诊的解析器伪阳性 $N_BAD 条（≤20 基线），明细 verification/formula-latest.txt"

$PY - <<'PY' || fail "docx 内嵌图数量核验"
import io, zipfile, collections, yaml, os, glob, re
d = "submission/人形机器人：从一颗关节往下挖-交稿版.docx"
z = zipfile.ZipFile(d)
media = [n for n in z.namelist() if n.startswith("word/media/")]
mb = os.path.getsize(d) / 1e6
print("docx: %.1f MB, 内嵌图 %d 张" % (mb, len(media)))
# 只取路径，不要取 pandoc 的图题：`![alt](f17.png "图 17-1 … /(z̈+g) …")` 的标题里有圆括号，
# 用 `[^)]+` 会把标题一起吞进来 ⇒ 去重后凭空多出一条"引用"，这道门就会假报警（2026-10-09 实测）。
refs = {os.path.basename(m.group(1))
        for p in glob.glob("submission/src-docx/*.md")
        for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)",
                             io.open(p, encoding="utf-8").read())}
n_ref = len(refs)
absent = [r for r in refs if not os.path.exists(os.path.join("submission/src-docx", r))]
if absent:
    raise SystemExit("src-docx 引用了不存在的图片文件：%s" % absent[:5])
n_svg = len(glob.glob("assets/fig/*.svg"))
print("src-docx 去重后图引用 %d 条；assets/fig SVG %d 张" % (n_ref, n_svg))
if len(media) != n_ref:
    raise SystemExit("内嵌图 %d != 去重引用 %d（pandoc 又静默丢图了）" % (len(media), n_ref))
if len(media) != n_svg:
    print("提示：图 %d 张，SVG %d 张，差 %d（待拍图未落地属正常）" % (len(media), n_svg, n_svg - len(media)))
t = io.open("project-status.yaml", encoding="utf-8").read()
k = [l.split(":")[0] for l in t.split("\n")
     if l and not l[0].isspace() and not l.startswith("#") and ":" in l]
dup = [x for x, c in collections.Counter(k).items() if c > 1]
if dup:
    raise SystemExit("project-status.yaml 顶层键重复，会被静默覆盖：%s" % dup)
print("project-status.yaml 顶层键唯一 ✓")
PY

echo
echo "全部通过。产物："
ls -la print/*.pdf submission/*.docx 2>/dev/null | sed 's/^/  /'
