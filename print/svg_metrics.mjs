// print/svg_metrics.mjs — 用 Chrome 自己量图：文字有没有冲出画布、有没有压住它所在的盒子。
//
// 为什么不用 Python 估字号（tools/svg_check.py 的 --fix 就是估的）：
//   估过两次都错。CJK 按整字宽、ASCII 按 0.55em 的模型，在 f10-clarke-park.svg 上判
//   “τ_cmd ÷ k_t = i_q_ref” 装得进 200 单位的盒子，而 Chrome 真渲染出来压住了边框
//   —— font-family 里的 Cascadia Mono 这台机器没装，τ ÷ ⇒ 这些字符还要走 fallback。
//   字宽由渲染器决定，那就问渲染器：把 SVG 内联进页面，用 getBBox() 取用户坐标。
//
// 判定（用户坐标，与 viewBox 同单位）：
//   OUT_OF_CANVAS  任一 text/path/rect 的 getBBox 超出 viewBox → 成品 PDF 会冲出页边。
//                  （Chrome 打 PDF 时不按 viewBox 裁 <img> 里的 SVG，2026-10-08 实测）
//   OUT_OF_BOX     文字中心落在某个 rect 内，但整行装不下 → 字压在边框上
// 用法：cd print && node svg_metrics.mjs [--json]
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const figDir = path.join(root, 'assets', 'fig');
const chrome = process.env.CHROME_PATH ||
  (process.platform === 'win32'
    ? 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');

const names = (await readdir(figDir)).filter(f => f.endsWith('.svg')).sort();
const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const page = await browser.newPage();
const rows = [];
for (const name of names) {
  const svg = await readFile(path.join(figDir, name), 'utf8');
  await page.setContent(`<!doctype html><meta charset="utf-8"><body style="margin:0">${svg}</body>`,
    { waitUntil: 'load' });
  const r = await page.evaluate(() => {
    const svg = document.querySelector('svg');
    if (!svg) return null;
    const vb = svg.viewBox && svg.viewBox.baseVal;
    const W = vb && vb.width ? vb.width : svg.clientWidth;
    const H = vb && vb.height ? vb.height : svg.clientHeight;
    const rects = [...svg.querySelectorAll('rect')].map(el => el.getBBox())
      .filter(b => b.width > 4 && b.height > 4);
    const canvas = [], box = [];
    for (const el of svg.querySelectorAll('text')) {
      const b = el.getBBox();
      const txt = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
      if (!txt) continue;
      if (b.x + b.width > W + 2 || b.x < -2 || b.y + b.height > H + 2 || b.y < -2) {
        canvas.push({ txt, kind: 'TEXT', x: +b.x.toFixed(1), right: +(b.x + b.width).toFixed(1),
          y: +b.y.toFixed(1), bottom: +(b.y + b.height).toFixed(1), W, H });
      }
      const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
      const host = rects.filter(q => q.x <= cx && cx <= q.x + q.width && q.y <= cy && cy <= q.y + q.height)
        .sort((p, q) => (p.width * p.height) - (q.width * q.height))[0];
      if (host) {
        const over = Math.max(b.x + b.width - (host.x + host.width), host.x - b.x,
          b.y + b.height - (host.y + host.height), host.y - b.y);
        if (over > 3) box.push({ txt, over: +over.toFixed(1), tw: +b.width.toFixed(1),
          bw: +host.width.toFixed(1) });
      }
    }
    for (const el of svg.querySelectorAll('path, line, polyline, circle, ellipse, image, g')) {
      if (el.tagName === 'g' && el.parentElement !== svg) continue;
      const b = el.getBBox();
      if (!b.width || !b.height) continue;
      if (b.x + b.width > W + 6 || b.x < -6 || b.y + b.height > H + 6 || b.y < -6) {
        canvas.push({ txt: `<${el.tagName}>`, kind: 'GEOM', x: +b.x.toFixed(1),
          right: +(b.x + b.width).toFixed(1), y: +b.y.toFixed(1),
          bottom: +(b.y + b.height).toFixed(1), W, H });
      }
    }
    return { canvas, box };
  });
  if (!r) { rows.push({ name, kind: 'ERR', txt: '没有 <svg>' }); continue; }
  for (const c of r.canvas) rows.push({ name, ...c });
  for (const c of r.box) rows.push({ name, kind: 'OUT_OF_BOX', ...c });
}
await browser.close();

if (process.argv.includes('--json')) {
  await writeFile(path.join(root, 'verification', 'svg-metrics.json'), JSON.stringify(rows, null, 1));
  console.log('写入 verification/svg-metrics.json');
}
const canvas = rows.filter(r => ['TEXT', 'GEOM', 'ERR'].includes(r.kind));
const box = rows.filter(r => r.kind === 'OUT_OF_BOX');
console.log(`量了 ${names.length} 张图：冲出画布 ${canvas.length} 处，压边框 ${box.length} 处`);
for (const r of canvas.slice(0, 22)) {
  console.log(`  [画布 ${r.kind}] ${r.name} x ${r.x}→${r.right}/${r.W} y ${r.y}→${r.bottom}/${r.H} ｜ ${r.txt}`);
}
for (const r of box.slice(0, 22)) {
  console.log(`  [盒子] ${r.name} 超出 ${r.over}（字宽 ${r.tw} 对盒宽 ${r.bw}）｜ ${r.txt}`);
}
// 只有 OUT_OF_CANVAS 判失败：它会印到页边外。压住自己盒子边框是外观项，报出来不阻断。
process.exit(canvas.length ? 1 : 0);
