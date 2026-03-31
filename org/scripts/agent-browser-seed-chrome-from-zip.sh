#!/bin/bash
# 当 `agent-browser install` 卡在从 storage.googleapis.com 下载时：用手动下载的
# chrome-mac-arm64.zip 铺到 agent-browser 期望的目录，无需跑 install 下载。
#
# 用法：
#   bash ~/.openclaw/org/scripts/agent-browser-seed-chrome-from-zip.sh ~/Downloads/chrome-mac-arm64.zip
#   bash ~/.openclaw/org/scripts/agent-browser-seed-chrome-from-zip.sh   # 默认读 ~/Downloads/chrome-mac-arm64.zip
#
# 版本号：与 zip 对应（须与 JSON 里 Stable 一致，否则可传第二个参数）：
#   bash .../agent-browser-seed-chrome-from-zip.sh ./chrome-mac-arm64.zip 147.0.7727.24
set -euo pipefail
ZIP="${1:-$HOME/Downloads/chrome-mac-arm64.zip}"
VERSION="${2:-}"

if [[ ! -f "$ZIP" ]]; then
  echo "找不到 zip: $ZIP"
  echo "请从 install 日志里的 URL 用浏览器下载，或打开："
  echo "  https://googlechromelabs.github.io/chrome-for-testing/"
  exit 1
fi

if [[ -z "$VERSION" ]]; then
  JSON="$(curl -fsS --max-time 30 "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")"
  VERSION="$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print(d['channels']['Stable']['version'])" "$JSON")"
  echo "从 last-known-good JSON 解析版本: $VERSION"
fi

DEST="$HOME/.agent-browser/browsers/chrome-${VERSION}"
BIN="$DEST/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

strip_quarantine() {
  local exe="$1"
  [[ -x "$exe" ]] || return 0
  local app
  app="$(dirname "$(dirname "$(dirname "$exe")")")"
  if [[ -d "$app" ]] && [[ "$app" == *.app ]]; then
    echo "移除 macOS 隔离标记（避免「已损坏」误报）…"
    xattr -dr com.apple.quarantine "$app" 2>/dev/null || xattr -c "$app" 2>/dev/null || true
  fi
}

if [[ -x "$BIN" ]]; then
  echo "已存在且可执行，跳过解压: $BIN"
  strip_quarantine "$BIN"
  exit 0
fi

mkdir -p "$DEST"
echo "解压到: $DEST"
# zip 根目录一般为 chrome-mac-arm64/
unzip -q -o "$ZIP" -d "$DEST"

if [[ ! -x "$BIN" ]]; then
  # 少数包结构不同：.app 直接在 DEST 下
  ALT="$DEST/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
  if [[ -x "$ALT" ]]; then
    strip_quarantine "$ALT"
    echo "OK: $ALT"
    exit 0
  fi
  echo "解压后未找到可执行文件，预期之一："
  echo "  $BIN"
  echo "  $ALT"
  find "$DEST" -maxdepth 4 -name "Google Chrome for Testing" 2>/dev/null || true
  exit 1
fi

strip_quarantine "$BIN"
echo "OK: $BIN"
echo "验证: agent-browser open about:blank"
