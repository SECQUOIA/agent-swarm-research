#!/bin/bash
# waits for the gen1 300 s comparison, then runs the (c) bounds and short SYNHEAT smoke tests
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit
until [ -f results/heatexch_gen1_solvers300.json ]; do sleep 5; done
echo "=== gen1_bounds ==="
uv run python -u gen1_bounds.py 600 2>&1 | grep -v "^$\|WORKING"
echo "=== smoke tests (30 s) ==="
for form in orig lift lift_cubic; do
  uv run python -u run_synheat.py ex1_yg1990_2h2c $form gurobi 30 2>&1 | grep "^synheat\|Error\|error" 
done
for form in orig lift; do
  uv run python -u run_synheat.py ex1_yg1990_2h2c $form baron 30 > results/synheat_ex1_yg1990_2h2c_${form}_baron.stdout 2>&1; grep "^synheat\|rror" results/synheat_ex1_yg1990_2h2c_${form}_baron.stdout
done
uv run python -u check_equiv.py gurobi
uv run python -u check_equiv.py baron
echo "=== chain done ==="
