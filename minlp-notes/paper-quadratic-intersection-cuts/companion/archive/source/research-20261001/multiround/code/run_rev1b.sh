#!/bin/sh
# Revision after review round 1 (2026-10-02), second batch: control rule rnd0.33 (orbit set for a
# random third of the terms) on all four sizes, 20 rounds.  At most NPROC processes; every job has
# a 1-hour wall-clock limit (timeout).  Usage: sh run_rev1b.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
{
for i in 0 25; do echo "10x20 $i 25 rnd0.33"; done
for i in 0 25; do echo "8x12 $i 25 rnd0.33"; done
echo "6x8 0 60 rnd0.33"
echo "4x4 0 60 rnd0.33"
} | xargs -P "$1" -L 1 sh -c 'timeout 3600 python3 mrloop.py ../data/inst_$0.json $3 20 ../logs/rev1/rev1b_$0_$1.jsonl $1 $(($1+$2)) > ../logs/rev1/rev1b_$0_$1.log 2>&1; echo "$0 $1 exit $?" >> ../logs/rev1/done_b.txt'
