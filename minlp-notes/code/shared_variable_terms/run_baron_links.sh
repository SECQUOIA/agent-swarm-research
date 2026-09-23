#!/bin/bash
cd "$(dirname "$0")"
for inst in waterno2_06 waterno2_09 waterno2_12 waterno2_18 ghg_2veh; do for mode in native linked; do
  (uv run --project ../minlp_solver_lab python baron_link.py $inst $mode 1800 2>/dev/null | grep "^{" >> results_baron_1800.jsonl) &
done; done; wait; echo finished > results_baron.log
