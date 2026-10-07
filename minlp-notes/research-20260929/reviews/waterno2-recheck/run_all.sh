#!/bin/bash
# Run all jobs in jobs.txt ("T t" per line), 6 at a time, 2400 s B&B limit each.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
export LIMIT=${LIMIT:-2400}
xargs -P 6 -L 1 bash -c 'T=$0; t=$1; TT=$(printf %02d $T); tt=$(printf %02d $t); timeout $((LIMIT+900)) python3 run_period.py $T $t '"$LIMIT"' logs/my_implied_$TT.json > logs/rb_${TT}_p${tt}.log 2>&1; echo "done $T $t $(date +%T)"' < ${1:-jobs.txt}
