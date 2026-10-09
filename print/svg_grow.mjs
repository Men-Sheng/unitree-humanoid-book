// print/svg_grow.mjs — 画布装不下内容时，把 viewBox 长到装得下（而不是缩字号）。
//
// 为什么选「长画布」而不是「缩字」：
//   缩字会逐行改变字与字、字与盒子的相对关系，改一处可能撞另一处（svg_fit.mjs 实测：
//   24 行改动后仍有 23 处装不下，而且缩到 72% 的标注印出来只有 4 pt，比缺陷更糟）。
//   长画布是纯几何：所有元素的相对位置一模一样，整张图在纸上等比小一点点，
//   版心 110 mm 定宽下最多小几个百分点，肉眼无感，且不可能制造新的压字。
//   冲出画布这一类（成品 PDF 里字跑到页边外）就此归零。
// 用法：cd print && node svg_grow.mjs [--dry]
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const figDir = path.join(root, 'assets', 'fig');
const chrome = process.platform === 'win32'
  ? 'C:/Program Files/Google/Chrome/Application/chrome.exe'
  : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PAD = 8;
const dry = process.argv.includes('--dry');

const probe = () => {
  const svg = document.querySelector('svg');
  const b = svg.getBBox();                       // 所有子元素的并集，用户坐标
  const vb = svg.viewBox.baseVal;
  return { bb: { x: b.x, y: b.y, w: b.width, h: b.height },
    vb: { x: vb.x, y: vb.y, w: vb.width, h: vb.height } };
};

const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || chrome,
  headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const page = await browser.newPage();
const names = (await readdir(figDir)).filter(f => f.endsWith('.svg')).sort();
let n = 0;
for (const name of names) {
  const file = path.join(figDir, name);
  const src = await readFile(file, 'utf8');
  await page.setContent(`<!doctype html><meta charset="utf-8"><body style="margin:0">${src}</body>`,
    { waitUntil: 'load' });
  const { bb, vb } = await page.evaluate(probe);
  const x = Math.min(vb.x, bb.x - PAD), y = Math.min(vb.y, bb.y - PAD);
  const w = Math.max(vb.x + vb.w, bb.x + bb.w + PAD) - x;
  const h = Math.max(vb.y + vb.h, bb.y + bb.h + PAD) - y;
  const same = Math.abs(x - vb.x) < 0.5 && Math.abs(y - vb.y) < 0.5
    && Math.abs(w - vb.w) < 0.5 && Math.abs(h - vb.h) < 0.5;
  if (same) continue;
  const grow = ((w * h) / (vb.w * vb.h) - 1) * 100;
  const out = src.replace(/viewBox="[^"]*"/,
    `viewBox="${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)}"`);
  console.log(`  ${name} viewBox ${vb.w.toFixed(0)}×${vb.h.toFixed(0)} → ${w.toFixed(0)}×${h.toFixed(0)} `
    + `（面积 +${grow.toFixed(1)}%，内容并集 x ${bb.x.toFixed(0)}→${(bb.x + bb.w).toFixed(0)}）`);
  n++;
  if (!dry) await writeFile(file, out);
}
await browser.close();
console.log(`${dry ? '[dry] ' : ''}长画布 ${n} 张，其余 ${names.length - n} 张本来就装得下`);
