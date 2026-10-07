#!/bin/bash
# Gurobi bounds on z_K for records with rho >= 4: one process per instance group (120 s per record,
# checkpointed in logs/gurobi_zk_<group>.jsonl), then 40 validation records with known z_K (60 s).
cd "$(dirname "$0")"
run() { g=$1; shift; files=$(for i in "$@"; do ls ../logs/an_minlplib/$i.jsonl ../logs/an_minlplib2/$i.jsonl 2>/dev/null; done)
        OMP_NUM_THREADS=1 timeout 7000 python3 gurobi_zk.py ../logs/gurobi_zk_$g.jsonl 120 upper $files; }
run a nvs23 &
run tln tln12 &
run wu25 waterund25 &
run wu36 waterund36 &
run rest genpooling_meyer04 blend480 waterund32 &
wait
OMP_NUM_THREADS=1 timeout 3600 python3 gurobi_zk.py ../logs/gurobi_zk_validate.jsonl 60 validate:40 ../logs/an_minlplib/*.jsonl ../logs/an_minlplib2/*.jsonl
cat ../logs/gurobi_zk_a.jsonl ../logs/gurobi_zk_tln.jsonl ../logs/gurobi_zk_wu25.jsonl ../logs/gurobi_zk_wu36.jsonl ../logs/gurobi_zk_rest.jsonl > ../logs/gurobi_zk.jsonl
echo GUROBIDONE
