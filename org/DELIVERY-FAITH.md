# 交付诚信（飞书 / 图片 / 链接）

各岗在对外回复（尤其飞书）时遵守；细节亦见 `workspace/SOUL.md`、`TOOLS.md`、`MEMORY.md`。

## 1. 图片与文件

- **禁止**在正文里写 `MEDIA:./xxx`、`./scene1.jpg` 等**未经验证**的路径，假装已生成图。
- 图、表、导出物必须先**真实写入**约定目录：  
  **`/Users/graves/Workspace/agent-outputs/images/`**（本机）或 **`/projects/agent-outputs/images/`**（沙箱），命名 `{描述}-{YYYYMMDD}.{ext}`。
- 写入后可用 `read` **确认文件存在**，再在回复里写**绝对路径**或说明已落盘位置。
- **飞书发图**：须通过飞书消息能力上传/发图（如 `feishu-messaging` 技能或渠道附件）；**仅一行文字不会变成图片**。

## 2. 链接与授权 URL

- **禁止**编造可点击链接；**禁止**使用 `https://.../xxxxxx`、`.../todo`、`.../placeholder` 等占位符冒充真实地址。
- 没有真实 URL 时：明确写「需主人在剪映/浏览器内自行完成授权」或分步操作说明，**不要**伪造域名+假 path。

## 3. 仪表盘 vs 飞书

- **Control UI 聊天**与**飞书投递**是两条链路；可能出现「仪表盘里看到回复、飞书未收到」（例如渠道发送失败、会话未绑定该群）。
- 若主人反馈飞书未收到：查 `openclaw logs`、`~/.openclaw/logs/gateway.log` 中 `feishu` / `error` / `429`；确认 `openclaw.json` 里 **`groupAllowFrom`** 与 **`groups.<chat_id>`** 已包含该群（见 `FEISHU-GROUPS.md`）。

## 4. 定时任务（cron）与进度

- **`payload.message` 会被当作用户消息**：若里面写了虚假进度，模型会照抄进飞书，表现为「定时在撒谎」。
- **正确写法**：只描述核对步骤（路径、`ls`/`find`、空目录如何表述）；**错误写法**：在 message 里写「已交付」「已上传」。
- **`delivery`**：`sessionTarget` 为 `isolated` 且带飞书 `announce` 时须设 **`delivery.channel: feishu`**（及 `to` 为群 `oc_...`），否则可能报 `Channel is required`、任务失败、群里收不到简报。
