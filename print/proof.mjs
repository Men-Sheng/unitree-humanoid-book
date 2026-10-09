// print/proof.mjs — 印前目视核对的自动化替身：分页、截图、并检查有没有东西溢出页面。
//
// 为什么要有它：交稿 DoD 第 6 条要求"逐页目视核对"（图不压字、表格不冲出页、
// 章末不留空页）。46 章 500+ 页靠人翻不现实，但**溢出与空页是可以量出来的**。
// 这个脚本把可量的一部分量掉，再把关键页截图给人看。
//
// 量什么（v2，上一版误报的教训）：
//   1. WIDE    —— 元素的右边界越过「版心」右边界。上一版比的是整页（含出血/白边），
//                 凡是表格贴到版心右沿就被判成溢出，21 处里绝大多数是这种假阳性。
//   2. SCROLL  —— 元素自己的 scrollWidth > clientWidth：内容被它自己的盒子切掉了。
//                 这才是"打印机出来缺一块字"的真信号。
//   3. THIN    —— 正文 <40 字的页，章末空页。
// 三者都打印证据（宽度、版心、类名、文本片段），存疑的页单独截图，
// 由人看图判定，不靠脚本一句话下结论。
//
// 用法：cd print && node proof.mjs
// 产出：print/proof/<页标记>.png + <页号>-overflow-*.png + 控制台报告
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const root = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(root, 'build', 'book.html');
const outDir = path.join(root, 'proof');
await mkdir(outDir, { recursive: true });
const chrome = process.env.CHROME_PATH ||
  (process.platform === 'win32'
    ? 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');

const html = await readFile(htmlPath, 'utf8');
const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'] });
const page = await browser.newPage();
await page.setViewport({ width: 1000, height: 1400, deviceScaleFactor: 2 });
page.on('pageerror', e => console.log('PAGEERROR', String(e).slice(0, 160)));

const tmp = path.join(root, 'build', 'proof.html');
await writeFile(tmp, html, 'utf8');
await page.goto('file://' + tmp, { waitUntil: 'load', timeout: 180_000 });
await page.waitForFunction('window.__pagedDone || window.__pagedError', { timeout: 420_000 })
  .catch(async () => {
    // book.html 里的 PagedConfig.auto=false 是给 build.mjs 用的；
    // 直接加载时要自己触发分页。
    await page.evaluate(`(async () => {
      await window.PagedPolyfill.preview();
      window.__pagedDone = true;
    })()`);
    await page.waitForFunction('window.__pagedDone', { timeout: 420_000 });
  });

const report = await page.evaluate((markers) => {
  const pages = [...document.querySelectorAll('.pagedjs_page')];
  const out = { total: pages.length, overflow: [], thin: [], found: {}, cbWidths: [], contentProbe: null };

  // 版心盒子：Paged.js 用 .pagedjs_page_content 表示去掉了页边距的内容区。
  // 找不到就退回"整页矩形 - padding"，并把这个事实打进报告（别悄悄换口径）。
  const first = pages[0];
  let selUsed = 'none';
  if (first) {
    const probe = first.querySelector('.pagedjs_page_content');
    selUsed = probe ? '.pagedjs_page_content' : 'page rect - padding';
    const pr = probe ? probe.getBoundingClientRect() : null;
    const cs = getComputedStyle(first);
    out.contentProbe = {
      sel: selUsed,
      pageW: Math.round(first.getBoundingClientRect().width),
      contentW: Math.round(pr ? pr.width
        : first.getBoundingClientRect().width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)),
      paddingLeft: cs.paddingLeft, paddingRight: cs.paddingRight,
    };
  }

  pages.forEach((pg, i) => {
    const pr = pg.getBoundingClientRect();
    const content = pg.querySelector('.pagedjs_page_content');
    let cb = content ? content.getBoundingClientRect() : null;
    if (!cb) {
      const cs = getComputedStyle(pg);
      const pl = parseFloat(cs.paddingLeft) || 0, prr = parseFloat(cs.paddingRight) || 0;
      cb = { left: pr.left + pl, right: pr.right - prr, width: pr.width - pl - prr };
    }
    if (i > 0) out.cbWidths.push(Math.round(cb.width));
    const txt = (pg.textContent || '').replace(/\s+/g, ' ').trim();

    pg.querySelectorAll('img, table, pre, svg').forEach(el => {
      const b = el.getBoundingClientRect();
      const wide = b.right > cb.right + 1.5 || b.left < cb.left - 1.5 || b.width > cb.width + 1.5;
      const scroll = el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0;
      if (wide || scroll) {
        out.overflow.push({
          page: i + 1, tag: el.tagName,
          kind: (wide && scroll) ? 'WIDE+SCROLL' : (wide ? 'WIDE' : 'SCROLL'),
          w: Math.round(b.width), cw: Math.round(cb.width),
          over: Math.round(b.right - cb.right),
          scrollW: el.scrollWidth, clientW: el.clientWidth,
          cls: (el.className || '').toString().slice(0, 24),
          txt: (el.getAttribute('alt') || el.textContent || '')
            .replace(/\s+/g, ' ').trim().slice(0, 60),
        });
      }
    });
    if (txt.length < 40 && i > 1 && i < pages.length - 1) {
      out.thin.push({ page: i + 1, chars: txt.length, head: txt.slice(0, 30) });
    }
    for (const m of markers) {
      if (!out.found[m] && txt.includes(m)) out.found[m] = i + 1;
    }
  });
  return out;
}, ['图 00-1', '图 04-1', '图 11-1', '图 19-1', '图 26-1', '目录', 'CIP', '参考文献', '附录 C']);

const p = report.contentProbe || {};
const uniq = [...new Set(report.cbWidths)].sort((a, b) => a - b);
console.log('分页数 %s', report.total);
console.log('页宽 %s px ｜ 封面页版心 %s px（口径：%s）｜ 其余各页版心宽度集合 %j',
  p.pageW, p.contentW, p.sel, uniq);
console.log('溢出元素 %s 处（WIDE=冲出版心，SCROLL=被自己的盒子切掉）', report.overflow.length);
for (const o of report.overflow) {
  console.log('  页 %s <%s> %s 宽 %s/版心 %s 越界 %s px scroll %s>%s ｜ %s ｜ %s',
    o.page, o.tag, o.kind.padEnd(11), o.w, o.cw, o.over, o.scrollW, o.clientW, o.cls, o.txt);
}
console.log('疑似空页（正文 <40 字）%s 处', report.thin.length);
report.thin.slice(0, 10).forEach(t =>
  console.log('  页 %s ｜ %s 字 ｜ %s', t.page, t.chars, t.head));

async function shot(n, label) {
  const el = await page.evaluateHandle(
    (i) => document.querySelectorAll('.pagedjs_page')[i - 1], n);
  try {
    await el.screenshot({ path: path.join(outDir, `p${String(n).padStart(3, '0')}-${label}.png`) });
    return true;
  } catch (e) { console.log('  截图失败', label, String(e).slice(0, 60)); return false; }
}

console.log('关键页定位：');
const shots = [];
for (const [m, n] of Object.entries(report.found)) {
  console.log('  %s 第 %s 页', m.padEnd(8), n);
  shots.push([m, n]);
}
for (const [m, n] of shots.slice(0, 8)) await shot(n, m);

// 存疑页逐页截图（同一页只截一次），给人眼判定用。
const suspect = [...new Set(report.overflow.map(o => o.page))].slice(0, 12);
for (const n of suspect) await shot(n, 'overflow');
if (suspect.length) console.log('存疑页截图：', suspect.join(', '));
await browser.close();
console.log('截图写入 print/proof/');
