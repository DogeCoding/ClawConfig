# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 本机托管浏览器（OpenClaw）

- 已配置 **`browser.defaultProfile: "openclaw"`** + **Google Chrome** 可执行路径；**有界面**（`headless: false`），专供 agent 自动化，与个人 Chrome 配置隔离。
- **沙箱内**已关闭 Docker 无头浏览器，浏览器工具**默认走本机 `host`**（`allowHostControl: true`），与枢衡无沙箱行为一致。
- 调用 `browser` 工具时可省略 `profile`（默认 `openclaw`）；若在沙箱会话中需显式自动化本机浏览器，使用 **`target: "host"`**。

## Docker 沙箱与 `~/Workspace`

- 工具在容器里跑时，**不要用 `~/Workspace`**；用 **`/projects/...`** 或 **`/host-workspace/...`**（与主机 `~/Workspace` 同内容）。
- **路径硬规则**：`read`/`edit`/`write` 等工具**禁用 `~`**（易导致 Edit failed）；一律用绝对路径：本机 **`/Users/graves/Workspace/...`**，沙箱 **`/projects/...`**。
- 例：`cookies.txt` → **`/projects/douyin-video-analyzer/cookies.txt`**；编辑项目代码 → **`/Users/graves/Workspace/douyin-video-analyzer/douyin_analyzer_v2.py`**。
- 改 `openclaw.json` 的 `sandbox.docker` 后：先 **`openclaw sandbox recreate --all --force`**，再测；与「第几条飞书消息」无关。
- 详见 `SOUL.md`「沙箱（硬规则）」与 `MEMORY.md`。

## OpenClaw 全量备份（本机）

- **脚本**：`/Users/graves/Data/OpenclawBackup/backup-openclaw.sh`
- **归档目录**：`/Users/graves/Data/OpenclawBackup/archives/openclaw-*.tar.gz`（保留个数由 **`OPENCLAW_BACKUP_KEEP`** 控制，默认 5）
- **覆盖根目录**：环境变量 **`OPENCLAW_BACKUP_ROOT`**（不设则用 `~/Data/OpenclawBackup`）
- **兼容**：`~/OpenclawBackup` → `~/Data/OpenclawBackup` 的符号链接，旧路径仍可打开

## 多岗 Skills 同步（last30days 等）

- ClawHub 默认装进 **`~/.openclaw/workspace/skills`**；**`workspace-juyi` 等子岗不会自动出现新包**，需手动对齐。
- 一键把主 workspace 的 `skills/` 推到所有 **`workspace-*/skills/`**：  
  `bash /Users/graves/.openclaw/org/scripts/sync-skills-to-agent-workspaces.sh`  
  （装完新技能或新开 agent 目录后跑一遍即可。）
- **`last30days-official`** 密钥：只维护一份 **`~/.config/last30days/.env`**（`chmod 600`）；已做 **`~/.openclaw/.env` → 该文件的符号链接**，便于网关按 [OpenClaw 文档](https://docs.openclaw.ai/gateway/configuration-reference#environment) 加载 `KEY=VAL`（与技能内 `get_config()` 读同一文件）。模板：`/Users/graves/.openclaw/org/last30days.env.example`。根配置已开 **`env.shellEnv`**：登录 shell 里 `export` 的变量可在未写进 `.env` 时补进网关（仅缺省键）。诊断：  
  `cd /Users/graves/.openclaw/workspace/skills/last30days-official && python3 scripts/last30days.py --diagnose`

## Agent 输出物路径

- **统一根目录**：`~/Workspace/agent-outputs/`（沙箱内 **`/projects/agent-outputs/`**）。
- **子目录**：`images/`、`documents/`、`exports/`、`scratch/`。
- **命名**：`{描述}-{YYYYMMDD}.{ext}`，禁止散落在 workspace 根。
- **禁止**正文写 `MEDIA:./xxx` 等假路径；**禁止**编造带 `xxxxxx` 的 URL。见 `org/DELIVERY-FAITH.md`。

## 飞书与新群

- 新群要在 `openclaw.json` 配 **`groupAllowFrom` + `groups.<chat_id>`**，否则可能只在仪表盘有记录、群里收不到。步骤见 **`~/.openclaw/org/FEISHU-GROUPS.md`**。

## 早间新闻推送（morning-news）

- **仓库**：`/Users/graves/Workspace/morning-news`；关键词触发：`scripts/trigger_news_push.py`。**勿用** `fast_push.py`（已废弃，仅 stderr 说明并 exit 2）。正式脚本若 SIGTERM，应 **重跑 trigger** 或 **加大 exec timeout**，禁止假兜底。
- **OpenClaw `exec`**：**优先省略 `timeout`**（网关默认约 **1800s**）。不要传 **`timeout: 300`**，否则会覆盖默认值并约 5 分钟杀进程；随后「网络不稳 / 明天 8:30」多为 **超时误报**。若必须填写，用 **≥900（建议 1200）**；定时 cron 无此限制。
- 代理干扰时可：`unset http_proxy https_proxy ALL_PROXY all_proxy` 再执行。

## 联网检索（本机约定）

- 内置 `web_search` 已关闭（不再用 Brave API）。
- 需要检索时：读 `skills/multi-search-engine/SKILL.md`，用 `web_fetch` 打开其中 **Baidu / Bing CN / DuckDuckGo** 等 URL（国内优先 Bing CN 或 Baidu），再基于正文作答。
- 可安装 ClawHub：`npx clawhub search …` / `npx clawhub install <name>`（遇 rate limit 可改时段重试）。
- 已装技能目录：`find-skills`、`ddgs-search`（需 `python3 skills/ddgs-search/scripts/install.py` 装 `ddgs`）、`multi-search-engine`、`feishu-messaging`、`self-improving-agent`、`sjht-doubao-image-gen`、**`jimeng-video-volc-sdk`**、**`capcut-skill`**（剪映/CapCut：`pyJianYingDraft` 建草稿/SRT、入场与滤镜、`jy_film_pipeline` 粗剪+可选 Whisper 字幕、`rough_cut_silence`；`references/FILM_OPENCLAW.md` 衔接即梦/漫剧；见 `skills/capcut-skill/README.md`；开发仓库 `/Users/graves/Workspace/Skills/capcut-skill`）；另自 ClawHub 下载榜批量安装：`summarize`、`agent-browser`（若未装上见下）、`skill-vetter`、`gog`、`ontology`、`github`、`proactive-agent`、`self-improving`、`weather`。
- 批量安装脚本（去重、间隔）：`bash ~/.openclaw/org/scripts/install-clawhub-top-downloads.sh 10`。`agent-browser` 需 `--force` 且易撞未登录 **rate limit**，补装：`cd ~/.openclaw/workspace && npx clawhub login && npx clawhub install --dir skills --force agent-browser`。

## 漫剧/视频生成工具（已部署/可落地）
### 方案1：墨影漫机（M芯片本地零成本方案 ✅ 优先选用）
- **方案定义**：基于Mochi Diffusion + MLX-AnimateDiff的本地化漫剧生产方案，零API费用，全流程跑在Mac Mini本地
- **核心优势**：零成本、M芯片原生适配、人物一致性100%可控、数据安全不泄露
- **工具链组成**：
  1. **分镜生成**：Mochi Diffusion（Mac原生SD可视化客户端，支持LoRA统一角色）
  2. **动态生成**：MLX-AnimateDiff（苹果MLX优化，静态分镜转动态片段）
  3. **配音生成**：Edge TTS（本地离线配音，多音色可选）
  4. **后期合成**：FFmpeg（批量拼接、加字幕、配BGM）
- **生产流程**：分镜生成 → 动态生成 → 配音生成 → 后期合成 → 成片输出
- **适配规格**：9:16竖屏/16:9横屏，支持15s/90s/15min多时长，支持日式漫剧/国风/3D等风格
- **安装命令**：
  ```bash
  # 1. 安装Mochi Diffusion（可视化客户端）
  brew install --cask mochi-diffusion
  # 2. 安装MLX-AnimateDiff
  pip install mlx-animate-diff
  ```
- **已预装依赖**：FFmpeg、Edge TTS已完成部署，可直接使用

### 方案2：火山即梦API方案
- **用途**：生成真人写实风短视频，速度快，适合批量生产
- **调用路径**：`/Users/graves/Workspace/film-projects/jimeng-volc-api/run_jimeng_video_sdk.py`
- **成本**：约1.2元/分钟

### 方案3：小云雀剪映混剪方案
- **用途**：真人素材混剪爽剧，制作速度最快，成本最低
- **工具**：剪映pyJianYingDraft SDK
- **成本**：约0.05元/分钟
