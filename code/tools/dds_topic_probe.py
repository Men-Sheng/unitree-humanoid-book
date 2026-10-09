#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dds_topic_probe.py — 一次跑完，测出"哪些话题在发、多少 Hz、字段长什么样"。

这是《宇树机器人开发者工作流全栈》附录 A1（话题全表）与 A2（兼容矩阵）的**数据采集器**。
话题清单不写死在代码里，读 `topic_registry.yaml`；加话题只加一行。

用法（在有 unitree_sdk2_python 的 Ubuntu/WSL2 环境里）：

    # 1) 装好 SDK 后，先设 DDS 环境变量（官方要求，否则收不到任何东西）
    export CYCLONEDDS_HOME=~/cyclonedds/install/etc/cyclonedds.xml

    # 2) 探测 20 秒，输出 JSON + Markdown
    python dds_topic_probe.py --seconds 20 --out probe-go2

    # 3) 只测某几个话题 / 指定网卡
    python dds_topic_probe.py --only rt/lowstate --nic eth0

    # 4) 离线自测（不需要机器人，用假模块验证脚本本身）
    python dds_topic_probe.py --stub --seconds 2

输出：
    probe-go2.json       机器可读，附录 A1 的真源
    probe-go2.md         直接能贴进书里的表格

诚实性规则（写进脚本，不靠自觉）：
  * 没收到数据的话题一律标 NO_DATA，不猜频率。
  * 频率是**测出来的**（收包数/时长），不是抄文档的；两者不一致时以实测为准并在书里注明版本。
  * `src: doc` 的条目本来就是待证假设，输出里保留这一列，防止把假设当事实。
"""
from __future__ import annotations

import argparse
import importlib
import json
import platform
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_registry(path: Path) -> list[dict]:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = data["topics"] if isinstance(data, dict) else data
    out = []
    for r in rows:
        if not r.get("topic"):
            continue
        out.append(
            {
                "topic": r["topic"],
                "module": r.get("module", ""),
                "cls": r.get("cls", ""),
                "dir": r.get("dir", "machine->you"),
                "src": r.get("src", "doc"),
                "note": r.get("note", ""),
            }
        )
    return out


def resolve_type(module: str, cls: str):
    """把 IDL 类名解析成 Python 类。unitree_go/unitree_hg 在 dds_ 子包，
    sensor_msgs/nav_msgs/std_msgs 不在，两种布局都试。"""
    candidates = [f"{module}.dds_", module]
    last_err = None
    for mod in candidates:
        try:
            m = importlib.import_module(mod)
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue
        if hasattr(m, cls):
            return getattr(m, cls)
        last_err = AttributeError(f"{mod} has no {cls}")
    raise ImportError(f"cannot resolve {module}.{cls}: {last_err}")


class Probe:
    def __init__(self, seconds: float, nic: str | None, domain: int, stub: bool):
        self.seconds = seconds
        self.counts: dict[str, int] = defaultdict(int)
        self.first: dict[str, dict] = {}
        self.errors: dict[str, str] = {}
        self.subs = []
        self.stub = stub
        if stub:
            self.factory_init = lambda: None
            self.make_sub = self._make_stub_sub
        else:
            from unitree_sdk2py.core.channel import (  # noqa: PLC0415
                ChannelFactoryInitialize,
                ChannelSubscriber,
            )

            self._Subscriber = ChannelSubscriber
            self.factory_init = lambda: ChannelFactoryInitialize(domain, nic)
            self.make_sub = self._make_real_sub

    def _make_real_sub(self, topic: str, typ, handler):
        sub = self._Subscriber(topic, typ)
        sub.Init(handler, 50)  # 队列 50：高频话题宁可丢包也不要阻塞回调线程
        self.subs.append(sub)

    def _make_stub_sub(self, topic: str, typ, handler):
        """离线自测：每 20ms 造一条假消息，验证计数/字段提取/表格生成都对。"""

        class _Fake:
            def __init__(self):
                self.position = [1.0, 2.0, 3.0]
                self.velocity = [0.0, 0.0, 0.5]
                self.mode = 3
                self.timestamp = 0

        self.counts[f"_stub_seed:{topic}"] = 0

        def tick():
            handler(_Fake())

        self.subs.append(_Ticker(tick))

    def handler_for(self, topic: str):
        def h(msg):
            self.counts[topic] += 1
            if topic not in self.first:
                self.first[topic] = summarize(msg)

        return h

    def run(self, rows: list[dict]) -> dict:
        self.factory_init()
        for r in rows:
            topic = r["topic"]
            try:
                typ = resolve_type(r["module"], r["cls"]) if not self.stub else dict
            except Exception as e:  # noqa: BLE001
                self.errors[topic] = f"type unresolved: {e}"
                continue
            try:
                self.make_sub(topic, typ, self.handler_for(topic))
            except Exception as e:  # noqa: BLE001
                self.errors[topic] = f"subscribe failed: {e}"

        t0 = time.monotonic()
        try:
            while time.monotonic() - t0 < self.seconds:
                for s in self.subs:
                    if hasattr(s, "pump"):
                        s.pump()
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("interrupted", file=sys.stderr)
        elapsed = time.monotonic() - t0

        for s in self.subs:
            if hasattr(s, "close"):
                try:
                    s.close()
                except Exception:  # noqa: BLE001
                    pass

        results = []
        for r in rows:
            n = self.counts.get(r["topic"], 0)
            results.append(
                {
                    **r,
                    "messages": n,
                    "hz_measured": round(n / elapsed, 2) if n else None,
                    "fields": self.first.get(r["topic"], {}),
                    "error": self.errors.get(r["topic"]),
                    "verdict": "ALIVE" if n else ("ERROR" if r["topic"] in self.errors else "NO_DATA"),
                }
            )
        return {
            "schema": "unitree-book/topic-probe@1",
            "collected_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": round(elapsed, 2),
            "host": {
                "platform": platform.platform(),
                "python": sys.version.split()[0],
                "stub": self.stub,
            },
            "results": results,
        }


class _Ticker:
    """stub 模式用的最小驱动：pump() 造一条假消息。"""

    def __init__(self, fn):
        self._fn = fn
        self._next = 0.0

    def pump(self):
        now = time.monotonic()
        if now >= self._next:
            self._next = now + 0.02
            self._fn()


def summarize(msg) -> dict:
    """提取顶层字段名 + 样例值（截断），用于写 Reference 层的字段表。"""
    out: dict[str, str] = {}
    for k in dir(msg):
        if k.startswith("_"):
            continue
        try:
            v = getattr(msg, k)
        except Exception:  # noqa: BLE001
            continue
        if callable(v):
            continue
        s = repr(v)
        out[k] = s if len(s) <= 60 else s[:57] + "..."
    return out


def to_markdown(rep: dict) -> str:
    lines = [
        f"# 话题探测结果（{rep['collected_utc']}，跑 {rep['elapsed_seconds']} 秒"
        + ("，**stub 自测，非真机数据**" if rep["host"]["stub"] else "")
        + "）",
        "",
        "| 话题 | 方向 | 结论 | 收包 | 实测 Hz | 来源 | 备注 |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rep["results"]:
        lines.append(
            "| `{}` | {} | {} | {} | {} | {} | {} |".format(
                r["topic"],
                r["dir"],
                r["verdict"],
                r["messages"],
                r["hz_measured"] if r["hz_measured"] is not None else "—",
                r["src"],
                (r["note"] or "") + ((" | " + r["error"]) if r["error"] else ""),
            )
        )
    alive = [r for r in rep["results"] if r["verdict"] == "ALIVE"]
    lines += ["", f"存活 {len(alive)} / {len(rep['results'])}。", ""]
    for r in alive[:3]:
        lines += [f"### {r['topic']} 顶层字段", "", "```"]
        lines += [f"{k} = {v}" for k, v in sorted(r["fields"].items())[:40]]
        lines += ["```", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="DDS topic probe for the Unitree book")
    ap.add_argument("--registry", default=str(HERE / "topic_registry.yaml"))
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--nic", default=None, help="网卡名，如 eth0；不给则用 SDK 自动选择")
    ap.add_argument("--domain", type=int, default=0)
    ap.add_argument("--only", nargs="*", default=None, help="只测这些话题")
    ap.add_argument("--out", default="probe", help="输出前缀，生成 <out>.json / <out>.md")
    ap.add_argument("--stub", action="store_true", help="离线自测：不 import SDK，造假消息")
    a = ap.parse_args()

    rows = load_registry(Path(a.registry))
    if a.only:
        rows = [r for r in rows if r["topic"] in set(a.only)]
    if not rows:
        print("registry 里没有匹配的话题", file=sys.stderr)
        return 2

    probe = Probe(a.seconds, a.nic, a.domain, a.stub)
    rep = probe.run(rows)

    Path(f"{a.out}.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path(f"{a.out}.md").write_text(to_markdown(rep), encoding="utf-8")

    for r in rep["results"]:
        print(
            "{:9} {:28} {:>6} 包  {:>7} Hz  {}".format(
                r["verdict"], r["topic"], r["messages"],
                r["hz_measured"] if r["hz_measured"] is not None else "—",
                r["error"] or "",
            )
        )
    print(f"\nwrote {a.out}.json / {a.out}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
