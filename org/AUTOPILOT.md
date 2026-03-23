# 自动推进与止损（枢衡堂）

## 全局开关

- `control.json`：`halt=true` 时 **禁止** 任何阶段推进、禁止为刷流转而改 `phase`。
- **一键停止**：`~/.openclaw/org/scripts/stop.sh [原因]`
- **恢复**：`~/.openclaw/org/scripts/resume.sh`

## 推进前检查（各 agent）

1. 读 `control.json`；若 `halt=true`，只汇报状态，不推进。
2. 读 `GUARD-ALERT.md`；若有告警，先处理或上报枢衡/主人。
3. 改任务 `phase` 时：`phase_transitions += 1`，更新 `last_activity_iso`（UTC ISO8601）；不得超过 `control.json` 的 `max_phase_transitions`（默认 24），否则标记 `blocked` 并停手。

## 空转 / 卡死

- **空转**：同一任务 `phase` 反复横跳或无新产出 → 用 `phase_transitions` 计数；守卫会告警。
- **卡死**：`last_activity_iso` 超过 `stale_task_hours`（默认 48h）未更新 → 守卫告警。

## Token

- 在 `metrics.json` 更新 `rolling_24h_tokens`（手工或后续接网关统计）。
- 超过 `token_soft_limit_24h` → `GUARD-ALERT.md` 提示。
- 超过 `token_hard_stop_24h`：若 `auto_halt_on_hard_token=true` 则 **自动 halt**（默认 false，仅告警）。

## 守卫

- 执行：`~/.openclaw/org/scripts/run-guard.sh`（或 `python3 .../guard.py`）
- 输出：`GUARD-ALERT.md`

## 备份

- `~/.openclaw/org/scripts/backup.sh` → 打包到 `org/backups/*.tar.gz`（不含 `backups` 目录自身）。

## 飞书少气泡

私聊下工具过程摘要 + 多轮工具间的 assistant 文本容易多条气泡。已用 `renderMode: "raw"`、`textChunkLimit` 减轻分段；根治仍靠 `SOUL` 与模型遵守「工具前后不闲聊」。

## 性能软告警 + 飞书推送

- `perf.json` 调阈值与冷却；`python3 ~/.openclaw/org/scripts/perf_watch.py` 写 `PERF-WARN.md`。
- 推送：复制 `local.env.example` → `local.env`，填 `FEISHU_NOTIFY_OPEN_ID`；执行  
  `set -a; source ~/.openclaw/org/local.env; set +a; python3 ~/.openclaw/org/scripts/perf_watch.py --push`  
  仅在 **SOFT_ALERT** 且过冷却时发一条飞书私聊（读 **本机** `openclaw.json` 里 default 机器人凭证，不入库）。
- 主人收到后：**停止** / **`/stop`** → 枢衡执行 `stop.sh`（见枢衡 `SOUL.md`）。

## 定时（可选）

网关运行时可加 cron，让枢衡周期性读守卫结果（Gateway 停止时不要改 `cron/jobs.json`）：

```bash
openclaw cron add \
  --name "枢衡堂-守卫" \
  --cron "*/15 * * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --system-event "执行: python3 ~/.openclaw/org/scripts/guard.py ；再阅读 ~/.openclaw/org/GUARD-ALERT.md 与 ~/.openclaw/org/control.json 。若 halt 或存在告警，用简短中文提醒 Graves，不要自动推进任务。" \
  --wake now
```

（按你环境调整路径与 `openclaw cron` 参数；不确定时用 `openclaw cron add --help`。）
