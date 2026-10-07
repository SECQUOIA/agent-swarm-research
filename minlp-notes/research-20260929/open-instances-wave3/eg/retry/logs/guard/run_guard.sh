#!/bin/bash
cd -- "$(dirname -- "$0")/../.." || exit
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
L=logs/guard
EG_ORDER=2 timeout 4000 python3 check_guard.py eg_int_s 1e-9 3600 > $L/int_1e-9_guard.log 2>&1 &
EG_ORDER=2 EGMODEL=ni timeout 9500 python3 check_guard.py eg_int_s 1e-9 9000 > $L/int_ni_1e-9_guard.log 2>&1 &
timeout 4000 python3 check_guard.py eg_int_s 1e-9 3600 > $L/int9_final_guard.log 2>&1 &
EGMODEL=ni timeout 9500 python3 check_guard.py eg_int_s 1e-9 9000 > $L/int9_ni3_guard.log 2>&1 &
for k in 0 1; do
  EG_ORDER=2 timeout 7600 python3 check_guard.py eg_disc_s 1e-6 7200 - - $k 2 > $L/disc_p${k}_guard.log 2>&1 &
  timeout 7600 python3 check_guard.py eg_disc_s 1e-9 7200 - - $k 2 > $L/disc9_p${k}_guard.log 2>&1 &
  EGMODEL=ni timeout 9500 python3 check_guard.py eg_disc_s 1e-9 9000 - - $k 2 > $L/disc9_ni3_p${k}_guard.log 2>&1 &
done
for k in 0 1 2 3 4 5 6 7; do
  timeout 7600 python3 check_guard.py eg_disc2_s 1e-9 7200 - - $k 8 > $L/disc2_9_p${k}_guard.log 2>&1 &
done
wait
echo ALL_DONE
