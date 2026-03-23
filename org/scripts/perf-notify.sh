#!/usr/bin/env bash
set -euo pipefail
ROOT="${OPENCLAW_ORG:-$HOME/.openclaw/org}"
if [[ -f "$ROOT/local.env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ROOT/local.env"
  set +a
fi
exec python3 "$ROOT/scripts/perf_watch.py" --push
