#!/bin/bash
# SCIP 10, 300 s, 1 thread: native / root-only / node separation to depth 3, 8 / every node.
cd "$(dirname "$0")"
RUN="uv run --project ../minlp_solver_lab python"
run() { $RUN scip_sepa.py 8 12 $1 $2 $3 $4 --tl 300 --maxdepth $5 2>/dev/null | grep "^{" | sed "s/\"mode\": \"tree\"/\"mode\": \"tree_d$5\"/" ; }
export -f run; export RUN
for seed in 0 1 2 3 4; do for cost in quad log; do for cap in uniform random; do
  echo "$seed $cap $cost native 1000"; echo "$seed $cap $cost root 0"; echo "$seed $cap $cost tree 3"; echo "$seed $cap $cost tree 8"; echo "$seed $cap $cost tree 1000"
done; done; done | nice xargs -P 20 -L 1 bash -c 'run $0 $1 $2 $3 $4' > results/scip_sepa_sweep.jsonl
echo finished > results/scip_sepa_sweep.log
