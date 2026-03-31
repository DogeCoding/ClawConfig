#!/bin/bash
# 按 ClawHub 公开下载榜（与 topclawhubskills.com / clawhub.ai 同源）安装前 N 名，已存在则跳过。
# agent-browser 被标记为 suspicious 时需加 --force；未登录时易触发 rate limit，可：clawhub login
set -euo pipefail
WORKDIR="${CLAWHUB_WORKDIR:-/Users/graves/.openclaw/workspace}"
SKILLS_SUBDIR="${CLAWHUB_SKILLS_DIR:-skills}"
N="${1:-10}"
API="https://topclawhubskills.com/api/top-downloads?limit=${N}"
echo "Fetching top ${N} by downloads from ${API}"
mapfile -t SLUGS < <(curl -fsS --max-time 30 "$API" | python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(x['slug'] for x in d.get('data',[])))")
if [[ ${#SLUGS[@]} -eq 0 ]]; then
  echo "No slugs from API; abort."
  exit 1
fi
cd "$WORKDIR"
for slug in "${SLUGS[@]}"; do
  if [[ -f "${SKILLS_SUBDIR}/${slug}/SKILL.md" ]]; then
    echo "SKIP (exists): ${slug}"
    continue
  fi
  echo "INSTALL: ${slug}"
  extra=()
  [[ "$slug" == agent-browser ]] && extra=(--force)
  npx --yes clawhub@latest install --workdir "$WORKDIR" --dir "$SKILLS_SUBDIR" "${extra[@]}" "$slug" || {
    echo "FAILED: ${slug} (rate limit? run: clawhub login ; or retry later)"
  }
  sleep 4
done
echo "Done. Check lock: (cd \"$WORKDIR\" && npx --yes clawhub@latest list)"
