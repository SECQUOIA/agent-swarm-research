#!/bin/bash
# local NLP solve of a MINLPLib gms model from a given start point (.sol), 300 s limit, 1 thread.
# usage: local.sh <name> <start.sol> <solver> <tag>
research_dir=$(cd -- "$(dirname -- "$0")/../../.." && pwd)
name=$1; start=$2; solver=$3; tag=$4
dir=run_${name}_${tag}_${solver}; rm -rf $dir; mkdir -p $dir; cd $dir
python3 - "$start" > start.gms <<'PY'
import sys
for line in open(sys.argv[1]):
    p = line.split()
    if len(p) == 2:
        print(f"{p[0]}.l = {p[1]};")
PY
printf "option nlp = %s; option reslim = 300;\n\$include start.gms\n" $solver > inc.gms
timeout 600 gams ../$name.gms u1=inc.gms lo=2 threads=1 savepoint=1 > gams.out 2>&1
python3 "$research_dir/open-instances-wave2/small/gdx2sol.py" m_p.gdx result.sol
echo "$name $tag $solver $(grep -E 'MODEL STATUS' $name.lst | tr -s ' ') objvar $(grep objvar result.sol)"
