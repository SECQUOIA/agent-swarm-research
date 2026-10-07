#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Upper bounds by block coordinate descent, then XF runs (exact lift on family-selected triples).
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
for f in ../data/chain_m*.json; do
  t=$(basename $f .json)
  m=$(echo $t | sed 's/chain_m\([0-9]*\)_.*/\1/')
  if [ $m -le 100 ]; then ns=100; elif [ $m -le 300 ]; then ns=20; else ns=4; fi
  OMP_NUM_THREADS=1 python ub_local.py $f $ns 1 > ../logs/ub/$t.json 2>&1
done
for t in chain_m30_e0_s1 chain_m30_e0_s2 chain_m30_e0.3_s1 chain_m30_e0.3_s2 chain_m30_e1_s1 chain_m30_e1_s2 chain_m100_e0_s1 chain_m100_e0.3_s1 chain_m100_e0.3_s2 chain_m100_e1_s1 chain_m300_e0_s1 chain_m300_e0.3_s1 chain_m300_e0.3_s2 chain_m300_e1_s1 chain_m1000_e0.3_s1; do
  OMP_NUM_THREADS=1 python driver.py --json ../data/$t.json --methods XF --log ../logs/chain/xf_$t.jsonl --max_rounds 25 > ../logs/chain/xf_$t.out 2>&1
done
