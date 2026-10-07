#!/bin/bash
# Revision after review: grid-restricted minimal certificates with certified bounds (kappa = 0, c = 0).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for a in "2 4 1e-2" "2 7 1e-4" "2 10 1e-6" "3 4 1e-2" "3 5 1e-3" "4 3 1e-2"; do
  set -- $a
  python3 grid_dp.py $1 $2 $3 > logs/grid_dp_n$1_$3.log 2>&1 &
done
wait
