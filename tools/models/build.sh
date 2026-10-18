#!/usr/bin/env bash
# Build OMG-C models: Blender (tools/models/assets/<id>.py) -> raw glb -> gltfpack (meshopt + quantization, named pivots kept)
# -> public/models/omg-c/<id>.glb, + ortho renders and deliverables/omg-c-models/<id>-compare.jpg.
# usage: tools/models/build.sh <id> [<id> ...]   env: BLENDER (default /workspace/tools/blender/blender), DESIGN (C design dir)
set -euo pipefail
cd "$(dirname "$0")/../.."
BLENDER=${BLENDER:-/workspace/tools/blender/blender}
DESIGN=${DESIGN:-/workspace/nj-design-v3/levels-design/omg/redesign-v3/C}
TMP=${TMP_DIR:-/tmp/omgc-build}; mkdir -p "$TMP" public/models/omg-c deliverables/omg-c-models
for id in "$@"; do
  # design dir: assets/<id>/ or the design id named in tools/models/specs/<id>.json ("design": "H01_popup_castle")
  did=$id; [ -f "tools/models/specs/$id.json" ] && did=$(python3 -c "import json;print(json.load(open('tools/models/specs/$id.json')).get('design','$id'))")
  ddir="$DESIGN/assets/$did"; spec=""; [ -f "$ddir/spec.json" ] && spec="$ddir/spec.json"
  [ -z "$spec" ] && [ -f "tools/models/specs/$id.json" ] && spec="tools/models/specs/$id.json"
  "$BLENDER" -b --factory-startup -P tools/models/run.py -- "$id" "$TMP" $spec 2>&1 | grep -E '^REPORT|Error|Traceback' || true
  [ -f "$TMP/$id.raw.glb" ] || { echo "FAILED $id"; continue; }
  npx --yes gltfpack@1.3.0 -i "$TMP/$id.raw.glb" -o "public/models/omg-c/$id.glb" -cc -kn -km -noq >/dev/null
  ref=""; [ -f "tools/models/specs/$id.json" ] && ref=$(python3 -c "import json;print(json.load(open('tools/models/specs/$id.json')).get('ref',''))")
  [ -n "$ref" ] && [ ! -f "$ref" ] && ref="$DESIGN/$ref"
  python3 tools/models/compare.py "$id" "$TMP" "deliverables/omg-c-models/$id-compare.jpg" "$ddir" "$ref" >/dev/null
  printf '%s raw=%s glb=%s\n' "$id" "$(stat -c%s "$TMP/$id.raw.glb")" "$(stat -c%s "public/models/omg-c/$id.glb")"
done
