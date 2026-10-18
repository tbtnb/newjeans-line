#!/usr/bin/env bash
# Publish the tapper page (tapper/) to gh-pages under /tapper/ ONLY. The live game at the site root and /preview/ are not touched.
# Appends a normal commit on gh-pages (no force push); roll back with git revert on gh-pages. Audio is shared from the site's /audio/.
set -euo pipefail
cd "$(dirname "$0")/.."
SHA=$(git rev-parse --short HEAD)
node tools/tapper/gen-songs.mjs
npx vite build -c vite.tapper.config.ts
git fetch -q origin gh-pages
WT=/workspace/nj-ghp
[ -d "$WT" ] || git worktree add -q "$WT" origin/gh-pages
cd "$WT" && git checkout -q --detach origin/gh-pages
rm -rf tapper && mkdir tapper && cp -r /workspace/nj-tapper-dist/. tapper/
echo "{\"tapper_of\":\"$(git -C "$OLDPWD" rev-parse --abbrev-ref HEAD)@$SHA\",\"built\":\"$(date -Iseconds)\"}" > tapper/build.json
CHANGED=$(git status --porcelain | grep -v '^.. tapper/' || true)
if [ -n "$CHANGED" ]; then echo "refusing: changes outside tapper/:"; echo "$CHANGED"; exit 1; fi
git add -A tapper && git commit -qm "Tapper: $SHA at /tapper/ (live root and /preview/ unchanged)" && git push -q origin HEAD:gh-pages
git log --oneline -1
