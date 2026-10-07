#!/bin/bash
# Rerun of the sfree note's exp_loop.py with z_K from zk_fast (2 processes, 1 h limit each).
cd "$(dirname "$0")"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 3600 python3 exp_loop_fixedzk.py 21 30 8 ../logs/exp_loop_small_fixedzk.json > ../logs/exp_loop_small_fixedzk.log 2>&1 &
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 3600 python3 exp_loop_fixedzk.py 22 30 10 ../logs/exp_loop_big_fixedzk.json 6 8 4 > ../logs/exp_loop_big_fixedzk.log 2>&1 &
wait
echo LOOPSDONE
