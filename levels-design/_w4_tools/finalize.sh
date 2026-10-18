#!/bin/bash
# finalize.sh <slug> : assemble docs, copy to clone, validate, (no commit)
set -e
S=$1; W=/workspace/w4; O=/workspace/newjeans-line-designs/$S; R=/workspace/nj-design-w4/levels-design
python3 $W/fixjudg.py $S; python3 $W/report.py $S >/dev/null; python3 $W/cpm.py $S; python3 $W/amd.py $S >/dev/null; python3 $W/facts.py $S >/dev/null
{ sed "2i\\\n> Note: the rationale below describes the curated basis chart. It was written before the 11:55 rhythmic-logic audit. Where it differs (for example, verse taps that followed vocals are now on the drum layer), the audit section and the per-section *what the taps follow* table are authoritative.\\n" $W/prose/$S.rat.md; echo; cat $O/chart-report.cpm.md; cat $W/prose/$S.cpm.md 2>/dev/null || true; echo; sed '1d' $O/chart-report.body.md; echo; cat $W/prose/method.md; } > $O/chart-report.md
{ cat $W/prose/$S.design.md; echo; cat $O/design.facts.md; } > $O/design.md
rm -f $O/chart-report.cpm.md $O/design.facts.md $O/chart-report.body.md $O/preview.png
mkdir -p $R/$S/art
cp $O/{chart.json,layout.json,analysis.json,analysis.md,chart-report.md,design.md,route.png,route-sections.png} $R/$S/
cp $O/art/* $R/$S/art/
cd /workspace/nj-design-w4 && python3 levels-design/validate.py $S --dir levels-design
