#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
# Reviewer: run the independent box verifier on all 16 certificate files, 3 at a time, each with a time limit.
cd "${_PUBLIC_REPO}"/research-20261001/ratio-bound/reviews/r1-code
D=../../logs/zB_cert
L=../r1-logs/boxes
mkdir -p $L
jobs_list=(
"leaves_rho137.jsonl.gz 137 B"
"leaves_rho138.jsonl.gz 138 B"
"leaves_rho140.jsonl.gz 140 B"
"leaves_rho160.jsonl.gz 160 B"
"leaves_rho200.jsonl.gz 200 B"
"leaves_tan_eta1e-3_k4_rho197_200.jsonl.gz 197/200 tan:1/1000:4"
"leaves_tan_eta1e-3_k4_rho99_100.jsonl.gz 99/100 tan:1/1000:4"
"leaves_tan_eta1e-3_k4_rho1.jsonl.gz 1 tan:1/1000:4"
"leaves_tan_eta1e-3_k4_rho21_20.jsonl.gz 21/20 tan:1/1000:4"
"leaves_tan_eta1e-2_k4_rho5_4.jsonl.gz 5/4 tan:1/100:4"
"leaves_tan_eta1e-2_k4_rho13_10.jsonl.gz 13/10 tan:1/100:4"
"leaves_tan_eta1e-2_k4_rho3_2.jsonl.gz 3/2 tan:1/100:4"
"leaves_tan_eta1e-3_k9_4_rho21_20.jsonl.gz 21/20 tan:1/1000:9/4"
"leaves_tan_eta1e-3_k9_4_rho11_10.jsonl.gz 11/10 tan:1/1000:9/4"
"leaves_tan_eta1e-3_k9_4_rho6_5.jsonl.gz 6/5 tan:1/1000:9/4"
"leaves_tan_eta1e-3_k49_25_rho11_10.jsonl.gz 11/10 tan:1/1000:49/25"
)
for j in "${jobs_list[@]}"; do
  set -- $j
  base=${1%.jsonl.gz}
  while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 2; done
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 1500 python3 indep_verify_boxes.py $D/$1 $2 $3 > $L/$base.log 2>&1 &
done
wait
grep -H "INDEPENDENT CHECK" $L/*.log
