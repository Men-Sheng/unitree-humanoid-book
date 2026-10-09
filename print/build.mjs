// Builds a book from src/*.md into build/book.html and "<title>.pdf", using
// the title in book.json. Markdown is rendered with marked; Mermaid renders the
// diagrams and Paged.js paginates (running heads, TOC page numbers) inside
// headless Chrome, which puppeteer-core drives to print the PDF.
import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { Marked } from 'marked';
import puppeteer from 'puppeteer-core';

const root = path.dirname(fileURLToPath(import.meta.url));
const srcDir = path.join(root, 'src');
const outDir = path.join(root, 'build');
const book = JSON.parse(await readFile(path.join(root, 'book.json'), 'utf8'));
const pdfPath = path.join(root, `${book.title.replace(/[\\/:*?"<>|]/g, '-')}.pdf`);
const chrome =
  process.env.CHROME_PATH ??
  (process.platform === 'win32'
    ? 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');

const slugCounts = new Map();
// CJK-safe slug: the upstream version strips everything outside a-z0-9, so a
// Chinese heading collapses to "" and <a href="#"> crashes Paged.js
// (querySelector('#') is not a valid selector). Keep any letter/number (incl.
// CJK) and always return a non-empty, CSS-identifier-safe id.
function slugify(text) {
  let base = text
    .toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/[`'’"]/g, '')
    .replace(/[^\p{L}\p{N}_-]+/gu, '-')
    .replace(/^-+|-+$/g, '');
  if (!base || /^[0-9]/.test(base)) base = base ? `h-${base}` : 'sec';
  const n = slugCounts.get(base) ?? 0;
  slugCounts.set(base, n + 1);
  return n === 0 ? base : `${base}-${n}`;
}

const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Convert GitHub-style alert blockquotes into styled callout blocks.
function convertCallouts(md) {
  const lines = md.split('\n');
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^> \[!(NOTE|IMPORTANT|WARNING|QUOTE|FIGURE)\]\s*$/);
    if (!m) {
      out.push(lines[i]);
      continue;
    }
    const body = [];
    while (i + 1 < lines.length && lines[i + 1].startsWith('>')) {
      body.push(lines[++i].replace(/^> ?/, ''));
    }
    const kind = m[1].toLowerCase();
    // QUOTE 块不显示 "Quote" 标题——它靠排版样式与署名行自证身份
    const label = kind === 'quote' ? '' : m[1][0] + m[1].slice(1).toLowerCase();
    out.push(
      `<div class="callout ${kind}"><div class="callout-label">${label}</div>`,
      '',
      ...body,
      '',
      '</div>',
    );
  }
  return out.join('\n');
}

const files = (await readdir(srcDir)).filter((f) => f.endsWith('.md')).sort();
const toc = [];
let chapter = 0;
let chapterNo = 0;      // 用于图号：图 章-序
let figN = 0;
let appendix = 0;
let currentChapterId = null;

const marked = new Marked({
  gfm: true,
  renderer: {
    heading({ tokens, depth, text }) {
      const raw = text;
      const attr = raw.match(/\s*\{\.(unnumbered|appendix)\}\s*$/);
      const custom = raw.match(/\s*\{#([\w.-]+)\}\s*$/);
      const clean = raw.replace(/\s*\{[#.][^}]*\}\s*$/, '');
      const inner = this.parser.parseInline(
        new Marked().lexer(clean)[0]?.tokens ?? tokens,
      );
      if (clean === 'Contents') return `<h2 class="toc-title">目录</h2>`;
      const id = custom ? custom[1] : slugify(clean);
      if (depth === 1) {
        let label = '';
        let cls = 'chapter';
        if (attr?.[1] === 'unnumbered') {
          cls = 'chapter unnumbered';
        } else if (attr?.[1] === 'appendix') {
          label = `附录 ${String.fromCharCode(65 + appendix)}`;
          chapterNo = String.fromCharCode(65 + appendix); appendix += 1; figN = 0;
          cls = 'chapter appendix';
        } else {
          chapterNo = ++chapter; figN = 0;
          label = `第 ${String(chapter).padStart(2, "0")} 章`;
        }
        currentChapterId = id;
        toc.push({ depth: 1, id, text: inner, label });
        return `<section class="${cls}-start"><div class="chapter-label">${label}</div><h1 id="${id}" class="${cls}">${inner}</h1></section>`;
      }
      if (depth === 2) toc.push({ depth: 2, id, text: inner, parent: currentChapterId });
      return `<h${depth} id="${id}">${inner}</h${depth}>`;
    },
    paragraph({ tokens }) {
      const inner = this.parser.parseInline(tokens);
      if (/^<strong>Figure /.test(inner)) return `<p class="figcaption">${inner}</p>\n`;
      return `<p>${inner}</p>\n`;
    },
    image(token, ...rest) {
      // marked ≥ v12 传的是 token 对象；旧签名 (href, title, text) 仍兼容。
      const href = typeof token === 'string' ? token : (token && token.href) || '';
      const title = (typeof token === 'object' && token && token.title) ?? rest[0] ?? '';
      const text = (typeof token === 'object' && token && token.text) ?? rest[1] ?? '';
      figN += 1;
      // 台账里的 path 相对仓库根；HTML 从 print/build/ 加载，必须转成绝对 file URL。
      const src = /^[a-z]+:|^\//.test(href)
        ? href
        : 'file:///' + path.resolve(root, '..', href).split(path.sep).join('/');
      const cap = title ? `<figcaption>${title}</figcaption>` : '';
      return `<figure class="fig"><img src="${src}" alt="${escapeHtml(String(text))}" />${cap}</figure>`;
    },
    code({ text, lang }) {
      if (lang === 'mermaid') return `<pre class="mermaid">${escapeHtml(text)}</pre>`;
      return `<pre class="code"><code class="lang-${lang ?? 'text'}">${escapeHtml(text)}</code></pre>`;
    },
  },
});

let body = '';
// 章/附录开头的"口径声明"引用块打上 scope-note 类（版式见 style.css）。
// 判据很窄：只处理**第一个 <h2 之前**出现的那一个 blockquote——正文里的引用都在 h2 之后，
// 而 QUOTE/WARNING 这类 callout 早就被 convertCallouts 变成 div 了，不会被误伤。
const markScopeNote = (html) => {
  const q = html.indexOf('<blockquote>');
  const h2 = html.search(/<h[23][ >]/);
  if (q < 0) return html;
  if (h2 >= 0 && q > h2) return html;
  return html.slice(0, q) + '<blockquote class="scope-note">' + html.slice(q + '<blockquote>'.length);
};
// 长参考表打 class：阈值 6 行——附录 D 的入口表 10 行、附录 A 的术语表十几行，
// 都是"整表不许断就会把表头挤成半页孤行"的量级（2026-10-09 量成品 PDF 第 497 页发现的）。
const countRows = (inner) => (inner.match(/<tr/g) || []).length;
const markLongTables = (html) =>
  html.replace(/<table>([\s\S]*?)<\/table>/g, (m, inner) =>
    (countRows(inner) > 6 ? '<table class="long">' + inner + '</table>' : m));
// 引号体例：中文句子里不许混 ASCII 直引号。草稿已由 tools/fix_quotes.py 归一，
// 但**章题、目录、页眉、版权页、语录出处**这些文字来自 outline/units.yaml、bible/quotes.yaml
// 和 build_book 的模板，改它们的 ASCII 引号会连带改到 YAML 的结构引号——所以在渲染这一层统一换。
// 规则：HTML 标签本身不动（alt="…" 里也有引号）；pre/code/style/script 内不动；只换"成对且含中文"的。
// marked 会把文本里的 " 转义成 &quot;，所以只匹配字面 `"` 会**假报 0 残留**（2026-10-09 实测：
// 计数器说干净，成品 PDF 第 2、5、11 页照样是 "未公布"）。先把 &quot; 换成哨兵字符再配对。
const QUOT = /&quot;|"/g;
// 保护"整块"元素（含内容）与单个标签，**只改它们之间的文本**。
// 顺序很要紧：先按单个标签切会把 <script> 的开标签吃掉，脚本内容就被当正文——
// 2026-10-09 实测那样会把 Paged.js 的 querySelectorAll 选择器里的引号换成 &quot;，
// 于是抛 "not a valid selector"，整本 PDF 渲染不出来。
const PROTECT = /<(?:pre|code|style|script)\b[\s\S]*?<\/(?:pre|code|style|script)>|<[^>]*>/g;
const quoteText = (txt) => txt.replace(QUOT, '␟')
  .replace(/␟([^␟\n]*[一-鿿][^␟\n]*)␟/g, (_, inner) => `“${inner}”`)
  .replace(/␟/g, '&quot;');
const walkText = (html, fn) => {
  let out = '', last = 0;
  for (const m of html.matchAll(PROTECT)) {
    out += fn(html.slice(last, m.index)) + m[0];
    last = m.index + m[0].length;
  }
  return out + fn(html.slice(last));
};
const typographicQuotes = (html) => walkText(html, quoteText);
// 残留计数走**同一套** walkText：一对被 <strong> 切开的引号是构建改不动的东西，
// 把它数成残留会让人学会忽略这条门。
const countCjkStraightQuotes = (html) => {
  let n = 0;
  walkText(html, (t) => {
    const m = t.replace(QUOT, '␟').match(/␟[^␟\n]*[一-鿿][^␟\n]*␟/g);
    if (m) { n += m.length; console.log('  未替换的中文直引号对：', m.slice(0, 3)); }
    return '';
  });
  return n;
};
const renderFile = (md) => markLongTables(markScopeNote(marked.parse(md)));
for (const file of files) {
  const md = convertCallouts(await readFile(path.join(srcDir, file), 'utf8'));
  body += `<div class="file file-${file.replace(/\.md$/, '')}">${renderFile(md)}</div>\n`;
}

const tocHtml =
  '<ul class="toc">' +
  toc
    .map((e) =>
      e.depth === 1
        ? `<li class="toc-1"><a href="#${e.id}"><span class="toc-label">${e.label}</span><span class="toc-text">${e.text}</span></a></li>`
        : `<li class="toc-2"><a href="#${e.id}"><span class="toc-text">${e.text}</span></a></li>`,
    )
    .join('') +
  '</ul>';
body = body.replace(
  /(<p class="figcaption">[\s\S]*?<\/p>)\s*(<pre class="mermaid">[\s\S]*?<\/pre>)/g,
  '<figure>$1$2</figure>',
);
body = body.replace('<nav id="toc"></nav>', `<nav id="toc">${tocHtml}</nav>`);

const css = (await readFile(path.join(root, 'style.css'), 'utf8')).replaceAll('__BOOK_TITLE__', book.title.replace(/"/g, '\\"'));
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>${book.title}</title>
<style>${css}</style>
<script>window.PagedConfig = { auto: false };</script>
<script src="../node_modules/mermaid/dist/mermaid.min.js"></script>
<script src="../node_modules/pagedjs/dist/paged.polyfill.js"></script>
</head><body>${body}
<script>
  (async () => {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
      fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif',
      flowchart: { htmlLabels: true, curve: 'basis' }, sequence: { useMaxWidth: true } });
    await mermaid.run({ querySelector: 'pre.mermaid' });
    await window.PagedPolyfill.preview();
    window.__pagedDone = true;
  })().catch((e) => { window.__pagedError = String(e && e.stack || e); });
</script>
</body></html>`;

await mkdir(outDir, { recursive: true });
const htmlPath = path.join(outDir, 'book.html');
const finalHtml = typographicQuotes(html);
const leftQuotes = countCjkStraightQuotes(finalHtml);
console.log(`引号体例（渲染层）：中文直引号残留 ${leftQuotes} 对；` +
  `弯引号 ${finalHtml.split('“').length - 1}/${finalHtml.split('”').length - 1}`);
if (leftQuotes > 0) {
  console.error('!! 渲染层还有没换掉的中文直引号，不写出 HTML（宁可不产 PDF，也不交一份体例不一致的稿子）');
  process.exit(1);
}
await writeFile(htmlPath, finalHtml);

const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ['--allow-file-access-from-files'] });
try {
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.error('pageerror', e.message));
  await page.goto('file://' + htmlPath, { waitUntil: 'load', timeout: 120_000 });
  await page.waitForFunction('window.__pagedDone || window.__pagedError', { timeout: 300_000 });
  const err = await page.evaluate('window.__pagedError');
  if (err) throw new Error(err);
  const pages = await page.evaluate('document.querySelectorAll(".pagedjs_page").length');
  await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true, timeout: 300_000 });
  console.log(`Wrote ${pdfPath} (${pages} pages)`);
} finally {
  await browser.close();
}
