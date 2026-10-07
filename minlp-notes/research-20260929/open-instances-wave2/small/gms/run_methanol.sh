#!/bin/bash
# usage: run_methanol.sh <name> <firstparamindex> <solver> <t1> <t2> <t3> <t4> <t5> <tag>
# Needs ../gms/<name>.gms from https://www.minlplib.org/gms/<name>.gms.
# Fix the 5 kinetic parameters at the given values, solve for the states, unfix, re-solve the full NLP.
name=$1; k=$2; solver=$3; tag=$9
dir=run_${name}_${solver}_${tag}; mkdir -p $dir; cd $dir
cat > inc.gms <<EOT
option nlp = $solver; option reslim = 300;
x$((k)).fx = $4; x$((k+1)).fx = $5; x$((k+2)).fx = $6; x$((k+3)).fx = $7; x$((k+4)).fx = $8;
Solve m using NLP minimizing objvar;
x$((k)).lo = 0; x$((k+1)).lo = 0; x$((k+2)).lo = 0; x$((k+3)).lo = 0; x$((k+4)).lo = 0;
x$((k)).up = inf; x$((k+1)).up = inf; x$((k+2)).up = inf; x$((k+3)).up = inf; x$((k+4)).up = inf;
EOT
timeout 900 gams ../$name.gms u1=inc.gms savepoint=1 lo=2 threads=1 > gams.out 2>&1
grep -E "SOLVER STATUS|MODEL STATUS|OBJECTIVE VALUE" $name.lst | tail -3
