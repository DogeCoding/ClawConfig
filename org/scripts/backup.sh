#!/usr/bin/env bash
set -euo pipefail
ORG="${OPENCLAW_ORG:-$HOME/.openclaw/org}"
TS="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ORG/backups"
OUT="$ORG/backups/org-backup-${TS}.tar.gz"
ROOT="$(dirname "$ORG")"
NAME="$(basename "$ORG")"
tar -czf "$OUT" -C "$ROOT" --exclude="${NAME}/backups" "$NAME"
echo "$OUT"
