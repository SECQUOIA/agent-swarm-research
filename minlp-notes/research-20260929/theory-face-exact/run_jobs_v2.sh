#!/bin/bash
# Revision after review: the runs cited in the note, again with certified node bounds.
# Single-threaded BLAS (the machine is shared), 14 in parallel.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
xargs -P 14 -L 1 -I{} sh -c 'python3 bb_path.py {} 2>&1; true' < jobs_v2.txt | grep --line-buffered -v "Warning\|pr.solve" > logs/bb_runs_v2.log
