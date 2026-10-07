#!/bin/sh
# Diagnostic runs (per-cut records, swap counterfactuals): 6x8 (60 instances), 10x20 (30).
# Usage: sh run_diag.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
R=scip,orbit,pertE0.1,geo,both
{
for i in 0 10 20 30 40 50; do echo "6x8 $i"; done
for i in 0 10 20; do echo "10x20 $i"; done
} | xargs -P "$1" -L 1 sh -c "python3 mrloop.py ../data/inst_\$0.json $R 20 ../logs/diag/diag_\$0_\$1.jsonl \$1 \$((\$1+10)) diag swap > ../logs/diag/diag_\$0_\$1.log 2>&1"
