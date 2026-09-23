#!/bin/bash
# Final study, run sequentially so that at most ~32 solver threads are active.
cd "$(dirname "$0")"
RUN="uv run --project ../minlp_solver_lab python"
sha256sum rowhull/*.py instances.py run_one.py sweep.py > results/code_version.sha256
$RUN sweep.py results/main_gurobi.jsonl --sizes 8x12 10x15 --seeds 0 1 2 3 4 --caps uniform random uncap --costs quad log sqrt --solvers gurobi --tl 300 --workers 8
$RUN sweep.py results/main_gurobi.jsonl --sizes g40n3d g60n3d --seeds 0 1 2 3 4 --caps uniform random --costs quad log --solvers gurobi --tl 300 --workers 8
$RUN sweep.py results/main_fc_gurobi.jsonl --sizes f8x12 f10x15 --seeds 0 1 2 3 4 --caps uniform random --costs quad log --solvers gurobi --tl 300 --workers 8
$RUN sweep.py results/main_others.jsonl --sizes 8x12 --seeds 0 1 2 3 4 --caps uniform random uncap --costs quad log --solvers scip baron --tl 300 --workers 30
$RUN sweep.py results/main_others.jsonl --sizes g40n3d --seeds 0 1 2 3 4 --caps uniform random --costs quad log --solvers scip baron --tl 300 --workers 30
echo finished
