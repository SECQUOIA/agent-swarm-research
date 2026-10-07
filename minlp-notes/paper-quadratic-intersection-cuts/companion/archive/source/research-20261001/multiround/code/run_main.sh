#!/bin/sh
# Main comparison: 20 rounds; 60 instances (4x4, 6x8) or 50 instances (8x12, 10x20); chunks of 5.
# Usage: sh run_main.sh NPROC   (run from code/)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
RULES_S=scip,orbit_core,orbit,orbitB,corner,pert0.01,pert0.1,pert1,geo,pertE0.1,pertE1,lex0.1,alt,alt2,first_orbit,both,bothpert,oracle,oracle_seq,eff,depth,sumstep
RULES_L=scip,orbit_core,orbit,corner,pert0.1,pert1,geo,pertE0.1,pertE1,lex0.1,alt,alt2,first_orbit,both,bothpert,oracle,oracle_seq,eff,depth,sumstep
{
for i in 0 5 10 15 20 25 30 35 40 45 50 55; do echo "6x8 $i $RULES_S"; done
for i in 0 5 10 15 20 25 30 35 40 45; do echo "10x20 $i $RULES_L"; done
for i in 0 5 10 15 20 25 30 35 40 45; do echo "8x12 $i $RULES_S"; done
for i in 0 5 10 15 20 25 30 35 40 45 50 55; do echo "4x4 $i $RULES_S"; done
} | xargs -P "$1" -L 1 sh -c 'python3 mrloop.py ../data/inst_$0.json $2 20 ../logs/main/main_$0_$1.jsonl $1 $(($1+5)) > ../logs/main/main_$0_$1.log 2>&1'
