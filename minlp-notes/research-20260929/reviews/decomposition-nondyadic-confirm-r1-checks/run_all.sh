#!/bin/sh
# Reruns E2, E3 and E4 (theta = 1/2 .. 1/32) with PAIR_TOL = 1e-12 (current code) and E2 with PAIR_TOL = 0.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
timeout 3000 python3 run_tol.py 1e-12 E2 > logs/E2_tol1e-12.log 2>&1
timeout 3000 python3 run_tol.py 0 E2 > logs/E2_tol0.log 2>&1
timeout 3000 python3 run_tol.py 1e-12 E3 > logs/E3_tol1e-12.log 2>&1
timeout 3000 python3 run_tol.py 1e-12 E4m5 > logs/E4m5_tol1e-12.log 2>&1
