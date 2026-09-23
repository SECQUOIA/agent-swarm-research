#!/bin/bash
cd "$(dirname "$0")"
for inst in waterno2_06 waterno2_09 waterno2_12 waterno2_18 ghg_2veh ex8_4_2; do
  (uv run --project ../minlp_solver_lab python gurobi_link.py $inst moment 1800 3 2>/dev/null | grep "^{" >> results_gurobi_1800_moment.jsonl) &
done; wait; echo finished > results_moment_1800.log
