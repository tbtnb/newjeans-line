#!/bin/bash
export PATH=/Users/bit_1/.nvm/versions/node/v22.17.0/bin:$PATH
ROOT=$HOME/nj-skins-art; cd $ROOT
job(){
  slug=$1; d=$ROOT/$slug; mkdir -p $d
  IFS=$'\t' read s name desc < <(awk -F'\t' -v s=$slug '$1==s' $ROOT/skins.tsv)
  ok=1; for f in concept trail particle icon; do [ -s $d/$f.png ] || ok=0; done; [ -s $d/design.md ] || ok=0
  [ $ok = 1 ] && { echo "skip $slug" >> $ROOT/status.txt; return; }
  echo "start $slug $(date +%T)" >> $ROOT/status.txt
  codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check -C "$d" "You are the art designer of a SKIN for the player's line in a fan-made web game recreating the mobile game 'Dancing Line' (跳舞的线) with NewJeans songs. In Dancing Line the player is a small cube 'head' that moves along a path, leaving a solid straight 'trail' bar behind it; it turns 90 degrees on each tap, emits a small burst on each turn, and shatters into particles on death.

Skin: '$name' (slug $slug). Design brief: $desc

Produce these files in this directory, each image made with your built-in image_gen tool (one call per image), then copied from \$CODEX_HOME/generated_images (default ~/.codex/generated_images) to the exact filename here:
1. concept.png — landscape 3:2 skin concept sheet on a clean light background: the head cube shown large in 3/4 isometric view, a trail segment with one 90-degree corner in isometric view, the tap/turn burst particles, the death shatter particles, and a row of 4-5 flat colour swatches. NO text, letters or numbers on the sheet.
2. trail.png — square SEAMLESS tileable flat texture for the trail bar surface (top-down, no perspective, no vignette, no focal object, tiles cleanly left-right and up-down).
3. particle.png — square particle sprite: ONE single particle shape (e.g. heart / bubble / pixel / snowflake / star) centred, filling ~80% of the frame, on a TRANSPARENT background. Mostly light/white-ish tones are fine since it will be tinted; keep it simple and bold so it reads at 32px.
4. icon.png — square UI thumbnail icon for the skin picker: the head cube with a short trail stub, centred, on a TRANSPARENT background, bold and readable at 64px.
For transparent images verify with python3 + PIL that the PNG is RGBA with transparent corners; if not, regenerate once on a perfectly flat solid #FF00FF background (subject must contain no magenta) and note that in prompts.md.
5. design.md — written by you: skin name, one-paragraph description, an exact palette as hex codes with roles (head base, head accent/emissive, trail base, trail edge/stitch, burst particle colours x2, death particle colours x2, picker UI accent), recommended material properties for a real-time Babylon.js StandardMaterial/PBR (glossiness/specular power, emissive strength, alpha), particle behaviour notes (count, size, lifetime, gravity, shape), and the image_gen prompts you used.
Hard rules: original designs only, NO official logos or brand marks copied, NO real people, no human faces or likenesses of any NewJeans member, NO letters/words/numbers in images, no watermarks. Style: clean, cute, Y2K-pastel casual-game art, crisp shapes, soft gradients. Do not create any other files. Finish when all 5 files exist." > $d/codex.log 2>&1
  echo "done $slug rc=$? $(date +%T)" >> $ROOT/status.txt
}
export -f job; export ROOT
echo "run $(date)" >> $ROOT/status.txt
printf '%s\n' bunny denim bubble-gum phoning film supernatural | xargs -P 6 -I{} bash -c 'job {}'
echo "ALLDONE $(date +%T)" >> $ROOT/status.txt
