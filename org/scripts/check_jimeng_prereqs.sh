#!/bin/bash
# 检测漫剧样片流水线前提：venv、网关能否读到 VOLC_*（不打印密钥值）
set -euo pipefail
echo "=== 1. jimeng-volc-api/.venv ==="
VENV_PY="/Users/graves/Workspace/film-projects/jimeng-volc-api/.venv/bin/python"
if [[ -x "$VENV_PY" ]]; then
  if "$VENV_PY" -c "from volcengine.visual.VisualService import VisualService" 2>/dev/null; then
    echo "OK: volcengine VisualService 可导入"
  else
    echo "FAIL: 无法导入 VisualService，请: cd .../jimeng-volc-api && .venv/bin/pip install -r requirements.txt"
  fi
else
  echo "FAIL: 无 .venv，请: cd .../jimeng-volc-api && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
fi

echo ""
echo "=== 2. 密钥文件 ~/.openclaw/org/volc-api.env ==="
ENV_F="${HOME}/.openclaw/org/volc-api.env"
if [[ -f "$ENV_F" ]]; then
  if grep -qE '^[[:space:]]*VOLC_ACCESSKEY[[:space:]]*=' "$ENV_F" && grep -qE '^[[:space:]]*VOLC_SECRETKEY[[:space:]]*=' "$ENV_F"; then
    echo "OK: 文件存在且含 VOLC_ACCESSKEY / VOLC_SECRETKEY 键（不校验值是否正确）"
  else
    echo "WARN: 文件存在但可能缺少两行键名，对照 volc-api.env.example"
  fi
else
  echo "MISS: 未创建。执行: cp ~/.openclaw/org/volc-api.env.example ~/.openclaw/org/volc-api.env && 编辑填入 AK/SK"
fi

echo ""
echo "=== 3. LaunchAgent 是否传入 VOLC（launchctl 用户域）==="
# 仅当 plist 用 gateway-volc-env.sh 且 volc-api.env 已配置时，子进程才有变量；
# launchctl getenv 反映的是 launchd 环境，包装脚本注入的在 node 进程内。
if launchctl print "gui/$(id -u)/ai.openclaw.gateway" 2>/dev/null | grep -q gateway-volc-env; then
  echo "OK: 当前 Label 的 ProgramArguments 含 gateway-volc-env.sh（会 source volc-api.env）"
else
  echo "INFO: 若未改 plist，网关 node 进程可能读不到 VOLC_*；请确认已按 org/VOLC-GATEWAY.md 更新 LaunchAgent"
fi

echo ""
echo "=== 4. gateway 进程与 VOLC 环境 ==="
# 避免变量名 PID：在 set -u 下，部分 bash/环境下与内建或解析边界冲突
GW_PID=$(pgrep -f "openclaw/dist/index.js.*gateway" | head -1 || true)
[[ -z "${GW_PID:-}" ]] && GW_PID=$(pgrep -x openclaw-gateway | head -1 || true)
if [[ -z "${GW_PID:-}" ]]; then
  echo "SKIP: 未发现 gateway 进程（未运行或未匹配）"
else
  echo "INFO: 发现 gateway 相关进程 pid=${GW_PID}（命令行可能显示为 openclaw-gateway）"
  # macOS：对 LaunchAgent 拉起的进程，ps eww 通常不打印环境变量（仅表头+COMMAND），
  # 用 ps grep VOLC_* 会恒为假阴性，不得据此报 WARN。
  PS_LINES=$(ps eww -p "$GW_PID" 2>/dev/null | wc -l | tr -d ' ')
  PS_HAS_ENV=false
  if [[ "${PS_LINES:-0}" -gt 2 ]] && ps eww -p "$GW_PID" 2>/dev/null | grep -qE '=[^[:space:]]+'; then
    PS_HAS_ENV=true
  fi
  if [[ "$PS_HAS_ENV" == true ]]; then
    if ps eww -p "$GW_PID" 2>/dev/null | grep -q VOLC_ACCESSKEY=; then
      echo "OK: ps 可见进程环境中含 VOLC_ACCESSKEY=（值已隐藏）"
    else
      echo "WARN: ps 能读环境但未发现 VOLC_ACCESSKEY=；请确认 gateway-volc-env.sh 与 volc-api.env"
    fi
  else
    echo "SKIP: 本机 ps 未展示该进程环境（常见于 macOS LaunchAgent）；不以 ps 结果判断密钥是否注入"
  fi
fi

echo ""
echo "=== 5. volc-api.env 可被 shell 加载且变量非空（不打印值）==="
ENV_F="${HOME}/.openclaw/org/volc-api.env"
if [[ -f "$ENV_F" ]]; then
  # shellcheck disable=SC1090
  if ( set -a; source "$ENV_F"; set +a; [[ -n "${VOLC_ACCESSKEY:-}" && -n "${VOLC_SECRETKEY:-}" ]] ); then
    echo "OK: source 后 VOLC_ACCESSKEY / VOLC_SECRETKEY 均非空（排除空值与明显语法错误）"
  else
    echo "WARN: 文件存在但 source 后缺少非空 VOLC_ACCESSKEY 或 VOLC_SECRETKEY，请检查内容与格式（每行 KEY=value）"
  fi
else
  echo "SKIP: 无 volc-api.env"
fi

echo ""
echo "完成。网关是否真带上 VOLC：以 agent 执行 run_jimeng_video_sdk 是否仍报缺密钥为准。"
echo "手动验收样片: bash .../jimeng-volc-api/verify_sample.sh <mp4> 50000"
