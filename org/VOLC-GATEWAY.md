# 让 OpenClaw 网关进程读到 VOLC_ACCESSKEY / VOLC_SECRETKEY

LaunchAgent **不会**读取你在终端里 `export` 的变量。已用包装脚本从 **`~/.openclaw/org/volc-api.env`** 注入（该文件已在 `.gitignore`）。

## 一次性配置

1. 复制模板并编辑（填入火山 AK/SK，**不要**提交 Git）：

   ```bash
   cp ~/.openclaw/org/volc-api.env.example ~/.openclaw/org/volc-api.env
   chmod 600 ~/.openclaw/org/volc-api.env
   # 用编辑器填入 VOLC_ACCESSKEY= 与 VOLC_SECRETKEY=
   ```

2. 确认 **`~/Library/LaunchAgents/ai.openclaw.gateway.plist`** 的 `ProgramArguments` 为：

   - `/bin/bash`
   - `/Users/graves/.openclaw/org/scripts/gateway-volc-env.sh`

   （若你重新跑过 `openclaw configure` 被改回纯 `node`，需按上项改回或重新执行本仓库里的 plist 片段。）

3. 加载并重启网关：

   ```bash
   launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
   launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist
   ```

   或使用：`openclaw gateway restart`（若其实现会覆盖 plist，请先备份再改）。

## 自检

```bash
bash ~/.openclaw/org/scripts/check_jimeng_prereqs.sh
```

说明：在 **macOS** 上，LaunchAgent 拉起的网关进程往往 **`ps eww` 不显示环境变量**，脚本第 4 步会 **SKIP** 而不是误报 WARN；以第 5 步（`volc-api.env` 能否被 source 且两项非空）及实际调用 API 是否仍报缺密钥为准。
