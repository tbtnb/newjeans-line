#!/usr/bin/env bash
# Publish the current build to gh-pages under /preview/ WITHOUT touching the live game at the site root.
# Appends a normal commit on gh-pages (no force push); roll back with git revert on gh-pages.
set -euo pipefail
cd "$(dirname "$0")/.."
SHA=$(git rev-parse --short HEAD)
node tools/build-levels.mjs
npx vite build --outDir /workspace/nj-preview-dist --emptyOutDir
git fetch -q origin gh-pages
WT=/workspace/nj-ghp
[ -d "$WT" ] || git worktree add -q "$WT" origin/gh-pages
cd "$WT" && git checkout -q --detach origin/gh-pages
rm -rf preview && mkdir preview && cp -r /workspace/nj-preview-dist/. preview/
echo "{\"preview_of\":\"rebuild@$SHA\",\"built\":\"$(date -Iseconds)\"}" > preview/build.json
git add -A preview && git commit -qm "Preview: rebuild@$SHA at /preview/ (live root unchanged)" && git push -q origin HEAD:gh-pages
git log --oneline -1
