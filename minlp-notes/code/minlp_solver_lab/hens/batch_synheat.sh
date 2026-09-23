#!/bin/bash
# Task 2 comparison: 3 examples x {orig, lift} x {gurobi, baron}, 600 s each, sequential, 4 threads.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd /home/sgusev/repo/minlp-notes/code/minlp_solver_lab/hens
T=${1:-600}
for ex in ex1_yg1990_2h2c ex2_5h1c ex3_10sp1_5h5c; do
  for form in orig lift; do
    uv run python -u run_synheat.py $ex $form gurobi $T 2>&1 | grep "^synheat\|rror"
    uv run python -u run_synheat.py $ex $form baron $T > results/synheat_${ex}_${form}_baron.stdout 2>&1
    grep "^synheat\|rror" results/synheat_${ex}_${form}_baron.stdout
  done
done
uv run python -u check_equiv.py gurobi
uv run python -u check_equiv.py baron
echo "=== batch done ==="
