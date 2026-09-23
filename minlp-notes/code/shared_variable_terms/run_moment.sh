#!/bin/bash
cd "$(dirname "$0")"
run() { uv run --project ../minlp_solver_lab python gurobi_link.py "$1" "$2" 60 4 2>/dev/null | grep "^{" ; }
export -f run
for mode in moment linkmoment; do cat moment_instances.txt | xargs -P 8 -I{} bash -c "run {} $mode"; done > results_gurobi_60_moment.jsonl
echo finished > results_moment.log
