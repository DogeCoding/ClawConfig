# 飞书与网关安全（枢衡堂）

## 当前策略（见 `openclaw.json` → `channels.feishu`）

- **私聊**：`dmPolicy: allowlist`，仅 `allowFrom` 中的 **open_id**（主人 Graves）可与任意已绑定机器人私聊。
- **群聊**：`groupPolicy: allowlist` 且 `groupAllowFrom: []` — **暂不处理任何群消息**。若要在群内用机器人，必须显式写入群 `oc_xxx`，并在 `channels.feishu.groups.oc_xxx.allowFrom` 中仅列主人 open_id（或可信小号）。
- **网关**：`bind: loopback`，远程调用需自备隧道并保管 `gateway.auth.token`。

## 轮换与核对

- 修改 `allowFrom` 后 **重启网关**。
- `org/local.env` 中 `FEISHU_NOTIFY_OPEN_ID` 应与 `allowFrom` 为 **同一应用下** 的主人 open_id。
- 勿将 `openclaw.json`、`local.env` 提交 Git。

## 模型与工具

- 子 agent 已按职配不同 `model.primary`；**财务/交易/删库/对外付款** 类指令：无主人明确书面确认前 **拒绝执行**，并写入任务单待批。
