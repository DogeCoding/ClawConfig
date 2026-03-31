---
name: jimeng-video-volc-sdk
description: "即梦/火山视频样片：零下一百度生存日记漫剧、生成样片、继续生成样片、漫剧 MVP、Jimeng VisualService SDK、下载 mp4、verify_sample 验收"
description_en: "Jimeng sample video, novel-to-drama MVP, VisualService SDK, mp4 download, verify_sample gate"
allowed-tools: Read,Write,Bash,exec
---

## 主人简口令（无需长复制）

当用户只说「继续生成零下一百度样片」「帮我生成漫剧样片」「即梦样片」等时，**直接按本文执行**，不要求用户粘贴指令模板。细则见 **`~/.openclaw/workspace/SOUL.md`「漫剧样片（主人简口令）」**。

**CRITICAL：禁止主答复为「去即梦网页复制参数」**（除非本技能中的脚本已实际执行失败且用户明确要求改网页）。接口与命令已固定；不得以「API 待确认」逃避 **`exec`**。

---

# 即梦视频（火山 VisualService SDK）

当前 PyPI 包 **`volcengine`（volc-sdk-python）已不包含 `volcengine.jimeng` 模块**。即梦视频请使用 **`VisualService.cv_sync2async_submit_task` / `cv_sync2async_get_result`**。SDK 内部使用 **Host=`visual.volcengineapi.com`、签名 Service=`cv`**，不要手写 OpenAPI 混用 `GenerateVideo`+`cv` 主机。

## 环境

1. 本机项目目录（ASCII，便于 Agent 编辑）：
   - `/Users/graves/Workspace/film-projects/jimeng-volc-api/`
2. 虚拟环境（推荐，避免 Homebrew PEP668 限制）：
   ```bash
   cd /Users/graves/Workspace/film-projects/jimeng-volc-api
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
3. 密钥（**勿写入脚本或 Git**）：
   - `export VOLC_ACCESSKEY="..."`  
   - `export VOLC_SECRETKEY="..."`  
   （亦支持 `VOLC_ACCESS_KEY` / `VOLC_SECRET_KEY`）

## 提交并下载样片

```bash
OUT="/Users/graves/Workspace/film-projects/零下一百度生存日记漫剧/成片/mvp-sdk-$(date +%Y%m%d).mp4"
mkdir -p "$(dirname "$OUT")"
/Users/graves/Workspace/film-projects/jimeng-volc-api/.venv/bin/python \
  /Users/graves/Workspace/film-projects/jimeng-volc-api/run_jimeng_video_sdk.py \
  --out "$OUT" \
  --prompt "你的分镜/风格描述"
```

仅提交、看 `task_id`：

```bash
.../run_jimeng_video_sdk.py --out /tmp/x.mp4 --dry-submit
```

`req_key` 必须与控制台开通能力一致（默认 `jimeng_t2v_v30`，可 `--req-key jimeng_t2v_v30_1080p` 等，以文档为准）。

## 硬验收（声称「有成片」前必跑）

```bash
bash /Users/graves/Workspace/film-projects/jimeng-volc-api/verify_sample.sh "$OUT" 50000
```

## AI / OpenClaw 流程

1. 确认 `.venv` 与 `requirements.txt` 已安装。  
2. 用 **Bash** 执行上述 `run_jimeng_video_sdk.py`（主 agent `sandbox: off` 时在本机执行）。  
3. 成功后执行 `verify_sample.sh`，再把 **绝对路径** 发给主人；飞书发文件走 `feishu-messaging` 等能力。  
4. **禁止**在 verify 通过前说「已生成样片」。  
5. 图生视频、运镜等：只改 `req_key` 与 form 字段，仍以 [智能视觉 / 即梦接口文档](https://www.volcengine.com/docs/85128/1792710) 为准。

## 参考

- 项目 RUNBOOK：`jimeng-volc-api/RUNBOOK_NOVEL_TO_DRAMA_MVP.md`  
- 无 SDK 手写签名（调试用）：`jimeng-volc-api/gen_sample_no_sdk.py`  
- 豆包文生图：`sjht-doubao-image-gen` skill
