#!/bin/bash
# Gurobi 13, native vs linked: 60 s pilot on all instances with links (4 threads, 8 at a time),
# then 1800 s runs on the open instances (3 threads, all ten at once).
cd "$(dirname "$0")"
run() { uv run --project ../minlp_solver_lab python gurobi_link.py "$1" "$2" "$3" "$4" 2>/dev/null | grep "^{" ; }
export -f run
for mode in native linked; do cat link_instances.txt | xargs -P 8 -I{} bash -c "run {} $mode 60 4"; done > results_gurobi_60.jsonl
for inst in waterno2_06 waterno2_09 waterno2_12 waterno2_18 ghg_2veh; do for mode in native linked; do
  (run $inst $mode 1800 3 >> results_gurobi_1800.jsonl) & done; done; wait
echo finished > results_gurobi.log
