#!/bin/bash
cd "$(dirname "$0")"
run() { nice uv run --project ../minlp_solver_lab python link_pilot.py "$1" "$2" 60 2>/dev/null | grep "^{" ; }
export -f run
for mode in native linked; do cat scan_candidates.txt | xargs -P 12 -I{} bash -c "run {} $mode"; done > results_links.jsonl
echo finished >> results_links.log
