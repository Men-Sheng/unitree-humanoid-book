// print/svg_boxfit.mjs — 图里压住自己盒子边框的文字：在 DOM 上缩它的字号，再把整张图写回。
//
// 为什么改 DOM 而不是正则改源文件：svg_fit.mjs 用「源文件里第 N 个 <text>」对上「DOM 里
// 第 N 个 text」，实测对不上（改了 24 行，复量仍有 23 处没变）—— 与其继续猜为什么对不上，
// 不如让浏览器自己改、自己序列化。改完立刻用同一把尺复量，改没改看得见。
// 只缩字号（写内联 style，呈现属性打不过 <style> 里的 class），且只缩到 86%（再小印出来就看不清了）；缩完仍装不下的，报出来留给排版的人。
// 用法：cd print && node svg_boxfit.mjs [--dry]
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const figDir = path.join(root, 'assets', 'fig');
const chrome = process.env.CHROME_PATH || (process.platform === 'win32'
  ? 'C:/Program Files/Google/Chrome/Application/chrome.exe'
  : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
const INSET = 6, FLOOR = 0.86, MIN_OVER = 4;
const dry = process.argv.includes('--dry');

const fit = ({ inset, floor, minOver }) => {
  const svg = document.querySelector('svg');
  const rects = [...svg.querySelectorAll('rect')].map(el => ({ b: el.getBBox(), el }))
    .filter(r => r.b.width > 8 && r.b.height > 8);
  let changed = 0; const left = [];
  for (const el of svg.querySelectorAll('text')) {
    const b = el.getBBox();
    const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
    const host = rects
      .filter(r => r.b.x <= cx && cx <= r.b.x + r.b.width && r.b.y <= cy && cy <= r.b.y + r.b.height
        && r.b.height >= b.height * 0.9)
      .sort((p, q) => (p.b.width * p.b.height) - (q.b.width * q.b.height))[0];
    if (!host) continue;
    const over = Math.max(b.x + b.width - (host.b.x + host.b.width), host.b.x - b.x,
      b.y + b.height - (host.b.y + host.b.height), host.b.y - b.y);
    if (over < minOver) continue;
    const need = Math.min((host.b.width - 2 * inset) / b.width, (host.b.height - 0.8 * inset) / b.height);
    const f = Math.max(floor, Math.min(1, need));
    if (f > 0.995) continue;
    const cur = parseFloat(el.getAttribute('font-size') || getComputedStyle(el).fontSize) || 16;
    el.style.fontSize = (cur * f).toFixed(2) + 'px';   // 内联样式才压得住 class 里的 font-size
    changed++;
    const nb = el.getBBox();
    const over2 = Math.max(nb.x + nb.width - (host.b.x + host.b.width), host.b.x - nb.x,
      nb.y + nb.height - (host.b.y + host.b.height), host.b.y - nb.y);
    if (over2 > minOver) left.push({ txt: (el.textContent || '').trim().slice(0, 34),
      over: +over2.toFixed(1), bw: +host.b.width.toFixed(1) });
  }
  return { svg: changed ? svg.outerHTML : '', changed, left };
};

const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const page = await browser.newPage();
const names = (await readdir(figDir)).filter(f => f.endsWith('.svg')).sort();
let total = 0; const residual = [];
for (const name of names) {
  const file = path.join(figDir, name);
  const src = await readFile(file, 'utf8');
  await page.setContent(`<!doctype html><meta charset="utf-8"><body style="margin:0">${src}</body>`,
    { waitUntil: 'load' });
  const r = await page.evaluate(fit, { inset: INSET, floor: FLOOR, minOver: MIN_OVER });
  for (const l of r.left) residual.push({ name, ...l });
  if (r.changed) {
    total += r.changed;
    const head = src.slice(0, src.indexOf('<svg'));
    if (!dry) await writeFile(file, head + r.svg.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"'));
    console.log(`  ${name} 缩了 ${r.changed} 行`);
  }
}
await browser.close();
console.log(`${dry ? '[dry] ' : ''}合计缩了 ${total} 行压边框的文字（地板 ${FLOOR}）`);
console.log(`缩到地板仍压边框：${residual.length} 处`);
for (const r of residual.slice(0, 16)) console.log(`  ${r.name} 仍超 ${r.over}（盒宽 ${r.bw}）｜ ${r.txt}`);
