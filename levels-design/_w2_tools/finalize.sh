#!/bin/bash
# finalize.sh slug : build -> report -> notes -> design.md (head + computed route table + tail + chart rationale) -> validate -> copy to clone
set -e
s=$1; cd /workspace/w2-work; . /workspace/venv-w2/bin/activate
python build.py $s 2>&1 | grep -v "drop close"
python report.py $s >/dev/null
python notes.py $s >/dev/null 2>&1 || true
D=/workspace/newjeans-line-designs/$s
cat docs/${s}_head.md > $D/design.md; python route_doc.py $s >> $D/design.md; cat docs/${s}_tail.md >> $D/design.md; python chartdoc.py $s
python3 /workspace/newjeans-line-designs/validate.py $s --dir /workspace/newjeans-line-designs --repo /workspace/nj-design-w2 | grep -vE "^   +[0-9]+\.[0-9]+-"
C=/workspace/nj-design-w2/levels-design; mkdir -p $C/$s $C/_w2_tools
rm -rf $C/$s/*; (cd $D && tar cf - --exclude codex-ref .) | tar xf - -C $C/$s
cp analyze.py gridfit.py setgrid.py rmap.py build.py route.py report.py notes.py cross.py jw.py route_doc.py chartdoc.py artgen.py art.py finalize.sh secstats.py spec_*.py $C/_w2_tools/
cp -r docs $C/_w2_tools/
cp $C/_w2_tools/* /workspace/newjeans-line-designs/_w2_tools/ 2>/dev/null || true
