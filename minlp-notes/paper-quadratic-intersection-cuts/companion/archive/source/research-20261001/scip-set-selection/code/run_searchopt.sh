#!/bin/bash
# search_optimality.py on the rule-1 dumps with dim(lambda) = 2 corners (40 corners, 720 angles), one process.
cd $(dirname $0)
for b in kall_circlespolygons_c1p11 st_e31 ex8_3_2 tln7 waterund08; do
  out=../logs/dumps/search_opt_$b.out
  [ -s $out ] && grep -q SUMMARY $out && continue
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 900 python3 search_optimality.py ../logs/dumps/$b.r1.jsonl.gz 40 40 720 > $out 2>&1
done
