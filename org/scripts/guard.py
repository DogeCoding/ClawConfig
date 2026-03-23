#!/usr/bin/env python3
"""Read control + tasks + metrics; write GUARD-ALERT.md; optional auto-halt on token hard."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ORG = Path.home() / ".openclaw/org"
FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONT.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    data: dict = {}
    for line in raw.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip().strip('"')
        if k in ("phase_transitions", "tokens_logged", "phase"):
            try:
                data[k] = int(v) if k != "phase" else int(v)
            except ValueError:
                data[k] = v
        elif k in ("halt", "spin_guard"):
            data[k] = v.lower() in ("true", "yes", "1")
        else:
            data[k] = v
    return data, text


def iso_age_hours(iso: str | None) -> float | None:
    if not iso or iso in ('""', "null", ""):
        return None
    try:
        s = iso.replace("Z", "+00:00")
        t = datetime.fromisoformat(s)
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() / 3600.0
    except Exception:
        return None


def main() -> int:
    ctl_path = ORG / "control.json"
    met_path = ORG / "metrics.json"
    alert_path = ORG / "GUARD-ALERT.md"
    lines: list[str] = []

    if not ctl_path.exists():
        print("missing control.json", file=sys.stderr)
        return 1

    ctl = json.loads(ctl_path.read_text(encoding="utf-8"))
    if ctl.get("halt"):
        lines.append("# 守卫\n\n**全局 halt=true**，自动推进应停止。\n")
        alert_path.write_text("\n".join(lines), encoding="utf-8")
        return 0

    metrics = {}
    if met_path.exists():
        metrics = json.loads(met_path.read_text(encoding="utf-8"))
    rolling = int(metrics.get("rolling_24h_tokens") or 0)
    soft = int(ctl.get("token_soft_limit_24h") or 0)
    hard = int(ctl.get("token_hard_stop_24h") or 0)
    auto_halt = bool(ctl.get("auto_halt_on_hard_token"))

    if soft and rolling >= soft:
        lines.append(f"- Token 告警：近窗约 **{rolling}** ≥ 软上限 **{soft}**（请人工确认或执行 stop.sh）。")
    if hard and rolling >= hard:
        lines.append(f"- Token 严重：近窗约 **{rolling}** ≥ 硬上限 **{hard}**。")
        if auto_halt:
            ctl["halt"] = True
            ctl["halt_set_at"] = datetime.now(timezone.utc).isoformat()
            ctl["halt_note"] = "auto_halt_on_hard_token"
            ctl_path.write_text(json.dumps(ctl, ensure_ascii=False, indent=2), encoding="utf-8")
            lines.append("- **已自动 halt**（auto_halt_on_hard_token）。")

    stale_h = float(ctl.get("stale_task_hours") or 48)
    max_tr = int(ctl.get("max_phase_transitions") or 24)
    tasks_dir = ORG / "tasks"
    if tasks_dir.is_dir():
        for p in sorted(tasks_dir.glob("TASK-*.md")):
            body = p.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(body)
            if fm.get("halt"):
                continue
            status = str(fm.get("status", "draft"))
            if status in ("done", "failed", "cancelled"):
                continue
            trans = int(fm.get("phase_transitions") or 0)
            if trans >= max_tr:
                lines.append(f"- 空转风险：**{p.name}** `phase_transitions={trans}` ≥ {max_tr}，应暂停并复盘，禁止无意义改 phase。")
            last = fm.get("last_activity_iso")
            age = iso_age_hours(str(last) if last else None)
            if age is not None and age > stale_h:
                lines.append(f"- 卡死风险：**{p.name}** 已 **{age:.1f}h** 无 `last_activity_iso` 更新（阈值 {stale_h}h）。")

    if not lines:
        alert_path.write_text("# 守卫\n\n（本轮无告警）\n", encoding="utf-8")
        return 0

    out = "# 守卫告警\n\n" + "\n".join(lines) + "\n"
    alert_path.write_text(out, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
