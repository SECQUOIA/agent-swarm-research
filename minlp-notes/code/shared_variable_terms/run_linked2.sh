#!/bin/bash
cd "$(dirname "$0")"
run() { uv run --project ../minlp_solver_lab python gurobi_link.py "$1" linked2 60 4 2>/dev/null | grep "^{" ; }
export -f run
cat power_instances.txt | xargs -P 8 -I{} bash -c "run {}" > results_gurobi_60_linked2.jsonl
echo finished > results_linked2.log
