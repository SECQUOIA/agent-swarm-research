#!/bin/sh
# Extra diagnostic runs (one process): choice frequencies of the selection rules, and the
# next-vertex state reached by a SCIP round versus an orbit round from the same state.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python3 mrloop.py ../data/inst_6x8.json scip,orbit 20 ../logs/diag/swapgamma_6x8.jsonl 0 60 diag swapgamma > ../logs/diag/swapgamma_6x8.log 2>&1
python3 mrloop.py ../data/inst_6x8.json eff,oracle_seq,sumstep 20 ../logs/diag/choice_6x8.jsonl 0 30 diag > ../logs/diag/choice_6x8.log 2>&1
