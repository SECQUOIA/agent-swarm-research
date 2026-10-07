#!/bin/bash
# Revision after review, final code (fixed secant upper bound, Clarabel fallback): the mc runs with kappa = 0.1.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
xargs -P 14 -L 1 -I{} sh -c 'python3 bb_path.py {} 2>&1; true' < jobs_v3.txt | grep --line-buffered -v "Warning\|pr.solve" > logs/bb_runs_v3_mc.log
