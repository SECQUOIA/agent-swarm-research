#!/bin/bash
# Needs <name>.gms from https://www.minlplib.org/gms/<name>.gms in this directory.
# usage: solve1.sh <name> <solver>   (default start point of the MINLPLib gms file; 300 s limit)
name=$1; solver=$2; dir=s1_${name}_${solver}; rm -rf $dir; mkdir -p $dir; cd $dir
echo "option nlp = $solver; option reslim = 300;" > inc.gms
timeout 600 gams ../$name.gms u1=inc.gms lo=2 threads=1 savepoint=1 > gams.out 2>&1
echo "$name $solver $(grep -E 'MODEL STATUS' $name.lst | tr -s ' ') $(gdxdump m_p.gdx symb=objvar 2>/dev/null | grep -o 'L [-0-9.eE+]*')"
