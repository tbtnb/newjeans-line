#!/usr/bin/env bash
# Build OMG-C models (box or Mac): Blender tools/models/assets/<id>.py -> raw glb -> gltfpack (meshopt, named pivots kept)
# -> public/models/omg-c/<id>.glb, ortho renders, deliverables/omg-c-models/<id>-compare.jpg (+ <id>.metrics.json in TMP_DIR).
# usage: tools/models/build.sh <id> [<id> ...]     env: BLENDER, DESIGN (C design dir containing assets/), TMP_DIR
set -uo pipefail
cd "$(dirname "$0")/../.."
if [ -z "${BLENDER:-}" ]; then for b in /workspace/tools/blender/blender "$HOME/tools/Blender.app/Contents/MacOS/Blender"; do [ -x "$b" ] && BLENDER=$b && break; done; fi
if [ -d design/assets ]; then DESIGN=${DESIGN:-$PWD/design}; TMP=${TMP_DIR:-$PWD/build}; else DESIGN=${DESIGN:-/workspace/nj-design-v3/levels-design/omg/redesign-v3/C}; TMP=${TMP_DIR:-/tmp/omgc-build}; fi
 mkdir -p "$TMP" public/models/omg-c deliverables/omg-c-models
for id in "$@"; do
  read -r did item < <(python3 -c "import json;c={x['id']:x for x in json.load(open('tools/models/catalog.json'))}.get('$id',{});print(c.get('design','$id'), c.get('item',''))")
  ddir="$DESIGN/assets/$did"; spec=""; [ -f "$ddir/spec.json" ] && spec="$ddir/spec.json"
  [ -z "$spec" ] && [ -f "tools/models/specs/$id.json" ] && spec="tools/models/specs/$id.json"
  rm -f "$TMP/$id.raw.glb"
  "$BLENDER" -b --factory-startup -P tools/models/run.py -- "$id" "$TMP" "$spec" "$item" 2>&1 | grep -E '^REPORT|Error|Traceback|line [0-9]+' || true
  [ -f "$TMP/$id.raw.glb" ] || { echo "FAILED $id"; continue; }
  npx --yes gltfpack@1.3.0 -i "$TMP/$id.raw.glb" -o "public/models/omg-c/$id.glb" -cc -kn -km -noq >/dev/null
  python3 tools/models/compare.py "$id" "$TMP" "deliverables/omg-c-models/$id-compare.jpg" "$ddir" "" ${item:+--item $item} | grep METRICS
  printf '%s glb=%s\n' "$id" "$(wc -c < "public/models/omg-c/$id.glb" | tr -d ' ')"
done
