---
id: TASK-20260323-morning-news-push
status: active
phase: 1
owner: main
assignees: []
phase_transitions: 0
last_activity_iso: "2026-03-23T03:28:00+08:00"
tokens_logged: 0
halt: false
spin_guard: true
---

# 每日早间新闻推送系统

## 上下文

主人 Graves 需求：
1. ~~创建一个只有枢衡和 Graves 的飞书群~~（已完成：用户手动创建）
2. 每天早上 8:30 推送新闻，包含：
   - 最近一天的新闻
   - 加密货币的投资意见和最新动态
   - AI 圈的最新动态
   - OpenClaw 的最新动态
   - GitHub 最火的五个项目和介绍

## 当前进展

- 已安装 `feishu-messaging` 技能（来自 ClawHub）
- 飞书群已由用户手动创建
- 已找到 News 群，群 ID：`oc_93086ae445f1b1f08c955acb931800b7`（正是当前群聊）
- 已创建飞书消息发送脚本并测试成功
- 已创建早间新闻推送主脚本（包含所有模块：新闻、加密货币、AI 动态、OpenClaw 动态、GitHub 热榜）

## 已创建的脚本

- `search-feishu-chat.py` - 搜索飞书群
- `send-feishu-message.py` - 发送飞书消息
- `morning-news-push.py` - 早间新闻推送主脚本

## 阶段推进记录

（每次改 `phase` 须：`phase_transitions += 1`，更新 `last_activity_iso`；先读 `../control.json`，`halt=true` 则禁止推进。）

### 阶段 1 — 拆解（进行中）
- 2026-03-23: 任务创建，等待计府拆解
- 2026-03-23: 安装 feishu-messaging 技能，飞书群已手动创建

## 验收标准

- [x] 飞书群创建成功，仅包含枢衡和 Graves
- [ ] 每日 8:30 准时推送
- [ ] 推送内容包含所有要求的模块
- [ ] 推送格式清晰易读
