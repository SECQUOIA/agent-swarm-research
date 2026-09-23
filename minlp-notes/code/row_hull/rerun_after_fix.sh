#!/bin/bash
cd "$(dirname "$0")"
RUN="uv run --project ../minlp_solver_lab python"
./run_queue.sh
$RUN root_bounds.py results/root_bounds_fc.jsonl f8x12 --caps uniform random --costs quad log --seeds 0 1 2 3 4 > results/root_bounds_fc.log 2>&1
$RUN minlplib_qp.py results/minlplib_qp.jsonl > results/minlplib_qp.log 2>&1
(for cap in random; do $RUN bb.py 5 7 $cap quad 3 2>&1 | grep transport; done) > results/bb_nodes_5x7_random_rerun.txt 2>&1
$RUN scip_sepa.py 8 12 0 random quad root --tl 300 2>&1 | grep "^{" > results/scip_sepa_random_rerun.jsonl
$RUN scip_sepa.py 8 12 0 random quad tree --tl 300 2>&1 | grep "^{" >> results/scip_sepa_random_rerun.jsonl
echo allfinished
