#!/bin/bash
# 在启动 OpenClaw gateway 前加载火山 AK/SK（供 exec 子进程继承）。
# 密钥文件：~/.openclaw/org/volc-api.env（勿提交 Git，见 .gitignore）
set -euo pipefail
ENV_FILE="${HOME}/.openclaw/org/volc-api.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi
exec /Users/graves/.nvm/versions/node/v25.8.1/bin/node \
  /Users/graves/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/index.js \
  gateway --port 18789
