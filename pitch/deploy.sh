#!/usr/bin/env bash
# Rebuild the hosted deck from slides/ + slides.py and deploy it to Cloudflare Workers.
# Refuses to deploy unless check.py passes (every slide number still matches its module README).
# After editing in Paper: re-export the changed artboards as PNG 2x into slides/NN.png, then run this.
set -euo pipefail
cd "$(dirname "$0")"
uv run -q --with python-pptx python -I check.py > /dev/null || { tail -40 check.txt; echo "deploy.sh: check failed, not deploying"; exit 1; }
python3 -I build_web.py web
WRANGLER=${WRANGLER:-../../coach-console/node_modules/.bin/wrangler}
"$WRANGLER" deploy
