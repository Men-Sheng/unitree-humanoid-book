#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""print/png2tif.py — 把 submission/images 里的 PNG 转成无压缩 RGB TIF（印厂口径）。

用法：python print/png2tif.py <目录>
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("PIL 不可用，跳过 TIF")
    raise SystemExit(0)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = Path(sys.argv[1])
n = 0
for p in sorted(d.glob("*.png")):
    im = Image.open(p).convert("RGB")
    out = p.with_suffix(".tif")
    im.save(out, format="TIFF", compression="none", dpi=(300, 300))
    n += 1
print(f"  {n} 个 TIF（无压缩 RGB，300 dpi）")
