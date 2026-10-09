import io, re, sys
import fitz

PDF = "print/人形机器人：从一颗关节往下挖.pdf"
d = fitz.open(PDF)
pages = d.page_count
print("pages:", pages, " size:", round(len(io.open(PDF, 'rb').read()) / 1e6, 2), "MB")

# whole-document text, normalized for the PDF's own line-breaking
raw = "".join(p.get_text() for p in d)
norm = re.sub(r"[\s\-–—/…]", "", raw)

def has(s):
    return re.sub(r"[\s\-–—/…]", "", s) in norm

NEW = [
 "2.6 J", "2.64 J", "0.005 J 是假的", "343 N·m", "15.3 N·m", "2.7 N·m", "5.7 倍",
 "177°", "0.32 s", "1.1 kW", "18–21 倍", "1.6 ms",
 "RTX 4090", "TABLE I", "only recomputing the suffix", "~300M",
 "every 0.5 seconds", "14.6 %", "65.5 ms", "2.4 倍", "11.9 ms", "6.1 倍",
 "32 GB/s", "320 GB/s", "simple transformer-based visuomotor policy",
 "asynchronous background process", "shared memory latent vector",
 "0.000049 s", "0.049 ms", "折算不变量", "3.2 ms", "0.24 ms",
 "9.8 mA", "0.20 %", "0.50 %", "稻草人", "1P18S", "0.2–0.35 V",
 "1,459 K", "507 K", "φ75 × 20", "60 K", "115 K", "仍超 22%",
 "1 ÷ 0.60 = 1.67", "5.96", "16.8%", "4.36", "16.3", "6.2%",
 "51 个刻度", "348 个刻度", "0.63895", "0.77 N·m", "64%", "155 倍",
 "P_迭代", "K × (2P_迭代",
]
GONE = [
 "0.005 J 是假的之外的一切旧写法：抱闸能当场吸收的只有那 0.005 J",
 "6.7 万倍", "绝不可能塞进十步迭代", "用掉 98 %", "三数闭合",
 "τ_m ≈ 4.9 ms", "3τ_m = 14.7 ms", "粗 4 倍", "×2.50", "便宜了 1.5 倍",
 "每拍预算 = 节拍 ÷ K", "0.1 V 跨 60% SOC", "12 bit ÷ ±20 A ⇒ LSB 4.9 mA",
 "上面那颗膝要散 55 W", "324 W（第 26 章", "10 A 是本章上面那个平均母线电流",
]
print("--- new needles ---")
miss = [s for s in NEW if not has(s)]
print("present %d/%d" % (len(NEW) - len(miss), len(NEW)))
for s in miss:
    print("  MISSING:", s)
print("--- retired needles (must be absent) ---")
bad = []
for s in GONE:
    key = s.split("：")[-1] if "之外的一切旧写法" in s else s
    if has(key):
        bad.append(key)
print("clean %d/%d" % (len(GONE) - len(bad), len(GONE)))
for s in bad:
    print("  STILL PRESENT:", s)

# geometry on the finished PDF
bleed_ok = overset = empty = 0
W, H = 145 / 25.4, 210 / 25.4  # pt
for p in d:
    r = p.rect
    if abs(r.width - W * 72 / 72 * 25.4 / 25.4 - 0) and False:
        pass
    mm = (r.width / 72 * 25.4, r.height / 72 * 25.4)
    if abs(mm[0] - 145) > 0.6 or abs(mm[1] - 210) > 0.6:
        overset += 1
    txt = p.get_text().strip()
    imgs = len(p.get_images())
    if len(txt) < 12 and imgs == 0:
        empty += 1
    for b in p.get_text("blocks"):
        x0, y0, x1, y1 = b[:4]
        mx, my = x0 / 72 * 25.4, y0 / 72 * 25.4
        if mx < -0.2 or my < -0.2 or x1 / 72 * 25.4 > 145.2 or y1 / 72 * 25.4 > 210.2:
            bleed_ok += 1
print("geometry: size-mismatch %d, off-page text blocks %d, near-empty pages %d" % (overset, bleed_ok, empty))
print("images embedded:", len(raw) and sum(len(p.get_images()) for p in d))
