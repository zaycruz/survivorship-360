#!/usr/bin/env bash
# Fails when the README no longer matches reality. Read-only: it never commits, pushes or bumps pins.
# Usage: scripts/check-drift.sh [path to local module checkouts, default ../]
set -uo pipefail
cd "$(dirname "$0")/.."
LOCAL=${1:-..}
MODULES="coach-console c1-acute-risk c3-rough-patch c4-glucose-guide coach-copilot challenge-mcp"
fail=0
bad() { echo "DRIFT  $*"; fail=1; }
ok() { echo "ok     $*"; }

echo "== submodule pins vs GitHub main"
for m in $MODULES; do
  pin=$(git ls-tree HEAD "modules/$m" | awk '{print $3}')
  remote=$(git ls-remote "https://github.com/zaycruz/$m" refs/heads/main | cut -f1)
  [ "$pin" = "$remote" ] && ok "$m pinned at ${pin:0:7}" || bad "$m pinned at ${pin:0:7}, main is ${remote:0:7}"
done

echo "== local module work not on GitHub"
for m in $MODULES; do
  d="$LOCAL/$m"; [ -d "$d/.git" ] || [ -f "$d/.git" ] || continue
  if ! git -C "$d" remote get-url origin >/dev/null 2>&1; then echo "note   $m has no GitHub remote"; continue; fi
  git -C "$d" fetch -q origin 2>/dev/null
  ahead=$(git -C "$d" rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
  [ "$ahead" = 0 ] && ok "$m: nothing unpushed" || bad "$m: $ahead commit(s) not pushed"
done

echo "== live URLs"
for u in https://patient-360.raava.dev https://c1-acute-risk.zay-259.workers.dev https://c3-rough-patch.zay-259.workers.dev \
         https://c4-glucose-guide.zay-259.workers.dev https://coach.raava.dev; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 20 "$u")
  [ "$code" -lt 400 ] 2>/dev/null && ok "$code $u" || bad "$code $u"
done
tools=$(curl -s -m 20 https://emerge-mcp.raava.dev/mcp -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' |
  python3 -c 'import sys,json; t=sys.stdin.read(); print(len(json.loads(t[t.index("{"):].splitlines()[0])["result"]["tools"]))' 2>/dev/null)
claimed=$(grep -oE '\| ([0-9]+) read-only tools' README.md | grep -oE '[0-9]+')
[ "$tools" = "$claimed" ] && ok "MCP serves $tools tools" || bad "MCP serves ${tools:-?} tools, README says $claimed"

echo "== headline numbers (docs/claims.tsv) in each module's docs on main"
tmp=$(mktemp -d)
for m in $MODULES; do
  git -C "modules/$m" fetch -q origin main 2>/dev/null
done
while IFS=$'\t' read -r m f lit; do
  case "$m" in ''|\#*) continue;; esac
  key="$tmp/$m.$(echo "$f" | tr / _)"
  [ -f "$key" ] || git -C "modules/$m" show "FETCH_HEAD:$f" > "$key" 2>/dev/null
  grep -qF -- "$lit" "$key" && ok "$m: $lit" || bad "$m/$f no longer says: $lit"
done < docs/claims.tsv
rm -rf "$tmp"

[ $fail = 0 ] && echo "README matches reality." || echo "README has drifted; fix it, the diagrams (docs/*.png from Paper) and the pins."
exit $fail
