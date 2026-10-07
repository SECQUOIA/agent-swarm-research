#!/bin/sh
# Continuation runs (2026-10-02): state-versus-policy rules (oKs, sKo) and cheap selection rules
# (eff2, hybT).  At most NPROC processes; every job has a 2-hour wall-clock limit (timeout).
# Records are appended per instance, so an interrupted chunk can be resumed by rerunning the
# missing instances.  Usage: sh run_new.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
RA=o2s,o3s,o5s,s1o,s3o,s5o,eff2,hyb0.9,hyb0.5
RB=eff2,hyb0.9,hyb0.5
{
for i in 0 5 10 15 20 25 30 35 40 45; do echo "10x20 $i 5 $RA"; done
for i in 0 5 10 15 20 25 30 35 40 45 50 55; do echo "6x8 $i 5 $RA"; done
for i in 0 10 20 30 40; do echo "8x12 $i 10 $RB"; done
for i in 0 20 40; do echo "4x4 $i 20 $RB"; done
} | xargs -P "$1" -L 1 sh -c 'timeout 7200 python3 mrloop.py ../data/inst_$0.json $3 20 ../logs/new/new_$0_$1.jsonl $1 $(($1+$2)) > ../logs/new/new_$0_$1.log 2>&1; echo "$0 $1 exit $?" >> ../logs/new/done.txt'
