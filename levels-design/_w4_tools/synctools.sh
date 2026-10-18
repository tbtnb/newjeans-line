#!/bin/bash
W=/workspace/w4; T=/workspace/nj-design-w4/levels-design/_w4_tools; T2=/workspace/newjeans-line-designs/_w4_tools
for D in $T $T2; do mkdir -p $D/designs $D/specs $D/prose
cp $W/*.py $W/*.sh $D/ ; cp $W/designs/*.py $D/designs/; cp $W/specs/*.py $D/specs/; cp $W/prose/*.md $D/prose/
cp $W/*.chart.raw.json $W/*.chart.raw.orig.json $W/*.grid.json $W/*.offsets.json $W/*.stem_onsets.json $D/ 2>/dev/null
cp $W/*.gen.log $D/ 2>/dev/null; done
