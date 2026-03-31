#!/usr/bin/env bash
# 将「主 workspace」的 skills/ 同步到所有 workspace-*/skills/（OpenClaw 多 agent）。
# 原因：ClawHub / 手工装技能往往只落在 ~/.openclaw/workspace/skills，新建岗（如 juyi）不会自动出现。
# 用法：bash ~/.openclaw/org/scripts/sync-skills-to-agent-workspaces.sh
# 可选：SOURCE_WORKSPACE=/path/to/main/workspace
set -euo pipefail
SOURCE_WORKSPACE="${SOURCE_WORKSPACE:-/Users/graves/.openclaw/workspace}"
SRC="${SOURCE_WORKSPACE%/}/skills"
ROOT="/Users/graves/.openclaw"

if [[ ! -d "$SRC" ]]; then
  echo "missing skills dir: $SRC" >&2
  exit 1
fi

shopt -s nullglob
for ws in "$ROOT"/workspace-*/; do
  [[ -d "$ws" ]] || continue
  dest="${ws}skills"
  mkdir -p "$dest"
  echo "rsync -> $(basename "$ws")"
  rsync -a \
    --exclude='.git/' \
    --exclude='**/.venv/' \
    --exclude='**/__pycache__/' \
    "$SRC/" "$dest/"
done

echo "Done. Source: $SRC"
