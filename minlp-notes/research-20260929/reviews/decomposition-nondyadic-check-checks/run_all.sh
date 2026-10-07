#!/bin/sh
# Runs every mode of nondyadic_check.py for E3, E2, E4m5 and E1x0 (logs in logs/).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
for exp in E3 E2 E4m5 E1x0; do
  for m in closed tol exact open; do
    timeout 3000 python3 nondyadic_check.py $m $exp > logs/${exp}_$m.log 2>&1
  done
done
python3 compare.py > logs/compare.log
