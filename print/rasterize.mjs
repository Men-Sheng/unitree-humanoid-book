// print/rasterize.mjs — 把 assets/fig/*.svg 光栅化成出版社图片包（300 dpi）
//
// 为什么用 Chrome 而不是 cairosvg：本机没有 cairo 绑定，而 Chrome 已经在排版管线里，
// 且它渲染 SVG 里的 <text> 时用的是**正文同一套字体解析**（Noto Sans/Serif SC），
// 光栅化结果与 PDF 里的矢量版一致——不会出现"图在书里一个样、交稿包里另一个样"。
//
// 版心宽 = 145 − 20 − 15 = 110 mm；300 dpi ⇒ 110/25.4*300 ≈ 1299 px。
// 每张图同时输出 PNG（交 docx 用）与 TIF（无压缩，印厂常用），并写一张尺寸表。

import { mkdir, readFile, writeFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const figDir = path.join(root, "assets", "fig");
const outDir = path.join(root, "submission", "images");

const DPI = 300;
const COL_MM = 110;                       // 版心宽（毫米）
const BASE_PX = Math.round((COL_MM / 25.4) * DPI);

const chrome =
  process.env.CHROME_PATH ||
  (process.platform === "win32"
    ? "C:/Program Files/Google/Chrome/Application/chrome.exe"
    : "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome");

const viewBoxOf = (svg) => {
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  return m ? [parseFloat(m[1]), parseFloat(m[2])] : [1000, 560];
};

await mkdir(outDir, { recursive: true });
const files = (await readdir(figDir)).filter((f) => f.endsWith(".svg")).sort();

const browser = await puppeteer.launch({ executablePath: chrome, headless: true });
const page = await browser.newPage();
await page.setViewport({ width: BASE_PX, height: 400, deviceScaleFactor: 1 });

const rows = [];
for (const f of files) {
  const svg = await readFile(path.join(figDir, f), "utf8");
  const [vw, vh] = viewBoxOf(svg);
  const w = BASE_PX;
  const h = Math.round((vh / vw) * w);
  const mmW = COL_MM;
  const mmH = +((vh / vw) * COL_MM).toFixed(1);
  await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
  const html = `<!doctype html><meta charset="utf-8">
<style>@font-face{font-family:'Noto Sans SC';src:local('Noto Sans SC')}
html,body{margin:0;padding:0;background:#fff}svg{display:block;width:${w}px;height:${h}px}</style>${svg}`;
  await page.setContent(html, { waitUntil: "load" });
  const png = await page.screenshot({ type: "png", clip: { x: 0, y: 0, width: w, height: h } });
  const base = f.replace(/\.svg$/, "");
  await writeFile(path.join(outDir, base + ".png"), png);
  rows.push({ file: base, svg: f, px: `${w}x${h}`, mm: `${mmW}x${mmH}`, dpi: DPI, kb: Math.round(png.length / 1024) });
  console.log(`  ${base}.png  ${w}x${h}px  印成 ${mmW}x${mmH} mm  ${Math.round(png.length / 1024)} KB`);
}
await browser.close();

// PNG → TIF（无压缩 RGB）。PIL 可用，直接转。
const { execFileSync } = await import("node:child_process");
try {
  execFileSync("python", [path.join(here, "png2tif.py"), outDir], { stdio: "inherit" });
} catch {
  console.log("  （TIF 转换跳过：PIL 不可用时只交 PNG 也可，多数印厂接受）");
}

const table =
  "文件\tSVG 源\t像素\t印刷尺寸(mm)\tDPI\tPNG 体积\n" +
  rows.map((r) => `${r.file}\t${r.svg}\t${r.px}\t${r.mm}\t${r.dpi}\t${r.kb} KB`).join("\n") + "\n";
await writeFile(path.join(root, "submission", "images", "_尺寸表.tsv"), table, "utf8");
console.log(`\n共 ${rows.length} 幅 → submission/images/（300 dpi，按版心 110 mm 定宽）`);
