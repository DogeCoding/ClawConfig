# 本机托管浏览器（agent 自动化）

- 配置在 **`~/.openclaw/openclaw.json`** 顶层 **`browser`**：`defaultProfile: "openclaw"`、`headless: false`、Chrome 可执行路径、`profiles.openclaw.cdpPort: 18800`。
- **`agents.defaults.sandbox.browser`**：`enabled: false`（不用 Docker 内无头浏览器）、**`allowHostControl: true`**（沙箱会话里浏览器工具走本机）。
- 网关重启后若需立即拉起窗口：`openclaw browser --browser-profile openclaw start`（也可由 agent 调 `browser` 工具的 `start`）。
