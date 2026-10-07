#!/bin/sh
# Revision after review round 2: diag records (chosen and SCIP steps per cut, no swaps) for six more
# rules that lose on 6x8 (60 instances, 20 rounds), to measure the "shorter sets" factor of
# note Section 3.6 for them.  Usage: sh run_rev2.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
R=pert0.1,pertE1,lex0.1,orbit_core,orbitB,alt
mkdir -p ../logs/rev2
for i in 0 10 20 30 40 50; do echo "6x8 $i"; done | xargs -P "$1" -L 1 sh -c "timeout 5400 python3 mrloop.py ../data/inst_\$0.json $R 20 ../logs/rev2/diag2_\$0_\$1.jsonl \$1 \$((\$1+10)) diag > ../logs/rev2/diag2_\$0_\$1.log 2>&1; echo \"\$0 \$1 exit \$?\" >> ../logs/rev2/done.txt"
