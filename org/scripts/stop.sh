#!/usr/bin/env bash
set -euo pipefail
export OPENCLAW_ORG="${OPENCLAW_ORG:-$HOME/.openclaw/org}"
NOTE="${1:-manual stop}"
export STOP_NOTE="$NOTE"
python3 <<'PY'
import json, os
from datetime import datetime, timezone
org = os.environ["OPENCLAW_ORG"]
note = os.environ.get("STOP_NOTE", "manual stop")
path = os.path.join(org, "control.json")
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)
d["halt"] = True
d["halt_set_at"] = datetime.now(timezone.utc).isoformat()
d["halt_note"] = note
with open(path, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("halt=true", d["halt_set_at"], d["halt_note"])
PY
