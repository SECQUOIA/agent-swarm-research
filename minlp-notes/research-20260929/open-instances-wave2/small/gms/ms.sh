#!/bin/bash
# Needs <name>.gms from https://www.minlplib.org/gms/<name>.gms in this directory.
# multistart local solves inside one GAMS job: random levels for the listed variables.
# usage: ms.sh <name> <solver> <nstarts> <seed> <lo> <hi> <var> [<var> ...]
name=$1; solver=$2; ns=$3; seed=$4; lo=$5; hi=$6; shift 6
dir=ms_${name}_${solver}_${seed}; rm -rf $dir; mkdir -p $dir; cd $dir
{
echo "option nlp = $solver; option reslim = 120; option seed = $seed; m.solprint = 2;"
echo "set k /k1*k$ns/; parameter res(k,*);"
echo "loop(k,"
for v in "$@"; do echo "  $v.l = uniform($lo, $hi);"; done
echo "  solve m using NLP minimizing objvar;"
echo "  res(k,'obj') = objvar.l; res(k,'ms') = m.modelstat; res(k,'ss') = m.solvestat;"
i=0; for v in "$@"; do i=$((i+1)); echo "  res(k,'v$i') = $v.l;"; done
echo ");"
echo "display res;"
} > inc.gms
timeout 1500 gams ../$name.gms u1=inc.gms lo=2 threads=1 > gams.out 2>&1
awk '/PARAMETER res/,/^$/' $name.lst | head -40
