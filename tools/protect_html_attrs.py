#!/usr/bin/env python3
"""tools/protect_html_attrs.py — 把渲染层/交稿包里被中文弯引号吃掉的 HTML 属性引号换回 ASCII。

背景：`fix_quotes.py --apply` 按段落归一引号，它保护 Markdown 链接目标（按括号深度）但**不认 HTML 标签**
（那套保护写在 build.mjs 的渲染层里）。结果 `submission/src-docx/000-cover.md` 里的
`<div class="cover-kicker">` 变成 `<div class=“cover-kicker”>`，pandoc 直接把 class 吞掉，
交稿包的封面排版无声丢失（2026-10-09 实测，document.xml 里没有 cover-kicker）。

规则：只在 `<` … `>` 之间动，把 `=“…”` / `=“…”` 形式的属性值换回 ASCII 双引号；标签外一律不碰。
用法：python -X utf8 tools/protect_html_attrs.py "submission/src-docx/*.md" [--selftest]
"""
import glob
import io
import re
import sys

ATTR = re.compile(r'=\u201c([^\u201c\u201d<>]*)\u201d')


def fix_text(s):
    n = 0

    def repl(m):
        nonlocal n
        inner = ATTR.sub(lambda a: '="%s"' % a.group(1), m.group(0))
        if inner != m.group(0):
            n += 1
        return inner
    out = re.sub(r'<[^>]*>', repl, s)
    return out, n


def main():
    if '--selftest' in sys.argv:
        bad = '<div class=“cover-kicker”>字</div><p class=“a b”>x</p>'
        good, k = fix_text(bad)
        ok1 = k == 2 and good == '<div class="cover-kicker">字</div><p class="a b">x</p>'
        zh = '他说“你好”，然后走了。'          # 标签外的中文引号必须原样不动
        good2, k2 = fix_text(zh)
        ok3 = k2 == 0 and good2 == zh
        img = '![图](f.png “题”) 与 <img src=“a.png”>'   # 链接目标不在标签里，本工具不碰
        good3, k3 = fix_text(img)
        ok4 = k3 == 1 and '“题”' in good3 and 'src="a.png"' in good3
        for label, ok in [('标签内属性引号还原', ok1), ('标签外中文引号不动', ok3), ('链接目标不误伤', ok4)]:
            print(('PASS ' if ok else 'FAIL ') + label)
        return 0 if (ok1 and ok3 and ok4) else 1
    pat = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not pat:
        print('用法：protect_html_attrs.py "<glob>"（或 --selftest）')
        return 1
    total = 0
    files = 0
    for g in pat:
        for p in sorted(glob.glob(g)):
            t = io.open(p, encoding='utf-8').read()
            new, n = fix_text(t)
            if n:
                io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
                total += n
                files += 1
                print('  还原 %d 处：%s' % (n, p))
    print('HTML 属性引号还原：%d 处 / %d 个文件' % (total, files))
    return 0


if __name__ == '__main__':
    sys.exit(main())
