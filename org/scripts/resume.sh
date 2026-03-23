#!/usr/bin/env bash
set -euo pipefail
export OPENCLAW_ORG="${OPENCLAW_ORG:-$HOME/.openclaw/org}"
python3 -c "
import json, os
org = os.environ['OPENCLAW_ORG']
path = os.path.join(org, 'control.json')
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)
d['halt'] = False
d['halt_set_at'] = None
d['halt_note'] = ''
with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('halt=false')
"
