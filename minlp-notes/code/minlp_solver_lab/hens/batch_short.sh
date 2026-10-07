#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit
T=150; ex=ex1_yg1990_2h2c
for form in orig lift; do
  uv run python -u run_synheat.py $ex $form gurobi $T 2>&1 | grep "^synheat\|rror"
done
for form in orig lift; do
  uv run python -u run_synheat.py $ex $form baron $T > results/synheat_${ex}_${form}_baron.stdout 2>&1
  grep "^synheat\|rror" results/synheat_${ex}_${form}_baron.stdout
done
uv run python -u check_equiv.py gurobi; uv run python -u check_equiv.py baron
echo "=== short batch done ==="
