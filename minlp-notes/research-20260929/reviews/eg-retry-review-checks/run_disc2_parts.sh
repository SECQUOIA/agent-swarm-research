#!/bin/bash
# eg_disc2_s run G, parts other than 1: record the tree (coverage check is complete) and
# independently certify the 2000 tightest closures plus a 10% random sample of all leaves.
# (Parts 2, 3, 4 were recorded by an earlier version of this script; their recordings are
# awaited here.)  Three slots run in parallel.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$(dirname "$0")"
TH=5.642100574331458
rec() { timeout 7200 python3 record_run.py eg_disc2_s 1e-9 7000 logs/rec_disc2_p$1.npz $1 8 > logs/rec_disc2_p$1.log 2>&1; }
ver() { until grep -q "^recorded" logs/rec_disc2_p$1.log 2>/dev/null; do sleep 20; done; sleep 5
        timeout 7200 python3 verify_tree.py logs/rec_disc2_p$1.npz eg_disc2_s $TH 0.1 $1 > logs/verify_disc2_p$1.log 2>&1; }
(ver 3; rec 5; ver 5) &
(ver 4; rec 0; ver 0) &
(ver 2; rec 6; ver 6; rec 7; ver 7) &
wait
