#!/usr/bin/env bash
# Preview-only, normal fast-forward publication. Never run without preview publish authorization.
set -euo pipefail
cd "$(dirname "$0")/.."
BR=$(git branch --show-current)
case "$BR" in omg-c|omg-c-preview|omg-c-*) ;; *) echo "Refusing non-OMG source branch: $BR" >&2; exit 1;; esac
git diff --quiet && git diff --cached --quiet || { echo 'Commit tracked source changes before publishing.' >&2; exit 1; }
SHA=$(git rev-parse --short HEAD)
ROOT=$(pwd)
RUN=$(mktemp -d "${TMPDIR:-/tmp}/nj-preview.XXXXXX")
WT="$RUN/pages"
echo "Source: $BR@$SHA; isolated output: $RUN"
node tools/build-levels.mjs
npx tsc --noEmit
npx vite build --outDir "$RUN/dist" --emptyOutDir
git diff --quiet || { echo 'Build changed tracked source; inspect and commit first.' >&2; exit 1; }
git fetch origin gh-pages
BASE=$(git rev-parse origin/gh-pages)
git worktree add --detach "$WT" "$BASE"
# WT is always a fresh, unique worktree owned by this invocation.
rm -rf -- "$WT/preview"
mkdir "$WT/preview"
cp -R "$RUN/dist/." "$WT/preview/"
printf '{"preview_of":"%s@%s","built":"%s"}\n' "$BR" "$SHA" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$WT/preview/build.json"
cd "$WT"
git add -A -- preview
while IFS= read -r -d '' p; do
  case "$p" in preview/*) ;; *) echo "Refusing non-preview change: $p" >&2; exit 1;; esac
done < <(git diff --cached --name-only -z)
# Includes root assets and tapper. A change outside preview aborts before any push.
git diff --cached --exit-code -- . ':(exclude)preview/**'
git commit -m "Preview: $BR@$SHA (root and tapper unchanged)"
git merge-base --is-ancestor "$BASE" HEAD
git diff --exit-code "$BASE" HEAD -- . ':(exclude)preview/**'
git push origin HEAD:gh-pages
cat preview/build.json
cd "$ROOT"
git worktree remove "$WT"
echo "Build and publication evidence retained at $RUN"
