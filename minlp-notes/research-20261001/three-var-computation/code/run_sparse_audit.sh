#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Triple-level audits of B on random plus, cactus and hard-triangle (ht) instances.
# At most 3 parallel processes, wall-clock limit 1 h per instance; skips finished instances.
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
for t in ht_plus_n30_k2_s1 ht_plus_n30_k3_s1 ht_plus_n60_k2_s1 ht_plus_n60_k3_s1 cactus_m30_s1 cactus_m30_s2 \
         plus_n100_k2_pp1_d5_s1 plus_n100_k2_pp1_d50_s1 plus_n100_k3_pp1_d5_s1 plus_n100_k3_pp1_d50_s1 \
         cactus_m100_s1 cactus_m100_s2 ht_plus_n300_k2_s1 ht_plus_n300_k3_s1 \
         plus_n300_k2_pp1_d5_s1 plus_n300_k2_pp1_d50_s1 plus_n300_k3_pp1_d5_s1 plus_n300_k3_pp1_d50_s1 \
         cactus_m300_s1 cactus_m300_s2 ht_plus_n1000_k2_s1 ht_plus_n1000_k3_s1 \
         plus_n1000_k2_pp1_d5_s1 plus_n1000_k2_pp1_d50_s1 plus_n1000_k3_pp1_d5_s1 plus_n1000_k3_pp1_d50_s1 \
         cactus_m1000_s1 cactus_m1000_s2 \
         plus_n3000_k2_pp1_d5_s1 plus_n3000_k2_pp1_d50_s1 plus_n3000_k3_pp1_d5_s1 plus_n3000_k3_pp1_d50_s1; do
  if [ ! -e ../logs/sparse_audit/$t.json ]; then echo $t; fi
done | OMP_NUM_THREADS=1 xargs -P 3 -I{} sh -c "timeout 3600 python sparse_audit.py ../data/{}.json ../logs/sparse_audit/{}.json > ../logs/sparse_audit/{}.out 2>&1"
