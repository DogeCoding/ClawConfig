#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ORG = Path.home() / ".openclaw" / "org"
PERF_JSON = ORG / "perf.json"
PERF_WARN = ORG / "PERF-WARN.md"
LAST = ORG / ".perf_last_notify"


def main() -> int:
    push = "--push" in sys.argv
    perf = {}
    if PERF_JSON.exists():
        perf = json.loads(PERF_JSON.read_text(encoding="utf-8"))
    cpus = os.cpu_count() or 4
    mult = float(perf.get("load1_soft_multiplier") or 0.85)
    threshold = max(1.0, cpus * mult)
    load1, load5, load15 = os.getloadavg()
    alert = load1 > threshold
    lines = [
        "# 性能软告警",
        "",
        f"- load1={load1:.2f} load5={load5:.2f} load15={load15:.2f}",
        f"- cpus={cpus} 软阈值≈{threshold:.2f} (cpus×{mult})",
        f"- 状态: **{'SOFT_ALERT' if alert else 'ok'}**",
        "",
        "主人可回复 **停止** 或发送 `/stop`，并会 `stop.sh` 暂停自动推进。",
    ]
    PERF_WARN.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not push or not alert:
        print("PERF_WARN written", "SOFT_ALERT" if alert else "ok")
        return 0
    cool = int(perf.get("notify_cooldown_seconds") or 3600)
    now = int(time.time())
    if LAST.exists():
        last = int(LAST.read_text(encoding="utf-8").strip() or "0")
        if now - last < cool:
            print("skip push: cooldown")
            return 0
    open_id = os.environ.get("FEISHU_NOTIFY_OPEN_ID", "").strip()
    if not open_id:
        print("skip push: set FEISHU_NOTIFY_OPEN_ID or source org/local.env", file=sys.stderr)
        return 0
    msg = f"枢衡堂·性能软告警 load1={load1:.2f}（阈值≈{threshold:.1f}）。回复「停止」或 /stop 可停。"
    import subprocess

    script = ORG / "scripts" / "feishu_notify_open.py"
    r = subprocess.run([sys.executable, str(script), open_id, msg], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return 1
    LAST.write_text(str(now), encoding="utf-8")
    print("pushed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
