# Docker 与 OpenClaw 架构（枢衡堂）

## 推荐拓扑（性能 + 安全）

| 组件 | 建议 | 说明 |
|------|------|------|
| **OpenClaw 网关**（Node、飞书 WS、会话路由） | **本机进程** | 少一层虚拟化；文件路径、`~/.openclaw`、本机插件与飞书长连接都简单；打满 CPU 时主要调 **并发会话数、模型、定时任务**，而非把网关塞进容器。 |
| **工具执行沙箱** | **Docker**（`agents.defaults.sandbox.mode: "all"`） | 仅 `exec` 等高危/任意命令进容器；**CPU/内存在 `sandbox.docker` 里封顶**，与宿主机隔离，防误删与越权。 |
| **整条网关跑在 Docker 里** | **一般不推荐**（自用单机） | 要挂卷、网络、Feishu、宿主机 PATH；排障成本高；Mac 上 Docker 本身还有 VM 开销。 |

## 资源上限（避免拖垮整机）

1. **Docker Desktop** → Settings → Resources：**CPU / Memory** 设上限（例如总内存的 40～50%）。  
2. **`openclaw.json`** → `agents.defaults.sandbox.docker`：`cpus`、`memory` 已可限制单容器；多任务并发高时再略收紧。  
3. **飞书**：少群、少机器人同醒；**perf_watch** 看 load1。  
4. 网关仍在本机：若 Node 飙高，用活动监视器查 `node`，再减并发/cron。

## 安装 Docker（macOS）

```bash
export HOMEBREW_NO_AUTO_UPDATE=1
brew install --cask docker
```

打开 **Docker**（`/Applications/Docker.app`），完成首次引导，菜单栏鲸鱼为 **Running**。终端执行：

```bash
docker version
```

## 启用 OpenClaw 沙箱（Docker 就绪后）

默认镜像名 `openclaw-sandbox:bookworm-slim` 由 OpenClaw 用 **`debian:bookworm-slim` 拉取后 `docker tag`** 得到（网关首次用沙箱时也会自动做）。可手动预热：

```bash
docker pull debian:bookworm-slim
docker tag debian:bookworm-slim openclaw-sandbox:bookworm-slim
```

将 `openclaw.json` 中 `agents.defaults.sandbox.mode` 设为 **`"all"`**，然后 `openclaw gateway restart`。自检：`openclaw sandbox explain`。

## 安全摘要

- **沙箱 on**：工具默认不直接写宿主机（按 `workspaceAccess` 与挂载策略）。  
- **飞书**：仍以 `SECURITY.md` 白名单为准；Docker 不替代渠道鉴权。  
- **资金/不可逆**：仍以主人确认为准，与是否 Docker 无关。
