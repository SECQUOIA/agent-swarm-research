#!/bin/bash
# sequential KAN runs (single-threaded); waits for the r5_n3 run to finish first
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
while pgrep -f "run_kan.py kan_r5_h1_n3" > /dev/null; do sleep 20; done
for n in kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9; do
  python3 -u run_kan.py $n 1e-10 1800 > ../logs/$n.bb.log 2>&1
done
for n in kan_r5_h1_n5 kan_r5_h1_n8; do
  python3 -u run_kan.py $n 1e-10 7200 > ../logs/$n.bb.log 2>&1
done
