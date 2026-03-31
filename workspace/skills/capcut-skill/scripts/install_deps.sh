#!/bin/bash
# 在 capcut-skill 根目录创建 .venv 并安装 requirements.txt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt
echo "OK. 使用: $ROOT/.venv/bin/python scripts/jy_create_from_media.py --help"
