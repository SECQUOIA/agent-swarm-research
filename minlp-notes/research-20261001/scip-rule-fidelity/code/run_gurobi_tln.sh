#!/bin/bash
# tln12 records with rho >= 4 in 6 shards (120 s per record), skipping records already in
# logs/gurobi_zk_tln.jsonl; merged into logs/gurobi_zk.jsonl at the end.
cd "$(dirname "$0")"
F="../logs/an_minlplib/tln12.jsonl ../logs/an_minlplib2/tln12.jsonl"
for r in 0 1 2 3 4 5; do
  SHARD=$r/6 DONE_FILES=../logs/gurobi_zk_tln.jsonl OMP_NUM_THREADS=1 timeout 5400 \
    python3 gurobi_zk.py ../logs/gurobi_zk_tln_s$r.jsonl 120 upper $F &
done
wait
cat ../logs/gurobi_zk_a.jsonl ../logs/gurobi_zk_tln*.jsonl ../logs/gurobi_zk_wu25.jsonl ../logs/gurobi_zk_wu36.jsonl ../logs/gurobi_zk_rest.jsonl > ../logs/gurobi_zk.jsonl
echo TLNDONE
