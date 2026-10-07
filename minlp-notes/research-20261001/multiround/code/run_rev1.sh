#!/bin/sh
# Revision after review round 1 (2026-10-02): rule first_orbit (= o1s) on 8x12 and 10x20, and the
# new rule maj2 on all four sizes, 20 rounds.  At most NPROC processes (3 were used, leaving one slot for analyses under the cap of 4); every job has a 1-hour
# wall-clock limit (timeout).  Records are appended per instance, so an interrupted chunk can be
# resumed by rerunning the missing instances.  Usage: sh run_rev1.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
{
for i in 0 10 20 30 40; do echo "10x20 $i 10 first_orbit,maj2"; done
for i in 0 10 20 30 40; do echo "8x12 $i 10 first_orbit,maj2"; done
for i in 0 30; do echo "6x8 $i 30 maj2"; done
echo "4x4 0 60 maj2"
} | xargs -P "$1" -L 1 sh -c 'timeout 3600 python3 mrloop.py ../data/inst_$0.json $3 20 ../logs/rev1/rev1_$0_$1.jsonl $1 $(($1+$2)) > ../logs/rev1/rev1_$0_$1.log 2>&1; echo "$0 $1 exit $?" >> ../logs/rev1/done.txt'
